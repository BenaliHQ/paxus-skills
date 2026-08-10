# Bundle Mechanics — filling, multi-entity, update mode, edge cases

Read this before Phase 4 (fill) and any time you touch an existing bundle.
SKILL.md carries the workflow and the rules; this file carries the mechanics.

## Copying and token fill

Copy `templates/bundle/` to the destination. Replace `{{CLIENT_NAME}}` and
fill `0-core/log.md`'s initialization tokens (`{{ONBOARDING_DATE}}`,
`{{SOURCES_LIST}}` from the manifest, status counts,
`{{GAP_DISPOSITIONS}}` and `{{OPEN_ITEMS}}` from the gap interview) **at
the end of Phase 5**, when the real values exist.

## Multi-entity transformation (apply mechanically)

1. For each entity in the manifest, copy the template's `d-books/` FILES
   into `d-books/<entity-slug>/` (never rename `d-books/` itself).
2. Inside each entity subfolder, rewrite every `/d-books/<file>.md` link to
   `/d-books/<entity-slug>/<file>.md`.
3. Rewrite cross-group references (e.g., from A/F files) to the correct
   entity's path; a link that applies to all entities points to
   `/d-books/index.md`.
4. Rewrite `d-books/index.md` as a directory of entity subfolders (one line
   per entity), each subfolder getting its own `index.md` listing.
5. F-group tables carry an Entity column; fill it per row.

The validator (E7) rejects any unscoped `/d-books/<file>.md` link in a
multi-entity bundle.

## Capture modes (how each property gets filled)

- **ASK** — answered from transcript/interview content.
- **CONFIRM** — current value plus the pointer to where it lives.
- **DOCUMENT** — extracted from a provided document; the extraction cites
  the document, and the bundle links the document rather than copying it.
- **EXPORT** — summarize the export's structure; link a pre-existing
  export file where one exists, or cite the QBO pointer (realm, report,
  as-of date) for CLI-pulled data. Don't paste hundreds of rows into a
  bundle file, and don't write raw data files into the client folder.
- **SCAFFOLD** — keep the empty structure (seed only from a real artifact,
  e.g. an actual kickoff recap; never date an entry to the onboarding run).
- **RUNTIME** — never stored (pointer to the system of record at most).

## Rules while filling

- **Per-entity switches.** Apply nonprofit/entity-type consequences to the
  entity they belong to: materiality collapse (no floor / ask everything —
  write it explicitly), attachment policy, budget vs. actual, fixed-asset
  schedule, board-keyed delivery, board escalation, and check-to-employee
  red flags for nonprofits; draws/distributions/shareholder-loan handling
  per for-profit entity type.
- **Conditional schema items** (marked CONDITIONAL in the template or
  intake set, e.g. the formal financial policy document) apply only to the
  client shapes they name. Where they don't apply, write "Not applicable
  per {name}, {date}: {reason}" in the file — that is an answer, not a gap.
- **Out-of-scope blocks** get "not in scope for this engagement" noted in
  the file (keep the file; don't delete it).
- **Citations** on every per-client concept file, from the source manifest
  only. AGENTS.md and reserved files (`index.md`, `log.md`) carry none.
- **Status discipline.** `scaffold` = untouched template; `partial` = some
  TBDs or unresolved conflicts remain; `active` = complete and confirmed
  (a file whose remaining items are all explicit "Not applicable" sign-offs
  is complete).
- **Frontmatter.** Keep `type` (OKF requirement), refresh `timestamp`, keep
  `schema_properties` accurate.
- **index.md files are listings.** Update each folder's index to match the
  actual files. The client's hard constraints go in
  `0-core/client-critical-rules.md` (2 to 4 rules, chosen from what the
  sources emphasize most) — not prose in the index.

## Update mode (existing bundle)

Never edit the live bundle in place.

1. Copy the existing `.agents/` to a timestamped backup
   (`.agents-backup-YYYYMMDD-HHMM/`) in the same parent folder.
2. Build the merged result in a local staging copy.
3. `active`/`partial` content is never regressed to template text — new
   facts merge in with new citations; supersession/conflict rules apply. A
   `scaffold`-status file may be filled wholesale ONLY if its current
   content is identical to the template; otherwise treat it as `partial`
   (status labels can be stale).
4. Show the operator a complete diff, get approval, then apply.
5. Every change gets a dated `0-core/log.md` entry.

**Template version drift.** If the existing bundle's AGENTS.md
`template_version` differs from this skill's template, flag it to the
operator before merging. Don't silently upgrade firm-standard files during
a content update; note the migration as its own follow-up. (Bundles built
before template 1.1.0 have `log.md`, `client-critical-rules.md`, and
`workspace-locations.md` loose at the root instead of in `0-core/` — that
layout move is part of the 1.0.x → 1.1.0 migration, never a silent fix.)

## Edge cases

- **Multi-entity clients.** `d-books/<entity-slug>/` per entity; groups A-C
  stay engagement-level; F-group tables key rows by entity; the
  entity-relationships file carries the intercompany accounts.
- **Mid-transition tooling.** Record BOTH states with dates and which is
  target. Coding context for old periods lives in the old system — say
  where.
- **"It's in the client intro / it's in FC."** Valid answers — capture the
  pointer, mine the referenced document if provided, and don't re-ask what a
  supplied document already answers.
- **Skills as report producers.** When a deliverable is produced by another
  Claude skill (dashboards, payroll allocation), the bundle names the skill
  and its halt conditions; the skill's own repo entry is the spec.
- **Budgeted hours known to be wrong.** Record the reset targets the team
  states, note the system-of-record update as an open item, keep controller
  vs. CFO hours separate.
- **Provisional tier ladder.** Record the tier as named, mark provisional,
  add "confirm against the canonical ladder" to the gap list — and gate
  everything by confirmed scope, not the tier name. Before declaring any
  commercial gap, search the firm's admin/onboarding drive for the accepted
  quote: it has turned out to hold the canonical tier ladder and resolve
  several "gaps" at once.
- **Research-sourced claims need re-reading once ownership context
  arrives.** A transcript line about ownership ("no business relationship")
  read in isolation can be wrong as a related-party statement; re-check
  such promotions (especially anything headed for client-critical-rules)
  after A3/A6 are answered.
