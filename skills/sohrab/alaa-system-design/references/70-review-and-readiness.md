# Review And Readiness

`SKILL.md` owns the rule that a design is reviewed before any implementation lane is dispatched, and the
stop conditions. This file is what the reviewer checks, how findings are classified, and what the
implementation lane may decide on its own once the record is reviewed. Read it when reviewing a record and
when handing one over.

Under `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) this review runs as the
`alaa-architecture-critic` role, which is already gated on contract, boundary, consistency, concurrency,
and caching changes. That role owns its verdict vocabulary and its output contract; this file supplies the
standard it reviews against. A human reviewer applies the same checks and reaches the same verdicts, and a
record reviewed by neither is a draft.

## What the reviewer checks

One check per procedure step, in order. Each is answered from the record itself — a check answered from the
reviewer's memory of a conversation is not answered, because the next reader will not have been in it.

| Step | The check |
|---|---|
| 1 | The trigger condition that fired is named, and the record states an outcome rather than a task |
| 2 | The inside/outside list separates changeable components from dependencies with owners; the seam is stated with all three boundary test results; the extend-or-create decision names which conditions were met and the evidence for each |
| 3 | Every interface kind is enumerated or explicitly marked none; every field crossing an interface has type, optionality, unit where it is a quantity, and identifier kind where it identifies; every dependency failure maps to exactly one caller-visible outcome; every changed interface states per consumer whether that consumer must change |
| 4 | Every datum has exactly one writer; every reader's access mode is one of the four permitted values; each critical journey's read and write paths carry a staleness column; each interaction's consistency model is chosen by the stated question; every second copy is labelled cache or fork with what that label obliges |
| 5 | Every dependency from all six derivation sources appears; every row carries classification, caller-visible failure, assumed load, and the source of its bounds; the assumed peak, the growth horizon, and the first resource to saturate are stated |
| 6 | At least two distinct candidates; the winner names the axis it won on and the axis it lost on; every rejection carries its axis and an observable reviving condition |
| 7 | The ship order, the mixed-version behaviour, the reversal, and any point of irreversibility are stated |
| all | Every "not applicable" carries its reason and evidence; no value owned by another skill is restated rather than cited |

## Blocking and non-blocking

**A finding blocks when the thing it names cannot be changed later without changing a consumer, a stored
shape, or a data owner.** That is the whole test, and it is deliberately narrow so that two reviewers block
on the same things.

Blocking, therefore: an interface shape, an error surface with an unmapped dependency failure, a data
owner, a consistency choice, a cache-or-fork label, an unclassified dependency, a missing second candidate,
an irreversible step with no stated reversal, and any "we will decide during implementation" applied to one
of these.

Non-blocking: naming, internal structure, the choice of construct or library, the order of implementation
lanes, and the record's prose. Report them as notes; they are fixed in the implementation lane and do not
hold the design.

**Blocking findings are resolved in the record, not in the implementation.** A finding closed by "the
implementer will handle it" has been moved to a place the reviewer cannot see and the next reader will not
find.

## What the reviewer must not do

- Redesign. The reviewer names what is undecided or wrong and what evidence would settle it; producing a
  competing design makes the reviewer the author and removes the review.
- Approve on style. A well-written decorative record — see `60-design-record.md` — fails; a terse record
  that decides everything passes.
- Accept a decision with no reason. A decision without its reason is rationalised away the first time it is
  inconvenient, which is a defect in the record rather than a matter of taste.
- Block on preference. A different but equally sound design is not a finding; it is a candidate, and if it
  is a real one it belongs in step 6 with its axis.

## Ready to build

A design is ready when all three hold: every check above has an answer in the record; every blocking finding
is resolved in the record; and no open question would change an interface shape, a data owner, or a
consistency choice.

An open question that would change none of those three does not block — record it with the decision it
defers and the point at which it must be answered. **The split matters because a design that waits for every
question to be answered ships nothing, and a design that starts with an interface shape unanswered ships the
first implementer's guess as the contract.**

## Handing over to implementation

The implementation lane receives the reviewed record, the contract files it points at, and the dependency
table. Within that, it decides on its own: internal structure and module layout, algorithms and data
structures inside the stated complexity and load budget, naming inside the component, test structure, and
the constructs that enforce the mechanism classes the record named.

It escalates back to a design change — not a code decision — when it finds that any of these must change:
an interface shape, an error outcome, a data owner, a consistency model, a cache-or-fork label, a dependency
classification, or the boundary itself. Escalating updates the record and re-runs the affected checks; it
does not create a second design in the pull request. **This split is what keeps a fleet's services
recognisable to each other: the decisions that cross components live in reviewed records, and the decisions
inside a component live in the code where they belong.**
