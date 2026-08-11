"""
Render the six-section month-end review.

Sections 2, 3 and 5 are questions for the operator — the run stops there and
waits. Nothing is written to the sheet until she approves.

Output is markdown, so it reads correctly in a terminal, in Cowork, and in
whatever the runner opens the saved file with. The reconciliation block stays
in a code fence to hold its decimal alignment.

PRIVACY. Sections 3 and 4 name individuals and are deliberately absent from the
app, which may be shared with the whole team. The report is written to the
RUNNER'S OWN Downloads folder and nowhere else — never to the shared Capacity
folder in Drive, where ten of the people named in section 3 have access.
Passing it on is a human decision, not something this script makes.
"""
import calendar
import csv
import os


def _h(n):
    return f'{round(float(n or 0), 1):g}'


def coverage(timesheet_path, period):
    """Sanity check that the export covers the whole month.

    Month-end only, by operator instruction — this catches a truncated export,
    it is not support for a deliberate mid-month run.
    """
    days = set()
    with open(timesheet_path, newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            for k in ('date', 'Date', 'local_date'):
                v = (row.get(k) or '').strip()[:10]
                if len(v) == 10:
                    days.add(v)
                    break
    if not days:
        return None
    y, m = int(period[:4]), int(period[5:7])
    last = calendar.monthrange(y, m)[1]
    lo, hi = min(days), max(days)
    return {'first': lo, 'last': hi,
            'covers_month': lo <= f'{y:04d}-{m:02d}-01' and hi >= f'{y:04d}-{m:02d}-{last:02d}'}


def _table(headers, rows, align=None):
    if not rows:
        return []
    align = align or ['---'] * len(headers)
    out = ['| ' + ' | '.join(headers) + ' |',
           '|' + '|'.join(align) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(c) for c in r) + ' |')
    out.append('')
    return out


