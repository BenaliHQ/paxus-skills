---
title: Phase 4 design notes (Onboarding Prep Notes + Team handoff email)
status: Prep-notes flow live as of 2026-08-13 (the Onboarding Dossier / Claude Design dashboard is retired; the lead's prep notes are now the record, kept in the client's Perm File)
last_updated: 2026-08-13
---

# /onboard-client-admin — Phase 4 design notes

Phase 4 = produce the **Onboarding Prep Notes** for a client from what we already know (engagement / consultation / memo), and draft the team handoff email. Sends the Lead into the kick-off call with everything Jennifer's already learned.

The Onboarding Dossier dashboard (the old Claude Design HTML at claude.ai) is **retired.** The prep notes replace it: they're a clean, readable markdown file that lives in the client's Perm File with every other permanent artifact, and the lead's skill reads it from there. No dashboard, no pasting.

The Service Fee Template already exists in the client's folder before Phase 4 runs — it's created before the quote is prepared. Phase 4 is read-only toward it (never stamps a starter copy). Note the direction is shifting (2026-08-13): budgeted hours will probably come from the client's discovery notes, not the Service Fee Template — see the Budgeted hours section.

**Trigger:** Phase 3 (welcome packet + welcome email) is complete and the welcome email has gone out.

---

## Deliverables (two files)

1. **Onboarding Prep Notes** (markdown) — the lead's kickoff reference, organized for reading top to bottom.
   Save to `G:\Shared drives\{Client Legal Name}\Perm File\Onboarding Prep Notes - {Client Legal Name}.md`.
   (Lives with the client, not in the skill's handoffs folder, so the Lead can find it inside the client's own Drive.)
2. **Team handoff email** — drafted directly in Gmail (Phase 4C), with a markdown copy archived at
   `G:\Shared drives\{Client Legal Name}\Perm File\Team Handoff Email - {Client Legal Name}.md`.

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

## Onboarding Prep Notes (the handoff file)

