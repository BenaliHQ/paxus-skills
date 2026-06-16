---
name: skill-name-in-kebab-case
description: One or two sentences. What the skill does AND when to run it — the description is how Claude decides to trigger the skill, so name the situations plainly (e.g. "Run when starting a monthly close for a client"). Keep client names OUT of this — skills are firm-wide.
---

# /skill-name — Short Human Title

You are doing <the workflow this skill automates> for the Paxus CPA team. Follow the phases below in order. Be conversational and warm — match the Paxus voice.

## Important rules for this skill

- **No fabrication.** If the operator doesn't know the answer to a question, write `[TBD — operator to fill]`. Never invent client details.
- **Skills are the engine; client data is the fuel.** This skill must work for ANY client. Do not hard-code a client's name, numbers, chart of accounts, or SOP text. When the workflow needs client-specific context, read it from the firm's Google Drive shared drive (see `docs/context-model.md`) — point the operator at the specific client folder; never bake the data into this file.

## Workflow

### Phase 1 — <gather inputs>

<What to ask for / read first. Reference SOPs from Google Drive here, not embedded copies.>

### Phase 2 — <do the work>

<The sequential steps. This is the "workflow" — capture every edge case the team hit when mapping it.>

### Phase 3 — <produce the output>

<What gets created, where it goes, what format.>

### Phase 4 — <verify before done>

<The checklist the skill runs before declaring complete.>

## Edge cases

<List the exceptions the team surfaced during workflow mapping. This section is where a skill earns its reliability — fill it from the real workflow, don't leave it thin.>
