# Bounded coverage and correction matrix

Audited 1 October 2026 against the complete package and HAProxy 3.4.6 release source.
Each row assigns guidance to its owner; a route is deliberate coverage, not a claim
that this package tests the other owner's behavior. Source keys resolve in SOURCES.md.

| Topic / existing owner | Verified gap and correction | Evidence / validation |
|---|---|---|
| Build, shared/per-thread state; 10 | Lua 5.5 support conflated with deployed interpreter; preserve state model and account for yield interleaving | INSTALL, hlua; exact-image unit gate |
| Load/init/request/reload; 10, 90 | Unsupported universal scalability, persistence and drain claims narrowed; initialization and reload budgets retained | configuration/API; source review, deployment drain unrun |
| Standard libraries; new 15 | Missing openlibs values/default/order and dependency closure; keep os where required | configuration/hlua; positive and negative parser tests |
| Registrations and contexts; 20 | Actions incorrectly described as ignoring returns; API/source argument counts disagree | Act/hlua; act.DENY and argument boundary probes |
| Actions/services/applets; 25 | Error variable set only on anticipated failures could admit exceptions; initialize deny before Lua, publish success last; services own partial-response failure | hlua_action; HTTP action error and success probes; applet disconnect tests required when used |
| Converters/fetches/variables; 30 | Blanket boolean ban and unconditional unset claim; directional conversion modes and explicit variable reset | hlua_lua2smp/hlua_smp2lua; nil/error/stale-variable HTTP probes |
| Sockets/subrequests; 25 | Claimed one-operation timeout and fragile gateway anecdote; inactivity plus overall bounds, fixed destination and framing validation | Socket API; dependency timeout/refusal harness required when introducing egress |
| Filters/tasks/CLI/events; 20, 90 | Sparse API list lacked callback lifetime, return/backpressure, privilege and idempotency decisions | API context/class entries; deployment-specific tests explicitly unrun |
| Clocks/randomness/identity; 40 | CPU clock banned as language fact; coarse unit conversion falsely invalid; per-value blocking entropy advice removed; preserve identifier contract | Lua manual/core.now; deterministic checker fixtures; codec owner for identity |
| Failure/logging; 30, 90 | pcall blanket rejection and stale measurements; preserve error contract and legitimate cleanup; label historical captures | Lua error/pcall, hlua; current error-level HTTP probes |
| Testing/module shape; 50, 60 | Mockability described as HAProxy restriction; checker clean falsely allowed shipping; exact-image harness added | lexical self-tests, embedded unit, native parser, HTTP tests |
| Cost/native alternatives; 70 | Non-yielding calls forbidden, maps all called hashes, patterns claimed no backtracking; bounded work and adversarial inputs required | configuration, Lua manual; static review, performance benchmark unrun |
| Input/security/secret scope; 80 | Private upvalue confused with global; retain strict logging/output validation and owner-approved failure policy | Lua lexical scope, API; malformed unit inputs and denial probes |
| Policy outside Lua | HAProxy directives/build/delivery -> `/alaa-haproxy`; trust -> `/alaa-trust-gateway-auth`; wire names/values -> `/alaa-services-contract`; review -> `/alaa-security-review` | topic-map routes, no consumer or gateway changes |
| Cache/freshness, retries and telemetry policy | `/alaa-reliability-sla` owns degradation/retry doctrine; `/alaa-observability-soc` owns telemetry gates; native caching belongs to `/alaa-haproxy` | routes only; no new fleet values |

The added openlibs reference owns library selection; the body routes to it. The
intentional behavior corrections above precede the final compression pass. That
pass preserves scope, exceptions, authority, validation and failure obligations.
