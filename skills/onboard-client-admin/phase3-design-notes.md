---
title: Phase 3 design notes (Welcome Packet via Canva)
status: built and working — first production run 2026-06-26
last_updated: 2026-06-26
---

# /onboard-client-admin — Phase 3 design notes

Phase 3 = generate a personalized welcome packet in Canva, save it to the client's Shared Drive, and draft the welcome email. **Working end-to-end as of 2026-06-26** — verified on a first production run that day. Build the SKILL.md section against this file's pattern.

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
| Cassie Rigsby.png | `1ecgr3re1JZhXIEKJ7KjzQiiXasxLismz` | https://lh3.googleusercontent.com/d/1ecgr3re1JZhXIEKJ7KjzQiiXasxLismz |
| 8_Joyce Maregmen.png | `11wk1kGoGal2CaC2NrbZhOWlzWm4OYgjH` | https://lh3.googleusercontent.com/d/11wk1kGoGal2CaC2NrbZhOWlzWm4OYgjH |
| 9_Rachel Hastings.png | `1X5fgFBWX-niiIAqav03kIwCQzLCSZ2xS` | https://lh3.googleusercontent.com/d/1X5fgFBWX-niiIAqav03kIwCQzLCSZ2xS |
| 2_Megan States.png | TBD | TBD |
| 3_Becky Humphers.png | TBD | TBD |
| 4_Caroline Jeffreys.png | TBD | TBD |
| 5_Landry Greenhill.png | `1UJno3wx-VJzMcwcNzfVMHv-LZLRWt4bz` | https://lh3.googleusercontent.com/d/1UJno3wx-VJzMcwcNzfVMHv-LZLRWt4bz |
| 6_Kristie Andrews.png | `1LNm9l7l_rjppcOUe6_Clh-Se86dcVpJQ` | https://lh3.googleusercontent.com/d/1LNm9l7l_rjppcOUe6_Clh-Se86dcVpJQ |
| 7_Consuelo Gervacio.png | TBD | TBD |
| 10_Michelle Mauldin.png | `1dgNzMOKnGC8zGHtebxu9zb7EhAczxOJm` | https://lh3.googleusercontent.com/d/1dgNzMOKnGC8zGHtebxu9zb7EhAczxOJm |

**How to look up a new file ID:** `curl -sL "https://drive.google.com/drive/folders/1L16UTDzb27mHmpcHJQprVkOxiwqHcZqV" -A "Mozilla/5.0" -o /tmp/bios.html` and grep for `data-id="..."` near the filename. Fill in this table as IDs become known so future runs skip the HTTP step.

**Each block is 1600×600 PNG (8:3 aspect).** When `upload-asset-from-url` succeeds you get an asset ID like `MAHNr7wzfPw` that lasts for the team's Canva account.

---

## Welcome email

Template lives at `~/.claude/skills/onboard-client-admin/welcome-email-template.md` (approved by Jennifer 2026-06-26). Placeholders to fill per client: client name, contact first name, onboarding fee, cleanup deposit, monthly fee, start month, Lead name, Controller name.

**Staff Accountant is intentionally "TBD" in the email** even when assigned internally — the packet page 2 shows the staff member but the email keeps that line open until services begin.

**Delivery (updated 2026-07-22):** create the email as a **live Gmail draft** via `mcp__claude_ai_Gmail__create_draft`, and keep a markdown archive in the client's Perm File. See SKILL.md Phase 3H for the exact call. The draft tool takes bare email addresses only (no `Name <email>`), uses plain-text `body`, no sign-off (Gmail signature auto-appends), and **cannot attach files** — Jennifer attaches the packet PDF manually before sending.

**Recipients:**
- TO: primary contact from FC (Phase 1 handoff)
- CC: Lead + Controller + Staff + lisa@paxuscpa.com
- Attach (manual): the rendered Welcome Packet PDF from Drive

---

## First production run (2026-06-26)

- Package: Full Service
- Team: Cassie (Controller), Rachel (Lead), Joyce (Staff)
- Canva design: `DAHNrogt5Ac` (moved to `FAF-ADpbNnU`)
- PDF exported at 11.6 MB, filed to the client's Perm File as usual.
- Jennifer's tweak: small spacing adjustments on page 2 done manually post-commit — the re-export captured them.

---

## Second production run (2026-08-07)