- **Where it lives:** `G:\Shared drives\{Client Legal Name}\Perm File\Onboarding Prep Notes - {Client Legal Name}.md`.
- **Who reads it:** the Lead (and the lead's skill), pulling it straight from the client's Perm File.
- **Golden rule:** every field is either filled in or explicitly marked `TBD — ask on call`. A silent blank is ambiguous — there's no way to tell a genuine unknown from a not-yet-filled field. `TBD — ask on call` turns an unknown into a question on the call sheet, which is where an unknown belongs.
- **Role terms:** Staff / Lead / Controller (our own terms). The old Lead / Accountant / Reviewer labels only existed for the retired dashboard — don't use them.

### Structure (in reading order)

1. **Header** — one line, then a small table: client name, package/tier, Kickoff (actual call date or `TBD` — NOT the cleanup start date), onboarding deadline (from the quote timeline, e.g. `08/31/2026`), Team of 3 (Lead / Staff / Controller, first names).
2. **Billing** — monthly fee, first monthly draft date, onboarding fee, cleanup deposit, cleanup balance. **Pull from the engagement, not the quote** — the engagement often consolidates line items. The lead covers billing while setting expectations on the call, so these figures must be in the file.
3. **Budgeted hours** — Staff / Lead / Controller + total, if available (discovery notes first, Service Fee Template only if it carries them — see the Budgeted hours section below). If no hours are available, mark `TBD — ask on call`. Never invent tier defaults; never say the Lead refines them.
4. **Cleanup scope** — in one place: what the cleanup covers (period/months, catch-up recs, COA cleanup, prior-year work), floor/ceiling or flat fee, any client-specific scope.
5. **Volumes & complexity** — in one place: # bank & credit-card accounts, monthly transaction volume, 1099 count, Dext (yes/no), payroll (yes+vendor / no — out of scope), entities in scope. Transaction volume and 1099 count are the two usually missing from the Service Fee Template — mark them `TBD — ask on call` when not found.
6. **Discovery** — one field per line: how they heard about us, entity type, # partners/team, tax returns current?, accounting software, payroll company, current CPA, services requested, pain points & priorities.
7. **Pre-Kickoff Readiness** — grouped ACCOUNTING · QBO / TAX / PAYROLL / SALES TAX & PORTAL, with the current-state note next to each item so the Lead knows where things stand going in. (See the 15-item checklist below.)
8. **Kickoff Call reference notes** — the 11-item agenda; pre-load only item 06 "Gather information" with client-specific bullets. The Lead works through the rest live.
9. **Reference files** — paths to engagement, quote, Service Fee Template, PNCR(s), welcome packet, and welcome email draft.

### Pre-Kickoff Readiness — the 15 items

- ACCOUNTING · QBO: (1) Do they have a QBO file? (2) Do we have access? (3) COA reviewed — needs cleanup? (4) Client OK cleaning up the COA? (5) Bank & card feeds connected? (6) How caught up is the file?
- TAX: (7) Prior-year returns — which years? (8) EIN on file. (9) Tax returns current?
- PAYROLL: (10) Are we running payroll? (11) If not, how do we gain access?
- SALES TAX & PORTAL: (12) Sales tax handled? (13) Current services confirmed. (14) Portal access — who is authorized? (2FA). (15) Next steps assigned (Lead completes post-kickoff).

### Kickoff Call — the 11 agenda items

01 Welcome · 02 Client intro · 03 Meet your Team of 3 · 04 Timeline & clean-up · 05 Communication · 06 Gather information · 07 Monthly workflow · 08 Two questions · 09 Tools & training · 10 Questions · 11 90-day call.

Pre-load only item 06 "Gather information" with the client-specific list of what we're actively chasing (EIN, 990 preparer, credit-card statements, payroll JE attachments, credentials, loans/assets, portal authorization, 2FA setup, etc.). The other 10 are the Lead's live agenda — no pre-fill.

---

## Budgeted hours (in flux — discovery notes first)

**Direction as of 2026-08-13:** budgeted hours will probably live in the client's **discovery notes**, not necessarily on the Service Fee Template. Look for them in this order:

1. **Discovery notes** for the prospective client — if they list Staff / Lead / Controller hours, use those.
2. **Service Fee Template**, only if it happens to carry them (read-only — see cell map below).
3. **If no hours are available anywhere:** there are no hours to list. Do NOT invent tier defaults. Prep notes → mark budgeted hours `TBD — ask on call`; team handoff email → leave the budgeted-hours sentence out entirely.

**The Lead does not determine or refine budgeted hours** — never attribute the hours (or their refinement) to the Lead.

### Service Fee Template cell map (when it carries the hours)

The Service Fee Template is created during quoting and is read-only in Phase 4 — never stamp, copy, or edit it. Path: `Active Clients\{Client Legal Name}\2 - Service Fee Template - {Client Legal Name}.xlsx` (convention; the SKILL also checks for `{Legal name} Service Fee.xlsx`). Read from the `Monthly Accounting Services` tab, "Monthly Time for Budgets for Team" summary block:

- **Full Service package block** (rows 59–64): `B60` Staff Accountant, `B61` Lead Accountant, `B62` CPA/Controller, `B64` Monthly Budget total.
- **Basic package block** (rows 67–72): `B68` Staff Accountant, `B69` Lead Accountant, `B70` CPA/Controller (Basic formula = `B31 / 3`), `B72` Monthly Budget total.
- **Premium package block** — TBD (build when the first Premium client runs through).

**openpyxl gotcha:** the aggregate cells (`B60`, `B68`, etc.) are formulas. If the .xlsx was saved without Excel recalculating them, `data_only=True` returns `None`. Compute manually from the inputs:
- Staff hours = `B17 + B18 + C22 + C23 + C24 + B29` (where `C22 = B22 × 2/60`, `C23 = B23 / 50`, `C24 = B24 × 2/60`)
- Lead hours = `B25 + B30`
- Controller hours = `B31` (Full Service) or `B31 / 3` (Basic)

Use the package block that matches the client's engagement tier. (This mechanic only applies when the Service Fee Template actually carries the hours — per the direction above, discovery notes are the preferred source.)

---

## Team handoff email

Replaces Jennifer's previous "Good morning, friends!" template with the same information re-clustered. Drafted directly in Gmail (Phase 4C), plain text only.

- **Suggested TO:** Lisa + the 3 assigned team members (Controller, Lead, Staff).
- **Suggested optional CC:** rest of the staff group for firm-wide visibility.
- **Subject:** `New client: {Client Legal Name} — kickoff & key details`
- **Body sections (in order):**
  1. One-paragraph opener: signed + paid + scope-entity nuance + key stakeholders.
  2. **Who's involved** — primary contact + helpers + external tax accountant.
  3. **Billing** — onboarding paid, cleanup deposit/balance amounts, monthly draft amount and start date (from the engagement).
  4. **Scope** — tier, what's in/out, cleanup window, first monthly month, software-transition notes.
  5. **Your team and budgeted hours** — Controller / Lead / Staff. List budgeted hours only if available (discovery notes first, Service Fee Template if it carries them); **if there are no hours to list, leave the budgeted-hours sentence out entirely** — no TBD, no tier defaults. Never say the Lead determines or refines them. Flag that Staff stays TBD client-facing (unless Staff is an intern — then name them).
  6. **Action items** — Lead schedules kick-off; point the Lead at the **Onboarding Prep Notes** in the client's Perm File (`Onboarding Prep Notes - {Client Legal Name}.md`) as the record to work from; what to confirm on the call. Do NOT reference the retired Sales Onboarding dashboard, a raw claude.ai/design URL, or any "Sales Onboarding .xlsx" worksheet.
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
- **2026-06-30** — xlsx-workbook flow. Dossier fill-in produced retroactively on 2026-07-06.
- **2026-07-01** — xlsx-workbook flow.
- **2026-07-06** — Dossier (Claude Design) flow adopted as the standard.
- **2026-08-13** — Dossier dashboard retired; prep-notes flow adopted. Phase 6 (dossier PDF archive) removed. Billing / cleanup-scope / volumes-&-complexity blocks added to the prep notes.

---

## Still to build out

1. **Premium package hour formulas** — the Service Fee Template's Premium block (rows ~59–64 with Premium-tier inputs from rows 42–50) hasn't been mapped yet. Capture the exact cell references when the first Premium client runs through.

---

## Safety notes (Phase 4 specific)

- **When parsing PDFs/DOCX/gdocs, surface uncertainty** rather than guessing — `TBD — ask on call` is fine; fabricated values are not.
- **Re-read the engagement letter on every Phase 4 run** — don't trust the Phase 1 handoff for final billing numbers.
- **Service Fee Template is read-only in Phase 4.** It's created during quoting; Phase 4 never stamps, copies, or edits it. It is no longer required — if it's missing or doesn't carry budgeted hours, fall back to the discovery notes; if hours aren't anywhere, mark them `TBD — ask on call` (don't stop the run).
- **Prep notes belong in the client's `Perm File\`**, not in the skill's handoffs folder — the Lead (and the lead's skill) need to find it inside the client's Drive. Team handoff email drafts are archived in Perm File too; the Gmail draft is the primary deliverable for the email.
