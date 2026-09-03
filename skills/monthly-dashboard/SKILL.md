---
name: monthly-dashboard
description: >
  Build the one-page monthly financial dashboard for any Paxus CFO, advisory, or bookkeeping client —
  non-profit or for-profit. For non-profits it fronts the monthly board financials package (CFO /
  non-profit clients); for for-profit clients it is the client's own monthly dashboard (Wheel of Service
  businesses, advisory clients, and similar). Pulls
  monthly financials from the Paxus shared Drive via the gws CLI, computes bespoke KPIs
  against confirmed benchmarks, renders a brand-consistent one-page dashboard to PDF, and either merges
  it as page 1 of the board package, delivers it standalone, or hands it off to the monthly client
  email. For repeat clients, uses the prior delivered dashboard and the per-client spec file as the spec; for
  brand-new clients, runs a cold-start intake, defaults to standalone/no-trend, documents benchmark
  sources, and saves the approved spec for future months. Use when the operator asks to build a monthly
  dashboard, make the dashboard, build the board/client dashboard, add the dashboard to monthly
  financials, or prepend a dashboard to a board financials package. SCOPED TO THE DASHBOARD PAGE — it
  does not draft the client email or update the forecast workbook.
---

# Monthly Financial Dashboard

Produces the one-page **monthly financial dashboard** for a Paxus client. For a **non-profit** it fronts
the monthly board financials package (audience: the board); for a **for-profit** client it is the
client's own monthly dashboard (audience: the owner/management). Either way it summarizes the month at a
glance — against the client's KPIs where the client has them — on a single printed Letter page.

**Two axes drive every build: client type (non-profit / for-profit) and history (repeat / cold-start).
Layout, KPIs, benchmarks, methods, audience, and delivery mode are all client-specific.** For repeat
clients, the client's own most recent delivered dashboard is the spec. For first-run clients, establish
the spec explicitly, default to standalone/no-trend, and preserve it so the next month has history.

First built for a non-profit with a **merged page-1, monthly-trend** layout. Validated as generalizing on a
second non-profit with a **standalone, no-trend** layout (4 header tiles + 4 KPI cards, revenue-mix + Top
Grants, Budget-vs-Actual, cash-by-account, A/R buckets, activity callout) — whose layout, KPIs, benchmarks,
and delivery differ on every axis. Two real non-profit clients, two different dashboards: proof the spec is
per-client, not one canonical template.

The **for-profit path is validated on a real for-profit client** (July 2026) — it is no longer provisional.
Build with it directly, no caveat to the operator. The same discipline applies on either path: that client's
own prior dashboard plus its `dashboard-spec.md` are the spec for its next month.

KPIs are always a confirmed input, never invented. On repeat runs, recover them (plus benchmark bands,
formulas, header methods, and color/label conventions) from the client's prior dashboard PDF and confirm
only unresolved conflicts. On cold starts, confirm the metric list, formulas, benchmark sources, layout,
and delivery mode before building.

**Some clients have no KPIs at all, and that is a normal outcome — not a gap to fill.** Bookkeeping-only /
Full Service (books + notes) engagements typically carry no KPI tracking or benchmarks; KPIs are a CFO /
advisory / Wheel of Service deliverable. **If no KPIs are provided, say so plainly, confirm it once, and
build the dashboard with no KPI section.** Never substitute a proposed, derived, or "reasonable" metric set
for a confirmed one. A dashboard with no KPI cards is a complete dashboard.

**Visual scheme is the same for every client — non-profit and for-profit alike: the neutral navy/teal
board scheme** (see Step 4). This is intentionally NOT the official Paxus plum/mauve brand
(`/paxus-brand`) — keep all client dashboards consistent and institutional. Flag the choice only if the
operator ever asks to rebrand a specific client.

---

## Step 0 — Determine client type, then repeat vs cold-start

**First, establish client type — non-profit or for-profit.** It sets the audience (board vs
owner/management), the default KPI palette, the statements available, and the terminology ("board
package" vs "client dashboard"). If the client's type isn't obvious from the spec or the engagement,
confirm it with the operator before anything else. Don't apply non-profit constructs (program
efficiency, grants, fund classes, budget-vs-actual) to a for-profit client, or commercial constructs
(gross margin, runway) to a non-profit.

