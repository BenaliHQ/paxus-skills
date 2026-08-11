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

```python
from build_month import build
a, s, r = build('<YYYY-MM>', None, '<timesheet.csv>', {}, None, app_path='app.xlsx')
```

The old staff scope spreadsheet is **not** part of this loop. Do not read capacity from it.

### Phase 3 — Produce the review

```python
from review import render, coverage, save
text = render('<YYYY-MM>', a, s, r, coverage('<timesheet.csv>', '<YYYY-MM>'))
path = save(text, '<YYYY-MM>')          # -> the runner's own ~/Downloads
```

Print `text` verbatim to the operator and tell them where the file was saved.

### Phase 4 — Stop and wait

Sections 2, 3 and 5 are questions. Do not proceed until they are answered:

- **§2 New clients** — hours logged against something with no entry in the app. Get the team and budgets. A client with hours but no entry is *flagged, never dropped*.
- **§3 Hours short** — recorded less than a full month with no reason on file. If the operator knows why, record it in the Staff tab's `unpaid_off_hours`; if not, those are conversations for them to have, not something to resolve here.
- **§5 Client phase** — the 20–50% onboarding band is deliberately undecided, and clean-up coded on an Active client is a flag. Both are the operator's call.

If reconciliation in §1 does not balance, **stop entirely** and say so. Do not write a month that does not tie.

### Phase 5 — Write back

Only after approval:

```python
from writeback import write_month
plan = write_month(SHEET_ID, '<YYYY-MM>', a, s,
                   new_clients=[...],   # approved in §2, or omit
                   dry_run=True)        # review the plan first
```

Show the plan (rows to write, rows replaced, staff updated, anything unmatched). If `unmatched` is non-empty, resolve it before applying. Then re-run with `dry_run=False`.

This replaces the Assignments tab wholesale with this month's rows and updates the numeric columns on Staff. It does **not** touch email, status, `client_pct`, `daily_rate` or `capacity_mode`.

### Phase 6 — The operator captures the snapshot

Snapshotting stays in the app so there is one implementation of that logic rather than two that can drift. Tell the operator to open CapacityIQ and capture the snapshot for the period.

Then verify: reconciliation balanced, the app total ties to client hours, no departed staff on a live assignment, nothing left unresolved.

## Edge cases

- **Bootstrap overrides must stay empty.** `overrides.py` ships empty on purpose. Populating it would mask a genuinely new client — the whole point of §2 is that an unknown client gets flagged. The populated version exists only for rebuilding history from the retired scope sheets and lives privately in the operator's own Drive.
- **Never add a column to the Assignments tab.** `Code.gs` rebuilds the entire row from the header and blanks any column its record does not know about, so a new column is wiped on every edit in the app. Staff and Clients are safe; Assignments is not.
- **Non-breaking spaces.** Client names arrive from QB carrying U+00A0, which silently splits one client into two. `tidy()` and `pname()` handle it — 23 names were affected when this was found.
- **Role suffixes on names.** Some sources carry a trailing role marker on a person's name (`... - S`) to denote a second role. `pname()` strips it; the role has its own column.
- **Deepest job code wins.** Resolve `<parent>: <sub>` against the client list, rolling up to the parent when it has no sub-clients. Anything unresolvable is reported, never guessed.
- **`Paxus Admin` is internal work, never time off.** It is already inside each person's client percentage; treating it as PTO double-counts.
- **Holidays are not deducted.** Capacity uses raw weekdays, which matches the operator's own figures.
- **Three kinds of time off** all reduce availability: `pto_hours` (the benefit), `banked_off_hours` (overtime bank drawn down), `unpaid_off_hours` (recorded by the operator when a shortfall is explained).
- **`capacity_mode = actual`** on the Staff tab means that person's availability tracks their real client work instead of a daily rate. It is set in the sheet, not in the app UI, and not in code.
- **Per-cell writes are far too slow.** Staff updates go through one batched call; ~200 individual writes will time out.
- **A high judgement-call count in §6 is the signal.** It means the roster is drifting out of date, not that the run went badly.
