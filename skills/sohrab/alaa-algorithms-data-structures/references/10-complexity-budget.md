# The Complexity Budget

Load when writing, recording, or reviewing a budget, and before returning any report from this skill.

`SKILL.md` owns the definition — four parts, and fewer than four is not a budget. This file says where a budget
lives, how to write bounds that involve more than one dimension, what a reviewer rejects, and the report block
every task using this skill returns.

## Where a budget is recorded

One budget lives in exactly one place, chosen by how long the decision must survive:

| Situation | Where the budget goes |
|---|---|
| A single function or method whose cost is not obvious from reading it | A comment on the function, above the signature |
| A route, consumer, job, or scheduled task | The handler's doc comment, beside the deadline the path already honours |
| A decision that shaped the design of a subsystem | The design record, per `/alaa-system-design` (`$alaa-system-design`) |
| A budget a test enforces | The test's name or its one-line comment, so a failure reads as a budget breach |

A budget recorded in a ticket, a chat message, or a pull-request description is not recorded. Those are read once,
by the people who already knew, and the next engineer to touch the path reads the code.

**One budget per operation, not per file and not per function.** An operation that spans four functions gets one
budget on the entry point, because the bound is a property of the whole call, and four partial budgets can each be
true while the operation misses the sum.

## Writing the bound

Use whatever notation the repository already uses. `O(n)` and "one query regardless of page size" are equally
acceptable; precision of notation buys nothing here, and the named dimension and stated size carry the meaning.

Prefer the countable form when one exists, because it is checkable by a test rather than by argument:

- "one query per request, regardless of page size" — a query-count assertion can enforce this.
- "one outbound call per event, regardless of recipient count" — a call-count assertion can enforce this.
- "memory proportional to chunk size, not to row count" — a peak-memory assertion can enforce this.

`O(...)` is the fallback for in-process work where no count is available.

### More than one growing dimension

Write every dimension that grows. An operation over `pages x rows_per_page` is bounded in both, and a budget naming
only one of them is satisfied by an implementation that moves the cost into the other.

```text
export_tenant is O(rows) time and O(chunk) memory in rows, one query per chunk,
measured at rows = 2,000,000, chunk = the configured default.
```

When two dimensions multiply, state the product and the bound on the product, because that product is the number
that actually reaches production. This is the same rule the cardinality ceiling in `/alaa-observability-soc`
(`$alaa-observability-soc`) applies to labels.

### Amortised and worst-case bounds

When a bound holds on average but not on every call — a structure that occasionally grows and copies, a cache that
occasionally refills, a batch that occasionally flushes — state both the amortised bound and the worst single call,
and say which one the path's deadline must accommodate. A path whose deadline is sized for the amortised case fails
on the call that pays the whole cost, and that call is the one a user is waiting on.

## What a reviewer rejects

Reject and return, naming which part is missing:

1. A bound with no dimension. "Fast", "efficient", "optimised", "O(1) lookups" with no statement of what is looked
   up in what.
2. A dimension with no bound found in the system — see `20-finding-n.md`. The budget cannot be checked against a
   number nobody has.
3. A stated size that is smaller than the enforced maximum on the dimension. A budget measured below the maximum the
   system permits says nothing about the path at that maximum.
4. A budget added in the same commit as the implementation with no evidence it preceded it, on a path where a
   structure decision was actually made. Order matters because a budget written afterwards is a description.
5. A budget that restates a value another skill owns — a timeout, a pool size, a page cap, a cardinality ceiling.
   Cite the owning skill instead, so the budget does not drift when the owner changes.

## Keeping a budget true

A budget is a claim about the future, so it decays. Two rules keep it honest:

- **The budget is re-checked when its dimension's enforced maximum changes.** Raising a page cap, a batch cap, or a
  retention window is a change to every budget stated in that dimension, and the change that raises the maximum
  re-states or re-measures them.
- **A budget breached in production is corrected in the code, not in the document.** Editing the stated bound to
  match observed behaviour converts a broken promise into a true description and removes the only signal that
  anything is wrong.

## The report block

Return these fields, in this order, for any budget decision, structure choice, or review of either. A field the task
did not reach is marked `not reached` rather than omitted, because an omitted field reads as "nothing to report".

```text
Decision: budget-stated | no-budget-required | blocked
Path: the operation, its entry point, and which of the three trigger conditions fired
Dimensions: dimension -> enforced maximum -> where enforced -> source (boundary|measurement|assumption)
Budget: operation -> growing dimension -> bound -> size at which measured or reasoned
Structure: chosen -> the access-pattern answer that chose it -> alternative rejected -> what revives it
Calls in loops: call site -> loop dimension -> resolution -> batch cap -> partial-failure behaviour
Memory: peak proportional to -> materialised|streamed -> chunk size, default, validated range
Tuning points: value -> configurable yes|no -> default -> validated range -> what moving it changes
Evidence: two input sizes -> observed ratio -> claimed shape -> agrees|disagrees
Gaps: unbounded dimensions and the boundary each needs, claims not measured, values another skill owns
```

`Gaps` is the field that carries the work this task did not do. An empty `Gaps` on a path with an unbounded
dimension is a false report, and the unbounded dimension is exactly what the next reader needs to see.
