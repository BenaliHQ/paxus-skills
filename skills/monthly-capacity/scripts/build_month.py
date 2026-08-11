"""
Build one month of CapacityIQ data from a QB Time itemized report.

Outputs, for a given period:
  assignments : [{client, staff, role, hours}]
  staff       : [{name, role, base_hours, pto_hours, available_hours,
                  total_hours, client_pct, status}]
  report      : everything that needed a judgement call, so nothing is silent.

Rules, all validated against May 2026 (293/304 rows reproduced exactly):
  clients  - deepest QB jobcode wins; resolve "<parent>: <sub>" against the scope
             sheet, falling back to the parent when it has no sub-clients.
  role     - the person's HIGHEST role on that client per the Assignments template
             (Controller > Lead > Staff); if unrostered, their primary role.
  capacity - base = workdays x daily rate; available = (base - PTO) x client %.
             PTO comes from the timesheet's Vacation / Paid Time Off codes.
             Paxus Admin is NOT PTO - it is internal work already priced into
             each person's client %.
"""
import csv, collections, openpyxl, re, json, datetime, calendar
import overrides as OV

RANK = {'Controller': 3, 'Lead': 2, 'Staff': 1}
PTO_CODES = {'vacation', 'paid time off', 'holiday', 'pto', 'sick', 'sick leave',
             'bereavement', 'jury duty'}
INTERNAL_PREFIX = ('paxus',)          # internal work, never client time, never PTO

# Banked overtime being drawn down. This IS time off — it reduces the hours
# available for client work — but it is kept apart from PTO because it is an
# earned balance being spent rather than a benefit, and not everyone has one.
# Checked before INTERNAL_PREFIX, since the code starts with "Paxus".
BANKED_CODES = ('overtime bank', 'overtime banked', 'banked overtime')

# Service items that mean "this client is still being onboarded". The firm codes
# the onboarding phase as Onboarding / Clean-up and switches to Bookkeeping and
# friends once the client is live.
ONBOARDING_ITEMS = ('onboarding', 'clean-up', 'cleanup', 'clean up')
ONB_CONFIDENT = 0.50   # >= this share of their hours -> Onboarding
ONB_REVIEW    = 0.20   # between the two -> flag, don't decide

# QB jobcode spellings that don't match the scope sheet. Keep this list short and
# explicit - anything not listed and not resolvable is reported, never guessed.
# In app mode these are loaded from the workbook's "Aliases" tab, so no client
# name is ever hard-coded here. In bootstrap mode they fall back to overrides.py.
QB_ALIASES = {}
_RENAME = {}
_MERGE = {}
_DROP = set()


def load_aliases(path):
    """Read the Aliases tab: qb_name | app_name | action | note.

    action is one of:
      alias  - matched against the raw QB jobcode (lowercased) by the resolver
      rename - client is known by another name; applied wherever a name appears
      merge  - several QB names are one client; app_name is canonical
      drop   - never a client; filtered out entirely
    """
    wb = openpyxl.load_workbook(path, data_only=True)
    if 'Aliases' not in wb.sheetnames:
        return {}, {}, {}, set()
    alias, rename, merge, drop = {}, {}, {}, set()
    for r in read_by_header(wb['Aliases']):
        src, dst = tidy(r.get('qb_name')), tidy(r.get('app_name'))
        act = (tidy(r.get('action')) or '').lower()
        if not src:
            continue
        if act == 'alias' and dst:
            alias[src.lower()] = dst
        elif act == 'rename' and dst:
            rename[src] = dst
        elif act == 'merge' and dst:
            merge[src] = dst
        elif act == 'drop':
            drop.add(src)
    return alias, rename, merge, drop


def tidy(n):
    n = str(n or '')
    for ch in (' ', ' ', ' '):
        n = n.replace(ch, ' ')
    n = n.replace('​', '').replace('﻿', '')
    return ' '.join(n.split())


ROLE_SUFFIX = re.compile(r'\s+-\s*[A-Za-z]{1,2}\s*$')


def pname(n):
    """Staff name without a trailing role marker (' - S'). Some scope sheets
    used that to denote a second role; the role has its own column."""
    return ROLE_SUFFIX.sub('', tidy(n)).strip()


def norm(s, drop_entity=False):
    s = tidy(s).lower().replace('&', 'and')
    if drop_entity:
        s = re.sub(r'\b(llc|l\.l\.c|inc|incorporated|co|company|ltd|lp|pllc|pc)\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', '', s)


