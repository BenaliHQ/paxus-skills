"""
Write one month back into the CapacityIQ Data sheet.

Runs ONLY after the operator has approved the review. The snapshot itself is
NOT taken here — `createSnapshot` lives in the app and stays the app's job, so
there is one implementation of snapshot logic rather than two that can drift.
The operator captures the snapshot in the app once this has run.

`createSnapshot` freezes whatever is currently in Clients / Staff / Assignments,
so Assignments must end up holding THIS month and nothing else — last month's
rows are replaced wholesale, not merged.

Schema note: the Assignments tab is written with its exact header schema. Never
add a column to that tab — Code.gs rebuilds the whole row from the header and
blanks anything its record does not know about (see Code.gs ~line 759).
"""
import json
import subprocess

ASSIGN_COLS = ['assignment_id', 'client_id', 'client_name',
               'staff_id', 'staff_name', 'role', 'hours']
STAFF_NUMERIC = ['base_hours', 'pto_hours', 'available_hours', 'total_hours',
                 'logged_hours', 'expected_hours', 'internal_hours',
                 'unpaid_off_hours', 'banked_off_hours']


def _gws(*args, payload=None):
    cmd = ['gws'] + list(args)
    if payload is not None:
        cmd += ['--json', json.dumps(payload)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    body = p.stdout
    i = body.find('{')
    if i < 0:
        raise RuntimeError(f'gws returned no JSON: {p.stdout[:200]} {p.stderr[:200]}')
    return json.loads(body[i:])


def _get(sid, rng):
    return _gws('sheets', 'spreadsheets', 'values', 'get',
                '--params', json.dumps({'spreadsheetId': sid, 'range': rng})
                ).get('values', [])


def _put(sid, rng, values):
    return _gws('sheets', 'spreadsheets', 'values', 'update',
                '--params', json.dumps({'spreadsheetId': sid, 'range': rng,
                                        'valueInputOption': 'RAW'}),
                payload={'values': values})


def _put_many(sid, pairs):
    """Many ranges in ONE API call. Per-cell writes are far too slow — 22 staff
    rows x 9 columns is ~200 round trips and times out."""
    if not pairs:
        return
    _gws('sheets', 'spreadsheets', 'values', 'batchUpdate',
         '--params', json.dumps({'spreadsheetId': sid}),
         payload={'valueInputOption': 'RAW',
                  'data': [{'range': r, 'values': [[v]]} for r, v in pairs]})


def _clear(sid, rng):
    return _gws('sheets', 'spreadsheets', 'values', 'clear',
                '--params', json.dumps({'spreadsheetId': sid, 'range': rng}),
                payload={})


def _rows(sid, tab):
    """Tab as a list of dicts plus its header and 1-based row numbers."""
    vals = _get(sid, f'{tab}!A:ZZ')
    if not vals:
        return [], []
    hdr = [str(h).strip() for h in vals[0]]
    out = []
    for i, r in enumerate(vals[1:], start=2):
        d = {h: (r[j] if j < len(r) else '') for j, h in enumerate(hdr)}
        d['_row'] = i
        out.append(d)
    return hdr, out


def _next_id(existing, prefix, width):
    n = 0
    for v in existing:
        s = str(v or '')
        if s.startswith(prefix) and s[len(prefix):].isdigit():
            n = max(n, int(s[len(prefix):]))
    while True:
        n += 1
        yield f'{prefix}{n:0{width}d}'


def write_month(sid, period, assignments, staff, new_clients=None, dry_run=True):
    """new_clients: [{'name':..., 'service_type':..., budgets...}] approved in §2."""
    plan = {'period': period, 'dry_run': dry_run,
            'clients_added': [], 'assignment_rows': 0,
            'assignments_replaced': 0, 'staff_updated': 0, 'unmatched': []}

    chdr, crows = _rows(sid, 'Clients')
    shdr, srows = _rows(sid, 'Staff')
    ahdr, arows = _rows(sid, 'Assignments')

    if ahdr != ASSIGN_COLS:
        raise RuntimeError(f'Assignments schema changed: {ahdr}')

    # --- new clients approved in section 2 ---------------------------------
    cid = {str(c['name']).strip(): str(c['client_id']) for c in crows if c.get('name')}
    gen = _next_id([c.get('client_id') for c in crows], 'C', 4)
    add_rows = []
    for nc in (new_clients or []):
        nm = str(nc['name']).strip()
        if nm in cid:
            continue
        new_id = next(gen)
        cid[nm] = new_id
        rec = dict(nc, client_id=new_id)
        rec.setdefault('status', 'Active')
        add_rows.append([rec.get(h, '') for h in chdr])
        plan['clients_added'].append({'name': nm, 'client_id': new_id})

    # --- staff ids keyed by (name, role) -----------------------------------
    sid_map = {(str(s.get('name', '')).strip(), str(s.get('role', '')).strip()):
               (str(s.get('staff_id', '')), s['_row']) for s in srows}

    # --- assignment rows ---------------------------------------------------
    gena = _next_id([], 'A', 4)
    lines = []
    for a in assignments:
        cn, sn, rl = a['client'], a['staff'], a['role']
        if cn not in cid:
            plan['unmatched'].append({'kind': 'client', 'name': cn,
                                      'hours': a['hours']})
            continue
        hit = sid_map.get((sn, rl))
        if not hit:
            hit = next((v for (n, r), v in sid_map.items() if n == sn), None)
        if not hit:
            plan['unmatched'].append({'kind': 'staff', 'name': sn,
                                      'client': cn, 'hours': a['hours']})
            continue
        lines.append([next(gena), cid[cn], cn, hit[0], sn, rl,
                      round(float(a['hours']), 2)])
    plan['assignment_rows'] = len(lines)
    plan['assignments_replaced'] = len(arows)

    # --- staff numeric updates ---------------------------------------------
    updates = []
    for s in staff:
        hit = sid_map.get((s['name'], s['role']))
        if not hit:
            plan['unmatched'].append({'kind': 'staff-row', 'name': s['name'],
                                      'role': s['role']})
            continue
        row = hit[1]
        for col in STAFF_NUMERIC:
            if col in shdr and col in s:
                a1 = _a1(shdr.index(col) + 1)
                updates.append((f'Staff!{a1}{row}', round(float(s[col] or 0), 2)))
    plan['staff_updated'] = len({u[0].split('!')[1][1:] for u in updates})

    if dry_run:
        return plan

    # --- apply -------------------------------------------------------------
    if add_rows:
        start = len(crows) + 2
        _put(sid, f'Clients!A{start}', add_rows)
    if arows:
        _clear(sid, f'Assignments!A2:G{len(arows) + 1}')
    if lines:
        _put(sid, 'Assignments!A2', lines)
    _put_many(sid, updates)
    return plan


def _a1(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s
