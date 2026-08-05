---
name: paxus-quote
description: Build the firm's standard client service proposal — a four-page branded PDF (cover, service levels, add-ons, getting started) plus the cover email that carries it. Starts from the firm's standard Basic / Full Service / Premium ladder and its standard service elements, takes the fees the operator supplies, and turns them into a finished, brand-correct, page-verified quote. Run when someone says they need to build a quote, put together a proposal, send pricing to a prospect, or update an existing quote's numbers. This skill does not decide pricing — bring the fees with you.
---

# /paxus-quote — Client Service Proposal

You are building a Paxus service proposal: a **four-page PDF** and the **email that delivers it**. The operator brings the pricing; you produce the document. Follow the phases in order. Be conversational and warm — match the Paxus voice.

## The idea in one line

**The quote is lean; the email carries the context.** Four pages, nothing else — terms, assumptions, exclusions, and signature blocks all live in the engagement letter, not the proposal. Anything the client needs to *understand* goes in the cover email.

## Important rules for this skill

- **No fabrication.** If the operator hasn't given you a fee, a date, a contact name, or a scope line, leave the `[bracketed placeholder]` in place and tell them what's missing. Never invent a number or a service inclusion.
- **This skill does not set prices.** It formats decisions already made. Ask for whatever fees are missing and use exactly what you're given. Never derive, estimate, or suggest a fee to fill a gap — if the operator doesn't have a number yet, leave the placeholder in and tell them which one is outstanding.
- **Skills are the engine; client data is the fuel.** Nothing client-specific belongs in this skill or its template. Client scope, prior quotes, and engagement history live in the client's Google Drive folder (see `docs/context-model.md`).
- **Never send email.** The skill writes the email; a human sends it. Don't add SMTP or Gmail-API send paths — the manual step is the safeguard, and some operators also have a mechanical send-guard on top of it.
- **Don't rebuild the print CSS.** `templates/proposal.html` holds a page engine that is already correct and already hard-won. Fill the content; leave the `@media print` block alone.
- **If `templates/proposal.html` is missing**, stop and tell the operator the skill is corrupted and to re-install from the `paxus-skills` repo. Do not regenerate it from memory.

## The four pages — and what never appears

| Page | Holds |
|---|---|
| 1 — Cover | Logo, client name, one-line positioning, prepared-for block, 30-day validity |
| 2 — Choose your level | Price cards + the service comparison table, ending in a Monthly fee row |
| 3 — Optional add-ons | Add-on hero boxes; any separately-quoted service and its timing constraint |
| 4 — Getting started | One-time fees, total due at signing, next steps, one "Good to know" callout |

**Never put in a quote:** terms and conditions · assumptions lists · exclusions lists · signature or acceptance blocks · volume statistics · hours or rates · margin math. Terms belong in the engagement letter. Explanation belongs in the cover email. A quote that needs a page of caveats is a quote that hasn't been decided yet.

## The default tier ladder — start here every time

Unless the operator says otherwise, a Paxus quote offers three levels with the service elements below. **Do not rebuild this table from scratch on each quote.** Present it, ask what's different for this client, and adjust.

**Premium and "Wheel of Service" are the same service level.** Wheel of Service is legacy naming from older clients who sat at that tier under a different label. Use **Premium** on new quotes.

### For-profit clients — default elements

| Service element | Basic | Full Service | Premium |
|---|---|---|---|
| Dedicated account team (staff, lead, controller) | ✓ | ✓ | ✓ |
| Data entry of all transactions; monitoring bank & credit-card feeds in QBO | ✓ | ✓ | ✓ |
| Reconciliation of all balance-sheet accounts (bank, credit card, loan) | ✓ | ✓ | ✓ |
| Monthly financial statements | ✓ | ✓ | ✓ |
| Controller review | ✓ | ✓ | ✓ |
| Year-end close for tax preparation | ✓ | ✓ | ✓ |
| Financial statements with notes & analysis | — | ✓ | ✓ |
| 1099 preparation (filing fees separate) | add-on | ✓ | ✓ |
| Collaboration with your tax preparer | — | ✓ | ✓ |
| Monthly controller advisory call | — | — | ✓ |
| KPI tracking & benchmarking | — | — | ✓ |
| Budget / forecast | — | — | ✓ |
| Workers' comp audit support † | — | — | ✓ |

