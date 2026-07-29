# JIB Coding Reference

The generalizable knowledge for coding an oil & gas JIB for a non-operated
working-interest owner. **Client-neutral by design** — no client names, wells,
operators or figures. Per-client specifics live in that client's `.agents/` context
bundle; see the skill's "Load the client's fuel first".

---

## Reading the JIB

Formats differ by operator, but the cost categories map consistently. Look for these
section headers or AFE codes within each well:

| What's on the JIB | Category |
|---|---|
| Intangible Well Cost (IDC) | **Well Costs — IDC** |
| Drilling intangibles, completion intangibles | **Well Costs — IDC** |
| AFE -10 capital costs (drilling) | **Well Costs — IDC** (mostly) |
| AFE -20 capital costs (completion) | **Split by line type** — see below |
| Tangible Well Cost | **Equipment** |
| Equipment Beyond Wellhead | **Equipment** |
| Surface Equipment | **Equipment** |
| Lease Operating Expense (LOE) | **Lease Operating Expense** |
| Production overhead, field labor | **Lease Operating Expense** |
| Compression, chemicals, pumping (producing well) | **Lease Operating Expense** |
| Saltwater Disposal / SWD (producing well) | **Lease Operating Expense** |
| Cash Call (positive, current period) | See Cash calls |
| Cash Call Credit (negative, being applied) | See Cash calls |

**This mapping — not a dollar amount — decides whether a cost capitalizes.** Resolve
each category to the client's real QBO account name before writing the file; the
capitalizing account often sits under fixed assets while the two expensed categories
sit under COGS, and the exact strings are per-client.

### AFE -10 vs AFE -20

Some operators split each well into **AFE -10** (drilling capital) and **AFE -20**
(completion capital), and within each AFE into Intangible Well Cost, Tangible Well
Cost, and Equipment Beyond Wellhead.

**Code each line by what it is, not by which AFE it sits under.** A "Tangible Well
Cost" line under AFE -10 is still Equipment.

### Well stage changes the answer

**The same cost type lands in different categories depending on well stage.**

* Active drilling / completion → **IDC** and **Equipment**
* Producing well → **LOE**

**Production Fluid Disposal / SWD is the recurring judgment call.** Default to LOE on
a producing well, but **check the dates** — costs dated during active completion,
before the well was producing, may be IDC. Mixed dates → split by date. **Flag the
judgment rather than deciding silently.**

### Negative lines are sometimes legitimate

A category can net negative when a credit exceeds the other lines in it — for example
a separation-and-treating equipment credit outweighing the rest of the equipment
lines. **Code it negative; it is not an error.** Put "net" in the description so the
intent is legible.

---

## Cash calls — the most common source of error

Cash calls are prepayments to the operator for upcoming drilling or completion work.
They appear two ways, and **the correct entry depends on history, not on the document
in front of you.**

**1. Operator collects a new cash call** (positive on the JIB, increases what's owed)

* Code to the client's **prepaid expenses** account where one exists — check their
  `transfer-and-clearing-rules.md`.
* If no prepaid account exists, code to **Well Costs — IDC** as a placeholder and
  **flag it for correction**.

**2. Operator applies a prior cash call as a credit** (negative, reduces what's owed)

The original coding decides the answer:

| Where the original cash call sits | Correct handling |
|---|---|
| **Prepaid expenses** | Credit prepaid for the credit amount; code the gross costs to their normal categories. |
| **Well Costs — IDC**, in a **prior closed period** | **Reduce the IDC line on the current check** by the credit amount. **Do not recode the closed period.** |

**Always ask the controller where the original cash call was coded before deciding.**
The document does not tell you, and guessing produces a wrong entry that reconciles.

A client may have a standing arrangement to be **billed monthly instead of paying
lump-sum cash calls**. Where that is the case (their bundle will say), a new lump-sum
cash call is an exception worth confirming rather than routine.

---

## The check amount

**Cut for the current period / new invoices only — never the total statement
balance.**

JIBs commonly show current balance due, over-30/60/90 aging, and a total. Pay the
current period; **flag any prior balance and ask** whether it should be paid
separately or has already been entered as A/P. Do not include a prior balance without
confirmation.

---

## Reconciliation

Two ties, both required, before the file is produced:

1. Each well's IDC + Equipment + LOE = that well's net amount on the JIB summary.
2. Sum of all well totals = the invoice total.

Verify with python. A penny or two of rounding is normal. **Dollars off means
something is miscategorized — stop and find it rather than forcing the tie.** If the
variance equals a cash call or credit amount, that is the cause.

---

## Classes, locations, and new wells

* Take the value list from the client's `classification-tracking.md`. **That is the
  authority** — a list embedded in a skill goes stale and drifts from QBO.
* Use the **exact live strings**. Clients' well names are usually longer and more
  qualified than their conversational short forms, and an approximate value creates a
  duplicate class on entry instead of matching.
* **A well not on the client's list needs setup before entry.** Flag it; never code to
  an approximate neighbour.
* Some clients track newer wells by **location** and older ones by **class**; others
  use one dimension for everything. The bundle says which. The Excel column header
  stays **CLASS** (the QBO check-entry label) — note in chat only when a value truly
  belongs on the other dimension. **If the client uses a single dimension, emit no
  flag at all.**

---

## Vendors and operators

* **New operators appear regularly.** Flag vendor setup and keep working; don't pause.
* **If a familiar well appears under a new operator, flag it** — it may be a sale, a
  partial-interest sale, or an operator change, and it needs the client's answer.
  Check whether the client's chart has divestiture or gain-on-sale accounts that a
  disposition would have landed in.

---

## Patterns worth remembering

1. **Reconcile by well first**, then sum to the invoice total. Anything off by more
   than a penny, stop and find out why.
2. **Producing wells = LOE; drilling and completion = IDC and Equipment.** The same
   cost type lands differently depending on stage.
3. **Cash calls are the most common source of confusion.** Always establish where the
   original was coded.
4. **New operators show up regularly.** Flag vendor setup, don't pause the work.
5. **Operator changes happen.** A familiar well under a new operator is a question for
   the client, not a coding decision.
6. **Capitalization is by line type, not amount** — unless the client's bundle records
   a threshold, don't invent one.
