import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "validate_bundle.py"
TEMPLATE = SKILL_DIR / "templates" / "bundle"


class ValidateBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.bundle = Path(self.temp_dir.name) / "bundle"
        shutil.copytree(TEMPLATE, self.bundle)
        self._fill_template_tokens()

    def _fill_template_tokens(self):
        statuses = {"active": 0, "partial": 0, "scaffold": 0}
        for path in self.bundle.rglob("*.md"):
            text = path.read_text()
            for status in statuses:
                statuses[status] += len(re.findall(rf"(?m)^status:\s*{status}\s*$", text))

        replacements = {
            "CLIENT_NAME": "Example Client",
            "ONBOARDING_DATE": "2026-08-10",
            "SOURCES_LIST": "operator interview",
            "N_ACTIVE": str(statuses["active"]),
            "N_PARTIAL": str(statuses["partial"]),
            "N_SCAFFOLD": str(statuses["scaffold"]),
            "GAP_DISPOSITIONS": "1 closed",
            "GAP_LEDGER_ROWS": (
                "| D7 | d-books/materiality-thresholds.md | closed | Pat | "
                "2026-08-10 | answered in interview |"
            ),
        }

        for path in self.bundle.rglob("*.md"):
            text = path.read_text()
            text = re.sub(
                r"\{\{([^}]+)\}\}",
                lambda match: replacements.get(match.group(1), "filled"),
                text,
            )
            path.write_text(text)

    def _run_validator(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.bundle), "--template", str(TEMPLATE)],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout + result.stderr

    def _replace_ledger_row(self, replacement):
        path = self.bundle / "0-core" / "log.md"
        text = path.read_text()
        text = re.sub(r"(?m)^\| D7 \|.*\|$", replacement, text)
        path.write_text(text)

    def _set_active_body(self, relative_path, body):
        path = self.bundle / relative_path
        text = path.read_text().replace("status: scaffold", "status: active", 1)
        frontmatter_end = text.find("\n---\n", 4)
        self.assertNotEqual(frontmatter_end, -1)
        path.write_text(text[:frontmatter_end + 5] + body)

    def test_01_baseline_filled_template_passes(self):
        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 0, output)
        self.assertIn("PASS: 0 errors", output)

    def test_02_missing_template_file_fires_e9(self):
        (self.bundle / "f-annual" / "year-end-close.md").unlink()
        index_path = self.bundle / "f-annual" / "index.md"
        index_path.write_text(
            "\n".join(
                line for line in index_path.read_text().splitlines()
                if "year-end-close.md" not in line
            ) + "\n"
        )
        qbo_path = self.bundle / "d-books" / "qbo-configuration.md"
        qbo_path.write_text(
            qbo_path.read_text().replace(
                "[year-end close](/f-annual/year-end-close.md)",
                "year-end close",
            )
        )

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 1, output)
        self.assertIn("E9 | f-annual/year-end-close.md", output)

    def test_03_active_file_with_tbd_fires_e10(self):
        self._set_active_body(
            "a-identity/profile.md",
            "# Identity\n\nThe legal name is TBD.\n\n# Citations\n\n[1] Pat, 2026-08-10.\n",
        )

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 1, output)
        self.assertIn("E10 | a-identity/profile.md", output)

    def test_04_active_file_with_only_tbd_citation_fires_e11(self):
        self._set_active_body(
            "a-identity/profile.md",
            "# Identity\n\nExample Client.\n\n# Citations\n\n[1] TBD\n",
        )

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 1, output)
        self.assertIn("E11 | a-identity/profile.md", output)

    def test_05_anonymous_bulk_ledger_gap_fires_e12(self):
        self._replace_ledger_row(
            "| 9 further items | — | deferred | Pat | 2026-08-10 | parked |"
        )

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 1, output)
        self.assertIn("E12 | 0-core/log.md", output)
        self.assertIn("anonymous bulk Gap", output)

    def test_06_bad_ledger_disposition_fires_e12(self):
        self._replace_ledger_row(
            "| D7 | d-books/materiality-thresholds.md | parked | Pat | 2026-08-10 | parked |"
        )

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 1, output)
        self.assertIn("E12 | 0-core/log.md", output)
        self.assertIn("invalid disposition: parked", output)

    def test_07_blocked_ledger_row_without_dependency_fires_e12(self):
        self._replace_ledger_row(
            "| D7 | d-books/materiality-thresholds.md | blocked | Pat | 2026-08-10 | |"
        )

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 1, output)
        self.assertIn("E12 | 0-core/log.md", output)
        self.assertIn("blocked disposition requires Dependency/reason", output)

    def test_08_wrong_log_counts_warn_without_failing(self):
        path = self.bundle / "0-core" / "log.md"
        text = re.sub(
            r"\d+ active, \d+ partial, \d+ scaffold",
            "99 active, 98 partial, 97 scaffold",
            path.read_text(),
            count=1,
        )
        path.write_text(text)

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 0, output)
        self.assertIn("W5 | 0-core/log.md", output)
        self.assertIn("add a dated log entry reflecting current statuses", output)

    def test_09_non_markdown_file_warns(self):
        (self.bundle / "data.csv").write_text("account,balance\nCash,100\n")

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 0, output)
        self.assertIn("W6 | data.csv", output)

    def test_10_legacy_root_log_still_fires_e2_and_e8(self):
        shutil.move(self.bundle / "0-core" / "log.md", self.bundle / "log.md")

        exit_code, output = self._run_validator()

        self.assertEqual(exit_code, 1, output)
        self.assertIn("E2 | root-level log.md", output)
        self.assertIn("E8 | log.md", output)


if __name__ == "__main__":
    unittest.main()
