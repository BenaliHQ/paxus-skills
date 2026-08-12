---
title: Phase 4 design notes (Kickoff prep packet + Team handoff email)
status: Reading-packet flow live as of 2026-08-12 — the claude.ai Onboarding Dossier dashboard is retired; the packet is now a plain markdown file the lead's /kickoff-prep skill reads from the client's Perm File
last_updated: 2026-08-12
---

# /onboard-client-admin — Phase 4 design notes

Phase 4 = produce the **kickoff prep packet** from what we already know (engagement / consultation / memo), and draft the team handoff email. Sends the Lead and Controller into the kick-off call with everything Jennifer's already learned.

The packet used to be a fill-in that Jennifer pasted, field-by-field, into a Claude Design dashboard (the "Paxus Onboarding Dossier"). **That dashboard is retired.** The packet is now a self-contained markdown file organized for *reading*, and the lead's `/kickoff-prep` skill reads it directly out of the client's Perm File. Same content, shaped for reading instead of pasting.

The Service Fee Template already exists in the client's folder before Phase 4 runs — it's created before the quote is prepared. Phase 4 only *reads* budgeted hours from it; it does not stamp a starter copy.

**Trigger:** Phase 3 (welcome packet + welcome email) is complete and the welcome email has gone out.

---

## Deliverables (two files)

1. **The kickoff prep packet** (markdown) — the single file the lead's `/kickoff-prep` skill reads to build the call sheet.
   Save to `G:\Shared drives\{Client Legal Name}\Perm File\Onboarding Dossier - {Client Legal Name} - fill-in.md`.
   (The packet lives with the client, not in the skill's handoffs folder, so the Lead — and `/kickoff-prep` — can find it inside the client's own Drive.)
