---
name: vector-rust-observability-pipelines
description: >
  Use this skill when the task is about Vector (the Rust-based observability data pipeline), including
  topology design, sources/transforms/sinks, VRL, buffering and backpressure, end-to-end acknowledgements,
  unit testing and validation, internal metrics/logs, sink reliability, ClickHouse sink tuning, and
  production troubleshooting. Do NOT use it for generic logging architecture unrelated to Vector, generic
  Rust programming, or OpenTelemetry Collector-specific tasks unless Vector is explicitly part of the design.
---

# Skill: Vector (Rust-based) observability pipelines

Date: 2026-03-01

This skill is for **production Vector work**:
- designing agent / aggregator / unified topologies
- writing and testing VRL safely
- choosing buffering, acknowledgements, and backpressure behavior deliberately
- tuning sinks, especially ClickHouse
- validating configurations before rollout
- monitoring Vector itself and debugging stalls, loss, duplication, or OOM scenarios

## Core operating principles

1. **Treat Vector as a topology, not a single config blob**
   Start by identifying:
   - deployment role: edge agent, central aggregator, or unified
   - sources
   - transforms
   - sinks
   - delivery guarantees
   - acceptable loss/latency tradeoffs
   - healthcheck, retry, and observability requirements

2. **Buffering and acknowledgements are product decisions**
   Never hand-wave:
   - memory vs disk buffer
   - `when_full = block` vs `drop_newest`
   - whether end-to-end acknowledgements are enabled
   - how multi-sink fanout affects durability and throughput
   - whether a failed experimental sink can slow production flow

3. **VRL is fail-safe**
   - handle fallible operations intentionally
   - use `vector vrl` to iterate on snippets
   - use `vector validate` and `vector test` before rollout
   - keep transformations small, testable, and named

4. **Make Vector observable**
   - wire `internal_logs` and `internal_metrics`
   - define `data_dir` for stateful features like disk buffers and checkpoints
   - decide what "healthy" means for startup and rollout
   - if healthchecks matter at startup, use `--require-healthy`

5. **Treat Helm as part of pipeline correctness**
   - map deployment role to workload shape explicitly:
     - Agent -> DaemonSet
     - Aggregator -> StatefulSet
     - Stateless-Aggregator -> Deployment
   - keep `values.yaml` overrides minimal to reduce upgrade drift
   - if `customConfig` is used, remember it replaces defaults and must be complete
   - when Vector template syntax is embedded in Helm values, escape it intentionally
   - for private registries, define image path and pull secrets explicitly

## Version guardrails (Vector 0.53.0+)

When the task includes an upgrade to 0.53.0 or later, explicitly check for:

- **Internal metrics rename and cardinality changes**
  - `buffer_max_size` -> `buffer_max_size_bytes`
  - `buffer_size` -> `buffer_size_bytes`
  - histogram buckets for `buffer_byte_size` changed from 10 to 26 buckets
  - dashboards/alerts using old metric names must be migrated
- **Component labels in internal metrics**
  - rely on current component labels and avoid assuming old field names in dashboards
- **VRL metric access**
  - prefer the newer helper functions for reading/aggregating internal metrics in VRL when needed
- **ClickHouse sink path**
  - re-evaluate `json_each_row` vs `batch_encoding.codec = "arrow_stream"` based on schema stability and destination behavior
- **Upgrade validation**
  - include a version check in runbooks/pipelines (for example `vector --version`) before `vector validate` / `vector test`

## Default workflow

### Step 1: classify the topology
Pick the closest shape:
- single-node edge agent
- central aggregator
- edge agent -> central vector sink -> downstream sinks
- Kubernetes daemonset + aggregator
- metrics-only
- logs-only
- mixed logs/metrics/traces
- ClickHouse landing pipeline

### Step 2: gather constraints
Collect or infer:
- Vector version and deployment mode
- source protocols and throughput
- downstream sink latency/error profile
- allowed event loss
- required at-least-once behavior
- transformation complexity
- whether per-event routing or dynamic tables/indexes are used
- authentication and TLS requirements
- expected backpressure strategy

