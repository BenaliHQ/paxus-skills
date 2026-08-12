---
type: Configuration
title: Point of sale
description: POS and payment platforms, per-platform report specs, and the sales-to-deposit reconciliation rules.
schema_properties: [point_of_sale_systems, pos_report_specification, sales_deposit_reconciliation_rules]
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

How gross sales tie to deposits: TBD (netted lump sums vs. exact payouts;
some platforms charge no fees and tie exactly — say which). Fees land at:
TBD. Note whether QBO-native platform sync is on or off, and why.

# Citations

[1] TBD — populate only from the actual sources ingested during onboarding (transcript, document, export, or named person + date). Never pre-claim a source.
