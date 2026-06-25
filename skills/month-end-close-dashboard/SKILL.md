---
name: month-end-close-dashboard
description: Operate and maintain the Paxus firm-internal month-end close dashboard and timeline-email system. Run when the operator asks about the close-progress dashboard refresh cadence, the cp5/cp10/cp15/cp20/cp25 checkpoint shifting, the close-timeline email draft, the Desktop launcher (Paxus Close.bat), or extending the close Google Calendar past its current end. Also covers diagnosing missed checkpoints and onboarding a new firm administrator into the system. FIRM-INTERNAL — this skill is not client-facing and is unrelated to /monthly-dashboard (which builds client board packages).
---

# /month-end-close-dashboard — Firm-Internal Close Tracking

You are operating the **Paxus firm-internal month-end close dashboard** — Jennifer's
(or any future firm administrator's) tool for tracking close progress against
deadlines and generating the monthly firm-wide close-timeline email. Be
conversational and warm — match the Paxus voice.

This is **firm administration infrastructure**, not a client deliverable. It
contains no client data and produces no client-facing output. Don't confuse it
with `/monthly-dashboard` (client board / for-profit dashboards).

## What the system does

Three products on one cadence:

1. **The close dashboard** (`project/dashboard.html`) — an HTML page that shows
   close-progress for the prior month's books across all ~121 Paxus clients,
   sourced from Financial Cents. It's snapshotted at five checkpoints during
   the work month so trend lines persist across the close. The same UI source
   lives in `project/Paxus Close Dashboard.dc.html` and is hosted at
   `claude.ai/design` for the team (see "Hosted dashboard" below).
2. **The checkpoint status email** — a `.txt` draft generated at each
   checkpoint (cp5/cp10/cp15/cp20/cp25) by `assets/compose_checkpoint_email.py`.
   Each draft includes the hosted dashboard link, a per-checkpoint narrative
   (top reconcilers / top reviewers / lead-queue stragglers, depending on
   which checkpoint), the Pipeline Breakdown table, and an open-items list.
   Saved to Downloads, opened automatically in Notepad for review.
3. **The close-timeline email** — a separate `.txt` draft generated once a
   month on the 25th by `assets/compose_close_email.py`. Previews the *next*
   close's W1/W2/W3 deadlines for the team. Jennifer reviews, pastes into
   Gmail, sends.

All three share the same federal-holiday + business-day-shifting logic, which
lives in `assets/schedule_checkpoints.py`.

## The five checkpoints (cp5 / cp10 / cp15 / cp20 / cp25)

Each checkpoint = the dashboard is refreshed and a snapshot is recorded into
month-over-month history. Targets are the 5th, 10th, 15th, 20th, and 25th of
the **work month** (i.e., the calendar month *after* the close period).

**Shifting rules** — every checkpoint moves to the nearest business day if the
target falls on a weekend or Paxus-observed federal holiday:

- **cp5, cp10, cp15, cp25** — milestones. Shift **forward** to the next business
  day (the team has the next business day to hit them).
- **cp20** — the final-delivery deadline. Shifts **backward** to the prior
  business day (clients must get statements *before* the weekend, not after).

**Paxus-observed federal holidays** (7 total — confirmed with Jennifer):

| Holiday | Date |
| --- | --- |
| New Year's Day | Jan 1 |
| Memorial Day | last Mon of May |
| Independence Day | Jul 4 |
| Labor Day | 1st Mon of Sep |
| Thanksgiving | 4th Thu of Nov |
| Christmas Eve | Dec 24 |
| Christmas Day | Dec 25 |

**Not observed by Paxus** (do not add these — Jennifer specifically excludes them):
MLK Day, Presidents Day, Juneteenth, Day-after-Thanksgiving.

Weekend-observed shifting also applies: Saturday holidays observe to the prior
Friday; Sunday holidays observe to the following Monday.

## How the system runs (the operator workflow)

1. **Google Calendar** holds the cadence. A popup reminder fires for each
   checkpoint (cp5/10/15/20/25 at 3 PM) and for the email draft (25th at 9 AM).
   The calendar was seeded by importing `Paxus Close Calendar.ics`, generated
   by `assets/generate_calendar.py`.
2. When the popup fires, the operator double-clicks **`Paxus Close.bat`** on
   the Desktop.
3. The `.bat` invokes `assets/run_today.py`, which:
   - Computes today's expected actions (shifted checkpoint match, and the
     25th-of-the-month timeline email check) and runs each in order.
   - **Dashboard refresh** (on every checkpoint date): calls
     `build_dashboard.py --period <prior-month> --checkpoint N --record` and
     opens `project/dashboard.html` in the browser.
   - **Checkpoint status email** (on every checkpoint date): calls
     `compose_checkpoint_email.py --checkpoint N` which writes
     `Checkpoint Email cp<N> - <Month>_<Year>.txt` to Downloads and opens
     it in Notepad.
   - **Close-timeline email** (only on the 25th): calls `compose_close_email.py
     --close <this-month>` which writes `Close Timeline Email - <Month> <Year>.txt`
     to the Desktop and opens it in Notepad.
   - If nothing matches today, prints the next 6 upcoming events.

