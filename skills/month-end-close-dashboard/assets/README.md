# Paxus Month-End Close Dashboard

Jennifer's internal system for tracking month-end close progress against
deadlines and drafting the firm-wide close-timeline email each month.

## What's in the box

| File | What it does |
| --- | --- |
| `build_dashboard.py` | Pulls Financial Cents project data and rewrites `project/close-data.js`. Run with `--period YYYY-MM --checkpoint N --record` to snapshot a checkpoint into the dashboard. |
| `compose_close_email.py` | Generates the firm-wide close-timeline email draft. Writes a `.txt` to the Desktop for Jennifer to review and send. |
| `schedule_checkpoints.py` | **Helpers only.** US federal holiday set (Paxus-observed), business-day shifting, checkpoint date computation. Imported by the launcher and the calendar generator. The schtasks-based scheduling functions here are deprecated — see "How scheduling works" below. |
| `run_today.py` | **The launcher.** Figures out what's scheduled for today (dashboard refresh, email draft, or both) and runs it. Triggered from the Desktop `.bat` shortcut. |
| `generate_calendar.py` | Produces `Paxus Close Calendar.ics` for import into Google Calendar. 12 months of reminders by default. |
| `probe_close.py` | Diagnostic — pokes at the Financial Cents API for the close-period filter. |
| `project/` | The HTML dashboard itself: `dashboard.html`, `close-data.js` (rebuilt by `build_dashboard.py`), assets, etc. |

## How the system runs (the current workflow)

1. **Google Calendar** holds the cadence: a popup reminder for each checkpoint
   (cp5 / cp10 / cp15 / cp20 / cp25 at 3 PM) and one for the close-timeline
   email draft (25th of each month at 9 AM). The calendar was seeded by
   importing `Paxus Close Calendar.ics`.
2. When Calendar pings Jennifer, she double-clicks **`Paxus Close.bat`** on
   her Desktop.
3. The `.bat` calls `run_today.py`, which:
   - Checks today's date against the (business-day-shifted) checkpoint dates
     for the current calendar month — runs `build_dashboard.py` for each match
     and opens `project/dashboard.html` in her browser.
   - If today is the 25th, runs `compose_close_email.py` and opens the draft
     `.txt` in Notepad.
   - If nothing matches, prints the next 6 upcoming events.

The two scripts that the launcher invokes are exactly the ones Jennifer would
have run manually before — the launcher just removes the "which one do I run
today?" step.

## Why we are NOT using Windows Task Scheduler

On 2026-06-24 we tried to register the per-checkpoint runs as Windows
scheduled tasks via `schtasks.exe`. Every attempt that referenced a script in
`C:\Users\paxus\paxus-ai\internal\…` returned **"Access is denied"** — running
as admin made no difference. Tests confirmed it's the destination path that's
blocked: `cmd /c echo hi` and `python.exe --version` registered fine, but the
moment the task pointed at a `.py` or `.bat` in this folder, registration was
rejected. Best guess is the Paxus EDR is flagging scheduled tasks that launch
scripts from a user-writable folder.

Calendar reminders + a single-click launcher sidestep the issue entirely.

## Extending the calendar past May 2027

The `.ics` ships 12 months. To extend:

```
cd C:\Users\paxus\paxus-ai\internal\month-end-close-dashboard
python generate_calendar.py --months 24
```

It writes to `~\OneDrive\Desktop\Paxus Close Calendar.ics`. Import that into
Google Calendar (Settings → Import & export → Import). Existing events are
not duplicated — each event UID is stable across regenerations.

## Manual runs

If Jennifer wants to refresh the dashboard or draft the email off-cycle, she
can run either script directly without going through the launcher:

```
python build_dashboard.py --period 2026-05 --checkpoint 25 --record
python compose_close_email.py --close 2026-06
python compose_close_email.py --close 2026-06 --ooo "Kaitlyn out Jul 6-10"
```

## Repo status

This folder is **not** under version control. The whole thing lives at
`C:\Users\paxus\paxus-ai\internal\month-end-close-dashboard\` on Jennifer's
laptop. If/when it's worth promoting this into a formal Claude skill in the
`paxus-skills` marketplace, the candidate scope is `run_today.py` +
`generate_calendar.py` + the helpers in `schedule_checkpoints.py` + this README.
