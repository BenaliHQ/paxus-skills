# Client Context Intake — The Question Set

Every question that must be answered to build a complete client context
bundle. The interview (or kickoff transcript, or form submission) answers
these; the answers fill `templates/bundle/`. Run the full set by default;
skip a block only when the CONFIRMED service scope (B3) excludes it — never
because of a tier name.

**Capture modes.** Not every property is an interview question. Each item is
tagged:

- **ASK** — lives in someone's head; the interview is the source.
- **CONFIRM** — already captured somewhere (Financial Cents, the master
  tracker, the client overview questionnaire, Drive); the question is
  "confirm it's current and give me the pointer."
- **DOCUMENT** — extracted from a provided document (engagement letter,
  client intro); the answer cites the document and links it rather than
  copying it.
- **EXPORT** — pulled from a system (QBO, FC), not asked; the interview just
  confirms which export.
- Modes combine where noted (e.g., EXPORT + ASK).
- **SCAFFOLD** — a living file that starts empty at onboarding; no question.
- **RUNTIME** — live state, queried from the system of record; never stored,
  never asked.

## 0. Routing items (establish first; they gate everything below)

Per SKILL.md, these are established from the Phase 1 locating answers and
Phase 2 research, then confirmed with the operator in the Phase 3 findings
review — asked directly only where research can't answer them. "First"
means before the substantive blocks below are filled, not before research.

1. Which client? Exact legal name, as it appears on the Drive folder.
2. **Entity manifest** — for each entity: legal name, slug, entity type,
   nonprofit yes/no, QBO company ID if known. Entity-type and nonprofit
   switches apply PER ENTITY (a mixed engagement gets each entity's own
   rules). Nonprofit activates: board delivery override, source-document
   policy, fixed-asset schedule, budget vs. actual, June 30 fiscal-year
   likelihood, board escalation, no-materiality-floor. Multi-entity books
   nest as `d-books/<entity-slug>/`; groups A through C stay
   engagement-level.
3. Which services are in scope? (Run B3 now — **confirmed scope gates the
   question blocks**, never the tier name alone. Record the tier as named
   and flag it provisional if the ladder is unsettled.)
4. Where is the client's shared drive (Drive folder / ID)?
5. Is the client folder firm-internal (client has NO Drive access)? The
   bundle holds internal economics and access routing; if the client can see
   the folder, stop and resolve placement first.

## A. Identity & relationship

| # | Property | Mode | Question(s) |
|---|---|---|---|
| A1 | client_name / dba | CONFIRM | Exact legal name? Does the Drive folder match? Any DBAs in use? |
| A2 | entity_type | CONFIRM | For each entity: sole prop / partnership / S-corp / C-corp / LLC + taxed-as / nonprofit? Drives draws vs. distributions, 1099 eligibility, tie-out, nonprofit path. |
| A3 | entity_relationships | ASK | Related entities? For each: relationship, do we keep its books, intercompany accounts (due to/from, clearing). Also external standing relationships (auditor, tax preparer if separate). |
| A4 | industry | ASK | Two to three sentences: what is this business actually? What do they sell, how many locations, revenue streams, seasonality? |
| A5 | founded_year | ASK | When founded? |
| A6 | ownership | ASK | Who owns it (name, role, % if known)? Partners and contributions? Nonprofit: no owners — capture board governance and the treasurer/finance chair instead. |
| A7 | service_start_date | CONFIRM | When did they become a client? (tracker) |
| A8 | referral_source | CONFIRM | Who referred them? |
| A9 | primary_contact | CONFIRM | Day-to-day contact? (FC) |
| A10 | client_contacts | ASK | Everyone we ever talk to: name, role, and what topics they cover. Emails/phones stay in FC; capture the pointer, not a duplicate directory. |
| A11 | portal_users | CONFIRM | Who on the client side has portal access (FC and any document tool)? Anyone being removed? |
| A12 | working_with_this_client | ASK | Preferred channels? Do they actually use the portal? What will they reliably do and not do (receipts, document uploads)? Responsiveness? Quirks a new team member must know on day one? What does the client do monthly to support us (their side of the work)? |

