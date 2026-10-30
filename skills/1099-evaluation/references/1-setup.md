# Step 1: Setup

Entry: client name, mode (initial or year-end), tax year (the current calendar year unless
told otherwise), the runner's name and role. Exit: every id below resolved, and the plan
stated in one short list.

## 1.1 The QuickBooks file

- `connections_list`: find the client's QuickBooks scope. Names differ across systems (the
  QBO company name, the legal name, the Drive name); match on a distinctive word and confirm
  with `quickbooks.company.get` (legal name). Two possible matches: ask, never pick.
- A client with several QuickBooks files (a group of entities): one evaluation file per file
  (per payer EIN). Ask which ones are in scope.

## 1.2 The client's Drive and bundle

- `google.drives.search` with a distinctive word from the client's name; then
  `google.drive.folder` on the drive id.
- Read the client's `.agents` bundle when it has one (`google.file.get`):
  `0-core/workspace-locations.md` (ids), `c-staffing/pod-assignment.md` (lead and
  controller), `a-identity/contacts.md` (who receives client email),
  `f-annual/1099-configuration.md` (anything client-specific about 1099s),
  `0-core/client-critical-rules.md`. No bundle: ask the person for the lead, controller and
  client contact.
- Find `Taxes`, then `Taxes > 1099` and `Taxes > W-9`. W-9s are often in subfolders
  (`W-9s`, a year): list them all.

## 1.3 Financial Cents (read-only)

- `financialcents.clients.list` → client id; `financialcents.client.projects` → the 1099s
  project for the year; `financialcents.project.tasks` for its tasks and who they're
  assigned to. If the client is in the "NO 1099" group or there is no 1099s project, say so
  and stop unless told to go on.

## 1.4 The evaluation file

- Initial mode: look in `Taxes > 1099 > <year>` for a file starting
  `1099 Vendor Report – `. If one exists, do not make another: ask whether to rebuild it in
  place (clear A6:T and refill) or stop. If none exists, the plan is: create the `<year>`
  folder if missing (`google.folder.create`), then `google.file.copy` the master template into
  it named `1099 Vendor Report – <Client> – MM.DD.YYYY` (today).
- Year-end mode: the file must exist; the plan is a new tab (see `5-year-end.md`).
- Read the master's (or the file's) Evaluation tab rows 1–6 with formulas
  (`google.sheet.get`, `formulas: true`) and its Instructions tab. Map columns by the row 5
  headers, not by letter. Expected: A–J the transaction columns (Distribution account …
  Balance), K OVER 2000 (formula), L IS A CORPORATION?, M LEGAL SERVICES, N MEDICAL /
  HEALTH CARE, O SEND TO LEAD? (formula), P W-9 ON FILE?, Q W-9 REQUESTED (date), R W-9
  RECEIVED (date), S 1099 TYPE, T NOTES, and U 1099 FILED (date) if the template has it.
  Note how many rows carry the K and O formulas (`google.sheet.get` without a range gives
  the tab size).

## 1.5 The controller's tracker

- Controller = the 1099s project's "Review and submit" assignee, else the bundle's
  controller.
- `google.drive.search` for `Tax1099 W-9 Request Tracker – <Controller>`. If it is not in
  the trackers folder, the plan includes creating it there (see `4-outputs.md`). A tracker
  in someone's My Drive cannot be reached by the firm's connection: say so and ask them to
  move it into the trackers folder.

## 1.6 State the plan

One short list: the QBO file, the Drive folder, the file to create or update, the tracker,
the date range, and every write the run will make. This is the approval point.
