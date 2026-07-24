---
type: Engagement Record
title: Engagement terms
description: Lifecycle status, tier, and terms extracted from the signed documents, each line pointing back to its source.
schema_properties: [client_lifecycle_status, service_tier, accepted_quote, signed_engagement, engagement_terms]
status: scaffold
---

# Status

| Field | Value |
|---|---|
| Lifecycle status | TBD (prospect / onboarding / cleanup / active / offboarding) |
| Service tier | TBD (provisional until the canonical ladder lands) |

# Terms (extracted; skills never parse PDFs)

| Term | Value | Source |
|---|---|---|
| Monthly fee | TBD | engagement letter (link TBD) |
| One-time fees (onboarding, conversion, setup) | TBD | |
| Cleanup range and split | TBD | |
| Start date | TBD | |
| Annual escalator | TBD | |
| Termination terms | TBD | |

If current billing differs from the signed letter (e.g., a temporary
increase), record BOTH with the written authorization (amendment, approval
email) and its effective date. Without documented authorization, keep both
positions and leave this file `partial`.

# Source documents (links, not copies)

* Accepted quote (PDF in client Drive folder): TBD
* Signed engagement (FC e-sign): TBD

# Citations

[1] TBD — populate only from the actual sources ingested during onboarding (transcript, document, export, or named person + date). Never pre-claim a source.
