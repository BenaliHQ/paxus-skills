---
type: Coding Rules
title: Vendor coding rules
description: Vendor to account/class/treatment rules with confidence markers, plus owner personal-expense handling. The highest-value file.
schema_properties: [vendor_coding_rules]
status: scaffold
---

# Existing QBO bank rules

Firm policy: existing QBO bank rules are kept, not replaced by AI coding.
Fix a broken rule in QBO; don't work around it. Export: TBD.

# Vendor rules (beyond the QBO rules)

Confidence markers: **always** = code it without verification. **default** =
code it, but verify when the amount exceeds the
[materiality threshold](/d-books/materiality-thresholds.md).

Precedence: the materiality gates and the source-document policy override
vendor confidence — an "always" vendor still lands on the questions list if
the amount breaches a gate or required documentation is missing. Anything
unmatched by a rule or a listed vendor goes to the questions list.

| Vendor | Account | Class | Treatment | Confidence |
|---|---|---|---|---|
| TBD | | | | always / default |

# Owner personal-expense rows

Treatment follows entity type (draws vs. distributions vs. shareholder loan);
see [profile](/a-identity/profile.md).

| Pattern (who / which card) | Treatment |
|---|---|
| TBD | |

# Citations

[1] TBD — populate only from the actual sources ingested during onboarding (transcript, document, export, or named person + date). Never pre-claim a source.
