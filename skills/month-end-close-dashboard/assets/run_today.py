"""
Date-aware launcher for the Paxus month-end close.

Run this from the "Paxus Close" shortcut on the Desktop whenever Google Calendar
pings you about a checkpoint or email-draft date. It figures out what should
happen today (dashboard refresh, email draft, or both) and runs it.

If nothing is scheduled for today, it prints the next few upcoming events.

Usage:
    python run_today.py
    python run_today.py --date 2026-06-25      # pretend today is that date
    python run_today.py --dry-run              # show actions, don't execute
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from schedule_checkpoints import (  # noqa: E402
    federal_holidays,
    compute_checkpoints,
    close_period_for_run_month,
)

PYTHON_EXE = Path(sys.executable)
BUILD_SCRIPT = SCRIPT_DIR / "build_dashboard.py"
EMAIL_SCRIPT = SCRIPT_DIR / "compose_close_email.py"
CHECKPOINT_EMAIL_SCRIPT = SCRIPT_DIR / "compose_checkpoint_email.py"
DASHBOARD_HTML = SCRIPT_DIR / "project" / "dashboard.html"
EMAIL_DRAFT_DAY = 25

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def actions_for(d: date) -> list[dict]:
    """Return a list of {label, cmd, post} dicts for everything scheduled on d.

    `post` is an optional callable to run after the command succeeds (e.g. open
    the dashboard in a browser, open the email draft in Notepad).
    """
    actions: list[dict] = []

    holidays = federal_holidays(d.year)
    if d.month == 12:
        holidays |= federal_holidays(d.year + 1)
    period = close_period_for_run_month(d.replace(day=1))

    for cp_day, _target, shifted in compute_checkpoints(d.year, d.month, holidays):
        if shifted == d:
            actions.append({
                "label": f"Dashboard refresh — close period {period}, checkpoint cp{cp_day}",
                "cmd": [str(PYTHON_EXE), str(BUILD_SCRIPT),
                        "--period", period, "--checkpoint", str(cp_day), "--record"],
                "post": open_dashboard,
            })
            actions.append({
                "label": f"Checkpoint status email draft — cp{cp_day}",
                "cmd": [str(PYTHON_EXE), str(CHECKPOINT_EMAIL_SCRIPT),
                        "--checkpoint", str(cp_day)],
                "post": open_checkpoint_email_draft,
            })

    if d.day == EMAIL_DRAFT_DAY:
        close_period = f"{d.year:04d}-{d.month:02d}"
        actions.append({
            "label": f"Close-timeline email draft — for {close_period} close",
            "cmd": [str(PYTHON_EXE), str(EMAIL_SCRIPT), "--close", close_period],
            "post": open_email_draft,
        })

    return actions


def open_dashboard() -> None:
    if DASHBOARD_HTML.exists():
        os.startfile(str(DASHBOARD_HTML))
        print(f"  → opened {DASHBOARD_HTML.name} in browser")


def _candidate_dirs() -> list[Path]:
    home = Path.home()
    return [home / "Downloads", home / "OneDrive" / "Desktop", home / "Desktop"]


def open_email_draft() -> None:
    for d in _candidate_dirs():
        if not d.is_dir():
            continue
        drafts = sorted(d.glob("Close Timeline Email - *.txt"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
        if drafts:
            os.startfile(str(drafts[0]))
            print(f"  → opened {drafts[0].name}")
            return


def open_checkpoint_email_draft() -> None:
    for d in _candidate_dirs():
        if not d.is_dir():
            continue
        drafts = sorted(d.glob("Checkpoint Email cp*.txt"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
        if drafts:
            os.startfile(str(drafts[0]))
            print(f"  → opened {drafts[0].name}")
            return


def upcoming(start: date, count: int = 6) -> list[tuple[date, str]]:
    events: list[tuple[date, str]] = []
    cursor = start
    while len(events) < count and (cursor - start).days <= 120:
        for a in actions_for(cursor):
            events.append((cursor, a["label"]))
            if len(events) >= count:
                break
        cursor += timedelta(days=1)
    return events


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--date", help="Override today's date (YYYY-MM-DD) for testing")
    parser.add_argument("--dry-run", action="store_true", help="Show actions, don't execute")
    args = parser.parse_args()

    today = date.fromisoformat(args.date) if args.date else date.today()
    actions = actions_for(today)

    print(f"Today: {today.strftime('%A, %B %d, %Y')}")
    print()

    if not actions:
        print("Nothing scheduled for today.")
        print()
        print("Upcoming Paxus close events:")
        for d, lbl in upcoming(today + timedelta(days=1)):
            print(f"  {d.strftime('%a %b %d')}  —  {lbl}")
        return 0

    print(f"{len(actions)} action(s) for today:")
    for a in actions:
        print(f"  • {a['label']}")
    print()

    if args.dry_run:
        print("[DRY RUN — nothing executed]")
        return 0

    failed = 0
    for a in actions:
        print(f"=== {a['label']} ===")
        rc = subprocess.run(a["cmd"]).returncode
        if rc != 0:
            print(f"  !! exited with code {rc}")
            failed += 1
        elif a.get("post"):
            try:
                a["post"]()
            except Exception as e:
                print(f"  (post-step skipped: {e})")
        print()

    if failed == 0:
        print(f"Done — {len(actions)} action(s) completed.")
    else:
        print(f"Done — {len(actions) - failed} succeeded, {failed} failed.")
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
