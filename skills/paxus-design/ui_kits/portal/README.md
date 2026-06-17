# Paxus CPA — Client portal kit

The product side of Paxus: a logged-in dashboard where clients see their books, upload source documents, message their accountant, and see their next call.

> ⚠️ **Structural reference only.** It still renders a `TaxTimeline` and frames document upload around tax filing — left in place because tax positioning is deferred, but **not endorsed copy.** Paxus's services are bookkeeping, advisory / fractional CFO, and outsourced controllership. **Use this kit for component structure only**, and rebuild its copy and flows around month-end close, advisory deliverables, and controller reporting. See the top-level `README.md` → "Known gaps."

## Components (in `components.jsx`)
- `PortalSidebar` — 248px sidebar, nav pills, badge counts, account card at bottom
- `PortalTopbar` — sticky blur header with eyebrow + page title + utility buttons
- `StatCard` — three tones: default white, blush, ink
- `TaxTimeline` — 5-step horizontal stepper w/ pulse animation on active node — ⚠️ **rename/repurpose** to a month-end-close or onboarding stepper; Paxus does not do tax filing
- `DocList` — striped row list with status pills (received/review/missing)
- `NextAppt` — burgundy card with rosette watermark + Join/Reschedule actions
- `MessageThread` — single accountant reply preview with inline composer

## Open
`ui_kits/portal/index.html`