## B. Engagement & commercial

| # | Property | Mode | Question(s) |
|---|---|---|---|
| B1 | client_lifecycle_status | CONFIRM | Prospect / onboarding / cleanup / active / offboarding? (canonical enum) |
| B2 | service_tier | CONFIRM | Which tier? Record as named; flag provisional if the ladder is unsettled. |
| B3 | service_scope | ASK | Walk the catalog on/off: bookkeeping, month-end close, delivery + analysis, budget, forecasting, CFO/advisory, payroll, 1099 add-on, bill pay, invoicing, sales tax, audit support. Billing notes per add-on. |
| B4 | accepted_quote | DOCUMENT | Link to the quote in the client Drive folder. |
| B5 | signed_engagement | DOCUMENT | Link to the engagement letter (FC e-sign or PDF). |
| B6 | engagement_terms | DOCUMENT + ASK | Extract terms from the signed letter: tier, monthly fee, one-time fees, cleanup range and split, start date, escalators, termination. If current billing differs from the letter, record BOTH; the changed amount becomes operative only with written authorization (amendment, approval email) and an effective date — otherwise the file stays partial and the discrepancy goes to the gap report. |
| B7 | billing_configuration | ASK | Billing platform? Draft date? Onboarding-fee timing? Cleanup billing split? |
| B8 | delivery_configuration | ASK | Cadence? Target date (20th default; board or standing-meeting override)? Route, recipients, format, archive location? |
| B9 | financial_delivery_owner | CONFIRM | Controller (default) or lead (legacy exception)? |
| B10 | controller_review_requirement | CONFIRM | Controller reviews every close? Exceptions? |
| B11 | custom_financial_report_configuration | ASK | Reports beyond standard P&L/BS? Per report: built where, what updates monthly, format. Link last period's package as the example. Note any report produced by a Claude skill and name the skill. |

## C. Staffing, ownership & capacity

| # | Property | Mode | Question(s) |
|---|---|---|---|
| C1 | pod_assignment | CONFIRM | Staff, lead, controller — and since when? Note multi-role reality (controller may also be the CFO) and any expected transitions. |
| C2 | client_response_owner_matrix | ASK | Who answers: transaction-level, financials/report, engagement/pricing, portal/tech? Client-side counterparts too. |
| C3 | budgeted_hours_by_role | CONFIRM | Hours/month per role. If the FC budget is known-wrong, capture reset targets from the team and flag the FC update as an open item. Keep controller and CFO hours separate. |
| C4 | profitability_baseline_as_of_date | CONFIRM | FC profitability as-of date. |
| C5 | recurring_work_schedule | CONFIRM | Weekly bookkeeping day, close window, review timing, payroll cadence, annual cycles. |
| C6 | client_application_setup | CONFIRM | Which firm apps apply and their setup state. Flag anything mid-transition (tool being retired/adopted) with dates. |
| C7 | internal_review_focus_areas | ASK | What does review specifically watch on this client? What has bitten before? (If a client intro / training guide exists, mine it — this is usually its richest content.) |
| C8 | monthly_controller_call_settings | CONFIRM | Standing meeting or scheduler link? Escalation policy if calls lapse. |

## D. Books & systems (repeat per entity)

