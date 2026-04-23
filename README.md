# Paxus Skills

Two Claude Code skills for the Paxus CPA team — the lean install, no terminal work required after install.

## What this installs

- **`/onboard-client`** — bring a new client into your AI workflow. Creates a standard folder structure at `~/paxus-ai/clients/{client}/` with CLAUDE.md, STATUS.md, and project-ready subfolders. Optionally scaffolds your first project at the end.
- **`/onboard-project`** — scaffold a new project inside an existing client. Creates `projects/{project}/` with the project's own CLAUDE.md, STATUS.md, and standard subfolders (`inputs/`, `deliverables/`, `notes/`).

Both skills run in the Claude Code desktop app. After the one-time install below, you never need to touch the terminal.

## How to install

Open Claude Code in your home folder and paste this single line:

```
Read https://raw.githubusercontent.com/BenaliHQ/paxus-skills/main/INSTALL.md and follow the instructions exactly.
```

Claude will walk you through each step. You'll see what it's about to do before it does it. Approve when prompted. Takes about one minute.

The install is safe by default: Claude will only create or modify the following locations on your machine:

- `~/.claude/skills/onboard-client/` (and its `templates/` folder)
- `~/.claude/skills/onboard-project/` (and its `templates/` folder)
- `~/paxus-ai/clients/` (the workstation folder — empty until you onboard your first client)

Nothing else on your machine is touched.

## How to use

### First client

1. Run `/onboard-client`
2. Answer Claude's questions about the client
3. Optionally scaffold your first project at the end

### New project for an existing client

1. Run `/onboard-project`
2. Pick the client from the list Claude shows you
3. Answer Claude's questions about the project

### Folder structure (after one client + one project)

```
~/paxus-ai/
  clients/
    {client-slug}/
      CLAUDE.md        # Client-specific rules Claude follows for this client
      STATUS.md        # Current state of the engagement
      notes/           # Working notes
      deliverables/    # Finished work product
      projects/
        {project-slug}/
          CLAUDE.md    # Project-specific rules
          STATUS.md    # Project status
          inputs/      # Drop QBO exports, bank statements, source docs here
          deliverables/# Draft and final project outputs
          notes/       # Working notes for this project
```

Three levels of instructions stack automatically: firm rules (global) + client rules + project rules. Open Claude Code inside any folder and it picks up the right context.

## What this does NOT install

This repo is skills-only. It does **not** install:

- The firm-wide rules in your global `~/.claude/CLAUDE.md`
- The allow / deny list in `~/.claude/settings.json`
- The safety hook at `~/.claude/hooks/paxus-pre-bash.sh`

Those live in the full `paxus-ai-workstation` repo and are a later-stage install once the policy framework is finalized.

## Questions

Email Khalil at khalil@benali.com or message in the shared Slack channel.

## Scope

Internal Paxus + Benali use only. Not for redistribution outside the engagement.
