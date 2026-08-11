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

### ~~[BLOCKER] How budgeted hours get calculated is undefined~~ — RESOLVED 2026-08-11

The blocker below stood from 2026-08-10 until 2026-08-11, when the hours method was worked out with Lisa and validated against the same client. **The gate is met; pricing now lives in `SKILL.md` Phase 0.** Kept here for the reasoning.

> The rates are settled. The other half of pricing is not: there is no agreed method for estimating hours by role for a given client.
>
> The evidence that this matters: the two independent buildups of the same prospect landed at **13.5 hours** and **16.5 hours** at Full Service — **$126/hr against $109/hr** — behind monthly fees that differed by only $100. The similar headline hid a ~15% difference in effective rate, and that gap repeats on every quote written off this ladder.
>
> Until there's a method, the skill cannot price honestly, and two people using it will keep producing different hours from the same facts.
>
> **[DECISION] Pricing was deliberately kept out of `SKILL.md`.** Built in on 2026-08-10 and removed the same day at the operator's instruction: *"We will eventually want this skill to price but we aren't there yet."* Do not re-add a pricing phase or the rate ladder until the hours method exists.

## 2026-08-11 — Lisa — electrical contractor (for-profit) — PRICING METHOD SETTLED

Worked out against the same client, comparing Lisa's buildup line-by-line against Cassie's. The full method is in `SKILL.md` Phase 0; this records what it resolved and why.

### [DECISION] Two of the three divergences were definitional, not judgment

The two buildups came out 15.1 hours and 16.5. Once compared component by component, the **staff layer agreed within 0.6 hours** — it is arithmetic off counted inputs. The whole gap sat in lead and controller, which had no anchors.

More striking: the coding counts differed because one treated **bill payments as auto-matches** and the other didn't. And "55 bills" turned out to be the count of bill *payments*, not bills *entered* — it matched the right answer by coincidence. Neither was an estimating error. Both were definition errors, which is why the fix is a script rather than better judgment.

### [DECISION] The settled definitions

- **A decision** = register line on a reconciled bank/card account that isn't an auto-match. **Bill payments count** — they land a cent off the bill and take real time to match. **Deposits split both ways** by their split account; they are frequently *not* from undeposited funds, so the type can't be classified wholesale.
- **Reconciliation is banded** 20/10/5 min by monthly line volume. A flat rate understates a 91-line operating account and overstates a dead Profit First account.
- **Accounts count by statement**, not by QBO account. Five employee cards on one statement are one reconciliation and one surcharge.
- **Project and class tracking** = 2.5 lead + 1.0 controller, applied once. Tagging rides inside the coding rate.
- **Sales tax filing is lead work at $135**, not staff $90 as the retired template had it.
- **Basic holds at 0.85 × Full as a rule**, not a calculation — built from its own hours it lands within ~$130 of Full, which doesn't read as a tier.

### [DECISION] Volume from bookkeeper activity needs normalizing; volume from bank activity does not

Bank-feed lines exist whether or not anyone codes them. Bills entered, invoices created, and journal entries posted exist only if somebody did the work. So **average bookkeeper-driven counts over the months the process was actually running.**

The client's bills entered ran 54 · 65 · 56 · 46 · 52 · 24 · 0 — all-months gave 42/mo, working-months 55/mo. The bills never stopped arriving; the entry stopped. Pricing off 42 would have underpriced go-forward work by 25%. The test is whether a low month reflects less business or less bookkeeping: that client's zero-bill month was their best revenue month of the year.

### [VALIDATION] The method reproduces the operator's own buildup

Run end to end: **14.72 hours, $1,907.60 raw, $118/hr effective** — against Lisa's judgment-built 15.1 hours and $1,881.50, and landing on her account count of 11 and surcharge of $100 exactly. Every volume input derived rather than estimated. `scripts/gl-volume.py` reproduces the hand analysis on the same file.

### [OPEN] Cleanup is still unquantified — it is the next piece

Cleanup was deliberately left out of Phase 0. What surfaced while scoping it:

- The two cleanup estimates differed because they priced **different periods for the same defects** — one a two-month gap-fill, the other a full-period rebuild. Not an hours disagreement.
- The shape a method would take: per defect, capture what's broken · how many periods it spans · whose hours fix it · bulk-reclassify vs line-by-line.
- **Coding-cleanup hours must never be counted against monthly coding.** That double-count once produced a figure several times too large.
- Operator's judgment check that killed the bad number: the client tracks ~$1.5M, so *"we can't afford that"* — and $6,600 read as *"almost half a year essentially for a cleanup."*

Take cleanup and setup figures from the operator until this ships. It may warrant its own skill.

### [SUGGESTION] Things to carry into the pricing work when it happens

- **Estimating agents double-count.** One run counted the same work under both coding and cleanup and produced a figure several times too large. Any startling number should be re-derived before it's believed.
- **Estimating low is not a kindness.** Understated hours don't reduce the work — they misstate the capacity budget and hide an unprofitable engagement until someone burns out on it.
- **Don't price AI efficiency straight through to the client.** As tooling takes work out of the process, hours fall. That does not become "this takes ten minutes now, so we'll charge $25." Price the outcome and the responsibility. The efficiency gain is the firm's margin and it funds the next improvement.
- **Gut-check the fee against the client's size.** A defensible hours-based number can still be one the client cannot pay. Surface it rather than shipping arithmetic that won't get signed.
- **The old service-fee template's only real output is the hours**, which the firm administrator needs for the budget. Its useful residue is the per-item time anchors — bank transactions, invoicing, bill pay. The rest is subjective and isn't worth reproducing.
