# Boundary And Seam

`SKILL.md` owns the six trigger conditions and the extend-by-default rule. This file says what evidence
settles each of that rule's five conditions, how to find the seam, how to test whether a proposed
boundary is real, and when two services should be merged back. Read it during step 2.

## Build the inside/outside list before drawing anything

1. List the journeys the design touches, from the constitution's critical-journey list or from the
   request.
2. For each journey, list every component it passes through, including the ones the platform inserts —
   gateway, auth, authorization, broker, datastore.
3. Mark each component `changeable-in-this-release` or not, applying the inside/outside rule in `SKILL.md`.
4. Every component marked not changeable becomes a dependency row carrying its owner and the contract you
   consume from it.

A component you want to change but cannot is the most valuable line in this list, because it is where the
design's cost actually sits. Name it, name its owner, and decide whether this design proceeds without that
change or waits for it — recording "we assumed they would change it" is how two teams each wait for the
other. When the plan requires an edit inside a dependency, that is either a second design or a contract
change: split it and name which, because a plan that quietly edits a dependency has no owner on either
side of the seam.

## Finding the seam

The seam is where the writer of the data changes. Find it mechanically rather than by intuition, so that
two agents given the same journeys find the same seam:

1. List every noun the journeys read or write — the entities, the state, the counters, the documents.
2. For each noun, name the single component that writes it today, or that would write it under this design.
3. Group the nouns by writer. Each group is a candidate component.
4. Walk each journey across the groups. Every point where the journey crosses from one group to another is a
   candidate seam.
5. For each candidate seam, ask whether the journey must be atomic across it. A seam that cuts through a
   set of writes that must all happen or none happen is in the wrong place: either move it so the atomic
   writes fall on one side, or accept a distributed workflow and design its compensation explicitly in
   step 4. There is no third option, and choosing neither means the system will take the failure path
   without a compensator.

## Is a proposed boundary real?

Apply all three tests and record the results. A boundary that fails the data test or the change test is a
module inside an existing component, whatever the diagram says.

| Test | Passes when | Fails when |
|---|---|---|
| **Data** | The candidate owns state that no component outside it writes directly | Every write it performs lands in state another component also writes, so the boundary runs through a shared write path and there is no owner to ask when the values disagree |
| **Change** | There is a plausible change to the candidate's internals that requires no coordinated change in any caller | Every realistic change is a lockstep change across the boundary, so the boundary adds a network hop and a deployment order without buying independence |
| **Failure** | The design states, per caller, what happens when the candidate is unavailable, and at least one caller has an answer other than "it is unavailable too" | Every caller's answer is "it is unavailable too", which means the boundary buys no isolation; that is permitted, but only when the data test and one other extend-or-create condition carry it, and the record says so |

## What settles each extend-or-create condition

The conditions are in `SKILL.md`. A condition counts only when evidence settles it; a condition argued
from intuition counts as not met, because intuition is exactly the input that makes two agents disagree.

| Condition | Settled by | Not settled by |
|---|---|---|
| Different data owner | The write list from the seam procedure, showing state no existing service writes | "It is a different domain", or a different noun in the name |
| Different failure domain | A named journey with a stated requirement to keep completing while the other side is down | "Isolation is good", or a general preference for smaller blast radius |
| Different scaling axis | Two load drivers that move independently, with the observed or projected ratio stated | "It might get big one day" with no driver named |
| Different trust or compliance boundary | A named datum, credential, or regulated class the host service may not hold, with the rule that forbids it — ask `/alaa-security-review` (`$alaa-security-review`) whether it is forbidden rather than assuming | "It handles sensitive data", where the host service already handles data of the same class |
| Different runtime or lifecycle | A named runtime, library, or release cadence the host cannot adopt without changing its own | A preference for a language or framework the team enjoys |

## Boundaries that look real and are not

- **The noun boundary.** A service per entity — user service, order service, comment service — drawn from
  the domain vocabulary rather than from the write list. It fails the data test as soon as two of them
  write the same row, which happens on the first feature that spans them.
- **The team boundary frozen in code.** A boundary drawn around who works on it today survives one
  reorganisation and then owns nothing. Draw on data and change; record the team as the owner of the
  contract, not as the reason for it.
- **The library boundary.** A service created to isolate a dependency, an SDK, or a runtime that could be
  isolated by a module and an interface. It buys the same isolation and costs a deployment unit.
- **The performance boundary with no measurement.** A service split out to "scale independently" with no
  stated load driver. The scaling axis condition exists to make this claim checkable.

## Merging two services back

The reverse decision uses the same evidence. Merge when all of these hold: they are always deployed
together; every change to one has required a change to the other over the last several changes; no journey
survives one being down without the other; and they write the same data. Merging removes a contract a
consumer can observe, so it runs through the deprecation procedure in `/alaa-services-contract`
(`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md` — a merge is a
contract change, not a refactor, and treating it as a refactor is how a consumer discovers it in
production.

## What the record carries out of step 2

The Scope section names: the components inside; the dependencies with their owners and the contract
consumed from each; the seam and the result of all three boundary tests; and the extend-or-create decision
naming which conditions were met and with what evidence. A Scope section that lists components without the
test results is a diagram, and a diagram cannot be disagreed with.
