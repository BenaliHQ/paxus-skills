# Step 3: Evaluate and write the file

Entry: `summary.md` and `totals.json`. Exit: the evaluation file filled; one line per $2,000+
vendor ready for the outputs.

## 3.1 Gather, once, for every vendor at $2,000+

- **QBO vendor fields**: `quickbooks.query`
  `select Id, DisplayName, Vendor1099, TaxIdentifier, PrimaryEmailAddr from Vendor where DisplayName in (...)`
  — 15 or so names a call; escape an apostrophe in a name as `\'`. TaxIdentifier comes back
  masked, and sometimes empty even when a TIN is on file: not proof either way.
- **QBO attachments**: `select Id, FileName, AttachableRef from Attachable where AttachableRef.EntityRef.Type = 'Vendor' maxresults 200`
  (page with `startposition` if full). Match `EntityRef.value` to the vendor Id.
- **Drive W-9s**: every file in `Taxes > W-9` and its subfolders. Match by vendor or
  owner name (file names are inconsistent).
- **Prior year**: last year's evaluation file, or for the 2025 tax year the "2025 Paxus 1099"
  Sheet (client name in column A; vendor rows below from column I: Vendor Name, …, Received
  W9, 1099 Required, …, Type of 1099 Filed). Use it only to know a W-9 is on file and how the
  vendor was treated. Never flag a missed past filing.

## 3.2 Decide, per vendor

Sources in this order; record which one decided it in NOTES.

1. **Entity type.** The QBO display-name suffix ("- Indiv", "- S-Corp", "- Corp",
   "- Pship"); then the W-9 in Drive (`google.file.get` reads PDFs through text recognition;
   read box 3a). An LLC with no tax classification entered is not a corporation. A
   handwritten mark the text can't show: say "W-9 box unreadable" and leave the answer
   blank. Inc, Corp or Co in the legal name and nothing else: a corporation, noted as
   "by name". Banks: corporations.
2. **Exceptions** for corporations: legal services (attorneys, law firms) and medical or
   health care. These get a 1099 even as corporations.
3. **1099 type** (column S, the template's list): NEC for services; MISC - Rents for rent and
   equipment rental; MISC - Attorney proceeds for settlements paid through an attorney;
   MISC - Medical; INT for interest paid to a non-bank lender ($600+ of interest; principal
   is never reportable).
4. **W-9 ON FILE?** Yes when a W-9 is in Drive, attached in QBO, or last year's sheet shows
   it received or a 1099 filed for this payer. Otherwise No.

Answer the columns:

- L IS A CORPORATION?: YES or NO; blank when unknown (the row shows CHECK).
- M and N: when L is YES, YES or NO each. When L is NO, follow the template's Instructions
  tab (the 2026 master says to leave them blank; a later version may say N/A).
- P, S, T as above. Leave Q, R and U empty on a build: they are dates people enter.
- NOTES (T), one or two sentences: entity source, W-9 location ("W-9 in Drive + QBO"), what
  the person must do, and the vendor's email if QBO has one. Examples:
  - "W-9 (single-member LLC, 2/13/24) in Drive + QBO. QBO Track 1099 NOT checked — check it."
  - "S corp (W-9 in Drive + QBO). No 1099. QBO Track 1099 is checked — uncheck."
  - "New vendor. No W-9, no email in QBO. Need email from client."

Flag (for the flag list, not decided by the skill): owners, family of owners, related
companies, and employees also paid as vendors; foreign vendors; trusts and estates; a vendor
under two names; payees whose name doesn't fit the account (a "consulting" LLC coded to
labor); a payee called "Rent" or similar with no landlord named; government entities.

## 3.3 Write the file

1. Initial mode: `google.sheet.clear` A6:T (in 5,000-cell parts) to remove the template's
   example rows. Then each write in `rows.json` with `google.sheet.update`.
2. If the last row passes the rows that carry the K and O formulas, copy the formulas down
   with `sheet.update` (formulas, one per row) before anything else.
3. For each $2,000+ vendor, write L:N, P, S:T on its Total row (`totals.json` gives the row).
   Batch them: one `sheet.update` per contiguous range is fine; keep each call under 5,000
   cells.
4. `google.sheet.format` I:J as `#,##0.00` for the data rows; `google.sheet.layout`: freeze
   5 rows and 1 column (unmerge A1:J3 first if the template merged them).
5. Read back the Total rows (`google.sheet.get` on K:P for those rows) and count YES, CHECK,
   NO in column O. The counts go in the summary.
