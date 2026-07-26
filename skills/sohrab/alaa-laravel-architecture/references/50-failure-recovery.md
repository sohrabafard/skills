# Failure classes this architecture creates, and the smallest action that fixes each

These four failures are produced by the layer map itself: each one is what a specific boundary violation looks like once it is running in production. Each entry is **symptom** (what an operator sees), **diagnosis** (the command that confirms it), **smallest retry** (the least-blast-radius action that restores correct behaviour), **escalation** (who owns the next step when the smallest action does not hold).

Proof-strength vocabulary for any of these actions is `/alaa-controlled-ops`' (`$alaa-controlled-ops`); values for any retry or timeout are in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.

## 1. Stale reads behind a bypassed decorator

**Symptom.** A read endpoint returns a value a write endpoint changed minutes ago. It corrects itself after the TTL, and it does not reproduce on a machine with the cache cleared. Different endpoints for the same entity disagree with each other.

**Diagnosis.** The cache is not the fault; a write path that does not pass through the decorated interface is. Confirm the bypass, not the staleness:

```sh
sh scripts/architecture-gate.sh --app-dir app        # L1 and L3 findings name the bypassing call sites
```

A single `L3-repository-bypass` finding on a domain whose decorator is bound is sufficient: that write cannot invalidate, so every key it should have invalidated is stale until it expires.

**Smallest retry.** Turn the decorator off for that domain by flipping its enable key (`references/70-config-contract.md`) and deploying config only — the binding falls back to the store implementation and every read becomes correct immediately. Do not start by flushing the cache: a flush restores correctness for one TTL and hides the bypass, so the same incident returns with a different key.

**Escalation.** Route the bypassing call site behind the interface, re-run the gate to exit 0, then re-enable. The completeness test the domain must pass before the flag goes back on is `alaa-data-layer references/50-redis-laravel-octane.md`, "Step 0". Key design and invalidation strategy: `/alaa-data-layer` (`$alaa-data-layer`).

## 2. An outbox row stuck in the claimed state

**Symptom.** Consumers stop seeing a class of event while the writing endpoint keeps returning success. Outbox depth and the age of the oldest row climb; publish counters do not — the surfaces in `references/60-telemetry-surfaces.md`. One row, or a batch, sits in the claimed state (`processing` in repositories that use that spelling; the state set is `/alaa-async-messaging`'s — `$alaa-async-messaging`) with no worker holding it, because the worker that claimed it died between claim and acknowledgement.

**Diagnosis.** Distinguish a stuck row from a slow publisher before touching anything: a claimed row whose age exceeds the publisher's own claim lifetime, with no live worker, is stuck; a growing depth with rising publish counters is a throughput problem and belongs to `/alaa-async-messaging` (`$alaa-async-messaging`). Confirm no live worker holds the row before treating it as orphaned — releasing a row a running worker still holds publishes it twice.

**Smallest retry.** Return the orphaned rows to the claimable state so the normal publisher picks them up on its next pass. Nothing is republished by hand, and no row is deleted: consumers are required to tolerate at-least-once delivery, so a redelivery is safe and a deleted row is a lost event that nothing will ever detect.

**Escalation.** A recurrence means the claim lifetime is shorter than a publish attempt, or the claim is not lock-protected as `references/30-events-and-outbox-seam.md` requires. The claim mechanism's semantics are `/alaa-data-layer`'s; its lifetime and retry values are the contract file's; the consumer's idempotency obligation is `/alaa-reliability-sla`'s (`$alaa-reliability-sla`).

## 3. A worker will not boot while a dependency is down

**Symptom.** The service is entirely unavailable rather than degraded. Workers restart in a loop and no request is answered, including the operational routes. The application logs show the failure during bootstrap rather than during a request. Restarting does not help; stopping the dependency reproduces it exactly.

**Diagnosis.** A provider is performing I/O. Name it mechanically before reading any code:

```sh
sh scripts/architecture-gate.sh --app-dir app        # L4 and L5 findings name the provider and line
```

Then reproduce deliberately: stop Redis and the database, start the workers, issue one request. That is the compliance observable in `references/20-composition-and-boot.md`, and it is the same test that proves the fix.

**Smallest retry.** Restore the dependency to stop the outage, then move the offending read out of the provider in the next deploy — to first use inside the consuming class, with the declared default and the fallback signal. Do not "fix" it by wrapping the provider's read in a `catch` that returns a default silently: that converts a total outage into a service answering from an unstated default, with nothing in telemetry saying so, which is harder to diagnose than the crash-loop was.

**Escalation.** Worker lifecycle, reload, and anything the worker retains between requests: `/alaa-octane-performance` (`$alaa-octane-performance`). Whether the dependency belongs in readiness at all: `references/40-degraded-mode.md`.

## 4. Envelope drift between endpoints

**Symptom.** A client's error handling works against one endpoint and breaks against another in the same service: a key is absent, `status` disagrees with the HTTP status line, or a validation failure comes back in the framework's default shape while a domain failure comes back in the contract's. Typically reported by a consumer team, not by any test in this repository.

**Diagnosis.** Count producers, not endpoints. More than one place assembling an error body is the defect:

```sh
grep -rn "response()->json" app/Http/Controllers | grep -iE "error|message|code"
grep -rln "render\(" app/Exceptions
```

Then check saved examples against the contract's own compliance observable — the `jq` assertion in `alaa-services-contract references/10-core-service-contract.md` — over every `4xx` and `5xx` example in the repository's tests and API collection. A repository with no `4xx` and no `5xx` saved example has not proven the envelope at all.

**Smallest retry.** Route the divergent endpoints through the single handler by making their Services throw the typed domain exception, and delete the hand-assembled bodies. This is a behaviour change to a public surface: it is not a silent cleanup inside a feature branch.

**Escalation.** Changing a shape a client already consumes runs through the deprecation procedure in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`, which owns the window. Code and key names are `/alaa-services-contract`'s (`$alaa-services-contract`). A test that would have caught this belongs at the layer `/alaa-testing-strategy` (`$alaa-testing-strategy`) names.
