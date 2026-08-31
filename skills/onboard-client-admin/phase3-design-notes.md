---
title: Phase 3 design notes (Welcome Packet via Canva)
status: built and working — first production run 2026-06-26
last_updated: 2026-06-26
---

# /onboard-client-admin — Phase 3 design notes

Phase 3 = generate a personalized welcome packet in Canva, save it to the client's Shared Drive, and draft the welcome email. **Working end-to-end as of 2026-06-26.** Build the SKILL.md section against this file's pattern.

---

## Confirmed working pattern

1. Operator picks the package (Full Service / Basic / Premium) and confirms which 3 team members fill Controller / Lead / Staff roles for this client.
2. `copy-design` from the package's master ID → throwaway copy.
3. `start-editing-transaction` on the copy.
4. `find_and_replace_text` swaps on:
   - Page 1 cover: package-name placeholder → **client legal name** (wraps to 2 lines for long names, looks fine).
   - Page 7 Lisa thank-you: `XXXXX` → **client legal name** (inline in prose, accepts longer names cleanly).
5. `update_title` to `{Client legal name} - Welcome Packet`.
6. `commit-editing-transaction`.
7. For each of the 3 assigned team members:
   - Build `https://lh3.googleusercontent.com/d/{FILE_ID}` from the Drive file ID for their Bios PNG.
   - `upload-asset-from-url` to ingest into Canva → asset ID returned.
8. `start-editing-transaction` (new transaction).
9. `insert_fill` for Controller/Lead/Staff in top-to-bottom order on page 2 — 693×260 px, left=62, tops 170 / 450 / 730.
10. `commit-editing-transaction`.
11. `move-item-to-folder` → final packets folder (see IDs below).
12. `export-design` as PDF (letter, pro quality).
13. `curl -o` the export URL into `G:\Shared drives\{Client legal name}\Perm File\Welcome Packet - {Client legal name}.pdf`.
14. Render the welcome email from `welcome-email-template.md` with placeholders filled, write to handoffs folder for operator to paste/send.

### Why each step works (don't re-probe)

- All pages on every master are `is_responsive: false` → full `perform-editing-operations` set is available, including `insert_fill`.
- `find_and_replace_text` operates on a specific `element_id`; the cover and Lisa-thank-you elements are stable across the masters since they were all derived from the Full Service master.
- `upload-asset-from-url` REJECTS:
  - Canva's own export-download URLs (private signed S3, requires `x-amz-expected-bucket-owner`).
  - Drive's `https://drive.google.com/uc?export=download&id={ID}` (returns HTTP 303 redirect, Canva won't follow).
- `upload-asset-from-url` ACCEPTS `https://lh3.googleusercontent.com/d/{FILE_ID}` (returns HTTP 200 with `Content-Type: image/png`).
- File IDs can be parsed from a public Drive folder's HTML — grep `data-id="..."` or look at character-range hits near the filename.

---

## Canva IDs (confirmed 2026-06-26)

### Master welcome packet templates
| Package | Design ID | Shortlink |
|---|---|---|
| Full Service | `DAHMXYL-a5g` | (no shortlink captured — open via web for now) |
| Basic | `DAHNmFp_ltM` | https://canva.link/ey6mftkakq5h5by |
| Premium | `DAHNmNfCQw8` | https://canva.link/1zl9eu80l0w1ld6 |

All three masters share the same page structure and placeholder pattern (cover package-name + page 7 `XXXXX`). Confirm element IDs on each master at first use — they should be similar to Full Service's but verify before relying on cached IDs.

