---
name: onboard-project
description: Scaffold a new project under an existing Paxus client. Creates ~/paxus-ai/clients/{client}/projects/{project}/ with CLAUDE.md, STATUS.md, and the standard subfolders (inputs/, deliverables/, notes/). Run after /client-context when you're ready to start a specific piece of work — monthly close, board package, advisory engagement, tax filing, SOP, dashboard build, or ad-hoc analysis.
---

# /onboard-project — Paxus Project Onboarding Skill

You are setting up a new project folder under an existing client in the operator's `~/paxus-ai/clients/{client}/projects/` workstation. Follow the five phases below in order. Be conversational and warm — match the Paxus voice from the firm rules.

## Important rules for this skill

- **No fabrication.** If the operator doesn't know the answer, write `[TBD — operator to fill]` in the generated file. Never invent details.
- **Slug discipline.** Derive the project slug from the project name using these rules in order:
  1. Lowercase everything
  2. Strip apostrophes, quotes, parentheses, and other punctuation entirely
  3. Replace any remaining non-alphanumeric character with a single dash
  4. Collapse consecutive dashes into one, trim leading/trailing dashes
  5. If the result is empty or starts with a digit, prepend `project-`
  Show the operator the derived slug and ask "Use `{slug}`, or want a different one?" before creating anything.
- **Client must exist first.** If no matching client folder exists in `~/paxus-ai/clients/`, stop and tell the operator: "I don't see any clients yet. Run `/client-context` first to bring your client in, then come back to `/onboard-project`."
- **Slug collisions.** If `~/paxus-ai/clients/{client-slug}/projects/{project-slug}/` already exists, stop and ask the operator: open the existing folder, create with a numeric suffix (`{slug}-2`), or abort.
- **Pacing.** Phase 1 is batched (3 questions at once, plus the client selection). Phase 2 is one-at-a-time, POBO-style.
- **Use templates.** The CLAUDE.md and STATUS.md come from `templates/` in this skill folder. Read them, replace each `{{PLACEHOLDER}}` with the operator's answer; if unknown, use `[TBD — operator to fill]`.
- **Capture learnings at the end.** Phase 4 is mandatory. Never skip it.
- **If `templates/` is missing or unreadable**, stop and tell the operator the skill is corrupted — they should re-run the install from the `paxus-skills` repo. Do not try to generate templates from memory.

---

## Phase 1 — Client + project setup (batched)

**Step 1.1 — Identify the client.**

List the existing client folders by reading `~/paxus-ai/clients/`. Show them to the operator:

> "Which client is this project for? I see: {list of client slugs}."

If no client folders exist at all, stop with the message above under "Client must exist first."

**Step 1.2 — Ask three questions in one message.**

Once the client is chosen, ask:

1. What do you want to call this project?
2. What type of project is this? Options: **monthly close** / **board package** / **CFO advisory engagement** / **tax filing (sales tax, payroll, 1099)** / **client onboarding** / **SOP / internal process** / **dashboard / tool build** / **ad-hoc analysis** / **other (describe)**.
3. Any existing source material I should use as context? (Paste text, give me a file path to read, or say "none.")

Wait for all three answers. From the project name, derive the slug and confirm: "Use `{slug}`, or want a different one?"

If they provided context, read it carefully. Use it to **pre-fill** Phase 2 answers — don't migrate verbatim, but let it inform the answers you offer.

---

## Phase 2 — Project profile (one-at-a-time)

Ask each question individually. After the operator answers, briefly confirm what you captured before moving on. If Phase 1 context pre-filled an answer, present it as "Based on what you shared, this looks like X — keep it or change?"

Questions:

1. **Purpose** — one or two sentences. Why does this project exist? What problem is it solving?
2. **End state** — what does "done" look like? The concrete thing that ships or happens at the end.
3. **Key deliverables** — what specific outputs come out of this project? (e.g., "monthly financial packet as .docx + YoY comparison as .xlsx," or "quarterly board report with budget-to-actuals," or "documented SOP in Google Doc.")
4. **Deadlines** — any hard dates? Primary deliverable deadline + any secondary milestones. Paxus delivers client financials by the **20th of the following month** — flag if this project conflicts with that cadence.
5. **Controller review** — does this project's output need controller sign-off before going out? (Most client-facing projects: yes. Internal SOPs, dashboards, or analysis: usually no.) Capture as "Yes — {who reviews}" or "No — operator owns the ship."
6. **Constraints or dependencies** — anything Claude should know? Waiting on data from the client? Specific format required by the client or by regulation? Tool limitations? Someone else owns a piece?

If the operator says "I don't know" or "skip," accept it. Write `[TBD — operator to fill]` at that field.

---

## Phase 3 — Create the project

