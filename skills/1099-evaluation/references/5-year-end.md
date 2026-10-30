# Step 5: Year-end mode

Entry: the books are closed through 12/31 and the bank and card accounts are reconciled
(ask; don't assume). Exit: a "Year-End MM.DD.YYYY" tab, filled and compared.

1. `google.sheet.tab.add` "Year-End MM.DD.YYYY" in the existing file. Copy rows 1–5 from the
   Evaluation tab (`sheet.get` with formulas, then `sheet.update`), and write the K and O
   formulas down every data row (copy the Evaluation tab's row 6 formulas, adjusting the row
   number). Freeze 5 rows and 1 column; bold header; same column widths as far as possible.
2. Run step 2 for January 1 – December 31, with `--start-row 6`, writing to this tab (change
   `Evaluation!` to the new tab name in `rows.json`).
3. Carry forward from the first tab, by vendor name, every L–T answer people entered (and
   U). Never overwrite a cell that already has a value on the new tab.
4. Evaluate only what's new: vendors not on the first tab, vendors that crossed $2,000,
   vendors whose amount moved by more than 10%, and the watch list.
5. Re-check Drive `Taxes > W-9` for W-9s received since the first run; update P and R.
6. Outputs as step 4, limited to what changed, plus: vendors ready to file (W-9 on file,
   1099 needed) as the "Review and submit" subtask block, and the vendors still outstanding
   at the cut-off. After the cut-off, don't wait on missing W-9s; list them for the
   controller.
