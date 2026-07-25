# Quantitative Budgets

Load when a change adds or alters a metric label, a histogram bucket set, or a sampling or profiling rate, or when the
question is whether a signal is affordable.

Three numbers are decided here and nowhere else: how many metric series a service may hold, where latency histogram
buckets fall, and what fraction of traces and profiles survives. Which label names are permitted at all is the contract's
list (`/alaa-services-contract`, `$alaa-services-contract` in Codex, `references/21-…`); this file sets the ceilings that
a permitted label can still breach.

## Cardinality: the series budget

Series count is the *product* of the cardinalities of a metric's labels, not their sum. Five labels at ten values each
produce 100,000 series from a single metric family, and one unbounded label multiplies series by one per request until
the metrics backend runs out of memory — which takes down metrics for every service sharing that backend, not just the
one that added the label. That blast radius is why these are hard ceilings and not guidance.

Ceilings, per service per environment, counted across all replicas:

| Budget | Ceiling |
|---|---|
| active time series, whole service | 50,000 |
| active time series, one metric family | 2,000 |
| distinct values of one label | 50 |
| distinct values of the templated-route label | 200, and only because it is templated |
| labels on one metric beyond service and environment | 5 |
| buckets on one latency histogram, including the overflow bucket | 16 |

Gate, before a metric or label change merges:

1. Compute the worst-case series count: multiply the declared distinct-value count of every label, then multiply by
   replica count if any label carries an instance dimension. Record the number in the change.
2. A change whose worst case cannot be computed is treated as unbounded and is refused. "It is probably small" is an
   unbounded answer.
3. Answer yes to all four of these, or the value goes to a span or log attribute instead and is reached through
   `trace_id`: is the value set bounded and small **under attack traffic as well as normal traffic**; is it stable across
   releases and tenants; can it be aggregated meaningfully for an SLO or capacity question; is it free of PII and
   secrets and not unique per request?
4. Breaching a ceiling requires a named owner and a written storage-cost figure recorded in the change. Silence is a
   refusal, not an approval.

The attack-traffic clause is the one most often missed: a label that is bounded by a valid client can be unbounded by a
hostile one, and a metrics backend is a denial-of-service target through any label an attacker can set.

Avoid combining two medium-cardinality labels on one metric even when both pass individually — that combination is how a
metric passes review at 40 series and arrives in production at 4,000.

## Histogram bucket boundaries

A percentile is interpolated *inside* the bucket it falls in, so a bucket that straddles the SLO threshold makes the SLO
unmeasurable: every value in that bucket reads as the same latency. The rule follows from that.

Rule: for every latency histogram with an SLO, at least three bucket boundaries fall below the SLO threshold and at least
two above it, one boundary sits on the threshold itself, and the total stays inside the 16-bucket ceiling above.

Platform default bucket sets, in seconds. Use these unless the service's SLO threshold differs, in which case move a
boundary onto the actual threshold and keep the shape.

| Histogram | Boundaries |
|---|---|
| inbound request duration | 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 5, 10 |
| dependency call and database query duration | 0.001, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5 |
| queue message and job duration | 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 30, 60, 300, 900 |

Rules:

- When an SLO threshold changes, move or add a bucket boundary onto the new threshold in the same change. A threshold
  with no boundary within 20% of it is not measurable, and an alert on it will fire or stay silent for arithmetic
  reasons rather than real ones.
- Use histograms for latency and never averages or summaries across replicas: summary quantiles cannot be aggregated
  across instances, so a fleet p99 computed from them is not a p99 of anything. Histograms aggregate, and they are what
  carries exemplars.
- Native histograms remove the boundary question, and the contract states the condition under which the platform allows
  them; until that condition holds, these explicit boundaries apply.

## Sampling

The decision: **head sampling stays at 100% inside every service; volume reduction happens by tail sampling at the
central gateway Collector, and nowhere else.**

Reason: a head sampler decides before the outcome is known, so on a service at 99.99% availability it drops the rare
failing traces with the same probability as the common succeeding ones — and those rare traces are the entire content of
the SLA. A tail sampler sees the finished trace and can keep every error deterministically.

Tail-sampling policy at the gateway, evaluated in this order:

1. keep 100% of traces containing a span with error status;
2. keep 100% of traces whose root duration exceeds the route's p99 SLO threshold;
3. keep 100% of traces carrying an event from the security catalog in `70-soc-evidence.md`;
4. keep 5% of everything remaining, and never less than 1% — below that a service has no baseline traffic to compare an
   incident against, which makes the kept error traces uninterpretable.

Constraints:

- Until tail sampling is actually deployed at the gateway, head sampling stays at 100% and volume is controlled by the
  cardinality and retention budgets. Introducing a head sampler as an interim measure trades away the failure evidence
  the SLA is defined on.
- Tail sampling runs at the gateway tier only. Across more than one gateway instance it requires the trace-affinity
  routing the contract mandates, because two instances each seeing part of a trace make independent keep decisions and
  produce half-traces, which are worse than no trace: they read as a missing dependency.
- Structured per-request logs are never sampled where the service contract requires one record per request.
- Metrics are never sampled. Aggregation is already the reduction mechanism.

Rates for the auxiliary paths:

| Path | Default | Ceiling without a written cost review |
|---|---|---|
| Sentry error capture | on, unsampled | — |
| Sentry tracing | 0 | 0.01, and only after duplication with the platform trace path is reviewed |
| Sentry profiling | 0 | 0.01 |
| continuous profiling on a service | 0 | 0.01 |

Every rate above 0 carries a named owner, a rollback switch, and a stated cost expectation in the change. Profiling in
particular starts disabled and is raised only after trace and metric evidence has already localised a real performance
problem; it answers *why* code is slow, and asking it before you know *what* is slow spends production budget on
narrowing nothing.
