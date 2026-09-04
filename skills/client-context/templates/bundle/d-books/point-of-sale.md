---
type: Configuration
title: Point of sale
description: POS and payment platforms, per-platform report specs, the sales-to-deposit reconciliation rules, and the month-end cut-off that drives accrued sales.
schema_properties: [point_of_sale_systems, pos_report_specification, sales_deposit_reconciliation_rules, sales_accrual_and_cutoff]
status: scaffold
---

# Platforms

| Platform | Access method |
|---|---|
| TBD (Stripe / PayPal / Toast / Venmo / Shopify) | Cloud Protect / read-only API / scheduled email |

# Report specification

| Platform | Report | Period | Delivery path | Destination |
|---|---|---|---|---|
| TBD | sales summary | | | |

# Deposit reconciliation

**What the reconciliation authority is, per channel:** TBD — the *payout*, or
a *statement* the platform or manager sends. Where a statement governs, the
statement **is** the reconciliation and there is no gross-to-net difference to
chase; say so plainly rather than forcing a tie-out that doesn't exist.

How sales tie: TBD (netted lump sums vs. exact payouts; some platforms charge
no fees and tie exactly — say which). Fees land at: TBD — netted against
income, or grossed back up into their own expense accounts. Note whether
QBO-native platform sync is on or off, and why.

# Period cut-off — accrued sales

Revenue earned inside the period whose payout or statement lands after month
end. This is where accrued revenue lives on POS and statement-driven channels.

| Channel | Settlement lag | Accrued into the period? | Support | Who computes it | Where in-transit sits |
|---|---|---|---|---|---|
| TBD | | | | | |

> [!warning] Watch for a statement window that straddles month end
> Where a platform or property manager issues a statement covering, say, the
> 20th of the prior month through the 11th of the current one, deposits are
> split in the **statement's** month rather than the month they land. That
> window sets both the accrual and the close's critical path — if the statement
> is late, the close is late. Record the actual dates, not "monthly."

**If nothing accrues** — every channel settles same-day and there is no
cut-off exposure — state that explicitly. An empty section reads like the
interview never got here.

*Conditional:* where gift cards, prepaid tuition, deposits or retainers run
through the same channel, record the **deferred**-revenue side here too — money
taken in before it is earned, and what draws it down.

Related: the accrual usually posts as a month-end entry — see
[recurring journal entries](/d-books/recurring-journal-entries.md). In-transit
balances live in a clearing or undeposited-funds account — see
[transfer & clearing rules](/d-books/transfer-and-clearing-rules.md).

# Citations

[1] TBD — populate only from the actual sources ingested during onboarding (transcript, document, export, or named person + date). Never pre-claim a source.
