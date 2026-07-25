# Error Budgets And SLOs

Read when an SLI, SLO, error budget, or release-gating policy is defined or challenged. This file owns how a target becomes a budget and what the budget obliges. **The burn-rate alerting arithmetic — the multi-window table, the confirmation-window ratio, the page-versus-ticket split, no-data behaviour, and the low-traffic exception — is owned by `/alaa-observability-soc` (`$alaa-observability-soc` in Codex) `references/40-alerting-slo-retention.md`.** Read that file to write the alert; read this one to decide what the alert is about and what happens when it fires.

## The chain: SLI, SLO, budget

- An **SLI** is a ratio of good events to valid events, measured from real traffic.
- An **SLO** is a target for that ratio over a stated window.
- The **error budget** is the complement: the quantity of bad events the SLO permits in the window. It is a budget in the literal sense — a finite amount that is spent, by outages, by deploys, by experiments, and by ordinary noise.

The budget's purpose is to turn "is our reliability good enough?" into arithmetic with an owner, so that the answer stops depending on whose incident is most recent. Without it, every reliability argument is a debate about anecdotes, which the loudest recent failure wins.

Each of the three needs one owner and one window, written down. An SLO without a stated window is not a target: 99.99% over a year and 99.99% over an hour permit different outages entirely.

## Defining an SLI that cannot be gamed

Five rules, each of which fixes a specific way SLIs go wrong.

1. **Count events, not time.** "Minutes of downtime" requires a definition of down, which becomes a negotiation during the incident. A request either succeeded within the threshold or it did not.
2. **Define "good" as a predicate on a single event** — this status class, and this latency threshold — evaluable per request with no aggregation. A predicate over an average cannot be evaluated per event and therefore cannot produce a budget.
3. **Measure as close to the user as the service can observe**, which for a backend service is at ingress after the request is admitted, and for a user-facing flow is at the edge. A number measured after the failing hop excludes the failures.
4. **Name the denominator explicitly.** Which requests are valid events, and which are excluded. Health probes, synthetic monitors, and load-test traffic are excluded because they are not users. **A request shed under load is a bad event and is never excluded** — excluding shed requests makes the SLO green during overload, which is the one condition it exists to catch.
5. **Include latency in the availability predicate** for any interactive route. A response that arrives after the caller gave up is a failure that a status-only SLI records as a success, which is how a service can hold 99.99% availability while being unusable.

## The budget arithmetic and burn rate

The budget is `(1 − target) × valid events in the window`. Stated as time it is `(1 − target) × window`, which is the form that makes a tight target concrete: a target with four nines leaves a budget measured in minutes per month, not hours.

**Burn rate is the multiple of the even spend rate.** Burn rate 1 spends the budget exactly evenly and exhausts it at the end of the window; burn rate 10 exhausts it in a tenth of the window. It is the right unit because it is dimensionless — the same threshold means the same thing on a service with a thousand times the traffic — and because it converts an error rate into the only question an operator needs at three in the morning: how long until there is nothing left.

Two properties to hold onto. A short spike of a very high burn rate and a long period of a slightly elevated one can consume identical budget, and both matter, which is why burn-rate alerting uses more than one window. And a burn rate below 1 is not a problem to be alerted on; it is the system operating inside its target.

## What consuming the budget obliges

**The policy is decided before the incident, because a policy decided during one is a negotiation.** Write it down, with an owner, in the service's own documentation.

The default policy:

- **Budget remaining** — ship normally. Release velocity is what the budget is for.
- **Budget exhausted for the trailing window** — changes that are not reliability fixes or rollbacks do not ship to that service, and the next unit of work is the largest contributor to the burn. The freeze lifts when the trailing window's budget is back inside the target, not when the incident closes.
- **Burning fast enough to exhaust the window's budget within hours** — this is an incident, and the response is mitigation and rollback, not analysis.

An error budget with no consequence attached is a dashboard. The consequence is the whole mechanism: it is what makes reliability work compete on equal terms with feature work, using a number both sides agreed to in advance.

The converse obligation is the one teams skip. **A budget that is never consumed means the SLO is set below what the service actually delivers**, and the response is to spend it deliberately — release more often, run the fault-injection experiments in `80-verification.md`, retire redundant machinery — or to tighten the target. An unspent budget is unpurchased velocity, and it also hides a target so loose that it will not detect a real regression.

Two more rules that keep a budget honest:

- **Do not reset or exempt the budget for a "known cause".** An outage caused by a dependency, a cloud provider, or a bad deploy spent the user's reliability regardless of whose fault it was. Excluding causes turns the budget into a scorecard, and a scorecard can be argued with.
- **Do not run a fault-injection experiment while the budget is exhausted.** The budget is the permission to experiment; without it there is no permission.

## An SLO on a symptom, never on a cause

**A symptom is what the user experiences: did this request succeed, within this latency? A cause is a mechanism inside the service: CPU, pool utilisation, queue depth, one dependency's error rate.**

Symptom SLOs survive re-architecture, because the user's experience is defined independently of how the service is built, and they cover failure modes nobody enumerated in advance. Cause SLOs fail in both directions: they go green while users are failing through a path the cause metric does not touch, and they go red while users are fine, which trains everyone to ignore them.

Causes still deserve instrumentation, thresholds, and dashboards — they are how an incident is diagnosed once a symptom alert has fired. They do not carry the SLO, and they do not page. `/alaa-observability-soc` (`$alaa-observability-soc`) owns that split for alerting.

The practical test when someone proposes an SLI: **name the user-visible failure this number would miss.** If the answer is short and easy to produce, the number is a cause.

## Aggregation hides the failures that matter

A fleet-wide SLO can be met while a whole class of users is completely broken. At a four-nines target, a tenant or a route carrying less than the budget's share of traffic can fail 100% of the time without moving the aggregate at all.

So define budgets at the granularity of the promise:

- **Per critical route family**, because a working browse path does not compensate for a broken checkout path.
- **Per tenant**, where per-tenant isolation is something the platform promises. Where that would produce too many SLOs to manage, track the worst-performing tenant's ratio as its own SLI, which catches the same failure with one number.
- **Per user-facing journey** for flows that span services, because each service can be inside its own SLO while the composed journey is outside any of them. A journey's target is derived from its hops rather than assumed: with independent hops the achievable target is the product of theirs, so a journey with several nine-nine-nine-nine hops does not itself reach four nines.

## SLA, SLO, and the gap between them

The **SLA** is the external commitment with a consequence — credits, penalties, a contract. The **SLO** is the internal target, and it is strictly stricter than the SLA. The gap is the whole point: it is the distance in which a problem can be detected and fixed before it becomes a commercial event. An SLO set equal to the SLA gives the team no warning and converts every budget overrun into a customer conversation.

The SLA's window and definitions are also frequently not the SLO's, and the difference must be recorded rather than assumed identical, since a monthly contractual availability computed on a different denominator than the internal SLI produces two numbers that disagree during exactly the month someone asks.
