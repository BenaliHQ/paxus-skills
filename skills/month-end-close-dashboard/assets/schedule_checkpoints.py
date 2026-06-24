"""
Paxus close-dashboard checkpoint helpers (date logic shared across scripts).

WHAT'S ACTIVE:
    Helper functions — federal_holidays(), is_business_day(),
    shift_for_checkpoint(), compute_checkpoints(), close_period_for_run_month().
    These are imported by run_today.py and generate_calendar.py.

WHAT'S DEPRECATED:
    The schtasks-based registration functions (register_checkpoint_task,
    register_monthly_scheduler, register_email_draft_task) and the CLI in
    main(). The Paxus EDR blocked all scheduled-task creation that referenced
    scripts in this folder (Access is denied), so this approach was abandoned
    on 2026-06-24.

    The current scheduling system is:
      • generate_calendar.py → emits a Google Calendar .ics with reminders
      • run_today.py        → date-aware launcher invoked by a Desktop .bat
                              when Calendar pings Jennifer

    The schtasks code is kept here only so a teammate can see the prior
    approach and what was tried; it is not invoked anywhere.
"""
from __future__ import annotations
import argparse
import calendar
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# === Configuration ===
SCRIPT_DIR = Path(__file__).resolve().parent
BUILD_SCRIPT = SCRIPT_DIR / "build_dashboard.py"
EMAIL_SCRIPT = SCRIPT_DIR / "compose_close_email.py"
PYTHON_EXE = Path(sys.executable)
TASK_PREFIX = "PaxusClose"  # Flat name prefix (avoids needing admin to create folder)
RUN_HOUR = 15  # 3 PM
RUN_MINUTE = 0
CHECKPOINT_DAYS = [5, 10, 15, 20, 25]


# === US federal holidays (Paxus-observed set) ===
def nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """Nth (1-5) occurrence of weekday (Mon=0..Sun=6) in month/year."""
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return date(year, month, 1 + offset + 7 * (n - 1))


def last_weekday(year: int, month: int, weekday: int) -> date:
    last_day = calendar.monthrange(year, month)[1]
    d = date(year, month, last_day)
    offset = (d.weekday() - weekday) % 7
    return date(year, month, last_day - offset)


def federal_holidays(year: int) -> set[date]:
    """Paxus-observed holidays (7 total). Per Jennifer: no MLK/Presidents Day,
    no Juneteenth, no Day-after-Thanksgiving."""
    h: set[date] = set()
    h.add(date(year, 1, 1))                          # New Year's Day
    h.add(last_weekday(year, 5, 0))                  # Memorial Day (last Mon May)
    h.add(date(year, 7, 4))                          # Independence Day
    h.add(nth_weekday(year, 9, 0, 1))                # Labor Day (1st Mon Sep)
    h.add(nth_weekday(year, 11, 3, 4))               # Thanksgiving (4th Thu Nov)
    h.add(date(year, 12, 24))                        # Christmas Eve
    h.add(date(year, 12, 25))                        # Christmas Day
    # Observed shifting: Sat → prior Fri, Sun → next Mon
    observed: set[date] = set()
    for d in list(h):
        if d.weekday() == 5:
            observed.add(d - timedelta(days=1))
        elif d.weekday() == 6:
            observed.add(d + timedelta(days=1))
    return h | observed


def is_business_day(d: date, holidays: set[date]) -> bool:
    return d.weekday() < 5 and d not in holidays


def shift_back_to_business_day(d: date, holidays: set[date]) -> date:
    while not is_business_day(d, holidays):
        d -= timedelta(days=1)
    return d


def shift_forward_to_business_day(d: date, holidays: set[date]) -> date:
    while not is_business_day(d, holidays):
        d += timedelta(days=1)
    return d


def shift_for_checkpoint(cp_day: int, target: date, holidays: set[date]) -> date:
    """20th = delivery deadline (shift backward so clients get statements before
    the weekend). All other checkpoints (5/10/15/25) = milestones (shift forward
    so the team has the next business day to hit them)."""
    if cp_day == 20:
        return shift_back_to_business_day(target, holidays)
    return shift_forward_to_business_day(target, holidays)


