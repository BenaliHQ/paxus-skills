#!/usr/bin/env python3
"""
gl-volume.py — derive pricing volume inputs from a QuickBooks Online General Ledger export.

Usage:
    python3 gl-volume.py "<GL export.xlsx>" [--months 01,02,03,04,05,06,07]

Returns the inputs Phase 0 of /paxus-quote consumes:
  * coding decisions per month  -> staff coding hours at 50/hr
  * bills entered per month     -> staff bill-entry hours at 2 min each
  * per-account line volume     -> reconciliation banding (20/10/5 min)
  * a lapse flag on any bookkeeper-driven count that stopped mid-period

No third-party packages. Reads the .xlsx directly.

WHAT COUNTS
  Register lines are rows whose distribution account is a bank or credit-card
  account. A GL lists each transaction under every account it touches, so raw
  GL rows run several times the register-line count. Never price off raw rows.

  A decision is a register line that is not an auto-match:
    decision : Expense, Bill Payment (Check), Credit Card Credit, Check
    match    : Payment (applied to A/R), Transfer, Credit Card Payment
    neither  : Journal Entry (not a bank-feed line at all)
    Deposit  : match when it splits to undeposited funds; mirrored transfer when
               it splits to another bank/card account; otherwise a decision.

  Bill payments COUNT as decisions -- they routinely land a cent off the bill
  and take real time to match.

ACCOUNT DETECTION
  Top-level accounts are classified by account number: 1000-1199 bank,
  2000-2199 credit card. Named sub-accounts carry no number, so they inherit
  from their parent -- which is how employee cards on a shared card account get
  picked up. Parent/child comes from the GL's own section headers.

  Sub-accounts are GROUPED UNDER THEIR PARENT for reconciliation, because one
  statement is one reconciliation and one surcharge. Split them with --split if
  a client genuinely receives a separate statement per sub-account.

  Detection is a starting point, not gospel: always eyeball the account list it
  prints and correct it with --bank / --card / --exclude if anything is off.
"""

import argparse
import collections
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

DECISION_TYPES = {"Expense", "Bill Payment (Check)", "Credit Card Credit", "Check",
                  "Bill Payment (Credit Card)", "Credit Card Expense"}
MATCH_TYPES = {"Payment", "Transfer", "Credit Card Payment", "Receive Payment"}
NON_FEED_TYPES = {"Journal Entry"}
UNDEPOSITED = re.compile(r"payments? to deposit|undeposited", re.I)

# Conventional QBO chart ranges. Cash sits in 1000-1199, credit cards in
# 2000-2199. Anything outside those is not a register account no matter what
# its name says -- "9605 Credit Card Rewards" is income, not a card.
BANK_PREFIX = re.compile(r"^1[01]\d\d\b")
CARD_PREFIX = re.compile(r"^2[01]\d\d\b")
NOT_AN_ACCOUNT = re.compile(r"payments? to deposit|undeposited|receivable|payable|"
                            r"inventory|tools fund|equity|depreciation", re.I)