A single click handles all today's work — including the 25th, when **three**
drafts run together: the cp25 dashboard refresh (for the prior month's close),
the cp25 status email, and the timeline email for the next close.

## Hosted dashboard

The dashboard is hosted on **Claude Design** at
`https://claude.ai/design/p/c9f5e7a2-8e99-42eb-b911-a399f0dd7284?file=Paxus+Close+Dashboard.dc.html`
so the Paxus team can view it from any browser without needing the local files.

The Claude Design project mirrors `project/Paxus Close Dashboard.dc.html` (UI
source) + `project/close-data.js` (live data). The hosted version does NOT
auto-refresh — at each checkpoint, after running `Paxus Close.bat`, the
operator manually updates the hosted project so the team sees current numbers:

1. Open the Claude Design URL in a browser.
2. Replace `close-data.js` in the project with the freshly-written copy from
   `paxus-ai\internal\month-end-close-dashboard\project\close-data.js`.
3. If `dashboard.html` or `Paxus Close Dashboard.dc.html` changed (rare —
   only when the UI itself is modified), replace those too.
4. Verify the hosted preview renders the new numbers, then send the
   checkpoint email — the link in the email will be live.

If Claude Design does not support in-place file replacement in a future
release, fall back to the inline Pipeline Breakdown table in the checkpoint
email (the email always contains current numbers regardless of the link), and
plan to migrate hosting to a static host (GitHub Pages, Google Drive
publish-to-web, internal Paxus share).

## Why this is NOT a Windows Task Scheduler job

On 2026-06-24 we tried registering each checkpoint as a `schtasks` one-shot.
Every attempt that referenced a `.py` or `.bat` in
`C:\Users\paxus\paxus-ai\internal\…` returned **"Access is denied"** — running
elevated didn't help. Isolation tests (`cmd /c echo`, `python.exe --version`,
both succeeded; same task pointing at any script in that folder, blocked)
confirmed the Paxus EDR is the gate. The Calendar + .bat launcher sidesteps it
entirely because nothing on the persistence-watchlist surface is touched.

If a future operator's EDR posture differs and `schtasks` registration is
allowed, the deprecated registration functions still exist in
`assets/schedule_checkpoints.py` and could be reactivated — but only after
testing on the operator's machine first.

## Workflow — common operator requests

### Phase 1 — "Refresh the dashboard / draft the email" (the daily click)

Almost always the operator just needs to click the Desktop `.bat`. If they're
asking Claude about it, something probably went wrong:

1. Confirm the popup said today's date.
2. Have them double-click `Paxus Close.bat` on the Desktop.
3. The black window shows what ran. If it says "Nothing scheduled for today"
   and a checkpoint *was* expected, jump to Edge Cases below.

### Phase 2 — "Extend the calendar past its current end"

The `.ics` ships 12 months at a time. To extend:

```bash
cd "C:\Users\paxus\paxus-ai\internal\month-end-close-dashboard"
python generate_calendar.py --months 24
```

Default output is `~\OneDrive\Desktop\Paxus Close Calendar.ics`. Then in Google
Calendar: Settings → Import & export → Import → pick the file → choose the
work calendar. Event UIDs are stable across regenerations, so re-importing
won't duplicate existing events.