| # | Property | Mode | Question(s) |
|---|---|---|---|
| D1 | qbo_company | CONFIRM | QBO company ID + access path. |
| D2 | accounting_method | CONFIRM | Cash or accrual (financials AND tax)? |
| D3 | fiscal_year_end | ASK | FYE? (Calendar for most; nonprofits often June 30.) |
| D4 | chart_of_accounts | EXPORT | Export the COA. Which accounts have non-obvious uses? Is Ask My Accountant in use? Does a Bank Review category exist or need creating? |
| D5 | classification_tracking | CONFIRM + ASK | Classes/projects on? What do classes represent, what do customers represent, and what are the application rules? (Nonprofit pattern: classes = functional categories required on every transaction; customers = grants.) |
| D6 | vendor_coding_rules | EXPORT + ASK | (1) Export existing QBO bank rules — they stay. (2) Vendors the team codes from memory: vendor, account, class, treatment, confidence marker ("always" vs. "default, verify over threshold"). (3) Owner personal-expense pattern (draws / distributions / shareholder loan per entity type) — or the nonprofit analog: checks written directly to employees are the red flag. |
| D7 | materiality_thresholds | ASK | Code-without-asking floor and default account? Questions-list threshold? Basis? Nonprofit: usually collapses to "no floor, ask about everything, source doc required regardless of amount" — record that explicitly. |
| D8 | transfer_and_clearing_rules | ASK | Which accounts move money between each other (sweep accounts)? Clearing accounts? How are these recognized and are QBO rules already set up? |
| D9 | recurring_journal_entries *(QBO templates)* | EXPORT + ASK | Export the recurring-transactions list. Per template: type, schedule, amount, and what it does. Which are standard monthly (prepaid spreads)? Which are deliberately NOT recurring because a skill generates them? Which are inactive or stale — flag any amount that no longer matches the engagement. |
| D9b | recurring_journal_entries *(hand-computed close entries)* | ASK | **The export cannot answer this — these live in the lead's head.** Which month-end entries does someone compute by hand each period? Walk the whole close and force out: functional or admin cost allocations, payroll allocation splits, amortization draw-downs of up-front grant/contract receipts, deferred-revenue recognition, depreciation where it is not templated, accrual entries and their reversals, full-year entries that pay down over the year. Per entry: **source report, who computes it, timing, and how it is validated.** Never let a split percentage be carried forward — record where the current split lives. Nonprofit and CFO clients: expect most of the close to sit here rather than in the templates. |
| D10 | loan_schedules | ASK | Loans? Schedule location, year-end tie-out owner, related JE. Watch for leases (ASC 842) — flag but track under review focus. |
| D11 | budget_configuration | ASK | Budget? Built by whom? Approval (board)? Where does the approved budget live? Who loads it to QBO? Budget vs. actual in the package? |
| D12 | budgeting process | ASK | Forecasting clients: how is the forecast maintained, what triggers changes, how often revisited, built with what tooling? |
| D13 | fixed_asset_schedule | ASK | (Nonprofit-flagged) Do we maintain it? Where? Who? If it should exist and doesn't, record "to build" as an open item. |
| D14 | financial_accounts (bank) | ASK + EXPORT | Per account: institution, role, statement source (who pulls/uploads), access-pain rating, credential pointer. A trial balance export enumerates the accounts. Note banks being exited. |
| D15 | credit_card_accounts | ASK | Same shape. Note card-platform transitions and legacy cards in history. |
| D16 | bank_feed_recovery_notes | ASK | Chronically flaky feeds? Where reconnect credentials live? (Live status stays in QBO.) |
| D17 | document_intake_configuration | CONFIRM | Which document tool(s), on/off, and why? Mid-transition: record both states with dates. |
| D18 | source_document_attachment_policy | ASK | Attachments required (audit)? Client willingness? Formal financial policy doc to link? — CONDITIONAL: a formal financial policy is expected only for nonprofit entities and engagements with confirmed CFO/advisory scope (scope, never the tier name). For small owner-operator clients, don't raise it as a gap; record "Not applicable" with the operator's sign-off. |
| D19 | point_of_sale_systems | ASK | POS / payment / donor platforms? Access method per platform? |
| D20 | pos_report_specification | ASK | Per platform: which report, period, delivery path, destination. |
| D21 | sales_deposit_reconciliation_rules | ASK | How do gross sales tie to deposits? Fees netted where? (Some platforms have no fees — payout ties exactly; say so.) |
| D22 | payroll_configuration | CONFIRM | Operator, platform, time tracking, cadence, auto-feed? |
| D23 | payroll_processing_rules | ASK | Client-specific if/then payroll logic. Force it out now: approval flow, allocation splits, what must run through payroll vs. direct expense. If a payroll skill exists for this client, name it and its halt conditions. |
| D24 | sales_tax_configuration | CONFIRM + ASK | Filing? Jurisdictions, method, frequency, login pointer. |
| D25 | bill_payment_configuration | CONFIRM + ASK | Do we pay bills? Platform, approval path, submission rules. |
| D26 | client_question_send_schedule | ASK | How often is the questions list sent: weekly, monthly, twice monthly? |
| D27 | client_workspace_locations | CONFIRM | The pointer file: shared drive ID, FC record, workbooks. Capture actual IDs, not descriptions. |

