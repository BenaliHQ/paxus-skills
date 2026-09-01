---
name: onboard-client-admin
description: Admin-side client onboarding for Paxus CPA. Phase 1 ingests the prospective-client quote, creates the client + primary contact in Financial Cents via API, spins up the New Client Onboarding project (Firm Admin Tasks auto-assigned to Jennifer), and drafts proposal content. Phase 2 (post-signing) copies the standard template into a new client Shared Drive, files the signed engagement PDF, moves the client from Prospective to Active, POSTs the Shared Drive link to FC's Resources section, creates an "Engagement Letters" folder in FC's Files tab with the engagement uploaded for client-portal access, attaches the 8 standard project templates (weekly bookkeeping, month-end review, month-end close, cleanup, post cleanup, kick-off call, client training manual, tax returns) with per-role task reassignment, and attaches the FC 1099 project templates for Full Service / Premium clients (Basic clients skip 1099). Phase 3 generates a personalized welcome packet in Canva, saves the PDF to the client's Shared Drive, and drafts the warm welcome email to the client. Phase 4 produces the internal Onboarding Prep Notes handoff file (Discovery, Pre-Kickoff Readiness, billing, cleanup scope, volumes/complexity, and Kickoff-Call reference notes) in the client's Perm File for the lead, then drafts the internal team handoff email. Phase 5 drafts the day-before-kickoff email to the client with a reminder of the meeting time and the outstanding items on the FC Onboarding Checklist. Run when a new client engages Paxus, when a signed engagement needs to be filed, or the day before a client's kickoff call.
---

# /onboard-client-admin — Paxus Admin-Side Client Onboarding

You are setting up the **administrative side** of a new Paxus client. This is the firm-operations companion to `/onboard-client` (which scaffolds the AI workflow folders). Be warm and conversational — match the Paxus voice from `~/.claude/CLAUDE.md`.

This skill is **phased**:

- **Phase 1 (active):** Ingest quote, create client + contact in FC, create the New Client Onboarding project (Firm Admin Tasks queued for Jennifer), draft proposal content, generate handoff for the rest.
- **Phase 2 (active):** Once the engagement is signed in FC — copy the standard template into a new Google Shared Drive, file the signed engagement PDF in `Perm File` and Active Clients, move the prospective folder over, POST the Shared Drive link to FC's Resources section, create an "Engagement Letters" folder in FC's Files tab with the engagement uploaded for client-portal access, attach the 8 standard project templates (weekly bookkeeping, month-end review, month-end close, cleanup, post cleanup, kick-off call, client training manual, tax returns) and reassign tasks by role, and (for Full Service / Premium clients only) attach the 1099 project templates.
- **Phase 3 (active):** Generate a personalized welcome packet in Canva, save the PDF to the client's Shared Drive `Perm File\`, and draft the warm welcome email to the client **directly in Gmail** (with a markdown copy archived in Perm File).
- **Phase 4 (active):** Produce the internal **Onboarding Prep Notes** handoff file for the lead (from engagement / consultation / memo) and save it to the client's `Perm File\`. Draft the internal team handoff email **directly in Gmail**, with a markdown copy archived in Perm File.
- **Phase 5 (active):** Draft the day-before-kickoff email to the client **directly in Gmail** (with a markdown copy archived in Perm File) — reminder of the meeting time, thank-you for what's been received, list of what's still outstanding on the FC Client's Onboarding Checklist.

### Phase routing at start

If the operator hasn't told you which phase, ask: **"Phase 1 (new prospect — create the FC client and proposal), Phase 2 (engagement just signed — Shared Drive + engagement filing + FC Resources/Files + 1099s), Phase 3 (welcome packet + client welcome email), Phase 4 (Onboarding Prep Notes + team handoff email), or Phase 5 (day-before-kickoff email to the client)?"**

The natural order is 1 → 2 → 3 → 4 → 5, with a pause between 1 and 2 while the client signs and another pause between 4 and 5 while the kickoff gets scheduled.

---

## Universal rules

- **No fabrication.** Accept `TBD` and write it through. Never invent contact info, fees, dates, or stakeholder names.
- **Trust the operator's client identification.** Once Jennifer names the client (or once the engagement is signed), the engagement letter is the source of truth on the legal client. Don't flag "entity mismatches" against pre-engagement consultation notes — they're context, not contradictions.
- **Engagement letter > quote** for post-signing billing numbers. The Phase 1 handoff is built from the quote (pre-signing) and may show different line items than the final engagement. Always re-read the engagement before quoting billing amounts in Phase 3 or 4 deliverables.
- **Date format.** Normalize to `YYYY-MM-DD` in stored handoffs. Accept "today" → today's date.
- **Slug.** Lowercase, strip apostrophes/quotes/parentheses, replace non-alphanumeric with single dash, collapse dashes, trim. Used for handoff filenames only.
- **Shared Drive root is `00 - Paxus CPA`,** not `Paxus CPA`. Both Git-Bash (`/g/Shared drives/00 - Paxus CPA/...`) and Windows (`G:\Shared drives\00 - Paxus CPA\...`) paths apply.

---

## Important rules for Phase 1

- **Quote is the source of truth for scope and pricing.** Operational scheduling (signing date, monthly draft date, cleanup start date) comes from the operator.
- **Read the FC token at runtime.** Lives at `C:/Users/paxus/.paxus/client onboarding.txt`. Read it fresh each run. If missing/empty, stop: "FC API token not found at `C:/Users/paxus/.paxus/client onboarding.txt` — drop the token there and re-run."
- **One creation per run.** Exactly one FC client + one primary contact + one New Client Onboarding project. Run the skill again for additional clients.
- **Project depends on client + contact.** Phase 1E must run only after 1C (client) AND 1D (contact) both return success. If 1C fails, stop before 1D. If 1D fails, stop before 1E — the operator adds the contact and project manually in the FC UI.
- **API scope.** `POST /clients`, `POST /clients/{id}/contacts`, and `POST /templates/{template_id}/projects` are supported. Proposals/engagements/invoices have **no public API** — those stay in the FC UI.
- **Money format.** Accept dollar amounts as the operator types them (`1,500`, `$1500`, `1500.00`). Strip commas/`$`, validate as positive number, present back as `$1,500.00`. Accept `TBD` / `varies` and pass through.

---

## Phase 1A — Ingest the quote

Prospective-client folder layout:
```
G:\Shared drives\00 - Paxus CPA\Admin\Client Onboarding\Prospective Clients\{Client Name}\
```

1. List the folder. Look for files containing `quote` (case-insensitive) — typically `{Client Name} Quote.pdf` and/or `.docx`.
2. Read the PDF quote. Extract:
   - Available packages and their monthly prices
   - Onboarding fee
   - Cleanup fee structure (floor/ceiling, deposit pattern)
   - Earliest start date
   - Any client-specific cleanup scope
3. Show the operator the package options found and ask: **"Which package did the client choose?"**
4. If the folder doesn't exist or contains no quote, ask whether to proceed without it (skill falls back to manual pricing) or stop.

---

## Phase 1B — Gather operational info (single batched message)

Ask in one message, numbered:

1. **Legal/business name** — becomes the FC display name
2. **Primary contact name**
3. **Primary contact email**
4. **Primary contact phone** (accept "no phone" / TBD)
5. **Engagement signing date** — when client signs (or "TBD" if not yet signed)
6. **Monthly draft date** — when monthly billing begins (e.g., "2026-08-05")
7. **Cleanup start date** — when cleanup work begins / deposit drafts (often matches earliest start in quote)
8. **Anything to override from the quote?** — confirm package choice if not already given; flag any custom pricing
9. **Team of 3 — Lead** (first name is fine — the person who owns the client relationship / kickoff)
10. **Team of 3 — Staff / Accountant** (first name — the person doing the day-to-day bookkeeping)
11. **Team of 3 — Controller / Reviewer** (first name — the CPA reviewer)

Echo back captured values in a tidy summary, then proceed — Jennifer prefers "create and report back."

**Team lookup:** resolve each team member's FC user_id via `GET /api/v1/users?per_page=100` and match on `name` (case-insensitive first-name match, then confirm the email address before storing). Store as `FC_LEAD_USER_ID`, `FC_STAFF_USER_ID`, `FC_CONTROLLER_USER_ID` for use in Phase 1E task reassignment. Current cached mapping (verified 2026-07-03):

| FC user_id | Name | Email | Typical role |
|---|---|---|---|
| `27782` | Rachel Hastings | rachelh@paxuscpa.com | Lead |
| `35262` | Megan States | megan@paxuscpa.com | Staff |
| `17957` | Cassie Rigsby | cassie@paxuscpa.com | Controller (also a partner) |
| `17946` | Lisa Dionisio | LISA@paxuscpa.com | Controller / partner |
| `26810` | Landry Greenhill | landry@paxuscpa.com | Lead |
| `19343` | Becky Humphers | becky@paxuscpa.com | Staff / Lead |
| `19334` | Michelle Mauldin | michelle@paxuscpa.com | Staff / Lead |
| `19331` | Kristie Andrews | kristie@paxuscpa.com | Staff |
| `19685` | Caroline Jeffreys | caroline@paxuscpa.com | Staff |
| `19998` | Consuelo Gervacio | consuelo@paxuscpa.com | Staff |
| `38164` | Joyce Ann Maregmen | joyce@paxuscpa.com | Staff |
| `17948` | Jennifer Sanders | jennifer@paxuscpa.com | Firm Admin (not on client Team of 3) |
| `31668` | Paxus Intern | intern@paxuscpa.com | Shared intern login |

If the operator names someone whose first name is ambiguous (e.g., two Rachels), ask for the last name or email to disambiguate. Do NOT guess.

**Interns map to the shared `Paxus Intern` login (`31668`, intern@paxuscpa.com).** Interns share one FC login, so they do NOT appear individually in the users roster — a first-name lookup will fail. Known interns (verified 2026-08-07): **Macie, Jenny, Kaitlyn**. When the operator names any intern for a Team-of-3 role (usually Staff/Accountant), assign `31668` — don't stop to disambiguate. Add new intern names here as they come up.

---

## Phase 1C — Create the client in Financial Cents

```bash
TOKEN=$(cat "C:/Users/paxus/.paxus/client onboarding.txt" | tr -d '\n\r' | tr -d ' ')
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"display_name":"<LEGAL_NAME>"}' \
  "https://app.financial-cents.com/api/v1/clients" \
  -w "\nHTTP %{http_code}\n"
```

- JSON-escape `<LEGAL_NAME>` (quotes → `\"`, backslash → `\\`).
- On HTTP 201: parse response, capture `id` → `FC_CLIENT_ID`.
- On 401: token expired/invalid — stop.
- On 422: surface FC's validation errors verbatim — stop.
- On other non-2xx: print body + status — stop.

Client URL: `https://app.financial-cents.com/clients/{FC_CLIENT_ID}`.

---

## Phase 1D — Create the primary contact

```bash
TOKEN=$(cat "C:/Users/paxus/.paxus/client onboarding.txt" | tr -d '\n\r' | tr -d ' ')
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"name":"<NAME>","email":"<EMAIL>","phone":"<PHONE>","notes":"<ROLE>"}' \
  "https://app.financial-cents.com/api/v1/clients/<FC_CLIENT_ID>/contacts" \
  -w "\nHTTP %{http_code}\n"
```

