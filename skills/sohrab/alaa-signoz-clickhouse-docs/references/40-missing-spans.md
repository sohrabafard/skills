# Missing Spans

Read this when SigNoz reports that a trace has missing spans, when a trace tree is broken, or when a
service dependency edge you expect is absent.

## What SigNoz is telling you

A span is reported missing when a collected span references a parent span id that no other span in
the same trace matches. The warning is about the *parent*, not about the span you are looking at:
the span in front of you arrived, and the one it names as its parent did not.

That distinction decides the whole investigation. A missing parent is either a span that was never
created, a span that was created and never arrived, or a parent id that was never real.

## The four causes, in the order worth checking

The vendor documents three, read from `https://signoz.io/docs/userguide/traces/` on 2026-07-30:
**tail sampling**, **spans dropped in transit**, and **services that never export**. Each is a real
span that did not reach storage.

The fourth is the one this fleet actually hits, and it is different in kind: **a parent id that was
never a real span.** A service generates its own `traceparent` value for response headers or log
correlation, then hands that generated value to the OpenTelemetry extractor as if it were inbound
context. The extractor believes it, so the request's server span is created as a child of a span id
that nothing ever exported. No sampling, no drop, no network fault — the parent never existed.

Check the fourth cause first when the affected spans are all server spans at the edge of one
service, and when the missing parent ids belong to no service in the graph. Check the vendor's three
when the missing parents are spread across services or correlate with a deployment or a load spike.

## The fix, when it is cause four

State it as a rule about inbound context, not about headers:

- Extract a parent from inbound W3C trace context **only when that context arrived on the request**.
  A value the process generated is not inbound context, whatever variable holds it.
- When inbound context is missing or invalid, start the request server span as a **root** span. Do
  not synthesise a parent to make the trace look connected; a fabricated parent turns one honest
  root into a permanent missing-span warning.
- Use the context of the span the SDK actually started for response headers and log correlation.
  Keep a locally generated fallback header only on paths where telemetry is disabled or failing
  open, and never feed it back into the extractor.

Whether W3C context propagation is required at all, and on which hops, is a gate owned by
`/alaa-observability-soc` (`$alaa-observability-soc`) `references/20-instrumentation-gates.md`. This
file owns only what a broken propagation looks like in SigNoz and how to read it.

## Verifying the fix

Send one request with **no** `traceparent` header at all. The service's server span must come back
with an empty parent span id, and its database and outbound spans must parent to that server span.
If the server span still carries a parent id, the generated value is still reaching the extractor.

This is an observation, not an inspection: run the request, then look at the trace.

## Confirming the scope with SQL

When ClickHouse access exists, the anti-join under *Recent spans whose parent span is missing* in
`clickhouse-traces-reference.md` lists the affected spans and shows whether the missing parents
cluster on one service. It tells you **which** spans are orphaned, not **why**, so read the causes
above first and use the query to confirm.

## A missing dependency edge is this same failure

SigNoz's dependency graph is built by a view that joins a span to its parent on
`A.span_id = B.parent_span_id`, so every cause above erases edges exactly as it erases parents. That
is why the graph is a lower bound and why a missing edge is never evidence that a call does not
happen. `50-service-topology.md` states what the graph does and does not record.
