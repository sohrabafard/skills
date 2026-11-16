# Layers, And How To Choose One

## The four layers, defined by what they can rule out

The real components define a layer, never a directory or a framework feature.

| Layer | Real | Substituted | Rules out |
|---|---|---|---|
| **Unit** | The code under test and its pure collaborators | Everything at the process edge: network, database, broker, filesystem, clock, randomness | A wrong decision, calculation, transformation, validation, state transition, ordering or boundary |
| **Integration** | This service's code and one real infrastructure dependency it owns | The other infrastructure dependencies, and every other service | What the driver, schema, query planner, serialiser, index, constraint or transaction decides |
| **Contract** | The shared artifact (schema, envelope definition, published collection) and one side of the agreement | The other party | A disagreement between what this service sends or accepts and what the other party expects |
| **End-to-end** | Every service and dependency in the crossing under test, deployed as in production | External third parties only | A wiring failure: routing, credential propagation, envelope translation, ordering across a queue, per-deployment configuration |

## The placement procedure

1. **Name the failure the test defends against** (`10-what-makes-a-test.md`). A test with no named failure has no layer.
2. **Name the smallest set of components that must be real for that failure to be producible**: if the failure exists in the code, this arrangement shows it. Make real every component whose substitution would hide the failure, and substitute every other one.
3. **Read the layer off that set.** Nothing outside the process: unit. One real infrastructure dependency: integration. A disagreement with another party's expectations: contract. Wiring between deployed services: end-to-end.
4. **Record the layer beside the failure.**

Step 2 decides the layer. Ask "what could hide this failure?", never "what would be more realistic?": the second question always produces an end-to-end suite.

## Where the common behaviours land

| Behaviour | Layer | Why this layer |
|---|---|---|
| A validation rule, a calculation, a state machine, a parse or a format | Unit | No infrastructure decides it |
| A query's rows, an index in use, a uniqueness constraint, an isolation-level behaviour, a migration's effect on existing data | Integration against the real engine | A substituted engine implements the author's belief about the engine |
| A queue consumer's acknowledgement, redelivery and dead-lettering | Integration against the real broker | The broker's protocol owns the behaviour |
| The success and error envelopes this service returns | Contract | An end-to-end test cannot tell a routing failure from an envelope failure |
| Authentication and authorization at the route boundary | Integration, plus one test per enforcing layer beneath it | The layers beneath run when the route boundary is bypassed |
| A user journey that crosses three services, where the crossing is the risk | End-to-end | Nothing lower exercises credential propagation and envelope translation together |
| A feature's business rules | Unit, with the journey covered once end-to-end | An end-to-end test of a rule is slow, and its failure is ambiguous between rule and wiring |

## The rule against triplication

When the removal discriminator in `SKILL.md` *The core rule* shows one mechanism tested at several layers, keep the test whose layer the placement procedure selects, and delete the others. A defence-in-depth control, which the discriminator shows as independent mechanisms, keeps one test per layer.

## Distribution is an output, not a target

Never set a target ratio between layers: tests written at the cheap layer satisfy it, whether or not the behaviour belongs there. When a suite looks wrong-shaped, re-run the placement procedure on its behaviours.

Two shapes are always defects: a suite with no integration layer, which cannot produce a schema, index, constraint, planner or delivery failure; and an end-to-end suite that carries the business rules.

## Suite time budgets

Give each layer a time budget: a suite past its budget runs less often, and an unrun test is an absent test.

- **Unit**: every save or commit. When it is too slow for that, find by placement the test that does I/O at the wrong layer; do not add parallelism.
- **Integration**: every push or merge request, against real engines started once per run and shared (`90-test-economy.md`).
- **Contract**: wherever its artifact changes, on both sides of the agreement.
- **End-to-end**: on merge to the mainline and before release. It holds crossings only, so the number of crossings bounds its size.
