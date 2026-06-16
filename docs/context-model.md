# Context Model — Skills are the Engine, Client Data is the Fuel

This is the single most important rule in the library. It is what keeps ~50 skills reusable instead of drifting back into a separate copy per client (the exact problem this library was created to solve).

## The boundary

| | Lives in | Why |
|---|---|---|
| **Skills (the engine)** | This repo, in `skills/` | Firm-wide, reusable, reviewed. Works for *any* client. |
| **Client data (the fuel)** | The firm's **Google Drive shared drive** | Per-client. Confidential. Changes constantly. Never reviewed through this repo. |

A skill describes *how* to do a workflow — month-end close, a journal entry, a board package. The *client-specific* inputs to that workflow — the chart of accounts, the SOP for that client, their entity list, prior-period numbers — are the fuel. The same skill, pointed at different fuel, produces the right output for any client.

## How a skill reads client context

Skills do **not** embed client data. When a skill needs client-specific context, it reads it from a folder in the firm's Google Drive shared drive that Cowork has access to locally.

The convention:

```
Google Drive (shared drive)
└── Clients/
    └── <Client Name>/
        ├── SOPs/                ← the client's standard operating procedures
        ├── chart-of-accounts/
        └── reference/           ← prior periods, entity lists, anything the workflow needs
```

In Cowork, the operator points the session at the specific client folder (e.g. `Clients/Acme Co/`), and the skill reads the SOPs and reference material from there. The skill itself only ever says *"read the client's SOP for this workflow from the client folder"* — it never contains the SOP.

## What this means when you write a skill

- ✅ "Read the client's month-end SOP from their `SOPs/` folder, then follow it step by step."
- ❌ Pasting Acme Co's actual month-end SOP into the skill.
- ✅ "Ask which client this is for, then point at `Clients/<that client>/`."
- ❌ Hard-coding `if client == "Acme"` anywhere.

If you find yourself wanting to put a client's name or numbers into a skill, that's the signal the content belongs in Google Drive, not here.

## Why Google Drive (and not this repo)

- Client data is confidential — it does not belong in a skills repo that's synced to every team member's Cowork.
- SOPs change far more often than skills do; keeping them in Drive means updating an SOP doesn't require a PR.
- Cowork already reads the local Google Drive mount, so the fuel is available without any extra plumbing.