# === Close period and checkpoint computation ===
def close_period_for_run_month(run_month_first: date) -> str:
    """The close period worked on during this calendar month = previous month."""
    prev = run_month_first - timedelta(days=1)
    return f"{prev.year:04d}-{prev.month:02d}"


def compute_checkpoints(run_year: int, run_month: int, holidays: set[date]) -> list[tuple[int, date, date]]:
    """Return [(checkpoint_day, target_date, shifted_date), ...] for each checkpoint."""
    out = []
    for cp in CHECKPOINT_DAYS:
        try:
            target = date(run_year, run_month, cp)
        except ValueError:
            continue
        shifted = shift_for_checkpoint(cp, target, holidays)
        out.append((cp, target, shifted))
    return out


# === schtasks helpers ===
def run_schtasks(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result.returncode, result.stdout or "", result.stderr or ""


def register_checkpoint_task(period: str, cp_day: int, run_date: date, dry_run: bool) -> bool:
    task_name = f"{TASK_PREFIX}-{period}-cp{cp_day}"
    cmd_line = f'"{PYTHON_EXE}" "{BUILD_SCRIPT}" --period {period} --checkpoint {cp_day} --record'
    sd = run_date.strftime("%m/%d/%Y")
    st = f"{RUN_HOUR:02d}:{RUN_MINUTE:02d}"
    pretty = f"{run_date.strftime('%a %b %d')} {st}"
    if dry_run:
        print(f"  [DRY] {task_name:<40s}  →  {pretty}")
        return True
    rc, out, err = run_schtasks([
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", cmd_line,
        "/sc", "once",
        "/sd", sd,
        "/st", st,
        "/f",
    ])
    if rc != 0:
        print(f"  !! {task_name}: {err.strip()}")
        return False
    print(f"  OK {task_name:<40s}  →  {pretty}")
    return True


def register_monthly_scheduler(dry_run: bool) -> None:
    task_name = f"{TASK_PREFIX}-Scheduler-Monthly"
    cmd_line = f'"{PYTHON_EXE}" "{Path(__file__).resolve()}"'
    if dry_run:
        print(f"  [DRY] {task_name}  →  monthly, day 1, 09:00")
        return
    rc, out, err = run_schtasks([
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", cmd_line,
        "/sc", "MONTHLY",
        "/d", "1",
        "/st", "09:00",
        "/f",
    ])
    if rc != 0:
        print(f"  !! {task_name}: {err.strip()}")
    else:
        print(f"  OK {task_name}  →  monthly, day 1, 09:00")


def register_email_draft_task(dry_run: bool) -> None:
    """Monthly recurring task: drops the close-timeline email draft on Jennifer's
    Desktop on the 25th of each month at 9 AM (last week of the month)."""
    task_name = f"{TASK_PREFIX}-EmailDraft-Monthly"
    cmd_line = f'"{PYTHON_EXE}" "{EMAIL_SCRIPT}"'
    if dry_run:
        print(f"  [DRY] {task_name}  →  monthly, day 25, 09:00")
        return
    rc, out, err = run_schtasks([
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", cmd_line,
        "/sc", "MONTHLY",
        "/d", "25",
        "/st", "09:00",
        "/f",
    ])
    if rc != 0:
        print(f"  !! {task_name}: {err.strip()}")
    else:
        print(f"  OK {task_name}  →  monthly, day 25, 09:00")


def list_tasks() -> None:
    rc, out, err = run_schtasks(["schtasks", "/query", "/fo", "LIST", "/v"])
    if rc != 0:
        print(err)
        return
    blocks = out.split("\n\n")
    relevant = [b for b in blocks if f"\\{TASK_PREFIX}-" in b]
    if not relevant:
        print("(no Paxus close tasks registered)")
        return
    for b in relevant:
        # Extract a few key fields for a tidier view
        lines = [ln for ln in b.splitlines() if any(
            ln.startswith(k) for k in ("TaskName:", "Next Run Time:", "Status:", "Task To Run:")
        )]
        print("\n".join(lines))
        print("---")


def unregister_all() -> None:
    """Delete every Paxus\\Close-* task."""
    rc, out, err = run_schtasks(["schtasks", "/query", "/fo", "CSV", "/nh"])
    if rc != 0:
        print(err)
        return
    import csv
    import io
    deleted = 0
    for row in csv.reader(io.StringIO(out)):
        if not row:
            continue
        name = row[0]
        if name.startswith(f"\\{TASK_PREFIX}-"):
            rc2, _, e2 = run_schtasks(["schtasks", "/delete", "/tn", name, "/f"])
            if rc2 == 0:
                print(f"  deleted {name}")
                deleted += 1
            else:
                print(f"  !! could not delete {name}: {e2.strip()}")
    print(f"\ntotal deleted: {deleted}")


# === Main ===
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--setup", action="store_true",
                        help="Also register the monthly recurring scheduler (first-time setup).")
    parser.add_argument("--month", help="Override run month YYYY-MM. Default: current month.")
    parser.add_argument("--print", dest="dry_run", action="store_true",
                        help="Preview without creating tasks.")
    parser.add_argument("--list", action="store_true",
                        help="Show currently registered Paxus close tasks.")
    parser.add_argument("--unregister-all", action="store_true",
                        help="Delete every Paxus\\Close-* task.")
    args = parser.parse_args()

    if args.list:
        list_tasks()
        return 0
    if args.unregister_all:
        unregister_all()
        return 0

    if not BUILD_SCRIPT.exists():
        sys.exit(f"build_dashboard.py not found at {BUILD_SCRIPT}")

    today = date.today()
    if args.month:
        try:
            yr, mo = (int(x) for x in args.month.split("-"))
            run_month_start = date(yr, mo, 1)
        except (ValueError, TypeError):
            sys.exit(f"--month must be YYYY-MM, got: {args.month!r}")
    else:
        run_month_start = today.replace(day=1)

    period = close_period_for_run_month(run_month_start)
    print(f"Run month:      {run_month_start.strftime('%B %Y')}")
    print(f"Close period:   {period}")
    print(f"Python:         {PYTHON_EXE}")
    print(f"Build script:   {BUILD_SCRIPT}")
    print()

    holidays = federal_holidays(run_month_start.year)
    if run_month_start.month == 12:
        holidays |= federal_holidays(run_month_start.year + 1)

    checkpoints = compute_checkpoints(run_month_start.year, run_month_start.month, holidays)
    print("Checkpoint dates:")
    for cp_day, target, shifted in checkpoints:
        note = "" if shifted == target else f"   (shifted from {target.strftime('%a %b %d')} — weekend/holiday)"
        print(f"  {cp_day:>2}th  →  {shifted.strftime('%a %b %d')}{note}")
    print()

    if args.setup:
        print("Registering monthly recurring scheduler:")
        register_monthly_scheduler(args.dry_run)
        print()
        print("Registering monthly email-draft task (25th at 9 AM):")
        register_email_draft_task(args.dry_run)
        print()

    print("Registering checkpoint tasks:")
    skipped = 0
    registered = 0
    failed = 0
    for cp_day, target, shifted in checkpoints:
        if shifted < today and not args.dry_run:
            print(f"  -- skipping cp{cp_day} ({shifted.strftime('%a %b %d')} is in the past)")
            skipped += 1
            continue
        if register_checkpoint_task(period, cp_day, shifted, args.dry_run):
            registered += 1
        else:
            failed += 1

    print()
    if args.dry_run:
        print("[DRY RUN — no tasks created]")
    else:
        parts = [f"{registered} task(s) registered"]
        if failed:
            parts.append(f"{failed} failed")
        if skipped:
            parts.append(f"{skipped} past date(s) skipped")
        print("Done. " + ", ".join(parts) + ".")
        print(f"View tasks any time with:  python schedule_checkpoints.py --list")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
