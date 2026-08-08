# Topic map

Match the situation you are in, read that one file, and return. Reading a file you
do not match costs context and buys nothing.

| You are about to | Read |
| --- | --- |
| lay out a pipeline, decide how many Vector tiers there are, write a per-path delivery contract, or work out whether one sink can stall another | `10-topology-and-delivery-contract.md` |
| write or debug a VRL program, handle a fallible call, default a missing field, or you hit `error[E651]` or an aborting `remap` | `20-vrl-transforms.md` |
| choose a buffer type, size a buffer, set `when_full`, enable acknowledgements, or answer what the pipeline does when the destination is unreachable | `30-buffers-acks-and-backpressure.md` |
| keep a source returning immediately and never slowing its upstream client, or check whether a path that answers fast today is actually configured to keep doing so | `35-pass-through-and-relay-paths.md` |
| configure the ClickHouse sink, set batching or retry options, template a `table` or `database`, or decide who owns the schema you are writing into | `40-clickhouse-sink.md` |
| work on the `wa` watch-time ingest pipeline, or decide whether a Vector path carrying product data fails open or fails closed | `75-ala-ingest-pipeline.md` |
| validate a config, write unit tests, choose the right `vector validate` flags, or interpret an exit code from Vector or from a checker | `50-validation-and-testing.md` |
| decide what to alert on, name an internal metric, or set the startup health policy | `60-internal-monitoring.md` |
| diagnose a live symptom: no data arriving, a stall, Vector exiting on its own, loss, duplication, high CPU, or a regression after an upgrade | `65-troubleshooting.md` |
| deploy or change Vector via the Helm chart, pick a role, or work out why a config change had no effect | `70-helm-chart-operations.md` |
| upgrade Vector, or repeat any claim about a version, a default, or a breaking change | `80-version-and-upgrade-deltas.md` |
| find out whether Vector can do a thing at the pinned version, or check that an option you are about to recommend is not deprecated | `82-capability-surface.md` |
| put a credential in a config, redact a field, or template a routing identifier | `85-security-and-secrets.md` |
| cite a source, or re-derive a version-sensitive fact rather than trusting this skill | `90-source-map.md` |

## Runnable checks

| You want to | Run |
| --- | --- |
| prove every shipped template and VRL snippet still compiles, and the unit tests pass | `node scripts/check-vector-configs.mjs` |
| prove the config checker can still detect the defects it claims to detect | `node scripts/check-vector-configs.mjs --self-test` |
| check whether this skill's version pins have gone stale | `node scripts/check-upstream-version.mjs` |
| prove the version resolver still rejects the `vdev-*` tag trap | `node scripts/check-upstream-version.mjs --self-test` |

All four honour `0` clean, `1` findings, `2` could not run, and all four take
`--help`.

## Not in this skill

| Question | Owner |
| --- | --- |
| What must a ClickHouse table be — engine, sorting key, partitioning, TTL, compression | `/clickhouse-performance-schema-ops` (`$clickhouse-performance-schema-ops`) |
| How is a SigNoz-owned table queried | `/alaa-signoz-clickhouse-docs` (`$alaa-signoz-clickhouse-docs`) |
| Is telemetry required here, and what gates on it | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| What is this field, metric, or variable called, and what is its Ala value | `/alaa-services-contract` (`$alaa-services-contract`) |
| Why does a reliability mechanism exist, and how do I choose its shape | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| How should this subsystem be designed | `/alaa-system-design` (`$alaa-system-design`) |
| What complexity bound must this path hold | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| How should this be tested, in general | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Is this trust boundary or credential path safe | `/alaa-security-review` (`$alaa-security-review`) |
| Kubernetes and Helm platform mechanics | `/alaa-k8s-helm` (`$alaa-k8s-helm`), and `/caas-arvan-kuber` (`$caas-arvan-kuber`) for Arvan CaaS |
| How do I plan or run a multi-agent change | `/alaa-cc-orchestrator` (`$alaa-cc-orchestrator`), or `/alaa-codex-orchestrator` (`$alaa-codex-orchestrator`) in Codex |
| Which model, and how much thinking | `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` |
| The ten-point quality bar | `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md` |
