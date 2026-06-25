"""
Stage 1 probe: classify Paxus month-end close work from live Financial Cents data.

Run:
    python ~/paxus-ai/internal/month-end-close-dashboard/probe_close.py

Optional args:
    --period 2026-05     pick a specific close period (default: previous calendar month)
    --detail             print the client list per stage
    --cache              reuse the last fetched project dump (skip the 2+ min API pull)

Output: a table of per-CLIENT counts per stage x frequency, plus a sanity summary.
This is a read-only probe. It does not write close-data.js (Stage 2).

Rollup rule: a client's stage = the EARLIEST stage among their in-scope projects
(close + review) for the period. A monthly client with both projects, where Close
is "Closed" but Review is still in "Initial Review", counts as Lead — not Closed.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import urllib.error
import urllib.request

# Windows default codepage can't print Unicode arrows etc.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

TOKEN_PATH = Path.home() / ".paxus" / "fc_token.txt"
CACHE_PATH = Path(__file__).parent / ".cache_projects.json"
BASE_URL = "https://app.financial-cents.com/api/v1"
USER_AGENT = "paxus-close-dashboard/0.1"

TITLE_PATTERNS = (
    "Monthly Client - Month End Close",
    "Monthly Client - Review",
    "Quarterly Client - Month End Close",
    "Quarterly Client - Review",
    "Annual Client - Month End Close",
    "Annual Client - Review",
)

CONTROLLER_TAGS = {"In Final Review", "Waiting on Controller"}
LEAD_TAGS = {"Initial Review", "Waiting on Lead"}

STAGES = ["staff", "lead", "controller", "closed"]
STAGE_RANK = {s: i for i, s in enumerate(STAGES)}


def normalize_title(t: str) -> str:
    return re.sub(r"^\*+", "", t).strip()


def title_in_scope(t: str) -> bool:
    return normalize_title(t) in TITLE_PATTERNS


def classify_stage(p: dict) -> str:
    if p.get("is_closed"):
        return "closed"
    tag_names = {t["name"] for t in (p.get("tags") or []) if isinstance(t, dict)}
    if tag_names & CONTROLLER_TAGS:
        return "controller"
    if tag_names & LEAD_TAGS:
        return "lead"
    return "staff"


def frequency_from_title(title: str) -> str:
    """Derive client frequency from the project title.

    Quarterly Client - ...   → quarterly
    Annual Client - ...      → monthly  (annual clients still close monthly)
    Monthly Client - ...     → monthly
    """
    n = normalize_title(title)
    if n.startswith("Quarterly Client"):
        return "quarterly"
    return "monthly"


def previous_month(today: date) -> str:
    first_of_this = today.replace(day=1)
    last_of_prev = first_of_this - timedelta(days=1)
    return f"{last_of_prev.year:04d}-{last_of_prev.month:02d}"


def fetch_all_projects(token: str) -> list[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    url = f"{BASE_URL}/projects?per_page=100"
    out: list[dict] = []
    pages = 0
    while url:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            sys.exit(f"FC API error on page {pages + 1}: HTTP {e.code} {e.reason}")
        out.extend(d.get("data", []))
        url = (d.get("links") or {}).get("next")
        pages += 1
        if pages % 25 == 0:
            print(f"  ... {pages} pages fetched ({len(out)} projects so far)")
        if pages > 500:
            sys.exit("aborting: more than 500 pages — pagination may be looping")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--period", help="close period in YYYY-MM form (default: previous month)")
    parser.add_argument("--detail", action="store_true", help="print client list per stage")
    parser.add_argument("--cache", action="store_true", help="reuse the last fetched project dump")
    args = parser.parse_args()

    if not TOKEN_PATH.exists():
        sys.exit(f"token file missing: {TOKEN_PATH}")
    token = TOKEN_PATH.read_text().strip()
    if not token:
        sys.exit(f"token file is empty: {TOKEN_PATH}")

    period = args.period or previous_month(date.today())
    if not re.fullmatch(r"\d{4}-\d{2}", period):
        sys.exit(f"--period must be YYYY-MM, got: {period}")

    if args.cache and CACHE_PATH.exists():
        print(f"=== Loading projects from cache ({CACHE_PATH}) ===")
        projects = json.loads(CACHE_PATH.read_text())
    else:
        print(f"=== Fetching all FC projects ===")
        projects = fetch_all_projects(token)
        CACHE_PATH.write_text(json.dumps(projects))
        print(f"  cached to {CACHE_PATH}")
    print(f"  total projects: {len(projects)}")

    in_scope = [p for p in projects if title_in_scope(p.get("title", ""))]
    print(f"  in scope by title: {len(in_scope)}")

    period_projects = [
        p for p in in_scope
        if (p.get("accounting_period_date") or "").startswith(period)
    ]
    print(f"  in scope AND in period {period}: {len(period_projects)}")
    print()

    if not period_projects:
        print(f"!! No projects found for period {period}. Available periods (top 10):")
        per_ctr = Counter((p.get("accounting_period_date") or "")[:7] for p in in_scope)
        for per, c in per_ctr.most_common(10):
            print(f"     {per}: {c}")
        return 1

    # === ROLL UP: group by client, take earliest stage across their projects ===
    by_client: dict[int, list[dict]] = defaultdict(list)
    for p in period_projects:
        by_client[p["client"]["id"]].append(p)

    client_rows: list[dict] = []
    for client_id, projs in by_client.items():
        # Earliest stage = min rank
        stages_present = [classify_stage(p) for p in projs]
        earliest = min(stages_present, key=lambda s: STAGE_RANK[s])
        # Frequency: if any quarterly title is present, mark quarterly; else monthly
        freqs = {frequency_from_title(p["title"]) for p in projs}
        freq = "quarterly" if "quarterly" in freqs else "monthly"
        client_rows.append({
            "client_id": client_id,
            "client_name": projs[0]["client"]["name"],
            "stage": earliest,
            "frequency": freq,
            "project_count": len(projs),
            "project_stages": stages_present,
            "titles": [normalize_title(p["title"]) for p in projs],
        })

    # === REPORT ===
    grid: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in client_rows:
        grid[(row["frequency"], row["stage"])].append(row)

    freqs = ["monthly", "quarterly"]

    print(f"=== {period} close — CLIENT counts (rollup: earliest stage wins) ===")
    header = f"  {'':12s} " + "  ".join(f"{s:>10s}" for s in STAGES) + f"  {'total':>10s}"
    print(header)
    totals = {s: 0 for s in STAGES}
    for f in freqs:
        row_counts = [len(grid[(f, s)]) for s in STAGES]
        row_total = sum(row_counts)
        for s, c in zip(STAGES, row_counts):
            totals[s] += c
        print(f"  {f:12s} " + "  ".join(f"{c:>10d}" for c in row_counts) + f"  {row_total:>10d}")
    grand = sum(totals.values())
    print(f"  {'TOTAL':12s} " + "  ".join(f"{totals[s]:>10d}" for s in STAGES) + f"  {grand:>10d}")
    print()

    pct_closed = (totals["closed"] / grand * 100) if grand else 0
    print(f"=== Health check ===")
    print(f"  {totals['closed']} of {grand} clients fully closed ({pct_closed:.1f}%)")
    print(f"  Underlying project count: {len(period_projects)}")
    print()
    print(f"  Compare to your FC manual filters today:")
    print(f"    'companywide-staff month-in-close'  →  staff clients: {totals['staff']}")
    print(f"    'companywide-lead'                  →  lead clients:  {totals['lead']}")
    print(f"    'companywide-controller'            →  controller:    {totals['controller']}")
    print(f"    Closed clients (monthly + quarterly): {totals['closed']}")
    print()

    if args.detail:
        print(f"=== Client detail (period {period}) ===")
        for f in freqs:
            for s in STAGES:
                bucket = grid[(f, s)]
                if not bucket:
                    continue
                print(f"\n  -- {f.upper()} / {s.upper()} ({len(bucket)}) --")
                for row in sorted(bucket, key=lambda r: r["client_name"]):
                    titles = " + ".join(row["titles"])
                    proj_stages = "+".join(row["project_stages"])
                    print(f"     {row['client_name']:50s}  [{proj_stages}]  ({titles})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