† **Only when the client runs payroll.** Drop the row entirely if they don't — it reads as padding.

### Non-profit clients — add these rows

Everything above still applies. A non-profit quote adds:

| Service element | Basic | Full Service | Premium |
|---|---|---|---|
| Class / program tracking for functional expense reporting | ✓ | ✓ | ✓ |
| Grant tracking | ✓ | ✓ | ✓ |
| Restricted vs unrestricted fund tracking (net assets) | ✓ | ✓ | ✓ |
| Board reporting package | — | ✓ | ✓ |

Non-profits have no tax preparer in the usual sense — reword that row to name the **990 preparer**.

**Keep these three straight — they are not the same mechanism, and conflating them produces a wrong sentence in the quote.**

- **Class / program tracking** exists for **functional expense reporting** — that's the 990 connection, and it's the *only* one. It is not "grant tracking," and it is not what makes the financials 990-ready in general.
- **Grant tracking** is separate work, tracked differently from functional expenses.
- **Restricted vs unrestricted** is net-asset accounting — separate again.

Never write a line like *"we keep your programs, grants, and restricted funds tracked the way your 990 needs them."* It collapses three different things into one and it isn't true.

### Rules for changing the default

- **Renaming a level is normal.** Both recent quotes did it: one used *Review-Only / Top-Tier*, another *Review & Reconcile / Full Service / Premium*. Rename freely when the client's decision is shaped differently — a level that exists only while the client keeps their own bookkeeper is worth naming for what it is.
- **Dropping to two levels is normal.** Delete the third card and column.
- **Adding a row is normal** when the engagement has a real element the default doesn't cover.
- **Silently removing a default row is not.** If a standard element is coming out, say so and confirm — an omission the operator didn't intend becomes a scope gap in a signed engagement.
- **A level where the client keeps their own bookkeeper** marks the coding and month-end rows as *Your team*, not as excluded. That distinction matters: it says who does the work, not whether it happens. This is a **deviation** from the default, not the default itself.

### What actually separates the three levels

**By default all three levels own the entire accounting function through monthly close.** That is not the differentiator, and a card description implying otherwise is wrong. What changes is the reporting and advisory layer on top:

| Level | What the client gets that the level below doesn't |
|---|---|
| **Basic** | Their monthly financial statements, delivered. |
| **Full Service** | Notes and analysis on the statements · 1099 preparation · collaboration with the tax or 990 preparer · board reporting package *(non-profit)* |
| **Premium** | A monthly advisory call · KPI tracking · budget and forecast support · workers' comp audit support *(when they run payroll)* |

**Write each price card's description to name what's new at that level** — not to restate what the level below already does. If two cards read almost the same, the tiering isn't being communicated.

### One-time fees — how the firm structures them

Two standard one-time items, billed on different schedules. Getting this wrong on page 4 misstates what the client owes up front.

| Item | How it's priced | When it's billed |
|---|---|---|
| **Onboarding** | A single figure | **Due at signing** — holds their place in the queue |
| **Cleanup** | A **floor-to-ceiling range**, never a blanket figure | **50% of the floor at the kickoff call**, balance at the end of the cleanup |

- Quote cleanup as a range (`$2,000–$3,000`) because the work depends on what's actually in the books. A single number becomes a cap you'll regret.
- The first cleanup payment is **50% of the floor**, not 50% of the midpoint or the ceiling. On a $2,000–$3,000 cleanup that's $1,000 at kickoff.
- **The "Total due at signing" bar shows only what is genuinely due at signing** — usually just onboarding. Never roll cleanup into it. If onboarding is the only at-signing item, you can drop the total bar entirely and let the onboarding figure speak for itself.
- Say the cleanup billing schedule in that item's description, so the range and its timing sit together.

### Pricing sanity check — non-profits price above for-profits

A non-profit at a given level is **more work** than a for-profit at the same level: functional expense tracking, grant tracking, and restricted-fund accounting all sit in every tier, including Basic. **Every non-profit tier should be priced above what the same tier would be quoted at for a comparable for-profit.**

This skill doesn't set prices — but if the operator supplies non-profit fees that look at or below their for-profit equivalents, **say so before building.** One sentence is enough: the extra tracking is real labor and it's in the lowest tier too.

### Common add-on gating

Gating is a judgment call per quote, but two patterns recur:

