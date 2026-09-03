---
name: monthly-capacity
description: Run the firm's month-end capacity build in CapacityIQ. Takes the month's QB Time itemized report, merges it against the roster in the CapacityIQ Data sheet, and produces a six-section review of everything that needed a judgement call — reconciliation, new clients, hours short, hours over target, client phase, and judgement calls made. After the review is approved it writes the month back to the sheet so the snapshot can be captured in the app. Run at month end, once the timesheet is final. Firm-internal capacity planning, not client work.
---

# /monthly-capacity — CapacityIQ month-end

You are running the firm's monthly capacity build. One QB Time report goes in; a reviewed, approved month lands in the CapacityIQ Data sheet.

Most of the work is already done by the bundled scripts. Your job is to orchestrate them, present the review faithfully, **stop and wait for answers**, and only then write anything.

## Important rules for this skill

- **Nothing is written to the sheet until the operator approves the review.** The review is a stopping point, not a status update. Sections 2, 3 and 5 are questions.
- **Print the review exactly as the script emits it.** Do not summarise it, re-order it, re-format it, or "tidy" the tables. It is markdown and renders correctly as-is. A review that looks different every month is one nobody trusts.
- **The report contains per-person detail and stays local.** It is written to the runner's own `~/Downloads`. Never upload it to the shared Capacity folder in Drive — ten of the people named in section 3 have access to that folder. Passing it on is the runner's decision to make, not this skill's.
- **No fabrication.** If a client's team or budget is unknown, leave it and flag it. Never guess a roster.
- **Run at month end only.** The script warns when the timesheet does not cover the whole month; if that warning fires, stop and get a complete export.
- **A filtered export is destructive, so check the input before trusting it.** Write-back *clears* the Assignments tab and rebuilds it from the timesheet alone, and the snapshot then freezes whatever that produced. So an export scoped to one person or one group does not produce a small month — it silently deletes everyone missing from the roster. Section 0 exists to catch this and it can halt the run. Never build past a halt.
- **Skills are the engine; the data is the fuel.** No client or staff names belong in this folder. Client name mappings live in the sheet's `Aliases` tab.

## What you need before starting

- `gws` authenticated (`gws auth status`), Python 3 with `openpyxl`.
- Editor access to the CapacityIQ Data sheet — Cassie, Jennifer and Lisa have it.
- The month's **itemized** QB Time report as CSV (columns include `fname`, `lname`, `jobcode_1..3`, `hours`, `service item`).

Working from `skills/monthly-capacity/scripts/`. The CapacityIQ Data sheet id is
`1ycxCUBlBq4TQY-54yM7hSiONA2285c630FNWfoNx_LQ`, in the Paxus shared Drive under
`00 - Paxus CPA / Admin / Business / Capacity`.

## Workflow

### Phase 1 — Take the timesheet

Ask which month is being closed and where the QB Time CSV is. File a copy in that month's folder in the Capacity Drive folder so the input is preserved.

### Phase 2 — Read the app, not the scope sheet

The app is the source of truth. Export the sheet and run the build:

```bash
gws drive files export \
  --params '{"fileId":"<SHEET_ID>","mimeType":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}' \
  -o app.xlsx
```

**Check the input before building.** This runs against the raw CSV, so it works even on a file the build would choke on:

```python
from checks import preflight, render as render_checks
pre = preflight('<YYYY-MM>', '<timesheet.csv>', 'app.xlsx')
print(render_checks(pre))
```

If `pre['halt']` is non-empty, **stop**. Show the operator what it says, get a complete export, and start again. Do not build, and above all do not write back. A halt means one of:

- **Active staff who logged real hours last month have no rows at all** — the signature of an export filtered to a subset of people. Graded against last month deliberately, so someone who simply does not book client time is a note rather than a stop.
- **Client hours or client count collapsed** against the previous snapshot — an export scoped to a group looks exactly like this.

