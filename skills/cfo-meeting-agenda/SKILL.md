---
name: cfo-meeting-agenda
description: Prep the agenda for a recurring CFO/advisory client meeting. Covers both standing monthly meetings these clients hold — the Financials + Forecast statement meeting, and the separate Process Improvement meeting — as two strictly separate paths chosen up front, never mixed. Pulls the client's prior agenda, latest financials, forecast workbook, process-improvement backlog, and prior meeting notes from the client's shared drive, verifies which prior action items actually landed, and drafts the new agenda in that client's own established format. Reads the client's agenda-spec.md for its meeting cadence, agenda-file location, and layout; builds the spec on a cold start. Use when someone says "prep the agenda for <client>", "financials meeting agenda", "process improvement agenda", "build the monthly agenda", or similar. SCOPED TO THE AGENDA — it does not update the forecast workbook or build the dashboard.
---

# CFO Meeting Agenda

Preps the agenda for a recurring CFO/advisory client meeting and hands the operator a draft to review.

These clients hold **two different standing monthly meetings**, and they are not interchangeable:

| Meeting | What it covers | Who attends |
|---|---|---|
| **Financials + Forecast** | Statement review, YTD-vs-PY, forecast walk-through | Client finance/leadership + Paxus |
| **Process Improvement** | Standing improvement backlog, operational projects | Often a wider client staff group |

Different agenda file. Different cadence. Different attendees. Different prior notes.
**Mixing them is the single biggest failure mode of this skill.** Everything below is built to prevent it.

---

## Step 0 — Pick the meeting. Never infer it.

**Ask which meeting this is, out loud, before anything else — unless the operator already named it
explicitly** ("prep the *process improvement* agenda for X"). A client name alone is never enough.

Do not guess from the date, from what was run last month, from which file you happened to find first, or
from the operator's calendar. If the request is ambiguous, ask a one-line question and wait:

> "Financials + Forecast, or Process Improvement?"

Once chosen, **that choice scopes every read that follows.** When gathering prior meeting notes:

- On the **Financials** path, skip every file whose name contains "Process Improvement."
- On the **Process Improvement** path, skip every file whose name contains "Financial Statement,"
  "Forecast," or "Financials."

Some clients keep these in sibling subfolders with near-identical names. Read the folder name, not just
the file name.

---

## Step 1 — Find the client's agenda spec

The spec records this client's cadence, attendees, agenda-file IDs, layout, and watch-outs **for each of
the two meetings**. It is what makes month 2 fast and what lets any teammate run this.

**Where the spec lives (canonical location, in this order of precedence):**

| Client drive shape | Canonical spec location |
|---|---|
| Drive has a `.agents/` context bundle (built by `/paxus-skills:client-context`) | `.agents/b-engagement/agenda-spec.md` |
| Single-entity drive, no bundle | `Perm File/agenda-spec.md` at the drive root |
| Multi-entity drive (one folder per entity at the root) | `<Entity folder>/Perm File/agenda-spec.md` |

The file is always named exactly `agenda-spec.md`. It never goes in `Financials/`, a year folder,
`Meeting Notes`, `CFO Work`, `Special Projects`, or Cowork's default `Claude outputs` folder — **always
name the destination folder explicitly when saving**, or Cowork will drop it in `Claude outputs`.

**Finding it on a repeat run:** search the client's drive for a file named `agenda-spec.md` (gws:
`name = 'agenda-spec.md'` with `corpora:"drive"` scoped to the client's `driveId`; Cowork: search the
connected client folder). Then:

- **One file, in the canonical folder** → that's the spec. Read it.
- **One file, in the wrong folder** → it's still the spec; *move* it (don't copy) to the canonical folder
  and tell the operator you did.
- **Two or more files** → the newest is operative. Move the others to the canonical folder renamed
  `agenda-spec-superseded-YYYY-MM-DD.md` (their modified date) and tell the operator.
- **None** → cold start. Build the spec from the client's existing agenda file as you go (Step 5), so the
  next run has one.

A copy on someone's laptop is an **optional local cache only** — unreachable from Cowork and from every
other teammate's machine. If a laptop copy and the Drive copy differ, **Drive wins.**

---

## Step 2 — Drive access

**Two environments, one rule: use whatever Drive access the session already has.**

- **Claude Code on macOS:** the local Google Drive path is sandbox-blocked (`Operation not permitted`) —
  **always use the gws CLI**, never the local `CloudStorage` path.
