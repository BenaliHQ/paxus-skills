# Paxus CPA — Design System

> A burgundy-and-blush identity for **Paxus CPA**, structured on the bold, billboard-scale design language of [wise.com](https://wise.com).

This system pairs Paxus's own brand colors — sampled directly from the logo — with the structural confidence of Wise: oversized display typography, pill CTAs, generous radii, ring shadows, and scale-on-hover micro-interactions. The result is a CPA brand that feels modern, deliberate, and unintimidating — the opposite of the navy-and-grey corporate accountancy default.

This is the firm's brand **fuel**, packaged as an installable skill. Brand-agnostic engines like `/design-pdf` pull their look from a design system like this one; point them here when the deliverable should be Paxus-branded.

---

## ⚠️ Read this before you build — what the brand actually is

This bundle was iterated in Claude Design. A few decisions landed **late in the conversation** and supersede anything that reads otherwise in older notes. These are the source of truth:

1. **Paxus does NOT do taxes.** Do not write tax headlines, tax calendars, "tax season" copy, or filing flows. Paxus's actual services are:
   - **Bookkeeping** — monthly close, reconciliation
   - **Advisory / Fractional CFO**
   - **Audit & assurance**
   - **Outsourced controller / Controllership**

   Paxus *refers out* for tax: "We don't prepare tax returns — we partner with firms that do."
2. **Body copy is a serif — Source Serif 4**, not Inter. Display stays Manrope 800; UI chrome (buttons, nav, eyebrows, captions, inputs) stays Inter. The serif-body / sans-display / sans-UI split is intentional.
3. **Icons are Lucide at 1.25px stroke** (softened from the original 1.75), set in **soft-blush pill tiles** with a subtle radial highlight. Glyphs stay **functional/financial** (`receipt`, `calculator`, `file-text`, …) — the brief was "softer styling, still financial icons," *not* decorative flower/heart glyphs.
4. **Sections never use burgundy-ink (`#2A0A1A`) as a large background.** The "case studies / the work" section uses **blush `#E0D0E0`** with white cards; hierarchy comes from a lifted "Featured" middle card (shadow + burgundy pill), not color inversion.
5. **No pricing tables.** Pricing was replaced with a **case studies / testimonials** section.
6. **Use the real logo PNGs.** The hand-rolled SVG marks (`paxus-mark.svg`, `paxus-mono-burgundy.svg`, `paxus-mono-cream.svg`) do **not** match the real rosette geometry — they're kept only for reference and should be treated as **deprecated**. Use `paxus-logo-full.png`, `paxus-wordmark.png`, `paxus-mark-real.png`, and the cream variants on dark.

---

## Sources

| Source | Path / link | Notes |
|---|---|---|
| Brand mark | `assets/paxus-logo-full.png` | Burgundy wordmark + pink rosette. Transparent PNG. |
| Inspiration design notes | (Wise.com structural language) | Type scale and component patterns carried across; colors swapped to Paxus. |
| Live reference | https://wise.com | Layout, motion, and component patterns. No Wise wordmark, illustration, or proprietary asset was copied. |

⚠️ No Paxus codebase or Figma was provided. The UI kits here are **original applications** of Paxus's brand to Wise-style layouts, retargeted to Paxus's real services. Treat them as a launch direction, not a recreation.

⚠️ **No proprietary fonts were provided.** Manrope 800 (display) and Source Serif 4 (body) are free Google Fonts substitutes. If Paxus adopts a licensed display face (Söhne, GT America) or a body serif (Tiempos, GT Sectra, Canela), drop the files into a `fonts/` folder and update `colors_and_type.css`.

---

## Repository index

```
README.md                  ← you are here (brand source of truth)
SKILL.md                   ← Agent Skills manifest
colors_and_type.css        ← all design tokens (CSS vars) + semantic classes

assets/                    ← logos, brand imagery
  paxus-logo-full.png      ← horizontal lockup (rosette + wordmark) — primary
  paxus-wordmark.png       ← wordmark only
  paxus-mark.png           ← rosette only (raster)
  paxus-mark-real.png      ← rosette only, original colors (watermark source)
  paxus-mark-cream.png     ← rosette only, recolored cream (reverse / on dark)
  paxus-logo-cream.png     ← full lockup, cream (reverse / on dark)
  paxus-mark.svg           ← ⚠️ DEPRECATED hand-rolled approximation
  paxus-mono-burgundy.svg  ← ⚠️ DEPRECATED hand-rolled approximation
  paxus-mono-cream.svg     ← ⚠️ DEPRECATED hand-rolled approximation

preview/                   ← 16 cards rendering tokens in context (open in a browser)
ui_kits/
  website/                 ← marketing site (final index.html reflects no-tax + case studies)
  portal/                  ← client portal (⚠️ still tax-themed — see "Known gaps")
```

---

## CONTENT FUNDAMENTALS

Two registers, both borrowed from Wise:

### 1. Confident, declarative headlines
Short, almost defiant. Sentence-case, no period, no qualifiers.

> **Books that balance themselves.**
> **Advisory that actually advises.**
> **Audit-ready, all year.**

Avoid corporate-accountancy clichés ("trusted partner", "comprehensive solutions", "best-in-class"). Headlines should be readable by a small-business owner who's never met an accountant. **No tax headlines** — Paxus doesn't do tax.

### 2. Plain, second-person body copy
Address the reader as "you". Refer to Paxus as "we" or "Paxus", never "the firm" or "our team of professionals". Contractions encouraged.

> "We close your books every month and tell you, in plain English, what the numbers say."

> "Need a CFO but not a CFO's salary? We sit in on the calls, build the model, and tell you what we'd do."

### Casing
- **Sentence case** for headlines, buttons, and nav.
- Title Case for proper-noun service names ("Paxus Year-Round Books") only.
- Buttons: verbs, sentence case — "Book a call", "See the work", "Sign in".

### Tone rules
- **Calm, never urgent.** No exclamation points outside microcopy ("Done!" after a successful action).
- **Specific, never vague.** Prefer "$240/month, billed quarterly" to "affordable pricing".
- **Numerate.** This is a CPA firm. "140+ active clients", "Avg. response time: 4 hours".
- **Empathetic about money.** People feel dumb about money. Don't compound it.

### What we don't do
- No emoji in product UI. (One careful exception: a 🎉 in a post-action confirmation screen.)
- No exclamation marks in headlines.
- No "leveraging", no "synergy", no "solutions".
- No tax language anywhere — Paxus refers out for tax.

---

## VISUAL FOUNDATIONS

### Color
The palette is **burgundy + blush + warm cream**, sampled from the logo. No greens, no blues — those are reserved exclusively for semantic states (success, info).

| Role | Token | Hex | Usage |
|---|---|---|---|
| Primary brand | `--paxus-burgundy` | `#681E44` | Wordmark, primary buttons, links, active nav |
| Brand pressed | `--paxus-burgundy-deep` | `#4A1430` | Active/pressed CTA, dark surfaces |
| Brand ink | `--paxus-burgundy-ink` | `#2A0A1A` | Footer / dark hero blocks only — **never** a large section background |
| Secondary accent | `--paxus-mauve` | `#B080A0` | Decorative only — never CTAs |
| Soft accent | `--paxus-blush` | `#E0D0E0` | Badges, selected pills, the "case studies" section background |
| Surface tint | `--paxus-blush-soft` | `#F2E8EE` | Section backgrounds, highlight cards |
| Canvas | `--paxus-cream` | `#FBF7F4` | Page background — warm, not white |
| Text primary | `--neutral-ink` | `#1A1217` | Body and headline text |

**Rules:**
- The canvas is **`#FBF7F4` cream**, not white. White (`#FFFFFF`) is reserved for cards that lift off the canvas.
- Burgundy is the **only** primary CTA color. Mauve and blush are for badges, accents, and decorative chips — never buttons.
- Keep burgundy under ~25% of any view. Cream + ink + the occasional burgundy block is the rhythm.

### Typography
- **Display:** Manrope 800. The weight is the identity — display headlines should feel **stamped**, billboard-scale. The contrast between the slim wordmark and heavy display type is intentional.
- **Body:** **Source Serif 4** (weight 400). A refined serif body against the heavy sans display reads professional without going law-firm-stuffy.
- **UI chrome:** Inter — buttons, nav, eyebrows, captions, inputs all force `--font-ui` for crispness.
- **Display line-height: 0.88–0.95** — tight. Manrope's metrics are taller than Wise Sans, so this is visually equivalent to Wise's 0.85.
- **OpenType `calt` and `ss01`** enabled globally.
- **Display sizes go big**: mega 112px, hero 88px, section openers 60px. Don't downscale "to be safe" — the ratio of headline to body IS the brand.

### Spacing
- 4px base unit. Scale: `4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128`.
- Vertical rhythm between sections: **96–128px** desktop, **64px** mobile.
- Card padding: **24–32px** small, **40–48px** large.

### Radii
| Element | Radius | Token |
|---|---|---|
| Tags, small chips | 4px | `--radius-xs` |
| Inputs, checkboxes | 8px | `--radius-sm` |
| Secondary cards | 14px | `--radius-md` |
| Cards (default) | 24px | `--radius-lg` |
| Hero / feature cards | 32px | `--radius-xl` |
| Large surfaces | 48px | `--radius-2xl` |
| Buttons (CTAs) | 9999px (pill) | `--radius-pill` |
| Avatars | 50% | circle |

### Elevation
**Ring shadows, almost exclusively.** Cards get a 1px ring (`var(--ring-2)`), inputs get an inset ring on focus. Drop shadows are reserved for floating elements (menus, toasts) and the lifted "Featured" case-study card — `var(--shadow-pop)` / `var(--shadow-deep)`.

```
--ring-2:      0 0 0 1px rgba(26,18,23,0.12);
--shadow-pop:  0 10px 30px -12px rgba(26,18,23,0.18), 0 0 0 1px rgba(26,18,23,0.06);
--focus-ring:  0 0 0 3px rgba(104,30,68,0.30);
```

### Backgrounds & imagery
- **Canvas:** flat warm cream. No gradients, no textures.
- **Hero blocks:** large flat-color burgundy or blush cards with 32–48px radii.
- **Photography:** warm, candid, real people. Avoid handshake/suit-pointing-at-laptop/calculator stock tropes. Prefer hands, paperwork, plants on a desk, coffee, a kitchen table — the actual context where small-business books happen.
- **No illustrations of money, briefcases, or graphs going up.** If a visual is needed, the rosette mark is the only decorative motif.
- **Decorative motif:** the **rosette** (`paxus-mark-real.png` / `paxus-mark-cream.png`) at low opacity (~6–8%) as a large background accent on dark hero/CTA blocks, contained inside the rounded card. Overuse cheapens it.

### Motion
- **`scale(1.03)` on hover** for primary CTAs (tamer than Wise's 1.05 — burgundy is heavier visually than lime).
- **`scale(0.97)` on active/press**.
- **Ease:** `cubic-bezier(0.22, 0.61, 0.36, 1)`, **200ms** default.
- **Page-level transitions:** opacity fades only. No slides, no parallax.
- **Hover on links:** color darkens to `--paxus-burgundy-deep`.
- **Hover on cards:** `translateY(-2px)` + bump ring-shadow opacity. Subtle.

### Borders
- Default: `1px solid rgba(26,18,23,0.12)`.
- Selected state: `1px solid var(--paxus-burgundy)`.
- Never use coloured borders for emphasis except burgundy. No left-accent-stripe cards.

### Transparency & blur
- **Sparingly.** Sticky headers use `backdrop-filter: blur(12px)` over `rgba(251,247,244,0.85)`.
- No blur on cards or modals — modals get a flat scrim (`rgba(26,18,23,0.40)`).

### Layout rules
- **Max content width:** 1200px desktop. Heroes can extend to 1400px.
- **Outer gutter:** 24px mobile, 48px tablet, 80px desktop.
- **Grid:** 12-column, 24px gutters on desktop.
- **Sticky header:** 64px tall, blur background.

---

## ICONOGRAPHY

**[Lucide](https://lucide.dev/)** at **1.25px stroke** is the sole icon system, set in soft-blush pill tiles.

```html
<script src="https://unpkg.com/lucide@latest"></script>
<i data-lucide="receipt"></i>
<script>lucide.createIcons();</script>
```

**Rules:**
- **Stroke 1.25px** — delicate, less utilitarian than the default 2px. Pairs with the slim wordmark.
- **Tile:** soft-blush (`#F2E8EE`) pill background with a subtle radial highlight — reads warm, not techy.
- **Glyphs stay functional/financial:** `receipt`, `calculator`, `file-text`, `line-chart`, `wallet`, `building-2`, `calendar`, `shield-check`. Soften the *styling*, not the meaning — these are still finance icons, not decorative flowers/hearts.
- **Color:** inherits from text (`currentColor`).
- **Size:** 16px (inline), 20px (UI), 24px (emphasis), 32–48px (feature blocks).
- **No emoji as iconography**, **no unicode symbols** (✓ ✗ →) — use Lucide's `check`, `x`, `arrow-right`. **No filled icons** in body UI; the rosette is the brand's only filled mark.

If a needed icon isn't in Lucide, draw it in the same style: 24×24 viewbox, 1.25px stroke, round caps/joins, no fills. Document additions in this README.

### Logo usage
- **Primary lockup:** `assets/paxus-logo-full.png` — rosette + wordmark. Light backgrounds, 48px+ height.
- **Wordmark only:** `assets/paxus-wordmark.png` — the PAXUS lettering only, **no rosette**, so it sits cleanly in thin headers/footers without anything clipping at the top edge. For the rosette + wordmark together, use `paxus-logo-full.png` instead.
- **Mark only:** `assets/paxus-mark.png` / `paxus-mark-real.png` — square contexts (avatar, favicon) and watermarks.
- **Reverse (on dark):** `assets/paxus-logo-cream.png` (lockup) or `paxus-mark-cream.png` (mark).
- **Clearspace:** at least the height of the "P" in PAXUS on all sides.
- **Don't:** recolor the rosette, place the logo on busy photography, add drop shadows, stretch it, or use the deprecated SVG marks.

---

## Known gaps in the bundled UI kits

These are real artifacts from the design session, carried forward honestly. Treat them as **layout/structure references**, and apply the brand rules above when building for real.

- **`ui_kits/website/`** — the final `index.html` reflects the correct direction (no tax; 4-card services for bookkeeping/CFO/audit/controller; a **case studies** section on `#E0D0E0`; burgundy footer). However `components.jsx` still contains a stale `PricingTable` and some tax-era copy, and the preview card subtitle mentions "pricing." Build from `index.html`'s final structure, not the leftover pricing component.
- **`ui_kits/portal/`** — ⚠️ **not updated for the no-tax pivot.** It still renders a `TaxTimeline` stepper and frames document upload around tax filing. This contradicts Paxus's actual services. Use it for component *structure* (sidebar, topbar, stat cards, doc list, next-call card) only — **rebuild its copy and flows around month-end close, advisory deliverables, audit prep, and controller reporting.** Do not ship the tax-filing timeline.

When in doubt, the order of authority is: **this README → `colors_and_type.css` → `preview/*.html` → the kits.**
