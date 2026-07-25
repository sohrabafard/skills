# The Design Record

`SKILL.md` owns the record's location, the two-screen budget, and the rule that its section order comes
from `assets/design-record-template.md`. This file says how the record is numbered and superseded, which
counterfactual is answered in which section, what makes a record reviewable rather than decorative, and
what belongs in the record versus in the constitution or the contract files. Read it when creating,
superseding, or judging a record.

## Numbering, location, and multi-repository designs

`NNNN` in the record's path is the next integer in that directory. Numbers are never reused, including for records closed as `not-required`, because
a reused number makes two different decisions share one citation.

When the design spans repositories, exactly one record exists, in the data owner's repository. Every other
affected repository carries a one-line pointer file at the same path — the record's title, its URL, and the
interfaces this repository owns in it. **Two full copies of one record is the failure this rule prevents**,
because the copies are edited in different pull requests and both then claim to be the design.

Where the repository has a docs index whose own contract requires new documents to be registered, add the
one line. Where it does not, do not create an index.

## Which counterfactual is answered where

The counterfactuals raised by `/alaa-project-constitution` (`$alaa-project-constitution`) enter the record
by class, so that the same question always lands in the same section and a reader can find it:

| Counterfactual class | Section |
|---|---|
| Peak load, storage exhaustion, growth | Failure and load — the assumed peak, the horizon, the first resource to saturate |
| Dependency outage, network interruption, expired credentials | Failure and load — the dependency row's classification and caller-visible failure |
| Duplicate delivery, concurrent writes, process restart | Data and consistency — the interleavings ruled out and the mechanism class |
| Stale cache | Data and consistency — the cache-or-fork label with its maximum age and invalidation trigger |
| Partial rollout, rollback | Rollout and reversal — mixed-version behaviour and what a rollback does to data already written |

A counterfactual that lands in no section is either out of scope, which the record states with its evidence,
or a gap in the design.

## Status lifecycle

`draft` → `reviewed` → `built` → `superseded`, plus the terminal `not-required`.

- `draft` — written, not yet reviewed. No implementation lane is dispatched against a draft.
- `reviewed` — a reviewer has applied `70-review-and-readiness.md` and its blocking findings are resolved in
  the record. Implementation may start.
- `built` — the change shipped. Record the commit or release that carries it.
- `superseded` — a later record replaces this decision. Add a link to the successor and change nothing else.
- `not-required` — the design pass produced no decision. Record which trigger condition misfired.

**After `built`, the only permitted edit is adding the link to a superseding record.** The record's value is
being the answer to "why is it like this"; editing it to match what was later built destroys that answer and
leaves a document that agrees with the code and explains nothing.

## Reviewable or decorative

A record is **reviewable** when every section either states a decision a reader could disagree with, or
names why the section does not apply together with the evidence that puts it out of scope.

A record is **decorative** when a reviewer's only available response is approval. Four smells, in the order
they appear:

1. **It restates the request.** The Frame section paraphrases the ticket and adds no outcome the design is
   accountable for.
2. **It describes the current system.** Sections narrate how things work today without stating what changes,
   which is documentation filed as a design.
3. **It lists technologies.** A stack, a library, a broker, a datastore named with no decision attached and
   no alternative considered.
4. **It states decisions without reasons.** Every "we will use X" with no "because Y" is a line the next
   agent will rationalise away the first time X is inconvenient.

An artifact that can only be approved is not a review gate, and a review gate that always passes is a step
everyone learns to skip.

## What belongs where

| Content | Home |
|---|---|
| A decision about this subsystem's shape, boundaries, owners, consistency, dependencies, or rollout | This record |
| A rule every service in the estate owes | `CONSTITUTION.md`, through `/alaa-project-constitution` |
| An exact interface, field, envelope, header, event, or code | The contract files, per `/alaa-services-contract` (`$alaa-services-contract`); the record points at them |
| A timeout, retry, pool, or shed value | `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md`; the record cites it |
| Investigation notes, benchmarks, and discarded reasoning | Outside the record, or compressed into one rejected-candidate line |

## Size discipline

Two screens. When it does not fit, one of three things is true and each has a fix: the design contains a
specification, which moves to the contract files; it contains a discussion, which compresses into
rejected-candidate lines; or it is two designs, which split into two records with two numbers.
