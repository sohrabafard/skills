# Layers, And How To Choose One

Read when deciding where a behaviour is tested, when a suite is slow, or when the same behaviour appears to be tested more than once. `SKILL.md` holds the binding rule: each behaviour is verified at exactly one layer, and the removal discriminator settles the defence-in-depth exception.

## The four layers, defined by what they can rule out

A layer is not a directory name and not a framework feature. It is defined by which components are real, because that is what fixes the class of failure the layer can produce.

| Layer | Real | Substituted | Rules out |
|---|---|---|---|
| **Unit** | The code under test and every pure collaborator it uses | Everything at the process edge: network, database, broker, filesystem, clock, randomness | A wrong decision, calculation, transformation, validation, state transition, ordering, or boundary |
| **Integration** | This service's code plus one real infrastructure dependency it owns | The other infrastructure dependencies, and every other service | Whatever the driver, schema, query planner, serialiser, index, constraint, or transaction decides |
| **Contract** | The shared artifact — schema, envelope definition, published collection — and one side of the agreement | The other party entirely | A disagreement between what this service sends or accepts and what the other party expects |
| **End-to-end** | Every service and dependency in the crossing under test, deployed as they are deployed | Nothing inside the crossing; external third parties only | A failure in the wiring itself: routing, credential propagation, envelope translation, ordering across a queue, configuration that differs per deployment |

## The placement procedure

Four steps, and the answer falls out of step 2.

1. **Name the failure the test defends against.** This comes from the derivation in `10-what-makes-a-test.md`; a test with no named failure has no layer because it has no purpose.
2. **Name the smallest set of components that must be real for that failure to be producible.** Producible means: if the failure exists in the code, this arrangement shows it. A component whose substitution would hide the failure must be real; every other component is substituted.
3. **Read the layer off that set.** Nothing outside the process → unit. One real infrastructure dependency → integration. The risk is disagreement with another party's expectations → contract. The risk lives in the wiring between deployed services → end-to-end.
4. **Record the layer beside the failure**, so the next reader can check the placement rather than re-deriving it.

The step that decides everything is 2, and the question that gets it wrong is "what would be more realistic?" — which always answers "more real components" and produces an end-to-end suite. The question that gets it right is "what could hide this failure?"

## Where the common behaviours land

| Behaviour | Layer | Why not lower, why not higher |
|---|---|---|
| A validation rule, a calculation, a state machine, a parse or format | Unit | No infrastructure decides it, so a higher layer adds cost and no coverage |
| A query returning the right rows, an index actually being used, a uniqueness constraint holding, an isolation-level behaviour, a migration's effect on existing data | Integration against the real engine | A substituted engine implements the author's belief about the engine, which is exactly the thing in question |
| A queue consumer's acknowledgement, redelivery, and dead-lettering behaviour | Integration against the real broker | The behaviour under test belongs to the broker's protocol, not to the handler |
| The success and error envelopes this service returns | Contract | An end-to-end test asserts them too, but reports a routing failure and an envelope failure identically |
| A double's fidelity to the dependency it replaces | Contract, as a parity suite | See `30-doubles.md` |
| Authentication and authorization at the route boundary | Integration, plus one per enforcing layer beneath it | The layers beneath are what run when the route boundary is bypassed |
| A user journey crossing three services, where the crossing is the risk | End-to-end | Nothing below it exercises credential propagation and envelope translation together |
| A feature's business rules | Unit, with the journey covered once end-to-end | End-to-end tests of business rules are the standard way a suite becomes slow and uninformative |

## The rule against triplication

**A behaviour verified at three layers buys the confidence once and charges a maintenance obligation three times: every future change to the behaviour must be reflected in three places, and all three tests fail together for the same cause, so the second and third failures carry no information.** Delete two, keeping the one whose layer the placement procedure selects.

The exception is a genuine defence-in-depth control implemented three times, and the discriminator in `SKILL.md` separates the two cases mechanically: remove the mechanism at one layer, run all three tests, and count the failures. One failure means three mechanisms and three tests. Three failures mean one mechanism and one test.

## Distribution is an output, not a target

The number of tests at each layer is whatever the placement procedure produced for the behaviours in the service. A target ratio between layers is the same defect as a coverage percentage: it can be satisfied by writing tests at the layer that is short, regardless of whether any behaviour belonged there. When a suite looks wrong-shaped, re-run the placement procedure on the behaviours and let the shape change as a consequence.

Two shapes that are always defects, because each names a failure the suite cannot produce:

- **No integration layer at all.** Every claim about a database, a broker, or a cache is then a claim about a substitute, and no test in the service can produce a schema, index, constraint, planner, or delivery failure.
- **An end-to-end suite carrying the business rules.** Each rule then costs a full environment to exercise, so the suite is slow, its failures are ambiguous between the rule and the wiring, and it is the first thing skipped under time pressure.

## Suite time budgets

Each layer has a budget, because a suite past its budget is run less often and eventually not at all, and an unrun test is an absent test.

- The unit suite runs on every save or every commit. When it stops being fast enough for that, the cause is almost always a test doing I/O at the wrong layer — find it by placement, not by parallelism.
- The integration suite runs on every push or merge request, against real engines started for the run.
- The contract suite runs wherever its artifact changes, on both sides of the agreement.
- The end-to-end suite runs on merge to the mainline and before release, and it holds only crossings, so its size stays bounded by the number of crossings rather than by the number of features.

`/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) owns how these commands are executed and under what resource policy; this file owns which suite exists and what belongs in it.
