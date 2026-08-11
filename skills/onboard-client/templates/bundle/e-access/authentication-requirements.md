---
type: Configuration
title: Authentication requirements
description: "Per-system 2FA behavior: how often each system challenges, how complex the challenge is, and who receives codes. This is what decides whether pulls (bank statements, reports) can be automated or need a human in the loop."
schema_properties: [authentication_requirements]
status: scaffold
---

# Requirements

The frequency and complexity columns are the point: "has 2FA" alone does not
gate automation. A code that routes to a shared inbox on rare new-device
checks is automatable; a push approval to a client's personal phone on every
login is not.

| System | Challenge frequency | Challenge complexity | Codes go to | Automation impact |
|---|---|---|---|---|
| TBD | every login / new device / periodic (~30d) / rare | e.g. SMS code, email code, push approval, security questions, hardware token | shared codes inbox / firm Google Voice / a named person's phone | automatable / human needed each time / human needed on re-auth only |

# Citations

[1] TBD — populate only from the actual sources ingested during onboarding (transcript, document, export, or named person + date). Never pre-claim a source.
