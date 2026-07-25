# Topic Map

Read this when the task touches more than one mechanism and the routing is not obvious. It routes only; every rule lives in the file named beside it, and the always-binding rules live in `SKILL.md`.

## By what the task is doing

| The task | Read |
|---|---|
| Adds or changes an outbound call of any kind | `10-deadlines-and-timeouts.md`, then `30-breakers-and-bulkheads.md` for the isolation slot |
| Adds, removes, or tunes a retry | `20-retries.md`, and `60-idempotency.md` before declaring the retry legal |
| Adds an end-to-end latency target, or splits one across hops | `10-deadlines-and-timeouts.md` |
| Adds a circuit breaker, or one dependency is exhausting a shared pool | `30-breakers-and-bulkheads.md` |
| Adds a queue, an in-flight limit, a rate limit, or a shed decision | `40-admission-and-shedding.md` |
| Makes a response partial, adds a fallback, or uses a cache to survive an outage | `50-degradation.md` |
| Adds a state-changing route a caller may repeat, or designs a key store | `60-idempotency.md` |
| Defines or challenges an SLI, SLO, error budget, or release gate | `70-error-budgets-and-slos.md` |
| Is about to be called done, or must decide what evidence a review accepts | `80-verification.md` |

## By symptom, when diagnosing

| Symptom | Most likely mechanism | Read |
|---|---|---|
| A request exceeded its target while every hop stayed inside its own timeout | No propagated deadline; the hops summed | `10-deadlines-and-timeouts.md` |
| One dependency's incident made every route on the service fail | No per-dependency isolation; the shared pool drained | `30-breakers-and-bulkheads.md` |
| A dependency's load rose during its own outage | Retry amplification, or an unbounded half-open probe | `20-retries.md`, `30-breakers-and-bulkheads.md` |
| Latency grew without bound but almost nothing errored | Work was queued where it shedding was required | `40-admission-and-shedding.md` |
| The service was removed from rotation while it was merely busy | A shed or blocked readiness path | `40-admission-and-shedding.md` |
| A duplicate record appeared under load and not in testing | Two concurrent requests carrying the same key | `60-idempotency.md` |
| Clients cached a partial answer as if it were complete | An unmarked degraded response | `50-degradation.md` |
| A stale value was served through an outage of the system that owns the truth | A cache absorbing the wrong outage | `50-degradation.md` |
| An alert fired only after the month's budget was already gone | A static threshold where a burn rate belonged | `70-error-budgets-and-slos.md` |
| The mechanism was in the code and did not run | It was never exercised | `80-verification.md` |

## Where the values are

No file in this skill states an Ala timeout, retry count, pool bound, acquire wait, shed threshold, response code, or event name. All of those are in `/alaa-services-contract` (`$alaa-services-contract` in Codex), `references/22-failure-load-and-deprecation-contract.md`. When a rule here needs a number, read that file for it.
