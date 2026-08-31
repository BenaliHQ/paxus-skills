---
title: Phase 4 design notes (Client Prep Notes + Team handoff email)
status: Client Prep Notes flow live as of 2026-08-31 (supersedes the Onboarding Dossier / claude.ai dashboard flow used 2026-07-06 to 2026-08-31, and the xlsx cell-map flow used 6/26–7/01 before that)
last_updated: 2026-08-31
---

# /onboard-client-admin — Phase 4 design notes

Phase 4 = write a **Client Prep Notes** file from what we already know (engagement / consultation / memo) and draft the team handoff email. Sends the Lead and Controller into the kick-off call with everything already learned, organized as a clean reading document rather than a form to paste into.

The Service Fee Template already exists in the client's folder before Phase 4 runs — it's created before the quote is prepared. Phase 4 only *reads* budgeted hours from it; it does not stamp a starter copy.

**Trigger:** Phase 3 (welcome packet + welcome email) is complete and the welcome email has gone out.

---

## Deliverables (two files, both in the client's Perm File)

1. **Client Prep Notes** (markdown) — the Lead reads this directly. No pasting, no external dashboard.
   Save to `G:\Shared drives\{Client Legal Name}\Perm File\Client Prep Notes - {Client Legal Name}.md`.
2. **Team handoff email** — drafted as markdown; Jennifer pastes into Gmail.
   Save to `G:\Shared drives\{Client Legal Name}\Perm File\Team Handoff Email - {Client Legal Name}.md`

(Both live with the client in Perm File, not in the skill's handoffs folder — the Lead and Controller need to find them inside the client's own Drive.)

---

## Inputs (already in place from prior phases)

| Source | Path | Reason |
|---|---|---|
| Phase 1 handoff | `~/.claude/skills/onboard-client-admin/handoffs/{slug}-{date}.md` | FC client ID, primary contact, package, monthly fee, cleanup figures |
| Engagement PDF | `Active Clients\{Client Legal Name}\Engagement - {Client Legal Name}.pdf` | Authoritative billing line items, signatory, signing date |
| Quote PDF | `Active Clients\{Client Legal Name}\*Quote*.pdf` | Package selected, recommended tier, services not in scope |
| Hours/Service Fee doc | `Active Clients\{Client Legal Name}\*Service Fee*.xlsx` or `*Hours Budget*.md` | Budgeted hours + volumes: bank/CC count, transaction volume, 1099 count, Dext, payroll flag. Format varies by client — some are the xlsx workbook, some are a plain markdown writeup. |
| Consultation / PNCR | `Active Clients\{Client Legal Name}\*Potential New Client Review*.gdoc` (Google-native) or `*Consultation*.pdf` | Pain points, current setup, stakeholders, scope nuance |
| Discovery call notes | `Active Clients\{Client Legal Name}\*Discovery Call Notes*.md`, if present | Same purpose as PNCR — some clients have a standalone transcript summary instead of a PNCR |
| Memo to File | `Active Clients\{Client Legal Name}\*Memo to File*.docx` | Internal notes — entity context, ownership, decisions |