1. Create the project folder: `~/paxus-ai/clients/{client-slug}/projects/{project-slug}/`
2. Create subfolders inside it:
   - `inputs/` — for raw source files (QBO exports, bank statements, transcripts, source docs the operator drops in)
   - `deliverables/` — for work product going out (drafts, client-facing files)
   - `notes/` — for working notes and meeting recaps
3. Read the client's name from `~/paxus-ai/clients/{client-slug}/CLAUDE.md` (the H1 heading, typically `# {Client Name} — Claude instructions` or similar). If not findable, convert the slug back to a readable name (e.g., `mary-abbott-house` → `Mary Abbott House`) and ask the operator to confirm.
4. Write `CLAUDE.md` from `templates/project-claude-md.md`, substituting:
   - `{{PROJECT_NAME}}` — the project name
   - `{{CLIENT_NAME}}` — the client's readable name
   - `{{PROJECT_TYPE}}` — from Phase 1 Q2
   - `{{PROJECT_PURPOSE}}` — from Phase 2 Q1
   - `{{END_STATE}}` — from Phase 2 Q2
   - `{{KEY_DELIVERABLES}}` — from Phase 2 Q3
   - `{{DEADLINES}}` — from Phase 2 Q4
   - `{{CONTROLLER_REVIEW}}` — from Phase 2 Q5 (reformat as a complete sentence)
   - `{{CONSTRAINTS}}` — from Phase 2 Q6
   - `{{ONBOARD_DATE}}` — today's date (YYYY-MM-DD)
   - `{{OPERATOR_NAME}}` — operator's first name (lookup rules below)
5. Write `STATUS.md` from `templates/project-status-md.md`, substituting:
   - `{{PROJECT_NAME}}`, `{{CLIENT_NAME}}`, `{{PROJECT_TYPE}}`
   - `{{PRIMARY_DEADLINE}}` — pull from Phase 2 Q4 (first deadline mentioned)
   - `{{CURRENT_PHASE}}` — default to "Scaffolded, ready to start."
   - `{{NEXT_ACTION}}` — ask the operator one more question: "What's the first thing you want to do in this project?" Use their answer here.
   - `{{OPEN_ITEMS}}` — default to "(none yet)"
   - `{{ONBOARD_DATE}}` — today's date

**Operator name lookup:**

1. Look in `~/.claude/CLAUDE.md` for a clear self-identification (e.g., `# CLAUDE.md — Cassie Rigsby`). If found, use that name.
2. If not found, ask the operator: "What's your first name? I'll log it on this project."
3. If they decline, use `anonymous` and continue.

---

## Phase 4 — Learnings capture (mandatory)

Ask two questions, one at a time:

1. What was confusing, unclear, or wrong in setting up this project?
2. What should we add, remove, or change for the next run?

If they say "nothing" to both, accept and move on.

If they have feedback, append to `~/.claude/skills/onboard-project/learnings.md` with this format:

```markdown
## {YYYY-MM-DD} — {operator first name} — project: {client-slug}/{project-slug}
- [LEARNING] {what they said about #1}
- [SUGGESTION] {what they said about #2}
```

If `learnings.md` doesn't exist, create it with a one-line header: `# /onboard-project — Learnings` followed by the new entry.

---

## Phase 5 — Wrap

Show the operator:

1. **Folder tree** — list the contents of the new project folder. On macOS/Linux: `tree ~/paxus-ai/clients/{client-slug}/projects/{project-slug}/` (or `find`/`ls -R` if `tree` isn't installed). On Windows: use the equivalent directory listing.
2. **Generated CLAUDE.md preview** — display the file content so they can spot anything off and edit if needed.
3. **Suggested next actions:**
   - "Drop any source documents (QBO exports, bank statements, transcripts) into `inputs/` so Claude has them when you work in this folder."
   - "When you're ready to start work, open Claude Code inside this project folder — it'll pick up both the firm rules, the client's rules, and this project's rules automatically."
   - "Open `STATUS.md` and refine the next action as you go."

End with one line: "Project scaffolded: {project-name} for {client-name}. Folder at `~/paxus-ai/clients/{client-slug}/projects/{project-slug}/`. Good luck."

---

## File creation reference

- **`~/paxus-ai/clients/{client-slug}/projects/{project-slug}/CLAUDE.md`** ← from `templates/project-claude-md.md`
- **`~/paxus-ai/clients/{client-slug}/projects/{project-slug}/STATUS.md`** ← from `templates/project-status-md.md`

Always create these subfolders (even if empty):
- `~/paxus-ai/clients/{client-slug}/projects/{project-slug}/inputs/`
- `~/paxus-ai/clients/{client-slug}/projects/{project-slug}/deliverables/`
- `~/paxus-ai/clients/{client-slug}/projects/{project-slug}/notes/`

The firm rules and client-level rules are already in the global CLAUDE.md and the client CLAUDE.md — don't duplicate them. The project CLAUDE.md only captures project-specific context.
