# Paxus CPA — Marketing website kit

A Wise-style marketing site applied to Paxus CPA's plum brand.

> **Final state:** `index.html` reflects the direction — a **3-card services grid** (bookkeeping / fractional CFO / outsourced controller), a **case studies** section on blush `#ECD2E1`, and a burgundy footer. Tax positioning is deferred — make no tax claim either way. Build from `index.html`. `components.jsx` still contains a leftover `PricingTable` from an earlier iteration — ignore it; it was superseded.

## Components (in `components.jsx`)

- `Button` — primary / secondary / outline / ghost / onDark / onDarkOutline; sm/md/lg
- `Header` — sticky blur header with logo, nav pills, sign-in, primary CTA
- `Hero` — billboard headline (Manrope 800, clamp 56–112px), eyebrow, stat row
- `ServiceCard` — default / blush / dark variants, Lucide icon, eyebrow + title + body
- `Services` — services grid (bookkeeping, fractional CFO, outsourced controller)
- `CaseStudies` — replaces the old pricing section: testimonial cards on blush, lifted "Featured" middle card
- `CtaBlock` — full-width burgundy block w/ rosette watermark
- `Footer` — link footer on burgundy
- ⚠️ `PricingTable` — **deprecated**, left over from an earlier iteration; not used in the final site

## Patterns demonstrated
- 32–48px card radii; pill CTAs (9999px)
- Scale 1.03 / 0.97 hover & active on buttons
- Translate-Y -2px hover on cards w/ ring → pop shadow swap
- Burgundy on cream + occasional blush sections for rhythm (no burgundy-ink section backgrounds)
- Lucide icons (1.25 stroke) inside soft-blush icon tiles

## Open
`ui_kits/website/index.html`