Then read the client's confirmed-spec file. **The spec lives in the shared firm client folder, not in any
one operator's private notes**, so every Paxus teammate who runs this skill gets the same spec:

```
~/paxus-ai/clients/<slug>/dashboard-spec.md
```

(the `<slug>` folder created by `/paxus-skills:client-context`). The spec records the confirmed
KPIs/benchmarks/formulas/methods, layout, delivery mode (merged vs standalone), the resolved Drive
shared-drive + folder IDs and file-name pattern, and recurring watch-outs. If a client was specced before
this shared-folder convention (the earliest non-profit specs were captured in an operator's personal
notes), migrate that spec into `dashboard-spec.md` on the next run. If no spec file exists, this is a
cold start. Then search for the client's **prior delivered dashboard PDF** (Step 1).

**Repeat path:** If a prior dashboard exists, it is the spec. Pull it, read it, and recover the exact
layout, KPI set, benchmark bands, formulas, header-tile methods, color/label conventions, delivery
mode, and naming pattern. Ask the operator only for what neither the spec nor the prior dashboard can
establish. If the spec and the prior PDF conflict, treat the latest delivered PDF as authoritative unless
the operator says it was wrong or the spec has changed. **A prior dashboard with no KPI cards — or a spec
recording `kpis: none` — establishes that this client has no KPIs.** That's the confirmed spec: rebuild the
no-KPI layout and don't reintroduce a KPI section unless the operator asks for one.

**Cold-start path:** If no prior dashboard exists, do not improvise from another client's dashboard. Use this
path for any client that needs a monthly financial dashboard, non-profit or for-profit. Establish:

1. **Delivery mode:** default to **standalone PDF**. Three modes are valid: (a) **merge as page 1** of a
   board package — only if the operator explicitly wants it prepended and there is a target package
   (typical non-profit); (b) **standalone PDF** (the default; either type); (c) **hand off to the monthly
   client email** — for for-profit Wheel of Service / advisory clients whose dashboard rides along with
   `/monthly-client-email`. This skill produces the PDF and stops; it never drafts the email (see scope).
2. **Starting layout:** default to a **standalone, no-trend** one-page layout. Start from the
   client-agnostic `assets/dashboard-base.html` (never another client's dashboard), then adjust sections to
   the confirmed KPI set and available statements. Add monthly trend bars only if the operator explicitly
   asks and monthly P&L data is available.
3. **KPI metric list:** bespoke each time, always operator-confirmed. Ask the operator for the metrics
   and formulas. **"None" is a valid and complete answer.**

   **If the operator doesn't provide KPIs, do not fill the gap.** State it plainly and confirm once —
   *"I don't have KPIs for this client. Should I build this dashboard with no KPI section?"* On a yes, build
   the **no-KPI layout** (Step 4), skip the KPI math (Step 3), and record `kpis: none — confirmed <date>` in
   the spec so next month doesn't re-ask. Engagement tier is the usual reason: bookkeeping-only / Full
   Service (books + notes) clients typically have no KPI tracking or benchmarks — that's a CFO / advisory /
   Wheel of Service deliverable.

   Only if the operator asks for candidates, propose a short list from the financials as an explicit
   discussion draft — and **never treat proposed metrics as confirmed** or let them reach the delivered
   dashboard on silence. Propose from the client type's typical palette:
   - **Non-profit:** Operating Margin, Revenue Growth (YTD), Program Efficiency (program ÷ total expenses
     from P&L by Class), Revenue Diversification (grants share — concentration flag), A/R Aging 91+ (flag).
   - **For-profit:** Gross Margin %, Net (Operating) Margin %, Revenue Growth (YoY or YTD), A/R days and
     A/P days, Current Ratio, Cash Runway (months of operating cash). Propose the subset the financials
     support; drop any the available statements can't derive rather than approximating.
4. **Benchmarks:** never fabricate. Legitimate sources are operator-provided board/management targets,
   budget targets, covenants or grant requirements, documented policy, or cited sector norms. If using
   sector norms, record the source/date in the work notes and in the saved spec. If no defensible
   benchmark exists, make the metric monitor-only or a risk flag instead of assigning a pass/fail band.
   **For-profit benchmarks are industry-specific — do not apply one band across industries.** Construction
   margins, professional-services margins, and non-profit ratios are not comparable. The most defensible
   cold-start sources for a for-profit client are the client's **own prior-year self-comparison** and
   **owner/management targets**; use cited industry norms only when neither exists, and record which
   industry (e.g. construction vs professional services) the norm came from.
5. **Sections and snapshot tiles:** confirm which sections matter for the first month (e.g. YTD revenue/
   expenses/net, cash, budget vs actual, revenue mix, grants/customers, A/R aging, A/P/LOC, activity
   notes). Omit sections with missing data rather than filling with guesses.
6. **Persistence target:** after approval, create `~/paxus-ai/clients/<slug>/dashboard-spec.md` so month 2
   has a spec — and the resolved Drive IDs — even before the prior PDF is pulled. (Shared firm location, not
   personal notes, so any teammate can run month 2.)

## Required Inputs — Confirm Before Proceeding

Do not begin until ALL of the following are confirmed (recovered from Step 0 where possible):

1. **Client** — which CFO/non-profit client.
2. **Month + period** — the reporting month and the YTD range (e.g., "May 2026, Jan–May").
3. **KPIs and benchmarks** — the specific KPIs this client tracks, each formula, each benchmark band or
   risk threshold, and the source for each benchmark. **Client-specific — recover from the prior dashboard
   on repeat runs; confirm bespoke inputs on cold starts. Never invent.** **A confirmed "this client has no
   KPIs" satisfies this input** — the dashboard then ships with no KPI section (Step 0 item 3, Step 4). What
   is never acceptable is proceeding with a KPI set the operator didn't confirm. Illustrative non-profit sets (the
   actual list/bands are per client): e.g. Operating Margin (−5% to +5%), Revenue Growth YTD (3%–8%), Program
   Efficiency (75%–85%); or Operating Margin (0–10%), Program Efficiency (65–85%), Revenue Diversification
   (grants share — concentration flag), A/R Aging 91+ (risk flag). Formulas and header-tile methods can also
   differ per client (see Step 3).
