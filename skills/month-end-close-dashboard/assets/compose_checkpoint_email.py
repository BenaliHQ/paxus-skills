"""
Generate the per-checkpoint status email for the Paxus team.

Each checkpoint highlights different information:
  cp5  — bank statements / reconciliations milestone
  cp10 — staff→lead handoff; clients still needing reconciliation
  cp15 — lead→controller handoff; top reviewers
  cp20 — final-review controllers; lead-queue stragglers
  cp25 — final wrap; remaining open items

Data sources:
  - project/close-data.js — current checkpoint counts and stage tables
  - project/uploads/*.csv  — Financial Cents exports (used for assignee data
    because the FC `/projects` API doesn't return assignees by default)

The script writes a plain-text draft to the Desktop. Jennifer reviews, pastes
into Gmail, and sends to the Paxus team distribution group. The script never
sends.

Usage:
    python compose_checkpoint_email.py --checkpoint 25
    python compose_checkpoint_email.py --checkpoint 25 --stdout
    python compose_checkpoint_email.py --checkpoint 25 --out my-draft.txt
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "project" / "close-data.js"
UPLOADS_DIR = SCRIPT_DIR / "project" / "uploads"
CHECKPOINT_KEYS = {5: "5th", 10: "10th", 15: "15th", 20: "20th", 25: "25th"}

DASHBOARD_URL = (
    "https://claude.ai/design/p/c9f5e7a2-8e99-42eb-b911-a399f0dd7284"
    "?file=Paxus+Close+Dashboard.dc.html"
)

CSV_STAGES = ["staff", "lead", "controller", "closed", "staffquarterly closed"]

# Interns share the "Paxus Intern" assignee in FC. Their actual identity is
# encoded in the Client Groups field as "<Name>'s Clients" — same convention
# used for the named staff. Credit each intern individually.
INTERN_NAMES = ["Kaitlyn", "Macie", "Jenny"]


def find_default_outdir() -> Path:
    """Downloads is more reliable than the OneDrive Desktop, which sometimes
    hides newly-written files from Explorer until OneDrive resolves them."""
    home = Path.home()
    downloads = home / "Downloads"
    if downloads.is_dir():
        return downloads
    od = home / "OneDrive" / "Desktop"
    return od if od.is_dir() else home / "Desktop"


def intern_from_groups(row: dict) -> str | None:
    """If the row belongs to a specific intern, return that intern's name."""
    groups = row.get("Client Groups") or ""
    for name in INTERN_NAMES:
        if f"{name}'s Clients" in groups:
            return name
    return None


def load_close_data() -> dict:
    if not DATA_PATH.exists():
        sys.exit(f"close-data.js not found at {DATA_PATH}")
    text = DATA_PATH.read_text(encoding="utf-8")
    m = re.search(r"window\.PAXUS_CLOSE\s*=\s*(\{.*\})\s*;\s*$", text, re.DOTALL)
    if not m:
        sys.exit(f"could not parse {DATA_PATH}")
    return json.loads(m.group(1))


def read_stage_csv(name: str) -> list[dict]:
    p = UPLOADS_DIR / f"{name}.csv"
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def all_csv_rows() -> list[dict]:
    rows = []
    for name in CSV_STAGES:
        rows.extend(read_stage_csv(name))
    return rows


def assignees_of(row: dict) -> list[str]:
    return [a.strip() for a in (row.get("Assignees") or "").split(";") if a.strip()]


def title_norm(row: dict) -> str:
    return re.sub(r"^\*+", "", row.get("Project Title", "") or "").strip()


def is_review(row: dict) -> bool:
    return "Review" in title_norm(row)


def is_close(row: dict) -> bool:
    return "Month End Close" in title_norm(row)


