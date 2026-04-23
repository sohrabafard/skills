# Alaa Observability And Services Contract Rewrite

## Timestamp

2026-04-22 20:54 Asia/Tehran

## Scope

Rewrite the local `alaa-observability-soc` and `alaa-services-contract` skills so future agents apply one deterministic Ala observability and service contract across current and future services.

## Objective

- Make conflicts between the two skills explicit.
- Make observability decisions mandatory where the platform contract requires them.
- Preserve current service reality for `auth`, `ticket`, `comment-service`, `content`, `gateway`, `entitlement-platform`, `wa`, and `notification`.
- Add the user's trace rule: OTLP and structured log output must make `trace_id` queryable alongside `traceparent`.

## Assumptions

- `assessment` is not present under `D:\Sohrab\Project` in this session.
- `notification` exists and is in development; it has request correlation and Sentry scaffolding but not the same completed OTel/Prometheus surface as the completed Laravel service rollouts.
- Sentry remains useful for exception grouping, release tracking, source maps, and developer workflow, but SigNoz plus OTel Collector remains the main Ala observability path.

## Constraints

- Do not change service repositories in this task.
- Keep skill `SKILL.md` files routing-first; detailed rules live in `references/`.
- Keep `alaa-services-contract` as the hard Ala platform contract and `alaa-observability-soc` as the deeper signal/SOC decision model.
- Do not allow per-run agent preference to override stable headers, event names, metric labels, collector topology, or Sentry role.

## Task Decomposition

1. Inspect target skills and references.
2. Verify current external observability guidance from official sources.
3. Inspect live local service repos for current Ala service shape.
4. Patch SOC skill reference with deterministic signal decision rules.
5. Patch services-contract reference with mandatory platform adoption rules and trace-id query contract.
6. Align topic maps and top-level skill routing.
7. Validate YAML/frontmatter and basic Markdown structure.

## Dependency Notes

- `alaa-services-contract` should require `alaa-observability-soc` for telemetry design, SOC evidence, alert/runbook, Sentry, or signal-catalog work.
- `alaa-observability-soc` should defer Ala-specific service headers, route contracts, trusted ingress, metric names, and deploy topology to `alaa-services-contract`.

## Validation Approach

- Run skill validation with the local skill-creator validation script if available.
- Run focused `rg` checks for stale optional language, `trace_id`, `traceparent`, Sentry role, and topic-map alignment.
- Run `git diff --check`.

## Parallelization Opportunities

No subagents were requested for this execution. Local read-only inspection was parallelized with shell reads/searches.

## Exit Criteria

- The two skills state their ownership boundary and conflict precedence.
- The platform rule is deterministic: logs/traces/metrics/exceptions are not optional for long-lived services.
- The user-provided OpenTelemetry, Collector, SigNoz, Sentry, metrics, logs, trace, exception, and profiling guidance is represented in concise skill form.
- `trace_id` is mandatory as a query field in logs/OTLP logs while `traceparent` remains the propagation header.
- Current service reality is summarized without making unverified changes to service repos.