4. **Financials location** — the Drive shared-drive + folder for this client's monthly financials. On
   repeat runs, read the resolved IDs from the client's `dashboard-spec.md` (don't re-search). On cold
   starts, resolve and record them (Step 1). Each client has its own shared drive (e.g. a drive named for
   the client) with a `Financials/<year>` folder.
5. **Delivery mode + target** — confirm from the prior package on repeat runs. On cold starts, default to
   **standalone PDF** unless the operator explicitly requests merged delivery and provides the target board
   financials package. Determines whether Step 6 runs at all.
6. **Cold-start spec record** — for a first run, confirm that the approved layout/KPIs/benchmarks/Drive-IDs
   will be saved to `~/paxus-ai/clients/<slug>/dashboard-spec.md` after operator review.

If anything is missing, stop and ask only for what's missing.

---

## Step 1 — Pull the source files (gws)

The local Google Drive path on macOS is sandbox-blocked (`Operation not permitted`) — **always use the
gws CLI**, never the local `CloudStorage` path. Everything in this step is a read; the only write this
skill ever makes is the finished dashboard in Step 7.

**Resolve the folder once, then store the IDs.** Drive has many same-named folders across clients (multiple
"Financials", "2026", etc.), so blind `name contains` searches are ambiguous and slow. On a **repeat** run,
read the resolved `drive_id` / `financials_folder_id` straight from the client's `dashboard-spec.md` and
skip discovery. On a **cold start**, resolve them once and record them in the spec:
- List shared drives (`gws drive drives list`) to get the client's **shared-drive ID** by name.
- Within that drive, walk to the `Financials/<year>` folder and capture its **folder ID**.
- When several same-named folders appear, disambiguate by parent chain — don't guess.
- Pass `--params` JSON via a file (heredoc) when a query contains a folder ID, to avoid shell-quote breakage.

1. `gws drive files list` with `includeItemsFromAllDrives:true, supportsAllDrives:true` scoped to the
   resolved `driveId` (`corpora:"drive"`). **The file set is client-specific:**
   - Some clients have **separate** detailed-financials and board-package PDFs. Pull both.
   - Some have **one combined** financials PDF carrying every statement — Balance Sheet, P&L by month,
     P&L YTD-vs-PY, P&L by Class, Budget-vs-Actual, A/R & A/P aging. One file is enough.
   - For repeat clients, always also pull the client's **most recent prior dashboard** (e.g.
     `MM.DD.YYYY <Client> Dashboard.pdf`).
   - For cold starts, search enough to confirm there is no prior delivered dashboard; record that this is
     the first-run path.
