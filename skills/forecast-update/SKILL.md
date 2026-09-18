---
name: forecast-update
description: Update a CFO or advisory client's forecast workbook with the latest month's actuals. Pulls the newest monthly financials PDF and the most recent forecast workbook from the client's shared Drive (gws in Claude Code, the connected folder in Cowork), reads the client's forecast spec from their Drive, pastes the new month's actuals into the workbook, applies any prior-month restatements found in the new financials, proves the result still ties to the statements, and hands back a finished workbook for review before upload. Works for any client on a formula-driven forecast workbook — non-profit or for-profit, calendar year or fiscal year. Use when someone says "run the forecast for <client>", "update the <client> forecast", "build the <month> forecast", "do the forecasting for <client>", or "roll the actuals into the forecast". SCOPED TO THE FORECAST WORKBOOK — it does not draft the meeting agenda and it does not build the dashboard.
---

# /forecast-update — Roll Actuals Into a Client's Forecast Workbook

You are updating a client's forecast workbook with the latest closed month. The output is a
finished `.xlsx` that **ties to the statements**, handed to the operator to review and upload
themselves. Be conversational and warm — match the Paxus voice.

Sibling skills: `/monthly-dashboard` (the one-page dashboard) and the financials meeting agenda.
Run this **before** the agenda so the agenda reflects current actuals.

## Important rules for this skill

- **No fabrication.** Every figure traces to the statements. Never infer a missing month, guess an
  account mapping, or fill a gap to make a number look right. If a label doesn't match, flag it.
- **Skills are the engine; client data is the fuel.** This file contains no client names, IDs, or
  numbers. Everything client-specific comes from the client's forecast spec (see Phase 1) and from
  the client's own files in Drive. See `docs/context-model.md`.
- **The workbook must tie before it leaves your hands** — new month *and* year-to-date. A workbook
  that doesn't tie is not a deliverable, it's a bug.
- **Edit a copy, never the source workbook.** Never upload to the shared Drive without an explicit
  go-ahead.
- **Detect the structure; never assume it.** These workbooks differ by client and the operator
  edits them between runs. Re-detect every single run.

## Why this is mostly mechanical

These workbooks are **formula-driven**. Actuals get pasted into one input tab and one control is
updated; the downstream tabs (rolling forecast, analysis, current month) recompute on their own.
Your job is only to (a) get the actuals in correctly, (b) catch any prior-month restatements, and
(c) prove the result still ties. Everything else the workbook does itself.

---

## Phase 1 — Resolve the client and read the spec

Ask which client this is for, then read that client's confirmed spec file, `forecast-spec.md`.
**The spec lives in the client's own shared drive** — never on one person's laptop and never in one
operator's private notes — so every Paxus teammate who runs this skill, from Claude Code or from
Cowork, finds the same spec.

**Where the spec lives (canonical location, in this order of precedence):**

| Client drive shape | Canonical spec location |
|---|---|
| Drive has a `.agents/` context bundle (built by `/paxus-skills:client-context`) | `.agents/b-engagement/forecast-spec.md` |
| Single-entity drive, no bundle | `Perm File/forecast-spec.md` at the drive root |
| Multi-entity drive (one folder per entity at the root) | `<Entity folder>/Perm File/forecast-spec.md` — one spec per entity |

This is the same rule `/monthly-dashboard` uses for `dashboard-spec.md`; the two specs sit side by
side. The file is always named exactly `forecast-spec.md`. It never goes in `Financials/`, the
forecast folder, the year folder, `Review Notes`, or Cowork's default `Claude outputs` folder —
**always name the destination folder explicitly when saving**, or Cowork will drop it in
`Claude outputs`.

**Finding it on a repeat run:** search the client's drive for a file named `forecast-spec.md` (gws:
`name = 'forecast-spec.md'` with `corpora:"drive"` scoped to the client's `driveId`; Cowork: search
the connected client folder). Then:

