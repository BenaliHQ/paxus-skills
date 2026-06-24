"""
Build the Paxus Month-End Close Dashboard data file.

Pulls live FC data, classifies projects by client/stage, and writes a fresh
close-data.js. Existing MoM history is preserved and appended to.

Usage:
    python build_dashboard.py                  # previous month + nearest checkpoint
    python build_dashboard.py --period 2026-05 # explicit close period
    python build_dashboard.py --checkpoint 20  # explicit checkpoint (5/10/15/20/25)
    python build_dashboard.py --cache          # reuse cached project pull
    python build_dashboard.py --record         # also append a row to MoM history
    python build_dashboard.py --dry-run        # preview without writing
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Global flag: when emitting close-data.js to stdout, all logs go to stderr.
_LOG_TO_STDERR = False
def log(*a, **kw):
    print(*a, file=(sys.stderr if _LOG_TO_STDERR else sys.stdout), **kw)

# === Configuration ===
SCRIPT_DIR = Path(__file__).parent
TOKEN_PATH = Path.home() / ".paxus" / "fc_token.txt"
CACHE_PATH = SCRIPT_DIR / ".cache_projects.json"
DATA_PATH = SCRIPT_DIR / "project" / "close-data.js"
BASE_URL = "https://app.financial-cents.com/api/v1"
USER_AGENT = "paxus-close-dashboard/0.1"

# === Scope rules ===
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
CHECKPOINT_DAYS = [5, 10, 15, 20, 25]
CHECKPOINT_KEYS = {5: "5th", 10: "10th", 15: "15th", 20: "20th", 25: "25th"}
MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHS_LONG = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# === Helpers ===
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
    n = normalize_title(title)
    if n.startswith("Quarterly Client"):
        return "Quarterly"
    return "Monthly"  # monthly + annual


def project_tag_string(p: dict) -> str:
    names = [t["name"] for t in (p.get("tags") or []) if isinstance(t, dict)]
    return "; ".join(names)


def previous_month(today: date) -> str:
    first = today.replace(day=1)
    last_prev = first - timedelta(days=1)
    return f"{last_prev.year:04d}-{last_prev.month:02d}"


def period_label_long(period: str) -> str:
    """'2026-05' -> 'May 2026'."""
    yr, mo = period.split("-")
    return f"{MONTHS_LONG[int(mo) - 1]} {yr}"


def period_label_short(period: str) -> str:
    """'2026-05' -> 'May 2026' (same as long but used in MoM rows)."""
    yr, mo = period.split("-")
    return f"{MONTHS_SHORT[int(mo) - 1]} {yr}"


def short_date_for(d: date) -> str:
    """date -> 'Jun 24'."""
    return f"{MONTHS_SHORT[d.month - 1]} {d.day}"


def full_date_for(d: date) -> str:
    """date -> 'Jun 24, 2026'."""
    return f"{MONTHS_SHORT[d.month - 1]} {d.day}, {d.year}"


def closest_checkpoint_day(today: date) -> int:
    return min(CHECKPOINT_DAYS, key=lambda c: abs(today.day - c))


def parse_closed_at(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
    except Exception:
        return None


# === Fetch / cache ===
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
            print(f"  ... {pages} pages fetched ({len(out)} projects)")
        if pages > 500:
            sys.exit("aborting: more than 500 pages — pagination loop?")
    return out


def load_projects(use_cache: bool, token: str) -> list[dict]:
    if use_cache and CACHE_PATH.exists():
        print(f"=== Loading from cache ({CACHE_PATH.name}) ===")
        return json.loads(CACHE_PATH.read_text())
    print("=== Fetching all FC projects (this takes ~2.5 min) ===")
    projects = fetch_all_projects(token)
    try:
        CACHE_PATH.write_text(json.dumps(projects))
        print(f"  cached to {CACHE_PATH}")
    except Exception as e:
        print(f"  (could not write cache: {e})")
    return projects


# === Parse / write close-data.js ===
def read_close_data() -> dict:
    if not DATA_PATH.exists():
        sys.exit(f"close-data.js not found at {DATA_PATH}")
    text = DATA_PATH.read_text(encoding="utf-8")
    m = re.search(r"window\.PAXUS_CLOSE\s*=\s*(\{.*\})\s*;\s*$", text, re.DOTALL)
    if not m:
        sys.exit("could not parse close-data.js (expected `window.PAXUS_CLOSE = {...};`)")
    return json.loads(m.group(1))


def write_close_data(data: dict, dry_run: bool, stdout: bool = False) -> None:
    js = "window.PAXUS_CLOSE = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    if dry_run:
        print("=== DRY RUN — would write close-data.js with: ===")
        cps = data.get("checkpoints", [])
        for cp in cps:
            print(f"  {cp.get('key'):>5s}  {cp.get('date'):>8s}   staff={cp.get('staff'):>3}  lead={cp.get('lead'):>3}  controller={cp.get('controller'):>3}  closed={cp.get('closed'):>3}  ({cp.get('status')})")
        return
    if stdout:
        sys.stdout.write(js)
        sys.stdout.flush()
        return
    DATA_PATH.write_text(js, encoding="utf-8")
    print(f"  wrote {DATA_PATH}")


# === Build today's snapshot ===
def build_period_snapshot(projects: list[dict], period: str) -> tuple[dict[str, list[dict]], list[dict]]:
    """Return (clients_by_stage, period_projects).

    clients_by_stage maps stage -> list of client rows for the detail tables.
    Each row is a dict with: client_id, name, frequency, stage, tag_status,
    closed_date (if stage == closed), project_titles.
    """
    in_scope = [p for p in projects if title_in_scope(p.get("title", ""))]
    period_projects = [
        p for p in in_scope
        if (p.get("accounting_period_date") or "").startswith(period)
    ]

    by_client: dict[int, list[dict]] = defaultdict(list)
    for p in period_projects:
        by_client[p["client"]["id"]].append(p)

    client_rows: list[dict] = []
    for client_id, projs in by_client.items():
        stages = [classify_stage(p) for p in projs]
        earliest = min(stages, key=lambda s: STAGE_RANK[s])
        freq = "Quarterly" if any(frequency_from_title(p["title"]) == "Quarterly" for p in projs) else "Monthly"
        # Tag status: tags from the project(s) at the earliest stage
        relevant_projs = [p for p in projs if classify_stage(p) == earliest]
        tag_set: list[str] = []
        for p in relevant_projs:
            for t in (p.get("tags") or []):
                if isinstance(t, dict) and t["name"] not in tag_set:
                    tag_set.append(t["name"])
        # Closed date: most recent closed_at among closed projects
        closed_dates = [parse_closed_at(p.get("closed_at")) for p in projs if p.get("closed_at")]
        closed_dates = [d for d in closed_dates if d is not None]
        latest_closed = max(closed_dates) if closed_dates else None
        client_rows.append({
            "client_id": client_id,
            "name": projs[0]["client"]["name"],
            "frequency": freq,
            "stage": earliest,
            "tag_status": "; ".join(tag_set),
            "closed_date": short_date_for(latest_closed) if latest_closed else "",
            "project_titles": [normalize_title(p["title"]) for p in projs],
        })

    by_stage: dict[str, list[dict]] = defaultdict(list)
    for r in client_rows:
        by_stage[r["stage"]].append(r)
    return by_stage, period_projects


# === Update data structure ===
def update_dashboard_data(
    existing: dict,
    by_stage: dict[str, list[dict]],
    period: str,
    today: date,
    checkpoint_day: int,
    record_to_mom: bool,
) -> dict:
    data = dict(existing)  # shallow copy; we'll overwrite arrays we own
    close_month_label = period_label_long(period)
    cp_key = CHECKPOINT_KEYS[checkpoint_day]

    # Counts for today
    counts = {s: len(by_stage.get(s, [])) for s in STAGES}
    total_clients = sum(counts.values())

    # === Header ===
    data["closeMonth"] = close_month_label
    data["reportDate"] = full_date_for(today)

    cp_label_map = {
        5: "5TH CHECKPOINT · STAFF RECONCILIATIONS",
        10: "10TH CHECKPOINT · STAFF WORK COMPLETE",
        15: "15TH CHECKPOINT · LEAD WORK COMPLETE",
        20: "20TH CHECKPOINT · CONTROLLER / FINAL REVIEW",
        25: "25TH CHECKPOINT · ALL CLOSED (FINAL)",
    }
    data["checkpointLabel"] = cp_label_map.get(checkpoint_day, f"{cp_key.upper()} CHECKPOINT")

    # Report note: blank by default; preserved if already set for same date
    data["reportNote"] = data.get("reportNote", "") if data.get("reportDate") == full_date_for(today) else ""

    # === Checkpoints (4-5 current-period snapshots) ===
    # If period changed, reset checkpoints
    existing_close_month = existing.get("closeMonth", "")
    period_changed = existing_close_month != close_month_label
    checkpoints = list(data.get("checkpoints", []))
    if period_changed:
        checkpoints = []

    # Build/refresh entries for all 5 checkpoint dates
    checkpoint_by_key = {cp.get("key"): cp for cp in checkpoints}
    new_checkpoints = []
    # Estimate checkpoint actual dates: use the day-of-month within the calendar
    # month that follows the close period. (e.g., May close → checkpoints in June.)
    yr, mo = (int(x) for x in period.split("-"))
    cp_year = yr if mo < 12 else yr + 1
    cp_month = mo + 1 if mo < 12 else 1
    for d in CHECKPOINT_DAYS:
        key = CHECKPOINT_KEYS[d]
        cp_date = date(cp_year, cp_month, d)
        existing_cp = checkpoint_by_key.get(key, {})
        if d == checkpoint_day:
            # This is the one we're updating now
            new_checkpoints.append({
                "key": key,
                "date": short_date_for(cp_date),
                "staff": counts["staff"],
                "lead": counts["lead"],
                "controller": counts["controller"],
                "closed": counts["closed"],
                "status": "current" if cp_date == today else ("past" if cp_date < today else "future"),
            })
        elif existing_cp:
            # Preserve, but recompute status against today
            status = "past" if cp_date < today else ("current" if cp_date == today else "future")
            new_checkpoints.append({**existing_cp, "status": status})
        else:
            new_checkpoints.append({
                "key": key,
                "date": short_date_for(cp_date),
                "staff": 0, "lead": 0, "controller": 0, "closed": 0,
                "status": "past" if cp_date < today else ("current" if cp_date == today else "future"),
            })
    data["checkpoints"] = new_checkpoints

    # === MoM history append ===
    if record_to_mom:
        mom = data.setdefault("mom", {})
        rows = mom.setdefault(cp_key, [])
        # Check for existing row for this period — replace it (idempotent)
        row_date_label = full_date_for(today)
        period_short = period_label_short(period)
        new_row = [
            row_date_label,
            period_short,
            counts["staff"], counts["lead"], counts["controller"], counts["closed"],
            total_clients,
        ]
        # Find existing row matching period and replace, else append
        for i, row in enumerate(rows):
            if len(row) >= 2 and row[1] == period_short:
                rows[i] = new_row
                break
        else:
            rows.append(new_row)

    # === Detail tables ===
    def sort_key(r):
        return r["name"].lower()

    def to_row_basic(r):
        # [name, freq, assignee_blank, tag_status]
        return [r["name"], r["frequency"], "", r["tag_status"]]

    def to_row_closed(r):
        # [name, freq, closed_date, assignees_blank]
        return [r["name"], r["frequency"], r["closed_date"], ""]

    data["staff"] = [to_row_basic(r) for r in sorted(by_stage.get("staff", []), key=sort_key)]
    data["lead"] = [to_row_basic(r) for r in sorted(by_stage.get("lead", []), key=sort_key)]
    data["controller"] = [to_row_basic(r) for r in sorted(by_stage.get("controller", []), key=sort_key)]
    # Closed: sort by closed_date desc, then name
    closed_rows = sorted(
        by_stage.get("closed", []),
        key=lambda r: (r["closed_date"] or "", r["name"].lower()),
        reverse=True,
    )
    data["closed"] = [to_row_closed(r) for r in closed_rows]

    # === Milestones: update status only ===
    # Preserve existing milestones (Jennifer's own labels), update status by date.
    # Dates in milestones look like "Jun 5" or "Jun 8–9"; not parsing complex ranges yet.
    milestones = data.get("milestones") or []
    today_short = short_date_for(today)
    for m in milestones:
        d_label = (m.get("date") or "").strip()
        # Try first token before space/dash
        first = re.split(r"[\s–\-]", d_label)
        try:
            mo_name = first[0]
            day_num = int(first[1])
            mo_idx = MONTHS_SHORT.index(mo_name) + 1
            md = date(today.year, mo_idx, day_num)
            if md < today: m["status"] = "past"
            elif md == today: m["status"] = "today"
            else: m["status"] = "future"
        except (ValueError, IndexError):
            pass  # leave status as-is
    data["milestones"] = milestones

    return data


# === Main ===
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--period", help="close period YYYY-MM (default: previous month)")
    parser.add_argument("--checkpoint", type=int, choices=CHECKPOINT_DAYS,
                        help="checkpoint day (5/10/15/20/25). Default: nearest to today.")
    parser.add_argument("--cache", action="store_true", help="reuse cached project pull")
    parser.add_argument("--record", action="store_true",
                        help="append today's snapshot to MoM history")
    parser.add_argument("--dry-run", action="store_true", help="don't write the file")
    parser.add_argument("--stdout", action="store_true", help="emit close-data.js to stdout only (no file write)")
    args = parser.parse_args()

    # If emitting to stdout, redirect all status logs to stderr so stdout stays clean.
    if args.stdout:
        sys.stdout = sys.stderr

    if not TOKEN_PATH.exists():
        sys.exit(f"token file missing: {TOKEN_PATH}")
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()

    today = date.today()
    period = args.period or previous_month(today)
    if not re.fullmatch(r"\d{4}-\d{2}", period):
        sys.exit(f"--period must be YYYY-MM, got: {period}")
    checkpoint = args.checkpoint or closest_checkpoint_day(today)

    print(f"  period:        {period} ({period_label_long(period)})")
    print(f"  today:         {today.isoformat()} ({short_date_for(today)})")
    print(f"  checkpoint:    {CHECKPOINT_KEYS[checkpoint]} (day {checkpoint})")
    print(f"  record to MoM: {args.record}")
    print(f"  dry run:       {args.dry_run}")
    print()

    projects = load_projects(args.cache, token)
    print(f"  total projects: {len(projects)}")

    by_stage, period_projects = build_period_snapshot(projects, period)
    counts = {s: len(by_stage.get(s, [])) for s in STAGES}
    print(f"  in-scope projects this period: {len(period_projects)}")
    print(f"  clients this period:           {sum(counts.values())}")
    print(f"    staff={counts['staff']}  lead={counts['lead']}  controller={counts['controller']}  closed={counts['closed']}")
    print()

    existing = read_close_data()
    updated = update_dashboard_data(
        existing, by_stage, period, today, checkpoint, args.record
    )
    if args.stdout:
        # Emit only the JS to stdout; status logs already went via prints above
        # — but we redirected stdout earlier if needed. Restore for final dump.
        sys.stdout = sys.__stdout__
        write_close_data(updated, dry_run=False, stdout=True)
        return 0
    write_close_data(updated, args.dry_run)
    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
