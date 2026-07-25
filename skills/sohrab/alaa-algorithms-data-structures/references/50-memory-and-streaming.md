# Memory And Streaming

Load when a result set, export, import, or file is read whole, and when peak memory is in question.

`SKILL.md` owns the rule: peak memory is stated as proportional to a named dimension, and a collection whose element
count is a growing dimension is streamed rather than materialised. This file says how to decide, what breaks
streaming, and what a chunked operation owes its caller.

## Stating peak memory

Peak memory is stated the same way as time, in the dimension that grows:

```text
export_tenant holds O(chunk) rows in memory regardless of tenant size,
measured at rows = 2,000,000, chunk = the configured default.
```

Two properties make the statement useful. It names what is *not* proportional to the growing dimension, which is the
claim a reviewer checks. And it is enforceable: a test that runs the operation over a large fixture and asserts peak
memory stays inside a band will fail when someone reintroduces materialisation.

The dimension that drives memory is often not the one that drives time. A path can be linear in rows for time and
constant in rows for memory, and that combination is the goal for every export, import, and report.

## Materialise or stream

**Materialise** when the collection's maximum is enforced in code and small — one page, one request's items, one
batch — and the whole operation needs random access to it. Streaming a bounded page adds a state machine that buys
nothing.

**Stream** when any of these holds:

- the element count is a growing dimension per `20-finding-n.md`;
- the elements are produced faster than they are consumed and the consumer can apply backpressure;
- the operation's output is itself a stream — a file download, an export, a bulk response;
- the elements are large enough that a bounded count still produces unbounded bytes, which is the case for anything
  carrying uploaded content or free text with no length limit.

**The deciding question is not "how many elements" but "how many bytes at once, at the largest input the system
permits".** A bounded row count multiplied by an unbounded row size is unbounded memory, and a length limit on the
largest field is the boundary that fixes it.

## What breaks streaming

A stream that accumulates is a materialisation with extra steps. These are the accumulations that appear in
otherwise-correct streaming code, each defeating the purpose:

- collecting results into a list to return at the end, rather than writing each to the output as it is produced;
- building a deduplication set, an aggregate map, or a seen-keys set across the whole stream — bounded only by the
  distinct-key count, which is usually the dimension being streamed over;
- accumulating errors to report at the end, which grows with the failure count in the worst case;
- holding an open transaction across the whole stream, which pins database resources for the stream's whole duration
  and is a pool and lock problem rather than a memory one;
- logging one record per element at a level that is enabled in production, which converts a memory bound into a log
  volume bound;
- a buffered writer whose buffer is never flushed until completion.

When an aggregate genuinely must be computed across the whole stream, state its own bound in its own dimension —
distinct keys, not rows — and bound that dimension. An unbounded aggregate is the memory defect the streaming was
meant to remove.

## What a chunked operation owes its caller

1. **A stated chunk size** with a default, a validated range, and one sentence on the trade it makes: larger chunks
   mean fewer round trips and more memory per chunk. The configurability rules are in `60-tuning-points.md`.
2. **Deterministic ordering across chunks**, so no record is skipped or repeated between chunks. Ordering by a
   non-unique column produces both when rows tie at a chunk boundary; order by something unique, or by the
   pagination mechanism `/alaa-data-layer` (`$alaa-data-layer`) prescribes.
3. **Stable behaviour when the underlying data changes mid-run**, stated explicitly: a long export runs while rows
   are inserted and deleted, so say whether the output is a snapshot, is best-effort, or is guaranteed to include
   every row present at the start.
4. **Resumability, or an explicit statement that it has none.** A chunked operation that fails at chunk nine hundred
   and restarts from chunk one will never finish on a large input. Resumability means recording the last completed
   position durably, and it makes re-processing a chunk possible, so the per-chunk work is idempotent —
   `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns that contract.
5. **Progress that an operator can observe**, so a run that has stalled is distinguishable from a run that is slow.
   The signal itself belongs to `/alaa-observability-soc` (`$alaa-observability-soc`).

## Allocation inside the loop

Two rules, and no more, because per-language allocation behaviour belongs to `/golang-performance`
(`$golang-performance`) and the per-language clean-code skills:

- **Allocate once outside the loop what is reused inside it**, when the loop is over a growing dimension and the
  allocation is proportional to element size. Below that threshold this trade buys nothing and costs readability.
- **Preallocate a collection whose final size is known before it is filled**, because growing it repeatedly copies
  what is already there. When the size is not known, do not guess one.

Both are conditional on the trigger test in `SKILL.md` having fired. Applying them to a bounded, small loop is the
premature optimisation `80-when-not-to.md` refuses.

## Anti-patterns

- reading a whole result set to compute a count, a sum, or a maximum the store can compute;
- an export implemented as fetch-all-then-format;
- a stream whose results are collected into a list and returned;
- a chunk size hardcoded inside the loop that uses it;
- chunked pagination ordered by a non-unique column;
- a long-running chunked job holding one transaction open for its whole duration;
- unbounded memory presented as bounded because the row count is bounded, where row size is not.