Warnings are for the operator to read, not to resolve here. One worth understanding: a person rostered in **two roles on the same client** will have *all* their hours booked to the higher role, leaving the other reading zero for the month. That reads as "no work done" when the work simply went to the other line, and it is not fixable in the data — either split the roles between two people or accept the split is not measurable.

Then build:

```python
from build_month import build
a, s, r = build('<YYYY-MM>', None, '<timesheet.csv>', {}, None, app_path='app.xlsx')
```

The old staff scope spreadsheet is **not** part of this loop. Do not read capacity from it.

### Phase 3 — Produce the review

```python
from review import render, coverage, save
from checks import drift
text = render('<YYYY-MM>', a, s, r, coverage('<timesheet.csv>', '<YYYY-MM>'))
dr = drift('<YYYY-MM>', a, 'app.xlsx')
path = save(render_checks(pre, dr) + text, '<YYYY-MM>')   # -> the runner's own ~/Downloads
```

Print the section 0 checks followed by `text` verbatim to the operator, and tell them where the file was saved.

`drift()` only ever warns, and both of its checks are worth reading rather than clearing:

- **A client/role line that carried hours last month and none this month.** Sometimes a client genuinely wound down. It is also exactly what an unflipped handoff looks like — someone changed role, nobody updated Assignments, and their hours are still booking to the role they left. Role comes from the roster, never from the timesheet, so this drifts silently and indefinitely.
- **Rostered people logging nothing, month after month.** A name that never carries hours makes the team list wrong and hides who actually owns the work. One person sat rostered on a client for ten months having logged 0.3 hours in total.

### Phase 4 — Stop and wait

Sections 2, 3 and 5 are questions. Do not proceed until they are answered:

- **§2 New clients** — hours logged against something with no entry in the app. Get the **team and the budgets**. The client is flagged, never silently ignored — but its **hours are not in the build**: they sit in `unresolved` in §1 until the client exists in the app. Phase 4b is what puts them in.
- **§3 Hours short** — recorded less than a full month with no reason on file. If the operator knows why, record it in the Staff tab's `unpaid_off_hours`; if not, those are conversations for them to have, not something to resolve here.
- **§5 Client phase** — the 20–50% onboarding band is deliberately undecided, and clean-up coded on an Active client is a flag. Both are the operator's call.

If reconciliation in §1 does not balance, **stop entirely** and say so. Do not write a month that does not tie.

### Phase 4b — Stage any new clients and rebuild

Skip this when §2 was empty. Otherwise it is **not optional** — the month does not tie without it.

`build()` only emits assignment rows for job codes that resolve to a known client, so a §2 client's hours are not in `a` at all. They are in `unresolved`. Adding the client at write-back time adds the *row* and not the *hours*, which writes a month that is short by exactly that client's total and a client sitting in the app with zero assignments.

So put them in the workbook first, then build the month again:

```python
from newclients import stage
stage('app.xlsx', [
    {'name': '<exactly as §2 shows it>',
     'team': [('<person>', 'Staff'), ('<person>', 'Lead'), ('<person>', 'Controller')],
     'status': 'Onboarding',        # or 'Active' — see below
     'staff_budget': 0.0, 'lead_budget': 0.0, 'controller_budget': 0.0},
])
a, s, r = build('<YYYY-MM>', None, '<timesheet.csv>', {}, None, app_path='app.xlsx')
```

Then **re-render the review** (Phase 3) and confirm `unresolved` is now **0** before going on.

- **The team is required, and it is why §2 asks for it.** Role comes from the roster, never from the timesheet. With no roster row the build falls back to each person's primary role, which is not necessarily the role the operator named.
- **Leave a budget out rather than inventing one.** A client quoted but not yet budgeted is a real state; a guessed budget is not.
- **Status follows the coding, not the default.** A client whose hours are mostly Onboarding / Clean-up service items belongs in `Onboarding` — check §5 rather than accepting `Active`.
- `stage()` refuses a duplicate client, a missing team, a (person, role) pair that is not on the Staff tab, or an unknown Clients column, and writes nothing when it refuses.

