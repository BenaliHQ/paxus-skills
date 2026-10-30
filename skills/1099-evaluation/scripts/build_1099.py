#!/usr/bin/env python3
"""Turn saved Transactions-by-Vendor pages into the 1099 evaluation rows.

Usage:
  python3 build_1099.py --pages <dir> --accounts <accounts.json> --out <dir>
                        [--start-row 6] [--client "Name"] [--period "..."]

--pages     folder of the raw quickbooks.report.transactions_by_vendor results,
            one file per call (any names; sorted by the first number in the
            name, so p0.md, p96.md ... works). Columns must be
            tx_date,txn_type,doc_num,account_name,split_acc,subt_nat_amount.
--accounts  JSON: {"bank": [...], "card": [...], "exclude_split": {"Name": "reason"},
            "exclude_vendor": {"Vendor name": "reason"}}
            Account names may be full ("Parent:Child") or leaf names. A row whose split
            account is one of the "bank" accounts is a transfer between the client's own
            accounts and is always dropped. exclude_vendor takes vendors off the list
            entirely (goods-only sellers, garnishment payees), named on "Not included".

Writes to --out:
  rows.json     sheet writes for A1:A3 and A<start>:J..., each <= 5,000 cells
  totals.json   one entry per vendor: total row number, bank-paid amount,
                card-paid amount (excluded), split accounts
  summary.md    vendors >= $2,000, watch list, excluded vendors, checks
"""
import argparse, json, os, re, sys
from collections import OrderedDict, defaultdict

KEEP_TYPES = {"Expense", "Check", "Bill Payment (Check)", "Cash Expense", "Bill Payment (Cash)"}
# Vendors that are never 1099 recipients (payroll providers, tax agencies, card
# issuers, title companies, merchant processors). Matched case-insensitively.
EXCLUDE_VENDOR = [
    (r"\b(gusto|adp|paychex|paylocity|ludt payroll|asure|intuit payroll|quickbooks payroll|payroll)\b", "payroll provider"),
    (r"^(irs|internal revenue|us treasury|united states treasury|oklahoma tax commission|otc|eftps)\b", "tax agency"),
    (r"\b(capital one|american express|amex|discover card|card services|credit card)\b", "credit card payment"),
    (r"\btitle\b", "title company / closing"),
    (r"^intuit\b", "merchant / software fees"),
    (r"^(square|toast|clover)\b", "merchant / POS fees"),
    (r"^cash$", "register change / petty cash"),
]
EXCLUDE_SPLIT_WORDS = [
    (r"\bowner", "owner pay / draws"), (r"\bdraw", "owner pay / draws"), (r"\bdistribution", "owner pay / draws"),
    (r"\bguaranteed\b", "owner guaranteed payments"),
    (r"\bearnest money\b", "earnest money"), (r"\butilit", "utility"), (r"\binsurance\b", "insurance"),
    (r"\bbank (charges|fees|service)", "bank fees"), (r"\bwages\b|\bpayroll\b|\bsalar", "payroll"),
    (r"^(?!.*(prof|prep|servic|advis|account|planning)).*\btax(es)?\b", "taxes"),
]

def leaf(n): return n.split(":")[-1].strip()

def num(s):
    s = s.replace(",", "").replace("$", "").strip()
    if s.startswith("(") and s.endswith(")"): s = "-" + s[1:-1]
    return float(s) if s not in ("", "-") else 0.0

def parse_pages(d):
    files = sorted(os.listdir(d), key=lambda f: int((re.findall(r"\d+", f) or ["0"])[0]))
    vendor, rows = None, []
    for f in files:
        for line in open(os.path.join(d, f), encoding="utf-8"):
            line = line.strip()
            if not line.startswith("|") or line.startswith("|---") or line.startswith("| Date"): continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            first = cells[0]
            m = re.match(r"^\*\*(.+)\*\*$", first)
            if m and not first.startswith("**TransactionList"): vendor = m.group(1); continue
            if first.startswith("*Total for"): continue
            if first.startswith("·"):
                if vendor is None: sys.exit(f"detail row before any vendor header in {f}")
                while len(cells) < 6: cells.append("")
                rows.append([vendor, first.lstrip("· ").strip()] + cells[1:6])
    return rows