- **Cowork (Windows or Mac):** there is no gws. The client's shared drive is a *connected folder* (e.g.
  `G:\Shared drives\<Client>\`). Read straight from it and save outputs back by explicit folder path.
  Record the connected-folder path in the spec alongside the Drive IDs.

Every gws Drive call needs `corpora:"drive"`, `driveId`, `includeItemsFromAllDrives:true`,
`supportsAllDrives:true`. Pass `--params` JSON via a heredoc file when the query contains a folder ID, to
avoid shell-quote breakage.

**Resolve folder IDs once, then store them in the spec.** Drive has many same-named folders across clients
("Financials", "Meeting Notes", "2026"), so blind `name contains` searches are ambiguous. On a repeat run,
read the IDs from the spec and skip discovery. When several same-named folders appear, disambiguate by
parent chain — don't guess.

Everything in Steps 1–3 is a **read**. The only write this skill ever makes is the agenda itself, and only
after Step 5 approval.

---

## Step 3A — Financials + Forecast path

Pull these (skip any the client doesn't have — not every client has all four):

1. **Newest monthly financials PDF**, plus the **dashboard** and **board packet** PDFs if the client gets
   them separately. Download with `alt:media`, then read.
2. **Prior financials-meeting notes** — the newest "Notes by Gemini" Doc in the financials meeting-notes
   folder that is *not* a Process Improvement note. Export `text/plain`.
3. **Latest forecast workbook** (`.xlsx`) — parse with python/openpyxl. Typical sheets: a full-year
   budget-vs-forecast analysis sheet, a month-by-month rolling forecast, and a summary sheet.
   **The summary sheet's headline numbers refresh but its narrative text often lags a month — flag it if
   stale rather than repeating last month's story.** If the client has no forecast, skip the forecast half.
4. **The running agenda Doc** (if the client keeps one) — export `text/plain` for the exact format and for
   open follow-ups. Some clients have no running doc and instead keep each month as its own notes file;
   in that case model the new agenda on the newest prior note.

**Draft in the client's established style:**

- Dated header in the client's format (e.g. `<Mon DD, YYYY> | <Client>/Paxus Financial Statement Meeting`).
- A **Financials** section, then a **Forecast** section.
- Conversational bullets that **pose questions**, with room to nest the client's answers underneath — that
  is how these calls are actually run. Not a report; a set of prompts.
- Default lens: **YTD-vs-PY board view with current-month callouts.**
- Weave in open follow-ups from the prior **financials** meeting. Leave process-improvement items out.
- Close with an **Action Items** table: **Owner / Description / Due Date**.
- **Round all dollar amounts to the nearest hundred.** No cents.

---

## Step 3B — Process Improvement path

This meeting runs off a **standing backlog** plus a **per-meeting agenda**, and the prep is as much
verification as it is drafting.

### 1. Read the master backlog in full

The backlog is the source of truth for what's open, who owns it, and what's changed. Typical columns:

`Priority Level | Process | <Client> Owner | Paxus Owner | Status | Details/Notes | Ideas`

Status values in common use: `Complete`, `In progress`, `Not Started`, `Blocked`.

> **Always read the `Ideas` / `Details-Notes` columns, not just the last meeting tab.** People type real
> answers into those cells that never make it into any meeting note — a vendor's reply, a resolved
> question, a decision. Skipping them is how an already-answered item gets re-raised at the meeting.

Column headers are sometimes mislabeled from a copy-pasted template (a client-owner column carrying
another client's name). Read the column by position and content, not by its header text.

### 2. Read the last two meeting tabs

Not just the last one. The two-tab window is what reveals items that have been carried twice and are
actually stuck rather than merely open.

### 3. Verify which prior action items actually happened — don't assume

**This is the step that earns the prep.** Take the prior meeting's action items and check them against
reality before writing "carried forward":

- Search **Gmail** for the deliverable or the thread it would have arrived on.
- Check the backlog's Status and Ideas columns for a quiet update.
- Check the client's drive for a file that was promised.

Client-promised pre-work in particular is worth verifying every single time. An item can sit "In progress"
for two meetings while the thing it was waiting on never arrived — and the agenda should say so plainly
rather than repeating the ask a third time as though it were new.

Report what you verified and what you couldn't. Never assert an item is done without a source.

### 4. Draft the new meeting agenda

In the client's own per-meeting format (Step 4 has the two shapes). Typical run of sections:

- **Meeting Attendees**
- **Agenda** — numbered topics, sub-bullets underneath each, with space for participants' pre-meeting
  replies where the client uses that convention
- **Notes:** — topic labels with room for live narrative
- **Action Items** — Owner / Description / Due Date (with a checkbox column where the client uses one)
- **Things to Watch** / **Carry into next meeting** — carryover lines

Order topics by the backlog's priority and by what's genuinely live, not by backlog row order.

---

## Step 4 — Write the agenda into the client's file

Two file shapes. The spec says which one this client uses. **They behave very differently.**

### Shape A — Google **Doc**, one tab per meeting

- Tabs are Docs-native tabs, usually titled `MM.DD.YYYY <Meeting Name>`, one per meeting.
- `docs.documents.get` **hides tabs by default** — pass `includeTabsContent:true`, and give every
  batchUpdate `Location`/`Range` its `tabId`.
- **The Docs API cannot create a tab.** There is no `createTab` request. The operator creates the blank
  tab in the UI first, names it, and hands back the tabId; only then can you populate it. Plan the handoff —
  don't plan to script it.
- Typical per-meeting layout: event/participants lines → a topics heading → a table
  (`# | Topic | Last Status | Ask Today | Owner`) → an action-items heading → a table
  (`Owner | Description | Due Date`). Header rows and section-divider rows are **bold**.
