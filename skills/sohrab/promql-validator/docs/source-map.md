# Official-first source map

Use this map before validating version-sensitive PromQL content. Prometheus docs and promtool behavior outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Prometheus docs home: https://prometheus.io/docs/introduction/overview/
- Querying basics: https://prometheus.io/docs/prometheus/latest/querying/basics/
- Operators: https://prometheus.io/docs/prometheus/latest/querying/operators/
- Functions: https://prometheus.io/docs/prometheus/latest/querying/functions/
- Recording rules: https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/
- Alerting rules: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
- promtool command docs: https://prometheus.io/docs/prometheus/latest/command-line/promtool/
- Feature flags: https://prometheus.io/docs/prometheus/latest/feature_flags/
- Native histograms: https://prometheus.io/docs/practices/histograms/

## Freshness triggers

Fetch current Prometheus docs when validation depends on runtime version, promtool parser behavior, native histograms, experimental functions, feature flags, alerting/recording rule syntax, vector matching, or any security/current behavior claim.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, forum posts, and community blogs only to troubleshoot observed failures. Confirm validation findings and remediation against Prometheus docs or promtool output.
