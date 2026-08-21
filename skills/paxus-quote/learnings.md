# /paxus-quote — learnings

Corrections and decisions captured from real runs. Recurring items get promoted into `SKILL.md`; see Phase 7.

## 2026-08-10 — Cassie & Lisa — electrical contractor (for-profit)

Two operators independently built a quote for the same prospect, then compared them line by line. Most of what came out of that session was promoted straight into `SKILL.md` the same day — the locked comparison table, the locked card wording, the required onboarding date, the workers' comp / GL vs annual audit distinction, the "how this works" alternative to page 3, and the house wording items. What stayed here is the pricing side, which is **not** ready to be built into the skill.

### [DECISION] The firm rate ladder — settled

Set jointly, 2026-08-10. Billing rates, not salaries. Firm-level: the same ladder prices every quote.

| Role | Billing rate | Fully burdened cost | Markup |
|---|---|---|---|
| Staff | **$90/hr** | ~$21/hr | 4.3× |
| Lead | **$135/hr** | ~$35/hr | 3.9× |
| Controller | **$165/hr** | ~$41/hr | 4.0× |

- Blends near **$110/hr**, but the intent is to build from roles. The blend hides which role is carrying the work.
- Gross margin across the ladder runs **74–77%**, against a firm floor of **65%**. The cushion is deliberate — it absorbs unforeseen hours and the third person who ends up touching the file.
- **Lead is the thinnest margin and the firm's bottleneck.** Watch buildups that push hours onto the lead.
- **These margin figures carry no profit share and no benefits.** Real margin is thinner than the table shows; don't treat 77% as headroom to discount into.
- Derived from a specific payroll snapshot. Re-check after raises, new hires, or a benefits change.
- Lead moved from $130 to $135 in this session. Prior figures in circulation — lead at $130 or $150, controller at $250 — are superseded.

### [DECISION] The advisory step-up — Premium is priced above its hours

**Premium sits at least $700 above Full Service**, typically $700–750, regardless of what the hours math produces.

The hours barely separate the two levels — the controller's time differs by an advisory call and its prep, two or three hours. Priced straight off the ladder, Premium lands only a few hundred above Full Service, and a cheap advisory call is the fastest route to an inefficient firm: clients book more calls, the controller absorbs them, and the tier stops paying for itself. The controller rate was briefly set at $250 to solve this before the standalone step-up replaced that approach.

### [BLOCKER] How budgeted hours get calculated is undefined — this is what gates pricing

The rates are settled. The other half of pricing is not: there is no agreed method for estimating hours by role for a given client.

The evidence that this matters: the two independent buildups of the same prospect landed at **13.5 hours** and **16.5 hours** at Full Service — **$126/hr against $109/hr** — behind monthly fees that differed by only $100. The similar headline hid a ~15% difference in effective rate, and that gap repeats on every quote written off this ladder.

Until there's a method, the skill cannot price honestly, and two people using it will keep producing different hours from the same facts.

### [DECISION] Pricing was deliberately kept out of `SKILL.md`

Pricing was built into the skill on 2026-08-10 and **removed the same day** at the operator's instruction: *"We will eventually want this skill to price but we aren't there yet."* The skill stays a formatter — it takes fees and budgeted hours from the operator and does not derive either.

**Do not re-add a pricing phase or the rate ladder to `SKILL.md` until the hours method above exists.** The rates alone are not enough, and a half-built pricing phase produces confident numbers with nothing behind them.

### [SUGGESTION] Things to carry into the pricing work when it happens

- **Estimating agents double-count.** One run counted the same work under both coding and cleanup and produced a figure several times too large. Any startling number should be re-derived before it's believed.
- **Estimating low is not a kindness.** Understated hours don't reduce the work — they misstate the capacity budget and hide an unprofitable engagement until someone burns out on it.
- **Don't price AI efficiency straight through to the client.** As tooling takes work out of the process, hours fall. That does not become "this takes ten minutes now, so we'll charge $25." Price the outcome and the responsibility. The efficiency gain is the firm's margin and it funds the next improvement.
- **Gut-check the fee against the client's size.** A defensible hours-based number can still be one the client cannot pay. Surface it rather than shipping arithmetic that won't get signed.
- **The old service-fee template's only real output is the hours**, which the firm administrator needs for the budget. Its useful residue is the per-item time anchors — bank transactions, invoicing, bill pay. The rest is subjective and isn't worth reproducing.

## 2026-08-21 — Lisa — for-profit construction consulting (S-corp, new entity)

### [PROMOTED] KPI tracking belongs in Full Service, not Premium

Her words: *"tracking KPIs is included in full service. That needs to go on the tier
above advisory call so all the check marks for full service are in line."*

Two things in one correction, and the second is the more general one:

- **The tier change.** KPI tracking & benchmarking is a Full Service element. Premium's
  differentiators are the advisory call, the budget/forecast, and the audit support.
- **Row order follows the checkmarks.** When a row changes tiers it has to be
  repositioned so each column's ✓ run stays unbroken. A gap mid-column reads to a client
  as a mistake rather than a distinction.

Both promoted to `SKILL.md` the same day — the default table, the card copy, the
level-differences table, and a new bullet under § Rules for changing the default.

### [SUGGESTION] The hard onboarding-date rule has now failed twice — change it

The 2026-08-21 real-estate entry already flagged this and said *"revisit before the next
quote."* This was the next quote, and the same thing happened: the useful answer was a
**window** ("week of September 21st"), not a date, and the quote shipped fine with it.

The skill still calls a specific date **blocking**. It isn't, in practice, and treating it
as blocking just means the operator gets asked a question she can't answer yet. Proposal:
accept a window, keep the first close month required, and let the exact date be set later
without holding the quote. Two occurrences now — this qualifies for promotion.

### [DECISION] Premium was set below the standard advisory step-up, knowingly

The 2026-08-10 decision puts Premium at least $700 above Full Service. This quote went out
at **$425 / $950 — a $525 step-up.** Raised with the operator before building; she chose
$950 deliberately.

Recorded because it is a real exception to a firm-level rule, not an error, and the
internal hours-budget file carries a note telling a future reviser not to "correct" it
back without asking. Worth watching whether the $700 floor holds in practice or wants
restating as a guideline.

### [SUGGESTION] The cover's preparer-name field has no source

`[PREPARER NAME]` on page 1 assumes the operator's full name is known. It wasn't — the
operator profile carried a first name only, and inventing a surname on a client proposal
isn't an option. The quote shipped with `Paxus CPA Group · August 2026` and no preparer
line, which reads fine. Either make the field genuinely optional in the template, or have
Phase 1 ask for it once.

### [DECISION] Sensitive call material stays out of the shared-drive summary

Phase 4 asks for the discovery-call minutes to be filed alongside the quote. This call's
meeting note was marked sensitive — it carried client disclosures that bear on whether to
take the engagement at all. Filing it as-is would have put that in front of the whole
team.

Resolution: a separate **team-scoped** scoping summary was written for the shared drive
(scope, systems, method items, what's quoted) and the full note stayed in the vault.
Worth saying explicitly in Phase 4 — the minutes that get filed are the ones the team
needs to serve the engagement, not necessarily everything that was said.
