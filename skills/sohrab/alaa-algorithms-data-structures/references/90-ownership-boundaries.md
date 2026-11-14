# Ownership Boundaries

Load when a question belongs to another skill's ground. `SKILL.md` *What this skill does not own* owns the rule that this skill states none of these owners' values. This file names each owner.

| Owner | What it owns |
|---|---|
| `/golang-data-structures` | Go slice, map, container internals; capacity growth; preallocation; copy semantics |
| `/golang-performance` | Go optimisation patterns once a bottleneck is identified |
| `/golang-benchmark` | Go benchmark, `pprof`, `benchstat` mechanics |
| `/golang-concurrency` | Goroutine, channel, synchronisation mechanics |
| `/alaa-php-clean-code`, `/alaa-golang-clean-code-principles`, `/alaa-vue-typescript-clean-code` | Language idiom, design patterns, and each framework's own N+1 fix |
| `/alaa-data-layer` | Query shape, index design, keyset pagination, driver and pool mechanics, cache semantics |
| `/alaa-observability-soc` | Telemetry's quantitative budgets: cardinality ceilings, histogram boundaries, sampling rates |
| `/alaa-services-contract` | Every Ala platform value: deadlines, timeouts, pool maxima, in-flight limits |
| `/alaa-reliability-sla` | Retry, breaker, shedding, degradation, and idempotency doctrine |
| `/alaa-system-design` | Subsystem design: boundaries, dependency table, assumed peak, growth horizon |
| `/alaa-testing-strategy` | Whether a benchmark is evidence, and at which proof level a claim may be reported |
| `/alaa-security-review` | Which cryptographic primitive belongs on which path |
| `/alaa-controlled-ops` | That package's canonical digest specification |
| `/alaa-project-constitution` | The quality bar whose obligation 7 this skill discharges |
| `/alaa-prompting-guide` | Model and effort capability evidence; the runtime orchestrator owns task allocation. Never name a model here |

