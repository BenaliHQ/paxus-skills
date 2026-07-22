---
title: Phase 4 design notes (Onboarding Dossier + Team handoff email)
status: HTML-dossier flow live as of 2026-07-06 (supersedes the xlsx cell-map flow used 6/26–7/01)
last_updated: 2026-07-07
---

# /onboard-client-admin — Phase 4 design notes

Phase 4 = populate the per-client **Client Onboarding Dossier** (Claude Design HTML template) from what we already know (engagement / consultation / memo), and draft the team handoff email. Sends Lead and Controller into the kick-off call with everything Jennifer's already learned.

The Service Fee Template already exists in the client's folder before Phase 4 runs — it's created before the quote is prepared. Phase 4 only *reads* budgeted hours from it; it does not stamp a starter copy.

**Trigger:** Phase 3 (welcome packet + welcome email) is complete and the welcome email has gone out.

---

## Deliverables (two files)

1. **Populated Dossier fill-in block** (markdown) — Jennifer pastes each section into the shared Claude Design dossier.
   Save to `G:\Shared drives\{Client Legal Name}\Perm File\Onboarding Dossier - {Client Legal Name} - fill-in.md`.
   (The fill-in lives with the client, not in the skill's handoffs folder, so Lead can find it inside the client's own Drive.)
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

## Client Onboarding Dossier (the HTML template)

- **Live template URL:** https://claude.ai/design/p/5e8d4de8-c45b-4e17-9d3c-df01ff490fcf?file=Sales+Onboarding+Service.dc.html&via=share
- **FC resource pointer:** The New Client Onboarding project template's "Sales Onboarding Service" resource points at this URL — same URL for every client.
- **File title inside Claude Design:** `Sales Onboarding Service.dc.html` (renders as "Client Onboarding Dossier").
- **Per-client persistence:** the doc auto-saves per client. Jennifer picks the client via the switcher at the top, then types into the fields.
- **Skill's job:** produce a markdown fill-in that Jennifer pastes/types into the template. The skill does NOT edit the HTML directly.

### Structure and fields

**Sidebar (client identity + team)**
- Client name (title)
- LEAD — name of the Lead accountant
- KICKOFF — date or `TBD`
- DEADLINE — target onboarding-complete date (typically month-end of first monthly close, e.g., `08/31/2026`)
- TEAM OF 3 — LEAD / ACCOUNTANT / REVIEWER (first names)
- KICKOFF READINESS — % (auto-fills as Lead ticks items in Section 02)

**Section 01 — Discovery** (Firm Admin fills, from the sales call)
- HOW THEY HEARD ABOUT US
- ENTITY TYPE
- # PARTNERS / TEAM
- TAX RETURNS CURRENT?
- ACCOUNTING SOFTWARE
- PAYROLL COMPANY
- CURRENT CPA
- SERVICES REQUESTED
- PAIN POINTS & PRIORITIES DURING ONBOARDING — long-form textarea: bank/coding narrative + numbered priorities.

**Section 02 — Pre-Kickoff Readiness** (Lead ticks as access is confirmed)
- ACCOUNTING · QBO: (1) Do they have a QBO file? (2) Do we have access? (3) COA reviewed — needs cleanup? (4) Client OK cleaning up the COA? (5) Bank & card feeds connected? (6) How caught up is the file?
- TAX: (7) Prior-year returns — which years? (8) EIN on file. (9) Tax returns current?
- PAYROLL: (10) Are we running payroll? (11) If not, how do we gain access?
- SALES TAX & PORTAL: (12) Sales tax handled? (13) Current services confirmed. (14) Portal access — who is authorized? (2FA). (15) Next steps assigned.

Skill pre-populates the **known state as short notes next to each item** (e.g., "No — existing QuickBooks file, but no access yet"). Lead confirms and ticks during pre-kickoff prep.

**Section 03 — Kickoff Call** (Lead fills live during the call — skill provides reference notes, not answers)
11 items: 01 Welcome · 02 Client intro · 03 Meet your Team of 3 · 04 Timeline & clean-up · 05 Communication · 06 Gather information · 07 Monthly workflow · 08 Two questions · 09 Tools & training · 10 Questions · 11 90-day call.

Skill drops the client-specific reminders next to each agenda item (e.g., item 06 "Gather information" — list the EIN / 990 preparer / credit card statements / payroll JE attachments we're actively chasing).

### Fill-in format

Deliver as a markdown file at `G:\Shared drives\{Client Legal Name}\Perm File\Onboarding Dossier - {Client Legal Name} - fill-in.md` with these sections in order:

1. **Instructions preamble** — one-paragraph "open the Paxus Onboarding Dossier at [URL], switch to {Client} in the client switcher, paste each section below." Note that Section 03 checkboxes stay unchecked until Lead runs the kickoff.
2. **Sidebar / header table** — two-column: Dashboard field → Fill-in value. Fields: Client name, Lead, Kickoff, Deadline, Team of 3 — Lead / Accountant / Reviewer.
3. **Budgeted hours** — bulleted list of the client's actual budgeted hours from their Service Fee Template (Accountant / Lead / Reviewer + total). **Never use tier defaults — every client has their own values.** Note that Lead refines after kickoff.
4. **Section 01 — Discovery** — one subheading per field (bolded), value below in prose.
5. **Section 02 — Pre-Kickoff Readiness** — group by category (ACCOUNTING · QBO / TAX / PAYROLL / SALES TAX & PORTAL). For each item: current state note plus explicit "tick" or "leave unchecked" guidance for Lead.
6. **Section 03 — Kickoff Call** — pre-load only item 06 "Gather information" with client-specific bullets. Explicitly state "Do NOT pre-check any of the checkboxes." Items 01/02/03/04/05/07/08/09/10/11 = "Lead fills live during the call."
7. **Reference files** — bulleted list of paths to engagement, quote, Service Fee Template, PNCR(s), Welcome Packet, and Welcome Email (draft).

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
  6. **Action items** — Lead schedules kick-off, where the dossier and Service Fee sheet live, what to confirm on the call.
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
- **2026-07-06** — Dossier flow adopted as the standard.

---

## Still to build out

1. **Premium package hour formulas** — the Service Fee Template's Premium block (rows ~59–64 with Premium-tier inputs from rows 42–50) hasn't been mapped yet. Capture the exact cell references when the first Premium client runs through.

---

## Safety notes (Phase 4 specific)

- **Never edit the shared Claude Design template directly.** Deliver a fill-in for Jennifer to paste — she owns the per-client save inside Design.
- **When parsing PDFs/DOCX/gdocs, surface uncertainty** rather than guessing — TBD is fine; fabricated values are not.
- **Re-read the engagement letter on every Phase 4 run** — don't trust the Phase 1 handoff for final billing numbers.
- **Service Fee Template is read-only in Phase 4.** It's created during quoting; Phase 4 never stamps, copies, or edits it. If it's missing, stop and ask Jennifer.
- **Dossier fill-in belongs in the client's `Perm File\`**, not in the skill's handoffs folder — Lead needs to find it inside the client's Drive. Team handoff email drafts stay in `~/.claude/skills/onboard-client-admin/handoffs/` since they're internal to Jennifer's workflow.