2. Download each with `gws drive files get --params '{"fileId":"…","alt":"media","supportsAllDrives":true}' -o <file>`
   into a working dir (e.g. `/tmp/<client>-financials/`).
3. **Repeat clients:** read the prior dashboard PDF and recover the spec — exact layout (which sections,
   in what order), KPI set, benchmark bands, formulas, header-tile methods, and color/label conventions.
   The new month matches it. This is the authoritative source for "what this client's dashboard looks like."
4. **Cold-start clients:** document the confirmed first-run spec before extracting figures: delivery mode,
   layout sections, KPI list, formulas, benchmark source/band, omitted sections, and naming convention.

---

## Step 2 — Extract the figures (no fabrication)

From the financials PDF(s), read exactly — never estimate or fabricate a figure. Read the **basis**
(cash vs accrual) off the statement header and note it; it changes how aging and margins read. Pull only
what the client's layout actually uses (don't extract trend data for a client whose dashboard has no trend):

- **Income Statement, YTD vs PY** (the comparison P&L): Total Revenue, Total Expenses, Net Income for
  current YTD and prior-year YTD, plus the QBO-computed % change.
- **Income Statement by month**: each month's net income — only if the client's layout has a monthly trend.
- **P&L by Class** (functional statement): program-class total expenses vs total expenses — basis for
  Program Efficiency. (e.g. `TOTAL *PROGRAMS` ÷ `TOTAL` expenditures on the P&L by Class.)
- **Budget vs. Actual**: notable-line actual/budget/variance and the YTD `% of budget` figures — if the
  client's layout has a budget section or budget-based header sub-lines.
- **Balance Sheet**: Total Bank Accounts (cash position; also per-account balances if the layout lists
  them), Total A/R, A/P, and any operating line-of-credit balance (current vs year-end → YTD draw).
- **A/R Aging**: bucket breakdown and largest aged balances for the observations.

Watch for one-time / timing items (an annual pledge, a large or front-loaded grant, an unexpected
one-time donation) that distort a month's or the YTD revenue, margin, or net income. These MUST be
flagged in the observations and footnoted — never let them read as an operating run-rate. (e.g. a large
grant front-loading Q1 makes the YTD surplus a timing artifact, not a run-rate.)

---

## Step 3 — Compute KPIs and snapshot

**KPI formulas are per-client — use the ones the prior dashboard establishes or the cold-start intake
confirms — and the exact formula + day-count convention MUST be written into the client's `dashboard-spec.md`
so every later month computes it identically.**

**No-KPI clients: skip the KPI math entirely.** Compute only the headline snapshot figures the client's
layout actually shows, then go to Step 4's no-KPI layout. Do not compute metrics "just in case," and do not
slip a derived ratio onto the page as a stand-in for a KPI — a ratio with a benchmark next to it *is* a KPI,
whatever it's labeled.

Standard formulas by client type:

**Non-profit:**
- **Operating Margin** = Net Operating Income ÷ Total Revenue. (e.g. bands like −5%–+5% or 0–10%, per client.)
- **Revenue Growth (YTD)** = QBO YTD-vs-PY total income % change.
- **Program Efficiency** = program-class expenses ÷ total expenses, from the P&L by Class. **Same method
  month over month** so it's comparable. (e.g. bands like 65–85% or 75–85%; classification-driven — volatile
  early in the year as coding catches up.)
- **Revenue Diversification** = grants ÷ total revenue — a concentration *flag*, not a pass/fail band.
- **A/R Aging (91+)** = 91+ bucket ÷ total A/R — a follow-up *flag*.

**For-profit** (define the convention once, record it, reuse it):
- **Gross Margin %** = Gross Profit ÷ Total Revenue.
- **Operating Margin %** = Net Operating Income ÷ Total Revenue. **Net Margin %** = Net Income ÷ Total Revenue.
- **Revenue Growth** = (YTD revenue − PY-YTD revenue) ÷ PY-YTD revenue (the QBO comparison-P&L % change).
- **Current Ratio** = Total Current Assets ÷ Total Current Liabilities (Balance Sheet).
- **A/R Days (DSO)** = Total A/R ÷ (YTD revenue ÷ days elapsed), where **days elapsed = calendar days from
  fiscal-year start through the statement date** (e.g. Jan 1–May 31 = 151). State the day-count in the spec.
