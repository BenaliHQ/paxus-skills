# D. Books & systems configuration

QBO configuration, coding rules, and schedules. Books are per-entity in QBO:
single-entity clients use this folder flat; multi-entity clients get one
subfolder per entity (`d-books/<entity-slug>/`), each holding this full file
set, and all books links must be entity-scoped. Never rename or duplicate the
`d-books` top-level folder itself.

* [QBO configuration](qbo-configuration.md) - company ID, accounting method, fiscal year end
* [Chart of accounts](chart-of-accounts.md) - export plus account-use notes, Bank Review category
* [Classification tracking](classification-tracking.md) - classes/projects and application rules
* [Vendor coding rules](vendor-coding-rules.md) - the highest-value file: rules, confidence markers, owner personal-expense rows
* [Materiality thresholds](materiality-thresholds.md) - what an agent may code without asking
* [Transfer & clearing rules](transfer-and-clearing-rules.md) - recognizing transfers vs. spend
* [Recurring journal entries](recurring-journal-entries.md) - the recurring JE recipes
* [Loan schedules](loan-schedules.md) - loans and amortization schedule pointers
* [Budget configuration](budget-configuration.md) - whether and how this client gets a budget
* [Budgeting process](budgeting-process.md) - how budgets and forecasts are built and maintained
* [Fixed asset schedule](fixed-asset-schedule.md) - nonprofit-flagged schedule pointer
* [Bank & card accounts](bank-and-card-accounts.md) - accounts, recon scope, statement sources, feed recovery notes
* [Document intake](document-intake.md) - document tool configuration and attachment policy
* [Point of sale](point-of-sale.md) - POS platforms, report specs, deposit reconciliation, month-end cut-off and accrued sales
* [Payroll](payroll.md) - configuration and processing rules
* [Sales tax](sales-tax.md) - filing configuration
* [Bill payment](bill-payment.md) - platform and approval path
* [Client questions schedule](client-questions-schedule.md) - how often the client is sent their questions list
