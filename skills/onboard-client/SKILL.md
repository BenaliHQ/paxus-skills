---
name: onboard-client
description: Bring a Paxus client into your AI workflow with the firm's standard folder structure. Run when starting work with a new client, or when bringing an existing client into Claude Code for the first time. Creates ~/paxus-ai/clients/{client-slug}/ with CLAUDE.md, STATUS.md, and the standard subfolders, and optionally scaffolds the first project under it.
---

# /onboard-client — Paxus Client Onboarding Skill

You are setting up a Paxus client folder in the operator's `~/paxus-ai/clients/` workstation. Follow the five phases below in order. Be conversational and warm — match the Paxus voice from the firm rules.

## Important rules for this skill

- **No fabrication.** If the operator doesn't know the answer to a question, write `[TBD — operator to fill]` in the generated file. Never invent details.
- **Slug discipline.** Generate the client slug from the client name using these rules in order:
  1. Lowercase everything
  2. Strip apostrophes, quotes, parentheses, and other punctuation entirely (e.g., `O'Reilly Construction` → `oreilly construction`)
  3. Replace any remaining non-alphanumeric character (including `&`, `/`, `.`, `,`) with a single dash
  4. Collapse consecutive dashes into one, trim leading/trailing dashes
  5. If the result is empty or starts with a digit, prepend `client-`
  Show the operator the derived slug and ask "Use `{slug}`, or want a different one?" before creating any folders.
- **Slug collisions.** If `~/paxus-ai/clients/{slug}/` already exists, stop and ask the operator: open the existing folder, create with a numeric suffix (`{slug}-2`, `{slug}-3`), or abort.
- **Pacing.** Phase 1 is batched (3 questions at once). Phase 2 is one-at-a-time, POBO-style.
- **Use templates.** The CLIENT.md, STATUS.md, and project files come from `templates/` in this skill folder. Read them, fill in the per-client values, write the result. Replace each `{{PLACEHOLDER}}` with the corresponding answer; if a field is unknown, use `[TBD — operator to fill]`.
- **Capture learnings at the end.** Phase 4 is mandatory. Never skip it.
- **If `templates/` is missing or unreadable**, stop and tell the operator the skill is corrupted — they should re-run the `paxus-ai-workstation` SETUP. Do not try to generate templates from memory.

---

## Phase 1 — Quick setup (batched)

Greet the operator and ask three questions in one message:

1. What's the client's name?
2. Website (if any)?
3. Do you have any existing materials on this client you want to give me as context? You can paste text, give me a file path to read, or say "none."

Wait for all three answers. From the name, derive a slug. Show the slug to the operator and ask "Use `{slug}`, or want a different one?"

If they provided context (text, file path), read it carefully. Use it to **pre-fill** answers for Phase 2 — don't migrate the file verbatim, but let it inform the answers you offer.

---

## Phase 2 — Client profile (one-at-a-time)

Ask each question individually. After the operator answers, briefly confirm what you captured before moving to the next question. If Phase 1 context pre-filled an answer, present it as "Based on what you shared, this looks like X — keep it or change?"

Questions:

1. **Entity type** — LLC, S-corp, C-corp, nonprofit, partnership, sole prop, or other?
2. **Industry + revenue tier** — what industry, and roughly what's their annual revenue? (Tiers: <$1M, $1M–$5M, $5M–$10M, $10M–$20M, >$20M)
3. **Service tier(s)** — which Paxus services does this client receive? Multi-select from: Wheel of Service, No-Notes, CFO advisory, Bookkeeping-only, Other.
4. **Recurring deliverables** (skip if No-Notes only) — what are the monthly recurring deliverables for this client? (e.g., "monthly financial packet by the 20th, board package quarterly")
5. **Paxus team assignments** — who's the assigned staff lead and controller? (Format: "Lead: {name}, Controller: {name}")
6. **Key contacts at the client** — for each, name + role + email. Ask for the primary contact first; offer to add more.
7. **Special rules or quirks unique to this client** — anything Claude should always know or never do for this client? (e.g., "always copy the CFO on board reports," "do not discuss X with Y," "uses Sage instead of QBO")
8. **Tech specifics** (skip if no exception) — does this client use anything different from the firm default (QBO, Financial Cents, Google Workspace)?

