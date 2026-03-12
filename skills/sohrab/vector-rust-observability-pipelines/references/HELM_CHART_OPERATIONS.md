# Helm chart operations (official Vector chart)

Use this when Vector is deployed via Helm.

## Role -> workload mapping
- `Agent` -> `DaemonSet`
- `Aggregator` -> `StatefulSet`
- `Stateless-Aggregator` -> `Deployment`

Pick role first, then tune buffers/persistence and rollout policy around that role.

## Values strategy
- Keep chart `values.yaml` overrides minimal and environment-focused.
- Avoid copying full defaults into your repo; this increases upgrade drift and merge pain.
- Prefer small overlay files per environment.

## Config source precedence
- `existingConfigMaps` takes precedence over inline/custom config.
- If using `existingConfigMaps`, ensure required settings are still provided in values:
  - `dataDir`
  - container ports
  - service/headless service ports (as applicable)

## customConfig safety
- `customConfig` can replace chart-generated defaults; treat it as a full config contract.
- Vector templating snippets can collide with Helm templating.
- Escape Vector templates in Helm values when needed (for example:
  `{{ print "{{ host }}" }}` pattern).

## Image and registry policy
- For private registry use:
  - fully-qualified image repository
  - explicit pull secrets
- In production, prefer digest pinning (`image.sha`) over mutable tags.
- Keep helper/runtime images aligned with your cluster pull policy.

## Persistence and reliability
- Aggregator role commonly benefits from persistent storage for disk buffers/checkpoints.
- Agent role with host-local data can use hostPath patterns deliberately.
- If data durability matters, confirm PVC/hostPath behavior before rollout.

## Rollout and health
- Use startup/readiness behavior that matches delivery expectations.
- If downstream dependency health must gate startup, enforce that policy explicitly.
- Validate rendered manifests and Vector config before deploy:
  - `helm template`
  - `helm lint`
  - `vector validate`
