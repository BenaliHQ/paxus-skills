# Paxus Skills — Install Instructions

**You are Claude Code reading this file. Install the Paxus skills on the user's machine by following these steps.** Each step modifies the user's machine. Describe what you're about to do *before* doing it. Show the user the change and let them approve.

The user is a Paxus CPA team member using Claude Code. Adapt shell commands to their OS — bash on macOS / Linux, PowerShell on Windows. Use `$HOME` / `~` on Unix, `$env:USERPROFILE` (PowerShell) or `%USERPROFILE%` (cmd) on Windows.

---

## Step 0 — Pre-flight (do this silently)

1. Confirm the user's OS. Use `uname -s` on Unix, or `$PSVersionTable.OS` / `systeminfo` on Windows.
2. Confirm Git is installed. Try `git --version`.
   - If Git isn't installed: stop and tell the user: "Git isn't installed on this machine. Install it from [git-scm.com](https://git-scm.com) first, then re-run this install. If that's not possible, ask Khalil for a manual install method."
3. Confirm the Claude config directory exists: `~/.claude/` on Unix, `%USERPROFILE%\.claude\` on Windows.
   - If it doesn't exist: stop and tell the user to open Claude Code at least once before running this install, then try again.

If any pre-flight check fails, stop and report the issue. Do not proceed.

---

## Step 1 — Clone the Paxus Skills repo

**Tell the user:** "I'm going to clone the Paxus Skills repo into a temporary folder so I can install the skills on your machine."

Clone `https://github.com/BenaliHQ/paxus-skills.git` into a temporary folder inside the user's home directory:

- macOS / Linux: `~/.paxus-skills-tmp`
- Windows: `%USERPROFILE%\.paxus-skills-tmp`

If a previous temp folder exists (leftover from a previous install attempt), delete it first and re-clone.

If the clone fails (network error, auth required, repo moved), stop and report the error to the user.

---

## Step 2 — Ensure the Claude skills folder exists

Create `~/.claude/skills/` (or `%USERPROFILE%\.claude\skills\` on Windows) if it doesn't already exist. On Windows, this is `C:\Users\{username}\.claude\skills\`.

---

## Step 3 — Install `/client-context`

**Tell the user:** "I'm going to install the `/client-context` skill. After this, you can run `/client-context` inside Claude Code to bring any Paxus client into your AI workflow."

1. Check whether `~/.claude/skills/client-context/` already exists.
   - **If yes**, ask the user: "The `/client-context` skill is already installed. Overwrite with the latest version, or skip?" Honor their answer.
   - **If no, or if they approved overwrite**, copy the entire `skills/client-context/` folder from the cloned repo to `~/.claude/skills/client-context/`. Include the full `templates/` subfolder.
2. Confirm the install by listing `~/.claude/skills/client-context/`. Expected: `SKILL.md` + `templates/` folder with 4 template files.
3. If `learnings.md` doesn't exist in the skill folder, create it with a one-line header: `# /client-context — Learnings`. This is where the skill appends operator feedback after each run.

---

## Step 4 — Install `/onboard-project`

**Tell the user:** "I'm going to install the `/onboard-project` skill. After this, you can run `/onboard-project` inside Claude Code to scaffold a new project under any existing client."

Same pattern as Step 3:

1. Check whether `~/.claude/skills/onboard-project/` already exists. Ask before overwriting.
2. Copy the entire `skills/onboard-project/` folder from the cloned repo to `~/.claude/skills/onboard-project/`. Include the `templates/` subfolder.
3. Confirm by listing the folder. Expected: `SKILL.md` + `templates/` folder with 2 template files.
4. Create an empty `learnings.md` with a one-line header: `# /onboard-project — Learnings`.

---

## Step 5 — Create the Paxus workstation folder

**Tell the user:** "I'm creating your Paxus AI workstation folder at `~/paxus-ai/clients/`. This is where your client and project folders will live."

Create the folder if it doesn't exist:

- macOS / Linux: `~/paxus-ai/clients/`
- Windows: `%USERPROFILE%\paxus-ai\clients\`

If the folder already exists, report that and continue without overwriting.

---

## Step 6 — Clean up

Remove the temporary cloned repo folder created in Step 1.

---

## Step 7 — Confirm

Run these checks and report each one to the user:

1. `~/.claude/skills/client-context/SKILL.md` exists.
2. `~/.claude/skills/client-context/templates/` contains 4 files.
3. `~/.claude/skills/onboard-project/SKILL.md` exists.
4. `~/.claude/skills/onboard-project/templates/` contains 2 files.
5. `~/paxus-ai/clients/` exists.

If all five check out, tell the user:

> Paxus Skills installed. You now have:
>
> - **`/client-context`** — bring a new client into your AI workflow
> - **`/onboard-project`** — scaffold a project under an existing client
> - Your Paxus workstation folder at `~/paxus-ai/`
>
> Try `/client-context` next to bring your first client in. Once that's done, run `/onboard-project` inside that client to start a specific piece of work.

If any check fails, stop and tell the user exactly what's missing.

---

## Rules

- **Only touch the listed paths.** `~/.claude/skills/client-context/`, `~/.claude/skills/onboard-project/`, `~/paxus-ai/clients/`, and the temporary clone folder. Nothing else on the user's machine.
- **Ask before overwriting.** Any existing file or folder gets explicit user confirmation before replacement.
- **Report errors clearly.** If any step fails, stop the install and tell the user what broke. Don't silently continue.
- **Don't modify `~/.claude/CLAUDE.md` or `~/.claude/settings.json`.** That's a separate install (the full `paxus-ai-workstation` repo). This install is skills-only.
