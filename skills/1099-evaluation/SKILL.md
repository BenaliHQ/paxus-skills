---
name: 1099-evaluation
description: Build and evaluate one client's 1099 vendor file for a lead or controller - pull every bank-paid vendor from QuickBooks, build the evaluation file in the client's Taxes > 1099 folder from the Google Sheets master template, evaluate every vendor at $2,000+, check W-9s, add the controller's tracker rows, and hand back the client email, Financial Cents note and subtasks, QBO fixes and flags. Two paces (walk through step by step while learning, or run straight through) and two modes (initial in the fall, year-end in January on a new tab). Use when someone says "run the 1099s for <client>", "walk me through <client>'s 1099s", or "1099 year-end rerun for <client>". Needs the Agent Base connection (QuickBooks, Google Drive, Financial Cents). The controller's Tax1099 filing stays manual.
---

# 1099 evaluation

This is the paxus-skills copy of the Agent Base skills `1099-evaluation-core`,
`1099-evaluation-walkthrough` and `1099-evaluation-run-through`. Keep the two in step until
the Agent Base versions are in use by everyone; then retire this one.

## Before you start

Ask (once, together): the client; the mode (initial, or year-end in January); the pace
(walk through step by step, or run straight through); and the runner's name and role (lead
or controller). Everything runs through the Agent Base connection; if `connections_list`
doesn't answer, stop and say the connection is missing.

## Outcome

1. The client's evaluation file in `[Client] > Taxes > 1099 > <year>`, built from the master
   template: every bank-paid vendor with its transactions, a "Total for" row each, and the
   tests answered for every vendor at $2,000+.
2. In the conversation: the client email asking for missing vendor emails, the Financial
   Cents (FC) note, the FC subtasks, the QBO fix list, and the flags that need a person.
3. New rows in the controller's own Tax1099 W-9 request tracker.

## Fixed locations

| What | Where |
|---|---|
| Master template (Google Sheet) | `1gW5uDdH9-v0AObECjHNdL1aWpptkoS1wpOXdDuf3DIY` (Paxus CPA shared drive > 1099 Training Documents) |
| Controller trackers | Paxus CPA shared drive > Admin > 1099s (`1FmyCAibl1CSNLGPZ0Meq-XMy-lYyr6Oh`) > `<year> W-9 Request Trackers`; one Sheet per controller named `Tax1099 W-9 Request Tracker – <Controller>` |
| Prior-year history, 2025 tax year | "2025 Paxus 1099" Sheet `1tX19C5N0SiJihuRCwcYzkQZyRkfTa2gBU0oAU2CO58o`: per-person tabs; client name in column A, its vendor rows below from column I. From 2026 on, last year's evaluation file |
| Firm procedures | Agent Base context `processes/1099-filing-process.md`; Drive 1099 Training Documents |

## Procedure

1. Setup: `references/1-setup.md`.
2. Pull QuickBooks and build the rows: `references/2-pull-and-build.md`.
3. Evaluate and write the file: `references/3-evaluate.md`.
4. Outputs: `references/4-outputs.md`.
5. Year-end mode only: `references/5-year-end.md`.
6. When the client replies or W-9s come back: `references/6-follow-up.md`.

### Pace: walk through (while learning)

Stop for the person's okay after each step: after the plan (step 1); after the pull, showing
the $2,000+ list, watch list and what was excluded (step 2); after the evaluation, one line
per $2,000+ vendor (steps 3.1–3.2); after writing the file, with the link and YES / CHECK /
NO counts (step 3.3); and before appending tracker rows (step 4.5). Keep each stop short:
what happened, what's next, the question.

### Pace: run straight through

One stop: the plan in step 1, with every write listed. After that, run steps 2–4 (and 5)
without stopping; judgment calls go on the flag list. Reply once at the end: the file link,
counts and watch list, the flags (numbered, most material first), then the client email, FC
note, FC subtask blocks, QBO fixes and tracker rows added. A write outside the plan: stop
and ask first.

## Standing rules (always)

`references/rules.md` holds the 1099 rules, exclusions and edge cases. The ones people have
corrected before:

- **W-9 REQUESTED (date)** is only the date the Tax1099 request went to the vendor. Asking
  the client for emails goes in NOTES ("Asked <client contact> for email MM/DD/YYYY").
- **Never flag a possible missed prior-year 1099.** The firm will not file late for past
  years. Use last year only to learn whether a W-9 is already on file.
- **Don't flag a missing EIN for a vendor that won't get a 1099.**
- **FC subtasks** go in one code block per parent task, one item per line, no bullets or
  commas, the first time (`references/4-outputs.md`).
- **One list, alphabetical**, with full transaction detail; never a summary block below TOTAL.
- A missing TaxIdentifier from the QBO API does not prove there is no TIN. Check the W-9.

## Side effects and approval points

Writes, each dry-run first and only after the okay the pace calls for: `google.folder.create`,
`google.file.copy` (the template), `google.sheet.update` / `sheet.clear` / `sheet.tab.add` /
`sheet.format` / `sheet.layout` (the evaluation file), `google.sheet.append` or `sheet.create`
(the tracker). Never send email (Agent Base has no mail access; a Gmail draft only if this
session has the person's own Gmail tool); never write to Financial Cents or QuickBooks;
never contact the client or a vendor.

## Acceptance criteria

- Every $2,000+ vendor answered, or CHECK with the reason in NOTES.
- The YES / CHECK / NO counts reported match the sheet read back.
- FC subtasks in the one-block-per-parent format; W-9 REQUESTED left empty.

## Failure and escalation

- Client, shared drive or Drive access not found: stop and say which; never guess between
  two matches.
- Master template missing or its row 5 headers changed: stop; don't build from an old copy.
- Client in the FC "NO 1099" group or no FC 1099s project: say so and stop unless told to go on.
- A Sheets write refused: stop, report the range, write nowhere else. If stopping partway,
  say what was written and where.
