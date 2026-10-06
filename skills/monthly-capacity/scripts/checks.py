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
        # a Payroll seat alongside another role is by design: payroll books by
        # service item, so it never collapses into the other role
        if c and s and rl and rl != 'Payroll':
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

    # Rostered people logging nothing are now a per-month question, not a
    # three-month warning: see zero_roster().
    return {'warn': warn, 'quiet_role_lines': len(warn)}


def zero_roster(period, assignments, app_path, staff=None):
    """Everyone still on a client's roster who logged zero hours there this month.

    A zero-hour row exists only because the build keeps the roster visible for
    clients that had activity, so each one is a question for the operator: is
    this person still on the client? Some genuinely had a quiet month. Others
    were never really on it: someone who does no client work, or a one-off month
    of covering that left them rostered for good. A yes goes to write-back as
    `remove`.

    For context, each row carries how many months in a row (this one included)
    that person has logged nothing on that client, and the last month they did.
    Per-person history comes from the snapshot `staff_hours` column; a month
    where that split is missing falls back to the row's staff list and total.

    Pass the build's `staff` rows to skip people who logged NO time at all this
    month (an owner who does not keep a timesheet, say). Zero hours on a client
    says nothing about someone who records nothing anywhere, and their seat is
    usually deliberate, kept so the role is not shown as empty. They are left
    out of the question and counted instead.
    """
    wb = openpyxl.load_workbook(app_path, data_only=True)
    zero = []
    total_now = collections.defaultdict(float)
    for a in assignments:
        total_now[pname(a.get('staff'))] += float(a.get('hours') or 0)
    no_timesheet = set()
    if staff is not None:
        logged = collections.defaultdict(float)
        for r in staff:
            logged[pname(r.get('name'))] += float(r.get('logged_hours') or 0)
        no_timesheet = {n for n, h in logged.items() if h <= 0}
    zero_roster.skipped = 0
    for a in assignments:
        if float(a.get('hours') or 0) > 0:
            continue
        if pname(a.get('staff')) in no_timesheet:
            zero_roster.skipped += 1
            continue
        zero.append((tidy(a.get('client')), pname(a.get('staff')), tidy(a.get('role'))))
    if not zero:
        return []

    # per (period, client, person) hours from saved snapshots
    hist = collections.defaultdict(float)
    known = set()
    periods = []
    if 'SnapshotRows' in wb.sheetnames and 'SnapshotIndex' in wb.sheetnames:
        periods = sorted({_pkey(r.get('period')) for r in read_by_header(wb['SnapshotIndex'])}
                         - {''})
        for r in read_by_header(wb['SnapshotRows']):
            pk, c = _pkey(r.get('period')), tidy(r.get('client'))
            raw = str(r.get('staff_hours') or '').strip()
            if raw:
                for part in raw.split(','):
                    if ':' not in part:
                        continue
                    k, v = part.rsplit(':', 1)
                    try:
                        hist[(pk, c, pname(k))] += float(v)
                    except ValueError:
                        pass
                    known.add((pk, c, pname(k)))
            else:
                names = [pname(x) for x in str(r.get('staff') or '').split(',') if pname(x)]
                try:
                    act = float(r.get('actual') or 0)
                except (TypeError, ValueError):
                    act = 0.0
                for n in names:
                    if len(names) == 1:
                        hist[(pk, c, n)] += act
                    known.add((pk, c, n))
    prior = [p for p in periods if p < period]

    out = []
    for c, s, rl in sorted(set(zero)):
        streak, last = 1, ''
        for pk in reversed(prior):
            if (pk, c, s) not in known:
                break           # not on that client then: the streak starts here
            if hist.get((pk, c, s), 0.0) > 0:
                last = pk
                break
            streak += 1
        if not last:
            last = next((pk for pk in reversed(prior) if hist.get((pk, c, s), 0.0) > 0), '')
        out.append({'client': c, 'staff': s, 'role': rl, 'zero_months': streak,
                    'last_hours': last or 'never',
                    'client_hours_anywhere': round(total_now.get(s, 0.0), 2)})
    out.sort(key=lambda d: (-d['zero_months'], d['staff'], d['client']))
    return out


