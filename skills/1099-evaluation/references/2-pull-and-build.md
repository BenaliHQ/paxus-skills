# Step 2: Pull QuickBooks and build the rows

Entry: setup done. Exit: `rows.json`, `totals.json` and `summary.md` from the `build_1099.py`
script, and the three extra checks in 2.4 done.

No saved-report export. One pull of every vendor transaction covers what the saved 1099
report showed plus vendors coded to accounts outside its list (office supplies, utilities,
supplies and materials, CapEx, flip inventory, balance sheet accounts).

## 2.1 Account types

Classify the paid-from account by type, never by name:

- `quickbooks.query`: `select Name, FullyQualifiedName from Account where AccountType = 'Bank'`
  and the same for `'Credit Card'` (add `maxresults 200`).
- Optional excluded-category accounts by subtype with `quickbooks.accounts.by_subtype`
  (Utilities, BankCharges, Insurance, PayrollExpenses, TaxesPaid) — the script already
  catches the common names, so add these only when a client's names are unusual.

Write `accounts.json`: `{"bank": [names], "card": [names], "exclude_split": {"Account name": "reason"}, "exclude_vendor": {"Vendor name": "reason"}}`.

List every Bank-type account in `bank`, including petty cash and savings: a payment whose
split is one of them is a transfer between the client's own accounts, and the script drops
it. Put vendors that only sold goods, inventory or equipment, wage-garnishment payees, and
the client paying itself in `exclude_vendor` so they come off the list entirely (see
`rules.md`). Read `summary.md` after the first build: if a vendor at $2,000+ is plainly one of
these, add it and build again rather than leaving it as a CHECK row.

## 2.2 The vendor pull

`quickbooks.report.transactions_by_vendor` with
`start_date` (Jan 1), `end_date` (today, or Dec 31 in year-end mode),
`columns`: `tx_date,txn_type,doc_num,account_name,split_acc,subt_nat_amount`.
It returns about 90 rows per call; call again with the `row_offset` each response names
until all rows are covered. Save each response body unchanged to its own file in one
folder (`p<offset>.md`).

A large client runs to 25+ calls. Where the session can start a subagent (Claude Code), hand
the paging to one with these exact arguments and have it save the files and report the row
count; keep the pages out of the main conversation. In Cowork, page in the main session and
save each page to a file as it arrives; do not repeat pages back in the conversation.

Check: the last response's total row count equals the rows saved.

## 2.3 Build

Run the script in this skill's `scripts/` folder:

`python3 scripts/build_1099.py --pages <folder> --accounts accounts.json --out <out> --client "<Client>" --period "<range> · built by Claude from QBO, bank-paid only, card payments excluded"`

The script keeps Expense, Check and Bill Payment (Check/Cash) rows paid from Bank accounts;
drops card-paid rows (reported as `card_paid_excluded`), bills, card payments, deposits and
transfers; drops excluded vendors and categories (`rules.md`); and lays out the rows in the
template's A–J shape, one alphabetical list: a vendor header row, its transactions, a
"Total for <vendor>" row; then TOTAL and a "Not included" line. `rows.json` holds the sheet
writes in 5,000-cell chunks; `totals.json` the Total row number and amount per vendor;
`summary.md` the $2,000+ list, the watch list ($1,500–$1,999.99), the excluded vendors and any
negative totals. Read `summary.md`; do not paste the rows into the conversation.

## 2.4 Three checks the vendor pull cannot see

- **Bank payments with no payee.** `quickbooks.report.transaction_list` with
  `source_account_type` `Bank`, the same dates, `columns`
  `tx_date,txn_type,doc_num,name,memo,account_name,other_account,subt_nat_amount`. Keep
  outflows with a blank Name. Any over $600, or several to what the memo says is one payee,
  go on the flag list with date, amount and memo ("add the payee, then re-run").
- **Bank payees that aren't set up as vendors.** `transactions_by_vendor` only lists
  Vendor-type names, so a payee set up as a customer, employee or other name (a landlord
  is a common one) never reaches the build, with no warning. From the same Bank
  `transaction_list`, take every outflow (Expense, Check, Bill Payment) with a Name and
  compare the names to the vendors in the saved pages. For each name missing from the
  pages, write its rows to one more page file in the same table shape (a `**<Name>**`
  header row, then one `· <date>` row per payment with the bank account, split account and
  the amount as a negative number) and re-run 2.3, so it lands on the sheet like any other
  vendor and the normal exclusions apply. Put "set up as a vendor and check Track 1099" on
  the QBO fix list for each one that ends up needing a 1099.
- **Journal entries and bulk-entered history.** `transaction_list` with `transaction_type`
  `JournalEntry` and the same columns. Lines to expense, COGS, CapEx or inventory accounts
  with no Name: read the memo for a payee. A payee named in a memo goes on the flag list
  with its total. Clients onboarded with bulk journal entries (entered by account, not by
  vendor) will show up here; say how much of the year is in journal entries with no payee.