- **One file, in the canonical folder** → that's the spec. Read it.
- **One file, in the wrong folder** → it's still the spec; *move* it (don't copy) to the canonical
  folder and say so.
- **Two or more** → the newest is operative. Move the others to the canonical folder renamed
  `forecast-spec-superseded-YYYY-MM-DD.md` (their modified date) and say so. Never leave two files
  named `forecast-spec.md` on one drive.
- **None** → cold start (below).

A copy at `~/paxus-ai/clients/<slug>/forecast-spec.md` on someone's laptop is an **optional local
cache only**. It is unreachable from Cowork and from every other teammate's machine. If a laptop copy
and the Drive copy differ, **Drive wins** — refresh the cache from Drive, never the other way round.

The spec records: resolved Drive IDs, the Cowork connected-folder path, the fiscal/calendar period
basis, which financials report and which page is the source, the workbook family and control, the
file-name patterns, the account-mapping quirks, the standing decisions (which unmapped accounts fold
where), and the run history.

- **Spec exists** → use it, then still re-detect the workbook structure in Phase 3 and reconcile.
- **No spec** → **cold start.** Work through the phases below discovering each piece, ask only what
  you genuinely cannot determine, and **write the spec to the client's canonical Drive location at
  the end** (Phase 8) so next month is a repeat run. Do not copy another client's spec.

## Phase 2 — Pull the two inputs

You need exactly two files: the **latest monthly financials PDF** and the **most recent forecast
workbook**.

**Two environments, one rule: use whatever Drive access the session already has.**

