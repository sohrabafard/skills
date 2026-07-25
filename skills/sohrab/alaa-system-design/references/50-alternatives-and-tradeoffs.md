# Alternatives And Trade-offs

`SKILL.md` owns the rules that at least two distinct candidates exist, that two candidates are distinct
only when they differ on a boundary, a data owner, or a consistency choice, and that each rejection is
recorded with the axis it lost on and the condition that would revive it. This file says where a second
candidate comes from, what the axes are, and how the comparison is written. Read it during step 6.

## Where the second candidate comes from

When only one design is obvious, generate the second from this list in order and take the first that
produces a genuinely different shape. The list is fixed so that two agents reach for the same alternatives
rather than each inventing their own.

1. **Put it inside.** Build the capability as a module in the component that already owns the data, instead
   of as a new component. This is the alternative to every new-service proposal and it is the one the
   extend-by-default rule expects to see beaten explicitly.
2. **Move the owner.** Instead of adding a hop to reach data, move the data's owner to the component that
   reads it most, and let the previous owner become a reader.
3. **Change the interaction mode.** Make a synchronous call asynchronous, or an asynchronous flow
   synchronous. This changes the failure behaviour, the consistency, and the caller's error surface, so it
   is always a distinct candidate rather than a variation.
4. **Do nothing structural.** Extend the existing shape, accept the known cost, and state what that cost is
   and when it becomes unacceptable.

**When no other candidate can be constructed, the do-nothing option is the second candidate, and the record
states what it costs.** A design that beats do-nothing on a stated cost is a stronger record than one that
beats an invented straw candidate, because the straw candidate proves only that the author could imagine a
worse design.

## The comparison axes

Compare every candidate on all six. The axes are fixed so that two records comparing the same candidates
compare them on the same grounds; a record that invents its own axes cannot be read against any other.

| Axis | Measured by |
|---|---|
| **Blast radius** | Which journeys stop working when this part fails, and how many callers see it |
| **Contract cost** | How many consumers must change now, and how many must change at the next foreseeable change |
| **Ownership clarity** | How many components write the same datum, and how many second copies exist |
| **Operational surface** | Deployable units, dependencies, queues, alerts, and runbooks added or removed |
| **Consistency and concurrency risk** | Which of lost update, double effect, out-of-order application, and stale read the candidate must actively prevent |
| **Cost to reverse** | What undoing this costs after six months of accumulated data, and whether it is reversible at all |

Two axes deserve a note because they are the ones a design under time pressure discounts. **Contract cost
compounds**, since every consumer that must change now is a consumer that must be coordinated with at every
future change. **Cost to reverse is asymmetric**: a cheap-to-reverse candidate that turns out wrong costs a
week, and an expensive-to-reverse candidate that turns out wrong costs a migration, so where two candidates
are close on the other axes, the reversible one wins and the record says that is why.

## Decide by naming the axis, not by scoring

Write the winner as one sentence naming the axis it won on and the axis it lost on. **Never compute a
weighted score**, because a weighted score hides the decision inside weights nobody agreed to and produces
a number a reviewer cannot argue with; naming the losing axis is precisely what a reviewer engages with.

A winner that loses on no axis is a sign that the candidates were not distinct. Every real design gives
something up; the record says what.

## Record each rejection as one line

```text
<candidate> — lost on <axis>: <one clause of why> — revisit if <condition>
```

The reviving condition is the load-bearing part. Make it observable: a load figure crossed, a consumer
count reached, a dependency's ownership changed, a compliance rule introduced. **A condition phrased as
"if requirements change" revives nothing**, because nobody can tell whether it has happened; a condition
phrased as a threshold or an event can be checked in one minute when someone proposes the same design
again.

Rejections stay in the record after the design is built. They are the record's second purpose: the first is
telling a reader what was decided, and the second is telling the reader who disagrees what has already been
considered and on what grounds.

## Anti-patterns

- one candidate presented as the design, so the reviewer's only options are approving it or rejecting the
  whole proposal;
- a second candidate that is the winner with different names, different libraries, or a different file
  layout;
- a straw candidate constructed to lose, which converts the comparison into a formality and teaches
  reviewers to skip the section;
- a weighted decision matrix, which relocates the argument into weights and out of the record;
- a rejection recorded without its axis, so a future reader knows the option was considered but not why it
  lost;
- a reviving condition nobody can evaluate, which is the same as no condition;
- deleting rejected candidates once the design is built, which guarantees the debate reopens from zero.