### Destination folder (final packets)
- **Folder ID:** `FAF-ADpbNnU` (https://www.canva.com/folder/FAF-ADpbNnU)
- Operator's stated location to save each finished client packet.
- Use `move-item-to-folder` after committing edits.

### Master Templates folder (don't write here)
- `FAF-AHGkFs0` — holds the 3 master designs and the team-member single-page blocks. Never edit anything here directly.

---

## Full Service master — page structure & key element IDs

(Likely the same on Basic/Premium since they were derived. Verify on first run with each.)

| Page | Page ID | Content | Notes |
|---|---|---|---|
| 1 | `PBBmQW3jLpcqG42m` | Cover: "Welcome Packet" / package name / Paxus office photo | Swap `FULL SERVICE` text element → client legal name |
| 2 | `PBNnwHFmMBcnzmd4` | "Meet Your Team" title (top) + URL (bottom) | Insert 3 team blocks at 693×260, left=62, tops 170/450/730 |
| 3 | `PBTh9HcnflqPLLTs` | Mission and values | No edits |
| 4 | `PBqd7FZwX2Bhjcxk` | What we need from you | No edits |
| 5 | `PBQHCV4YGGLdZx1b` | Client Portal | No edits |
| 6 | `PBS3v9gZrj5bKyb0` | What we provide | No edits |
| 7 | `PBfbgrMgx6k3P9Mm` | Lisa thank-you + group photo | Swap `XXXXX` text element → client legal name |

**Full Service stable element IDs (don't refetch unless missing):**
- Page 1 "FULL SERVICE": `PBBmQW3jLpcqG42m-LBNJHY2pW54z1Fnf`
- Page 7 "XXXXX": `PBfbgrMgx6k3P9Mm-LBVBvW2L098zGTDK`

---

## Team-member assets (Drive PNGs)

**Bios folder** (publicly shared, "anyone with the link can view"):
- Folder: https://drive.google.com/drive/folders/1L16UTDzb27mHmpcHJQprVkOxiwqHcZqV
- Folder ID: `1L16UTDzb27mHmpcHJQprVkOxiwqHcZqV`
- Path on disk: `G:\Shared drives\00 - Paxus CPA\Admin\Website\Bios\`

**File ID map** (parse from folder HTML on first use, then cache here):
| File | Drive file ID | Canonical Canva direct URL |
|---|---|---|
| 1_Cassie Rigsby.png | `1ThyCuUzlm4V4vTSKizYFYAIqRIVphx7a` | https://lh3.googleusercontent.com/d/1ThyCuUzlm4V4vTSKizYFYAIqRIVphx7a |
| 8_Joyce Maregmen.png | `11wk1kGoGal2CaC2NrbZhOWlzWm4OYgjH` | https://lh3.googleusercontent.com/d/11wk1kGoGal2CaC2NrbZhOWlzWm4OYgjH |
| 9_Rachel Hastings.png | `1X5fgFBWX-niiIAqav03kIwCQzLCSZ2xS` | https://lh3.googleusercontent.com/d/1X5fgFBWX-niiIAqav03kIwCQzLCSZ2xS |
| 2_Megan States.png | TBD | TBD |
| 3_Becky Humphers.png | TBD | TBD |
| 4_Caroline Jeffreys.png | TBD | TBD |
| 5_Landry Greenhill.png | TBD | TBD |
| 6_Kristie Andrews.png | TBD | TBD |
| 7_Consuelo Gervacio.png | TBD | TBD |
| 10_Michelle Mauldin.png | TBD | TBD |

**How to look up a new file ID:** `curl -sL "https://drive.google.com/drive/folders/1L16UTDzb27mHmpcHJQprVkOxiwqHcZqV" -A "Mozilla/5.0" -o /tmp/bios.html` and grep for `data-id="..."` near the filename. Fill in this table as IDs become known so future runs skip the HTTP step.

**Each block is 1600×600 PNG (8:3 aspect).** When `upload-asset-from-url` succeeds you get an asset ID like `MAHNr7wzfPw` that lasts for the team's Canva account.

---

## Welcome email

Template lives at `~/.claude/skills/onboard-client-admin/welcome-email-template.md` (approved by Jennifer 2026-06-26). Placeholders to fill per client: client name, contact first name, onboarding fee, cleanup deposit, monthly fee, start month, Lead name, Controller name.

**Staff Accountant is intentionally "TBD" in the email** even when assigned internally — the packet page 2 shows the staff member but the email keeps that line open until services begin.

**Delivery (updated 2026-07-22):** create the email as a **live Gmail draft** via `mcp__claude_ai_Gmail__create_draft`, and keep a markdown archive in the client's Perm File. See SKILL.md Phase 3H for the exact call. The draft tool takes bare email addresses only (no `Name <email>`), uses plain-text `body`, no sign-off (Gmail signature auto-appends).

**Attaching the packet — CORRECTED 2026-08-31:** the draft tool's schema DOES accept attachments (base64 `content` in an `attachments` array) — it's not a missing capability. But a real welcome packet PDF (even "regular" export quality, ~1-1.5MB) base64-encodes to ~1.5-2M characters, and base64 tokenizes at close to 1 token per character — embedding that inline would take ~1.5-2M tokens in one tool call, which no single assistant turn can produce. This is a hard ceiling on assistant output, not a tool limitation. **Jennifer still attaches the packet PDF manually before sending** — don't keep re-attempting this per client.

**Recipients:**
- TO: primary contact from FC (Phase 1 handoff)
- CC: Lead + Controller + Staff + lisa@paxuscpa.com
- Attach (manual): the rendered Welcome Packet PDF from Drive

---

## Known layout issues + fixes (found 2026-08-31, check on every client)

**Page 1 title can overlap the photo when the client name wraps to 2 lines.** The title text box auto-grows in height when `find_and_replace_text` produces a longer string, but it grows *downward* from the same anchored `top` — so a 2-line client name (most names longer than "FULL SERVICE"/"BASIC"/"PREMIUM") pushes the second line down toward the fixed-position photo below it. Always check the after-thumbnail for this. Fix: `position_element` to move the title's `top` up (e.g., from ~204 to ~90) so the taller box has room before the photo starts (~327). A single-line name may not need this — only reposition if the thumbnail actually shows tight/overlapping spacing.

**Page 2 team blocks look off-center when fewer than 3 are placed.** The default positions (tops 170/450/730) assume all 3 slots are filled. If Staff is `TBD` and only 2 blocks are inserted, they sit high on the page with a large empty gap below — not vertically balanced. Fix: reposition both used blocks to center as a pair between the "Meet Your Team" title (bottom ~166) and the footer URL (top ~993) — e.g., tops 290 and 610 (matches the exact gap of 3 blocks, 260 each, but centered as 2). Recompute if the actual title/footer positions differ on a master.

Both fixes are per-page `position_element` operations inside the existing editing transaction — no new transaction needed if caught before commit; if caught after commit (as happened here), open a fresh transaction, fix, commit again, and re-export.

---

## First production run (2026-06-26)

- Client: (first production run — client identity omitted per no-client-data rule)
- Package: Full Service
- Team blocks placed in Controller / Lead / Staff order on page 2.
- Canva working copy moved to `FAF-ADpbNnU` before export.
- PDF: `G:\Shared drives\{Client legal name}\Perm File\Welcome Packet - {Client legal name}.pdf` (~11-12 MB at pro quality).
- Email: archived in the client's Perm File as `Welcome Email - {Client legal name}.md` (see SKILL.md Phase 3H).
- Jennifer's tweak: small spacing adjustments on page 2 done manually post-commit — the re-export captured them.

---

## Still to build out

1. **SKILL.md section.** Encode the pattern above as "Phase 3 — Welcome Packet" in the main SKILL.md. Wire it to the package selection captured in Phase 1.
2. **Team-block file ID lookup.** Either (a) cache as more clients run and fill in the TBD rows above, or (b) automate the folder-HTML scrape with a small Python helper.
3. **Auto-detect element IDs on Basic/Premium masters.** Don't hardcode the Full Service IDs — at first run for each package, `start-editing-transaction` and parse out the elements matching "FULL SERVICE"/"BASIC"/"PREMIUM" and `XXXXX`.

---

## Safety notes (still apply)

- **Never edit the 3 master designs directly.** `copy-design` first.
- **Never edit team-member block designs directly** — they're shared assets across all clients.
- The throwaway-to-deliverable optimization works: there's no need to make a second copy after probing on a copy. The "throwaway" IS the deliverable once probes succeed.