- **Outsourced CFO on a non-profit attaches to Premium only.** It's the firm's typical non-profit add-on and it assumes the Premium reporting layer underneath it.
- **Add-ons that replace client staff work** (invoicing, bill pay) don't belong on a level that assumes the client's own team is doing the daily work — that level exists *because* they have staff.

## Phase 1 — Gather (batched — ask once, not one at a time)

First establish two things, because they select the default table above: **for-profit or non-profit**, and **does the client run payroll**.

Then ask for everything else in a single message:

1. **Client and contact** — legal name for the cover, and who it's addressed to.
2. **One-line positioning** — what this engagement is, in a phrase ("Monthly bookkeeping, financial reporting & advisory").
3. **The fees** — one per level. Names default to Basic / Full Service / Premium; ask whether this quote renames or drops any.
4. **Deviations from the default table** — show it and ask what's different for this client. Rows to add, rows that don't apply, anything the client's own team keeps.
5. **Add-ons** — name, fee, one-line scope, and **which levels each one attaches to**. Gating is per add-on, not one blanket rule: some attach to Full Service and Premium, others to Premium only. There is deliberately no standing list — add-ons come out of the discovery call, so they're specific to what surfaced with this client. Outsourced CFO, invoicing, bill pay, and payroll are all common, but none is assumed.
6. **Separately-quoted services** — anything with its own timing (payroll conversions, cleanups), plus the constraint that drives the date.
7. **One-time fees** — onboarding, cleanup, and anything else. See § One-time fees below for how each is structured and billed; they are not all due at the same time.
8. **Start timing** — onboarding window and first close month.
9. **Scope boundaries** — what's expressly out, or quoted later. This is the "Good to know" callout, and it should be short.

Two judgment calls to raise if the operator hasn't:

- **Highlighting one level.** The template supports a `Recommended` badge on a single card. Use it only when the firm genuinely steers toward one option. When every level is a legitimate choice depending on what the client wants, leave it off — and keep it off in the cover email too, so the recommendation doesn't sneak back in through the prose.
- **Stating scope as a range.** Where a count could drift (invoices per month, bills, accounts), prefer a band — "covers 100 to 125 invoices a month" — or drop the number. A precise figure in a quote becomes a commitment the client measures you against, and a number you aren't sure of shouldn't be there at all.

## Phase 2 — Build

1. Copy `templates/proposal.html` to a working file named for the client.
2. Build the logo data URI from the design system and substitute it for `__LOGO_DATA_URI__`:

```bash
python3 -c "
import base64,pathlib,sys
p=pathlib.Path(sys.argv[1]); src=pathlib.Path(sys.argv[2]); out=pathlib.Path(sys.argv[3])
uri='data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
out.write_text(src.read_text().replace('__LOGO_DATA_URI__',uri))
" <path-to>/skills/paxus-design/assets/paxus-logo-full.png working.html "{Client Name} Quote.html"
```

Embedding the logo keeps the file self-contained, so it opens anywhere and emails as one attachment.

3. Replace every bracketed placeholder. Delete unused `OPTIONAL` blocks and any third tier card/column on a two-level quote.
4. Keep the brand exact — `#682145` plum, `#C084A4` mauve, `#ECD2E1` blush, `#F7EDF3` tint, Calibri throughout, logo centered. Pull from `/paxus-design` if you need more. **`#660033` is not a Paxus color** — if you see it in an older quote or tool, it's wrong; use `#682145`.

## Phase 3 — Export and verify (do not skip)

### Export — the way anyone on the team can do it

Open the HTML in **Google Chrome**, then:

1. <kbd>Cmd</kbd> + <kbd>P</kbd> (macOS) or <kbd>Ctrl</kbd> + <kbd>P</kbd> (Windows)
2. **Destination:** Save as PDF
3. **Paper size:** Letter
4. **Margins:** **None** — the template carries its own margins; anything else double-margins the page
5. **More settings → Background graphics: ON** — without this the plum cover and every shaded row print white
6. Save

