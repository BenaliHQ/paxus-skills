---
title: Phase 4 design notes (Onboarding Dossier prep notes + Team handoff email)
status: Read-oriented prep-notes flow live as of 2026-08-05 (the claude.ai Onboarding Dossier dashboard was retired; the prep-notes file in Perm File is now the record). Supersedes the HTML-dossier paste flow (7/06–8/05) and the xlsx cell-map flow (6/26–7/01).
last_updated: 2026-08-05
---

# /onboard-client-admin — Phase 4 design notes

Phase 4 = produce the per-client **Onboarding Dossier prep-notes file** in the client's Perm File from what we already know (engagement / consultation / memo), and draft the team handoff email. Sends Lead and Controller into the kick-off call with everything Jennifer's already learned. The file is read by the Lead's kickoff-prep skill — it is not pasted into any dashboard.

The Service Fee Template already exists in the client's folder before Phase 4 runs — it's created before the quote is prepared. Phase 4 only *reads* budgeted hours from it; it does not stamp a starter copy.

**Trigger:** Phase 3 (welcome packet + welcome email) is complete and the welcome email has gone out.

---

## Deliverables (two files)

1. **Onboarding Dossier prep-notes file** (markdown) — a read-oriented handoff the Lead's kickoff-prep skill reads. Not pasted anywhere.
   Save to `G:\Shared drives\{Client Legal Name}\Perm File\Onboarding Dossier - {Client Legal Name} - fill-in.md`.
   (Keep this exact filename — the Lead's kickoff-prep skill reads this path. The file lives with the client, not in the skill's handoffs folder, so Lead can find it inside the client's own Drive.)
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

## Onboarding Dossier prep notes (structure)

- **Dashboard retired.** The claude.ai Onboarding Dossier dashboard (`Sales Onboarding Service.dc.html`) is no longer used — no template URL to paste into, no per-client dashboard entry. The prep-notes file in the client's Perm File is the record. The "Sales Onboarding Service" resource has been removed from the New Client Onboarding template (one-time; the client's Shared Drive is already surfaced by the Phase 2F "Google Drive" FC resource).
- **Skill's job:** produce a read-oriented markdown prep-notes file the Lead's kickoff-prep skill reads. Every field is filled in or marked `TBD — ask on call` — never silently blank, since a blank is ambiguous to the reading skill.

### Structure and fields (order in the file)

**Client identity + team**
- Client name
- LEAD — name of the Lead
- KICKOFF — date or `TBD — ask on call`
- DEADLINE — target onboarding-complete date (typically month-end of first monthly close, e.g., `08/31/2026`)
- TEAM OF 3 — STAFF / LEAD / CONTROLLER (first names)

**Budgeted hours** — (unchanged) Staff / Lead / Controller + total; see the Service Fee Template section below. Name who refines after kickoff (the Lead).

**Billing** (from the **engagement**, not the quote — the engagement often consolidates line items) — monthly amount, first monthly draft date, onboarding fee (note if paid), cleanup deposit, cleanup balance. Anything not in the engagement → `TBD — ask on call`.

**Cleanup scope** — one consolidated block: period being cleaned, what's in scope (recs, COA rebuild, catch-up months, prior-year adjustments), known exclusions.

**Volumes & complexity** — one consolidated block: bank/CC accounts (count + list), monthly transaction volume, 1099 count, Dext (in scope?), payroll flag + vendor, entities in scope. Transaction volume and 1099 count are usually missing → `TBD — ask on call`.

**Section 01 — Discovery**
- HOW THEY HEARD ABOUT US
- ENTITY TYPE
- # PARTNERS / TEAM
- TAX RETURNS CURRENT?
- ACCOUNTING SOFTWARE
- PAYROLL COMPANY
- CURRENT CPA
- SERVICES REQUESTED
- PAIN POINTS & PRIORITIES DURING ONBOARDING — bank/coding narrative + numbered priorities.

**Section 02 — Pre-Kickoff Readiness** (skill records the known state for each item so the Lead knows where things stand going in)
- ACCOUNTING · QBO: (1) Do they have a QBO file? (2) Do we have access? (3) COA reviewed — needs cleanup? (4) Client OK cleaning up the COA? (5) Bank & card feeds connected? (6) How caught up is the file?
- TAX: (7) Prior-year returns — which years? (8) EIN on file. (9) Tax returns current?
- PAYROLL: (10) Are we running payroll? (11) If not, how do we gain access?
- SALES TAX & PORTAL: (12) Sales tax handled? (13) Current services confirmed. (14) Portal access — who is authorized? (2FA). (15) Next steps assigned.

Skill records the **known state as a short note next to each item** (e.g., "No — existing QuickBooks file, but no access yet"), or `TBD — ask on call` where unknown.

**Section 03 — Kickoff Call reference notes** (the Lead works through these live on the call — skill provides reference notes, not answers)
11 items: 01 Welcome · 02 Client intro · 03 Meet your Team of 3 · 04 Timeline & clean-up · 05 Communication · 06 Gather information · 07 Monthly workflow · 08 Two questions · 09 Tools & training · 10 Questions · 11 90-day call.