def workdays(year, month):
    """Weekdays in the month. Holidays are NOT deducted - matches the operator's
    own figures (Feb 2026 = 20 weekdays = 160 hrs for a full-timer)."""
    return sum(1 for d in range(1, calendar.monthrange(year, month)[1] + 1)
               if datetime.date(year, month, d).weekday() < 5)


def sheet(wb, *must, forbid=()):
    for ws in wb.worksheets:
        t = re.sub(r'[^a-z0-9]', '', ws.title.lower())
        if all(re.sub(r'[^a-z0-9]', '', m.lower()) in t for m in must) \
           and not any(f in t for f in forbid):
            return ws
    raise KeyError(' '.join(must))


def read_roster(ws):
    hdr = [re.sub(r'[^a-z0-9]', '', str(h or '').lower())
           for h in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
    gs = [i for i, h in enumerate(hdr) if h.startswith('staffname')]
    out = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[0]:
            continue
        c = tidy(row[0])
        for gi in gs:
            sn = pname(row[gi]) if gi < len(row) else ''
            rl = tidy(row[gi + 1]) if gi + 1 < len(row) else ''
            if not sn or rl not in RANK:
                continue
            out.append((c, sn, rl))
    return out


def read_staff(ws):
    out = collections.defaultdict(
        lambda: {'roles': {}, 'total': 0.0, 'pct': None, 'status': 'Active',
                 'email': ''})
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        nm, rl = pname(r[0]), tidy(r[1])
        if rl not in RANK:
            continue
        g = lambda i: (float(r[i]) if i < len(r) and r[i] not in (None, '') else 0.0)
        d = out[nm]
        d['roles'][rl] = g(2)
        d['total'] += g(5)
        if len(r) > 3 and r[3]:
            d['email'] = tidy(r[3]).replace('$', '@')
        if len(r) > 4 and r[4]:
            d['status'] = tidy(r[4])
        if len(r) > 6 and r[6] not in (None, ''):
            try:
                d['pct'] = float(r[6])
            except (TypeError, ValueError):
                pass
    return out


def read_by_header(ws):
    """Rows of a tab as dicts keyed by header name."""
    hdr = [tidy(h) for h in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
    out = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or all(x in (None, '') for x in r):
            continue
        out.append({h: v for h, v in zip(hdr, r) if h})
    return out


def load_app(path):
    """
    Read the roster, staff and client list from the CapacityIQ Data workbook —
    the app IS the source of truth, so a client added in the Sheet is known to
    the next monthly build without touching the scope spreadsheet.

    Returns the same shapes the scope-sheet reader produces.
    """
    wb = openpyxl.load_workbook(path, data_only=True)

    def num(v):
        try:
            return round(float(v), 4)
        except (TypeError, ValueError):
            return 0.0

    roster = []
    for r in read_by_header(wb['Assignments']):
        c, s, rl = pname(r.get('client_name')), pname(r.get('staff_name')), tidy(r.get('role'))
        if c and s and rl in RANK:
            roster.append((c, s, rl))

    staff = collections.defaultdict(
        lambda: {'roles': {}, 'total': 0.0, 'pct': None, 'status': 'Active',
                 'email': '', 'sheet_unpaid': {}, 'capacity_mode': ''})
    rates = {}
    for r in read_by_header(wb['Staff']):
        nm, rl = pname(r.get('name')), tidy(r.get('role'))
        if not nm or rl not in RANK:
            continue
        d = staff[nm]
        d['roles'][rl] = num(r.get('available_hours'))
        d['total'] += num(r.get('total_hours'))
        d['status'] = tidy(r.get('status')) or 'Active'
        d['email'] = tidy(r.get('email'))
        if r.get('client_pct') not in (None, ''):
            d['pct'] = num(r.get('client_pct'))
        if num(r.get('unpaid_off_hours')):
            d.setdefault('sheet_unpaid', {})[rl] = num(r.get('unpaid_off_hours'))
        if num(r.get('daily_rate')):
            rates[nm] = num(r.get('daily_rate'))
        # 'actual' = availability tracks real client work rather than a daily
        # rate. Set per person in the sheet so no name is hard-coded here.
        if tidy(r.get('capacity_mode')):
            d['capacity_mode'] = tidy(r.get('capacity_mode')).lower()

    clients, budget = [], {}
    for r in read_by_header(wb['Clients']):
        nm = tidy(r.get('name'))
        if not nm:
            continue
        clients.append(nm)
        budget[nm] = r          # dict, keyed by header

    return roster, staff, clients, budget, rates


class ClientResolver:
    """Maps a QB (jobcode_1, jobcode_2, jobcode_3) triple to a scope client name."""

    def __init__(self, scope_clients):
        self.names = list(scope_clients)
        self.exact = {}
        self.loose = collections.defaultdict(list)
        for n in self.names:
            self.exact[norm(n)] = n
            self.loose[norm(n, True)].append(n)
        # which parents actually have sub-clients in the scope sheet
        self.parents = collections.defaultdict(list)
        for n in self.names:
            if ':' in n:
                self.parents[norm(n.split(':', 1)[0])].append(n)

    def _match(self, cand):
        k = norm(cand)
        if k in self.exact:
            return self.exact[k]
        lk = norm(cand, True)
        if len(self.loose.get(lk, [])) == 1:
            return self.loose[lk][0]
        return None

    def resolve(self, j1, j2, j3):
        j1, j2, j3 = tidy(j1), tidy(j2), tidy(j3)
        # apply operator renames/merges to the incoming jobcode too, so a client
        # that was renamed in the app still matches its QB spelling
        j1 = _RENAME.get(j1, _MERGE.get(j1, j1))
        alias = QB_ALIASES.get(j1.lower())
        if alias:
            hit = self._match(alias)
            if hit:
                return hit, None
        if j1 in _DROP:
            return None, j1
        sub = j3 or j2
        # QB often repeats the parent inside the child: "Parent - Child"
        if sub and ' - ' in sub:
            sub = sub.split(' - ', 1)[1].strip()

        # a parent with sub-clients in scope -> resolve to the sub
        if sub and norm(j1) in self.parents:
            hit = self._match(j1 + ': ' + sub)
            if hit:
                return hit, None
            # try the sub against the parent's children by its tail
            cands = [n for n in self.parents[norm(j1)]
                     if norm(n, True).endswith(norm(sub, True))]
            if len(cands) == 1:
                return cands[0], None
            return None, f'{j1} > {sub}'

        # otherwise roll up to the parent (some parents have no sub-clients)
        hit = self._match(j1)
        if hit:
            return hit, None
        return None, (j1 + (' > ' + sub if sub else ''))


def is_onboarding_item(si):
    si = tidy(si).lower()
    return any(k in si for k in ONBOARDING_ITEMS)


def load_timesheet(path, resolver):
    client_hours = collections.defaultdict(float)   # (client, person) -> hrs
    pto = collections.defaultdict(float)            # person -> hrs
    internal = collections.defaultdict(float)
    internal_by_person = collections.defaultdict(float)
    banked = collections.defaultdict(float)
    unresolved = collections.defaultdict(float)
    logged = collections.defaultdict(float)         # person -> ALL hours logged
    phase = collections.defaultdict(lambda: {'onb': 0.0, 'total': 0.0})
    with open(path, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            person = pname((r.get('fname') or '') + ' ' + (r.get('lname') or ''))
            j1 = tidy(r.get('jobcode_1'))
            if not person or not j1:
                continue
            try:
                h = float(r.get('hours') or 0)
            except ValueError:
                h = 0.0
            logged[person] += h
            low = j1.lower()
            if any(k in low for k in BANKED_CODES):
                banked[person] += h
                continue
            if low in PTO_CODES:
                pto[person] += h
                continue
            if low.startswith(INTERNAL_PREFIX):
                internal[(j1, person)] += h
                internal_by_person[person] += h
                continue
            client, miss = resolver.resolve(j1, r.get('jobcode_2'), r.get('jobcode_3'))
            if client is None:
                unresolved[(miss, person)] += h
                continue
            client_hours[(client, person)] += h
            phase[client]['total'] += h
            if is_onboarding_item(r.get('service item')):
                phase[client]['onb'] += h
    return (client_hours, pto, internal, unresolved, logged, phase,
            internal_by_person, banked)


def canon(name):
    """Operator renames + merges, applied everywhere a client name appears."""
    n = tidy(name)
    n = _RENAME.get(n, n)
    return _MERGE.get(n, n)


def build(period, scope_path, timesheet_path, rate_table, unpaid_off=None,
          app_path=None):
    """
    app_path — read the roster, staff and clients from the CapacityIQ Data
    workbook (the app is the source of truth). Falls back to the scope
    spreadsheet when not given, which is how the historical months were built.
    """
    unpaid_off = unpaid_off or {}
    year, month = int(period[:4]), int(period[5:7])
    wd = workdays(year, month)

    global QB_ALIASES, _RENAME, _MERGE, _DROP
    if app_path:
        # name mappings come from the sheet, so the engine carries no client names
        QB_ALIASES, _RENAME, _MERGE, _DROP = load_aliases(app_path)
        roster, staff, scope_clients, budget, app_rates = load_app(app_path)
        rate_table = dict(rate_table or {})
        rate_table.update(app_rates)     # the sheet's daily_rate wins
    else:
        QB_ALIASES = dict(getattr(OV, 'QB_ALIASES', {}))
        _RENAME = dict(getattr(OV, 'CLIENT_RENAME', {}))
        _MERGE = dict(getattr(OV, 'CLIENT_MERGE', {}))
        _DROP = set(getattr(OV, 'CLIENT_DROP', set()))
        wb = openpyxl.load_workbook(scope_path, data_only=True)
        roster = read_roster(sheet(wb, 'assignments', 'template'))
        staff = read_staff(sheet(wb, 'staff'))
        budget_ws = sheet(wb, 'clients', 'budget')
        scope_clients, budget = [], {}
        for r in budget_ws.iter_rows(min_row=2, values_only=True):
            if not r or not r[0]:
                continue
            nm = tidy(r[0])
            scope_clients.append(nm)
            budget[nm] = r

    scope_clients = [canon(c) for c in scope_clients
                     if canon(c) not in _DROP]
    if not app_path:
        # bootstrap-only; in app mode the client list IS the app's Clients tab,
        # so anything missing from it is genuinely new and must be flagged
        for c, _s, _r in OV.ROSTER_ADD:
            if canon(c) not in scope_clients: scope_clients.append(canon(c))
        for c in getattr(OV, 'CLIENT_PENDING', {}):
            if canon(c) not in scope_clients: scope_clients.append(canon(c))
    budget = {canon(k): v for k, v in budget.items() if canon(k) not in _DROP}
    for c in scope_clients: budget.setdefault(c, None)
    resolver = ClientResolver(scope_clients)
    (client_hours, pto, internal, unresolved, logged, phase,
     internal_by_person, banked) = load_timesheet(timesheet_path, resolver)

    roster = [(canon(c), s, rl) for c, s, rl in roster
              if app_path or s not in OV.STAFF_DROP]
    if not app_path:
        # bootstrap-only: these corrections are already in the app's own data
        roster += [(canon(c), s, rl) for c, s, rl in OV.ROSTER_REPLACE]
        roster += [(canon(c), s, rl) for c, s, rl in OV.ROSTER_ADD]
    seen_r = set(); dedup = []
    for c, s, rl in roster:
        if (c, s, rl) in seen_r: continue
        seen_r.add((c, s, rl)); dedup.append((c, s, rl))
    roster = dedup

    roles_for = collections.defaultdict(list)
    for c, s, rl in roster:
        roles_for[(c, s)].append(rl)
    primary = {p: max(d['roles'], key=d['roles'].get)
               for p, d in staff.items() if d['roles']}

    report = {'period': period, 'workdays': wd, 'unresolved_clients': [],
              'unknown_person': [], 'not_rostered': [], 'multi_role': [],
              'internal_time': [], 'pto': [], 'banked': [], 'inactive': [],
              'jenn': None,
              'phase_onboarding': [], 'phase_review': [],
              'cleanup_on_active': [], 'hours_short': [], 'hours_over': [],
              'recon': {}}

    # --- client phase, from the service items on their time entries ----------
    phases = {}
    for c, d in sorted(phase.items()):
        if d['total'] <= 0.05:
            continue
        share = d['onb'] / d['total']
        if share >= ONB_CONFIDENT:
            phases[c] = 'Onboarding'
            report['phase_onboarding'].append(
                {'client': c, 'onb_hours': round(d['onb'], 2),
                 'total': round(d['total'], 2), 'share': round(share * 100)})
        elif share >= ONB_REVIEW:
            report['phase_review'].append(
                {'client': c, 'onb_hours': round(d['onb'], 2),
                 'total': round(d['total'], 2), 'share': round(share * 100)})
        elif d['onb'] > 0.05:
            # Clean-up on a client that is plainly not onboarding. The service
            # item is for onboarding only, so this is either miscoded time or a
            # client that has quietly gone back into cleanup.
            report['cleanup_on_active'].append(
                {'client': c, 'onb_hours': round(d['onb'], 2),
                 'total': round(d['total'], 2), 'share': round(share * 100)})
    report['phases'] = phases
    report['cleanup_hours'] = {c: round(d['onb'], 2) for c, d in phase.items()
                               if d['onb'] > 0.05}

    assignments = []
    for (c, p), h in sorted(client_hours.items()):
        h = round(h, 2)
        rs = roles_for.get((c, p))
        if rs:
            role = max(rs, key=lambda r: RANK[r])
            if len(rs) > 1:
                report['multi_role'].append(
                    {'client': c, 'staff': p, 'hours': h, 'roles': rs, 'used': role})
        else:
            role = primary.get(p)
            if not role:
                report['unknown_person'].append({'client': c, 'staff': p, 'hours': h})
                continue
            report['not_rostered'].append(
                {'client': c, 'staff': p, 'hours': h, 'role_used': role})
        assignments.append({'client': c, 'staff': p, 'role': role, 'hours': h})

    # keep the roster visible at 0 hrs for clients that had activity this month
    active = {a['client'] for a in assignments}
    have = {(a['client'], a['staff']) for a in assignments}
    for c, s, rl in roster:
        if c in active and (c, s) not in have:
            assignments.append({'client': c, 'staff': s, 'role': rl, 'hours': 0.0})

    for (code, person), h in sorted(internal.items(), key=lambda x: -x[1]):
        report['internal_time'].append({'code': code, 'staff': person, 'hours': round(h, 2)})
    for (miss, person), h in sorted(unresolved.items(), key=lambda x: -x[1]):
        report['unresolved_clients'].append({'jobcode': miss, 'staff': person,
                                            'hours': round(h, 2)})

    # ---- capacity -----------------------------------------------------------
    actual_by_person = collections.defaultdict(float)
    for a in assignments:
        actual_by_person[a['staff']] += a['hours']

    staff_rows = []
    for nm, d in sorted(staff.items()):
        if nm in OV.STAFF_DROP:
            report['inactive'].append({'staff': nm, 'reason': 'no longer at the firm'})
            continue
        pct = d['pct']
        rate = (rate_table.get(nm) if app_path
                else OV.RATE_OVERRIDES.get((nm, period), rate_table.get(nm)))
        ptoh = round(pto.get(nm, 0.0), 2)
        if ptoh:
            report['pto'].append({'staff': nm, 'hours': ptoh})
        if banked.get(nm, 0.0) > 0.05:
            report['banked'].append({'staff': nm,
                                     'hours': round(banked[nm], 2)})

        # capacity_mode='actual': availability tracks real client work rather
        # than a daily rate (operator's step 7). Set per person in the sheet.
        if d.get('capacity_mode') == 'actual':
            act = round(actual_by_person.get(nm, 0.0), 2)
            role = primary.get(nm) or 'Lead'
            report['jenn'] = {'actual_client_hours': act}
            staff_rows.append({'name': nm, 'role': role, 'base_hours': act,
                               'pto_hours': ptoh, 'available_hours': act,
                               'total_hours': act, 'client_pct': 1.0,
                               'daily_rate': 0.0,
                               'logged_hours': round(logged.get(nm, 0.0), 2),
                               'expected_hours': 0.0,
                               'internal_hours': round(
                                   internal_by_person.get(nm, 0.0), 2),
                               'unpaid_off_hours': 0.0, 'banked_off_hours': 0.0,
                               'status': d['status'], 'email': d['email']})
            continue

        if not pct or not rate or d['total'] <= 0:
            report['inactive'].append({'staff': nm, 'reason':
                'no client %' if not pct else ('no rate' if not rate else 'zero hours this month')})
            for role, av in d['roles'].items():
                staff_rows.append({'name': nm, 'role': role, 'base_hours': 0.0,
                                   'pto_hours': 0.0, 'available_hours': 0.0,
                                   'total_hours': 0.0, 'client_pct': pct or 0.0,
                                   'daily_rate': rate or 0.0,
                                   'logged_hours': 0.0, 'expected_hours': 0.0,
                                   'internal_hours': 0.0, 'unpaid_off_hours': 0.0,
                                   'banked_off_hours': 0.0,
                                   'status': d['status'], 'email': d['email']})
            continue

        base_total = round(rate * wd, 2)
        # unpaid / uncoded time off, carried forward from the sheet if the
        # operator already recorded it for this person this month
        if app_path:
            # the sheet stores it already scaled by client_pct; unscale so the
            # arithmetic below is the same in both modes
            _p = d['pct'] or 1
            unpaid = round(sum(v for k, v in d.get('sheet_unpaid', {}).items()) / _p, 2) \
                if d.get('sheet_unpaid') else round(unpaid_off.get(nm, 0.0), 2)
        else:
            unpaid = round(unpaid_off.get(nm, 0.0), 2)
        bank = round(banked.get(nm, 0.0), 2)
        net_total = round(max(0.0, base_total - ptoh - unpaid - bank), 2)
        logged_total = round(logged.get(nm, 0.0), 2)
        # preserve the person's existing split across roles
        split_base = sum(d['roles'].values()) or 1.0
        for role, av in sorted(d['roles'].items(), key=lambda x: -RANK[x[0]]):
            share = av / split_base
            staff_rows.append({
                'name': nm, 'role': role,
                'base_hours': round(base_total * pct * share, 2),
                'pto_hours': round(ptoh * pct * share, 2),
                'available_hours': round(net_total * pct * share, 2),
                'total_hours': round(net_total * share, 2),
                'client_pct': pct, 'daily_rate': rate,
                # total time this person recorded in QB (all jobcodes), against
                # what a full month at their rate would be. A big gap either way
                # is a signal: low = absent or under-logging, high = their
                # recorded rate is too low.
                'logged_hours': round(logged_total * share, 2),
                'expected_hours': round(base_total * share, 2),
                # internal (Paxus Admin etc). Not client capacity, but it is
                # real time — someone whose admin has ballooned has less room
                # than their planned client capacity suggests.
                'internal_hours': round(
                    internal_by_person.get(nm, 0.0) * share, 2),
                'unpaid_off_hours': round(unpaid * pct * share, 2),
                'banked_off_hours': round(bank * pct * share, 2),
                'status': d['status'], 'email': d['email'],
            })

    qb_total = 0.0
    with open(timesheet_path, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if not tidy((r.get('fname') or '') + ' ' + (r.get('lname') or '')):
                continue
            if not tidy(r.get('jobcode_1')):
                continue
            try:
                qb_total += float(r.get('hours') or 0)
            except ValueError:
                pass
    client_total = sum(h for h in client_hours.values())
    pto_total = sum(pto.values())
    banked_total = sum(banked.values())
    internal_total = sum(internal.values())
    unresolved_total = sum(unresolved.values())
    entered = sum(a['hours'] for a in assignments)
    report['recon'] = {
        'qb_report_total': round(qb_total, 2),
        'client_hours': round(client_total, 2),
        'pto': round(pto_total, 2),
        'banked': round(banked_total, 2),
        'internal': round(internal_total, 2),
        'unresolved': round(unresolved_total, 2),
        'accounted': round(client_total + pto_total + banked_total
                           + internal_total + unresolved_total, 2),
        'entered_in_app': round(entered, 2),
        'balances': abs(qb_total - (client_total + pto_total + banked_total
                                    + internal_total + unresolved_total)) < 0.05,
        'app_ties_to_client_hours': abs(entered - client_total) < 0.05,
    }
    # --- who didn't record a full month, and who recorded more --------------
    # An absence with no PTO benefit only shows as hours that never got logged,
    # so this is the standing question each month: is there a known reason?
    by_person = collections.defaultdict(
        lambda: {'logged': 0.0, 'expected': 0.0, 'pto': 0.0, 'off': 0.0,
                 'pct': 0.0})
    for r in staff_rows:
        d = by_person[r['name']]
        d['logged'] += r.get('logged_hours', 0.0)
        d['expected'] += r.get('expected_hours', 0.0)
        d['pto'] += r.get('pto_hours', 0.0)
        d['off'] += r.get('unpaid_off_hours', 0.0)
        d['pct'] = d['pct'] or r.get('client_pct', 0.0)
    for nm, d in sorted(by_person.items()):
        if d['expected'] <= 0:
            continue
        recorded = round(d['off'] / d['pct'], 2) if d['pct'] else 0.0
        gap = round(d['expected'] - d['logged'] - recorded, 2)
        adj = (d['logged'] + recorded) / d['expected'] * 100
        entry = {'staff': nm, 'logged': round(d['logged'], 2),
                 'expected': round(d['expected'], 2),
                 'coded_pto': round(d['pto'] / d['pct'], 2) if d['pct'] else 0.0,
                 'already_recorded': recorded, 'gap': gap,
                 'pct_of_expected': round(adj, 1)}
        if adj < 88:
            report['hours_short'].append(entry)
        elif adj > 112:
            report['hours_over'].append(entry)


    return assignments, staff_rows, report
