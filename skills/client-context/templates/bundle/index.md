---
okf_version: "0.1"
---
# {{CLIENT_NAME}} — Client Context Bundle

Per-client context package for AI skills at Paxus CPA. One markdown file per
knowledge unit; skills load only the files their task requires. Context stores
knowledge, not state: anything that changes weekly lives in QuickBooks or
Financial Cents and is queried live. Credentials are never stored here, only
pointers to where they live.

# Bundle map

* [Agent contract](AGENTS.md) - how to work in this bundle. Read before making any change.
* [0. Core](0-core/) - client-critical rules, workspace locations, and the update log; read the rules first
* [A. Identity & relationship](a-identity/) - who the client is; durable, set once
* [B. Engagement & commercial](b-engagement/) - what we do for them and on what terms
* [C. Staffing & capacity](c-staffing/) - who serves them and how the work is scheduled
* [D. Books & systems](d-books/) - QBO configuration, coding rules, schedules; one folder per entity for multi-entity clients
* [E. Access & credentials](e-access/) - credential pointers and authorization matrix; pointers only, never values
* [F. Annual](f-annual/) - cleanup and year-end
* [G. Living context](g-living/) - files that grow as work happens

# History

* [Update log](0-core/log.md) - who changed what, when