- If phone is TBD/empty, omit the `phone` field (don't send `"TBD"` as a value).
- If you don't know the role, omit `notes`.
- On HTTP 201: capture contact `id` → `FC_CONTACT_ID`.
- On error: print and stop. Client record already exists — tell the operator to add the contact manually.

---

## Phase 1E — Create the New Client Onboarding project from template

**Preconditions:** `FC_CLIENT_ID` (from 1C) and `FC_CONTACT_ID` (from 1D) both exist. Do not run 1E if either creation failed.

The template (id `13946930`, named "Client Onboarding" in FC) already has Jennifer's user_id (`17948`) baked into the "Firm Admin Tasks" section — POSTing from the template auto-assigns those tasks to her (15 admin-workflow tasks).

⚠️ **Do NOT use template `13565957`.** That ID now maps to **"Client - Kick-Off Call"**, which is a separate automation that runs on its own while Jennifer handles the onboarding project — creating it here makes a stray project you can't delete via API (DELETE → 405; UI-only close). Verified on two separate client runs (2026-07-27 and 2026-07-21). Always confirm the target template's `title` is "Client Onboarding" before POSTing.

```bash
TOKEN=$(cat "C:/Users/paxus/.paxus/client onboarding.txt" | tr -d '\n\r' | tr -d ' ')
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"client_id":<FC_CLIENT_ID>}' \
  "https://app.financial-cents.com/api/v1/templates/13946930/projects" \
  -w "\nHTTP %{http_code}\n"
```

- On 200/201: parse response, capture `id` → `FC_PROJECT_ID`. Confirm `client.id` in the response matches `<FC_CLIENT_ID>` AND `title` is "Client Onboarding" (not "Client - Kick-Off Call") — that's how attachment + correct-template is verified (no `client_id` field on the response, only the nested `client` object).
- On error: print body + status and continue. Tell the operator they need to add the New Client Onboarding template manually in the FC UI.

**Why this works (don't re-probe):**
- Endpoint shape: `POST /api/v1/templates/{template_id}/projects`. The unscoped `/projects` and `/clients/{id}/projects` both 405/404.
- Body `{"client_id":<id>}` attaches the project. Body `{}` creates an orphan — avoid.
- No `GET /projects/{id}` or `DELETE /projects/{id}`. To verify tasks: `GET /api/v1/tasks?project_id={FC_PROJECT_ID}`. Stray projects must be closed via FC UI.
- Section-to-user mappings inherit from the template — don't try to assign at creation time.

**8 standard project templates are NOT attached in Phase 1.** They're operational (weekly bookkeeping, month-end review, month-end close, cleanup, post cleanup, kick-off call, client training manual, tax returns) and only make sense after the engagement is signed. Attaching them pre-signing clutters the prospect's FC record and creates cleanup work if the client doesn't sign (FC has no API to delete a stray project — closure is UI-only). See **Phase 2H** for the template attachment + role-reassignment logic.

**Client's Onboarding Checklist (`9685085`) — the skill never POSTs it (Jennifer's rule 2026-08-13).** The client-facing checklist is created by an **FC automation that fires when Jennifer marks the triggering task complete** — not by the skill, and not by template inheritance. Do NOT POST `9685085` in Phase 1 or Phase 2; doing so would create a duplicate. Phase 5's day-before-kickoff email just reads whatever checklist exists at that point (it will, once Jennifer has completed the triggering task).

---

## Phase 1F — Draft proposal content

Write to `~/.claude/skills/onboard-client-admin/handoffs/{slug}-{YYYY-MM-DD}-proposal.md`:

```markdown
# Engagement Proposal — {Legal name}

*Source: {full path to quote PDF}*
*Package selected: **{Package name}***
*Drafted: {YYYY-MM-DD}*

---

## Overview

Paxus CPA Group is pleased to provide accounting services to **{Legal name}** under the **{Package}** package. {1-sentence summary.}

---

## Scope of Services

### Monthly Recurring Services — {Package} (${monthly}/month)
{Pulled from quote.}

### One-Time Onboarding (${onboarding fee})
{Pulled from quote — bullets.}

### Cleanup Project (Floor: ${floor} — Ceiling: ${ceiling})
{Pulled from quote — specific scope bullets.}
Cleanup billing: 50% drafted when cleanup begins; remaining 50% due upon completion.

---

## Fees & Payment Schedule

| Component | Amount | Timing |
|---|---|---|
| Monthly accounting services | ${monthly}/month | Monthly draft beginning {YYYY-MM-DD} |
| Onboarding fee | ${onboarding} | Due upon signing — holds your place in the queue |
| Cleanup deposit (50%) | ${50% of floor} | Drafted {YYYY-MM-DD} when cleanup begins |
| Cleanup balance (50%) | ${remaining range} | Due upon completion |

---

## Terms

- Prices are based on signing up for an ongoing monthly package.
- This quote is valid for **30 days** from issuance.
- Place in the onboarding queue is determined by acceptance of this quote and receipt of the onboarding fee.
- Earliest engagement start date: **{YYYY-MM-DD}**.

---

## Acceptance

By signing below, {Legal name} accepts the scope, fees, and terms above.

**{Legal name}**
Signature: ______________________________
Name: {Contact name}, {Role if known}
Date: __________________________________

**Paxus CPA Group**
Signature: ______________________________
Name: ___________________________________
Date: __________________________________
```

---

## Phase 1G — Generate the handoff doc

Write to `~/.claude/skills/onboard-client-admin/handoffs/{slug}-{YYYY-MM-DD}.md`:

```markdown
# {Legal name} — FC Onboarding Handoff
**Created:** {YYYY-MM-DD}
**FC client ID:** {FC_CLIENT_ID}
**FC link:** https://app.financial-cents.com/clients/{FC_CLIENT_ID}
**FC project ID:** {FC_PROJECT_ID} (New Client Onboarding)
**Package:** {Package}

## What's done
- [x] Client record created in Financial Cents
- [x] Primary contact added: {Name} ({Role}) — {email}
- [x] New Client Onboarding project created and attached to client — Firm Admin Tasks queued for Jennifer
- [x] Proposal content drafted — see `{slug}-{YYYY-MM-DD}-proposal.md`

## What you still need to do in the FC UI

### 1. Build the proposal/engagement in FC
- Open: https://app.financial-cents.com/clients/{FC_CLIENT_ID}
- Copy content from the proposal draft and send to {Contact name} for signature.
- *(No FC public API endpoint exists for proposals — must be done in the UI)*

### 2. Set up billing (after engagement is signed)
| Component | Amount | Cadence | Notes |
|---|---|---|---|
| Accounting services ({Package}) | ${monthly} | Monthly, recurring | Monthly draft begins {YYYY-MM-DD} |
| Onboarding | ${onboarding} | One-time | Due at signing |
| Cleanup deposit | ${50% of floor} | One-time, deposit | Drafted {YYYY-MM-DD}; remaining 50% (${range}) due on completion |

### 3. Engagement start date
- {As captured — "Begins upon signing" or specific date}

## Notes
- {Phone TBD note if applicable}
- After signing, re-run `/onboard-client-admin` for Phase 2.
```

Replace `TBD` for unknowns; don't omit lines.

---

## Phase 1H — Report back

```
Client created in Financial Cents.

  Name:       {Legal name}
  Package:    {Package} — ${monthly}/month
  FC ID:      {FC_CLIENT_ID}
  FC link:    https://app.financial-cents.com/clients/{FC_CLIENT_ID}
  Contact:    {Name} ({email})
  Project:    New Client Onboarding (id {FC_PROJECT_ID}) — Firm Admin Tasks assigned to you

Files saved:
  • Handoff:   C:\Users\paxus\.claude\skills\onboard-client-admin\handoffs\{slug}-{date}.md
  • Proposal:  C:\Users\paxus\.claude\skills\onboard-client-admin\handoffs\{slug}-{date}-proposal.md

Next in FC UI:
  • Build the proposal (paste from draft) and send for signature.
  • Once signed, run /onboard-client-admin → Phase 2.
```

End with one warm line — e.g., "Done — {Legal name} is in the books."

---

## Phase 2 — Post-signing setup (Shared Drive, engagement filing, FC dashboard)

Run when the engagement is signed in FC. No FC API for engagement status — the operator confirms verbally.

**Phase 2 steps at a glance (execute in order):**

| Step | What it does |
|---|---|
| 2A | Confirm preconditions + auto-discover engagement PDF |
| 2B | Prompt operator to create the Shared Drive |
| 2C | Copy the client template into the new Shared Drive |
| 2D | File signed engagement PDF to Perm File + Active Clients |
| 2E | Move prospective folder to Active Clients |
| 2F | POST Shared Drive URL to FC as a "Google Drive" Resource |
| 2G | Create "Engagement Letters" folder in FC Files tab + upload engagement |
| 2H | Attach the 8 standard project templates (all tiers) + reassign tasks by role |
| 2I | Attach 1099 project templates (Full Service / Premium only — skip for Basic) |
| 2J | Write the working handoff doc into the client's Perm File |
| 2K | Report back to operator |

### Important rules for Phase 2

- **Shared Drive name = the exact legal client name** as the operator types it. No prefix, no slug. (Operator may use punctuation like commas; match what they create.)
- **Template path:** `/g/Shared drives/00 - Paxus CPA/Clients/02 - Client Template to copy/`.
- **No fabrication.** If the engagement PDF isn't where the operator says, stop and ask.
- **Drive for Desktop sync lag is real.** If a copy fails partway through, files may still be streaming. Re-check before assuming files are lost — many will show up in Shared Drive Trash if they were placeholder-only at copy time.
- **Assume ready by default.** Jennifer's rule: when she kicks off Phase 2 after signing, don't re-ask whether the Shared Drive is created or the engagement is downloaded — assume both. Only pause and ask if the drive isn't mounted or the `Engagement*.pdf` auto-discovery finds nothing.
- **`.gdoc` files are unreadable through the mount.** Drive-native files (Google Docs / Sheets / Slides) appear as 176-byte pointers on Drive for Desktop and refuse byte-level reads via any local mechanism (Read, cp, Python, PowerShell). Expect `cp -r` to fail on them during the Prospective → Active move; they land in the source Shared Drive's Trash. Always list stragglers in the handoff so the operator can restore them from Drive web → Trash.

---

### Phase 2A — Confirm preconditions and locate Phase 1 artifacts

**Engagement file discovery:** Jennifer's downloaded engagement PDF is **always the most recent file in `~/Downloads/` whose name matches `Engagement*.pdf`**. Auto-discover it with:

```bash
ls -t ~/Downloads/Engagement*.pdf 2>/dev/null | head -1
```

Show her the file (name + modification time) and confirm it's the right one before using it. Only ask for the filename if this discovery finds nothing.

Ask the operator (one batched message — skip questions the auto-discovery already answered):

1. **Which client?** (legal name — usually recoverable from the Phase 1 handoff or by scanning Prospective Clients; confirm if ambiguous)
2. **Is the engagement signed in FC?** (must be yes to proceed)
3. **Shared Drive name?** (default = the exact legal client name as it appears in FC and on the engagement; confirm before she creates it)
4. **Team of 3 — Lead, Staff, Controller** (first names). Required for Phase 2H task reassignment. If the Phase 1 handoff already lists them, confirm; if TBD, ask now. Resolve each first name to a `user_id` via `GET /api/v1/users?per_page=100` — see the cached mapping in Phase 1B.

Then look for a Phase 1 handoff at `handoffs/{slug}-*.md`. If found, read it to recover FC client ID, contact, package. If not found, ask for the FC client ID so Phase 2's handoff entry can link to it.

**Verify the Phase 1 Client Onboarding project still exists (do NOT skip).** Phase 2 assumes Phase 1's onboarding project is still attached — but it can be gone. The FC **UI can hard-delete** projects (the API can't — `DELETE /projects/{id}` → 405), and when the operator cleans up stray projects after Phase 1, it's easy to delete the legitimate Client Onboarding project along with them. This happened on a prior client run (the Phase 1 FC project came back `GET /projects/{id}` → HTTP 404 "No query results"). If it's missing and Phase 2 proceeds blindly, the client ends up with no Firm Admin Tasks. (The **Client's Onboarding Checklist is separate** — created by an FC automation when Jennifer marks the triggering task complete, not by the skill — so it is NOT something to restore here.)

Check it explicitly:

```bash
# Direct existence probe on the Phase 1 project id (from the handoff). 404 = deleted; 200 = still there.
curl -s -A "Mozilla/5.0" -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "https://app.financial-cents.com/api/v1/projects/<FC_PROJECT_ID>" -w "\nHTTP %{http_code}\n"
# Belt-and-suspenders: paginate GET /projects?per_page=100 and confirm at least one project with
# client.id == <FC_CLIENT_ID> whose title matches "onboarding" (Client Onboarding).
# Closed projects DO appear in the list, so absence = deleted.
```

If the **Client Onboarding project is missing**, stop and tell the operator, then ask how to restore before continuing Phase 2:
- **Restore it:** `POST /templates/13946930/projects {"client_id":<id>}` — restores the 15 Firm Admin Tasks (auto-assigned to Jennifer). Do NOT use `13565957` (that's the Kick-Off Call template). Note the pre-signing Firm Admin Tasks reappear as open even if already done — the operator ticks those off.
- **Leave it:** operator handles manually in the FC UI. If chosen, record the decision in the handoff.

Do NOT POST the Client's Onboarding Checklist (`9685085`) — it's created by an FC automation when Jennifer completes the triggering task, so POSTing it would make a duplicate.

Record the outcome (found intact / restored via which template / left per operator) in the Phase 2 handoff.

**FC API needs a browser User-Agent.** FC's WAF returns HTTP 403 to the default Python `urllib` User-Agent (`Python-urllib/x.y`) while `curl` passes. If you script FC calls in Python (`urllib`/`requests`), always send `User-Agent: Mozilla/5.0`. (Discovered 2026-07-10 — a paginated `urllib` scan 403'd on every page until the UA header was added; `curl` had been fine throughout.)

**Windows Python vs Git-Bash `/tmp`.** In the Bash tool, `/tmp` maps to `C:\Users\paxus\AppData\Local\Temp`, but Windows-native Python resolves a bare `/tmp/foo.json` to `C:\tmp\foo.json` (nonexistent → `FileNotFoundError`). When a Python heredoc reads/writes files the bash side put in `/tmp`, use the real Windows path (`C:/Users/paxus/AppData/Local/Temp/...`), not `/tmp/...`.

---

### Phase 2B — Create the Shared Drive (operator action, then verify)

Tell the operator:

> Open Google Drive → "Shared drives" → "+ New" → name it exactly **`{Legal name}`** (no prefix, no suffix). Type `ready` when the drive exists.

Verify the drive is mounted:

```bash
test -d "/g/Shared drives/{Legal name}" && echo "FOUND" || echo "MISSING"
```

If `MISSING`, give Drive for Desktop ~15 seconds, then re-check. If still missing, list `/g/Shared drives/` and grep for a close match — operator may have used slightly different punctuation. Confirm name with operator before proceeding.

---

### Phase 2C — Copy template into the new Shared Drive

```bash
cp -r "/g/Shared drives/00 - Paxus CPA/Clients/02 - Client Template to copy/." "/g/Shared drives/{Legal name}/"
ls "/g/Shared drives/{Legal name}/"
```

Confirm 11 standard folders: Audit, Bank Statements, CC Stmts, Certificates of Insurance, Client Intro, Financials, Loans, Payroll, Perm File, Review Notes, Taxes. Then verify the seed files copied:

```bash
ls "/g/Shared drives/{Legal name}/Perm File/" "/g/Shared drives/{Legal name}/Client Intro/"
```

Expected seed files:
- `Perm File/Blank Password Log.xlsx`
- `Perm File/Checklist - Change of Bank Account.docx`
- `Perm File/Client Overview Questionnaire.docx`
- `Client Intro/Client Intro Questionnaire - FILLABLE v2.docx`

---

### Phase 2D — File the signed engagement PDF

Use the filename captured in 2A. Copy to both locations, renaming to include the client:

```bash
cp ~/Downloads/{FILENAME} "/g/Shared drives/{Legal name}/Perm File/Engagement - {Legal name}.pdf"
mkdir -p "/g/Shared drives/00 - Paxus CPA/Admin/Client Onboarding/Active Clients/{Legal name}"
cp ~/Downloads/{FILENAME} "/g/Shared drives/00 - Paxus CPA/Admin/Client Onboarding/Active Clients/{Legal name}/Engagement - {Legal name}.pdf"
ls -la "/g/Shared drives/{Legal name}/Perm File/Engagement - {Legal name}.pdf" "/g/Shared drives/00 - Paxus CPA/Admin/Client Onboarding/Active Clients/{Legal name}/Engagement - {Legal name}.pdf"
```

---

### Phase 2E — Move the prospective folder to Active Clients

The prospective folder name may differ slightly from the FC name (e.g., extra punctuation). Check both literal name and similar-name match, and — critically — check whether any `.gdoc` (or `.gsheet`/`.gslides`) files are in the source before deleting anything.

**`.gdoc` rule (durable — chosen by Jennifer 2026-07-03):** If ANY Drive-native pointer file (`.gdoc`, `.gsheet`, `.gslides`) exists in the source folder, **copy the non-native files to Active and leave the source folder in place**. `.gdoc` pointers can't be read or copied through the Drive-for-Desktop mount, and `rm -rf`'ing them deletes the pointer (the underlying Google Doc survives in Drive itself but detaches from the folder tree). Leaving the source folder in place is the recover-your-gdoc-here signal to the operator. The operator manually finalizes by opening each `.gdoc` in Drive web, converting to `.docx`, dropping the converted file in Active Clients, then deleting the source folder from Drive web.

If NO `.gdoc`/`.gsheet`/`.gslides` files are in the source, do the full move (`cp` + `rm -rf`) as normal.

```bash
SRC="/g/Shared drives/00 - Paxus CPA/Admin/Client Onboarding/Prospective Clients/{Legal name}"
DEST="/g/Shared drives/00 - Paxus CPA/Admin/Client Onboarding/Active Clients/{Legal name}"
if [ -d "$SRC" ]; then
  mkdir -p "$DEST"
  # Check for Drive-native pointer files
  GDOC_COUNT=$(find "$SRC" -maxdepth 1 -type f \( -name '*.gdoc' -o -name '*.gsheet' -o -name '*.gslides' \) 2>/dev/null | wc -l)
  cp -r "$SRC/." "$DEST/" 2>&1 | grep -v "cannot stat" || true
  if [ "$GDOC_COUNT" -gt 0 ]; then
    echo "Copied to $DEST — $GDOC_COUNT Drive-native pointer file(s) left in $SRC for manual conversion."
    find "$SRC" -maxdepth 1 -type f \( -name '*.gdoc' -o -name '*.gsheet' -o -name '*.gslides' \)
  else
    rm -rf "$SRC" && echo "Moved (full) -> $DEST"
  fi
else
  echo "Exact name not found — searching for close match:"
  ls "/g/Shared drives/00 - Paxus CPA/Admin/Client Onboarding/Prospective Clients/" | grep -i "{distinctive-substring}"
fi
```

If a close match exists, confirm with the operator before moving.

**When `.gdoc` stragglers exist:** report them in the handoff with an "operator to-do: convert to .docx in Drive web and move to Active Clients, then delete the source folder from Drive web" line. Do not attempt to delete the source folder from the local mount — Drive-for-Desktop will resurrect the phantom (verified 2026-07-03) until the operator handles it via Drive web.

---

### Phase 2F — Add the Shared Drive link to FC as a client Resource

FC exposes a Resources section on each client dashboard. Attach the new Shared Drive there so the team can jump to it from FC. Endpoint: `POST /api/v1/clients/{FC_CLIENT_ID}/resources` with `{"label":"Google Drive","url":"<share URL>"}`.

**Getting the Shared Drive share URL:** the Drive-for-Desktop mount doesn't expose the underlying Drive ID. Ask the operator to grab it:

> Open https://drive.google.com/ → Shared drives → **{Legal name}** → click the drive name → the browser URL now shows `.../drive/u/0/folders/{DRIVE_ID}`. Paste the full URL.

Then POST it:

```bash
TOKEN=$(cat "C:/Users/paxus/.paxus/client onboarding.txt" | tr -d '\n\r' | tr -d ' ')
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"label":"Google Drive","url":"<share URL>"}' \
  "https://app.financial-cents.com/api/v1/clients/<FC_CLIENT_ID>/resources" \
  -w "\nHTTP %{http_code}\n"
```

- On 200/201: capture `id` → `FC_RESOURCE_ID` for the handoff doc.
- Before POSTing, `GET /clients/{FC_CLIENT_ID}/resources` and check whether a "Google Drive" resource already exists (label match). If so, skip the POST — don't create duplicates.
- On error: print body + status and continue. Tell the operator to add the resource manually in the FC UI (client dashboard → Resources → add link).

---

### Phase 2G — Attach the engagement letter to FC's Files tab

Create an "Engagement Letters" folder in the client's FC Files tab and upload the signed engagement PDF into it. Uses two endpoints:

**Create the folder** (`POST /api/v1/clients/{FC_CLIENT_ID}/attachments/folders`):

```bash
TOKEN=$(cat "C:/Users/paxus/.paxus/client onboarding.txt" | tr -d '\n\r' | tr -d ' ')
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"name":"Engagement Letters"}' \
  "https://app.financial-cents.com/api/v1/clients/<FC_CLIENT_ID>/attachments/folders" \
  -w "\nHTTP %{http_code}\n"
```

- On 201: capture `id` → `FC_FOLDER_ID`.
- Before POSTing, `GET /clients/{FC_CLIENT_ID}/attachments` and check whether an "Engagement Letters" folder already exists. If so, reuse its `id` — the API happily creates duplicates.

**Upload the engagement** (`POST /api/v1/clients/{FC_CLIENT_ID}/attachments` with multipart form-data):

```bash
# curl multipart uploads want a real filesystem path — copy to /tmp first so the client-friendly name gets preserved.
cp ~/Downloads/Engagement.pdf "/tmp/Engagement - <Legal name>.pdf"
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -F "file=@/tmp/Engagement - <Legal name>.pdf" \
  -F "parent_id=<FC_FOLDER_ID>" \
  "https://app.financial-cents.com/api/v1/clients/<FC_CLIENT_ID>/attachments" \
  -w "\nHTTP %{http_code}\n"
```

- On 201: capture `id` → `FC_ENGAGEMENT_ATTACHMENT_ID` for the handoff.
- On error: print body + status. Tell the operator they need to add the folder + upload manually.

**Client-portal visibility caveat.** The API surfaces neither a per-folder nor a per-file "share with client" field — `contact_id`, `visible_to_client`, `share_with_client`, `is_shared_with_client`, and a `/share` sub-route all no-op or 404. The contact's `nothing_shared` field suggests FC's default is that the primary contact can see firm-side files unless restricted, but confirm on first run and flag in the handoff so the operator can toggle in the UI if needed.

**Attachments endpoints (confirmed 2026-07-01):**
- `GET /clients/{id}/attachments` — list top-level attachments; each folder record has `items_count`.
- `POST /clients/{id}/attachments/folders` — body `{"name":"..."}`; only `name` is honored.
- `POST /clients/{id}/attachments` — multipart, requires `file`; accepts `parent_id` to nest inside a folder.
- `DELETE /clients/{id}/attachments/{attachment_id}` — works for both files and folders; returns HTTP 201 with empty body.
- `PATCH`/`PUT` on `/clients/{id}/attachments/{id}` → 405; folders/files are immutable after creation.

---

### Phase 2H — Attach the 8 standard project templates (all tiers)

These are operational projects that make sense only after the engagement is signed. They're attached here (Phase 2), NOT Phase 1 — a prospect who never signs shouldn't have Weekly Bookkeeping or Cleanup projects sitting in their FC record, and FC has no API to delete a stray project (closure is UI-only).

**Template IDs (all verified live 2026-08-13):**

| Purpose | Template ID | Title in FC |
|---|---|---|
| Weekly Bookkeeping Tasks | `5082639` | `Weekly Bookkeeping Tasks` |
| Month-End Review | `5082645` | `Month-End Review` |
| Month-End Close | `5110296` | `Month-End Close` |
| Cleanup | `8266589` | `Client - Cleanup` |
| Post Cleanup | `13989492` | `Client - Post Cleanup` |
| Kick-Off Call | `13565957` | `Client - Kick-Off Call` |
| Client Training Manual | `7995444` | `Employee - Client Training Manual` |
| Tax Returns | `7959692` | `Tax Returns` |

All 8 attach for every tier. Notes:
- **Kick-Off Call (`13565957`) is intentional here.** The Phase 1E warning about `13565957` is only about NOT using it as the *onboarding* project in Phase 1 (that ID's title is "Client - Kick-Off Call", not "Client Onboarding"). Attaching it in Phase 2 as the client's kickoff-call project is correct and expected.
- **Client Training Manual (`7995444`)** is the `Employee - Client Training Manual` template. Do NOT confuse it with the other `Employee - *` training templates (Tech Stack `7995684`, Non-Profit `8838356`, Dext `8573106`) — those are not attached here.
- FC renamed the two monthly templates to `Month-End Review` / `Month-End Close` (previously `**Monthly Client - *`); IDs unchanged. Titles no longer carry leading asterisks.
- Post Cleanup is the transition-to-recurring project that follows the initial Cleanup.
- Client's Onboarding Checklist (`9685085`) is NOT part of this 8-project loop — it's handled separately (see Phase 1E / Phase 2A). Do NOT POST it here.

**Attach each, then reassign by role:**

```bash
for TID in 5082639 5082645 5110296 8266589 13989492 13565957 7995444 7959692; do
  # 1. Create the project
  curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{\"client_id\":<FC_CLIENT_ID>}" \
    "https://app.financial-cents.com/api/v1/templates/${TID}/projects" \
    -w "\nHTTP %{http_code}\n"
  # capture the returned project id as $NEW_PROJECT_ID from the response

  # 2. List that project's tasks and reassign by project_role.name
  curl -s -H "Authorization: Bearer $TOKEN" \
    "https://app.financial-cents.com/api/v1/tasks?project_id=${NEW_PROJECT_ID}" \
    > /tmp/tasks_${NEW_PROJECT_ID}.json
  # For each task, look at task.project_role.name and PUT the correct user_id.
done
```

**Role → team member mapping** (captured in Phase 2A):

| FC `project_role.name` | Team member variable | Rationale |
|---|---|---|
| `Lead Accountant` | `FC_LEAD_USER_ID` | The Lead owns the client relationship and drives kickoff. |
| `Staff Accountant` | `FC_STAFF_USER_ID` | The Staff does day-to-day bookkeeping tasks. |
| `CPA/Controller` | `FC_CONTROLLER_USER_ID` | The Controller (partner-level) does the CPA-side reviews. |

If a task has a `project_role.name` that doesn't match any of the three above (rare — usually a template glitch), leave the default assignment in place and note it in the handoff.

**Reassign each task:**

```bash
# For each task where project_role.name matches one of the three roles:
curl -s -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{\"assignees\":[<TARGET_USER_ID>]}" \
  "https://app.financial-cents.com/api/v1/tasks/<TASK_ID>" \
  -w "\nHTTP %{http_code}\n"
```

- **Body field is `assignees` (array), NOT `user_id`.** Verified 2026-07-03. `PUT` with `{"user_id":...}` returns HTTP 200 with the task record but silently discards the change — the `user` field is derived, not writable directly. The writable field is the `assignees` array. `{"assignees":[N]}` replaces the assignee list; include every desired assignee in the array.
- **Use PUT, not PATCH.** `PATCH /tasks/{id}` returns HTTP 405.
- The response includes `"assignees":[{"id":N,"name":"..."}]` — confirm the target user is present.
- **Idempotency check per task:** if the task's current `assignees` is already `[target_user_id]` (single-element list matching the target), skip the PUT.
- On error for any single task: print body + status and continue. Log the failure in the handoff so the operator can reassign that specific task manually.

**Note on the top-level `user` field:** every task record also has a top-level `user` object which stays populated with whatever the template's default was (usually Lisa or Jennifer). That field is not user-writable via the tasks endpoint and doesn't affect FC's UI display of "who's assigned to this task" — the FC UI shows the `assignees` list. Don't waste time trying to update `user`.

**Verification after the loop:**

```bash
# GET tasks per project and confirm distribution matches expected roles
curl -s -H "Authorization: Bearer $TOKEN" "https://app.financial-cents.com/api/v1/tasks?project_id=${NEW_PROJECT_ID}" \
  | python -c "
import sys, json
d = json.load(sys.stdin).get('data', [])
from collections import Counter
by_role = Counter(((t.get('project_role') or {}).get('name'), (t.get('user') or {}).get('name')) for t in d)
for (role, user), n in by_role.items():
    print(f'  {role} → {user}: {n} tasks')
"
```

Ideal outcome: every `Lead Accountant` task → Lead's name; every `Staff Accountant` task → Staff's name; every `CPA/Controller` task → Controller's name.

- **Idempotency:** if this run is re-invoked and any of the 8 templates are already attached (e.g., an earlier Phase 2 pass ran), FC will happily create duplicates. Before POSTing, `GET /projects?per_page=100` (paginate as needed) and filter for `client.id == FC_CLIENT_ID`; skip any template whose title (case-insensitive, stripping leading `*`s) already appears in the client's project list. Even on skip, run the task reassignment loop against the existing project — role assignments may not have been done yet.
- **Non-recurring projects (Client Onboarding, Client's Onboarding Checklist) are NOT reassigned** — Jennifer's rule 2026-07-03. Those have Firm Admin Tasks (Jennifer) and Onboarding Checklist tasks that stay on defaults.
- **No API to delete a stray project.** `DELETE /projects/{id}` returns HTTP 405 — verified 2026-07-03. Any duplicate that gets created (bad template ID, retry storm, etc.) must be closed via FC UI.

---

### Phase 2I — Attach 1099 project templates (Full Service / Premium Service only)

**Package gate.** Read the package from the Phase 1 handoff (`**Package:**` line) or, if unavailable, ask the operator. Three tiers:

| Package | 1099 behavior |
|---|---|
| `Basic` | Skip this entire step. Log `1099 projects: skipped (Basic)` in the handoff addendum and continue to 2J. |
| `Full Service` | Attach the 1099 *work* templates (see exclusion below). |
| `Premium Service` | Attach the 1099 *work* templates (see exclusion below). |

Match is case-insensitive; a `Basic` package skips even if the string is `Basic Service`, `basic`, etc.

**Do NOT attach the "1099 - Bill Clients | Admin" template during onboarding** (Jennifer's rule 2026-07-25). That billing project is **auto-created when the 1099 work project is closed** — attaching it here would create a premature duplicate that has to be closed via the FC UI (no delete API). Attach only the 1099 *work* templates and exclude any template whose title matches `1099 - Bill Clients` (case-insensitive).

**Discover 1099 templates dynamically** (do NOT hardcode IDs — Jennifer may add more later):

```bash
TOKEN=$(cat "C:/Users/paxus/.paxus/client onboarding.txt" | tr -d '\n\r' | tr -d ' ')
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://app.financial-cents.com/api/v1/templates?per_page=100" \
  -o /tmp/fc_templates.json

# FC template records carry `title` (not `name`) and have NO `category` field.
# 1099 templates are identified by title starting with "1099 -" (or "1099 " prefix).
# EXCLUDE the billing template — "1099 - Bill Clients | Admin" (auto-created on 1099 project close).
jq '.data[] | select(.title | test("^1099[ -]"; "i")) | select(.title | test("bill clients"; "i") | not) | {id, title}' /tmp/fc_templates.json
```

Show the operator the discovered list (id + title) and confirm before creating projects.

**Known 1099 templates as of 2026-07-25** (for verification):

| Template ID | Title | Attach? |
|---|---|---|
| `8846512` | 1099 - Bill Clients \| Admin | **NO — excluded** (auto-created when the 1099 work project is closed) |
| `8856701` | 1099 - End of Year | Yes |
| `13103367` | 1099 - Identify Vendors Requiring W-9s \| Staff and Lead | Yes |
| `13103482` | 1099 - Vendor Cleanup in QBO | Yes |

**Attach each 1099 template to the client:**

```bash
# For each TEMPLATE_ID discovered above (billing template already excluded):
for TEMPLATE_ID in <1099_TEMPLATE_ID_1> <1099_TEMPLATE_ID_2> ...; do
  curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{\"client_id\":<FC_CLIENT_ID>}" \
    "https://app.financial-cents.com/api/v1/templates/${TEMPLATE_ID}/projects" \
    -w "\nHTTP %{http_code}\n"
done
```

- On 200/201 for each: parse response, capture `id` → append to `FC_1099_PROJECT_IDS` (list of `{template_title, project_id}` pairs for the handoff).
- Verify each response's nested `client.id` matches `<FC_CLIENT_ID>` — same attachment check as Phase 1E's New Client Onboarding POST.
- On error for any template: print body + status and continue with the next one. Note the failure in the handoff so the operator can attach that specific template manually via FC UI.

**Idempotency check (optional but cheap):** before POSTing, `GET /projects?per_page=100` and filter for `client.id == FC_CLIENT_ID` and name matching `1099`. If a matching project already exists, skip that template — don't create duplicates.

**Why this step is skill work, not template-inherited:** The New Client Onboarding template no longer auto-attaches 1099 projects (updated in FC 2026-07-02 — differs from the earlier 2026-07-01 behavior). The skill now owns 1099 attachment decisions based on package tier.

---

### Phase 2J — Write the handoff doc to the client's Perm File

Save the working handoff to the **client's Shared Drive `Perm File\`** so it lives alongside the engagement, welcome packet, and other permanent artifacts:

```
/g/Shared drives/{Legal name}/Perm File/Onboarding Handoff - {Legal name}.md
```

If a Phase 1 handoff exists at `~/.claude/skills/onboard-client-admin/handoffs/{slug}-*.md`, copy it into Perm File under that name, then append a `## Phase 2 completed {YYYY-MM-DD}` section listing:
- Shared Drive path + template-copy confirmation
- Engagement PDF locations (Perm File + Active Clients)
- Prospective → Active move result
- FC Resource link added (label + URL + resource ID), or "already existed" if skipped
- 8 project IDs (Weekly Bookkeeping, Month-End Review, Month-End Close, Cleanup, Post Cleanup, Kick-Off Call, Client Training Manual, Tax Returns) + task-reassignment result per role
- 1099 projects: either `skipped (Basic Service)` or the list of `{template name → project id}` created (plus any failures)
- Any stragglers in Shared Drive Trash (filenames)
- Open: `team@paxuscpa.com` membership not yet added (manual)

If no Phase 1 handoff exists, write a fresh handoff directly in Perm File with the same content + the FC client ID. Leave a mirror copy in `~/.claude/skills/onboard-client-admin/handoffs/` for reference — but Perm File is the source of truth going forward.

---

### Phase 2K — Report back

```
Phase 2 done — {Legal name} is set up.

  Shared Drive:    /g/Shared drives/{Legal name}/ — template copied (11 folders, 4 seed files)
  Engagement:      Filed in Perm File + Active Clients + FC Files tab
  FC Resource:     "Google Drive" link added to client dashboard (or "already existed")
  FC Files:        "Engagement Letters" folder + engagement uploaded (verify client-portal visibility in FC UI)
  Folder move:     Prospective → Active Clients
  Projects:        8 project templates attached — Weekly Bookkeeping, Month-End Review, Month-End Close, Cleanup, Post Cleanup, Kick-Off Call, Client Training Manual, Tax Returns; tasks reassigned by role (Lead / Staff / Controller)
  1099 projects:   {"skipped (Basic Service)" | list of "<template name> (id <project_id>)"}
  Handoff:         /g/Shared drives/{Legal name}/Perm File/Onboarding Handoff - {Legal name}.md

Still to do (manual, in Drive UI):
  • Add team@paxuscpa.com to the new Shared Drive as a Manager
    — open https://drive.google.com/ → Shared drives → {Legal name} → Manage members

Next: run /onboard-client-admin → Phase 3 (welcome packet + welcome email).
```

End warmly — e.g., "Welcome, {Legal name} — they're officially active."

---

## Phase 3 — Welcome packet (Canva) + welcome email

Run after Phase 2 completes. Personalizes the package master in Canva, exports a PDF to the client's Shared Drive `Perm File\`, and drafts the warm welcome email to the client.

### Important rules for Phase 3

- **Never edit the master designs directly.** `copy-design` first.
- **Never edit team-member block designs directly** — they're shared assets across all clients.
- **Interns: named in the welcome email, omitted from the packet (Jennifer's rules; email behavior updated 2026-08-13).** Interns don't get a bio block. When a Team-of-3 role (usually Staff) is filled by an intern (Paxus Intern / Macie / Jenny / Kaitlyn — see the Phase 1B intern note):
  1. **Welcome packet:** omit that block from the team page — the packet shows only the Controller and Lead blocks. Adjust the page-2 layout to 2 blocks (see Phase 3C / 3E).
  2. **Welcome email:** **name the intern** (first name) under Team of Three — do NOT list them as "to be determined." *(This reverses the earlier 2026-08-07 rule. Non-intern Staff still show as "to be determined" in the email — see Phase 3H.)*

  Interns are still assigned in FC in Phase 2H under the shared intern login (`31668`).
- **Drive PNG → Canva upload URL pattern:** `https://lh3.googleusercontent.com/d/{FILE_ID}`. The `drive.google.com/uc?export=download&id=...` URL is NOT accepted by Canva (303 redirect, ingest fails). Canva's own export URLs are also rejected (private signed S3).
- **Welcome email template** lives at `welcome-email-template.md`. Don't ship the "(50% of the lower range)" wording when the engagement uses a flat or bundled cleanup fee — rewrite the line to match the engagement.

### Canva IDs (Paxus team account, confirmed 2026-06-26)

| Package | Master design ID |
|---|---|
| Full Service | `DAHMXYL-a5g` |
| Basic | `DAHNmFp_ltM` |
| Premium | `DAHNmNfCQw8` |
| **Destination folder** (finished packets) | `FAF-ADpbNnU` |

### Drive Bios folder (team-member PNGs, anyone-with-link sharing on)

- Folder: `https://drive.google.com/drive/folders/1L16UTDzb27mHmpcHJQprVkOxiwqHcZqV`
- Folder ID: `1L16UTDzb27mHmpcHJQprVkOxiwqHcZqV`
- Path on disk: `G:\Shared drives\00 - Paxus CPA\Admin\Website\Bios\`

**Always re-parse the Bios folder before uploading — don't trust the cache blindly.** Bios get edited in place (Jennifer re-does a person's slide, replaces the PNG, sometimes renames the file). Cached IDs go stale silently and you'll ship the old design. Command:

```bash
curl -sL "https://drive.google.com/drive/folders/1L16UTDzb27mHmpcHJQprVkOxiwqHcZqV" -A "Mozilla/5.0" > /tmp/bios.html
# extract each staff member's current file ID by matching the trailing chars near data-tooltip
```

Reference cache (last verified 2026-07-01 — treat as hints, verify freshness on each run):

| Filename | Drive file ID | Last verified |
|---|---|---|
| Cassie Rigsby.png | `1ecgr3re1JZhXIEKJ7KjzQiiXasxLismz` | 2026-07-01 (renamed from `1_Cassie Rigsby.png`; content updated to say "Controller") |
| 8_Joyce Maregmen.png | `11wk1kGoGal2CaC2NrbZhOWlzWm4OYgjH` | 2026-06-26 |
| 9_Rachel Hastings.png | `1X5fgFBWX-niiIAqav03kIwCQzLCSZ2xS` | 2026-06-26 |
| 6_Kristie Andrews.png | `1LNm9l7l_rjppcOUe6_Clh-Se86dcVpJQ` | 2026-06-30 |
| 7_Consuelo Gervacio.png | `14IY1ytJIwwh2GketIzDZJToD-UJfARDE` | 2026-06-30 |
| 2_Megan States.png | `1paEK1x8OCAIK_2G1jjKJDSxKwVnkUgGs` | 2026-06-30 |
| 3_Becky Humphers.png | `1dKbkW6_aT3fRFoIMcE9YKlHPdj_kvOAt` | 2026-06-30 |
| 4_Caroline Jeffreys.png | `17ZyXMqClR5L5E23ilFz0a5uKnKAuGY4a` | 2026-06-30 |
| 5_Landry Greenhill.png | `1UJno3wx-VJzMcwcNzfVMHv-LZLRWt4bz` | 2026-06-30 |
| 10_Michelle Mauldin.png | `1dgNzMOKnGC8zGHtebxu9zb7EhAczxOJm` | 2026-06-30 |

(Lisa, Megan, Becky, Caroline, Landry, Kristie, Consuelo, Michelle — TBD until they appear in a client's team.)

---

### Phase 3A — Confirm preconditions and gather inputs (single batched message)

Read the Phase 1 handoff for `{slug}-*.md` to recover client name, FC ID, package, and primary contact. Then ask:

1. **Which 3 team members fill Controller / Lead / Staff** for this client?
2. **Send time** — morning or afternoon? (Used for "Good morning" vs "Good afternoon" in the email.)
3. **For the cover page** — full legal client name fits on 2 lines; confirm or offer a short form if the legal name is unusually long.

---

### Phase 3B — Copy the package master to a throwaway

```
mcp__claude_ai_Canva__copy-design(design_id: <package master ID>)
```

The returned design ID is the working copy. Use this for all subsequent edits — do not touch the master.

---

### Phase 3C — Get team-block file IDs and upload to Canva

For each assigned team member who has a bio block (Controller, Lead, Staff in that page-2 order):

**Intern exception:** if the Staff member is an intern, they usually have no bio slide in the Bios folder. It's OK to **leave the intern off the Welcome Packet** — upload only the blocks that exist (typically Controller + Lead) and place just those on page 2 (see Phase 3E). The intern is still named in the welcome email's Team of Three (Phase 3H); they just don't appear on the packet.

1. **Resolve Drive file ID:** always re-parse the Bios folder HTML on each run and compare to the cache. If the cache entry disagrees (file was renamed or replaced), use the fresh ID and update the cache with the new "last verified" date.
2. **Build the direct-fetch URL:** `https://lh3.googleusercontent.com/d/{FILE_ID}`
3. **Upload:**
   ```
   mcp__claude_ai_Canva__upload-asset-from-url(url: <lh3 URL>, name: "{First Last} - team block")
   ```
   Returns an `asset_id`. Keep all 3 — they're needed for Phase 3E.

---

### Phase 3D — Text-swap pages 1 and 7

Start an editing transaction on the working copy:

```
mcp__claude_ai_Canva__start-editing-transaction(design_id: <working copy>)
```

Find the element IDs for the package-name placeholder on page 1 (e.g., `FULL SERVICE` / `BASIC` / `PREMIUM`) and the `XXXXX` placeholder on page 7. These are stable on the Full Service master:
- Page 1 "FULL SERVICE": `PBBmQW3jLpcqG42m-LBNJHY2pW54z1Fnf`
- Page 7 "XXXXX": `PBfbgrMgx6k3P9Mm-LBVBvW2L098zGTDK`

For Basic / Premium, verify the element IDs on first use (re-parse from the start-editing-transaction response).

Operations to issue in a single `perform-editing-operations` call:

```python
[
  {"type": "find_and_replace_text", "element_id": "<page1 placeholder>", "find_text": "<package name>", "replace_text": "<Client legal name>"},
  {"type": "find_and_replace_text", "element_id": "<page7 placeholder>", "find_text": "XXXXX", "replace_text": "<Client legal name>"},
  {"type": "update_title", "title": "<Client legal name> - Welcome Packet"}
]
```

Then commit:
```
mcp__claude_ai_Canva__commit-editing-transaction(transaction_id: <returned id>)
```

---

### Phase 3E — Insert 3 team blocks on page 2

Open a new editing transaction on the same working copy. Page 2 layout (816×1056, "Meet Your Team" title at y≈122, URL at y≈993):

| Position | Top | Left | Width | Height |
|---|---|---|---|---|
| Controller (top) | 170 | 62 | 693 | 260 |
| Lead (middle) | 450 | 62 | 693 | 260 |
| Staff (bottom) | 730 | 62 | 693 | 260 |

Single `perform-editing-operations` call with one `insert_fill` op per uploaded block (asset_type=image, asset_ids from Phase 3C, page_id of page 2). Then commit.

**If the Staff is an intern and was omitted (2 blocks):** place Controller (top) and Lead (middle) in their normal slots and leave the bottom slot empty, or ask the operator whether to re-center the two blocks. Don't invent a third block for the intern.

**Visual-size mismatch escape hatch.** If the operator says one block renders visually larger than the others after export (because a bio PNG's internal composition has less padding than the others), keep the other two blocks alone and shrink the offending one:

```python
# Inside a fresh transaction:
{"type": "resize_element", "element_id": "<block element id>", "width": 640, "preserve_aspect_ratio": True}
{"type": "position_element", "element_id": "<block element id>", "top": <adjusted top>, "left": <adjusted left>}
```

Rule of thumb: `width: 640` (down from 693, ~92%) with `preserve_aspect_ratio: true` and re-centering (top +10, left +26) matched the sizing on the other two blocks on a prior production run. Iterate as needed.

---

### Phase 3F — Move design to the destination folder and re-export

```
mcp__claude_ai_Canva__move-item-to-folder(item_id: <working copy>, to_folder_id: "FAF-ADpbNnU")
mcp__claude_ai_Canva__export-design(design_id: <working copy>, format: {"type": "pdf", "size": "letter", "export_quality": "pro"})
```

If the operator makes manual spacing tweaks in Canva after the auto-build, ask before declaring done — and re-export to pick up the tweaks. The export returns a temporary download URL.

---

### Phase 3G — Download PDF to the client's Shared Drive

```bash
curl -sL "<export URL>" -o "/g/Shared drives/{Client legal name}/Perm File/Welcome Packet - {Client legal name}.pdf"
ls -la "/g/Shared drives/{Client legal name}/Perm File/Welcome Packet - {Client legal name}.pdf"
```

---

### Phase 3H — Render the welcome email and create the Gmail draft

Read `~/.claude/skills/onboard-client-admin/welcome-email-template.md`. Fill placeholders:

| Placeholder | Source |
|---|---|
| `{Client Name}` | FC display name |
| `{Greeting}` | "Good morning" / "Good afternoon" — from Phase 3A |
| `{Contact First Name}` | First name from FC primary contact |
| `{Onboarding}` | From **engagement letter** (not quote) |
| `{Cleanup Deposit}` | From engagement — adapt the line if the engagement bundles QBO setup or uses a flat fee instead of a range |
| `{Cleanup Deposit Date}` | The 20th of the month **prior** to the first monthly draft (e.g., monthly draft Aug 5 → cleanup deposit July 20). Spelled-out month + day. |
| `{Monthly}` | Monthly fee |
| `{Month}` | Spelled-out month monthly billing begins |
| `{Lead}` | Lead Accountant — first name only |
| `{Controller}` | Controller — first name only |
| `{Staff}` | Staff Accountant line — see the intern rule below |

**Staff Accountant line — intern vs. non-intern:**
- **If the Staff member is an intern:** name them (first name only) under "Your team" — e.g., `- Staff Accountant: Macie`. Do NOT write "to be determined." (Interns are identified per the Phase 1B intern mapping — Macie, Jenny, Kaitlyn, etc.)
- **If the Staff member is NOT an intern** (e.g., Joyce): keep the line **"to be determined (we'll confirm before monthly services begin)"** even though they're assigned internally and shown on the packet page 2 — that's intentional.

The email CC still includes the Staff member's Paxus email either way (for interns, `intern@paxuscpa.com`).

Recipients: TO primary contact email; CC Lead/Controller/Staff Paxus emails + `lisa@paxuscpa.com` (look up emails from the `paxus_team_emails` memory).

Produce **two** outputs — the live Gmail draft (primary deliverable) and a markdown archive in Perm File.

**1. Create the Gmail draft directly** via `mcp__claude_ai_Gmail__create_draft`:

```
mcp__claude_ai_Gmail__create_draft(
  to:      ["<primary contact email>"],
  cc:      ["<lead>@paxuscpa.com", "<controller>@paxuscpa.com", "<staff>@paxuscpa.com", "lisa@paxuscpa.com"],
  subject: "Welcome to Paxus, {Client Name}!",
  body:    "<rendered plain-text body — no subject/recipient lines, no sign-off>"
)
```

Rules for the draft (all verified against the tool):
- **Bare email addresses only.** The tool rejects the `Name <email>` format — pass plain addresses in the `to`/`cc` arrays.
- **Use `body` (plain text), not `htmlBody`.** Keeps it clean and matches Jennifer's paste-clean preference. Don't include the subject line or a `TO:/CC:` block inside the body — those are separate fields.
- **No sign-off or signature in the body** — Gmail's signature auto-appends (per `~/.claude/CLAUDE.md`). End on the warm closer line only.
- **Attachments are NOT supported by the draft tool** (confirmed — the `attachments` field no-ops). The welcome packet PDF cannot be attached programmatically. Flag this in the report so Jennifer attaches `Welcome Packet - {Client legal name}.pdf` from Perm File manually before sending.
- Capture the returned draft `id` for the report.
- If the Gmail MCP tool is unavailable (e.g., headless/cron run with no interactive auth), skip the draft, note it in the report, and rely on the markdown archive so Jennifer can paste manually.

**2. Archive the rendered email** — subject, recipients block, and body — to the **client's Shared Drive `Perm File\` alongside the welcome packet PDF** (the durable record; also the fallback if the draft can't be created):

```
/g/Shared drives/{Client legal name}/Perm File/Welcome Email - {Client legal name}.md
```

---

### Phase 3I — Report back

```
Phase 3 done — {Client name}'s welcome packet is ready.

  Canva design:  https://www.canva.com/design/{working copy ID}
  PDF filed:     /g/Shared drives/{Client legal name}/Perm File/Welcome Packet - {Client legal name}.pdf
  Gmail draft:   created in your Drafts (id {draft_id})
                 TO: {primary contact email}
                 CC: {Lead, Controller, Staff, Lisa}@paxuscpa.com
  Email archive: /g/Shared drives/{Client legal name}/Perm File/Welcome Email - {Client legal name}.md

Next: open the Canva design and skim for spacing/sizing. If tweaks needed, make them and I'll re-export.
Then open the Gmail draft, attach the welcome packet PDF (the draft tool can't attach it automatically), and send.

Still to do (manual, in FC UI):
  • Add {Lead}'s Clients, {Controller}'s Clients, and {Staff}'s Clients groups on the FC client dashboard.
    — FC API does not support attaching Groups to a client (verified 2026-07-01: PUT ignores `groups`, PATCH → 405,
      POST /clients/{id}/groups → 404, POST /groups/{id}/clients → 404). UI clicks only.
    — Open https://app.financial-cents.com/clients/{FC_CLIENT_ID} → Groups → add each staff-clients group.

After the welcome email goes out, run Phase 4 (Onboarding Prep Notes + team handoff email).
```

---

## Phase 4 — Onboarding Prep Notes + team handoff email

Run after Phase 3 (welcome email sent or queued). Produces the **Onboarding Prep Notes** — a clean, readable handoff file for the lead — from the engagement / consultation / memo, saves it to the client's `Perm File\`, and drafts the internal team handoff email. The prep notes are the record the lead works from going into the kickoff call; they live in the client's Perm File alongside every other permanent artifact.

### Important rules for Phase 4

- **Engagement is the source of truth on billing.** Re-read the engagement letter — the Phase 1 handoff figures may be quote-shaped (pre-signing) and the engagement often consolidates line items.
- **The signed engagement names the legal client. Period.** Pre-engagement consultation notes that mention related entities the principal owns are context, not contradictions. Do not flag "entity mismatches" or write parenthetical "(scope: SomeOtherEntity)" qualifiers.
- **Every field is either filled in or explicitly marked `TBD — ask on call`.** Never leave a field silently blank. A blank is ambiguous to the lead — there's no way to tell a genuine unknown from a not-yet-filled field. `TBD — ask on call` turns an unknown into a question for the kickoff, which is where it belongs.
- **Use Paxus role terms: Staff / Lead / Controller.** (The old Lead / Accountant / Reviewer labels only existed for the retired dashboard.)
- **Kickoff = the actual kickoff call date — NOT the cleanup start date.** Usually `TBD` (the Lead schedules it); use `TBD`, not the cleanup start.
- **Onboarding deadline** = the deadline from the quote timeline (e.g., `08/31/2026`), not a Paxus-internal deadline.

### Budgeted hours source (in flux — discovery notes first)

**We're moving toward carrying budgeted hours in the client's discovery notes, not necessarily on the Service Fee Template** (Jennifer, 2026-08-13). Look for hours in this order:

1. **Discovery notes** for the prospective client (the direction we're moving) — if they list Staff / Lead / Controller hours, use those.
2. **Service Fee Template**, only if it happens to carry them — READ-ONLY. The "Monthly Time for Budgets for Team" block (pink, fill `FFD5A6BD`): Full Service rows ~59–64, Basic rows ~67–72. Cell map for reference:

```python
from openpyxl import load_workbook
wb = load_workbook(r"G:\Shared drives\00 - Paxus CPA\Admin\Client Onboarding\Active Clients\{Legal name}\{Legal name} Service Fee.xlsx", data_only=True)
ws = wb["Monthly Accounting Services"]
# For Basic (rows 67–72): B68 = Staff hrs, B69 = Lead hrs, B70 = Controller hrs, B72 = total hrs
# For Full  (rows 59–64): B60 = Staff hrs, B61 = Lead hrs, B62 = Controller hrs, B64 = total hrs
```

3. **If no hours are available in either place, there are no hours to list.** Do NOT invent tier defaults. In the prep notes, mark budgeted hours `TBD — ask on call`; in the team handoff email, **leave the budgeted-hours sentence out entirely**.

**The Lead does not determine or refine budgeted hours** — never attribute the hours (or any "refinement" of them) to the Lead anywhere in Phase 4.

### One-time FC cleanup (do NOT repeat per client)

The old **"Sales Onboarding Service"** resource on the Client Onboarding project template pointed at the retired dashboard. **Remove it from the template** in the FC UI — it no longer points anywhere useful, and each client's Shared Drive is already linked on their client record via the Phase 2F "Google Drive" resource, so there's nothing to repoint it to. This is a one-time template cleanup; nothing per-client is needed.

---

### Phase 4A — Confirm preconditions and read source docs

Read these in parallel from `/g/Shared drives/00 - Paxus CPA/Admin/Client Onboarding/Active Clients/{Legal name}/`:

- `Engagement - {Legal name}.pdf` (authoritative billing)
- `Quote - *.pdf` (package + scope reference)
- `{Legal name} Service Fee.xlsx` — **authoritative per-client budgeted hours** (pink block on the Monthly Accounting Services tab) plus a lot of consultation-shaped data: gross revenue estimate, bank/CC count, transaction volume, 1099 count, Dext subscription, payroll flag. Read this before drafting the team email so hours and volumes are correct.
- `{Legal name} Potential New Client Review.docx` — the PNCR. **Note:** the source in Prospective is often a Google Doc (`.gdoc`); those pointer files are unreadable through the Drive-for-Desktop mount on Windows (byte-level reads return "Invalid request code"). If you only see a `.gdoc`, ask Jennifer to open the Google Doc → File → Download → Microsoft Word (.docx) → drop it into the Active Clients folder next to the other files. Then read the `.docx` (unzip → `word/document.xml` → strip `<w:t>` runs).
- `*Consultation*.pdf` (pain points, stakeholders, current setup — if present)
- `*Memo to File*.docx` (internal notes — if present)

Also pull from the Phase 1 handoff (FC ID, package, primary contact).

If any source is missing, ask — don't fabricate.

---

### Phase 4B — Produce the Onboarding Prep Notes

Write a clean, readable markdown handoff file to `/g/Shared drives/{Legal name}/Perm File/Onboarding Prep Notes - {Legal name}.md`. This is the lead's reference going into the kickoff — organize it for reading, top to bottom, not for pasting anywhere. Open with a one-line note that this is the lead's onboarding prep record for {Legal name}, kept in Perm File. **Every field is filled or explicitly marked `TBD — ask on call`** (see the Phase 4 rule) — never a silent blank.

**Header block:**

| Field | Value | Source |
|---|---|---|
| Client name | `{Legal name}` | Engagement / FC display name |
| Package / tier | `{Package}` | Engagement |
| Kickoff | `TBD` (or actual date if scheduled) | **Not the cleanup start date** |
| Onboarding deadline | e.g., `08/31/2026` | Quote timeline |
| Team of 3 — Lead | `{Lead first}` | Phase 3 handoff |
| Team of 3 — Staff | `{Staff first}` | Phase 3 handoff |
| Team of 3 — Controller | `{Controller first}` | Phase 3 handoff |

**Billing** (pull from the **engagement**, not the quote — the engagement often consolidates line items):

| Field | Value | Source |
|---|---|---|
| Monthly fee | `${monthly}/month` | Engagement |
| First monthly draft date | `{date}` or `TBD — ask on call` | Engagement / Phase 1 handoff |
| Onboarding fee | `${onboarding}` (paid at signing) | Engagement |
| Cleanup deposit | `${deposit}` (drafted when cleanup begins) | Engagement |
| Cleanup balance | `${balance}` (due on completion) | Engagement |

**Budgeted hours** — list Staff / Lead / Controller + total if available (see the *Budgeted hours source* section above — discovery notes first, Service Fee Template only if it carries them). If no hours are available, mark this `TBD — ask on call`. Do NOT invent tier defaults, and do NOT say the Lead determines or refines them.

**Cleanup scope** — in one place: what the cleanup covers (period / months, catch-up reconciliations, COA cleanup, prior-year work), the floor/ceiling or flat fee, and any client-specific scope from the quote/engagement. Mark `TBD — ask on call` for anything not yet known.

**Volumes & complexity** — in one place, mostly from the Service Fee Template:

- # bank & credit-card accounts
- Monthly transaction volume — *usually missing from the Service Fee Template; mark `TBD — ask on call` if not found*
- 1099 count — *usually missing; mark `TBD — ask on call` if not found*
- Dext subscription: `Yes / No`
- Payroll: `Yes ({vendor}) / No — out of scope`
- Entities in scope: `{list}`

**Discovery** (free-text fields):

| Field | Value | Source |
|---|---|---|
| HOW THEY HEARD ABOUT US | referral source | Consultation / memo |
| ENTITY TYPE | `LLC`, `Nonprofit — files 990. Fiscal year end M/D.`, `Sole Prop`, etc. | Engagement / memo |
| # PARTNERS / TEAM | Owners/partners + employee count | Consultation |
| TAX RETURNS CURRENT? | `TBD` or `Yes through {year}` | Consultation / memo |
| ACCOUNTING SOFTWARE | QBO / Quicken / Xero + one-line status | Consultation |
| PAYROLL COMPANY | Vendor name or `None` — flag if Paxus is/isn't running it | Consultation |
| CURRENT CPA | External tax accountant + note if we need contact permission | Consultation |
| SERVICES REQUESTED | Package tier + one-line scope summary | Engagement |
| PAIN POINTS & PRIORITIES DURING ONBOARDING | Verbatim pain points + numbered priority list | Consultation + memo |

**Pre-Kickoff Readiness** — note the current state next to each item so the Lead knows where things stand going in:

Under ACCOUNTING · QBO:
- `Do they have a QBO file?` — YES / NO
- `Do we have access?` — YES / NOT YET (obtain during/after kickoff)
- `Chart of accounts reviewed — needs cleanup` — YES + brief note, or N/A
- `Client OK with us cleaning up the COA?` — TBD (confirm on kickoff) or YES
- `Bank & card feeds connected?` — YES / NO + note if there are mapping errors
- `How caught up is the file?` — plain-text status (e.g., "Behind — last rec 3/31; April–June open")

Under TAX:
- `Prior-year returns — which years?` — years received or `TBD`
- `EIN on file` — YES/NO/TBD
- `Tax returns current?` — YES/NO/TBD

Under PAYROLL:
- `Are we running payroll?` — YES/NO (usually NO — out of scope)
- `If not, how do we gain access?` — vendor name if we ever need read access, or `N/A`

Under SALES TAX & PORTAL:
- `Sales tax handled?` — YES/NO/N/A
- `Current services confirmed` — one-line scope confirmation
- `Portal access — who is authorized? (2FA)` — comma-separated names + roles
- `Next steps assigned` — Lead completes post-kickoff

**Kickoff Call reference notes** — the 11-item call agenda; the Lead works through these live during the call:

Pre-load only item **06 Gather information** — a bulleted reference list of what to ask the client during the call (EIN, board contacts, prior return, credentials list, loans/assets, portal authorization, 2FA setup, etc.).

Items 01/02/03/04/05/07/08/09/10/11 need no pre-fill — they're the Lead's live agenda.

**Save the prep notes:**

```
/g/Shared drives/{Legal name}/Perm File/Onboarding Prep Notes - {Legal name}.md
```

No dashboard, no pasting — the lead reads the file straight through. Close with a *Reference files* section listing the paths to the engagement, quote, Service Fee Template, PNCR, welcome packet, and welcome email draft.

---

### Phase 4C — Draft the team handoff email

Use the body structure that replaces Jennifer's previous template — same information, less list-y. **Formatting: plain text only.** No `**bold**`, no `<b><u>...</u></b>`, no other markup — Jennifer copies straight from the file into Gmail, and any inline formatting tags come through as literal characters that she has to strip. Section headers are just plain-text lines (dash bullets, numbered lists, blank lines for separation). See `feedback_email_formatting.md` for the durable rule.

Save to the **client's Shared Drive `Perm File\` alongside the other permanent artifacts**:

```
/g/Shared drives/{Legal name}/Perm File/Team Handoff Email - {Legal name}.md
```

Before drafting, pull the primary contact's email + phone fresh from FC (`GET /clients/{FC_CLIENT_ID}`) so the email carries the real contact details, not TBDs.

**Subject:** `New client: {Legal name} — kickoff & key details`

**Recipients:**
- TO: `lisa@paxuscpa.com` + the 3 assigned team members (from `paxus_team_emails` memory)
- Optional CC: rest of the staff group for firm-wide visibility

**Body sections (in order):**

1. **Opener** — one paragraph: signed + paid + scope summary + key stakeholders (primary contact, helpers if relevant). Start "Good morning, friends!"
2. **Who's involved** — primary contact (name, email, phone), helpers (nephew/assistant/etc.), external tax accountant. Mention portal-dashboard pointer.
3. **Billing** — onboarding paid; cleanup deposit + balance amounts (from engagement); monthly draft amount + start date.
4. **Scope** — tier, what's in/out, cleanup window, first monthly month, software transition notes (e.g., Quicken → QBO).
5. **Your team and budgeted hours** — Controller / Lead / Staff. If budgeted hours are available (discovery notes first, Service Fee Template only if it carries them — see the *Budgeted hours source* section), list them. **If there are no hours to list, leave the budgeted-hours sentence out of the email entirely** — do NOT write TBD and do NOT invent tier defaults (Jennifer's rule 2026-08-13). Never say the Lead determines or refines the hours. Flag that Staff stays TBD client-facing (unless Staff is an intern — then name them, per Phase 3H).
6. **Action items** — Lead schedules kick-off; point the Lead at the **Onboarding Prep Notes** saved in the client's Perm File (`Onboarding Prep Notes - {Legal name}.md`) as the record to work from going into the call; what to confirm on the call. Do NOT reference the retired Sales Onboarding dashboard, a raw claude.ai/design URL, or any "Sales Onboarding …xlsx" worksheet.
7. **Things to know going in** — pain points, complex transactions, system quirks (e.g., check-printing needs), access gaps, FC checklist status, tax-return status.
8. **One-line close:** "Let me know if anything is unclear — happy to chase down any of the TBDs."

**Always verify before writing:**
- Billing numbers match the engagement letter (not the quote).
- Staff Accountant assignment is shown internally but kept TBD client-facing.
- No "(scope: SomeOtherEntity)" qualifiers anywhere.

**Create the Gmail draft directly (primary deliverable).** After rendering the body and saving the markdown archive to Perm File, create the draft in Jennifer's Gmail via `mcp__claude_ai_Gmail__create_draft` — same mechanics as Phase 3H:

```
mcp__claude_ai_Gmail__create_draft(
  to:      ["lisa@paxuscpa.com", "<lead>@paxuscpa.com", "<controller>@paxuscpa.com"],   # add "<staff>@paxuscpa.com" once Staff is named
  cc:      [],                     # optional: rest of the staff group for firm-wide visibility
  subject: "New client: {Legal name} — kickoff & key details",
  body:    "<rendered plain-text body — starts 'Good morning, friends!'; no Subject or TO/CC lines inside the body>"
)
```

- **Bare email addresses only** (the tool rejects `Name <email>`), **`body` as plain text** (not `htmlBody`), and **no sign-off/signature** — Gmail auto-appends it. Same rules as Phase 3H.
- Resolve team emails from the `paxus_team_emails` memory. Omit any TBD role from `to` (e.g., Staff not yet named) rather than passing a literal "TBD" address.
- The draft tool can't add attachments — none are needed for this email.
- Capture the returned draft `id` for the Phase 4D report.
- If the Gmail MCP tool is unavailable (headless/cron run), skip the draft, note it in the report, and rely on the markdown archive so Jennifer can paste manually.

---

### Phase 4D — Update the handoff doc and report back

Append a `## Phase 4 completed {YYYY-MM-DD}` section to the **main handoff at `/g/Shared drives/{Legal name}/Perm File/Onboarding Handoff - {Legal name}.md`** (created/moved into Perm File in Phase 2G) with:
- Onboarding Prep Notes file path (`Onboarding Prep Notes - {Legal name}.md`)
- Team handoff email: Gmail draft id + Perm File markdown archive path
- Suggested recipients and subject

Report:

```
Phase 4 done — kickoff materials ready.

  Prep notes:          G:\Shared drives\{Legal name}\Perm File\Onboarding Prep Notes - {Legal name}.md
  Team email:          Gmail draft created in your Drafts (id {draft_id})
                       TO: lisa@ + {Lead}@ + {Controller}@paxuscpa.com  (Staff added once named)
  Email archive:       G:\Shared drives\{Legal name}\Perm File\Team Handoff Email - {Legal name}.md

Still to do (manual):
  • Send the team handoff email after the welcome email has gone out.
```

End warmly — e.g., "All set — {Legal name} is fully launched."

---

## Phase 5 — Kickoff Prep Email

Run **the day before** the client's kickoff call. Drafts a client-facing email that:
- Reminds the client of the meeting time and who they'll meet with.
- Thanks them for what they've already provided to the portal.
- Lists the items still outstanding on the FC Client's Onboarding Checklist.
- Confirms the Lead is their primary contact going forward.

### Important rules for Phase 5

- **FC DOES expose client-facing checklist items — via `GET /api/v1/client-tasks` (hyphenated).** Discovered 2026-07-20. This endpoint returns every client task across all projects, each with `title`, `is_completed`, `completed_at`, `index`, and a nested `project` object. The `?project_id=` query filter is **ignored** (returns everything), so paginate `?per_page=100` following `links.next` and filter client-side on `project.id == <the client's Client's Onboarding Checklist project id>`. Get that project id by scanning `GET /projects?per_page=100` (paginate) for `client.id == FC_CLIENT_ID` and `title == "Client's Onboarding Checklist"`. Outstanding items = those with `is_completed == false`. (The old dead-ends still 404: `/client_tasks` underscore, `/projects/{id}/client_tasks`, `/tasks?type=client`, `?include=client_tasks`. Use the hyphenated top-level route.) Only fall back to operator-paste if the endpoint returns nothing.
- **No Google Calendar access.** Environment has no Calendar OAuth; operator pastes the date/time.
- **Plain text only.** Same rule as every other email — no markdown asterisks, no `<b>`/`<u>` tags. Jennifer copies straight into Gmail.
- **Lead's first name comes from the Perm-File handoff doc**, not from FC. Team-role assignments live only in `Onboarding Handoff - {Legal name}.md` (captured during Phase 3).

### Phase 5A — Recover context and gather inputs

Read the Perm-File handoff at `/g/Shared drives/{Legal name}/Perm File/Onboarding Handoff - {Legal name}.md` to recover:
- FC client ID
- Client legal name
- Lead's first name (from the Phase 3 team-block section)

Query FC for the primary-contact record:

```bash
TOKEN=$(cat "C:/Users/paxus/.paxus/client onboarding.txt" | tr -d '\n\r' | tr -d ' ')
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://app.financial-cents.com/api/v1/clients/<FC_CLIENT_ID>" \
  | python -c "import sys,json;d=json.loads(sys.stdin.read());[print(c['id'],c['name'],c.get('email'),c.get('notes')) for c in d.get('contacts',[])]"
```

Ask the operator (one batched message — skip the ones the handoff already answered):

1. **Kickoff date and time** — paste from Google Calendar (e.g., `Tuesday, July 15 at 2:00 PM`).
2. **What's been received so far** — one short line (e.g., `the bank statements, prior 990, and QBO login`). Leave blank if nothing yet.
3. **Outstanding items** — pull these live from FC via `GET /api/v1/client-tasks` (see the Phase 5 rule above): find the client's "Client's Onboarding Checklist" project id, then list the client tasks on it where `is_completed == false`. Only ask the operator to paste if the endpoint returns nothing.
4. **Primary contact** — if the client has multiple FC contacts (e.g., President + Treasurer), confirm which one gets the TO line. Default to the treasurer / original consultation contact — that's usually the day-to-day.
5. **Send-time greeting** — default "Good afternoon" per Jennifer's template. Override only if she says otherwise.

### Phase 5B — Render the email

Write to `/g/Shared drives/{Legal name}/Perm File/Kickoff Prep Email - {Legal name}.md` and mirror to `~/.claude/skills/onboard-client-admin/handoffs/{slug}-{YYYY-MM-DD}-kickoff-prep-email.md`.

**Template (plain text — no markdown, no HTML):**

```
Subject: Kickoff call tomorrow — {Client Name}

{Greeting} {Contact First Name},

The kickoff call for {Client Name} is scheduled for {Kickoff Date/Time} with {Lead}. You should have received a calendar invitation containing the Google Meet link.

Thank you for setting up the client portal. We have received all requested information to date{received-clause}. To complete your file, please provide the following additional documents:

{outstanding items — one per line, prefixed with "- "}

{Lead} will be your primary contact moving forward, though please feel free to reach out to me with any administrative questions.
```

**Fill rules:**

| Placeholder | Fill from |
|---|---|
| `{Greeting}` | Operator's send-time answer ("Good morning" / "Good afternoon"). Default `Good afternoon`. |
| `{Contact First Name}` | First token of the confirmed primary contact's `name` in FC. |
| `{Client Name}` | FC client `display_name`. |
| `{Kickoff Date/Time}` | Operator paste. |
| `{Lead}` | First name only, from the handoff doc. |
| `{received-clause}` | If the operator supplied a "received so far" line: `, and {received}`. Otherwise omit the clause entirely (period after `date`). |
| `{outstanding items}` | Operator paste, one per line, each prefixed with `- `. |

**Create the Gmail draft directly (primary deliverable).** After rendering the email and saving the markdown archive, create the draft in Jennifer's Gmail via `mcp__claude_ai_Gmail__create_draft`:

```
mcp__claude_ai_Gmail__create_draft(
  to:      ["<primary contact email>"],
  cc:      [],                 # client-facing email — CC the internal team only if Jennifer asks
  subject: "Kickoff call tomorrow — {Client Name}",
  body:    "<rendered plain-text body — the greeting line through the closing paragraph; no Subject line inside the body>"
)
```

- **Bare addresses only**, **`body` as plain text** (not `htmlBody`), **no sign-off/signature** (Gmail auto-appends). Same rules as Phase 3H / 4C.
- The `Subject:` line in the template above is the `subject` field — do NOT include it inside `body`.
- Capture the returned draft `id` for the Phase 5C report.
- If the Gmail MCP tool is unavailable, skip the draft, note it, and rely on the markdown archive.

### Phase 5C — Report back

```
Phase 5 done — kickoff prep email drafted in your Gmail.

  Gmail draft:   created in your Drafts (id {draft_id})
                 TO: {primary contact email}
  Email archive: /g/Shared drives/{Legal name}/Perm File/Kickoff Prep Email - {Legal name}.md

Open the draft and send. This is a client-facing email — CC the internal team if you want them looped in.
```

---

## Legacy note (recurring FC projects)

**Skill work — split across phases by signing gate.** As of 2026-07-08, recurring project attachment moved out of Phase 1 and into Phase 2 (post-signing). Rationale: attaching operational recurring projects (weekly bookkeeping, cleanup, tax returns, etc.) to a prospect who hasn't signed clutters the FC record and creates cleanup work if they don't sign — FC has no API to delete a stray project, so closures are UI-only. The skill only POSTs the New Client Onboarding project itself in Phase 1 (its Firm Admin Tasks belong pre-signing).

- **Phase 1E** POSTs the Client Onboarding project only. Client's Onboarding Checklist (`9685085`) is created by an FC automation when Jennifer completes the triggering task — the skill never POSTs it.
- **Phase 2H** POSTs the 8 standard templates (Weekly Bookkeeping Tasks `5082639`, Month-End Review `5082645`, Month-End Close `5110296`, Client - Cleanup `8266589`, Client - Post Cleanup `13989492`, Client - Kick-Off Call `13565957`, Employee - Client Training Manual `7995444`, Tax Returns `7959692`) and reassigns tasks by role.
- **Phase 2I** POSTs the 1099 templates when the package is Full Service or Premium Service.

As of 2026-07-03 the skill POSTs these templates explicitly rather than relying on the FC template's auto-attach — that auto-attach became unreliable after the New Client Onboarding template was edited to strip 1099 auto-attach (a 2026-07-03 regression). If future FC template edits break something else, add it to the Phase 2H/2I loops the same way.

---

## Known API constraints (reference)

Confirmed 2026-06-24/25:

**Supported (FC v1):**
- `POST /clients` — only required field is `display_name`.
- `POST /clients/{id}/contacts` — fields: `name`, `email`, `phone`, `mobile`, `address`, `notes`. Only `name` required.
- `POST /templates/{template_id}/projects` — send `{"client_id":<id>}` to attach. Section-to-user assignments inherit from the template.
- `POST /clients/{id}/resources` — body `{"label":"...","url":"..."}`. Used in Phase 2 to attach the Shared Drive link. **Verified 2026-07-01** (HTTP 201, returned `id`, `client_id`, `label`, `url`, `list_index`, `created_at`, `updated_at`). Check for existing "Google Drive" label via GET before POSTing to avoid duplicates.
- `POST /clients/{id}/attachments/folders` — body `{"name":"..."}`. Creates a folder in FC's Files tab. Verified 2026-07-01. No visibility/contact fields honored — FC UI toggle needed for per-folder sharing if the default (visible to primary contact) doesn't apply.
- `POST /clients/{id}/attachments` — multipart form-data upload; requires `file`, accepts optional `parent_id` to nest. Verified 2026-07-01. Same visibility caveat.
- `DELETE /clients/{id}/attachments/{attachment_id}` — deletes files or folders; returns HTTP 201 with empty body. Verified 2026-07-01.
- `GET /projects` — supports `per_page` up to at least 100; filter client-side via `client.id`. Verified 2026-07-01.
- `GET /projects/{id}` — returns full project record. Verified 2026-07-01. (Contradicts an earlier probe finding — endpoint IS supported.)
- `GET /projects/{id}/resources` — returns the project's Resources section (each with `id`, `project_id`, `label`, `url`, `list_index`, `type`). Verified 2026-07-01.
- `POST /projects/{id}/resources` — body `{"label":"...","url":"..."}`. Creates a new resource on the project. `list_index` in the body is ignored — FC auto-assigns. Verified 2026-07-01.
- `DELETE /projects/{id}/resources/{resource_id}` — deletes; returns HTTP 202. Verified 2026-07-01.
- `PATCH`/`PUT` on `/projects/{id}/resources/{id}` → 405; only DELETE is supported for individual resources.
- `PUT /clients/{id}` — accepts `display_name` and nested `contacts` array.
- `DELETE /clients/{id}`, `DELETE /contacts/{id}`.
- `GET /clients`, `GET /clients/{id}`, `GET /contacts`, `GET /clients/{id}/resources`, `GET /clients/{id}/notes`, `GET /clients/{id}/attachments`, `GET /invoices`, `GET /users`, `GET /templates`, `GET /tasks?project_id={id}` — read-only.

**Not supported (FC UI only):**
- `POST /contacts` (unscoped) → 405. Use nested `/clients/{id}/contacts`.
- `POST /projects` (unscoped) → 405. Use `POST /templates/{template_id}/projects`.
- `POST /clients/{id}/projects` → 404.
- `GET`/`PUT`/`DELETE /projects/{id}` → all 404. Projects must be modified/closed in the FC UI; stray projects (body `{}` without client_id) must be cleaned up manually.
- `POST /invoices` → 405. Recurring invoices/billing in FC UI.
- Proposals, engagements, agreements, billing-subscriptions — all 404. Proposals exist internally (referenced as `proposal_id` on invoices) but no CRUD endpoint.

**Conventions:**
- Base URL: `https://app.financial-cents.com/api/v1`
- Auth: `Authorization: Bearer <token>`
- Money in API responses is in **cents** (e.g., `220000` = $2,200.00).

If FC expands the public API to expose proposals or invoices, update Phase 1F/G and shrink the handoff accordingly.

---

## Reference files in this skill folder

| File | Purpose |
|---|---|
| `SKILL.md` | This file — operational instructions |
| `welcome-email-template.md` | Approved warm/concise client welcome email |
| `handoffs/` | Per-client artifacts (proposal, welcome email draft, team email draft) |
