# Helm chart operations

The official chart, verified 2026-07-30: chart `0.58.0`, appVersion
`0.57.0-distroless-libc`. Every claim below was read from the chart's own
`values.yaml` on that date.

Re-derive the versions:

```bash
curl -s https://raw.githubusercontent.com/vectordotdev/helm-charts/develop/charts/vector/Chart.yaml
```

Re-derive the option semantics:

```bash
curl -s https://raw.githubusercontent.com/vectordotdev/helm-charts/develop/charts/vector/values.yaml
```

**The chart version and the Vector version are two different numbers.** Compare the
chart's `appVersion` against the Vector release pin in
`80-version-and-upgrade-deltas.md` on every bump. When they differ, a Helm-deployed
pipeline runs a different Vector build from a package-installed one, and a
version-sensitive change — 0.57.0's interpolation default, for instance — lands in
one environment and not the other. `scripts/check-upstream-version.mjs` prints both
and flags the mismatch.

Kubernetes platform mechanics beyond these Vector-specific keys belong to
`/alaa-k8s-helm` (`$alaa-k8s-helm`), and Arvan CaaS platform constraints to
`/caas-arvan-kuber` (`$caas-arvan-kuber`).

## Role determines the workload, so pick it first

The chart's comment states the mapping:

```
Agent                = DaemonSet
Aggregator           = StatefulSet
Stateless-Aggregator = Deployment
```

`role` defaults to `"Aggregator"`, so a values file that omits it gets a
StatefulSet. Set it explicitly — the default is not a choice you made.

The role decides whether disk buffers are viable, which is why it is the first
decision and not a deployment detail:

- **Agent (DaemonSet)** — node-local. A disk buffer means a `hostPath`, which is
  tied to the node's lifecycle: drain the node and the buffered events go with it.
- **Aggregator (StatefulSet)** — has stable storage. This is the only role where a
  disk buffer survives a pod reschedule, so an audit-grade path with
  `when_full: block` belongs here.
- **Stateless-Aggregator (Deployment)** — no stable storage. Memory buffers only.
  Do not configure a disk buffer for this role; it will not survive a rollout.

Delivery contract per path is written once in
`10-topology-and-delivery-contract.md`; this is where it becomes a workload choice.

## Config source precedence

Verified from `values.yaml`: *"existingConfigMaps -- List of existing ConfigMaps for
Vector's configuration instead of creating a new one. Requires dataDir to be set.
Additionally, containerPorts, service.ports, and serviceHeadless.ports should be
specified based on your supplied configuration. **If set, this parameter takes
precedence over customConfig and the chart's default configs.**"*

So the order is `existingConfigMaps` > `customConfig` > chart defaults. Two
consequences:

- Setting both `existingConfigMaps` and `customConfig` is not an error and not a
  merge — `customConfig` is **silently ignored**. If a config change appears to have
  no effect, check for a leftover `existingConfigMaps` first.
- With `existingConfigMaps`, the chart no longer derives values from your config, so
  you must supply `dataDir`, `containerPorts`, `service.ports` and
  `serviceHeadless.ports` yourself. Note that `dataDir` is *only* used when
  `existingConfigMaps` is set — setting it otherwise does nothing, which is a
  frequent source of "my disk buffer has no data_dir" confusion.

`customConfig` is a full replacement, not an overlay: *"Override Vector's default
configs, if used all options need to be specified."* A `customConfig` that forgets
`internal_metrics` does not inherit it — self-observation silently disappears. Treat
`customConfig` as the whole config contract and validate the rendered result.

## Vector templates collide with Helm templates

`customConfig` supports Helm templating, so `{{ }}` is ambiguous: Helm renders it
before Vector ever sees it. A Vector routing template must be escaped:

```yaml
table: '{{ print "logs_{{ tenant }}" }}'
```

Get this wrong and Helm resolves `{{ tenant }}` to empty, producing `table: "logs_"`
— a config that deploys, validates, and writes every tenant's data to one table.
Always confirm the rendered output with `helm template` rather than reasoning about
the escaping.

## Images

- `image.repository` for a private registry, fully qualified.
- `image.pullSecrets` explicitly; it defaults to `[]`.
- `image.tag` defaults to empty and is *derived from the chart's appVersion*. So
  bumping the chart changes the Vector version unless you pin.
- `image.sha` exists and takes a digest. Prefer it in production: a digest cannot
  move under you, and it makes the deployed Vector version an auditable fact rather
  than a tag lookup.

## Persistence

`persistence.enabled` defaults to `false`. `persistence.existingClaim` is valid for
the Aggregator role only. If a disk buffer is configured and persistence is off, the
buffer lives in the pod's ephemeral storage: it is lost on every restart, which
removes the durability the disk buffer was chosen for, and the pod's ephemeral
storage limit — not the buffer's `max_size` — decides when Vector exits. Size the
volume against the sum of every configured `max_size`, per
`30-buffers-acks-and-backpressure.md`.

## Before deploying

```bash
helm lint .
helm template . -f values.yaml > rendered.yaml
# then extract the Vector config from the rendered ConfigMap and validate it:
vector validate --skip-healthchecks vector.yaml
```

Validate the **rendered** config, not the values file. The values file is not a
Vector config and `vector validate` cannot check it, so a Helm-level templating
mistake is invisible until the rendered form is checked. Use the flag set from
`50-validation-and-testing.md`, not `--no-environment`.

Startup health gating (`--require-healthy`) and its trade-off are in
`60-internal-monitoring.md`.
