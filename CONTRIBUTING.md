# Contributing to the Paxus Skills Library

This repo is the **single source of truth** for the firm's skills. Cowork syncs skills directly from here, so **whatever is on the `main` branch is what the whole team gets.** That is exactly why every change goes through review first — no skill reaches the team without a second set of eyes.

You do **not** need to be a coder to contribute. The steps below are the whole process.

## The golden rule

**Never use the in-app "Share with organization" button.** It has no review step — it broadcasts a skill to everyone instantly. That is the thing we are protecting against. All sharing happens through this repo. The org setting stays **off**.

## How a skill gets added or changed

1. **Make a branch.** Don't edit `main` directly. Create a branch named for what you're doing, e.g. `add-monthly-close` or `fix-journal-entries-edge-case`.
2. **Add or edit the skill.** Copy `template/SKILL.md` into a new folder under `skills/<your-skill-name>/`, or edit an existing `skills/<name>/SKILL.md`. One skill = one folder.
3. **Keep client data out.** No client names, numbers, or SOP text in the skill. Client context comes from Google Drive — see [`docs/context-model.md`](docs/context-model.md).
4. **If you added a new skill, list it.** Add its path (e.g. `./skills/your-skill-name`) to the `skills` array in `.claude-plugin/marketplace.json` so Cowork knows to sync it.
5. **Open a Pull Request.** This is the "submit it for review" step. Describe what the skill does and what you changed.
6. **Review.** A reviewer — **Cassie Rigsby, Landry Greenhill, or Jennifer Sanders** — reads it, tests it, and either requests changes or approves. This is the test → revise loop.
7. **Merge = release.** Once approved and merged into `main`, Cowork picks it up automatically on the next sync. You're done. No manual upload, no zip files.

## The flow in one line

`branch → edit skill → open PR → reviewer tests & approves → merge → Cowork auto-pulls`

## Reviewers

| Reviewer | |
|---|---|
| Cassie Rigsby | |
| Landry Greenhill | |
| Jennifer Sanders | |

Reviewers need a GitHub account and basic comfort reading a Pull Request — no coding required.