- **A/P Days (DPO)** = Total A/P ÷ (YTD COGS ÷ days elapsed), same day-count convention.
- **Cash Runway (months)** = Cash ÷ average monthly net cash burn — **meaningful only for a cash-burning
  client. If the client is profitable (positive operating cash), mark it N/A and use a Cash-Position /
  months-of-operating-expense read instead** — don't show a meaningless or infinite runway.

**Header-tile / snapshot methods can also differ — recover them from the prior dashboard or confirm them
in the cold-start intake. Don't assume.** E.g. one client's "YTD Revenue/Expenses" tiles may be **operating
only**, while "Net Revenue YTD" is **total net incl. interest/other**; `% of budget` comes from the
Budget-vs-Actual YTD budget. Typical snapshot lines: Total Revenue, Total Expenses, Net Income (Loss),
Cash Position (= total of all bank accounts), Total A/R, with sub-lines for % vs PY, % of budget, cash
vs YE / LOC draw, A/P note.

**Rules:** Round every dollar to the nearest hundred (percentages, ratios, and day-counts are NOT rounded
to hundreds — show them at sensible precision, e.g. 49.3%, 2.45, ~25 days). KPI status color is not
strictly binary: green when within/favorable, red for genuine risk (concentration, heavy aging), and
**amber/neutral when a figure is outside a band but not alarming** (e.g. a surplus "above range", a ratio
improving toward range). Match the prior dashboard's labels and colors. If a figure can't be derived,
write "[Insufficient data]" — do not guess.

**Tie-out checklist — run before building the HTML.** Every figure on the dashboard must trace to the
statements and the math must foot:
- Total Revenue − Total COGS = Gross Profit; Gross Profit − Operating Expenses = Net Operating Income;
  NOI + net other income/expense = Net Income — each ties to the P&L.
- Total Current Assets and Total Current Liabilities foot to the Balance Sheet; Current Ratio recomputes.
- A/R aging buckets sum to Total A/R; revenue-by-source/channel sums to the income total used.
- Every KPI recomputed independently from the source figures (don't trust a single read).
- Headline tiles match the statement (and the budget %, if shown, matches the Budget-vs-Actual).

---

## Step 4 — Build the dashboard HTML

**Never start a build from another client's dashboard.** Each client's dashboard is built only from the
shared client-agnostic base template plus *that same client's* own prior dashboard and spec file. Opening
one client's worked dashboard to build another's would leak that client's data into the starting point —
barred by confidentiality (operator's CLAUDE.md: never reference one client's details in content going to
another) and by operator preference. The base template is the only cross-client shared asset.

**The only shared asset is `assets/dashboard-base.html`** — a neutral house-style scaffold with the
navy/teal CSS, header tiles, KPI cards, two-column sections, a commented-out trend block, and a notes
callout. **No client names, no real numbers.** This is the canonical look and the single starting point for
every cold-start. **No client's worked dashboard ever lives in this skill's `assets/`** — that would ship
one client's data to every teammate. Client-specific material lives with the client (Drive + client folder),
never in the skill.

- **Cold-start clients:** copy `assets/dashboard-base.html`, then fill it from this client's confirmed
  cold-start spec (sections, KPI count, delivery). Default standalone/no-trend; enable the trend block only
  if the spec calls for it and monthly data exists. The approved layout is captured in the client's
  `dashboard-spec.md` (sections/KPIs/methods) — that spec, plus the delivered PDF, is what month 2 rebuilds from.
- **Repeat clients:** the client's own prior **delivered dashboard PDF** (in its Drive `Financials/<year>`
  folder) plus its `dashboard-spec.md` are the spec. Reconstruct the HTML from `dashboard-base.html` following
  the spec and matching the prior PDF exactly, with the new month's actuals. (A teammate may keep a convenience
  HTML copy of the prior in the client's own folder — never in this skill.)
- **No-KPI clients:** delete the KPI block from the template outright — the `Key Performance Indicators`
  section head and its `.kpi-row`. Don't leave empty cards, placeholder benchmarks, or "n/a" status chips on
  the page. Reflow the freed vertical space into the sections the client *does* get (headline tiles, cash,
  revenue mix, budget vs actual, A/R, activity notes) so it still reads as a deliberate, full one-pager. The
  dashboard is then a **financial-position snapshot rather than a scorecard**: keep the observations
  descriptive — what changed, what to watch — with no pass/fail, benchmark, or status-color language.

