"""
Generate the firm-wide month-end close timeline email — a draft for Jennifer to
review and send manually.

Structure rules (per Jennifer):
  - W1 / W2 / W3 are three consecutive Mon-Fri weeks of the WORK month, starting
    with the first week whose Monday is in the month.
  - Each deadline appears under the section for the week it actually falls in
    (so cp10 lives in W1 some months, W2 in others).
  - Bank statements are not available before the 1st of the work month.

Usage:
    python compose_close_email.py                         # current calendar month's close
    python compose_close_email.py --close 2026-06         # specific close period
    python compose_close_email.py --ooo "Kaitlyn out Jul 6-10"
    python compose_close_email.py --note "extra context line"
    python compose_close_email.py --stdout                # print, no file
    python compose_close_email.py --out my-draft.txt      # custom path
"""
from __future__ import annotations
import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from schedule_checkpoints import (  # noqa: E402
    federal_holidays,
    compute_checkpoints,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

MONTHS_LONG = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
DOW_LONG = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def label(d: date) -> str:
    return f"{DOW_LONG[d.weekday()]}, {MONTHS_LONG[d.month - 1]} {d.day}"


def short_range(start: date, end: date) -> str:
    if start.month == end.month:
        return f"{MONTHS_LONG[start.month - 1]} {start.day}-{end.day}"
    return f"{MONTHS_LONG[start.month - 1]} {start.day} - {MONTHS_LONG[end.month - 1]} {end.day}"


def first_full_workweek(year: int, month: int) -> tuple[date, date]:
    """First Mon-Fri whose Monday is in the given month."""
    d = date(year, month, 1)
    while d.weekday() != 0:  # advance to Monday
        d += timedelta(days=1)
    return d, d + timedelta(days=4)


def prev_business_days(d: date, n: int, holidays: set) -> list[date]:
    """The n business days immediately preceding d, returned ASCENDING."""
    out: list[date] = []
    cur = d - timedelta(days=1)
    while len(out) < n:
        if cur.weekday() < 5 and cur not in holidays:
            out.append(cur)
        cur -= timedelta(days=1)
    out.sort()
    return out


def week_for(d: date, weeks: list[tuple[date, date]]) -> int:
    """Return 1, 2, or 3 if d falls in W1/W2/W3; 0 if before W1; 4 if after W3."""
    for i, (mon, fri) in enumerate(weeks, start=1):
        if mon <= d <= fri:
            return i
    if d < weeks[0][0]:
        return 0
    return 4


def compose_email(close_year: int, close_month: int, ooo: str, note: str) -> str:
    close_name = MONTHS_LONG[close_month - 1]
    work_year, work_month = (close_year, close_month + 1) if close_month < 12 else (close_year + 1, 1)
    work_name = MONTHS_LONG[work_month - 1]

    holidays = federal_holidays(work_year)
    if work_month == 12:
        holidays |= federal_holidays(work_year + 1)
    cps = compute_checkpoints(work_year, work_month, holidays)
    cp5, cp10, cp15, cp20, cp25 = [c[2] for c in cps]

    # Three consecutive Mon-Fri weeks starting from first full week of work month,
    # plus a pre-week (W0) for finalizing close-month coding.
    w1 = first_full_workweek(work_year, work_month)
    w0 = (w1[0] - timedelta(days=7), w1[1] - timedelta(days=7))
    w2 = (w1[0] + timedelta(days=7), w1[1] + timedelta(days=7))
    w3 = (w2[0] + timedelta(days=7), w2[1] + timedelta(days=7))
    weeks = [w1, w2, w3]

    # Deadlines + which week each belongs in
    staff_to_lead = cp10                                       # all-other-clients staff handoff
    wos_staff_dates = prev_business_days(cp10, 2, holidays)    # 2 days before cp10
    lead_to_ctrl = cp15                                        # all-other-clients lead handoff
    wos_lead = prev_business_days(cp15, 1, holidays)[-1]       # 1 day before cp15
    final_delivery = cp20

    # Bank statements goal: Tuesday of W1 (or earliest weekday on/after day 1)
    bs_goal = w1[0] + timedelta(days=1)
    # Reconciliation deadline: Friday of W1
    recon_by = w1[1]

    # Week-membership for each deadline (1=W1, 2=W2, 3=W3, 0/4 outside)
    wk_staff_to_lead = week_for(staff_to_lead, weeks)
    wk_lead_to_ctrl = week_for(lead_to_ctrl, weeks)
    wk_wos_staff = week_for(wos_staff_dates[0], weeks)
    wk_wos_lead = week_for(wos_lead, weeks)
    wk_final = week_for(final_delivery, weeks)

    # Section labels — adjust if staff/leads are or aren't active in W2/W3
    w1_label = "interns and staff"
    w2_label = "staff, leads and controllers" if wk_staff_to_lead >= 2 else "leads and controllers"
    w3_label = "lead and controllers" if wk_lead_to_ctrl >= 3 else "controllers"

    # Build deadline lines per week
    def wos_staff_str(dates: list[date]) -> str:
        if len(dates) >= 2 and (dates[1] - dates[0]).days == 1:
            return f"{DOW_LONG[dates[0].weekday()]}-{DOW_LONG[dates[1].weekday()]}, {MONTHS_LONG[dates[0].month - 1]} {dates[0].day}-{dates[1].day}"
        return " or ".join(label(d) for d in dates)

    week_lines: dict[int, list[str]] = {1: [], 2: [], 3: []}
    if wk_wos_staff in (1, 2, 3):
        week_lines[wk_wos_staff].append(
            f"• Wheel-of-service clients: All staff work wrapped up and handed off to leads by {wos_staff_str(wos_staff_dates)}."
        )
    if wk_staff_to_lead in (1, 2, 3):
        week_lines[wk_staff_to_lead].append(
            f"• All other clients: Staff work to leads by EOD {label(staff_to_lead)}."
        )
    if wk_wos_lead in (1, 2, 3):
        week_lines[wk_wos_lead].append(
            f"• Wheel-of-service clients: Lead work on WOS clients should go to controllers by {label(wos_lead)}."
        )
    if wk_lead_to_ctrl in (1, 2, 3):
        week_lines[wk_lead_to_ctrl].append(
            f"• All other clients: Lead work should be handed off to controllers by EOD {label(lead_to_ctrl)}."
        )
    if wk_final in (1, 2, 3):
        week_lines[wk_final].append(
            f"• Final deadline for all controller work is {label(final_delivery)}."
        )
        week_lines[wk_final].append(
            f"• All financial statements delivered to clients by EOD {label(final_delivery)}."
        )

    # Weekend note for the 20th
    cp20_original = date(work_year, work_month, 20)
    weekend_note = ""
    if cp20 != cp20_original:
        weekend_note = f" (Note: {MONTHS_LONG[cp20_original.month - 1]} {cp20_original.day}-{cp20_original.day + 1} fall on a weekend.)"

    ooo_block = ""
    if ooo:
        ooo_block = f"A couple of things to be aware of: {ooo}\n\n"
    if note:
        ooo_block += f"{note}\n\n"

    # === Assemble body ===
    parts: list[str] = []
    parts.append(f"""Hi team,

As we head into the {close_name} close, I wanted to share the timeline and key deadlines — plus a few scheduling notes to keep in mind.

{ooo_block}Staff — please don't worry about {work_name} coding until all {close_name} clients are reconciled and handed off to your lead.

As you work through the close, look for opportunities to build in efficiencies — implementing new rules or using Claude for journal entries are both great places to start.

See the timeline breakdown below. Please reach out if you run into any blockers!

Thanks, everyone!
""")

    # If W0 contains any work-month days (i.e. partial week straddling the
    # month boundary), bank-statement and reconciliation work BEGINS in W0.
    w0_has_work_month_days = any(
        (w0[0] + timedelta(days=i)).month == work_month for i in range(5)
    )

    # Helper to indent a bullet list (4-space indent under 2-space sub-heads)
    def indent_bullets(lines: list[str]) -> str:
        # Lines come in with leading "• "; add 4 spaces of indent
        return "\n".join("    " + ln for ln in lines)

    # --- Week 0 section (pre-W1: wrap up close-month coding) ---
    w0_bullets = [
        f"• Finalizing {close_name} coding.",
        "• Wrapping up any outstanding questions.",
    ]
    if w0_has_work_month_days:
        w0_bullets.append(
            f"• Beginning bank statement download and reconciliation as statements become available (starting {work_name} 1)."
        )
    parts.append(f"""
Week of {short_range(*w0)}
  Focus on:
{indent_bullets(w0_bullets)}
""")

    # --- Week 1 section ---
    if w0_has_work_month_days:
        w1_focus_bullets = [
            "• Continuing bank statement download from clients.",
            "• Reconciliation once all bank statements are pulled.",
        ]
    else:
        w1_focus_bullets = [
            f"• Pulling bank statements as they become available (not available until the 1st of {work_name} at the earliest).",
            "• Reconciliation once all bank statements are pulled.",
        ]
    w1_should_bullets = [
        "• No outstanding questions, unless waiting on the client.",
        f"• Goal: Pull bank statements by {label(bs_goal)} if possible, and have all accounts reconciled by {label(recon_by)}.",
    ]
    parts.append(f"""
Week of {short_range(*w1)} ({w1_label})
  Focus on:
{indent_bullets(w1_focus_bullets)}

  There should be:
{indent_bullets(w1_should_bullets)}
""")
    if week_lines[1]:
        parts.append(f"\n  Deadlines this week:\n{indent_bullets(week_lines[1])}\n")

    # --- Week 2 section ---
    w2_focus_bullets = [
        "• Reviewing and completing reconciliations handed off from staff.",
        "• Moving completed work up the chain per the deadlines below.",
    ]
    parts.append(f"""
Week of {short_range(*w2)} ({w2_label})
  Focus on:
{indent_bullets(w2_focus_bullets)}
""")
    if week_lines[2]:
        parts.append(f"\n  Deadlines to keep in mind:\n{indent_bullets(week_lines[2])}\n")

    # --- Week 3 section ---
    parts.append(f"\nWeek of {short_range(*w3)} ({w3_label})\n")
    if week_lines[3]:
        lines = []
        for ln in week_lines[3]:
            if "Final deadline for all controller work" in ln and weekend_note:
                ln = ln.rstrip(".") + "." + weekend_note
            lines.append(ln)
        parts.append(indent_bullets(lines) + "\n")

    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--close", help="Close period YYYY-MM (default: current calendar month)")
    parser.add_argument("--ooo", default="", help="OOO notes (single line)")
    parser.add_argument("--note", default="", help="Additional context line")
    parser.add_argument("--out", help="Output file path")
    parser.add_argument("--stdout", action="store_true", help="Print, don't write a file")
    args = parser.parse_args()

    today = date.today()
    if args.close:
        try:
            yr, mo = (int(x) for x in args.close.split("-"))
        except (ValueError, TypeError):
            sys.exit(f"--close must be YYYY-MM, got: {args.close!r}")
    else:
        yr, mo = today.year, today.month

    email_text = compose_email(yr, mo, args.ooo, args.note)

    if args.stdout:
        sys.stdout.write(email_text)
        return 0

    out_path = Path(args.out) if args.out else (
        Path.home() / "Desktop" / f"Close Timeline Email - {MONTHS_LONG[mo - 1]} {yr}.txt"
    )
    out_path.write_text(email_text, encoding="utf-8")
    print(f"Wrote draft email: {out_path}")
    print()
    print("Review, paste into Gmail, send to the team.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
