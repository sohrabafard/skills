# Finding The Real Bound On N

Load before stating any budget, and whenever a bound is about to be assumed rather than found.

`SKILL.md` owns the rule: the bound is found in the system, never assumed; the value used is the largest the system
permits; a bound that cannot be found is unbounded and is reported as a design defect. This file says where to look
per class of dimension, what to ask, and what to do when production data is unavailable.

## Where each class of dimension is found

Work down this list for the path under examination. Each row names the artifact that holds the answer, so the bound
is read rather than estimated.

| Dimension | Where its maximum is enforced, if anywhere |
|---|---|
| Items in one request | The request schema or validation rule: array `maxItems`, string length, file size limit |
| Rows returned by a query | The page size cap at the route, or the `LIMIT` in the query — a query with neither is unbounded |
| Rows per tenant | Nothing in the code. Read the largest tenant's current count from production and apply the growth horizon |
| Retained history | The retention policy or the partition drop job. No retention policy means unbounded |
| Fan-out per event | The recipient, subscriber, or consumer list length, and whatever bounds that list |
| Concurrent in-flight work | The in-flight limit and worker count, owned by `/alaa-services-contract` (`$alaa-services-contract`) |
| Depth of a tree, graph, or recursion | The explicit depth limit. Recursion with no depth limit is unbounded |
| Distinct keys in a cache or map held across requests | The eviction policy and maximum entry count. No maximum means unbounded |
| Retries multiplying a downstream call | The retry budget, owned by `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Elements in an uploaded or imported file | The upload size limit divided by the smallest plausible record size |

The rows with no enforcing artifact are the interesting ones. They are where the defect lives, and naming the
missing boundary is the deliverable.

## The four questions per dimension

1. **What is the largest value the system currently permits?** Not the largest observed — permitted. An enforced
   maximum of ten thousand is the bound even when today's largest tenant holds forty.
2. **What makes it grow?** Signups, time, a customer's own usage, a bulk import, an integration partner. A dimension
   that grows with time is unbounded unless something deletes.
3. **What does an attacker or a mistaken client control?** A dimension a caller sets is bounded by the validation
   rule, never by the caller's good behaviour. A request field with no maximum is a request field an attacker sets
   to a million.
4. **What is the worst case, not the typical one?** The median tenant, the demo dataset, and the developer's own
   account are the three sources that make an unbounded path look fine in review.

## When the worst case is a product

**A worst case that is a product of dimensions is computed, not estimated.** Multiply every dimension that
participates, then multiply by any per-instance factor — replicas, partitions, workers, retries.

Worked shapes that recur here:

- notification fan-out: `recipients_per_command x channels_per_recipient x retries_per_send`;
- permission evaluation: `resources_in_page x relations_checked_per_resource`;
- an import: `rows_in_file x lookups_per_row`;
- a scheduled reconciliation: `rows_scanned_per_run x runs_per_day`.

**A product that cannot be computed because one factor has no maximum is unbounded, and "it is probably small" is an
unbounded answer.** This is the same discipline `/alaa-observability-soc` (`$alaa-observability-soc`) applies to
metric cardinality, where an uncomputable worst case is refused rather than accepted.

## When production data is unavailable

Do not stop, and do not guess silently. Take the largest bound available in this order and label it:

1. **`boundary`** — a maximum enforced in code, a schema, or a platform contract. Always preferred, because it is
   true by construction rather than by observation.
2. **`measurement`** — the largest value observed in production, with where it was read and when, multiplied by the
   growth horizon the design states.
3. **`assumption`** — a stated figure with the reasoning that produced it, marked as an assumption in the budget.

An assumption is legitimate and can be checked against production later; silence cannot. What is never acceptable is
an unlabelled number, because the next reader cannot tell whether it is enforced, observed, or invented.

## Turning an unbounded dimension into a bounded one

The fix is always a boundary, and the boundary goes at the outermost place that can enforce it, so nothing
downstream has to trust its caller:

- a maximum page size at the route, with a default and a rejection above the maximum rather than a silent clamp —
  silently clamping makes a client's pagination loop skip records;
- `maxItems` on every array in a request schema, and a maximum length on every string;
- a `LIMIT` on every query whose result feeds a loop or a response;
- an explicit maximum batch size wherever work is grouped;
- a maximum depth on every recursive traversal, returning an error at the limit rather than truncating silently;
- a maximum entry count and an eviction policy on every map that outlives a request;
- a retention policy on every table that only ever grows.

**Report the boundary you added or the boundary that is missing, in the same change.** An unbounded dimension
reported with no named boundary leaves the next engineer to re-derive what you already worked out, and the platform
values for any of these boundaries belong to `/alaa-services-contract` (`$alaa-services-contract`) rather than to
this file.

## Anti-patterns

- a bound read from the seed data, the fixture, or the developer's own tenant;
- "the list is always short" with no artifact enforcing shortness;
- a maximum enforced in the frontend only, where the API accepts anything;
- a clamp that silently reduces an over-large request instead of rejecting it, so the caller never learns its
  request was truncated;
- a growth horizon omitted, which bounds the dimension at the day the budget was written;
- treating a dimension bounded by a well-behaved client as bounded.