def render(period, assignments, staff, report, cover=None):
    R = report
    o = []
    ch = sum(a['hours'] for a in assignments)
    av = sum(s['available_hours'] for s in staff)
    util = round(ch / av * 100) if av else 0

    o.append(f'# CapacityIQ — {period} month-end review')
    o.append('')
    o.append(f'{len({a["client"] for a in assignments})} clients · '
             f'{len(assignments)} assignment rows · {R["workdays"]} workdays  ')
    o.append(f'**{_h(ch)} client hours** against **{_h(av)} available** — '
             f'**{util}% firm utilisation**')
    o.append('')
    o.append('> Contains per-person detail. Keep it to Cassie, Jenn and Lisa '
             'unless you have decided otherwise.')
    o.append('')

    if cover and not cover['covers_month']:
        o.append(f'> [!warning] The timesheet covers {cover["first"]} to {cover["last"]}, '
                 f'not the whole month. This is built for month-end — check the export.')
        o.append('')

    # --- 1 --------------------------------------------------------------
    rc = R['recon']
    o.append('## 1. Reconciliation')
    o.append('')
    o.append('```')
    o.append(f'QB report total     {_h(rc["qb_report_total"]):>9}')
    o.append(f'  client hours      {_h(rc["client_hours"]):>9}')
    o.append(f'  internal (Paxus)  {_h(rc["internal"]):>9}')
    o.append(f'  PTO               {_h(rc["pto"]):>9}')
    o.append(f'  banked time off   {_h(rc["banked"]):>9}')
    o.append(f'  unresolved        {_h(rc["unresolved"]):>9}')
    o.append(f'accounted for       {_h(rc["accounted"]):>9}')
    o.append('```')
    o.append('')
    ok = lambda b: 'yes' if b else '**NO — STOP**'
    o.append(f'- every hour accounted for: {ok(rc["balances"])}')
    o.append(f'- app ties to client hours: {ok(rc["app_ties_to_client_hours"])}')
    o.append('')

    # --- 2 --------------------------------------------------------------
    o.append('## 2. New clients — *needs your answer*')
    o.append('')
    if R['unresolved_clients']:
        o.append('Hours logged against something with no entry in the app. '
                 'Give me the team and budgets and I will add them.')
        o.append('')
        o += _table(['Job code', 'Hours', 'Logged by'],
                    [(x['jobcode'], _h(x['hours']), x['staff'])
                     for x in R['unresolved_clients']],
                    ['---', '---:', '---'])
    else:
        o.append('None — every job code resolved to a known client.')
        o.append('')

    # --- 3 --------------------------------------------------------------
    o.append('## 3. Hours short — *needs your answer*')
    o.append('')
    if R['hours_short']:
        o.append('Recorded less than a full month with no reason on file. '
                 'If you know why, tell me and I will record it — if you do not, '
                 'these are the conversations to have.')
        o.append('')
        o += _table(['Person', 'Logged', 'Expected', 'Gap', '% of expected'],
                    [(x['staff'], _h(x['logged']), _h(x['expected']),
                      _h(x['gap']), f'{x["pct_of_expected"]:.0f}%')
                     for x in sorted(R['hours_short'], key=lambda z: -z['gap'])],
                    ['---', '---:', '---:', '---:', '---:'])
    else:
        o.append('None.')
        o.append('')

    # --- 4 --------------------------------------------------------------
    o.append('## 4. Hours over target')
    o.append('')
    if R['hours_over']:
        o.append('Either the rate on file is stale, or they are genuinely over. '
                 'Not guessing which.')
        o.append('')
        o += _table(['Person', 'Logged', 'Expected'],
                    [(x['staff'], _h(x.get('logged')), _h(x.get('expected')))
                     for x in R['hours_over']],
                    ['---', '---:', '---:'])
    else:
        o.append('None.')
        o.append('')

    # --- 5 --------------------------------------------------------------
    o.append('## 5. Client phase — *needs your answer*')
    o.append('')
    any5 = False
    if R['phase_onboarding']:
        any5 = True
        o.append(f'**Classified as Onboarding ({len(R["phase_onboarding"])})** — '
                 f'over half their hours are onboarding or clean-up.')
        o.append('')
        o += _table(['Client', 'Share', 'Onboarding hrs', 'Total hrs'],
                    [(x['client'], f'{x["share"]}%', _h(x['onb_hours']), _h(x['total']))
                     for x in R['phase_onboarding']],
                    ['---', '---:', '---:', '---:'])
    if R['phase_review']:
        any5 = True
        o.append(f'**In the 20–50% band ({len(R["phase_review"])})** — your call, '
                 f'I have not decided.')
        o.append('')
        o += _table(['Client', 'Share', 'Onboarding hrs', 'Total hrs'],
                    [(x['client'], f'{x["share"]}%', _h(x['onb_hours']), _h(x['total']))
                     for x in R['phase_review']],
                    ['---', '---:', '---:', '---:'])
    if R['cleanup_on_active']:
        any5 = True
        o.append(f'**Clean-up coded on an Active client ({len(R["cleanup_on_active"])})** — '
                 f'miscoded time, or quietly back in clean-up.')
        o.append('')
        o += _table(['Client', 'Clean-up hrs', 'Total hrs'],
                    [(x['client'], _h(x['onb_hours']), _h(x['total']))
                     for x in R['cleanup_on_active']],
                    ['---', '---:', '---:'])
    if not any5:
        o.append('Nothing to review — every client reads as Active.')
        o.append('')

    # --- 6 --------------------------------------------------------------
    n = (len(R['not_rostered']) + len(R['multi_role']) + len(R['pto'])
         + len(R['banked']) + len(R['inactive']) + len(R['unknown_person']))
    o.append(f'## 6. Judgement calls made ({n})')
    o.append('')
    o.append('Nothing here is silent. A high count means the roster is drifting.')
    o.append('')

    def block(title, rows, headers, fmt, align=None):
        if not rows:
            return
        o.append(f'**{title} ({len(rows)})**')
        o.append('')
        o.extend(_table(headers, [fmt(x) for x in rows], align))

    block('Not rostered — used their primary role', R['not_rostered'],
          ['Person', 'Client', 'Hours', 'Role used'],
          lambda x: (x['staff'], x['client'], _h(x['hours']), x['role_used']),
          ['---', '---', '---:', '---'])
    block('On the client in more than one role — used the highest', R['multi_role'],
          ['Person', 'Client', 'Hours', 'Roles', 'Used'],
          lambda x: (x['staff'], x['client'], _h(x['hours']),
                     ', '.join(x['roles']), x['used']),
          ['---', '---', '---:', '---', '---'])
    block('PTO applied', R['pto'], ['Person', 'Hours'],
          lambda x: (x['staff'], _h(x['hours'])), ['---', '---:'])
    block('Banked overtime drawn down', R['banked'], ['Person', 'Hours'],
          lambda x: (x['staff'], _h(x['hours'])), ['---', '---:'])
    block('No capacity calculated', R['inactive'], ['Person', 'Reason'],
          lambda x: (x['staff'], x['reason']))
    block('Name not recognised', R['unknown_person'], ['Name', 'Hours'],
          lambda x: (x.get('staff', '?'), _h(x.get('hours'))), ['---', '---:'])

    if R.get('jenn'):
        o.append(f'**Availability tracked to actual client work** '
                 f'(`capacity_mode=actual`): {_h(R["jenn"]["actual_client_hours"])} hrs')
        o.append('')

    o.append('---')
    o.append('')
    o.append('**Nothing has been written to the sheet.** Answer sections 2, 3 and 5, '
             'then the month gets written back and you capture the snapshot in the app.')
    return '\n'.join(o)


def save(text, period, folder=None):
    """Write the review to the runner's own Downloads folder.

    Deliberately local. Whoever runs this decides who else sees it.
    """
    folder = folder or os.path.join(os.path.expanduser('~'), 'Downloads')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'CapacityIQ Review - {period}.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return path
