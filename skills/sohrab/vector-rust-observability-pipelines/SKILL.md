---
name: vector-rust-observability-pipelines
description: "Production Vector pipelines: topology and per-path delivery contracts, VRL transforms, buffering, end-to-end acknowledgements, backpressure, sink retry and batching, and what the pipeline does when its destination is unreachable. Use when writing or reviewing a Vector config, a VRL program, or a buffer or acknowledgement setting; when a pipeline stalls, drops, duplicates, or exits on its own; when a ClickHouse sink needs batching, retry, or credential handling; when upgrading Vector across a breaking change; and when validating a config before rollout. Do not use it for generic logging advice independent of Vector mechanics, for what a ClickHouse table must be, which belongs to /clickhouse-performance-schema-ops, for how a SigNoz-owned table is queried, which belongs to /alaa-signoz-clickhouse-docs, or for whether telemetry is required at all, which belongs to /alaa-observability-soc."
---

# Vector observability pipelines

**A log pipeline that drops silently under load is an observability outage that hides
itself.** That is the failure this skill exists to prevent, and why every rule below
is about making loss visible, chosen, and bounded rather than about tidy config.

Pinned to Vector `0.57.0` (`references/80-version-and-upgrade-deltas.md`). Vector
changed interpolation defaults, template confinement and internal metric names within
five releases, so state the version you verified against and re-derive every
version-sensitive claim rather than recalling it: `references/90-source-map.md`.

## Rules

1. **Every path has a written delivery contract before it has a config.** Source,
   transforms, sink, schema in and out, gate or contributor, tolerable outage
   duration, retry ceiling, the metric that proves it healthy, and how it is tested.
   A blank field is a decision nobody has made, and the default will make it.
   `references/10-topology-and-delivery-contract.md`.

2. **Buffering, acknowledgements and `when_full` are never left to the default.**
   Writing no `buffer` block still chooses one: an in-memory buffer of 500 events that
   blocks forever, behind a sink that retries forever. State each value and its reason.
   `references/30-buffers-acks-and-backpressure.md`.

3. **Product telemetry fails open; audit evidence fails closed.** This skill does
   not choose the policy — `/alaa-observability-soc` (`$alaa-observability-soc`)
   already binds the fleet to fail-open for product traffic. This skill states which
   Vector option expresses it: `when_full: drop_newest`, sized for the burst, and
   never `block` on a product path, because `block` turns a destination outage into
   a latency incident on the producing service.

4. **Every fallible VRL call is handled deliberately.** `f(x)` returns an error and
   can be coalesced with `??`; `f!(x)` aborts and cannot; a path lookup never fails,
   so `??` after one is dead code. `??` coalesces errors, not null.
   `references/20-vrl-transforms.md`.

5. **Credentials come from a secret backend, never from `${VAR}` interpolation.**
   Vector 0.57.0 disabled interpolation by default, so a config using
   `${CLICKHOUSE_PASSWORD}` passes validation and then authenticates with that
   literal string. It fails open, silently, exactly where the value is a secret.
   `references/85-security-and-secrets.md`.

6. **Every templated `table`, `database`, object key, file path or header carries a
   literal prefix.** Vector 0.57.0 confines routing templates and rejects unprefixed
   ones at startup. It is the mitigation for injection through a routing field, so
   take the prefix rather than the opt-out.

7. **Validate with `vector validate --skip-healthchecks --deny-warnings`, not with
   `--no-environment`.** That flag suppresses component checks, so an unconfined
   template and an undersized disk buffer both validate clean under it — proven by
   two committed fixtures. Warnings matter too: "acknowledgements are not supported
   by this source" means the durability you configured does not exist.
   `references/50-validation-and-testing.md`.

8. **Unit-test the failure classes, not the happy path.** Absent field, wrong type,
   malformed payload, and the event that must be dropped: a suite that only proves
   the good input works cannot tell a correct transform from a broken one. Pass the
   test file together with the config defining the transform, or it fails as an
   unknown component.

9. **A critical path does not share an acknowledging source with an unreliable one.**
   Fanout acknowledgement uses the worst status, so one failing sink causes
   re-delivery to the sinks that already succeeded. Isolation is a topology decision
   and no sink setting undoes it.

10. **Disk buffers are a capacity dependency of the process.** A full volume makes
    Vector forcefully stop itself, by design, because it can no longer guarantee what
    reached disk. Alert on free bytes on the `data_dir` volume and keep it larger than
    the sum of every configured `max_size`, whose minimum is 268435488 bytes —
    exactly 256 MiB is rejected.

## When NOT to use

- Generic logging or metrics advice that does not depend on Vector topology, VRL,
  buffering, or sink behaviour.
- Deciding what a ClickHouse table must be, whether a signal is required, or what an
  Ala timeout or threshold value is. Those have owners, named below.

## References

Route through `references/00-topic-map.md`: situation to the one file that answers it.

## Checks

```bash
node scripts/check-vector-configs.mjs [--self-test]   # templates, unit tests, red fixtures
node scripts/check-upstream-version.mjs [--self-test] # version drift against upstream
```

Both honour `0` clean, `1` findings, `2` could not run, and both take `--help`. Exit `2`
is not a pass: a gate that cannot tell "Vector is missing" from "nothing is wrong" treats
every broken runner as clean. Detail: `references/50-validation-and-testing.md`.

## Not owned here

The three-way ClickHouse boundary: `clickhouse-performance-schema-ops` owns what a
ClickHouse table must be — engine, sorting key, partitioning, TTL, compression — for
tables the fleet controls. `alaa-signoz-clickhouse-docs` owns how a SigNoz-owned
table is queried, and states that those tables are vendor-owned and read-only to the
fleet. `vector-rust-observability-pipelines` owns what the pipeline writes into a
ClickHouse table and how it behaves when that table is unreachable, and decides no
schema. Route to `/clickhouse-performance-schema-ops`
(`$clickhouse-performance-schema-ops`) and `/alaa-signoz-clickhouse-docs`
(`$alaa-signoz-clickhouse-docs`). Requirement levels and gates are
`/alaa-observability-soc` (`$alaa-observability-soc`); every name and every Ala value
is `/alaa-services-contract` (`$alaa-services-contract`). Every other owner is listed
once in `references/00-topic-map.md`, at the rule it governs.

## Output contract

Every answer using this skill states:

1. the topology, as one line per path
2. the config fragments, with each non-default value's reason
3. the buffer, acknowledgement and `when_full` decision, and which path type it follows
4. the validation and test commands, with their observed exit codes
5. the monitoring plan: the metric, the condition, and where it is shipped
6. the risks, and the rollback