2. **Team handoff email** — drafted as markdown; Jennifer pastes into Gmail.
   Save to `~/.claude/skills/onboard-client-admin/handoffs/{slug}-{date}-team-handoff-email.md`
   (email drafts stay in the skill's handoffs folder — they're internal to Jennifer's workflow, not a client artifact).

---

## Inputs (already in place from prior phases)

| Source | Path | Reason |
|---|---|---|
| Phase 1 handoff | `~/.claude/skills/onboard-client-admin/handoffs/{slug}-{date}.md` | FC client ID, primary contact, package, monthly fee, cleanup figures |
| Engagement PDF | `Active Clients\{Client Legal Name}\Engagement - {Client Legal Name}.pdf` | Authoritative billing line items, signatory, signing date |
| Quote PDF | `Active Clients\{Client Legal Name}\*Quote*.pdf` | Package selected, recommended tier, services not in scope |
| Consultation / PNCR | `Active Clients\{Client Legal Name}\*Potential New Client Review*.gdoc` (Google-native) or `*Consultation*.pdf` | Pain points, current setup, stakeholders, scope nuance |
| Memo to File | `Active Clients\{Client Legal Name}\*Memo to File*.docx` | Internal notes — entity context, ownership, decisions |

If the engagement is in `Perm File\` as well as Active Clients, prefer the Perm File copy.

**PNCR gotcha:** Potential New Client Review docs are often Google-native `.gdoc` pointers that can't be read from disk. If the skill can't parse them, ask Jennifer to paste the content into chat rather than leaving Discovery fields TBD.

---

## The kickoff prep packet (the `/kickoff-prep` contract)

- **The filename is a contract.** `/kickoff-prep` searches the client's Perm File for exactly `Onboarding Dossier - {Client Legal Name} - fill-in.md`. Keep the name — it's the handshake between the two skills, not a pointer to any live dashboard. (The lead-side contract is documented in the `kickoff-prep` skill under `references/dossier-fields.md`.)
- **It's a reading file, not a paste-source.** No dashboard URL, no "paste each section," no client switcher. The Lead — or the `/kickoff-prep` skill — opens the file and reads it top to bottom.
- **Skill's job:** produce the markdown packet, filled from the engagement / consultation / memo, with every field either filled or explicitly `TBD — ask on call`.

### The completeness rule (why silent blanks are banned)

`/kickoff-prep` classifies every field as one of three states:

| State | What the lead side does with it |
|---|---|
| **Filled** | Flows onto the call sheet as fact. |
| **`TBD — ask on call`** | Becomes a discovery question on the call sheet (agenda item 06). Working as intended. |
| **Missing / silently blank** | Ambiguous — can't tell "genuinely unknown" from "not filled in yet." Gets flagged loudly in a "Request from firm admin" block. |

So Phase 4 must never leave a field silently blank. If a value can't be known yet, write `TBD — ask on call` **verbatim** — that exact string is the signal the lead side keys on.

### Blocks and fields (in reading order)

**Header** — Client legal name · Lead (name) · Kickoff (date or `TBD — ask on call`) · Deadline (onboarding-complete target, e.g. `08/31/2026`) · Team of 3 — **Lead / Staff / Controller** (first names).

> Role labels are the firm's own terms — **Lead / Staff / Controller**. The retired dashboard used Lead / Accountant / Reviewer (Accountant = Staff, Reviewer = Controller); those labels are gone.

**Billing** (engagement is authoritative — the engagement often consolidates line items the quote itemized):
- Monthly amount — the headline the client is drafted for. If it bundles a sub-item (service fee + software subscription), note the breakdown but never report a sub-item as the monthly fee.
- First draft date.
- Onboarding fee + paid status.
- Cleanup amounts — record **whichever shape the engagement uses**: deposit + balance (two fixed one-time items) OR floor / ceiling (a range). Don't coerce one into the other; never report a ceiling that isn't there. `N/A` if no cleanup in scope.
- Exact figures — `$799` is not `$800`. Never round a contractual amount.

**Team and budgeted hours** — Lead / Staff / Controller, each with name + budgeted hours. Staff may stay `TBD` client-facing. Hours come from the client's Service Fee Template (see below); if that block was unpopulated and tier defaults were used, **say so explicitly**, and note the Lead refines the hours after kickoff.

**Cleanup scope** — the punch list as quoted, gathered in one place: Cleanup in scope? (`No` → the lead side renders the no-cleanup variant) · Punch list (one line per item) · Cleanup window (start + target end) · First monthly close month.

**Volumes and complexity** — gathered in one place: bank account count + nicknames (**last-four only**) · credit card count · monthly transaction volume · 1099 count · Dext subscribed? · payroll flag (are we running it) · entity manifest (one row per entity). Transaction volume and 1099 count are the two usually missing — mark them `TBD — ask on call`, don't drop them.

> **Never full account or routing numbers.** Nicknames and last-four only, anywhere in the packet. Both are permanent Drive artifacts.

**Section 01 — Discovery** (Firm Admin fills, from the sales call): HOW THEY HEARD ABOUT US · ENTITY TYPE · # PARTNERS / TEAM · TAX RETURNS CURRENT? · ACCOUNTING SOFTWARE · PAYROLL COMPANY · CURRENT CPA · SERVICES REQUESTED · PAIN POINTS & PRIORITIES DURING ONBOARDING (bank/coding narrative + numbered priorities).

**Section 02 — Pre-Kickoff Readiness** — a current-state note next to each item so the Lead knows where things stand:
- ACCOUNTING · QBO: (1) QBO file exists? (2) do we have access? (3) COA reviewed — needs cleanup? (4) client OK cleaning up the COA? (5) bank & card feeds connected? (6) how caught up is the file?
- TAX: (7) prior-year returns — which years? (8) EIN on file. (9) tax returns current?
- PAYROLL: (10) are we running payroll? (11) if not, how do we gain access?
- SALES TAX & PORTAL: (12) sales tax handled? (13) current services confirmed. (14) portal access — who is authorized? (2FA). (15) next steps assigned.

Credentials are pointers, never values — record *that* access exists and *where it lives*, never the login.

**Section 03 — Kickoff Call** (Lead fills live during the call — skill provides reference notes, not answers): 11 items — 01 Welcome · 02 Client intro · 03 Meet your Team of 3 · 04 Timeline & clean-up · 05 Communication · 06 Gather information · 07 Monthly workflow · 08 Two questions · 09 Tools & training · 10 Questions · 11 90-day call. Pre-load only item **06 Gather information** with the client-specific reminders (EIN / 990 preparer / credit card statements / payroll JE attachments we're actively chasing). Leave the other ten blank.

**Reference files** — bulleted list of paths to engagement, quote, Service Fee Template, PNCR(s), Welcome Packet, and Welcome Email draft.

### Fill-in format

Deliver as a markdown file at `G:\Shared drives\{Client Legal Name}\Perm File\Onboarding Dossier - {Client Legal Name} - fill-in.md` with, in order:

1. **Preamble** — one short paragraph: this is {Client}'s kickoff prep packet, the single file `/kickoff-prep` reads; it lives in the Perm File; every field is filled or `TBD — ask on call`; the Section 03 kickoff items stay blank until the Lead runs the call. No dashboard, no paste instructions, no URL.
2. **Header** — two-column table: Field → Value (Client name, Lead, Kickoff, Deadline, Team of 3 — Lead / Staff / Controller).
3. **Billing** — the four billing fields above.
4. **Team and budgeted hours** — bulleted, Lead / Staff / Controller + hours + the tier-default flag if applicable.
5. **Cleanup scope** — the punch list gathered in one place.
6. **Volumes and complexity** — the volume/complexity fields gathered in one place.
7. **Section 01 — Discovery** — one subheading per field, value below in prose.
8. **Section 02 — Pre-Kickoff Readiness** — grouped by category, current-state note per item.
9. **Section 03 — Kickoff Call** — pre-load only item 06; the other ten are "Lead fills live during the call."
10. **Reference files** — paths to the source docs.

---

## Service Fee Template (the "hours sheet")

The Service Fee Template already exists in the client's folder before Phase 4 runs — Jennifer creates it during quoting, before the engagement is sent. Phase 4 is read-only: pull budgeted hours from it, don't overwrite anything.

- **Expected path:** `Active Clients\{Client Legal Name}\2 - Service Fee Template - {Client Legal Name}.xlsx` (or a similarly-named file in the same folder — the filename `2 - Service Fee Template - {name}` is the convention, but check the folder if it's missing).
- If no Service Fee Template is found in the client's folder, stop and ask Jennifer — do not fall back to tier defaults without confirming.

**Reading budgeted hours:** prefer the client's own budgeted hours calculated from the inputs in their Service Fee Template. Read from the client's file, `Monthly Accounting Services` tab, "Monthly Time for Budgets for Team" summary block:

- **Full Service package block** (rows 59–64): `B60` Staff, `B61` Lead, `B62` Controller, `B64` Monthly Budget total.
- **Basic package block** (rows 67–72): `B68` Staff, `B69` Lead, `B70` Controller (Basic formula = `B31 / 3`), `B72` Monthly Budget total.
- **Premium package block** — TBD (build when the first Premium client runs through).

Use the package block that matches the client's engagement tier. If that block is unpopulated (row labels present but value cells blank), fall back to the tier defaults in SKILL.md's "Budgeted hours source" section **and flag in the packet that they're tier defaults** — that's the endorsed behavior, and it matches the `/kickoff-prep` contract's block B. (`Staff` / `Lead` / `Controller` are the FC/tier role names; the sheet's own headers still read `Staff Accountant` / `Lead Accountant` / `CPA/Controller`.)

**openpyxl gotcha:** the aggregate cells (`B60`, `B68`, etc.) are formulas. If the .xlsx was saved without Excel recalculating them, `data_only=True` returns `None`. Distinguish "formula never recalculated" (unreadable — fall back to the engagement / tier defaults, don't read as zero) from "row present, value blank" (nobody filled it in — tier defaults, say so). Compute manually from the inputs when needed:
- Staff hours = `B17 + B18 + C22 + C23 + C24 + B29` (where `C22 = B22 × 2/60`, `C23 = B23 / 50`, `C24 = B24 × 2/60`)
- Lead hours = `B25 + B30`
- Controller hours = `B31` (Full Service) or `B31 / 3` (Basic)

---

## Team handoff email

Replaces Jennifer's previous "Good morning, friends!" template with the same information re-clustered.

- **Suggested TO:** Lisa + the 3 assigned team members (Controller, Lead, Staff).
- **Suggested optional CC:** rest of the staff group for firm-wide visibility.
- **Subject:** `New client: {Client Legal Name} — kickoff & key details`
- **Body sections (in order):**
  1. One-paragraph opener: signed + paid + scope-entity nuance + key stakeholders.
  2. **Who's involved** — primary contact + helpers + external tax accountant.
  3. **Billing** — onboarding paid, cleanup deposit/balance amounts, monthly draft amount and start date.
  4. **Scope** — tier, what's in/out, cleanup window, first monthly month, software-transition notes.
  5. **Your team and budgeted hours** — Controller / Lead / Staff with hours read from the client's Service Fee Template (tier defaults + flag if the block wasn't populated); flag that Staff stays TBD client-facing.
  6. **Action items** — Lead schedules kick-off; point the Lead at the **client's Perm File**, where the kickoff prep packet (`Onboarding Dossier - {Client Legal Name} - fill-in.md`) lives for `/kickoff-prep` to read; where the Service Fee sheet lives; what to confirm on the call. (The FC project's "Sales Onboarding Service" resource also links to the client's Shared Drive now — repointed in Phase 2F.)
  7. **Things to know going in** — pain points, complex transactions, system quirks, access gaps, FC checklist status, tax-return status.
  8. One-line close: "Let me know if anything is unclear — happy to chase down any of the TBDs."

**Always verify before sending:**
- Numbers match the engagement letter (not the quote).
- Staff Accountant assignment shown internally but kept TBD client-facing (consistent with welcome email + packet).
- Any entity-name nuance is flagged.

---

## Discrepancies to actively check on every run

1. **Engagement vs. quote billing.** Engagement letter often consolidates/restructures the quote's line items. **Always pull billing numbers from the engagement.** The Phase 1 handoff (built pre-signing) may show stale quote-shaped numbers.
2. **Engagement is the source of truth on entity identity.** Consultation summary may describe multiple entities — whichever is named on the signed engagement IS the client. Don't flag mismatches; ask Jennifer if something looks genuinely contradictory.
3. **Cleanup billing shape.** If the engagement bundles cleanup with another fee or uses a flat fee, drop the "50% of the lower range" phrasing and record the actual deposit/balance the engagement states. Don't coerce deposit+balance into floor/ceiling or vice-versa.
4. **PNCR gdocs may be unreadable.** If the PNCR is Google-native (`.gdoc`), the skill can't parse it from disk — ask Jennifer to paste content rather than leaving Discovery TBD.

---

## Production runs

- **2026-06-26** — first Phase 4 run (xlsx-workbook flow, pre-dossier).
- **2026-06-30** — Mu Alpha Theta — xlsx-workbook flow. Dossier fill-in produced retroactively on 2026-07-06; xlsx workbook + duplicate team-handoff-email removed from Perm File.
- **2026-07-01** — xlsx-workbook flow.
- **2026-07-06** — Dossier fill-in flow adopted as the standard (paste-into-dashboard).
- **2026-08-12** — Dashboard retired. Packet becomes a reading file for the lead's `/kickoff-prep` skill; billing / cleanup-scope / volumes blocks added; role labels simplified to Staff / Lead / Controller.

---

## Still to build out

1. **Premium package hour formulas** — the Service Fee Template's Premium block (rows ~59–64 with Premium-tier inputs from rows 42–50) hasn't been mapped yet. Capture the exact cell references when the first Premium client runs through.

---

## Safety notes (Phase 4 specific)

- **The packet is a reading file, not a paste-source.** Deliver the markdown; the Lead / `/kickoff-prep` reads it from the Perm File. No dashboard to edit anymore.
- **When parsing PDFs/DOCX/gdocs, surface uncertainty** rather than guessing — `TBD — ask on call` is fine; fabricated values are not.
- **Re-read the engagement letter on every Phase 4 run** — don't trust the Phase 1 handoff for final billing numbers.
- **Service Fee Template is read-only in Phase 4.** It's created during quoting; Phase 4 never stamps, copies, or edits it. If it's missing, stop and ask Jennifer.
- **The packet belongs in the client's `Perm File\`**, under the exact contract filename — `/kickoff-prep` needs to find it inside the client's Drive. Team handoff email drafts stay in `~/.claude/skills/onboard-client-admin/handoffs/` since they're internal to Jennifer's workflow.
- **Never full account or routing numbers; credentials are pointers, never values.**