Skill drops client-specific reminders next to item 06 "Gather information" only (the EIN / 990 preparer / credit card statements / payroll JE attachments we're actively chasing). Items 01/02/03/04/05/07/08/09/10/11 = "Lead fills live during the call."

### Prep-notes file format

Deliver as a markdown file at `G:\Shared drives\{Client Legal Name}\Perm File\Onboarding Dossier - {Client Legal Name} - fill-in.md` (keep this exact filename — the Lead's kickoff-prep skill reads it) with these sections in order:

1. **Header line** — "Onboarding prep notes for {Client} — for the Lead's kickoff-prep. Every field is filled in or marked `TBD — ask on call`." No dashboard URL, no paste instructions.
2. **Client identity + team table** — Client name, Lead, Kickoff, Deadline, Team of 3 — Staff / Lead / Controller.
3. **Budgeted hours** — (unchanged) Staff / Lead / Controller + total, from the client's Service Fee Template (or tier defaults with a note that the Service Fee template block wasn't populated). Note that the Lead refines after kickoff.
4. **Billing** — table, from the engagement.
5. **Cleanup scope** — consolidated block.
6. **Volumes & complexity** — consolidated block.
7. **Section 01 — Discovery** — one subheading per field, value below in prose.
8. **Section 02 — Pre-Kickoff Readiness** — group by category (ACCOUNTING · QBO / TAX / PAYROLL / SALES TAX & PORTAL). For each item: current known state or `TBD — ask on call`. No tick/uncheck language.
9. **Section 03 — Kickoff Call reference notes** — pre-load only item 06 with client-specific bullets. Items 01/02/03/04/05/07/08/09/10/11 = "Lead fills live during the call."
10. **Reference files** — bulleted list of paths to engagement, quote, Service Fee Template, PNCR(s), Welcome Packet, and Welcome Email (draft).

---

## Service Fee Template (the "hours sheet")

The Service Fee Template already exists in the client's folder before Phase 4 runs — Jennifer creates it during quoting, before the engagement is sent. Phase 4 is read-only: pull budgeted hours from it, don't overwrite anything.

- **Expected path:** `Active Clients\{Client Legal Name}\2 - Service Fee Template - {Client Legal Name}.xlsx` (or a similarly-named file in the same folder — the filename `2 - Service Fee Template - {name}` is the convention, but check the folder if it's missing).
- If no Service Fee Template is found in the client's folder, stop and ask Jennifer — do not fall back to tier defaults without confirming.

**Reading budgeted hours (there are no tier defaults):** every client has their own budgeted hours calculated from the inputs in their Service Fee Template. Read from the client's file, `Monthly Accounting Services` tab, "Monthly Time for Budgets for Team" summary block:

- **Full Service package block** (rows 59–64): `B60` Staff Accountant, `B61` Lead Accountant, `B62` CPA/Controller, `B64` Monthly Budget total.
- **Basic package block** (rows 67–72): `B68` Staff Accountant, `B69` Lead Accountant, `B70` CPA/Controller (Basic formula = `B31 / 3`), `B72` Monthly Budget total.
- **Premium package block** — TBD (build when the first Premium client runs through).

Use the package block that matches the client's engagement tier.

**openpyxl gotcha:** the aggregate cells (`B60`, `B68`, etc.) are formulas. If the .xlsx was saved without Excel recalculating them, `data_only=True` returns `None`. Compute manually from the inputs:
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
  5. **Your team and budgeted hours** — Controller / Lead / Staff with hours **read from the client's Service Fee Template** (never tier defaults); flag that Staff stays TBD client-facing.
  6. **Action items** — Lead schedules kick-off; point to the client's Perm File, where the prep-notes file (`Onboarding Dossier - {Client Legal Name} - fill-in.md`) and Service Fee sheet live; what to confirm on the call.
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
3. **"50% of the lower range" wording.** If the engagement bundles cleanup with another fee or uses a flat fee, drop the range phrasing and give the actual deposit amount.
4. **PNCR gdocs may be unreadable.** If the PNCR is Google-native (`.gdoc`), the skill can't parse it from disk — ask Jennifer to paste content rather than leaving Discovery TBD.

---

## Production runs

- **2026-06-26** — first Phase 4 run (xlsx-workbook flow, pre-dossier).
- **2026-06-30** — Mu Alpha Theta — xlsx-workbook flow. Dossier fill-in produced retroactively on 2026-07-06; xlsx workbook + duplicate team-handoff-email removed from Perm File.
- **2026-07-01** — xlsx-workbook flow.
- **2026-07-06** — Dossier (dashboard paste) flow adopted as the standard.
- **2026-08-05** — Dashboard retired. Phase 4 now produces a read-oriented prep-notes file in Perm File for the Lead's kickoff-prep skill; Phase 6 (dossier PDF archive) removed; role labels simplified to Staff / Lead / Controller; Billing / Cleanup scope / Volumes & complexity added as their own blocks.

---

## Still to build out

1. **Premium package hour formulas** — the Service Fee Template's Premium block (rows ~59–64 with Premium-tier inputs from rows 42–50) hasn't been mapped yet. Capture the exact cell references when the first Premium client runs through.

---

## Safety notes (Phase 4 specific)

- **No dashboard to edit.** The claude.ai Onboarding Dossier dashboard is retired — deliver the read-oriented prep-notes file into the client's Perm File; it's the record, not a paste-source.
- **When parsing PDFs/DOCX/gdocs, surface uncertainty** rather than guessing — TBD is fine; fabricated values are not.
- **Re-read the engagement letter on every Phase 4 run** — don't trust the Phase 1 handoff for final billing numbers.
- **Service Fee Template is read-only in Phase 4.** It's created during quoting; Phase 4 never stamps, copies, or edits it. If it's missing, stop and ask Jennifer.
- **Dossier fill-in belongs in the client's `Perm File\`**, not in the skill's handoffs folder — Lead needs to find it inside the client's Drive. Team handoff email drafts stay in `~/.claude/skills/onboard-client-admin/handoffs/` since they're internal to Jennifer's workflow.
