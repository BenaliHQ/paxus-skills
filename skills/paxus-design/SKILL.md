---
name: paxus-design
description: Design and build well-branded interfaces and assets for Paxus CPA's own brand — marketing pages, the client portal, decks, mocks, one-pagers, or production UI. Ships the firm's design tokens, logos, type, iconography, and reference UI kits. Run when the deliverable should look like Paxus, or when another skill (e.g. /design-pdf) needs a Paxus design system to pull from.
---

# /paxus-design — Paxus CPA brand system

You are designing or building something in **Paxus CPA's own brand**. This skill is the firm's design **fuel**, packaged: tokens, logos, type, iconography, and two reference UI kits. Brand-agnostic engines (like `/design-pdf`) read their look from a design system — point them here when the output should be Paxus-branded.

Be conversational and warm — match the Paxus voice: calm, confident, plain-spoken, numerate.

> **Why a brand lives in this repo when client data must not:** the engine/fuel rule (`docs/context-model.md`) keeps *client* data out of skills. This is the **firm's own** brand — firm-wide, reusable, and reviewed — so it belongs here, the same way `/design-pdf`'s scaffold does. Never embed a *client's* brand or data in a skill; that still comes from Google Drive.

## Important rules for this skill

- **Read `README.md` first.** It is the brand source of truth and it overrides anything that reads otherwise elsewhere. Then open the specific files you need.
- **No fabrication.** Hero stats, client names, and case-study quotes in the kits are placeholders. Leave `[bracketed placeholders]` until the operator gives real values — never invent client wins, numbers, or logos.
- **Don't hand-roll the tokens.** `colors_and_type.css` drops into any HTML and provides every variable + semantic class. Adapt with it; don't re-derive hexes from memory.
- **If `README.md` or `colors_and_type.css` is missing or unreadable**, stop and tell the operator the skill is corrupted and to re-install from the `paxus-skills` repo. Do not regenerate the brand from memory.

## Five things people get wrong (the brand landed here late in design)

1. **Paxus does NOT do taxes.** Services are **bookkeeping (monthly close), advisory / fractional CFO, audit & assurance, outsourced controller**. No tax headlines, tax calendars, or filing flows. Paxus refers out for tax.
2. **Body copy is the serif Source Serif 4** — not Inter. Display = Manrope 800; UI chrome (buttons/nav/eyebrows/inputs) = Inter.
3. **Icons = Lucide @ 1.25px stroke** in soft-blush pill tiles, with **functional/financial** glyphs (`receipt`, `calculator`, …) — softer styling, not decorative flower/heart icons.
4. **No burgundy-ink section backgrounds.** The case-studies section is **blush `#E0D0E0`** with white cards; the middle card lifts ("Featured" pill + shadow). **No pricing tables** — case studies / testimonials instead.
5. **Use the real logo PNGs.** The `*.svg` marks are **deprecated** approximations that don't match the rosette.

## How to use

- **Throwaway visual (mock, deck, prototype):** copy the assets you need and `colors_and_type.css` next to a static HTML file the operator can open. Build with the semantic classes (`.t-display-hero`, `.t-body`, etc.).
- **Production code:** read the README + tokens to become an expert in the brand, then implement in whatever stack the target repo uses. Recreate the look; don't copy the prototype's internal structure.
- **As fuel for another skill:** when running `/design-pdf` (or similar) for a Paxus-branded document, point it at this skill's `colors_and_type.css` and `assets/`.
- **No guidance given:** ask what they want to build, ask a couple of scoping questions, then act as an expert designer who outputs HTML artifacts *or* production code.

## Quick reference

- **Brand color:** `#681E44` burgundy. Pressed `#4A1430`. Ink `#2A0A1A` (dark blocks only, never section backgrounds).
- **Accents:** mauve `#B080A0`, blush `#E0D0E0`, blush-soft `#F2E8EE`. Decorative only — never CTAs.
- **Canvas:** warm cream `#FBF7F4`. White is for cards lifting off the canvas.
- **Display:** Manrope 800, tight line-height (0.88–0.95), big (60–112px). **Body:** Source Serif 4 (serif). **UI:** Inter.
- **`font-feature-settings: "calt" 1, "ss01" 1`** everywhere.
- **CTAs:** pill (9999px) burgundy → cream text. `scale(1.03)` hover, `scale(0.97)` active.
- **Cards:** 24–48px radii, `0 0 0 1px rgba(26,18,23,0.12)` ring, `translateY(-2px)` on hover.
- **Icons:** Lucide @ 1.25 stroke, blush pill tiles, financial glyphs. No emoji, no unicode-as-icon, no filled icons.
- **Tone:** confident-and-calm, sentence case, "we" / "you", numerate, no exclamation points.

## Files

- `README.md` — brand source of truth. **Read this first.**
- `colors_and_type.css` — every token (CSS vars) + semantic classes. Drop into any HTML.
- `assets/` — logos. Use `paxus-logo-full.png`, `paxus-wordmark.png`, `paxus-mark-real.png`, and the `*-cream.png` reverse variants. The `*.svg` marks are deprecated.
- `preview/*.html` — 16 cards showing every token in context. Open in a browser to see the system.
- `ui_kits/website/` — marketing-site reference. Final `index.html` reflects the no-tax, case-studies direction.
- `ui_kits/portal/` — client-portal reference. ⚠️ Still tax-themed — use for structure only and rebuild copy/flows around real services. See README "Known gaps".

When in doubt, read the full `README.md`.
