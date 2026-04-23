# Official-first source map

Use this map before generating version-sensitive PromQL content. Prometheus docs outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Prometheus docs home: https://prometheus.io/docs/introduction/overview/
- Querying basics: https://prometheus.io/docs/prometheus/latest/querying/basics/
- Operators: https://prometheus.io/docs/prometheus/latest/querying/operators/
- Functions: https://prometheus.io/docs/prometheus/latest/querying/functions/
- Examples: https://prometheus.io/docs/prometheus/latest/querying/examples/
- Recording rules: https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/
- Alerting rules: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
- Histograms and native histograms: https://prometheus.io/docs/practices/histograms/
- Feature flags: https://prometheus.io/docs/prometheus/latest/feature_flags/

## Freshness triggers

Fetch current Prometheus docs when the task mentions `latest`, Prometheus 3.x behavior, native histograms, experimental functions, feature flags, alerting/recording rule syntax, vector matching edge cases, or syntax rejected by the user's runtime.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, forum posts, and community blogs only to troubleshoot observed query/runtime failures. Confirm syntax, functions, and alerting semantics against Prometheus docs.
