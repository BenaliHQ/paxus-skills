---
type: Schedule
title: Recurring journal entries
description: "The recurring transactions actually scheduled in QBO, plus the hand-computed monthly entries the close depends on: type, source report, accounts, timing, validation."
schema_properties: [recurring_journal_entries]
status: scaffold
---

# Scheduled in QBO

From the recurring-transactions export (D9). One row per template.

| Template | Type | Schedule | Amount | Notes |
|---|---|---|---|---|
| TBD | | | | |

**Deliberately not recurring:** TBD — any JE suppressed because a skill
generates it. If nothing, say so explicitly.

# Maintained outside the recurring templates

These run as part of the close but are **not** QBO recurring templates — each
needs judgment or an external input every period, so the export above will
never show them. From D9b (interview-only). Typical shapes: functional/admin
cost allocations, payroll allocation splits, amortization draw-downs of
up-front grant or contract receipts, deferred-revenue recognition,
non-templated depreciation, accruals and their reversals, full-year entries
that pay down over the year.

| Entry | Source report | Who computes it | Timing | Validation |
|---|---|---|---|---|
| TBD | | | | |

> [!warning] Do not carry split percentages forward
> Where an entry depends on a split (payroll, admin allocation, prepaid
> spread), record **where the current split lives** rather than the numbers
> themselves. The percentages change, and a stale split in this file is worse
> than no split at all.

**If this section is genuinely empty**, state that the whole close runs off
the QBO templates — don't leave the heading looking like the interview
failed to reach it.

Related: [loan schedules](/d-books/loan-schedules.md) and the
[fixed asset schedule](/d-books/fixed-asset-schedule.md) both link back to
their depreciation/amortization entries here. Payroll splits are specified in
[payroll](/d-books/payroll.md); this file records the entry that posts them.

# Citations

[1] TBD — populate only from the actual sources ingested during onboarding (transcript, document, export, or named person + date). Never pre-claim a source.