def read_rows(path):
    """Yield each GL row as a dict of column-letter -> value."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        shared = ["".join(t.text or "" for t in si.iter(NS + "t"))
                  for si in ET.fromstring(z.read("xl/sharedStrings.xml"))]
    sheets = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet")]
    if not sheets:
        sys.exit("No worksheet found in that file — is it a real .xlsx export?")
    root = ET.fromstring(z.read(sorted(sheets)[0]))
    letters = lambda ref: "".join(c for c in ref if c.isalpha())
    for row in root.iter(NS + "row"):
        d = {}
        for c in row.iter(NS + "c"):
            v = c.find(NS + "v")
            if v is None:
                continue
            val = v.text or ""
            if c.get("t") == "s":
                val = shared[int(val)]
            d[letters(c.get("r"))] = val
        if d:
            yield d


def build_parentage(rows):
    """Map each account to its top-level ancestor, from the GL's section headers.

    A parent's plain 'Total for X' closes only its own direct lines; the group
    stays open until 'Total for X with sub-accounts'. Sub-accounts appear
    between the two, so we must not pop on the plain total when a
    with-sub-accounts total exists for the same name.
    """
    # The report's title block sits above the column-header row; those lines are
    # not account sections and must not open a group.
    started = False
    headers = []
    for r in rows:
        if not started:
            started = r.get("B") == "Distribution account"
            continue
        if r.get("A") and not r.get("C"):
            headers.append(r["A"])
    has_children = {h[len("Total for "):-len(" with sub-accounts")]
                    for h in headers if h.startswith("Total for ")
                    and h.endswith(" with sub-accounts")}
    ancestor, stack = {}, []
    for h in headers:
        if h.startswith("Total for "):
            name = h[len("Total for "):]
            if name.endswith(" with sub-accounts"):
                name = name[:-len(" with sub-accounts")]
                while stack and stack[-1] != name:
                    stack.pop()
                if stack:
                    stack.pop()
            elif name not in has_children:
                if stack and stack[-1] == name:
                    stack.pop()
        else:
            ancestor[h] = stack[0] if stack else h
            stack.append(h)
    return ancestor


def classify_accounts(accounts, ancestor, force_bank, force_card, exclude):
    bank, card = set(), set()
    for a in accounts:
        if a in exclude:
            continue
        if a in force_bank:
            bank.add(a)
            continue
        if a in force_card:
            card.add(a)
            continue
        # An unnumbered sub-account inherits its parent's classification.
        top = ancestor.get(a, a)
        if NOT_AN_ACCOUNT.search(top):
            continue
        if BANK_PREFIX.match(top):
            bank.add(a)
        elif CARD_PREFIX.match(top):
            card.add(a)
    return bank, card


def band(v):
    if v >= 50:
        return "heavy", 20
    if v >= 10:
        return "normal", 10
    return "light", 5


def main():
    p = argparse.ArgumentParser()
    p.add_argument("gl")
    p.add_argument("--months", help="comma-separated MM to include, e.g. 01,02,03")
    p.add_argument("--bank", default="", help="comma-separated account names to force as bank")
    p.add_argument("--card", default="", help="comma-separated account names to force as card")
    p.add_argument("--exclude", default="", help="comma-separated account names to drop")
    p.add_argument("--split", action="store_true",
                   help="reconcile each sub-account separately instead of grouping "
                        "by parent (use only when each carries its own statement)")
    args = p.parse_args()

    split = lambda s: {x.strip() for x in s.split(",") if x.strip()}

    all_rows = list(read_rows(args.gl))
    ancestor = build_parentage(all_rows)
    rows = [r for r in all_rows if r.get("B") and r.get("C") and r.get("D")]
    if not rows:
        sys.exit("Couldn't find GL data rows. Expected columns: B=account, C=date, "
                 "D=type, H=split. Re-export as 'General Ledger' from QBO.")

    bank, card = classify_accounts({r["B"] for r in rows}, ancestor,
                                   split(args.bank), split(args.card), split(args.exclude))
    reg_accounts = bank | card
    if not reg_accounts:
        sys.exit("No bank or credit-card accounts detected. Pass them with --bank / --card.")

    months = split(args.months) if args.months else None
    mon = lambda r: r["C"][:2]
    reg = [r for r in rows if r["B"] in reg_accounts and (not months or mon(r) in months)]
    present = sorted({mon(r) for r in reg})
    # A trailing month with almost no activity is usually a partial export.
    per_mon = {m: sum(1 for r in reg if mon(r) == m) for m in present}
    full = [m for m in present if per_mon[m] >= 0.15 * max(per_mon.values())]
    reg = [r for r in reg if mon(r) in full]
    M = len(full)

    print(f"GL rows: {len(rows)}    register lines: {len(reg)}    "
          f"inflation: {len(rows)/max(len(reg),1):.1f}x")
    print(f"months counted: {', '.join(full)}  (n={M})")
    if len(present) > len(full):
        print(f"  dropped as partial: {', '.join(m for m in present if m not in full)}")
    print()

    # ---- coding decisions -------------------------------------------------
    counts = collections.Counter(r["D"] for r in reg)
    decisions = sum(counts[t] for t in DECISION_TYPES)
    dep = [r for r in reg if r["D"] == "Deposit"]
    dep_match = [r for r in dep if UNDEPOSITED.search(r.get("H", ""))]
    dep_mirror = [r for r in dep if r.get("H") in reg_accounts and r not in dep_match]
    dep_dec = [r for r in dep if r not in dep_match and r not in dep_mirror]
    decisions += len(dep_dec)

    print("=== CODING ===")
    for t in sorted(DECISION_TYPES):
        if counts[t]:
            print(f"  {counts[t]:6d}  {counts[t]/M:7.1f}/mo  {t}")
    if dep:
        print(f"  {len(dep_dec):6d}  {len(dep_dec)/M:7.1f}/mo  Deposit (decision)")
        print(f"       .  matched to undeposited funds: {len(dep_match)} | "
              f"mirrored transfer: {len(dep_mirror)}")
    excluded = sum(counts[t] for t in MATCH_TYPES | NON_FEED_TYPES)
    print(f"  {'-'*46}")
    print(f"  {decisions:6d}  {decisions/M:7.1f}/mo  DECISIONS")
    print(f"  {excluded:6d}  {excluded/M:7.1f}/mo  excluded (auto-match / journal entry)")
    hrs = decisions / M / 50
    print(f"\n  -> {hrs:.2f} staff hrs/mo @ 50 per hour  =  ${hrs*90:,.2f}")

    # ---- bills entered ----------------------------------------------------
    ap = [r for r in rows if "payable" in r["B"].lower() and r["D"] == "Bill"
          and (not months or mon(r) in months)]
    print("\n=== BILL ENTRY ===")
    if not ap:
        print("  No Bill transactions found in A/P — confirm whether we enter bills.")
    else:
        by_m = {m: sum(1 for r in ap if mon(r) == m) for m in sorted({mon(r) for r in ap})}
        print("  by month: " + " · ".join(f"{m}:{n}" for m, n in by_m.items()))
        working = {m: n for m, n in by_m.items() if n >= 0.4 * max(by_m.values())}
        all_avg = sum(by_m.values()) / len(by_m)
        wk_avg = sum(working.values()) / len(working)
        print(f"  average across all months : {all_avg:.1f}/mo")
        if len(working) < len(by_m):
            print(f"  average across working months only : {wk_avg:.1f}/mo   <-- USE THIS")
            print("  ** Entry lapsed mid-period. Bills kept arriving; recording stopped.")
            print("     Cross-check against revenue before accepting: a low month means")
            print("     less bookkeeping, not less business. See Phase 0 Step 6.")
        b = wk_avg * 2 / 60
        print(f"\n  -> {b:.2f} staff hrs/mo @ 2 min each  =  ${b*90:,.2f}")

    # ---- reconciliation ---------------------------------------------------
    print("\n=== RECONCILIATION ===")
    if args.split:
        print("  --split: each sub-account banded on its own.\n")
        group = lambda a: a
    else:
        print("  Sub-accounts grouped under their parent — one statement is one")
        print("  reconciliation and one surcharge. Use --split to separate them.\n")
        group = lambda a: ancestor.get(a, a)
    vols = collections.defaultdict(float)
    for a in reg_accounts:
        vols[group(a)] += sum(1 for r in reg if r["B"] == a) / M
    vols = dict(vols)
    total = 0
    print(f"  {'ACCOUNT':38s} {'lines/mo':>9s}  {'band':<7s} {'min':>4s}")
    for a, v in sorted(vols.items(), key=lambda x: -x[1]):
        b, m = band(v)
        total += m
        print(f"  {a[:38]:38s} {v:9.1f}  {b:<7s} {m:4d}")
    print(f"  {'-'*62}")
    print(f"  {len(vols)} accounts, {total} min = {total/60:.2f} staff hrs "
          f"= ${total/60*90:,.2f}")
    print(f"  surcharge: {len(vols)-1} accounts beyond the first x $10 = ${(len(vols)-1)*10}")
    print("\n  Accounts detected above — correct with --bank / --card / --exclude if wrong.")

    print("\nNOT DERIVED HERE: journal-entry hours, financial-statement review, project or")
    print("class tracking, cleanup. Those are judgment inputs — see Phase 0.")


if __name__ == "__main__":
    main()