- **Claude Code on macOS:** the local Google Drive path is sandbox-blocked (`Operation not
  permitted`) — **always use the gws CLI**, never the local `CloudStorage` path. Every gws Drive call
  needs `includeItemsFromAllDrives:true` and `supportsAllDrives:true` (plus `corpora:"drive"` with the
  client's `driveId` for searches). Download with `alt:media`, and **size-verify every download** —
  gws can truncate silently. Note that `--upload` only accepts a path **inside the current working
  directory**, so `cd` to the file's folder and pass a relative path.
- **Cowork (Windows or Mac):** there is no gws. The client's shared drive is a *connected folder*
  (e.g. `G:\Shared drives\<Client>\`). Read the financials, the workbook, and `forecast-spec.md`
  straight from it, and save outputs back into it by explicit folder path. **Record the
  connected-folder path in the spec** alongside the Drive IDs so either environment can run next
  month.

Everything here is a read. The only writes this skill makes are the finished workbook and the
client's `forecast-spec.md` (Phase 8).

**Resolve the folders once, then store the IDs.** Drive has many same-named folders across clients
(multiple "Financials", "2026", etc.), so blind `name contains` searches are ambiguous and slow. On a
**repeat** run read the resolved IDs from the spec and skip discovery. On a **cold start**:

- List shared drives to get the client's **own shared-drive ID** by name. Most clients have their own
  drive; don't assume everything hangs off a single firm-wide drive.
- Find the **financials** folder and the **forecast** folder. Forecast-folder names vary (`Forecast`,
  `Forecasts`, `Budgets and forecasts`), the workbooks are sometimes in a *subfolder* of that, and a
  drive may contain **both** a `Forecast` and a `Forecasts` folder — disambiguate by parent chain and
  contents, don't guess.
- Find the right **year subfolder**. Calendar-year clients use the calendar year; fiscal-year clients
  use a fiscal label like `FYE 06.30.YYYY`. Confirm the period if it's ambiguous — getting this wrong
  wastes the whole run.
- Pass `--params` JSON via a file (heredoc) when a query contains a folder ID, to avoid shell-quote
  breakage.

**Which financials file.** Many clients have both a detailed financials PDF and a board/summary
packet. The source is whichever carries the **per-month P&L with a column per month plus a
TOTAL/YTD column** — that one page is the source of truth for both the new actuals and any
restatements. If the packet carries both a **cash** and an **accrual** presentation, use the basis the
workbook is built on, and record which one in the spec.

> **Re-pull before building.** Some clients reissue the packet the same day, replacing the file in
> place (same file ID), so only `modifiedTime`/size reveal it. Diff the fresh copy against what you
> pulled, with timestamp header lines stripped, or every page reads as changed.

## Phase 3 — Detect the workbook structure

Parse with `openpyxl` (`data_only=False`, so you see formulas). Identify all four:

**1. The workbook family.** Two are in use across the firm's clients:

| Family | Control | How a month closes |
|---|---|---|
| **Control-cell** | An integer "completed months" cell on a settings tab | Paste actuals, bump the integer |
| **Label-row** | A literal `Actual`/`Forecast` label per month column on the rolling-forecast tab | Paste actuals, flip that month's label |

Never apply one client's family to another. A label-row workbook has no settings tab at all.

**2. The actuals input tab and its month-column layout** — which columns are which months (calendar
and fiscal clients differ), and which column holds the YTD total.

**3. The account → row mapping** — see Phase 4. Regenerate it every run; **never hardcode row
numbers.**

**4. Which tabs are row-aligned.** This decides whether a row insertion is safe (Phase 6). Usually
every P&L tab is row-aligned and the settings/summary tabs are not.

Compare what you find to the spec. **If it diverges — new control, renamed tab, shifted rows, a
deleted tab — stop and confirm with the operator before writing anything.** Operators restructure
these workbooks between runs, and a silent mismatch corrupts the whole file.

## Phase 4 — Extract the financials and build the diff

Use **`pdfplumber`** (`pip install pdfplumber` — pure Python, no system dependencies). The per-month
P&L spans several pages. Cluster words into rows by `top`, and bucket numeric tokens into month
columns by their **right edge** (`x1`) against the header's column right-edges. Parentheses mean
negative.

### PDF extraction traps

Each of these has silently broken a real tie-out at least once. Check for all of them:

- **Column edges shift as months are added** (~56–57px per added month). Re-derive them each run
  from the header row; never carry last month's numbers forward.
- **Continuation-page headers sit higher than page one's.** Page one carries the report title, so
  its month-header row is lower on the page than the repeated header on later pages. A fixed
  "skip anything above N" cutoff silently swallows the first several accounts of every continuation
  page. **Detect the header position per page** from the first month word, then skip only at or
  above that.
- **QBO can glue annotation markers onto the number** (`AR3,000.00`) — strip a leading one-to-three
  letter prefix before parsing, or the value is dropped.
- **Wrapped labels.** A two-line label can put the values row *between* its two label lines. Attach
  a value-only row to the preceding label line and absorb the following same-indent line to rebuild
  the full label.
- **Detached minus signs.** Some total rows render as `$ -` then the number. Derive the sign from
  the arithmetic (income − expense), not from the token.
- **Report retitling.** QBO renames reports between versions (e.g. "Profit and Loss" →
  "Statement of Activity"). Match on either.

### Account → row mapping

Match each PDF line to a workbook **input** row **by label**, not by position — the PDF orders
accounts differently from the workbook (grants are often alphabetical in the PDF, chart-order in
the workbook). Four rules:

- **Section-aware.** Track the current section (Revenue / Expenditures / Other Revenue / Other
  Expenditures) on both sides and match within it. Duplicate labels legitimately exist across
  sections — the same name can be both a grant and an expense, and utility lines repeat under
  different facilities. Without section scoping, an expense lands in revenue and the month is off
  by exactly that amount.
- **Exact match first, then prefix-tolerant.** PDF labels truncate. Fall back to a prefix match
  (minimum ~10 characters) only after exact fails — otherwise a short label binds to a longer
  similarly-named row. Normalize `&` to `and` before comparing.
- **Multiple occurrences in document order.** For a label that legitimately repeats within a
  section, consume PDF occurrences in order, taking the first unused candidate at or after the last
  matched row.
- **Leaf classification.** A row is an input leaf if it is **not** a subtotal **and** it
  participates in some subtotal (a component of an explicit cell-sum, or inside a `SUM(range)`).
  A YTD formula alone is **not** sufficient evidence — some real dollar-carrying rows have none, and
  treating them as headers silently drops their values.

**Relabels are not restatements.** A renamed account carrying the same dollars maps to the existing
row. A genuinely new account with no row is a decision point (Phase 5).

### Build the diff

- **New month** → the current-month column, mapped to the new month's column on the actuals tab.
- **Restatements** → for every already-closed month, compare the financials' figure to what's in the
  workbook now. Any difference is a restatement to apply — prior-month actuals get corrected when
  the new financials change them. List each with its delta.
- **Unmapped accounts** → any account with dollars but no workbook row.

## Phase 5 — Decision points: ask, don't decide

Bring these to the operator as **one grouped question**, not a stream:

- **Unmapped / new account.** Default recommendation: fold it into the closest existing line for the
  new month so the group total ties, and add a cell comment noting the breakdown. **Do not insert a
  row** unless they ask — see Phase 6 for why. If the client's spec already records a standing fold
  for that account, apply it and just mention it.
- **A fold applies to every month, not just the new one.** When you fold account A into row B, merge
  A into B's values for **all** months before writing. Folding only the current month lets B's own
  (zero) value overwrite a prior month's fold and silently breaks that month's tie.
- **Large or surprising restatement.** Apply it — the financials are authoritative — but flag the
  size so nobody is surprised in the meeting.
- **A structural reclass** (an account moving between sections, contra-revenue, a budget line moving
  with it). Follow the statements, but **this is the operator's call, not yours.** Say what the
  statements now show, what it implies for the budget line, and wait.
- **Output.** Default: hand back the finished file. Upload only on an explicit go-ahead.

**If you are a lead running this rather than the engagement's controller**, escalate rather than
decide: any row insertion, any structural reclass, any restatement large enough to change the story
the client hears, and anything where the spec and the workbook disagree.

## Phase 6 — Apply the update

Start from a **copy** of the latest workbook.

1. **Update the control** — bump the completed-month integer, or flip that month's `Actual` label,
   depending on the family.
2. **Paste the new-month actuals** into the new month's column. Match the prior column's cell style
   (`cell._style = copy.copy(prior_cell._style)`). Follow the workbook's own convention for
   zero-activity rows in a closed month — some write explicit zeros, some leave blanks to make an
   unclosed month visible.
3. **Apply the restatements** to the prior-month cells.
4. **Handle unmapped accounts** per the operator's choice.
5. **Leave the forward-looking forecast tab alone** unless asked — the rolling forecast blends
   actuals and forecast automatically. Leave free-text note columns alone too; those are the
   operator's own words.
6. **Save under the client's file-name convention** from the spec.

### Safe row insertion (only when the operator asks for a broken-out row)

`openpyxl`'s `insert_rows` shifts values and styles but **adjusts no formulas**, and these workbooks
reference the actuals tab **by absolute self-row** — thousands of references. A single inserted row
therefore requires:

1. `insert_rows(idx)` at the **same index on every row-aligned tab** (never the settings tab).
2. **Bump every row reference ≥ idx by 1 across all those tabs**, with a regex handling an optional
   sheet qualifier (quoted or bare) and `$` anchors. Do inserts **bottom-up** so earlier indices stay
   stable, or run one full insert-and-bump pass per inserted row.
3. To get the new row **auto-included in a `SUM(range)` subtotal**, insert it *inside* the range —
   the bump then expands the range. For **explicit-cell-sum** subtotals (`=E124+E125`), the bump
   never adds the new cell: **append it by hand**, then let later passes bump it. Explicit cell sums
   are common in these workbooks — always check which kind each subtotal is.
4. Watch percent-of-revenue anchors on the analysis tab. They anchor to a total row; inserting above
   it shifts the anchor. The bump handles it, but write any new analysis row with the anchor row
   that is current *at the time you write it*.
5. Populate the new row on every tab from its sibling row's pattern, copying `cell._style`.

**The cheaper alternative:** relabeling an already-wired empty row gives a named broken-out line with
**zero** formula surgery. Offer it — but only when that row carries no budget dollars, and only when
destroying its existing name is acceptable.

## Phase 7 — Tie out, verify, deliver

**The tie-out is mandatory and it is not optional-when-rushed.**

Replay the workbook's own roll-up logic and prove:

- **New-month column total** = the financials' current-month Total Income / Total Expense / Net Income.
- **YTD** (all closed months including restatements) = the financials' YTD TOTAL column.

Both reconcile **to the penny**. If a tie is off, the cause is almost always an unmapped account or a
misclassified leaf — resolve it. Never ship a workbook that doesn't tie.

**Verifying without Excel.** A workstation may have no LibreOffice and no native recalc, and
`openpyxl` drops cached formula values on save (harmless — Excel recalculates on open). So verify by
**evaluating the actual post-build formulas** against the PDF's printed subtotals: read each
subtotal cell's formula string, resolve its cell references and `SUM` ranges from the workbook's
data values, compute, and compare — per month **and** YTD.

Then assert, before delivery:

- Every rolling-forecast reference to the actuals tab sits in its **own** row (zero misaligned).
- Any inserted rows fall **inside** their subtotal formulas.
- No `#REF` or out-of-range references.
- No charts or objects were lost (`unzip -l` diff, old vs new — `openpyxl` can drop features it
  doesn't support).
- The zip is intact.

**Deliver:** hand over the file path, offer to open it, and summarize in plain language — the month
closed, what tied, each restatement with its delta, every decision made and who made it. Round to
the nearest hundred in the **summary**; the **workbook keeps full precision** because it has to tie.
Upload only on the go-ahead.

## Phase 8 — Write the spec back

Create or update `forecast-spec.md` in the client's **canonical Drive location** (the Phase 1 table:
`.agents/b-engagement/` when the client has a context bundle, otherwise `Perm File/`; per-entity
`Perm File/` on multi-entity drives). **Saving the spec into the client's drive is part of finishing
the run** — a spec that only exists on one laptop is the problem this skill was built to fix.

Name the destination folder explicitly when saving, or Cowork drops the file in `Claude outputs`.
If the client has an `.agents/` bundle, follow the bundle's `AGENTS.md`: OKF frontmatter on the file
and a line in the section index.

Record anything this run learned: newly resolved folder IDs, the Cowork connected-folder path, a
changed workbook structure, new PDF column geometry, a new standing fold decision, and a run-history
entry (month, file built, what tied, restatements applied, decisions made and by whom, and any **row
renumbering** downstream months will need). Row renumbering is the one thing future-you will most
want and most regret not writing down.

If a local cache exists at `~/paxus-ai/clients/<slug>/forecast-spec.md`, refresh it *from* Drive.
Never let the laptop copy become the source of truth.

## Edge cases

- **Fiscal-year clients.** Month 1 is not January. The year subfolder is labelled by fiscal year end.
  Getting this wrong points you at the wrong workbook entirely.
- **A month was never closed.** Two months sometimes roll in together. Apply them in order and tie
  both.
- **The operator restructured the workbook since last run.** Tabs deleted, columns moved, links
  repointed. Re-detect, reconcile against the spec, and confirm before writing.
- **An inherited formula bug in the prior year's workbook.** These exist — subtotal rows whose
  analysis formulas point a row or two off. Fix it in the new build and **record it in the spec so
  it doesn't get copied forward again.**
- **A budget that lumps two accounts together, or spreads flat at 1/12.** If the client's budget
  source does this, mirror it so the analysis tab ties line-for-line to what the board sees — and
  flag it for cleanup rather than silently correcting it.
- **A mid-year amended budget.** Its actuals columns are usually rounded and carry manual reclasses.
  **Never use them as actuals** — actuals always come from the financials PDF.
- **No prior workbook at all.** That is a build, not an update. Stop and hand it back to the
  engagement's controller.
