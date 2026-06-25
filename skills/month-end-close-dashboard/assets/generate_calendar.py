"""
Generate an .ics file of Paxus close events for import into Google Calendar.

Creates one event per dashboard checkpoint (cp5/10/15/20/25) plus one per
month-end-email draft (25th of each calendar month). Checkpoint dates use the
same business-day shifting as the rest of the close system.

Each event includes a popup notification, so when Google Calendar fires the
event you click the "Paxus Close" shortcut on your Desktop and the launcher
runs the right action for that date.

Usage:
    python generate_calendar.py                  # next 12 months
    python generate_calendar.py --months 24      # next 24 months
    python generate_calendar.py --out my.ics     # custom output path
"""
from __future__ import annotations
import argparse
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from schedule_checkpoints import (  # noqa: E402
    federal_holidays,
    compute_checkpoints,
    close_period_for_run_month,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DASHBOARD_HOUR = 15  # 3 PM
EMAIL_HOUR = 9       # 9 AM
EMAIL_DRAFT_DAY = 25


def add_months(d: date, months: int) -> date:
    m = d.month - 1 + months
    return date(d.year + m // 12, m % 12 + 1, 1)


def fmt_dt(d: date, hour: int) -> str:
    return datetime(d.year, d.month, d.day, hour, 0).strftime("%Y%m%dT%H%M%S")


def stamp_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def vevent(uid: str, start: date, hour: int, summary: str, description: str, duration_min: int = 30) -> str:
    start_dt = datetime(start.year, start.month, start.day, hour, 0)
    end_dt = start_dt + timedelta(minutes=duration_min)
    return "\r\n".join([
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{stamp_now()}",
        f"DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}",
        f"SUMMARY:{summary}",
        f"DESCRIPTION:{description}",
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        "TRIGGER:-PT0M",
        f"DESCRIPTION:{summary}",
        "END:VALARM",
        "END:VEVENT",
    ])


def generate(months: int, start_month: date) -> str:
    events: list[str] = []
    cur = start_month
    for _ in range(months):
        holidays = federal_holidays(cur.year)
        if cur.month == 12:
            holidays |= federal_holidays(cur.year + 1)

        period = close_period_for_run_month(cur)
        for cp_day, _target, shifted in compute_checkpoints(cur.year, cur.month, holidays):
            uid = f"paxus-cp{cp_day}-{shifted.isoformat()}@paxuscpa"
            summary = f"Paxus Close: cp{cp_day} dashboard refresh ({period} close)"
            description = (
                f"Click the 'Paxus Close' shortcut on your Desktop. "
                f"It will refresh the dashboard for the {period} close at checkpoint {cp_day}."
            )
            events.append(vevent(uid, shifted, DASHBOARD_HOUR, summary, description))

        email_date = date(cur.year, cur.month, EMAIL_DRAFT_DAY)
        email_close_period = f"{cur.year:04d}-{cur.month:02d}"
        uid = f"paxus-email-{email_date.isoformat()}@paxuscpa"
        summary = f"Paxus Close: draft month-end email ({email_close_period} close)"
        description = (
            f"Click the 'Paxus Close' shortcut on your Desktop. "
            f"It will drop a draft of the close-timeline email for the {email_close_period} close on your Desktop."
        )
        events.append(vevent(uid, email_date, EMAIL_HOUR, summary, description))

        cur = add_months(cur, 1)

    header = "\r\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Paxus//Close Dashboard//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ])
    return header + "\r\n" + "\r\n".join(events) + "\r\nEND:VCALENDAR\r\n"


def find_desktop() -> Path:
    """Locate the active Desktop folder, accounting for OneDrive sync."""
    home = Path.home()
    onedrive_desktop = home / "OneDrive" / "Desktop"
    if onedrive_desktop.is_dir():
        return onedrive_desktop
    return home / "Desktop"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--months", type=int, default=12, help="How many months to generate (default: 12)")
    parser.add_argument("--start", help="Start month YYYY-MM (default: this month)")
    parser.add_argument("--out", help="Output path (default: Desktop\\Paxus Close Calendar.ics)")
    args = parser.parse_args()

    today = date.today()
    if args.start:
        yr, mo = (int(x) for x in args.start.split("-"))
        start = date(yr, mo, 1)
    else:
        start = today.replace(day=1)

    out = Path(args.out) if args.out else (find_desktop() / "Paxus Close Calendar.ics")
    ics = generate(args.months, start)
    out.write_text(ics, encoding="utf-8", newline="")
    end = add_months(start, args.months - 1)
    print(f"Wrote {out}")
    print(f"  • {args.months} months: {start.strftime('%B %Y')} → {end.strftime('%B %Y')}")
    print(f"  • Import this file into Google Calendar (Settings → Import & export → Import).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