def tally(rows: list[dict], filt=None, top: int | None = 5) -> list[tuple[str, int]]:
    c: Counter[str] = Counter()
    for r in rows:
        if filt and not filt(r):
            continue
        for a in assignees_of(r):
            if a == "Paxus Intern":
                intern = intern_from_groups(r)
                if intern:
                    c[intern] += 1
                    continue
            c[a] += 1
    items = c.most_common(top) if top else c.most_common()
    return items


def get_checkpoint(D: dict, cp_key: str) -> dict:
    for cp in D.get("checkpoints", []):
        if cp.get("key") == cp_key:
            return cp
    return {}


def pipeline_breakdown(D: dict, cp_key: str) -> str:
    cp = get_checkpoint(D, cp_key)
    if not cp:
        return ""
    rows = [
        ("Staff (Open)", cp.get("staff", 0), "Reconciliation In Progress"),
        ("Lead", cp.get("lead", 0), "In Lead Review"),
        ("Controller", cp.get("controller", 0), "In Final Review"),
        ("Closed (incl. SQC)", cp.get("closed", 0), "Fully Closed"),
    ]
    total = sum(r[1] for r in rows)
    lines = [f"{'STAGE':<22s} {'COUNT':>6s}   {'OF TOTAL':>9s}   STATUS"]
    lines.append("-" * 70)
    for name, count, status in rows:
        pct = (count / total * 100) if total else 0
        lines.append(f"{name:<22s} {count:>6d}   {pct:>8.1f}%   {status}")
    lines.append("-" * 70)
    lines.append(f"{'TOTAL':<22s} {total:>6d}   {'100.0%':>9s}")
    return "\n".join(lines)


def stage_clients(D: dict, stage: str) -> list[str]:
    return [r[0] for r in (D.get(stage) or [])]


def joiner(top: list[tuple[str, int]]) -> str:
    return ", ".join(f"{n} ({c})" for n, c in top)