If the OneDrive Desktop hides the `.ics` from File Explorer view (we hit this
once — Defender or OneDrive sync), copy it to `~\Downloads\` with
`--out "C:\Users\paxus\Downloads\Paxus Close Calendar.ics"` instead.

### Phase 3 — "Onboard a new firm administrator into this system"

Three deployment artifacts, in order:

1. **Scripts:** copy `assets/` into
   `C:\Users\<them>\paxus-ai\internal\month-end-close-dashboard\` (or set up
   their `paxus-ai` repo first).
2. **Desktop launcher:** create `Paxus Close.bat` on their Desktop with this
   content, with their Python path and the path to `run_today.py`:

   ```batch
   @echo off
   title Paxus Close
   cd /d "C:\Users\<them>\paxus-ai\internal\month-end-close-dashboard"
   "C:\Users\<them>\AppData\Local\Programs\Python\Python313\python.exe" "run_today.py"
   echo.
   pause >nul
   ```
3. **Calendar:** run `python assets/generate_calendar.py` on their machine,
   import the resulting `.ics` into their Google Calendar.

Sanity check: have them double-click the .bat on a non-checkpoint day. They
should see "Nothing scheduled for today" plus the upcoming list. That's the
smoke test.

### Phase 4 — "A checkpoint was missed / dashboard didn't update"

1. Read the most recent close-data snapshot in `project/close-data.js` to see
   the last recorded checkpoint.
2. Manually re-run the missed checkpoint:

   ```bash
   python build_dashboard.py --period <YYYY-MM> --checkpoint <N> --record
   ```
   `--period` is the **close period** (the month being closed), not the work
   month. So a missed cp10 in July 2026 (closing June) → `--period 2026-06`.
3. If multiple checkpoints were missed, run them in chronological order so the
   history records cleanly.

### Phase 5 — "Edit the close-timeline email content"

The email body templating lives in `assets/compose_close_email.py`. The W1/W2/W3
deadline lines are computed from the checkpoints, but the human prose (greeting,
OOO block, sign-off voice) is in the template string. Edit there, then run with
`--stdout` to preview before letting it write to Desktop:

```bash
python compose_close_email.py --close 2026-07 --stdout
```

## Important rules for this skill

- **No fabrication.** If the operator doesn't know an answer (Python path,
  checkpoint target month, OOO dates), write `[TBD — operator to fill]` rather
  than guessing.
- **The 7-holiday set is canonical.** Do not add MLK / Presidents / Juneteenth
  / day-after-Thanksgiving. Jennifer confirmed the list; changing it shifts
  every checkpoint date downstream.
- **`--period` is the CLOSE month, not the work month.** A cp25 in June (work
  month) is closing May → `--period 2026-05`. Read this every time before
  running `build_dashboard.py` manually — it's the most common operator mistake.
- **The schtasks code in `schedule_checkpoints.py` is deprecated.** Its helper
  functions (`federal_holidays`, `compute_checkpoints`, `close_period_for_run_month`,
  `shift_for_checkpoint`) are imported by `run_today.py` and `generate_calendar.py`
  and must stay; the `register_*` functions and the `main()` CLI are dead.
  Don't reintroduce them without first confirming the operator's EDR allows
  scheduled-task creation against scripts in `paxus-ai\internal\`.
- **No client data lives here.** This system tracks aggregate close progress,
  not individual client work. The dashboard shows counts and percentages, not
  client names or numbers from QBO. If a request would put a specific client's
  details into the system, redirect — that belongs in the client's Drive folder,
  not this skill.

## Edge cases

- **`.ics` file silently disappears from Desktop after generation.** Defender
  or OneDrive Files-On-Demand may hide it from the Desktop view. Workaround:
  generate to `~\Downloads\` with `--out` instead, or open File Explorer
  directly at `C:\Users\paxus\OneDrive\Desktop\` and locate it there.
- **Holiday observance shifting.** If a checkpoint falls on a Saturday holiday,
  the observed date moves to Friday and Friday is the blocked business day for
  the checkpoint. The shifter handles this automatically; don't bypass it.
- **Year boundary (work month = January).** When the work month is January, the
  holiday set must include New Year's of *that* year. The compute code already
  unions the next year's holidays when work_month == 12; don't change the
  union without rechecking January cp5.
- **Email draft text file is plain `.txt`.** Jennifer pastes into Gmail manually
  — the skill never sends. Don't add SMTP / Gmail-API send paths; the manual
  review step is the entire point of the draft model.
- **Multiple checkpoints on the same date.** Rare but possible with holiday
  stacking. `run_today.py` handles this by iterating; manual re-runs should
  invoke `build_dashboard.py` separately for each checkpoint to keep history
  rows distinct.
- **Operator's `paxus-ai` folder lives elsewhere.** The deployed scripts use
  `sys.executable` and `__file__`-relative paths, so they work wherever the
  scripts live. Only the Desktop `.bat` has a hard-coded Python path — that's
  the one piece that needs editing per machine.

## Where the live files run

The skill ships **canonical copies** of the operational scripts AND the
dashboard UI templates in `assets/`:

- Python scripts: `assets/*.py` (build, compose, schedule, launch, generate).
- Dashboard template: `assets/project/dashboard.html` and
  `assets/project/Paxus Close Dashboard.dc.html` (Claude Design source).
- Runtime + brand assets: `assets/project/support.js`,
  `assets/project/assets/paxus-logo.*`.

What's NOT in the skill (deliberately):

- `project/close-data.js` — regenerated every checkpoint, contains client
  names from FC. Stays per-deployment, never committed.
- `project/uploads/*.csv` — Financial Cents exports with client data. Stays
  per-deployment, never committed.
- `.cache_projects.json` — cached FC pull. Stays per-deployment.

The active *deployment* on Jennifer's machine lives at
`C:\Users\paxus\paxus-ai\internal\month-end-close-dashboard\` — her Desktop
`.bat` points at that copy. When changes flow into this skill via the PR-review
process, the operator manually pulls the updated `assets/` files into their
local deployment. There is no auto-sync between the two — the skill folder is
the source of truth; the deployed copy is "installed."

## Persistence note

This skill is firm-internal infrastructure for the close cadence. The deployed
scripts live with the operator. Per-month state (last recorded checkpoint,
draft email contents) lives on the operator's machine, not in this skill — the
skill itself contains no time-sensitive state and is safe to commit / share / sync.