- **Font trap:** text inserted via the API takes the tab's default font, which is often a display font at
  12pt, while the existing tables are a plain font at ~10.5pt — the new month visibly doesn't match.
  After inserting cell text, restyle it with `updateTextStyle`
  (`weightedFontFamily={fontFamily:"<doc's table font>", weight:400}` plus the correct `fontSize`).
  **Apply bold LAST** — a font restyle can drop bold.
- Building a populated table: `insertTable` (empty) → re-fetch the doc to read each cell's
  `content[0].startIndex` → insert cell text in **descending index order** so earlier insertions don't
  invalidate later positions.

### Shape B — Google **Sheet**, master backlog tab + one tab per meeting

- **The Sheets API *can* create tabs** — `addSheet` in `spreadsheets.batchUpdate`. This is the opposite of
  Docs, so a Sheet-shaped agenda builds end to end in one pass:
  `addSheet` → `values.update` → `batchUpdate` formatting.
- Per-meeting tabs are titled `MM.DD.YYYY Meeting` (older ones may use `MM/DD/YYYY` — match the newest).
- Build a `{row: {col: value}}` map plus a list of cells to bold, emit a ragged 2D array, write from A1.
- **Apply the blanket font/size `repeatCell` FIRST and the per-cell bold LAST** — the blanket format clears
  bold if applied after.
- Match the client's column widths and font size from the prior meeting tab; the spec records them.

---

## Step 5 — Review, deliver, persist

**Show the draft to the operator before it touches the client's file.** Every time. Delivery mode is
per-client and recorded in the spec:

| Mode | When | What you do |
|---|---|---|
| **Draft for paste** (default) | Operator maintains the running doc themselves | Deliver the agenda in-conversation, formatted for paste. Do not write to the file. |
| **Write after approval** | Client's file is a Sheet the operator has asked you to populate | Show the draft, get an explicit go-ahead, then write it. |

Writing into a client's live agenda file is visible to the client. **Confirm before every write, name the
file and tab you're writing to, and never batch the write with other work.** Approval to write one month's
tab is not approval for the next.

Then persist:

1. **Save or update `agenda-spec.md`** at the canonical location (Step 1 table), recording — for *each*
   meeting type — the cadence and usual day, attendees, the agenda file's ID and shape (A or B), the
   meeting-notes folder ID (and which sibling folder to skip), the financials/forecast folder IDs and file
   name patterns, the layout, column widths and fonts, delivery mode, and recurring watch-outs.
2. Note anything you verified in Step 3B.3 that changed a backlog item's real status, so it isn't
   re-verified from scratch next month.

---

## Cold start — a client with no spec yet

1. Confirm which two meetings this client actually holds. Not every client has both.
2. Find each meeting's agenda file and identify its shape (Doc-with-tabs or Sheet-with-tabs).
3. Read the **two most recent** meeting entries to recover the layout, the section order, the fonts and
   column widths, and the action-item conventions. The client's own prior meetings are the format spec —
   never import another client's layout.
4. Confirm attendees and cadence with the operator.
5. Resolve and record the Drive IDs.
6. Draft the first agenda, get it reviewed, then save `agenda-spec.md`.

---

## Important rules (always follow)

- **Meeting type is chosen explicitly at Step 0, never inferred.** Ask if there's any doubt.
- **Never mix the two meetings' files, notes, or open items.** Filter by folder and by file name.
- **Never use one client's agenda as a template for another.** Each client's own prior meetings are its
  spec. Client data never travels between clients, and never goes into this skill file.
- **Read the backlog's Ideas/Notes columns before drafting** — they hold answers the meeting notes missed.
- **Verify prior action items against Gmail and the drive before calling anything carried forward.**
- **No fabrication.** Every figure traces to the actual statements or forecast workbook. Every status
  claim traces to a source. If you couldn't verify something, say so in the draft.
- **Round all dollar amounts to the nearest hundred.**
- **Action items always carry Owner / Description / Due Date.**
- Auto-generated meeting notes (Gemini and similar) are **imprecise on timing and attribution.** Verify
  with the operator before asserting a number, a date, or who committed to what.
- **Confirm before any write to a client file.** Reads need no confirmation; writes always do.
- On macOS Claude Code use gws, never the local CloudStorage path.

---

## Scope

This skill produces **the agenda**. It does not:

- update the forecast workbook — that's a separate forecasting pass
- build the monthly dashboard or board package — that's `/paxus-skills:monthly-dashboard`
- draft the monthly client email
