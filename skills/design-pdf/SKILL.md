---
name: design-pdf
description: Build a vertical (portrait) print-ready PDF from HTML — proposals, board packages, one-pagers, reports, handouts. Hands over a proven portrait scaffold where one HTML page equals one PDF sheet, then gives clean export steps. Pulls colors, type, and spacing from a design system if one is available; falls back to a neutral professional style. Run when the deliverable is a vertical document that needs to print cleanly to PDF.
---

# /design-pdf — Portrait PDF from HTML

You are helping the operator produce a **vertical (portrait), print-ready PDF document** — the kind of thing you hand a client: a proposal, a board package, a one-pager, a report, a handout. You do this by giving them a proven HTML scaffold (the dimensions and structure) and a reliable export path, not by hand-rolling print CSS from scratch. Follow the phases in order. Be conversational and warm — match the Paxus voice.

## The idea in one line

**One `<section class="page">` = one physical sheet.** What the operator sees in the browser is exactly what prints to PDF. The scaffold makes that true. The operator's job is to fill the pages; your job is to set up the scaffold, fit it to whatever design system applies, and get it exporting cleanly.

## Important rules for this skill

- **No fabrication.** If you don't have a real value — a recipient name, a number, a date — leave the template's `[bracketed placeholder]` in place and tell the operator to fill it. Never invent client details, figures, or branding.
- **Skills are the engine; design is the fuel.** The *dimensions and structure* are the engine — they ship in this skill's `templates/presentation.html` and work for any document. The *look* (colors, fonts, logo) is fuel: pull it from a design system when one exists, never hard-code a specific client's or firm's brand into this skill.
- **Don't reinvent the print CSS.** The hard-won part — page dimensions, the `@page` rule, the print media query, color preservation — already lives in the template. Adapt content and tokens; leave the dimension engine alone.
- **If `templates/presentation.html` is missing or unreadable**, stop and tell the operator the skill is corrupted and to re-install from the `paxus-skills` repo. Do not regenerate the template from memory.

---

## Phase 1 — Gather (batched)

Ask these in one message:

