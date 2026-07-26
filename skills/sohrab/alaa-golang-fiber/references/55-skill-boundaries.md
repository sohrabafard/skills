# Skill Boundaries

Read this file when a question in front of you may belong to another skill.

This skill owns one thing: how Fiber v3 behaves, and what a Fiber service on this platform must do
about it. Everything below is owned elsewhere. When the triggering condition in the left column is
true, load the owning skill and follow it. Do not answer from this skill, and do not restate the
owner's rules here in weaker language - a second statement of a rule is a second rule, and the two
drift.

## The boundaries

| You are about to | Owner |
| --- | --- |
| Decide whether a service uses chi or Fiber, or justify an existing choice | `alaa-golang` `references/30-http-api-framework-choice.md` - `/alaa-golang`, `$alaa-golang` |
| Ask any general Go question: package layout, interface design, error mechanics, concurrency primitives, naming, lint, refactoring, dependency or toolchain work | `/alaa-golang` (`$alaa-golang`), which routes to the specific public Go skill |
| Apply or check the P1-P13 clean-code discipline on Ala Go code | `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) |
| Set a retry policy, a backoff curve, a timeout budget, a degradation posture, or an SLO error budget | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Write any concrete name or value: header names, env keys, error codes, metric names, envelope fields, timeout durations, body caps, probe paths | `/alaa-services-contract` (`$alaa-services-contract`) |
| Decide what to test at which layer, how to build fixtures, or what coverage is sufficient | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Design an authorization model, a tenancy boundary, or a fail-closed rule; or grant an exception to one | `/alaa-security-review` (`$alaa-security-review`) |
| Decide whether a signal is required, recommended or optional; or set metric naming, cardinality budgets, alert rules, or SOC routing | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Choose a PostgreSQL or Redis client, size a connection pool, design a cache topology, or write a migration | `/alaa-data-layer` (`$alaa-data-layer`) |
| Interpret a trusted gateway header, use or shape `TrustCtx`, or reason about gateway proof | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Touch anything kit-governed: a change request, the consumer registry, the phase gate, propagation to consumers, or the kit's own contracts | `/alaa-go-chi-development` (`$alaa-go-chi-development`) |
| Ask which model to use, what reasoning effort to set, how to write a delegation prompt, or what a runtime is capable of | `/alaa-prompting-guide` (`$alaa-prompting-guide`) |

## Why this file exists

The previous version of this skill named three of these eleven owners. That is why it had grown its
own framework-choice criteria, its own data-layer defaults, its own retry guidance and its own
observability requirement levels - each one a weaker restatement of a rule that already had an
owner, and each one a place where an agent reading this skill would reach a different answer than an
agent reading the owner.

A boundary is only useful if it names the observable condition that triggers it, which is why the
left column describes what you are doing rather than what the topic is called. "Security" is not a
triggering condition; "you are about to grant an exception to a fail-closed rule" is.

## The one thing to check before writing Fiber code at all

A new Ala service is an `alaa-go-chi` kit consumer on chi. Fiber for such a service is the project
owner's recorded decision, made through `/alaa-go-chi-development`
(`$alaa-go-chi-development`). If you cannot point at that record, you are not authorized to start;
say so and stop. The full statement of this, with the consumer registry evidence, is in `SKILL.md`.