If the operator says "I don't know" or "skip" for a question, accept it. Write `[TBD — operator to fill]` in the generated file at that field.

---

## Phase 3 — Project scaffold (optional)

Ask: "Want to scaffold your first project for this client now? If yes, what's it called?"

Suggest defaults based on context — e.g., if it's the middle of the month, suggest `{current-month}-close`; if Phase 2 mentioned an upcoming board meeting, suggest `{date}-board-package`.

If yes:
- Derive a project slug (lowercase, dashes)
- Create `~/paxus-ai/clients/{client-slug}/projects/{project-slug}/`
- Use `templates/project-claude-md.md` and `templates/project-status-md.md`, fill in project name + purpose + end state, write to the new folder

If no:
- Note in client STATUS.md that no project is scaffolded yet
- Tell the operator they can re-run `/onboard-client` later or create a project folder manually

---

## Phase 4 — Learnings capture (mandatory)

Ask two questions, one at a time:

1. What was confusing, unclear, or wrong in this onboarding?
2. What should we add, remove, or change for the next run?

If the operator says "nothing" to both, accept and move on.

If they have feedback, append to `~/.claude/skills/onboard-client/learnings.md` with this format:

```markdown
## {YYYY-MM-DD} — {operator first name} — client: {slug}
- [LEARNING] {what they said about #1}
- [SUGGESTION] {what they said about #2}
```

To get the operator's first name:
1. Look in `~/.claude/CLAUDE.md` for a clear self-identification (e.g., a heading like `# CLAUDE.md — Cassie Rigsby` or a line "I'm Cassie..."). If you find one, use that name.
2. If you don't find one, **ask the operator**: "What's your first name? I'll log it with this learning so we know who flagged what." Use what they say. Don't guess from filenames or environment variables.
3. If they decline to give a name, use `anonymous` and continue. Do not block the learning capture on this.

---

## Phase 5 — Wrap

Show the operator:

1. **Folder tree** — `tree ~/paxus-ai/clients/{client-slug}/` (or `find`/`ls -R` if tree isn't installed). Visual confirmation of what was created.
2. **Generated CLIENT.md preview** — display the file content so they can spot anything off.
3. **Suggested next actions:**
   - "Drop any existing client documents into `notes/` so Claude has them when you work in this folder"
   - "Open `STATUS.md` and fill in your immediate next steps"
   - If a project was scaffolded: "Your first project is ready at `projects/{slug}/`. Open Code in that folder when you're ready to start."

End with one line: "Client onboarded: {name}. Folder at ~/paxus-ai/clients/{slug}/. Run `/onboard-client` again whenever you bring on the next client."

---

## File creation reference

When generating files, use these templates from the `templates/` folder:

- **`~/paxus-ai/clients/{slug}/CLAUDE.md`** ← from `templates/client-claude-md.md`
- **`~/paxus-ai/clients/{slug}/STATUS.md`** ← from `templates/client-status-md.md`
- **`~/paxus-ai/clients/{slug}/projects/{project-slug}/CLAUDE.md`** ← from `templates/project-claude-md.md` (Phase 3 only)
- **`~/paxus-ai/clients/{slug}/projects/{project-slug}/STATUS.md`** ← from `templates/project-status-md.md` (Phase 3 only)

Always create these folders even if empty:
- `~/paxus-ai/clients/{slug}/notes/`
- `~/paxus-ai/clients/{slug}/deliverables/`
- `~/paxus-ai/clients/{slug}/projects/`

The standardized firm rules (`templates/firm-rules.md`) are referenced by the client CLAUDE.md but not duplicated — they live once in the operator's global `~/.claude/CLAUDE.md`.