def compose(checkpoint_day: int) -> tuple[str, str]:
    D = load_close_data()
    cp_key = CHECKPOINT_KEYS[checkpoint_day]
    close_month = D.get("closeMonth", "")
    cp = get_checkpoint(D, cp_key)
    cp_total = sum([cp.get(k, 0) for k in ("staff", "lead", "controller", "closed")])
    cp_closed = cp.get("closed", 0)
    pct_closed = (cp_closed / cp_total * 100) if cp_total else 0

    all_rows = all_csv_rows()
    staff_csv = read_stage_csv("staff")
    lead_csv = read_stage_csv("lead")
    controller_csv = read_stage_csv("controller")
    closed_csv = read_stage_csv("closed")

    # Rows representing projects that have moved out of the staff stage
    past_staff = lead_csv + controller_csv + closed_csv + read_stage_csv("staffquarterly closed")

    subject = f"Re: Month-End Close Dashboard"
    parts: list[str] = []
    parts.append(f"Subject: {subject}")
    parts.append("")
    parts.append("Here is our Month-End Dashboard for your review:")
    parts.append(DASHBOARD_URL)
    parts.append("")

    if checkpoint_day == 5:
        parts.append(
            f"The 5th is our target for reconciliations — bank statements pulled "
            f"and accounts reconciled."
        )
        parts.append("")
        top = tally(past_staff, filt=is_close, top=3)
        if top:
            parts.append("Recognition — top reconciliations completed so far:")
            for name, n in top:
                parts.append(f"  • {name} — {n}")
            parts.append("")

    elif checkpoint_day == 10:
        top_staff = tally(past_staff, filt=is_close, top=1)
        top_lead = tally(closed_csv, filt=is_review, top=1)
        stragglers = stage_clients(D, "staff")
        parts.append("• The 10th is our target date for submitting all work to the leads for review.")
        parts.append("• REMINDER: Month-End Close projects must be manually closed.")
        if top_staff:
            n_completed = top_staff[0][1]
            parts.append(f"• Great job, {top_staff[0][0]}! You have completed {n_completed} month-end closes so far!")
        if top_lead:
            parts.append(f"• {top_lead[0][0]} is the lead who has completed the most reviews!")
        if stragglers:
            parts.append(f"• {len(stragglers)} clients still need reconciliation.")
        parts.append("")
        if stragglers:
            parts.append("Client Name")
            for name in stragglers:
                parts.append(f"  {name}")
            parts.append("")

    elif checkpoint_day == 15:
        opener = (
            f"Great job everyone — over half of the projects are now closed! "
            f"As a reminder, the 15th was the target date for all reviews to be "
            f"submitted to the controllers."
        ) if pct_closed >= 50 else (
            f"Reminder: the 15th is the target date for all reviews to be "
            f"submitted to the controllers."
        )
        parts.append(opener)
        parts.append("")
        top_reviewers = tally(closed_csv, filt=is_review, top=5)
        if top_reviewers:
            parts.append("Excellence Spotlight — Reviews Closed:")
            for i, (name, n) in enumerate(top_reviewers, 1):
                parts.append(f"  {i}. {name} — {n}")
            parts.append("")

    elif checkpoint_day == 20:
        parts.append("Hello, Team!")
        parts.append("")
        parts.append(f"We have {pct_closed:.0f}% closed at this point.")
        parts.append("")
        parts.append("★ Excellence Spotlight — Controllers + Leads")
        parts.append("")
        in_final = tally(controller_csv, top=None)
        if in_final:
            parts.append("In Final Review — by Controller:")
            for name, n in in_final:
                parts.append(f"  • {name} — {n}")
            parts.append("")
        reviews_done = tally(closed_csv, filt=is_review, top=5)
        if reviews_done:
            parts.append("Reviews Completed — credited:")
            for name, n in reviews_done:
                parts.append(f"  • {name} — {n}")
            parts.append("")
        lead_queue = tally(lead_csv, top=None)
        if lead_queue:
            parts.append("⚠ Still in lead queue: " + joiner(lead_queue))
            parts.append("")

    elif checkpoint_day == 25:
        open_count = cp_total - cp_closed
        if open_count == 0:
            parts.append(f"The {close_month} close is complete — every project closed!")
        else:
            parts.append(
                f"We're wrapping up the {close_month} close: "
                f"{cp_closed} of {cp_total} closed ({pct_closed:.1f}%), "
                f"with {open_count} still open."
            )
        parts.append("")
        # Final stragglers list
        if open_count > 0:
            parts.append("Still open:")
            for name in stage_clients(D, "staff"):
                parts.append(f"  • {name} (with staff)")
            for name in stage_clients(D, "lead"):
                parts.append(f"  • {name} (with lead)")
            for name in stage_clients(D, "controller"):
                parts.append(f"  • {name} (with controller)")
            parts.append("")
        # Top closers — staff with most closes moved past them
        top_staff = tally(past_staff, filt=is_close, top=5)
        if top_staff:
            parts.append("Recognition — month-end closes completed this cycle:")
            for name, n in top_staff:
                parts.append(f"  • {name} — {n}")
            parts.append("")

    parts.append("PIPELINE BREAKDOWN")
    parts.append(pipeline_breakdown(D, cp_key))
    parts.append("")

    return subject, "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--checkpoint", type=int, required=True, choices=[5, 10, 15, 20, 25])
    parser.add_argument("--out", help="Output file path")
    parser.add_argument("--stdout", action="store_true", help="Print, don't write a file")
    args = parser.parse_args()

    subject, body = compose(args.checkpoint)

    if args.stdout:
        sys.stdout.write(body)
        return 0

    D = load_close_data()
    close_month = (D.get("closeMonth") or "Close").replace(" ", "_")
    fname = f"Checkpoint Email cp{args.checkpoint} - {close_month}.txt"
    out_path = Path(args.out) if args.out else (find_default_outdir() / fname)
    out_path.write_text(body, encoding="utf-8")
    print(f"Wrote draft email: {out_path}")
    print()
    print("Review, paste into Gmail, send to the Paxus team.")
    try:
        os.startfile(str(out_path))
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
