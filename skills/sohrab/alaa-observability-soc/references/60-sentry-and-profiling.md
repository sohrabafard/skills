# Sentry and Profiling

Load when the task enables, tunes, or reviews Sentry, or turns profiling on or off.

Sentry env variable names and their default values, and the package set for each runtime, belong to
`/alaa-services-contract`, `references/21-alaa-platform-observability-directive.md`. Sample rates and their ceilings are in
`30-quantitative-budgets.md`. This file owns the role split, the gates, and the reasons.

## The role split

SigNoz is the operational source of truth for service health: traces, logs, metrics, dashboards, alerts, and
cross-signal correlation. Sentry is a focused application-exception and developer-workflow tool: grouping, stack traces,
first-seen and regression detection, release health, frontend source maps and debug IDs, issue ownership, and developer
notification.

## Optional direct SDK telemetry

Direct Sentry SDK logs and traces are optional alongside application -> Vector -> Collector. Both paths may run
simultaneously and deliver duplicate logs/traces; no duplication approval is required. Direct delivery adds no filtering
or data-inspection gate; the platform privacy invariant still binds. In sensitive environments, operators disable direct
Sentry logs/traces while retaining Sentry exceptions and the Vector/Collector path.

## Exception coverage gates

- Exceptions are observable with Sentry absent, disabled, or unreachable. The platform path always records the exception
  on the active span and emits a structured error log carrying the correlation fields, exception type, safe message, and
  route or operation, and exports both over OTLP.
- Sentry is never the only exception path, and platform metrics and traces are never sent only to Sentry.
- Sentry logs and traces do not replace the platform pipeline.

Reason the exception-coverage requirement is a gate rather than a preference: an unhandled exception is by definition
unhandled, and the cases that matter most — a crash at boot, a worker dying, a panic outside any request — often have no
active span at all.
Those never reach the Collector on their own, which is why a dedicated capture path stays in place.

## Can Sentry be just an OTLP destination behind the Collector?

No, and the reason is specific. Dated 2026-07; version-sensitive, re-check `90-source-map.md` before restating.

- Sentry ingests OTLP for traces and logs through the Collector. That path is open beta and single-project by default;
  routing several customers or services into separate projects needs the Collector's routing connector.
- OTLP does not carry errors to Sentry. Only the Sentry SDK captures backend exceptions and links them to the trace, and
  error grouping, first-seen and regression detection, source maps and debug IDs, and release health all depend on the
  SDK.
- Therefore the SDK stays. Removing it to make Sentry a pure OTLP sink silently ends exception grouping while leaving the
  integration looking connected, which is the worst kind of regression: the dashboards still render.

## Sentry configuration gates

- Real DSNs are never committed. Release and environment are injected by the build or deploy, never hardcoded, because a
  Sentry issue with the wrong release attribution sends the regression hunt to the wrong commit.
- Default-PII sending stays off unless an approved written data policy says otherwise. Scrub with the SDK's own
  before-send hook for exception events rather than filtering downstream, so the data never leaves the process.
- On a long-lived runtime — Octane, a resident worker, any process reused across requests — Sentry scope and context are
  reset per request or per job, and no request-scoped state lives in a static or a singleton without an explicit reset
  path. Leaked scope attributes one customer's error to another customer's user, which is a data-protection incident,
  not a cosmetic bug.
- Source-map or release upload tokens live in CI secrets.

Validation before calling a Sentry integration done: outbound connectivity confirmed; one controlled test exception sent
from a non-production environment and observed arriving with the expected environment and release; sensitive fields
confirmed absent from the received event; trace and profile rates confirmed at the intended values; and the platform
OTLP path confirmed still carrying exceptions with Sentry disabled.

## Profiling

Profiles answer why code is expensive. Enable profiling only when trace and metric evidence has already localised a real
performance problem, the runtime and storage cost is acceptable, and the data sensitivity has been checked — a profile
captures stack and sometimes argument context, so it is subject to the same privacy invariant as every other signal.

Gates:

- Profiling starts disabled. Rates and ceilings are in `30-quantitative-budgets.md`.
- Enabling it requires a named owner, a documented rollback switch, a stated cost expectation, and a retention period
  from `40-alerting-slo-retention.md`.
- Continuous profiling is not a fleet minimum. Reach for it on CPU or memory contention, tail latency with no visible
  slow span, allocator pressure, or a long-lived worker whose cost grows over time.
- Where the task changes a hot path rather than only observing it, pair the runtime's performance skill; this skill
  decides whether the profile may be collected, not how to make the code faster.
