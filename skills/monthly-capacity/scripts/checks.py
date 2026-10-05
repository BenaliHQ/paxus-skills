"""
Pre-flight and roster-drift checks for the month-end capacity build.

Two real failures this exists to catch, neither of which the six-section review
can see:

1. A PERSON-FILTERED timesheet export. `review.coverage()` checks that the
   export's DATES span the month; it cannot see that only some people's rows are
   in the file. `writeback.write_month()` then clears the Assignments tab and
   writes only what it found, and `createSnapshot` freezes that — so a filtered
   export silently reduces the firm's roster to whoever happened to be in the
   CSV. Two exports sitting in a runner's Downloads folder in August 2026 would
   have done exactly that: one carried 1 person where the month had 14, another
   carried 2. A date check passed both.

2. A ROLE HANDOFF that was never flipped on the roster. Role comes from the
   roster, not from the timesheet, so when someone moves from staff to lead and
   nobody updates Assignments, their hours keep booking to the old role
   indefinitely and the new role reads zero. One client ran two months with no
   lead line at all before anyone noticed, and a person sat rostered on another
   for ten months having logged 0.3 hours total.

`preflight()` runs BEFORE the build and can halt it. `drift()` runs after and
only ever warns — a drifting roster is a conversation, not a broken month.

No client or staff names live in this file. Everything is read from the sheet.
"""
import collections
import csv
import datetime

import openpyxl

from build_month import pname, tidy, read_by_header

# Job codes that are never client work. Mirrors the build's own exclusions.
NON_CLIENT = ('paxus', 'vacation', 'paid time off', 'holiday')

# A month whose client hours or client count falls this far below the previous
# snapshot is treated as a truncated or filtered export rather than a quiet
# month. Deliberately loose — this is a tripwire for a broken input, not a
# business-variance alarm.
HOURS_FLOOR = 0.60
CLIENT_FLOOR = 0.70
SOFT_FLOOR = 0.85

# Hours in the previous month above which a person counts as a timekeeper, and
# so their total absence from an export is a stop rather than a note.
TIMEKEEPER_HOURS = 5.0


def _pkey(v):
    """A period cell as "YYYY-MM", whether it holds text or a date.

    A snapshot captured through the app before its 2026-09 fix stored a DATE in
    that column, not the period string: Apps Script's setValues() parses
    date-looking text the way typing into the cell does, so "2026-08" became
    2026-08-01. str() of that is "2026-08-01 00:00:00", which equals no period
    string, so every comparison in this file silently found nothing — no prior
    snapshot, no baseline, and therefore none of the checks below. A month that
    goes wrong this way must not take the next month's guard rails down with it.

    Mirrors periodKey_() in the app's Code.gs.
    """
    if isinstance(v, (datetime.datetime, datetime.date)):
        return f'{v.year:04d}-{v.month:02d}'
    return str(v or '')


def _is_client(code):
    c = str(code or '').strip().lower()
    return bool(c) and not any(c.startswith(x) for x in NON_CLIENT)


