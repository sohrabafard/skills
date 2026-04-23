# Source Map

Use this file when the service contract depends on standards, framework behavior, observability tooling, deployment tooling, or current platform docs.

## Source priority

1. Target repo truth: routes, controllers, middleware, resources, tests, config, Helm/Compose files, CI files, and current docs.
2. Ala platform skills that own the concern: this skill, `$alaa-trust-gateway-auth`, `$alaa-observability-soc`, `$alaa-docker-production`, `$caas-arvan-kuber`, `$alaa-gitlab-ci-cd`, and `$alaa-docs-farsi`.
3. Official or primary standards and product docs:
   - W3C Trace Context: https://www.w3.org/TR/trace-context/
   - OpenTelemetry docs and specs: https://opentelemetry.io/docs/
   - OpenTelemetry semantic conventions: https://opentelemetry.io/docs/specs/semconv/
   - Prometheus docs: https://prometheus.io/docs/
   - SigNoz docs: https://signoz.io/docs/
   - Sentry docs: https://docs.sentry.io/
   - Laravel docs: https://laravel.com/docs
   - Docker docs: https://docs.docker.com/
   - Kubernetes docs: https://kubernetes.io/docs/
   - GitLab CI/CD docs: https://docs.gitlab.com/ci/
4. Community posts, StackOverflow answers, blog posts, or vendor blogs only for troubleshooting a concrete failure or filling a gap after official docs and repo truth are checked.

## Freshness triggers

Re-check official docs and target repo truth when the task mentions:

- latest, current, today, version bump, upgrade, security, deprecation, breaking change, or compatibility
- OpenTelemetry packages, semantic conventions, Collector pipelines, SigNoz, Sentry, Prometheus, or W3C trace propagation
- Laravel, Docker, Kubernetes, GitLab, Arvan, gateway, or shared `service-ci-kit` behavior
- new service names, route families, readiness shape, response envelopes, or trusted-header contracts

## Example and anti-pattern

Good: before changing `/metrics`, verify the service route, the Prometheus scrape path, the Collector/SigNoz route, and the exact metric names in the repo.

Bad: copying a blog's OpenTelemetry package list into a Laravel service without checking the repo's current runtime, Composer constraints, and this contract's Collector/SigNoz ownership.