If the engagement is in `Perm File\` as well as Active Clients, prefer the Perm File copy.

**PNCR gotcha:** Potential New Client Review docs are often Google-native `.gdoc` pointers that can't be read from disk. If the skill can't parse them, ask Jennifer to paste the content into chat rather than leaving Discovery fields TBD.

---

## Client Prep Notes (the file itself)

**No live template, no dashboard.** This replaces the Claude Design "Onboarding Dossier" that lived at claude.ai/design — that dashboard is retired (2026-08-31). There is nothing to paste into and no shared URL to reference anywhere in the output.

**Role labels:** use Paxus's own terms everywhere — **Staff / Lead / Controller**. The old dashboard forced a Lead/Accountant/Reviewer mapping; that mapping no longer exists or matters.

### Structure and blocks

**Header** — client name, package tier, Lead/Staff/Controller names, Kickoff (`TBD` until scheduled — never the cleanup start date), onboarding-begins date.

**Discovery** (prose/bullets, one item per line):
- How they heard about us
- Entity type
- Partners/team
- Tax returns current?
- Accounting software + status
- Payroll company
- Current CPA/tax preparer
- Services requested
- Pain points & priorities

**Billing** (NEW block, from the signed engagement — not the quote):
- Onboarding fee + billing timing
- Monthly fee + first draft date
- Cleanup deposit + billing date/timing + balance or range
- Any other one-time/add-on fees + billing timing

**Cleanup scope** (NEW as its own block — previously scattered into Discovery/Pre-Kickoff):
- What's being rebuilt (bulleted, from engagement/quote)
- Floor/ceiling hours or dollar range if budgeted
- Any known role-split or sequencing detail worth flagging for scheduling

**Volumes & complexity** (NEW as its own block — previously scattered):
- Account count, transaction volume, 1099 count, Dext status, payroll flag, related entities

**Pre-Kickoff Readiness** (grouped by category, current-state notes, `TBD — ask on call` for unknowns):
- ACCOUNTING · QBO / TAX / PAYROLL / SALES TAX & PORTAL — same item list as before, just without dashboard checkbox framing.

**Kickoff Call reference notes:**
Pre-load only a "Gather information" bulleted list of what to ask on the call. Don't try to pre-fill the rest of a call agenda — that's the Lead's job live.

**Budgeted hours** — from the Service Fee Template (never tier defaults unless the template is genuinely missing, and flag clearly when defaults are used). Note who refines hours after kickoff.

**Golden rule carried over from the dashboard era:** every field is either filled in or explicitly marked `TBD — ask on call` (or `N/A` if it plainly doesn't apply). A silently blank field is ambiguous — a marked one becomes a question on the call sheet.

---

## Service Fee Template (the "hours sheet")

The Service Fee Template already exists in the client's folder before Phase 4 runs — Jennifer creates it during quoting, before the engagement is sent. Phase 4 is read-only: pull budgeted hours from it, don't overwrite anything.

- **Expected path:** `Active Clients\{Client Legal Name}\2 - Service Fee Template - {Client Legal Name}.xlsx` (or a similarly-named file in the same folder — the filename `2 - Service Fee Template - {name}` is the convention, but check the folder if it's missing). **Some clients instead have a plain markdown "Hours Budget" writeup in the same folder** — read whichever format is actually present; don't assume xlsx.
- If no hours source is found in the client's folder at all, stop and ask Jennifer — do not fall back to tier defaults without confirming.

**Reading budgeted hours from the xlsx (there are no tier defaults when this exists):** every client has their own budgeted hours calculated from the inputs in their Service Fee Template. Read from the client's file, `Monthly Accounting Services` tab, "Monthly Time for Budgets for Team" summary block:

- **Full Service package block** (rows 59–64): `B60` Staff, `B61` Lead, `B62` Controller, `B64` Monthly Budget total.
- **Basic package block** (rows 67–72): `B68` Staff, `B69` Lead, `B70` Controller (Basic formula = `B31 / 3`), `B72` Monthly Budget total.
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
  6. **Action items** — Lead schedules kick-off; **point at the client's Perm File** (name the Client Prep Notes file directly — no dashboard URL anymore); where the Service Fee sheet lives; what to confirm on the call.
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
3. **"50% of the lower range" wording.** If the engagement bundles cleanup with another fee, uses a flat fee, or splits the range into two flat deposit/balance halves instead of stating a range, drop the range phrasing and give the actual deposit amount as billed.
4. **PNCR gdocs may be unreadable.** If the PNCR is Google-native (`.gdoc`), the skill can't parse it from disk — ask Jennifer to paste content rather than leaving Discovery TBD.
5. **Hours source format varies.** Don't assume the xlsx workbook — check the folder for whatever hours-budget document actually exists.

---

## Production runs

- **2026-06-26** — first Phase 4 run (xlsx-workbook flow, pre-dossier).
- **2026-06-30** — xlsx-workbook flow. Dossier fill-in produced retroactively on 2026-07-06.
- **2026-07-01** — xlsx-workbook flow.
- **2026-07-06** — Dossier flow (claude.ai dashboard) adopted as the standard.
- **2026-08-31** — Dossier retired. Client Prep Notes (this flow) adopted as the standard; Billing and Volumes & Complexity added as explicit blocks; role labels simplified to Staff/Lead/Controller everywhere.

---

## Still to build out

1. **Premium package hour formulas** — the Service Fee Template's Premium block (rows ~59–64 with Premium-tier inputs from rows 42–50) hasn't been mapped yet. Capture the exact cell references when the first Premium client runs through.

---

## Safety notes (Phase 4 specific)

- **When parsing PDFs/DOCX/gdocs/markdown, surface uncertainty** rather than guessing — TBD is fine; fabricated values are not.
- **Re-read the engagement letter on every Phase 4 run** — don't trust the Phase 1 handoff for final billing numbers.
- **Service Fee Template (or equivalent hours doc) is read-only in Phase 4.** It's created during quoting; Phase 4 never stamps, copies, or edits it. If it's missing entirely, stop and ask Jennifer.
- **Client Prep Notes and the team handoff email both belong in the client's `Perm File\`**, not in the skill's handoffs folder — the Lead and Controller need to find them inside the client's Drive.