1. **What's the document?** (proposal, board package, one-pager, report, handout, other) — and roughly how many pages.
2. **Page size?** Default is **US Letter (8.5 × 11 in)**. Offer A4 if they're sending it internationally.
3. **Is there a design system or brand to follow?** "Point me at it — a file or folder (e.g. the client's `reference/` or `brand/` folder in the shared drive), a live website URL, or a set of brand colors/fonts. Or say *none* and I'll use a clean neutral style." (Per the firm's engine-vs-fuel rule, the design lives outside this skill — see `docs/context-model.md`.)
4. **Where should the finished file go?** Default to the current project's `deliverables/` folder if you're inside one.

Wait for the answers before building.

---

## Phase 2 — Pull the design system (or go neutral)

**If they pointed you at a design system:**

- Read it. Extract the tokens the scaffold uses: a primary/accent color, text color, a muted/secondary color, hairline/border color, heading font, body font. Note the logo if there is one.
- From a website URL: read the page and pull the dominant colors and font families. From a brand file/folder: read the tokens or style guide. From colors/fonts the operator typed: use those directly.
- **Only map what the design system actually specifies.** For anything it doesn't cover, keep the template's neutral default for that one token rather than inventing a value (no fabrication).
- **Logo:** reference or inline the operator's real logo file only. Never recreate a logo from memory or describe one that doesn't exist.

**If they said none:** use the template's neutral defaults as-is. They're already professional — clean serif headings, sans body, a deep-blue accent, gray hairlines.

Either way, the tokens are the only thing that changes. The geometry stays fixed.

---

## Phase 3 — Stand up the scaffold

1. **Copy** `templates/presentation.html` from this skill folder to the output location the operator chose, named for the document (e.g. `acme-q3-board-package.html`).
2. **Apply the tokens** by editing only the `:root` block — the `--color-*` and `--font-*` variables. Don't touch the `@page` rule, the `.page` width/height, or the `@media print` block.
3. **For A4:** in the template, set `@page { size: A4 portrait; }` and `--page-w: 210mm; --page-h: 297mm;`.
4. **Lay out the page types they need** by duplicating the example `<section class="page">` blocks — a cover, content pages, a data/table page, a closing page. Keep the operator's real content where you have it; leave `[bracketed placeholders]` everywhere you don't.
5. **Respect the page invariants** (these are what make export clean — do not change them):
   - Every sheet is a `<section class="page">`; one page element = one PDF sheet.
   - `overflow: hidden` clips anything past the sheet edge — so when a page is too full, **split it into two `<section class="page">` blocks** rather than shrinking text or removing the clip.
   - `print-color-adjust: exact` stays in — it's what keeps background colors and shaded boxes in the exported PDF.
   - The `@media print` block stays in — it strips the on-screen gray gutter and shadows so each sheet maps 1:1 to a PDF page.

---

## Phase 4 — Export (tell the operator exactly this)

Open the HTML file in **Google Chrome** (most reliable for print-to-PDF), then:

1. Press <kbd>Cmd</kbd> + <kbd>P</kbd> (macOS) or <kbd>Ctrl</kbd> + <kbd>P</kbd> (Windows).
2. **Destination:** Save as PDF.
3. **Paper size:** Letter (or A4 if that's what you built).
4. **Margins:** None.
5. **More settings → Background graphics:** ON. *(Without this, colored covers and shaded boxes print white.)*
6. Save.

---

## Phase 5 — Verify before done

- **Page count matches:** the PDF has the same number of sheets as `<section class="page">` blocks in the HTML. A mismatch means content overflowed onto an extra page — go back and split that page in Phase 3.
- **Nothing is clipped:** no sentence or table row is cut off at a page edge.
- **Colors survived:** the cover and any shaded boxes show their colors (if not, Background graphics was off).
- **Placeholders are gone:** no `[bracketed placeholder]` text remains in a file that's about to go to a client. If any real values are still unknown, tell the operator which ones.

Show the operator the file path and a one-line summary, then walk them through the export steps above.

---

## Phase 6 — Learnings capture (mandatory)

Ask, one at a time:

1. What was confusing, unclear, or wrong in building this PDF?
2. What should we add, remove, or change for the next run?

If they have feedback, append to `~/.claude/skills/design-pdf/learnings.md`:

```markdown
## {YYYY-MM-DD} — {operator first name} — {document type}
- [LEARNING] {answer to #1}
- [SUGGESTION] {answer to #2}
```

If `learnings.md` doesn't exist, create it with the header `# /design-pdf — Learnings` followed by the entry. If they say "nothing" to both, accept and move on.

---

## Edge cases

- **A page overflows.** The clip is intentional — it's the signal to split. Move the overflow into a new `<section class="page">`; never shrink the font or delete `overflow: hidden` to cram it in.
- **A table spans more than one page.** Repeat the `<thead>` on the second page's table so the columns stay labeled. Split the rows at a sensible boundary.
- **Fonts.** System fonts (the neutral default) always render. If the design system uses a custom font, add its Google Fonts `<link>` in the `<head>`; for a fully portable file with no internet, fall back to the closest system font.
- **A4 vs Letter.** Set both the `@page size` and the `--page-w` / `--page-h` variables, or the screen view and the PDF won't match.
- **Landscape.** This skill is portrait by design. If the operator truly needs landscape (a wide data table), set `@page { size: letter landscape; }` and swap the width/height variables — but confirm that's really what they want first.
- **Export looks fine on screen but the PDF clips or shifts.** Almost always Margins wasn't set to None, or they printed from a browser other than Chrome. Re-do the export steps in Chrome.
- **No design system and they want it to "look more like us" later.** That's fine — the tokens are isolated in `:root`, so the look can be retuned any time without touching content.
