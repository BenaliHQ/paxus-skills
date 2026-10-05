---
name: jib-to-check-coding
description: Use this skill whenever a JIB (Joint Interest Billing) invoice or invoice summary from an oil & gas operator is uploaded for a working-interest client and a check needs to be cut or coded. Triggers include any mention of a JIB, phrases like "code this JIB", "create a check for this", "cut a check to [operator]", or an invoice upload with well-level cost detail. Produces a QBO-ready Excel file with CATEGORY, DESCRIPTION, AMOUNT, CLASS columns that ties to the invoice's current-period balance exactly. Client-neutral — reads the client's accounts, classes, operators and thresholds from that client's context bundle.
---

# JIB to Check Coding

Convert an oil & gas **JIB** (Joint Interest Billing) into a QBO-ready check-coding
Excel file. Output columns: **CATEGORY, DESCRIPTION, AMOUNT, CLASS**, tying to the
invoice's current-period balance exactly.

This skill is the **engine**. Everything client-specific — which QBO accounts the
categories map to, the class/location list, known operators, materiality gates,
owner-expense treatment — is **fuel, and lives in the client's context bundle**, not
here. See "Load the client's fuel first" below.

## When this skill applies

Any non-operated **working-interest** client whose costs arrive as operator JIBs.
Works for any operator, including ones the firm hasn't seen before.

## Load the client's fuel first

Before coding anything, read from the client's `.agents/` context bundle (built by
`/client-context`):

| Read this | For |
|---|---|
| `/0-core/client-critical-rules.md` | The client's hard constraints. Read first, always. (Bundles built before template 1.1.0 have this file at the bundle root.) |
| `/d-books/chart-of-accounts.md` | **The client's actual QBO account names** for the three categories. Do not assume the names in this skill's reference — a client's capitalizing account may sit under fixed assets while the expensed ones sit under COGS, and the exact colon-qualified strings differ per client. |
| `/d-books/classification-tracking.md` | Whether the client tracks by **class**, **location**, or both, the rule for which applies, and the **live list of values**. This is the authority — never a list hard-coded in a skill. |
| `/d-books/vendor-coding-rules.md` | Known operators, owner-expense patterns, confidence markers. |
| `/d-books/transfer-and-clearing-rules.md` | Cash-call handling and whether a prepaid account exists. |
| `/d-books/materiality-thresholds.md` | What may be coded without asking, and what goes to the questions list. |

**No bundle for this client?** Say so and ask before proceeding — do not invent the
mapping. A wrong account or a wrong class is worse than a delayed check.

## The workflow

1. Read the JIB and identify each well's costs split by category.
2. Reconcile each well's components to its total, and the wells to the invoice total.
3. Build the QBO-paste-ready Excel file.
4. Flag setup needs and judgment calls in chat.

Always reconcile the math before producing the file. **If something doesn't tie, ask
before guessing.**

See `references/coding-reference.md` for the full category mapping, the AFE
structure, well-stage rules, the cash-call decision tree, and the check-amount rule.

## The three categories

Every JIB line lands in exactly one of:

* **Well Costs — IDC** — intangible drilling costs. Expensed.
* **Equipment** — tangible well equipment. **Capitalized.**
* **Lease Operating Expense** — producing-well operating costs. Expensed.

**Capitalize-vs-expense is decided by the JIB line's expense type, not by a dollar
amount.** Unless the client's bundle records a capitalization threshold, do not apply
one. Resolve each category to the client's real account name from their
`chart-of-accounts.md` before writing the file.

## Reconciling the math

Two ties, both required:

1. Each well's IDC + Equipment + LOE = that well's net amount on the JIB summary.
2. Sum of all well totals = the invoice total.

Use python to verify. A penny or two of rounding is normal; **dollars off means
something is miscategorized — stop and find it.** If the variance equals a cash call
or credit amount, that is the cause.

## Class and location values

Take the value list from the client's `classification-tracking.md`, and use the
**exact live strings** — clients' well names are often longer and more qualified than
their conversational short forms, and an approximate value creates a new class on
entry rather than matching the existing one.

**A well not on the client's list needs setup before entry** — flag it; don't code it
to an approximate neighbour.

If the client tracks some wells by **location** rather than class, the bundle says so
and says which. The Excel column header stays **CLASS** because that is the QBO
check-entry screen's label; note in chat when a value belongs on the other dimension
so the reviewer can adjust. **If the client uses only one dimension, say nothing —
don't emit a flag that is always wrong.**

## Halt conditions — ask, don't guess

Stop and ask the controller when:

* The math doesn't tie beyond a cent or two.
* A cash-call credit appears and the original cash call's coding is unknown.
* A prior statement balance appears and it's unclear whether it's already in A/P.
* Production-fluid-disposal or saltwater-disposal dates straddle completion and
  production.
* An unfamiliar operator appears, or a familiar well appears under a new operator.
* The client has no context bundle, or its account mapping is marked unresolved.

## Building the Excel file

Read the xlsx skill's own guidance before building. Use
`references/excel_template.py` as the starting point — it is client-neutral; replace
the placeholder vendor, invoice, month, total and rows.

* Sheet name: `Check Coding`
* Header rows 1–4: Vendor, Invoice #, Accounting Month, Check Total
* Header row 6: `CATEGORY | DESCRIPTION | AMOUNT | CLASS` — Paxus burgundy `#682145`,
  white text, bold
* Data rows from row 7; total row uses a `SUM` formula, never a hardcoded value
* Font Arial 11; currency format `$#,##0.00;($#,##0.00)` (parentheses for negatives)
* Column widths: A=28, B=75, C=14, D=30
* Filename: `{Operator}_Check_Coding_{Month}_{Year}.xlsx`
* Recalc formulas after saving, then share the file

> [!note] Runtime paths
> The template's recalc step references the xlsx skill's script path. That path
> differs between the Claude web/desktop runtime and a local workstation — resolve it
> for wherever this is running rather than assuming.

## Description text patterns

Short but specific, and always carrying the JIB month so the audit trail is clear:

* `AFE -10 IDC - Transportation (Mar 2026 JIB)`
* `LOE - SWD, supervision, chemicals (Mar 2026 JIB)`
* `Completion - Logging/Wireline (Mar 2026 JIB)`
* `AFE -20 Equipment Beyond Wellhead, net (Mar 2026 JIB)`

When a line nets negative (a legitimate credit on the JIB), include "net" in the
description so it reads as intentional.

## What to say in chat

Keep it brief — the Excel file is the deliverable, not a restated table.

1. **One-line summary** — total split by category.
2. **Setup needed** — new vendors, classes or locations to add in QBO before entry.
3. **Judgment calls flagged** — PFD treatment, cash calls, prior balances, operator
   changes.
4. **Math notes** — anything that required rounding to tie.

## Recording what you learn

A durable coding decision belongs in the **client's bundle**, not in this skill:
a new vendor rule goes to their `vendor-coding-rules.md`, a resolved cash-call
question to their `transfer-and-clearing-rules.md`, with a citation and a `log.md`
entry. **Never add a client's wells, operators, or figures to this skill** — that is
what made the previous version stale and client-specific.
