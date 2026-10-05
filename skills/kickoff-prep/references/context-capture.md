# Context capture — what the kickoff should land for `/client-context`

The kickoff call is the richest single conversation the firm ever has with a new client,
and most of it happens once. `/client-context` builds the client's context bundle from a
question set (`skills/client-context/references/intake-questions.md`) whose ASK-mode items
"live in someone's head" — which means every one of them either gets answered at the kickoff
or gets chased later, one email at a time.

This document is the map. It says which bundle items the kickoff can realistically land,
where in the eleven-item spine each one belongs, and — just as importantly — which ones it
should **not** try to land.

Operator instruction, 2026-08-26: *"Can we capture some of that stuff on the front end with
the kickoff questions… so that as we continue to run this moving forward, we're not having a
lot of back and forth."*

## The honest scope of this

The kickoff lands the **head-knowledge** items — what the business is, who we talk to, how
they work, how they want to be dealt with. It does **not** land the **books-knowledge** items
— the chart of accounts, vendor coding rules, clearing accounts, recurring journal entries.
Those come out of the QuickBooks file and the first close, and asking a client about them on
a first call produces low-quality answers and burns the goodwill the call is for.

So: groups A, C2, E, G and the workflow half of D are in reach at kickoff. The rest is not,
and saying otherwise sets the lead up to look unprepared. **Never present this as "the bundle
is now complete."**

## Rules for using this map

1. **The eleven-item spine does not change.** Items are fixed by the controller
   (`references/call-agenda.md`). These questions ride *inside* existing items. Never add an
   item, never reorder.
2. **If the dossier already answers it, don't ask it.** Re-asking a client something firm
   admin already collected is the fastest way to look disorganized. The prep notes carry what
   is already known; the agenda carries only what is genuinely open.
3. **Cap it at three or four added questions per item**, and never at the cost of the item's
   own purpose. Item 4 is about the timeline; it does not become a questionnaire.
4. **Plain client language, always.** *"What do you need to be able to see the numbers cut
   by — by job, by location, by program?"* — never *"classification_tracking."*
5. **Conditional items stay conditional.** A formal source-document policy is a nonprofit /
   CFO-scope question. Payroll rules only where payroll is in scope. Bill pay only where bill
   pay is in scope. An off-scope question makes the client wonder what they bought.
6. **Deferring is a real answer.** An item marked *defer* below is not a failure — it is
   scheduled for the place where it gets a better answer.

## Ask at kickoff