def leaving(period, assignments, app_path):
    """Clients marked "Client leaving" on the app's Transitions tab that are
    still not Inactive. Each one is a question for the operator: has it fully
    left? If so it goes to write-back as `inactivate`, because a departed client
    left Active keeps producing budget nobody will deliver.

    Reads the Transitions tab when it exists; an older sheet without it simply
    has nothing to ask.
    """
    wb = openpyxl.load_workbook(app_path, data_only=True)
    if 'Transitions' not in wb.sheetnames:
        return []
    status = {tidy(r.get('name')): tidy(r.get('status')) or 'Active'
              for r in read_by_header(wb['Clients']) if tidy(r.get('name'))}
    hrs = collections.defaultdict(float)
    for a in assignments:
        hrs[tidy(a['client'])] += float(a['hours'] or 0)
    by = {}
    for r in read_by_header(wb['Transitions']):
        if tidy(r.get('reason')) != 'Client leaving':
            continue
        if tidy(r.get('status')) == 'Cancelled':
            continue
        c = tidy(r.get('client_name'))
        if not c or status.get(c) == 'Inactive':
            continue
        d = by.setdefault(c, {'client': c, 'status': status.get(c, 'Active'),
                              'target': '', 'plans': 0,
                              'hours_this_month': round(hrs.get(c, 0.0), 2)})
        d['plans'] += 1
        t = r.get('target_date')
        t = t.strftime('%Y-%m-%d') if hasattr(t, 'strftime') else tidy(t)
        if t and t > d['target']:
            d['target'] = t
    return sorted(by.values(), key=lambda d: d['client'])


def render(pre, dr=None, lv=None, zr=None):
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
    if zr:
        # Grouped by person, because a roster goes stale person by person: a
        # first pass found 144 zero-hour seats, most belonging to a handful of
        # people. One quiet month is usually just that, so those are a count
        # rather than a question until they repeat.
        # Asked when a seat first reaches two months at zero, then every six.
        # Without that, every seat the operator decided to keep (a quarterly
        # client, a controller who only reviews) would be asked about again
        # every single month, and the question would become noise.
        def due(n):
            return n == 2 or (n >= 6 and n % 6 == 0)
        ask = [d for d in zr if due(d['zero_months'])]
        once = [d for d in zr if d['zero_months'] < 2]
        held = [d for d in zr if d['zero_months'] >= 2 and not due(d['zero_months'])]
        out.append('### On the roster with zero hours — keep or remove?')
        out.append('')
        out.append(f"{len(ask)} seats reached two months at zero this month, or "
                   "another six since they were last asked about. "
                   "Some are genuinely quiet clients; others are people who are not "
                   "really on the client any more. Each **remove** goes to "
                   "write-back as `remove`; anything not answered stays on.")
        out.append('')
        by = collections.OrderedDict()
        for d in sorted(ask, key=lambda d: (d['client_hours_anywhere'] > 0,
                                            d['staff'], -d['zero_months'])):
            by.setdefault(d['staff'], []).append(d)
        for person, rows in by.items():
            none = rows[0]['client_hours_anywhere'] == 0
            out.append(f"- **{person}** — {len(rows)} seat{'s' if len(rows) != 1 else ''}"
                       + (" · *logged no client hours anywhere this month*" if none else ''))
            out.append('  ' + '; '.join(
                f"{d['client']} ({d['role']}, {d['zero_months']} mo"
                + (f", last {d['last_hours']}" if d['last_hours'] != 'never' else ', never')
                + ')' for d in rows))
        out.append('')
        if once:
            out.append(f"{len(once)} more seats are at zero for the first month. Not "
                       "asked about yet; they come back here if it repeats.")
            out.append('')
        if held:
            out.append(f"{len(held)} seats have been at zero longer and were already "
                       "asked about. Not repeated; they come back at the next "
                       "six-month mark.")
            out.append('')
    if lv:
        out.append('### Clients marked leaving — still not Inactive')
        out.append('')
        out.append('Each was marked *Client leaving* on Transitions. Has it fully '
                   'left? A yes goes to write-back as `inactivate`.')
        out.append('')
        out.append('| Client | Status in the app | Target | Hours this month |')
        out.append('|---|---|---|---:|')
        for d in lv:
            out.append(f"| {d['client']} | {d['status']} | {d['target'] or '—'} "
                       f"| {d['hours_this_month']:g} |")
        out.append('')
    return '\n'.join(out)
