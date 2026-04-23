
# Official-first source map

Use this map before giving version-sensitive Vector topology, VRL, sink, buffering, or operations guidance. Official Vector docs, official component docs, and the target runtime's `vector --version`/`vector validate` evidence outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Vector docs home:
  https://vector.dev/docs/
- Concepts:
  https://vector.dev/docs/introduction/concepts/
- Buffering model:
  https://vector.dev/docs/architecture/buffering-model/
- End-to-end acknowledgements:
  https://vector.dev/docs/architecture/end-to-end-acknowledgements/
- Validation:
  https://vector.dev/docs/administration/validating/
- Unit tests:
  https://vector.dev/docs/reference/configuration/unit-tests/
- Internal monitoring:
  https://vector.dev/docs/administration/monitoring/
- VRL reference:
  https://vector.dev/docs/reference/vrl/
- VRL functions:
  https://vector.dev/docs/reference/vrl/functions/
- ClickHouse sink:
  https://vector.dev/docs/reference/configuration/sinks/clickhouse/
- Helm install docs:
  https://vector.dev/docs/setup/installation/package-managers/helm/
- Official Vector Helm chart repo:
  https://github.com/vectordotdev/helm-charts
- Vector chart README:
  https://github.com/vectordotdev/helm-charts/blob/develop/charts/vector/README.md
- Releases:
  https://github.com/vectordotdev/vector/releases
- Security policy:
  https://github.com/vectordotdev/vector/security/policy

## Freshness triggers

Fetch current official docs when the task mentions `latest`, Vector versions, VRL function behavior, component option names, ClickHouse sink behavior, acknowledgements, disk buffers, internal metrics, Helm chart values, Kubernetes deployment mode, deprecations, or security/current-runtime behavior.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, forum posts, and community blogs only to troubleshoot observed failures or collect hypotheses. Confirm topology, VRL, sink, buffering, acknowledgement, and Helm guidance against Vector docs or runtime validation evidence.
