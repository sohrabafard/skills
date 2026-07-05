# Topic Map — Shortest Reading Path

Match the task to the smallest set of files. When two rows match, read both; when the task is a whole feature or
a whole-package review, read `full-guide.md` instead of assembling pieces.

| Task looks like | Read |
|---|---|
| New HTTP endpoint (handler + route) | `10-kit-and-trust-boundary.md` (P1, P2, P3) + `20-domain-data-and-consistency.md` (P4) |
| Authorization / permission / TOTP check in code | `10-kit-and-trust-boundary.md` (P2, P3); pair with `alaa-trust-gateway-auth` |
| New use case / business rule | `20-domain-data-and-consistency.md` (P4, P5, P6) |
| Repository / SQL / migration work | `20-domain-data-and-consistency.md` (P5, P6, P7); pooling lanes note in P6 |
| Anything that publishes events or commands | `20-domain-data-and-consistency.md` (P6, P8) |
| Consumer, seeder, retry, or replay logic | `20-domain-data-and-consistency.md` (P7) |
| Wire structs, DTOs, command payloads | `20-domain-data-and-consistency.md` (P8) |
| Worker, background loop, buffer, flusher | `30-runtime-and-observability.md` (P9) |
| Config, env vars, feature flags | `30-runtime-and-observability.md` (P10) |
| Logs, metrics, traces, Sentry, dashboards | `30-runtime-and-observability.md` (P11); pair with `alaa-observability-soc` |
| Writing or reviewing tests | `40-testing-and-contracts.md` (P12) |
| Calling / consuming another service | `40-testing-and-contracts.md` (P13); pair with `alaa-services-contract` |
| Full feature end to end, or package-level review | `full-guide.md` |
| "Where does this Go topic live?" | `50-skill-boundaries.md` |

Rule of thumb: if you are about to write a shape the kit might own (an envelope, a table, a middleware, a
metric name), stop and check P1 first — the most expensive mistake this skill prevents is a correct-looking
local implementation of something that already exists once.
