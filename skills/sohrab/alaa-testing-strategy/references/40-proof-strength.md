# Proof Strength

Use each level name with exactly the meaning below, in every service, language and report.

## The six levels

The order is by what a level can rule out.

1. **Static proof**: inspection only (the code, the configuration, the types, a linter, a schema validation). It proves that an artifact says something, and nothing about behaviour.
2. **Unit or in-memory proof**: the behaviour executed in process against in-memory or embedded substitutes, such as an embedded database, an in-memory broker or a controllable clock. It proves the logic, and nothing that the substituted engine decides.
3. **Parity proof**: one suite run against the double and the real implementation, with identical results required. It proves that the double is honest, and nothing else.
4. **Local smoke proof**: the built artifact started in its real container or process form and exercised from outside over its real interface. It proves that the artifact boots, wires and answers.
5. **In-runtime service proof**: the service running inside the composed local runtime with its declared dependencies present, exercised through its real transport. It proves the behaviour in its deployed shape.
6. **Live-dependency proof**: the behaviour exercised against the real production-grade dependency engine, with real drivers, transactions, ordering and delivery. It proves what only that engine decides.

## The mapping: which level a claim requires

Each level named is the **minimum**. A higher level satisfies it; a lower one never does.

| The claim | Minimum level |
|---|---|
| "The code follows the convention" / "the configuration declares this value" | 1 |
| "This type or schema rejects that shape" | 1 |
| "This decision, calculation, validation, state transition, parse or format is correct" | 2 |
| "This caller behaves correctly when its dependency times out, refuses or answers wrongly" | 2, with the fault injected at the boundary |
| "This double behaves like the real implementation" | 3 |
| "The service starts, wires its dependencies and serves its interface" | 4 |
| "This configuration value reaches the component that reads it" | 4 |
| "This route, consumer or job behaves correctly in the shape it is deployed in" | 5 |
| "This retry, timeout, breaker, bulkhead, shed, degradation or idempotency mechanism fired" | 5, with injection at the boundary the mechanism guards |
| "Credential issue, verification, refresh and revocation behave correctly" | 5, and 6 wherever a datastore holds the revocation or the key state |
| "This query returns the right rows at the right cost" | 6 |
| "This index is used" / "this constraint holds" / "this migration is safe on existing data" | 6 |
| "This isolation level, lock or transaction boundary behaves correctly under concurrency" | 6 |
| "This delivery, acknowledgement, redelivery, ordering or dead-letter behaviour is correct" | 6 |
| "This control cannot be bypassed" | 6 wherever the datastore enforces it (a row-level policy, a unique constraint, a tenant filter); 2 only where the control is entirely in process. `/alaa-security-review` owns which controls exist and what each must refuse |
| "Latency, throughput, pool or contention behaviour is acceptable" | 6, under load |

Two claims have no level: "this is fast enough" with no stated budget, and "this is secure". Convert each into a claim from the table, or record it as an unmade decision.

## The escalation rule

**Escalate the level when the substituted component decides the outcome.**

- An embedded database proves the calling logic. A claim about the production engine's planner, constraints, isolation semantics or type coercion needs level 6.
- An in-memory broker proves the handler logic. A claim about acknowledgement, redelivery, prefetch or ordering needs level 6.
- A stubbed HTTP client proves the caller's handling. A claim about the real endpoint's shape needs level 3 against the published schema, or level 5 against the real service.

## The prohibition, and what to report instead

**Never describe a lower level in language that implies a higher one.** Two common errors: "tested against the database" for an embedded substitute, and "verified end to end" for a local smoke run.

When this environment cannot reach the required level, follow `80-evidence-and-reporting.md` *When a test cannot be run at all*: name both levels and the blocker, write the test at the required level anyway, and record the gap.

## Where the runtimes come from

Levels 4, 5 and 6 need a running local runtime. Obtain it through the render, bootstrap and validate path of `/service-runtime-kit-governance`. Never assemble one per service, because level 5 would then mean something different in each repository.

Level 6 needs the production-grade engine itself. Where the fleet's release gates name the engines and commands, `/alaa-controlled-ops` owns those gate lists.