### Phase 5 — Write back

Only after approval:

```python
from writeback import write_month
plan = write_month(SHEET_ID, '<YYYY-MM>', a, s,
                   new_clients=[...],   # approved in §2, or omit
                   dry_run=True)        # review the plan first
```

`new_clients` here adds the rows to the **live sheet's** Clients tab and nothing more — it is the counterpart to Phase 4b, not a replacement for it. Pass the same clients to both. The ids the two assign do not need to match: writeback matches assignment rows to clients by name.

Show the plan (rows to write, rows replaced, staff updated, anything unmatched). If `unmatched` is non-empty, resolve it before applying. Then re-run with `dry_run=False`.

This replaces the Assignments tab wholesale with this month's rows and updates the numeric columns on Staff. It does **not** touch email, status, `client_pct`, `daily_rate` or `capacity_mode`.

### Phase 6 — The operator captures the snapshot

Snapshotting stays in the app so there is one implementation of that logic rather than two that can drift. Tell the operator to open CapacityIQ and capture the snapshot for the period.

Capturing the snapshot also fills the `staff_hours` column and feeds the app's **Handoffs** tab, which compares a seat's new occupant against the previous one. That analysis lives in the app, editor-only — not in this review — so nothing needs doing here beyond capturing the month.

Then verify: reconciliation balanced, the app total ties to client hours, no departed staff on a live assignment, nothing left unresolved.

## Edge cases

- **A client is never dropped for being unknown, but its hours are.** The review flags it in §2; the build leaves the hours in `unresolved`. Only Phase 4b brings them into the month. Verified on the 2026-08 close: two new clients, 11.13 hours, which write-back alone would have silently omitted.
- **Bootstrap overrides must stay empty.** `overrides.py` ships empty on purpose. Populating it would mask a genuinely new client — the whole point of §2 is that an unknown client gets flagged. The populated version exists only for rebuilding history from the retired scope sheets and lives privately in the operator's own Drive.
- **Never add a column to the Assignments tab.** `Code.gs` rebuilds the entire row from the header and blanks any column its record does not know about, so a new column is wiped on every edit in the app. Staff and Clients are safe; Assignments is not.
- **`SnapshotRows` has eight columns, not seven.** The eighth, `staff_hours`, holds the per-person split behind each role total as `Name:hrs, Name:hrs`. `createSnapshot` fills it from the Assignments tab automatically, so the monthly flow needs no extra step — but anything that writes `SnapshotRows` directly must carry all eight, or the per-person history silently stops. It is what lets a months-long overlap be read as the handoff it is, instead of a transition window belonging to no one. Unlike Assignments, adding to this tab is safe.
- **Non-breaking spaces.** Client names arrive from QB carrying U+00A0, which silently splits one client into two. `tidy()` and `pname()` handle it — 23 names were affected when this was found.
- **Role suffixes on names.** Some sources carry a trailing role marker on a person's name (`... - S`) to denote a second role. `pname()` strips it; the role has its own column.
- **Deepest job code wins.** Resolve `<parent>: <sub>` against the client list, rolling up to the parent when it has no sub-clients. Anything unresolvable is reported, never guessed.
- **`Paxus Admin` is internal work, never time off.** It is already inside each person's client percentage; treating it as PTO double-counts.
- **Holidays are not deducted.** Capacity uses raw weekdays, which matches the operator's own figures.
- **Three kinds of time off** all reduce availability: `pto_hours` (the benefit), `banked_off_hours` (overtime bank drawn down), `unpaid_off_hours` (recorded by the operator when a shortfall is explained).
- **`capacity_mode = actual`** on the Staff tab means that person's availability tracks their real client work instead of a daily rate. It is set in the sheet, not in the app UI, and not in code.
- **Per-cell writes are far too slow.** Staff updates go through one batched call; ~200 individual writes will time out.
- **A high judgement-call count in §6 is the signal.** It means the roster is drifting out of date, not that the run went badly.