### Step 3: choose a topology contract
For each path, write:
- source -> transform(s) -> sink(s)
- event schema in and out
- failure behavior
- buffer type and size
- acknowledgement expectations
- retry and timeout behavior
- how the path is tested

Do not mix experimental and production sinks casually. Fanout and acknowledgement semantics can surprise you.

### Step 4: implement VRL safely
Rules:
- keep programs readable and composable
- explicitly handle fallible parsing and coercion
- normalize timestamps, levels, service labels, and routing keys
- add unit tests for every non-trivial transform
- use the REPL / `vector vrl` for quick experiments

### Step 5: validate and test
Before suggesting rollout:
- run `vector validate`
- run `vector test`
- if config is split across files, validate/test the combined set
- check that `data_dir` exists and is writable when disk buffers/checkpoints are involved

### Step 6: observe the observer
Default observability plan:
- route `internal_logs`
- scrape or ship `internal_metrics`
- watch buffer, retry, dropped-event, and backpressure signals
- expose enough metadata to trace sink-specific failures

## Delivery guarantee rules

### Acknowledgements
- Use end-to-end acknowledgements only when the source and sink path actually support the durability contract you need.
- Explain that acknowledgements can reduce throughput and change failure semantics.
- In fanout, remember sinks can influence source acknowledgement behavior.

### Buffers
- `memory`: faster, less durable
- `disk`: more durable, slower, needs `data_dir`, enough disk, and monitoring
- `when_full = block`: preserve data, propagate backpressure
- `when_full = drop_newest`: prioritize liveness, knowingly lose data

### Health checks
- start with sink healthchecks enabled
- when startup must fail fast on unhealthy downstreams, use `vector --require-healthy`

## ClickHouse sink rules
When the user is sending Vector data to ClickHouse:
- decide whether standard JSON formats are good enough or whether `batch_encoding.codec = "arrow_stream"` is worth it
- set batching deliberately: `batch.max_bytes`, `batch.max_events`, `batch.timeout_secs`
- pick compression intentionally (`gzip`, `zstd`, etc.)
- consider `date_time_best_effort` when RFC3339 / ISO8601 timestamps are involved
- use `skip_unknown_fields` only if you are intentionally tolerating schema drift
- document auth, TLS, retries, and timeout behavior
- mention current edge cases if using Arrow stream with complex ClickHouse schemas

## Multi-agent plan
If multi-agent is enabled, use or suggest:
- `topology_architect`: break the pipeline into contracts and failure domains
- `vrl_engineer`: implement / test transformations
- `delivery_guarantees`: analyse acks, buffers, retries, and loss semantics
- `sink_specialist`: tune the destination sink (ClickHouse, Kafka, S3, etc.)
- `ops_observability`: internal metrics/logs, rollout, capacity, and incident playbooks
- `community_risk_reviewer`: scan current issues/community threads for sharp edges

## Output contract
Every final answer using this skill should include:
1. topology summary
2. config fragments
3. buffer/ack rationale
4. validation/test commands
5. monitoring plan
6. risk notes and rollback/fallback strategy

## Included resources
Open only what you need:
- `references/TOPOLOGY_WORKFLOW.md`
- `references/VRL_GUIDE.md`
- `references/BUFFERS_AND_ACKS.md`
- `references/CLICKHOUSE_SINK.md`
- `references/VALIDATION_AND_TESTING.md`
- `references/INTERNAL_MONITORING.md`
- `references/HELM_CHART_OPERATIONS.md`
- `references/TROUBLESHOOTING.md`
- `references/COMMUNITY_NOTES.md`
- `assets/templates/vector-basic.yaml`
- `assets/templates/vector-clickhouse.yaml`
- `assets/templates/vector-tests.yaml`
- `assets/templates/common.vrl`
- `prompts/AGENT_PROMPT.md`
- `prompts/MULTI_AGENT_PROMPT.md`