## E. Access & credentials (pointers only, never values)

| # | Property | Mode | Question(s) |
|---|---|---|---|
| E1 | credential_locations | ASK | Per portal: where does the credential live and who is assigned? Note any systems accessed with the CLIENT's own logins. |
| E2 | client_system_access_assignments | ASK | Which role/person has what access, per system? Note pending grants. |
| E3 | authentication_requirements | ASK | Per system: how OFTEN does 2FA challenge (every login / new device / periodic / rare), how COMPLEX is the challenge (SMS/email code, push approval to whose device, security questions), and where do codes route (codes email, firm Google Voice, a person's phone)? Frequency + complexity decide whether pulls can be automated or need a human — "has 2FA" alone answers nothing. |

## F. Annual: cleanup & year-end

| # | Property | Mode | Question(s) |
|---|---|---|---|
| F1 | cleanup_scope | CONFIRM | Scope, range, tie-out baseline, billing terms — and the durable outcome story (what restructure happened, was it priced right). |
| F2 | tax_return_baseline | CONFIRM | Most recent filed return (year, location)? Return in progress? |
| F3 | tax_accountant_contact | ASK | External CPA/auditor and the request path. Note when one firm does both audit and tax. |
| F4 | year_end_close_requirements | ASK | Client-specific checklist additions, lock expectations, tax handoff. Nonprofit: audit-support work and its timing (audit-driven, not year-end-driven). |
| F5 | 1099_service_configuration | CONFIRM | Add-on on? Tracking pointer. Special payee rules (legal and medical payees get 1099s regardless of entity type). Model changes on the horizon. |

## G. Living context

| # | Property | Mode | Question(s) |
|---|---|---|---|
| G1 | onboarding_checklist_status | CONFIRM | FC checklist pointer + state. |
| G2 | onboarding_outstanding_items | CONFIRM | Anything outstanding: item, owner, follow-up. |
| G3 | cleanup_outcomes | ASK | Durable results: decisions, coding rules discovered, where historical context lives (old bank?). |
| G4 | known_challenges_recurring_issues | ASK | What breaks repeatedly? What does the team brace for monthly? |
| G5 | current_review_exceptions | SCAFFOLD | Starts empty. |
| G6 | financial_delivery_history | CONFIRM | Seed with last delivered period + archive pointer. |
| G7 | meeting_calendar | ASK | Standing dates that move work timing: board meetings, controller calls, advisory sessions. |
| G8 | year_end_close_status | RUNTIME | Live state — never stored; the bundle may hold at most the FC pointer. |
| G9 | escalation_map | ASK | If the client goes unresponsive, who unblocks? Nonprofit: which board member? |

## Firm-level per-client files

| # | Property | Mode | Question(s) |
|---|---|---|---|
| H1 | correction_and_skill_feedback_log | SCAFFOLD | Starts empty; one-line text entries at review time. |
| H2 | advisory_service_plan | ASK | Advisory/CFO tier: cadence, participants, outputs. |
| H3 | meeting_records_and_commitments | SCAFFOLD | Starts empty; seed ONLY from a real kickoff recap if one exists — never date an entry to the onboarding run. |
| H4 | capacity_profitability_variance | SCAFFOLD | Starts empty. |
| H5 | context_change_log | SCAFFOLD | Satisfied by the bundle's `log.md`. |

## Never asked, never stored (live state)

`bank_feed_connection_status` (QBO), `cleanup_progress` (FC cleanup project),
`open_uncategorized_items` (FC month-end close). Skills query the system of
record at runtime.