*(If you're on a Mac with Chrome and want it scripted, this does the same thing:*

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="{Client Name} Quote.pdf" "file://<absolute-path>"
```

*Windows equivalent swaps in `"C:\Program Files\Google\Chrome\Application\chrome.exe"`.)*

### Verify — always, and on the PDF rather than the browser

**Both overflow failure modes are silent.** Content past the bottom of a sheet is clipped at the page boundary; it does not spill onto a visible extra page. A quote missing its fee row still looks fine at a glance. So check deliberately.

**Manual check — works for anyone, takes thirty seconds.** Open the PDF and confirm:

- It is exactly 4 pages (3 if there are no add-ons)
- Page 2 ends with the **Monthly fee row** and the page footer below it
- Every service element you intended is present — count the rows
- Page 4 shows **Total due at signing** and the footer
- The cover is plum, not white *(white = Background graphics was off)*

**Scripted check — if Python with PyMuPDF is available:**

```bash
python3 -c "
import fitz, re, sys
d=fitz.open(sys.argv[1]); norm=lambda t: re.sub(r'\s+','',t).lower()
print('pages:', d.page_count)
must={1:['Service Proposal','Valid for 30 days'],
      2:['Monthly fee','Paxus CPA Group'],
      3:['Paxus CPA Group'],
      4:['Total due at signing','Next steps','Paxus CPA Group']}
for i,pg in enumerate(d):
    n=i+1; t=norm(pg.get_text())
    miss=[m for m in must.get(n,[]) if norm(m) not in t]
    print(f'  p{n}:', 'complete' if not miss else f'MISSING {miss}')
" "{Client Name} Quote.pdf"
```

Add this quote's fees and level names to the `must` map — those are the strings that must never go missing. **Compare case-insensitively and with whitespace stripped**: letter-spaced headings come out of the text layer as `S E R V I C E  P R O P O S A L`. And use word boundaries in any substring test, or `thin` matches `think`.

### When page 2 overflows

The comparison table is what runs long. In order:

1. **14 or more rows — switch to compact mode.** Add `class="compact"` to the `<table>` and to the `<div class="cards">`, and `compact-intro` to the intro paragraph.
2. **At 15+ rows, drop the optional callout from page 2.** Compact mode plus a full 17-row non-profit table plus a real-length intro leaves no room for it — tested, and the footer falls off. The callout is optional for exactly this reason; move that explanation into the cover email, where it reads better anyway. **17 rows with no callout fits and is verified.**
3. **Still over?** Shorten row labels, or cut rows that aren't doing work. Past about 18 rows the table stops being scannable anyway, which is the real problem.
4. **Never add `overflow:hidden`.** It resolves the symptom by hiding your content.

### Brand check

```bash
python3 -c "
import re,sys,pathlib
s=pathlib.Path(sys.argv[1]).read_text()
allowed={'#682145','#c084a4','#ecd2e1','#f7edf3','#333333','#666666','#fff','#ffffff','#eee'}
bad=sorted({h.lower() for h in re.findall(r'#[0-9A-Fa-f]{3,6}',s)}-allowed)
print('off-palette:', bad or 'NONE'); print('#660033 present:', '#660033' in s)
" "{Client Name} Quote.html"
```

## Phase 4 — File it where the firm expects it

The finished quote goes in the prospective-client folder on the **`00 - Paxus CPA`** shared drive:

```
00 - Paxus CPA\Admin\Client Onboarding\Prospective Clients\{Client Name}\
```

- **Windows:** `G:\Shared drives\00 - Paxus CPA\Admin\Client Onboarding\Prospective Clients\{Client Name}\`
- **Git-Bash:** `/g/Shared drives/00 - Paxus CPA/Admin/Client Onboarding/Prospective Clients/{Client Name}/`
- **macOS:** the local Google Drive mount is often unavailable; upload with the `gws` CLI instead of hunting for a local path.

**Create the client's folder if it doesn't exist yet** — one folder per prospect, named with their legal name.

**Name the file `{Client Name} Quote.pdf`.** This matters beyond tidiness: `/onboard-client-admin` Phase 1A reads this folder when the client signs, looking for a file whose name contains *quote*, and pulls the packages, onboarding fee, cleanup structure, and earliest start date straight out of it. A quote filed under any other name is a quote that skill can't find.

Save the **HTML alongside it** — that's the editable source when the numbers change. `{Client Name} Quote.html`.

When the client signs, `/onboard-client-admin` moves the whole folder to `Active Clients`. Nothing to do here for that.

## Phase 5 — Write the cover email

The quote is deliberately thin, so the email carries everything the client needs to *understand* — while still being short.

**Write it to a plain `.txt` file next to the PDF; the operator pastes it into Gmail and sends.** Do not wire up a send path. The manual paste is the safeguard, and it's the library's convention. Name it `{Client Name} Quote - cover email.txt`.

Structure:

- **One warm opening line**, then the attachment.
- **The levels**, framed around the decision the client is actually making — not a re-listing of the table. If no level is being recommended, don't recommend one here either; the recommendation must not sneak back in through the prose.
- **Timing** — when work starts, and what stays with the client until then.
- **Anything with a constraint the client controls** — a broker, a third-party administrator, a system migration. Name what sits with them and the date it implies.
- **What the firm needs from them** to deliver any add-on they picked.
- **Any open questions**, phrased neutrally. If a question could read as criticism of the client's staff or their prior bookkeeper, soften it or suggest saving it for a call — and tell the operator which you did.
- Close with an offer to walk through it.

Short paragraphs with bolded mini-headers. Long paragraphs lose people.

Two things worth offering the operator:

- **A short walkthrough video.** Recording a two-minute Loom over the quote and dropping the link above the signature has worked well on past proposals — the email stays short and the detail lives in the video.
- **An internal rationale email** to the reviewing partner, when the quote wants a second opinion before it goes out: background, the structure, why these numbers, and anything worth flagging. **That one may contain hours and rates. The client-facing email never does.** Write it to its own `.txt` file.

*(If the operator has the `gws` CLI set up and prefers a ready-made Gmail draft, that's fine — build the MIME with the PDF attached, pass it as the Draft resource via `--json` (not `--params`, which is query-only and returns `411 Length Required`), pull their live signature from `settings.sendAs`, and then **read the draft back** to confirm what landed. Still a draft. Still never sent.)*

## Phase 6 — Verify before done

- [ ] PDF is exactly 4 pages (or 3, on a quote with no add-ons)
- [ ] Cover prints plum, not white — Background graphics was ON
- [ ] Page 2 ends with the Monthly fee row **and** its footer
- [ ] Every fee, level name, and total appears in the rendered text layer
- [ ] No off-palette colors; no `#660033`
- [ ] No bracketed placeholders left anywhere
- [ ] No terms, assumptions, exclusions, or signature block in the document
- [ ] "Total due at signing" reflects only at-signing items — cleanup is not rolled in
- [ ] Cleanup shown as a floor-to-ceiling range with its billing schedule
- [ ] No hours, rates, or margin figures in the client-facing file or email
- [ ] Cover email written to a `.txt` file for the operator to paste — nothing sent
- [ ] Recipient address verified before the operator sends, not copied from an old note
- [ ] PDF and HTML filed in the client's Prospective Clients folder, named `{Client Name} Quote.pdf` / `.html`

## Phase 7 — Learnings capture (mandatory)

Before declaring done, ask: *"Anything about the format or wording you'd want changed for next time?"* Append what they say to `learnings.md` beside this file:

```
## {YYYY-MM-DD} — {operator first name} — {client type, not client name}
- {what they changed and why}
```

Recurring corrections belong in this SKILL.md; run `/manage-skills` to propose the change.

## Edge cases

- **Two levels instead of three.** Delete the third card and the third column. The cards flex to fill.
- **A long comparison table** (14+ rows — common on a non-profit Premium quote). Switch the table and cards to `compact`; see Phase 3.
- **The operator is on Windows.** The manual Chrome export in Phase 3 is the path — don't hand them a macOS-only command.
- **No add-ons.** Delete page 3 entirely and renumber the footer. A three-page quote is fine.
- **Updating an existing quote's numbers.** Edit the saved HTML, re-render, re-verify. Never hand-edit a PDF.
- **The operator wants terms in the document.** Push back once: terms live in the engagement letter, and a quote that carries them stops being scannable. If they still want them, that's their call — put them on a fifth page rather than crowding page 4.
- **A count the operator isn't sure of.** Leave it out. An unverified number in a client document is worse than no number.
- **A figure that could read as criticism** of the client's staff or prior bookkeeper. Flag it and offer to move it to a call.
- **Older quotes and internal tools using `#660033` or a non-Calibri font.** Off-brand. Don't sample their palette; flag it to the operator.
- **The firm's rates changed.** They aren't in this skill by design — pricing comes from the operator and the fee calculator each time, so there's nothing here to go stale.