def read_timesheet_shape(path):
    """Who and what is actually in this export, with no resolution or aliasing.

    Deliberately dumb: it must work on a file the build would choke on, because
    the whole point is to inspect the input before trusting it.
    """
    people, clients = set(), set()
    hours = 0.0
    with open(path, newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            nm = pname((row.get('fname') or '') + ' ' + (row.get('lname') or ''))
            if nm:
                people.add(nm)
            code = ''
            for k in ('jobcode_3', 'jobcode_2', 'jobcode_1', 'jobcode'):
                v = (row.get(k) or '').strip()
                if v:
                    code = v
                    break
            top = (row.get('jobcode_1') or row.get('jobcode') or '').strip()
            if _is_client(top):
                if code:
                    clients.add(code)
                try:
                    hours += float(row.get('hours') or 0)
                except ValueError:
                    pass
    return {'people': people, 'clients': clients, 'hours': round(hours, 2)}


def _prior_person_hours(wb, period):
    """What each person logged in the previous snapshot.

    This is what makes the people-coverage check self-calibrating. Someone who
    logged nothing last month and nothing this month is simply not a timekeeper
    — an owner, or a role that does not book client time. Someone who logged
    real hours last month and has NO rows this month is the filtered-export
    signature. Treating those two the same would make the check cry wolf every
    month, and a check that cries wolf gets ignored.

    Uses the per-person `staff_hours` column where a snapshot has it, and falls
    back to name-appears-on-a-row-with-hours for older snapshots.
    """
    prev = _prior_period(wb, period)
    if not prev:
        return {}
    out = collections.defaultdict(float)
    for r in read_by_header(wb['SnapshotRows']):
        if _pkey(r.get('period')) != prev:
            continue
        try:
            act = float(r.get('actual') or 0)
        except (TypeError, ValueError):
            act = 0.0
        detail = str(r.get('staff_hours') or '').strip()
        if detail:
            for part in detail.split(','):
                if ':' not in part:
                    continue
                nm, _, hv = part.rpartition(':')
                try:
                    out[pname(nm)] += float(hv)
                except ValueError:
                    pass
        elif act > 0:
            names = [pname(x) for x in str(r.get('staff') or '').split(',')]
            names = [n for n in names if n and n not in ('Unassigned', 'Unknown')]
            for n in names:
                out[n] += act / len(names)     # even split; only used as a >0 test
    return dict(out)


def _prior_period(wb, period):
    try:
        idx = read_by_header(wb['SnapshotIndex'])
    except KeyError:
        return None
    periods = sorted({_pkey(r.get('period')) for r in idx} - {''})
    earlier = [p for p in periods if p < period]
    return earlier[-1] if earlier else None


def _prior_snapshot(wb, period):
    """Client hours and client count from the newest snapshot before `period`."""
    prev = _prior_period(wb, period)
    if not prev:
        return None
    try:
        rows = read_by_header(wb['SnapshotRows'])
    except KeyError:
        return None
    hours, clients = 0.0, set()
    for r in rows:
        if _pkey(r.get('period')) != prev:
            continue
        try:
            a = float(r.get('actual') or 0)
        except (TypeError, ValueError):
            a = 0.0
        hours += a
        nm = tidy(r.get('client'))
        if nm and a > 0:
            clients.add(nm)
    return {'period': prev, 'hours': round(hours, 2), 'clients': len(clients)}


def preflight(period, timesheet_path, app_path):
    """Inspect the input before the build trusts it.

    Returns {'halt': [...], 'warn': [...], 'shape': {...}, 'prior': {...}}.
    Anything in 'halt' means stop and get a better export — do NOT build, and
    above all do not write back, because write-back is destructive to the
    roster.
    """
    shape = read_timesheet_shape(timesheet_path)
    wb = openpyxl.load_workbook(app_path, data_only=True)

    active = set()
    for r in read_by_header(wb['Staff']):
        nm = pname(r.get('name'))
        if nm and str(r.get('status') or 'Active').strip().lower() == 'active':
            active.add(nm)

    halt, warn = [], []

    # --- 1. people coverage: the check that dates cannot make -----------------
    # Graded against what each person logged LAST month, so a non-timekeeper is
    # a note and a vanished timekeeper is a stop.
    was = _prior_person_hours(wb, period)
    missing = sorted(active - shape['people'])
    vanished = [m for m in missing if was.get(m, 0.0) >= TIMEKEEPER_HOURS]
    dormant = [m for m in missing if m not in vanished]
    if vanished:
        lost = sum(was.get(m, 0.0) for m in vanished)
        halt.append(
            f"{len(vanished)} of {len(active)} active staff have NO rows in this "
            f"export but logged real hours last month "
            f"({', '.join(f'{m} {was.get(m, 0):g}h' for m in vanished[:6])}"
            f"{' …' if len(vanished) > 6 else ''}) — {lost:g} hours between them. "
            f"That is the signature of an export filtered to a subset of people. "
            f"Write-back clears the Assignments tab and rebuilds it from this file "
            f"alone, so building on this would drop every one of them off the "
            f"roster and the snapshot would freeze it."
        )
    if dormant:
        warn.append(
            f"{len(dormant)} active staff have no rows this month and logged "
            f"little or nothing last month either "
            f"({', '.join(dormant[:6])}{' …' if len(dormant) > 6 else ''}). "
            f"Normal for anyone who does not book client time; worth confirming "
            f"if you expected hours from them."
        )
    extra = sorted(shape['people'] - active) if active else []
    if extra:
        warn.append(
            f"{len(extra)} people in the export are not Active on the Staff tab "
            f"({', '.join(extra[:6])}{' …' if len(extra) > 6 else ''}). A leaver "
            f"with final-month hours is normal; a new hire needs adding."
        )

    # --- 2. volume sanity against the previous month --------------------------
    prior = _prior_snapshot(wb, period)
    if prior and prior['hours'] > 0:
        hr = shape['hours'] / prior['hours']
        cr = (len(shape['clients']) / prior['clients']) if prior['clients'] else 1.0
        if hr < HOURS_FLOOR:
            halt.append(
                f"Client hours in this export are {shape['hours']:g}, "
                f"{hr:.0%} of {prior['period']}'s {prior['hours']:g}. That is a "
                f"bigger fall than a real month produces — check the export was "
                f"not scoped to a group, a client, or part of the month."
            )
        elif hr < SOFT_FLOOR:
            warn.append(
                f"Client hours are {hr:.0%} of {prior['period']} "
                f"({shape['hours']:g} vs {prior['hours']:g}). Plausible, but "
                f"worth a glance before writing."
            )
        if cr < CLIENT_FLOOR:
            halt.append(
                f"Only {len(shape['clients'])} job codes carry client hours, "
                f"{cr:.0%} of the {prior['clients']} clients with hours in "
                f"{prior['period']}. An export scoped to one group looks exactly "
                f"like this."
            )

    # --- 3. double-rostered people: hours collapse into one role --------------
    pairs = collections.defaultdict(set)
    for r in read_by_header(wb['Assignments']):
        c, s, rl = pname(r.get('client_name')), pname(r.get('staff_name')), tidy(r.get('role'))
        if c and s and rl:
            pairs[(c, s)].add(rl)
    doubled = sorted(k for k, v in pairs.items() if len(v) > 1)
    if doubled:
        warn.append(
            f"{len(doubled)} person/client pairs are rostered in more than one "
            f"role: " + '; '.join(f'{s} on {c} ({"/".join(sorted(pairs[(c, s)]))})'
                                  for c, s in doubled[:5]) +
            (' …' if len(doubled) > 5 else '') +
            ". All of that person's hours will book to their highest role and the "
            "other role will read zero for the month — which reads as 'no work "
            "done' when the work simply went to the other line. Split the roles "
            "between two people, or accept that the split is not measurable."
        )

    return {'halt': halt, 'warn': warn, 'shape': shape, 'prior': prior,
            'active': len(active), 'doubled': doubled}


def drift(period, assignments, app_path, quiet_months=3):
    """Roster rot: rostered people doing nothing, and roles that went silent.

    Warnings only. `assignments` is the list this month's build produced.
    """
    wb = openpyxl.load_workbook(app_path, data_only=True)
    warn = []

    # hours this month, per (client, role) and per (client, person)
    now_role, now_person = collections.defaultdict(float), collections.defaultdict(float)
    for a in assignments:
        c = tidy(a.get('client') or a.get('client_name'))
        rl = tidy(a.get('role'))
        s = pname(a.get('staff') or a.get('staff_name'))
        h = float(a.get('hours') or 0)
        if c and rl:
            now_role[(c, rl)] += h
        if c and s:
            now_person[(c, s)] += h

    # --- a role that carried hours last month and none this month ------------
    prior = _prior_snapshot(wb, period)
    if prior:
        rows = read_by_header(wb['SnapshotRows'])
        went_quiet = []
        for r in rows:
            if _pkey(r.get('period')) != prior['period']:
                continue
            c, rl = tidy(r.get('client')), tidy(r.get('role'))
            try:
                was = float(r.get('actual') or 0)
            except (TypeError, ValueError):
                was = 0.0
            if was > 1.0 and c and rl and now_role.get((c, rl), 0.0) == 0.0:
                went_quiet.append((c, rl, was))
        if went_quiet:
            went_quiet.sort(key=lambda x: -x[2])
            warn.append(
                f"{len(went_quiet)} client/role lines carried hours in "
                f"{prior['period']} and none this month: " +
                '; '.join(f'{c} {rl} (was {h:g})' for c, rl, h in went_quiet[:6]) +
                (' …' if len(went_quiet) > 6 else '') +
                ". Sometimes real. But it is also what an unflipped handoff looks "
                "like: the person moved role, nobody updated Assignments, and "
                "their hours are still booking to the role they left."
            )

    # --- someone rostered on a client but logging nothing, month after month --
    try:
        rows = read_by_header(wb['SnapshotRows'])
        idx = read_by_header(wb['SnapshotIndex'])
    except KeyError:
        return {'warn': warn}
    periods = sorted({_pkey(r.get('period')) for r in idx} - {''})
    recent = [p for p in periods if p < period][-(quiet_months - 1):]
    stale = []
    for (c, s), h in sorted(now_person.items()):
        if h > 0:
            continue
        quiet = True
        for r in rows:
            if _pkey(r.get('period')) not in recent:
                continue
            if tidy(r.get('client')) != c:
                continue
            if s not in str(r.get('staff') or ''):
                continue
            try:
                if float(r.get('actual') or 0) > 0:
                    quiet = False
            except (TypeError, ValueError):
                pass
        if quiet:
            stale.append((c, s))
    if stale:
        warn.append(
            f"{len(stale)} rostered people logged nothing on their client this "
            f"month and nothing in the {quiet_months - 1} months before: " +
            '; '.join(f'{s} on {c}' for c, s in stale[:6]) +
            (' …' if len(stale) > 6 else '') +
            ". Candidates for coming off the roster — a name that never carries "
            "hours makes the team list wrong and hides who actually owns the work."
        )

    return {'warn': warn, 'quiet_role_lines': len(warn)}


def render(pre, dr=None):
    """Plain markdown for the operator. Halts first, in bold, because they stop
    the run."""
    out = ['## 0. Input checks', '']
    s, p = pre['shape'], pre['prior']
    out.append(f"Export carries **{len(s['people'])} people**, "
               f"**{len(s['clients'])} client job codes**, "
               f"**{s['hours']:g} client hours**. "
               f"Staff tab lists {pre['active']} active.")
    if p:
        out.append(f"Previous snapshot {p['period']}: {p['hours']:g} hours across "
                   f"{p['clients']} clients.")
    out.append('')
    if pre['halt']:
        out.append('### STOP — do not build or write back')
        out.append('')
        for h in pre['halt']:
            out.append(f'- **{h}**')
        out.append('')
    warns = list(pre['warn']) + list((dr or {}).get('warn', []))
    if warns:
        out.append('### Worth a look')
        out.append('')
        for w in warns:
            out.append(f'- {w}')
        out.append('')
    if not pre['halt'] and not warns:
        out.append('Nothing to flag — the export looks complete and the roster '
                   'looks current.')
        out.append('')
    return '\n'.join(out)
