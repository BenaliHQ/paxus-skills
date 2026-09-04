# Research Map — where the skill finds answers on its own

Phase 2 works through this map before any substantive intake question is asked. Property IDs
reference `intake-questions.md`. Everything here is read-only; anything not
findable through these sources lands in the findings review (Phase 3) or the
gap interview (Phase 5) as a question.

## Financial Cents (the firm's FC connection, read-only)

| Property | Where in FC |
|---|---|
| A1 client name | Client record |
| A7 service_start_date | Client record / master tracker |
| A8 referral_source | Client record, where captured |
| A9 primary_contact | Client contacts |
| A10 client_contacts | Client contacts — prefill names/roles; confirm topics-covered with the team; emails/phones stay in FC; store the FC pointer |
| A11 portal_users | Client portal users |
| A2 entity_type | Client overview questionnaire, where filed in FC |
| B1 lifecycle_status | Client status / groups |
| B2 service_tier | FC groups (record as named; provisional if ladder unsettled) |
| B5 signed_engagement | FC e-sign — link, not copy |
| B9 financial_delivery_owner | Team assignment / delivery config (controller default) |
| B10 controller_review_requirement | Review workflow config (firm default: every close) |
| C1 pod_assignment | Team assignments |
| C3 budgeted_hours_by_role | Client budget fields |
| C4 profitability_baseline_as_of_date | Profitability as-of |
| C5 recurring_work_schedule | Recurring projects and their cadence |
| C6 client_application_setup | Setup subtasks / checklists |
| C8 controller_call_settings | Recurring meeting project, where modeled |
| D17 document_intake_configuration | Setup subtasks (which document tools are configured) |
| D22 payroll_configuration | Payroll project / setup record |
| D24 sales_tax_configuration (CONFIRM part) | Setup record: filing on/off, frequency |
| D25 bill_payment_configuration (CONFIRM part) | Setup record: platform, whether firm pays bills |
| F1 cleanup_scope | Cleanup project record |
| F5 1099_service_configuration | FC groups / add-on flags |
| G1/G2 onboarding checklist + outstanding | Onboarding checklist state |
| G6 financial_delivery_history | Delivery archive — seed last period + pointer |
| G8 year_end_close_status | Pointer only (live state) |

## Client Drive folder (inventory first, read selectively)

**Check the `perm` folder first.** Each client's Drive folder has a `perm`
(permanent documents) folder, and it is the firm-standard landing spot for
QuickBooks exports pulled for onboarding (firm decision, 2026-08-04). Before
putting any export on the request list, inventory `perm` — the exports the
skill wants are, increasingly, already sitting there:

| Export in `perm` | Feeds |
|---|---|
| Chart of accounts | D4 |
| Bank-feed rules (QBO bank rules export) | D6 |
| Class list | D5 |
| Trial balance | D14/D15 account enumeration |
| Recurring transactions | D9 *(the template half only; D9b is interview-only)* |

(The firm is still finalizing the full export list; treat any other QBO
export found in `perm` as fair game and cite it like the rest.)

| Property | Which document |
|---|---|
| B4 accepted_quote | Quote PDF |
| B5/B6 engagement terms | Signed engagement letter |
| B3 service_scope (draft) | Engagement letter package list — confirm with operator |
| B11 custom reports | Prior delivery package, if archived in Drive |
| C7 review_focus_areas | Client intro / training guide (mine it hard — usually the richest doc) |
| D5/D6 classification + coding workflow | Client intro / training guide |
| D11 budget_configuration | Budget files |
| D2 accounting_method | Client overview questionnaire / engagement letter |
| D18 attachment policy | Financial policy document (expected only for nonprofit / CFO-tier clients — its absence is a gap only there) |
| F2 tax_return_baseline | Most recent filed return PDF, where saved |
| D4/D5/D6/D9/D14 exports | The `perm` folder (see above), then anywhere else in the client folder |
| G4 known_challenges (draft) | Client intro "recurring issues" sections — confirm with operator |
| Entity manifest (draft) | Engagement letter + questionnaire — confirm with operator |

## QBO (only via the firm's approved read-only CLI connection, if set up)

| Property | Source |
|---|---|
| D1 qbo_company | Company info |
| D2 accounting_method | Company settings, where readable |
| D27 client_workspace_locations | Assembled from Phase 1 (Drive ID) + FC record + QBO company ID |
| D4 chart_of_accounts | COA export |
| D5 classification_tracking (enumeration) | Class list |
| D6 vendor_coding_rules (existing-rules part) | Bank rules export |
| D9 recurring_journal_entries *(templates only)* | Recurring-transactions list. Does NOT cover D9b, the hand-computed close entries — those are interview-only. |
| D14/D15 bank + card accounts (enumeration) | Trial balance / account list |

Never authenticate to QBO, a bank, or any portal yourself. No connection →
these go on the export-request list in the gap report.

## Interview-only (research cannot answer these — plan to ask)

Head-knowledge items, mostly judgment and process: A3 relationships, A4
industry description, A5 founded, A6 ownership/governance, A12 working with
this client, B7 billing config detail, B8 delivery config detail, C2
response owner matrix, D3 FYE, D7 materiality, D8 transfers, D10 loans, D12
budgeting process, D9b hand-computed close entries, D13 fixed assets, D16
feed recovery, D19-21 POS, D23
payroll processing rules, D26 questions cadence, E1-3 access and
budgeting process, D13 fixed assets, D16 feed recovery, D19-21 POS, D23
payroll processing rules, D21b sales accrual and cut-off, D26 questions
cadence, E1-3 access and
credentials, F3 tax accountant, F4 year-end requirements, G3 cleanup
outcomes, G4 challenges, G7 meeting calendar, G9 escalation, H2 advisory
plan — plus the ASK residue of any mapped item research couldn't fill
(e.g., the judgment parts of D17/D22/D24/D25). Batch these per person
(controller / lead / client contact) so the interview stays short.