- Package: Premium (master `DAHNmNfCQw8`)
- Team: Kristie Andrews (Controller), Rachel Hastings (Lead) — **intern excluded** (Staff = Paxus Intern/Macie), so only 2 blocks on page 2.
- Canva design: `DAHRpD4x9Gw` (moved to `FAF-ADpbNnU`)
- PDF exported at 10.68 MB, filed to the client's Perm File as usual.
- **Premium master element IDs confirmed identical to Full Service:** page 1 cover `PBBmQW3jLpcqG42m-LBNJHY2pW54z1Fnf`, page 7 XXXXX `PBfbgrMgx6k3P9Mm-LBVBvW2L098zGTDK`. Cover placeholder text is `PREMIUM SERVICE`.
- **Page-7 double-space fix:** the placeholder is `have XXXXX  as` (two spaces). Use `find_and_replace_text` on `have XXXXX  as` → `have {name} as` to avoid a leftover double space.
- **2-block layout (intern excluded):** Premium page 2 = `PBNnwHFmMBcnzmd4`. Placed blocks at 693×260, left=62, **tops 330 (Controller) / 665 (Lead)** — centered in the open area below the title/divider with balanced top/bottom gaps. Looks clean; use this when only 2 team members are client-facing.

## Third production run (2026-08-12)

- Package: Basic (master `DAHNmFp_ltM`)
- Team: Rachel Hastings (Controller), Landry Greenhill (Lead) — Staff = TBD, so 2-block layout (tops 330 / 665, left 62, 693×260).
- Canva design: `DAHSGTT-OAg` (moved to `FAF-ADpbNnU`); PDF 11.1 MB in Perm File.
- **Basic master element IDs confirmed identical to Full Service:** page 1 cover `PBBmQW3jLpcqG42m-LBNJHY2pW54z1Fnf` (text `BASIC SERVICE`), page 7 XXXXX `PBfbgrMgx6k3P9Mm-LBVBvW2L098zGTDK` (same `have XXXXX  as` double-space — replace `have XXXXX  as` → `have {name} as`).
- Canva API is now transaction-based: `read-design(open_transaction:true)` → `edit-design(operations, finalize:"keep_open")` per page → `edit-design(finalize:"commit")`. (Old start/perform/commit-editing-transaction tools are gone.)
- **Role-label gotcha:** when a person serves a role their bio PNG isn't labeled for (here Rachel = Controller but her standard block says "Lead Accountant"), page 2 shows a mismatched/duplicate label. Resolved this run: Jennifer dropped `Rachel Hastings - Controller.pdf` (Drive id `14ZYA1eHINU6qJjQudUEyanM3v1Jp1IxY`) into the Bios folder; swapped it onto the top block via `update_fill`.
- **Bios can arrive as PDF, and lh3 renders a Drive PDF to an image.** `https://lh3.googleusercontent.com/d/{PDF_FILE_ID}=s1600` returns a clean rendered PNG (this one came back 1024×384, the correct 8:3 block aspect, no page margins) — upload that URL to Canva just like a PNG. No local PDF→PNG converter needed (none installed on this machine anyway: no magick/pdftoppm/fitz).
- **lh3 CDN caches in-place content updates.** When a bio is updated *in place* (same Drive file id), re-ingesting the same `lh3/d/{id}` URL can return the STALE image (hit this first — got the old "Lead Accountant" render back). Always verify the after-thumbnail shows the new content before committing; a brand-new file id (like the Controller PDF) sidesteps the cache.

## Still to build out

1. **SKILL.md section.** Encode the pattern above as "Phase 3 — Welcome Packet" in the main SKILL.md. Wire it to the package selection captured in Phase 1.
2. **Team-block file ID lookup.** Either (a) cache as more clients run and fill in the TBD rows above, or (b) automate the folder-HTML scrape with a small Python helper.
3. **Auto-detect element IDs on Basic/Premium masters.** Don't hardcode the Full Service IDs — at first run for each package, `start-editing-transaction` and parse out the elements matching "FULL SERVICE"/"BASIC"/"PREMIUM" and `XXXXX`.

---

## Safety notes (still apply)

- **Never edit the 3 master designs directly.** `copy-design` first.
- **Never edit team-member block designs directly** — they're shared assets across all clients.
- The throwaway-to-deliverable optimization works: there's no need to make a second copy after probing on a copy. The "throwaway" IS the deliverable once probes succeed.
