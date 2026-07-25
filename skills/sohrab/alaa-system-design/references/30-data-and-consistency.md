# Data Ownership And Consistency

`SKILL.md` owns the one-writer rule and the cache-versus-fork rule. This file says how to build the
ownership table, how to resolve a proposed second writer, how to choose a consistency model, which
interleavings a write path must rule out, and what a fork obliges. Read it during step 4.

`/alaa-data-layer` (`$alaa-data-layer`) owns the mechanics — schema, constraints, indexes, migrations,
isolation levels, pooling, projections, Redis behaviour. This file decides what must be true; that skill
decides how it is enforced.

## Build the ownership table

One row per piece of data the design reads or writes, including data owned by another service:

| Datum | Owning component | Who writes it | Who reads it | How readers read it |
|---|---|---|---|---|

"How readers read it" takes one of four values and no others: through the owner's interface; from an event
the owner emits; from a declared replica the owner publishes; or directly from the owner's datastore. The
fourth value is a finding, not a design — record it, then decide whether it becomes one of the first three
or the reader is merged into the owner.

## When two components want to write the same datum

Exactly three resolutions exist. Pick one and record it; leaving it unresolved means the last write wins
and no one decided that.

1. **One is the owner** and the other writes through the owner's interface. The cost is a hop; the benefit
   is a single place where the invariant is enforced.
2. **They are two different data sharing a name.** Split them, name them differently, and state the
   relation between them. This is the resolution the vocabulary hides: "status" in two components is
   usually two statuses.
3. **The datum moves** to a component that owns both write paths, which is a boundary change and returns
   to step 2.

## Draw the read path and the write path

For each critical journey write the hop sequence for reads and for writes, naming at each hop the component,
the datum, and whether the value read may be stale. A path drawn without the staleness column is a diagram;
the staleness column is what turns it into a design.

Then state, for each journey, whether it needs to read its own writes. **Read-your-own-writes is a
requirement, not a property that happens.** When the journey needs it and the read path crosses a replica,
a cache, or an event, the design names the mechanism that provides it — routing that read to the owner,
waiting on a version, or returning the written value from the write itself.

## Choose the consistency model

One question decides it: **what does a reader do with a value that is stale by the maximum staleness this
path can produce?**

| Answer | Model | What the design must then state |
|---|---|---|
| Takes an action that cannot be undone, moves money or entitlement, or grants access | Read from the owner inside the same transactional boundary; no cache, no replica | The boundary, and the constraint that enforces the invariant. If the read decides whether a caller may act, it is a gate and `/alaa-security-review` (`$alaa-security-review`) owns it — never a cache |
| Takes an action a named later step can correct | Bounded staleness | The bound, the compensating step, who runs it, and how a correction is observed |
| Is displayed, or feeds a computation that runs again | Eventual | The convergence trigger and the maximum time to converge |

The question is about the consequence of staleness, not about how important the data feels. Applying it
consistently is what makes two agents choose the same model for the same read.

## Rule out the interleavings

For every write path, name which of these must be impossible and the mechanism class that makes it
impossible. A write path with none named has decided that all of them are acceptable.

- **Lost update** — two writers read, compute, and write, and one result disappears. Ruled out by a version
  check, a conditional write, or a lock held across the read and the write.
- **Double effect** — the same logical request applied twice, from a retry, a redelivery, or a user's second
  click. Ruled out by an idempotency key with a uniqueness constraint in the same store as the effect; the
  full contract, including two concurrent requests carrying one key, belongs to `/alaa-reliability-sla`
  (`$alaa-reliability-sla`).
- **Out-of-order application** — a later state overwritten by an earlier one, which any at-least-once
  delivery will produce. Ruled out by a monotonic version on the datum, not by trusting delivery order.
- **Phantom or cross-tenant read** — a query that sees rows it must not. `/alaa-security-review` owns
  tenant isolation; the design states which reads are scoped and by what.

Name the mechanism class here and let `/alaa-data-layer` pick the construct. A design that names the exact
index or isolation level has taken a decision it cannot enforce.

## Cache or fork

Apply the rule in `SKILL.md` by answering two questions about the second copy:

1. **If it were deleted right now, would anything be lost that cannot be recovered by re-reading the owner?**
2. **Does anything write to it without also writing to the owner?**

Two noes means cache. Any yes means fork.

A cache carries, in the record: its key, its maximum age, its invalidation trigger, and what a request does
on a miss and on a cache outage. A cache with no stated maximum age is a fork that has not been recognised
yet, because nothing will ever delete it.

A fork carries, in the record: which copy wins when they disagree, the reconciliation path that detects and
repairs drift, who runs it and how often, and the signal that shows drift exists — the signal's design
belongs to `/alaa-observability-soc` (`$alaa-observability-soc`). A fork is a legitimate design; an
unrecognised fork is a data-loss incident with a long fuse.

A projection or a read model is a fork unless it can be rebuilt from the owner's data alone. State the
rebuild procedure and whether it has ever been run. **A projection nobody has rebuilt is a projection that
cannot be rebuilt.**

## Anti-patterns

- a second copy added "for performance" with no maximum age and no invalidation trigger;
- read-your-own-writes assumed across a replica or an event, which works in every test and fails under load;
- a cross-service join performed by reading another service's tables, which makes that service's schema a
  contract nobody agreed to;
- a distributed workflow with no compensating step, where the design assumes the second write succeeds;
- ordering guaranteed by "the broker delivers in order", which stops being true at the first redelivery or
  the second consumer;
- an idempotency key stored somewhere other than the store holding the effect, so the two can disagree.
