---
type: Agent Contract
title: Agent contract
description: The operating contract for any AI agent working in this client context bundle. Firm-standard; identical across all Paxus client bundles.
status: active
template_version: "1.1.0"
timestamp: 2026-08-10T00:00:00-05:00
---

This folder is a Paxus CPA client context bundle in the Open Knowledge Format
(OKF v0.1). If you are an AI agent doing work for this client, this file is
your operating contract. It is the same for every Paxus client; anything
client-specific lives in the bundle's other files.

# How to traverse

1. Start at [/index.md](/index.md): it lists what exists. Then read
   [/0-core/client-critical-rules.md](/0-core/client-critical-rules.md) — the
   few rules no task may violate for this client — before touching books or
   communications. Each folder has its own `index.md` listing.
2. Load only the files your task requires. The per-file `description` and
   `schema_properties` frontmatter tell you what each file covers. When you
   are coding transactions, that means the `d-books/` coding files, not the
   whole bundle.
3. [/0-core/workspace-locations.md](/0-core/workspace-locations.md) holds the
   IDs and links (QBO company, Financial Cents, Drive) that anchor everything
   else. Navigate by ID, never by search.
4. A client drive with no bundle folder is not a managed context: do not
   create one on your own. Bundles are scaffolded from the firm template
   during onboarding.

# Knowledge, not state

This bundle stores knowledge that systems of record cannot tell you. It never
stores live state. Bank-feed status, cleanup progress, open uncategorized
items, and task states live in QuickBooks and Financial Cents: query them at
runtime.
If you find yourself writing something here that will be stale in a week, it
belongs in the system of record instead.

# Credentials

Pointers only, never values. This bundle records WHERE a credential lives
(Cloud Protect, the FC vault) and who is assigned. Never write a password,
token, or 2FA code. Never write a full bank account or routing number:
account nicknames and last-four digits only.

# Editing rules

- Update the relevant concept file in place; keep the writing factual and
  attributed. Every non-obvious claim traces to a source in that file's
  `# Citations` section. (Scope: per-client concept documents. This
  firm-standard contract and the reserved `index.md`/`log.md` files carry no
  citations.)
- Every meaningful change also gets a dated entry in
  [/0-core/log.md](/0-core/log.md), newest first (`## YYYY-MM-DD`, bold
  change-type lead like **Update** / **Creation** / **Deprecation**).
- Maintain frontmatter: keep `type` (required by OKF), refresh `timestamp` on
  meaningful change, and move `status` along `scaffold → partial → active` as
  content firms up. Preserve keys you do not understand.
- `index.md` files are listings only: update them when files are added or
  removed, keep them boring, no frontmatter (the root `index.md` carries only
  `okf_version`).
- Use bundle-relative links (`/d-books/file.md`). Do not add new top-level
  folders or rename groups: the structure is the firm schema and is versioned
  in the template (see `template_version` above), not per client.
  Multi-entity clients nest one subfolder per entity INSIDE `d-books/`
  (`/d-books/<entity-slug>/file.md`); books links must then be
  entity-scoped. The only permitted unscoped books link is
  `/d-books/index.md` (the all-entities directory); any other unscoped
  `/d-books/` link is an error.
- Conflicting sources are information: record both positions with
  attribution; never silently overwrite the earlier one.

# Judgment limits

- Never guess an allocation, threshold, or coding rule that is not written
  down. Ask, or route the item to the client questions list per this
  client's materiality file.
- Internal economics (budgeted hours, profitability) never change how the
  work is performed. They exist so scope conversations can be intentional.
- When a file says a correction was made, append it to
  `/g-living/correction-and-skill-feedback-log.md` as a one-line entry. That
  log is the AI-readable source of truth for improving skills.