- **Bar widths (revenue by source / stacked mix):** `width% = round(value ÷ total_or_largest × 100)`.
  For tiny bars or "n/a" prior-year values, use the `.bar-wrap` + `.bar-out` pattern so labels aren't clipped.
- **Trend bars (only if the client's layout has them):** loss months in the lower zone (`.nz`, red `#c0392b`),
  positive months in the upper zone (`.pz`, green `#2e8b57`), all anchored to the shared dashed zero line —
  never let a positive bar "float." Height px = `round(abs(month_ni) ÷ largest_abs_monthly_ni × 52)`.
- **Color scheme:** keep the navy/teal/green-red scheme for board-package consistency. This is
  **intentionally NOT** the official Paxus plum/mauve brand (`/paxus-brand`) — flag the choice if the
  operator ever wants to rebrand, but default to matching the prior board packages.

---

## Step 5 — Operator reviews the HTML first, then render to PDF

**Always review the HTML before converting to PDF.** The HTML is the review artifact; the PDF is only the
final export. This saves tokens — iterating on a text HTML file is cheap, and reading a rendered PDF back
into context as an image is expensive. Do **not** render or read back a PDF until the HTML is approved.

1. **Show the operator the HTML.** Write the dashboard to `<client>-dashboard.html` and hand them the
   absolute path to open in a browser (`open "<abs-path>/dashboard.html"` opens it for them). Tell them what
   to check: the KPI values and benchmark colors (if the client has KPIs), the snapshot figures, the
   observations wording, and that it reads as one page.
2. **Iterate in HTML.** Apply requested changes as text edits to the HTML and re-show. Stay in HTML for all
   content/layout/number corrections — never round-trip through PDF to make an edit.
3. **Only after the operator approves the HTML, render to PDF (one shot):**

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="<client>-dashboard.pdf" "file://<abs-path>/dashboard.html"
```

4. **Verify one page cheaply — do not read the PDF back as an image.** Check the page count with a text
   tool (`python3 -c "import pypdf;print(len(pypdf.PdfReader('<client>-dashboard.pdf').pages))"` or
   `pdfinfo`). If it's more than one page, the HTML overflowed — fix spacing in the HTML (zone heights,
   margins, `.bar-item`/`.obs`/table spacing), re-render, re-check the count. Visual correctness was already
   confirmed by the operator's HTML review, so a PDF image read-back is unnecessary in the normal path.

---

## Step 6 — Merge as page 1 (merged-delivery clients only)

**Skip this step for standalone-delivery clients** — their dashboard ships as its own
file; go straight to Step 7. For merged-delivery clients, **back up the original board file first** (copy it
aside before any operation that overwrites it), then prepend with pypdf:

```bash
pip3 install --quiet pypdf   # if not already present
python3 - <<'PY'
import pypdf
w = pypdf.PdfWriter()
for p in pypdf.PdfReader("<client>-dashboard.pdf").pages: w.add_page(p)
for p in pypdf.PdfReader("<board-financials>.pdf").pages: w.add_page(p)
with open("<board>-with-dashboard.pdf","wb") as f: w.write(f)
PY
```

First confirm the board file doesn't already start with a dashboard (read page 1) so you don't
double-add. Verify the merged page count and that page 1 is the dashboard.

---

## Step 7 — Operator review, upload, and persistence

**Try the upload; fall back to the operator if it fails.** gws can write to Drive when the operator's
account allows it — attempt the upload, and hand off the local path only if it doesn't go through. Never
change or widen the gws scope to make an upload work: if it fails, that is the fall-back path, not a
problem to solve.

**Ask before uploading.** The operator approves the dashboard content at Step 5; uploading puts a file in
the client's Drive, which is a separate decision. Confirm it plainly — *"Want me to save this to their
Drive, or hand you the file?"* — unless they already said to file it.

**Step 7a — attempt the upload** (standalone and merged modes; skip for email ride-along):

```bash
cd <folder containing the PDF>      # --upload only accepts a path INSIDE the working directory
gws drive files create \
  --json '{"name":"MM.DD.YYYY <Client> Dashboard.pdf","parents":["<financials-folder-id>"],"mimeType":"application/pdf"}' \
  --upload "MM.DD.YYYY <Client> Dashboard.pdf" \
  --params '{"supportsAllDrives":true,"fields":"id,name,parents,webViewLink"}'
```

- `--upload` rejects an absolute path outside the current directory with a `validationError`. `cd` to the
  file's folder first and pass a **relative filename** — this is the most common failure and it is not a
  permissions problem.
- On success, verify by listing the target folder, and give the operator the `webViewLink`.
- **A 403 / insufficient-permission error means this operator can't write to that drive.** Say so plainly
  and switch to the manual hand-off below. Don't retry, and don't try another scope or account.

Two separate gates decide whether the upload works, and it's worth naming which one failed:
1. **Drive role on that shared drive.** *Content manager* or *Manager* can upload; *Contributor* varies;
   *Viewer* / *Commenter* cannot. Roles differ per drive and per teammate — check with
   `gws drive permissions list --params '{"fileId":"<driveId>","supportsAllDrives":true}'`.
2. **gws being installed and authenticated** on that person's machine at all.

**Step 7b — manual hand-off** (when the upload isn't possible, wasn't wanted, or the mode is ride-along).
Hand the operator the exact local path plus the steps for the client's delivery mode:

- **Merged:** open the existing board financials file → **Manage versions → Upload new version**
  (keeps the link stable and a recoverable prior version), or replace it.
- **Standalone (standalone non-profits and for-profit clients):** upload as a **new file** in the client's
  `Financials/<year>` folder, named to match the convention (e.g. `MM.DD.YYYY <Client> Dashboard.pdf`).
- **Email ride-along (for-profit Wheel of Service / advisory):** there is nothing to upload here — the
  dashboard rides along with the monthly client email. Save the approved PDF to a known working path and
  hand the operator that path; they attach it (or pass it to `/monthly-client-email`). This skill never
  drafts the email and never sends it.

**Record which path was used** in the client's `dashboard-spec.md`, so the next month starts from what
actually worked for the person running it rather than re-discovering it.

After operator approval, create/update `~/paxus-ai/clients/<slug>/dashboard-spec.md` (the **shared firm
location**, so any teammate can run next month). Mandatory for cold starts; required whenever a repeat
client's spec changes. Record:

- Client name and type (NP/FP), reporting month used for the first/updated spec, accounting basis, and the
  upload/naming convention.
- **Resolved Drive IDs:** shared-drive ID, `Financials/<year>` folder ID, and the source-file name pattern —
  so the next run skips Drive discovery.
- Delivery mode (merged / standalone / email ride-along) and target-package rules.
- Layout sections in order, header tiles, KPI card count, template/asset used, and whether trend bars are
  included.
- KPI list, **exact formulas and day-count conventions**, benchmark bands or risk thresholds, and the source
  for each benchmark (operator, board/owner target, budget, covenant/grant requirement, policy, or cited
  industry norm — name the industry for FP). **If the client has no KPIs, record `kpis: none (confirmed
  <date>)`** — an explicit record, not an omitted field, so next month builds the no-KPI layout without
  re-asking and no future run mistakes the blank for an oversight.
- Known data caveats: unavailable statements, class-coding dependencies, one-time/timing items, and any
  monitor-only metrics with no defensible benchmark.

---

## Cold-Start Edge Cases

**History / spec resolution**
- If a prior delivered dashboard appears mid-run, switch to the repeat path and use it as the spec unless
  the operator says the new dashboard should intentionally differ.
- If there are multiple possible priors, use the most recent delivered/approved dashboard, not drafts or
  working files. Ask only if delivered status is unclear.

**Data availability** (most common on a brand-new client whose books are young)
- **No prior-year comparison** (new QBO file, client onboarded this year): any YoY/YTD-growth metric is
  underivable → make it monitor-only, show the current figure without a growth %, and note "no PY in QBO."
- **First fiscal month:** YTD = one month, no trend, budget-vs-actual barely meaningful. Drop the trend
  section and lean on the single-month snapshot; say so in the observations.
- **Books mid-cleanup / not closed:** KPIs are volatile and may restate. Footnote the dashboard
  "preliminary — books in onboarding cleanup," same spirit as the program-efficiency caveat.
- **Cash-basis books:** A/R / A/P aging and accrual margins are misleading → omit aging, and flag that
  margins reflect cash timing, not earned activity. Confirm basis with the operator if unclear.
- **No budget loaded / no class or department tracking:** drop the budget-vs-actual tiles and any
  class-derived metric (program efficiency for NP, segment margin for FP) rather than approximating.

**Metrics & benchmarks**
- **No KPIs provided:** confirm that explicitly, then build with no KPI section and record `kpis: none` in
  the spec. Never invent a KPI set, never promote a candidate list into the delivered dashboard because the
  operator didn't answer, and never treat a missing KPI list as a blocker — it's a layout decision, not a
  gap. Bookkeeping-only / Full Service clients are the common case.
- If no benchmark source exists, do not make up a band. Use monitor-only, directional language, or a risk
  flag until the operator approves a benchmark source.
- If a confirmed KPI depends on unavailable data (no class P&L, no budget, no A/R aging, no prior-year
  comparison), mark it "[Insufficient data]" or omit it with operator approval. Do not substitute a similar
  metric without confirmation.
- **For-profit benchmarks are industry-specific.** Do not carry a construction client's margin band onto a
  professional-services client. Prefer the client's own prior-year self-comparison or owner targets; cite
  the industry when using an external norm.
- If sector norms are used for benchmarks, cite enough detail in the work notes and saved spec for a future
  agent to understand why the band was legitimate.

**Delivery & layout**
- If merged delivery is requested but there is no target board package yet, deliver standalone first and
  note that it can be prepended later.
- If the dashboard is meant to ride along with the monthly client email (for-profit Wheel of Service /
  advisory), produce the standalone PDF and hand off the path — do not draft the email here (`/monthly-client-email`
  owns that).
- If the cold-start layout overflows one page, preserve the confirmed KPI cards and headline snapshot first;
  trim detail tables, combine observations, or defer lower-priority sections rather than shrinking text into
  unreadability.

## Important Rules (Always Follow)

Quick cheat-sheet; the steps above are authoritative.

- **Never reference another client.** Build only from `assets/dashboard-base.html` + *this same client's* own
  prior dashboard and spec. A different client's dashboard/figures are never a template — confidentiality.
- **Client type first** (NP vs FP) — it sets audience, KPI palette, statements, terminology. Never mix the two.
- **Confirm, never invent.** KPIs, formulas, and benchmarks are client-specific and operator-confirmed.
  Recover them from the prior dashboard + `dashboard-spec.md` on repeats; establish + record them on cold starts.
- **No KPIs = no KPI section.** If KPIs aren't provided, confirm that once and build the dashboard without
  them — never make some up, and never let a proposed candidate list stand in for a confirmed one. Record
  `kpis: none` in the spec.
- **Round dollars to the nearest hundred;** never estimate or fabricate a figure. Tie every number to the
  statements before building.
- **Same method every month** for any class/ratio metric (NP Program Efficiency; FP margins/DSO/DPO) — the
  formula and day-count live in the spec so months stay comparable.
- **Flag one-time/timing items** (pledges, front-loaded grants, one-time donations, one-off gains) — footnote
  them; never let them read as run-rate.
- **One page, navy/teal scheme** for every client (not the Paxus brand) unless the operator says to rebrand.
- **Delivery is per-client:** merged page-1, standalone file, or email ride-along. Ask before filing to
  Drive, then **try the upload and fall back to handing over the file** if the operator's account can't
  write. Never widen the gws scope to force it. Back up the original before any merge/overwrite.
- **Spec is shared, not personal:** persist to `~/paxus-ai/clients/<slug>/dashboard-spec.md` so any teammate
  can run next month.

## Persistence note

Two kinds of state, two homes:
- **The skill itself** (this `SKILL.md` + `assets/`) lives in the **Paxus firm skills repo**, committed via
  `/paxus-skills:manage-skills`. It is firm-specific — keep it out of any shared general-purpose product repo.
- **Per-client specs and delivered dashboards** live with the client: `dashboard-spec.md` in
  `~/paxus-ai/clients/<slug>/`, and the PDF in the client's Drive `Financials/<year>` folder. Never store
  client specs in one operator's personal notes — teammates must be able to run the skill and get the same spec.

**Self-contained:** this skill must not depend on any one operator's private notes or vault rules — a
teammate running it from the firm repo won't have those. State principles inline rather than linking them.

**Status:** validated on real clients on both paths — two non-profit clients and one for-profit client
(July 2026). Neither path is provisional; build with either directly.
