# Rules, exclusions and edge cases

## 1099 rules (2026 tax year)

- Threshold $2,000 for NEC and MISC (the template's OVER 2000 column). Interest: 1099-INT
  at $600+ of interest paid to a non-bank lender. Principal is never reportable.
- Corporations (C and S) get no 1099, except attorneys and law firms (legal services or
  gross proceeds) and medical or health care providers.
- LLCs follow their tax classification on the W-9; an LLC box with no classification is
  not a corporation. Single-member LLCs and sole proprietors get a 1099.
- Card-paid payments are excluded (the card company reports them on 1099-K). So are
  PayPal and Venmo business payments. Zelle and ACH come from the bank: they count.
- Bills paid by card are excluded automatically (the script drops Bill Payment (Credit
  Card)); no A/P spot-check is needed with this method.
- Filing and W-9 requests go through Tax1099, not QBO or FC. The controller files.
- Dates for the 2026 tax year: client email for vendor emails as early as the evaluation is
  done (by 12/5 at the latest); W-9 cut-off Monday 1/11/2027; filing deadline 2/1/2027.
  Check the Quick Reference each year.

## Excluded automatically (the script; listed on the sheet's "Not included" line)

Payroll providers (Gusto, ADP, Paychex, payroll services) and wages; tax agencies and tax
payments; utilities; bank fees; insurance; owner pay, draws and distributions; credit card
payments; title companies, closings and earnest money; merchant and QuickBooks fees.
Contractors paid through a payroll provider get their 1099 from the provider: if a payroll
provider's payments look like contractor payments, flag it.

## Edge cases

- **Names that don't match across systems** (QBO name, legal name, Drive name): resolve
  with the bundle's `workspace-locations.md`; ask when two candidates fit.
- **Several companies for one client**: one evaluation file per QuickBooks file.
- **No payee**: bank outflows with a blank Name and journal-entry lines with no Name are
  checked in step 2.4; a payee found in a memo is flagged with its total.
- **Clients onboarded with bulk journal entries**: payees only appear if the memo names
  them; say how much of the year has no payee and flag it for the lead.
- **Refunds, credits, voids**: a negative or very small total is listed in `summary.md`;
  check before evaluating.
- **One payee under two names** (a person and their business; a company that renamed):
  flag; the W-9 decides which name and TIN are filed. A vendor that is also a customer is
  normal; keep only payments.
- **Owners, family, related companies, employees**: never decided by the skill; flag.
- **Foreign vendors** (W-8BEN), **trusts and estates**, **government entities**: flag for
  the controller.
- **Rent**: MISC Box 1 when paid to an individual or non-corporate LLC; a payee called
  "Rent" needs the landlord's real name from the client.
- **Loans**: banks are exempt; a private lender with $600+ of interest gets a 1099-INT; the
  loan should be tied out at 12/31 before the INT goes out, but a missing statement doesn't
  hold up the client's other forms.
- **Vendors just under $2,000** ($1,500–$1,999.99): the January watch list.
- **Existing evaluation file**: never make a second one; rebuild in place only on the
  person's okay; year-end adds a tab and never overwrites typed answers.
- **Large clients**: page the vendor pull to files (a subagent in Claude Code); write the
  sheet in 5,000-cell chunks; extend the K and O formulas past the template's last row.
- **W-9 attached in QBO but not in Drive**: Drive is the source of truth; list it so the
  person saves a copy (the firm connection can't move QBO attachments).
- **A tracker in someone's My Drive**: the firm connection can't reach it; ask to move it to
  the trackers folder.
