# When None Of This Applies

Load when the trigger test in `SKILL.md` did not fire and an optimisation is still being proposed, and when
reviewing code that defends against load its boundary already prevents.

Most code in this estate operates on bounded, small inputs and needs no budget, no measurement, and no structure
beyond the obvious one. This file is the counterweight, and it carries the same authority as every rule in
`SKILL.md`: a skill that only pushes toward budgets and structures produces unreadable code defending against load
that never arrives, and that is a real defect with a real cost, not a lesser one.

## The rule, restated as a refusal

**When no input dimension on the path is unbounded, no per-element work leaves the process, and no dimension grows
with tenants, history, catalogue, fan-out, or time, the path is finished when it is clear.** State no budget, run no
benchmark, choose no structure other than the obvious one, and do not stream what already fits.

The trigger test is a gate in both directions. It licenses the work when it fires, and it refuses the work when it
does not, and the refusal is the half that gets skipped.

## Why the refusal is a rule and not a preference

Three costs, all of which are paid on every future change and none of which appear in a benchmark:

- **A reader must reconstruct the reason.** A map where a list would read plainly, a hand-rolled loop where a
  library call would say what it means, an index built for one lookup — each makes the next reader ask what problem
  it solves, and the answer is usually none.
- **Uniformity is lost.** The estate's own standing preference is that all services look alike, because
  inconsistency across services costs more than any local cleverness saves. An optimised path that no other service
  matches is a path only its author can review.
- **The complexity hides the real defect.** A path already carrying an unjustified optimisation is where a genuine
  complexity defect goes unnoticed, because everything on it already looks deliberate.

## The observable separation

Two questions decide it, and both are answered from the code rather than from judgment:

1. **Does the dimension have a maximum enforced in code that a reader can name?** Yes for a validated request array,
   a page cap, a fixed enum, a configuration list, a fixed set of channels or statuses. No for anything that grows
   with rows, tenants, time, or a caller's input with no validation rule.
2. **Does the per-element work leave the process?** A query, a network call, a cache round trip, a lock, a file. In
   memory only means the answer is no.

Named maximum and in-memory work: write the clearest code. Anything else: `SKILL.md` applies.

## Cases that look like they need a budget and do not

- A loop over a fixed set of statuses, channels, roles, or supported locales.
- A loop over the fields of one request, or the columns of one row.
- A sort of one page of results already bounded by the page cap.
- A membership check against a handful of constants.
- A startup-time computation that runs once per process.
- A path whose per-element work is arithmetic on values already in memory, over a dimension with a named maximum.

In each of these the fastest possible implementation and the clearest one differ by an amount no user can perceive,
and the clearest one wins on every future change.

## The one thing to do anyway

**When the trigger test does not fire because a boundary enforces the maximum, name that boundary in the code.** One
comment — "bounded by the page cap at the route" — or a test asserting the maximum is enough. It costs a line and it
converts an invisible assumption into a checked one, so a later change that removes the boundary has something to
break. This is the only obligation this file imposes on an untriggered path.

## Revisiting

An untriggered path becomes a triggered one when its boundary is removed or raised, when a per-element call is
introduced into its loop, or when the dimension starts growing with something the business grows. The change that
does any of those runs the trigger test again; nothing else does.

Do not schedule a review of untriggered paths. A sweep looking for optimisation opportunities finds them everywhere,
because the question "could this be faster" always has a yes, and it is the wrong question. The right question is
the trigger test, and it is asked when the code changes.

## Anti-patterns

- optimising a path because its name sounds hot, rather than because a dimension on it grows;
- introducing a cache to a path with a named small maximum, adding an invalidation problem to solve nothing;
- replacing a clear library call with a hand-written loop for a gain nobody measured;
- micro-optimising inside a request that spends most of its time waiting on one network call;
- treating a review comment about performance as a requirement without running the trigger test first;
- adding a benchmark for a path whose dimensions all have named maxima, which then has to be maintained forever;
- refusing a genuine budget on this file's authority, when the trigger test did fire.