| Item | Bundle | What to ask, in client language |
|---|---|---|
| **02** Client intro | A4 industry | What the business actually is — what they sell, how many locations, revenue streams, busy and slow seasons. |
| **02** | A5 founded_year | How long they've been at it. |
| **02** | A6 ownership | Who owns it and who's involved day to day. *Nonprofit: board governance, and who the treasurer or finance chair is.* |
| **02** | A3 entity_relationships | Any other entities — and whether we keep their books. Also who does the tax return, and the auditor if there is one. |
| **03** Meet your team | A10 client_contacts | Who on their side we'll be talking to, and what each of them handles. |
| **03** | C2 response_owner_matrix *(client half)* | Who answers a question about a transaction, versus about the financials, versus about the engagement itself. |
| **03** | G9 escalation_map | If we can't reach their day-to-day person, who unblocks us. *Nonprofit: which board member.* |
| **05** Communication | A12 working_with_this_client | How they prefer to hear from us, whether they'll actually use the portal, and how quickly they can usually turn things around. |
| **05** | E3 authentication_requirements | Which of their systems will challenge us for a code, **how often**, and where that code lands. Frequency and complexity are the point — "it has 2FA" answers nothing. |
| **05** | E1 / E2 credential_locations, access_assignments | Where each login will live and who's assigned. **Pointer only — never the value.** |
| **06** Gathering information | D14 / D15 financial_accounts | Per account: which institution, what it's used for, and **who pulls the statement each month** — them or us. Nicknames and last-four only. |
| **06** | D10 loan_schedules | Any loans or notes, and whether an amortization schedule exists anywhere. |
| **06** | F2 / F3 tax baseline and contact | Most recent filed return, and who prepares it — plus how we should reach them. |
| **07** Monthly workflow | D2 accounting_method | Cash or accrual — for the financials and for the tax return. |
| **07** | D3 fiscal_year_end | Year end. *Nonprofits are often June 30 — ask, don't assume.* |
| **07** | D5 classification_tracking | What they need the numbers cut by — by job, by location, by program, by department. The single highest-value question on this list for job-cost businesses. |
| **07** | D9b recurring_journal_entries *(hand-computed half)* | Which month-end entries someone works out by hand each period rather than QuickBooks posting them automatically — cost allocations, wage splits across programs or jobs, drawing down money received up front, accruals. For each one: what report it comes off, who works it out, and how we check it. *Head knowledge — no export will ever find these.* |
| **07** | D7 materiality *(client-facing half)* | What we should just code and what they always want to be asked about. |
| **07** | D26 client_question_send_schedule | How often they want the open-questions list — weekly, monthly, twice a month. |
| **07** | A12 *(their side)* | What they'll be doing each month to support us, so it's said out loud once. |
| **07** | D18 source_document_attachment_policy | *Conditional — nonprofit or CFO scope only.* Whether receipts and source documents have to be attached, and whether they'll do it. |
| **08** Reporting preferences | B8 delivery_configuration | Who should receive the financials, in what format, and by when in the month. |
| **08** | B11 custom_financial_reports | Anything they need beyond a P&L and balance sheet. |
| **08** | D11 budget_configuration | Whether there's a budget, who builds it, and whether a board approves it. |
| **09** Tools and training | D19 / D20 point_of_sale | Any POS, payment, or donor platform in the mix — and how we'd get the monthly report out of it. |
| **09** | D23 payroll_processing_rules | *Where payroll is in scope.* Who approves it, and whether wages get split across jobs, locations, or programs. |
| **09** | D25 bill_payment_configuration | *Where bill pay is in scope.* Who approves a bill before it goes out. |
| **10 / 11** Open floor, 90-day | G7 meeting_calendar | Standing dates that move our timing — board meetings, standing calls, anything with a hard date. |
| **10 / 11** | H2 advisory_service_plan | *Advisory or CFO scope only.* Cadence, who attends, what they expect out of each session. |

## Deliberately not at kickoff

Record these as deferred, with where the answer actually comes from. Never leave them looking
like the call failed to get them.

| Bundle | Where it comes from instead |
|---|---|
| D4 chart_of_accounts | The COA export and the QuickBooks review. |
| D6 vendor_coding_rules | The first close, and the bank-rule export. |
| D8 transfer_and_clearing_rules | The file — visible in the accounts, not in the client's head. |
| D9 recurring_journal_entries *(QBO templates only)* | The recurring-transactions export. **Only the templated half** — the hand-computed close entries (D9b) are head knowledge and are asked at item 07 above. |
| D21 sales_deposit_reconciliation_rules | The first month's tie-out. |
| D24 sales_tax detail *(jurisdictions, logins)* | The dossier flag plus item 6 pointers; the detail follows. |
| D7 exact thresholds | Ours to set, informed by what the client says at item 7. |
| F4 year_end_close_requirements | *Partial exception:* on a nonprofit, ask when the audit lands — that date moves our work. |
| G3 cleanup_outcomes | The end of cleanup. |
| C1 / C3 / C4 internal economics | Never client-facing. Already in the prep notes. |

## Where the answers go

- **Prep mode** writes a **Client context to capture** section into the prep notes — internal,
  grouped by bundle letter, with anything the dossier already answered marked *already known*
  so the lead doesn't re-ask it. Only the genuinely open questions reach the agenda.
- **Debrief mode** fills that same section from the transcript, each item marked *answered* ·
  *partly answered* · *not reached* · *deferred by design*, with the client's own words where
  they're worth keeping.
- `/client-context` then reads the prep notes as a source. It still cites and verifies for
  itself; this section is a well-organized input, not a bypass of its own rules.

**Never write into the bundle from this skill.** The bundle is `/client-context`'s to build.
This skill's job is to make sure the answers exist somewhere it can find them.
