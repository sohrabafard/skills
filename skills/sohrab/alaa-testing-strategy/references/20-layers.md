# Layers, And How To Choose One

## The four layers, defined by what they can rule out

A layer is defined by which components are real, not by a directory or a framework feature, because the real components fix the class of failure the layer can produce.

| Layer | Real | Substituted | Rules out |
|---|---|---|---|
| **Unit** | The code under test and every pure collaborator it uses | Everything at the process edge: network, database, broker, filesystem, clock, randomness | A wrong decision, calculation, transformation, validation, state transition, ordering, or boundary |
| **Integration** | This service's code plus one real infrastructure dependency it owns | The other infrastructure dependencies, and every other service | Whatever the driver, schema, query planner, serialiser, index, constraint, or transaction decides |
| **Contract** | The shared artifact — schema, envelope definition, published collection — and one side of the agreement | The other party entirely | A disagreement between what this service sends or accepts and what the other party expects |
| **End-to-end** | Every service and dependency in the crossing under test, deployed as they are deployed | Nothing inside the crossing; external third parties only | A failure in the wiring itself: routing, credential propagation, envelope translation, ordering across a queue, configuration that differs per deployment |

## The placement procedure

1. **Name the failure the test defends against**, from the derivation in `10-what-makes-a-test.md`. A test with no named failure has no layer.
2. **Name the smallest set of components that must be real for that failure to be producible.** Producible means that, if the failure exists in the code, this arrangement shows it. Make real every component whose substitution would hide the failure. Substitute every other component.
3. **Read the layer off that set.** Nothing outside the process: unit. One real infrastructure dependency: integration. Disagreement with another party's expectations: contract. Wiring between deployed services: end-to-end.
4. **Record the layer beside the failure**, so that the next reader can check the placement.

Step 2 decides the layer. Ask "what could hide this failure?", never "what would be more realistic?", because the second question always answers "more real components" and produces an end-to-end suite.

## Where the common behaviours land

| Behaviour | Layer | Why not lower, why not higher |
|---|---|---|
| A validation rule, a calculation, a state machine, a parse or format | Unit | No infrastructure decides it, so a higher layer adds cost and no coverage |
| A query returning the right rows, an index actually being used, a uniqueness constraint holding, an isolation-level behaviour, a migration's effect on existing data | Integration against the real engine | A substituted engine implements the author's belief about the engine, which is exactly the thing in question |
| A queue consumer's acknowledgement, redelivery, and dead-lettering behaviour | Integration against the real broker | The behaviour belongs to the broker's protocol, not to the handler |
| The success and error envelopes this service returns | Contract | An end-to-end test reports a routing failure and an envelope failure identically |
| A double's fidelity to the dependency it replaces | Contract, as a parity suite | See `30-doubles.md` |
| Authentication and authorization at the route boundary | Integration, plus one per enforcing layer beneath it | The layers beneath run when the route boundary is bypassed |
| A user journey crossing three services, where the crossing is the risk | End-to-end | Nothing below it exercises credential propagation and envelope translation together |
| A feature's business rules | Unit, with the journey covered once end-to-end | End-to-end tests of business rules make a suite slow and uninformative |

## The rule against triplication

When the removal discriminator in `SKILL.md` *The core rule* shows one mechanism tested at several layers, keep the test whose layer the placement procedure selects and delete the others. Otherwise every change to the behaviour must be made in each copy, and the copies fail together for one cause. A genuine defence-in-depth control, which the discriminator shows as independent mechanisms, keeps one test per layer.

## Distribution is an output, not a target

The number of tests per layer is whatever the placement procedure produced. Never set a target ratio between layers: like a coverage percentage, it is satisfied by writing tests at the short layer whether or not a behaviour belongs there. When a suite looks wrong-shaped, re-run the placement procedure on its behaviours and let the shape follow.

Two shapes are always defects, because each names a failure the suite cannot produce:

- **No integration layer.** Every database, broker or cache claim is then a claim about a substitute, and no test can produce a schema, index, constraint, planner or delivery failure.
- **An end-to-end suite that carries the business rules.** Each rule then costs a full environment, failures are ambiguous between rule and wiring, and the suite is the first thing skipped under time pressure.

## Suite time budgets

Give each layer a budget, because a suite past its budget runs less often and then not at all, and an unrun test is an absent test.

- The unit suite runs on every save or commit. When it becomes too slow for that, find the test that does I/O at the wrong layer by placement, not by parallelism.
- The integration suite runs on every push or merge request, against real engines started once per run and shared under `90-test-economy.md`.
- The contract suite runs wherever its artifact changes, on both sides of the agreement.
- The end-to-end suite runs on merge to the mainline and before release. It holds only crossings, so the number of crossings, not of features, bounds its size.

This file owns which suites exist and what belongs in each. Before you execute them, read `100-test-execution.md` for scope and collection, and `110-execution-resources.md` for resources.