def fmt_date(d):
    y, m, dd = d.split("-"); return f"{m}/{dd}/{y}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", required=True); ap.add_argument("--accounts", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--start-row", type=int, default=6)
    ap.add_argument("--client", default=""); ap.add_argument("--period", default="")
    a = ap.parse_args()
    acc = json.load(open(a.accounts))
    bank = {leaf(x) for x in acc.get("bank", [])} | set(acc.get("bank", []))
    card = {leaf(x) for x in acc.get("card", [])} | set(acc.get("card", []))
    ex_split = {}
    for k, v in acc.get("exclude_split", {}).items(): ex_split[k] = v; ex_split[leaf(k)] = v
    for b in bank: ex_split.setdefault(b, "transfer between own accounts")
    ex_vendor = {k.lower(): v for k, v in acc.get("exclude_vendor", {}).items()}
    raw = parse_pages(a.pages)
    if not raw: sys.exit("no detail rows parsed — check the pages folder")

    data, card_paid, excluded, ex_rows = OrderedDict(), defaultdict(float), {}, defaultdict(float)
    billsplit = defaultdict(set)
    for v, d, t, num_, acct, split, amt in raw:
        if t == "Bill": billsplit[v].add(split)
    for v, d, t, num_, acct, split, amt in raw:
        reason = ex_vendor.get(v.lower()) or next((r for p, r in EXCLUDE_VENDOR if re.search(p, v, re.I)), None)
        x = num(amt)
        if acct in card or leaf(acct) in card:
            if t != "Bill": card_paid[v] += abs(x)
            continue
        if t not in KEEP_TYPES: continue
        if acct not in bank and leaf(acct) not in bank: continue
        paid = -x  # bank outflows are negative on this report
        if reason: excluded[v] = reason; ex_rows[v] += paid; continue
        if t.startswith("Bill Payment") and len(billsplit[v]) == 1: split = list(billsplit[v])[0] + " (via bill)"
        sreason = ex_split.get(split) or ex_split.get(leaf(split.replace(" (via bill)", ""))) or \
                  next((r for p, r in EXCLUDE_SPLIT_WORDS if re.search(p, split, re.I)), None)
        if sreason and split not in ("-Split-",):
            excluded.setdefault(v, sreason); ex_rows[v] += paid; continue
        data.setdefault(v, []).append([d, t, num_, acct, split, paid])

    body, totals, r = [], {}, a.start_row
    for v in sorted(data, key=str.lower):
        body.append([v] + [""] * 9); r += 1; bal = 0.0; splits = defaultdict(float)
        for d, t, n, acct, split, paid in sorted(data[v]):
            bal += paid; splits[split] += paid
            body.append(["", split, fmt_date(d), t, n, "", split, acct, round(paid, 2), round(bal, 2)]); r += 1
        body.append([f"Total for {v}", "", "", "", "", "", "", "", round(bal, 2), ""])
        totals[v] = {"row": r, "amount": round(bal, 2), "card_paid_excluded": round(card_paid.get(v, 0), 2),
                     "splits": {k: round(s, 2) for k, s in sorted(splits.items(), key=lambda i: -i[1])}}
        r += 1
    grand = round(sum(t["amount"] for t in totals.values()), 2)
    body.append(["TOTAL", "", "", "", "", "", "", "", grand, ""]); total_row = r; r += 1
    body.append([""] * 10); r += 1
    exl = sorted(excluded.items())
    body.append(["Not included (not 1099 categories): " + "; ".join(f"{k} ({v})" for k, v in exl)] + [""] * 9)

    writes = [{"range": "Evaluation!A1:A3", "values": [[a.client], ["1099 Report"], [a.period]]}]
    step = 500  # 500 rows x 10 columns = 5,000 cells
    for i in range(0, len(body), step):
        chunk = body[i:i + step]; s = a.start_row + i
        writes.append({"range": f"Evaluation!A{s}:J{s + len(chunk) - 1}", "values": chunk})
    os.makedirs(a.out, exist_ok=True)
    json.dump({"writes": writes, "last_row": a.start_row + len(body) - 1, "total_row": total_row},
              open(os.path.join(a.out, "rows.json"), "w"), indent=1)
    json.dump(totals, open(os.path.join(a.out, "totals.json"), "w"), indent=1)

    over = sorted([(v, t) for v, t in totals.items() if t["amount"] >= 2000], key=lambda i: -i[1]["amount"])
    watch = sorted([(v, t) for v, t in totals.items() if 1500 <= t["amount"] < 2000], key=lambda i: -i[1]["amount"])
    neg = [(v, t) for v, t in totals.items() if t["amount"] < 0]
    with open(os.path.join(a.out, "summary.md"), "w") as f:
        f.write(f"Detail rows parsed: {len(raw)}; vendors kept: {len(totals)}; bank-paid total {grand:,.2f}; "
                f"sheet rows {a.start_row}–{a.start_row + len(body) - 1}; TOTAL row {total_row}\n\n")
        f.write("## Vendors at $2,000+ (row, amount, top accounts, card-paid excluded)\n")
        for v, t in over:
            top = ", ".join(f"{k} {s:,.0f}" for k, s in list(t["splits"].items())[:3])
            f.write(f"- row {t['row']} | {v} | {t['amount']:,.2f} | {top}" +
                    (f" | card {t['card_paid_excluded']:,.0f}" if t["card_paid_excluded"] else "") + "\n")
        f.write("\n## Watch list ($1,500–$1,999.99)\n" + "".join(f"- {v} | {t['amount']:,.2f}\n" for v, t in watch))
        f.write("\n## Excluded vendors (bank-paid amount dropped)\n" + "".join(f"- {v} | {r} | {ex_rows[v]:,.2f}\n" for v, r in exl))
        if neg: f.write("\n## Negative totals (refunds or credits — check)\n" + "".join(f"- {v} | {t['amount']:,.2f}\n" for v, t in neg))
    print(open(os.path.join(a.out, "summary.md")).read())

if __name__ == "__main__":
    main()
