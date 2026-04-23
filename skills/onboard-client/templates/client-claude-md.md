# {{CLIENT_NAME}}

Client folder for Paxus CPA work with {{CLIENT_NAME}}. The Paxus standardized firm rules (no income tax, source citations, draft-don't-send, dollar rounding, controller flag protocol, etc.) live in your global `~/.claude/CLAUDE.md` and apply automatically. This file adds client-specific context.

## Client snapshot

- **Entity type:** {{ENTITY_TYPE}}
- **Industry:** {{INDUSTRY}}
- **Revenue tier:** {{REVENUE_TIER}}
- **Website:** {{WEBSITE}}

## Service relationship

- **Service tier(s):** {{SERVICE_TIERS}}
- **Assigned staff lead:** {{STAFF_LEAD}}
- **Assigned controller:** {{CONTROLLER}}

## Recurring deliverables

{{RECURRING_DELIVERABLES}}

## Key contacts

{{KEY_CONTACTS}}

## Tech stack

Default Paxus stack (QuickBooks Online, Financial Cents, Google Workspace) unless noted below.

{{TECH_SPECIFICS}}

## Client-specific rules and quirks

{{SPECIAL_RULES}}

## Folder structure

```
{{CLIENT_SLUG}}/
├── CLAUDE.md           ← this file
├── STATUS.md           ← current engagement state
├── notes/              ← meeting notes, ad-hoc captures
├── deliverables/       ← finished outputs
└── projects/           ← closable subprojects (e.g., 2026-04-close)
```

## Source

Onboarded via `/onboard-client` on {{ONBOARD_DATE}} by {{OPERATOR_NAME}}.
