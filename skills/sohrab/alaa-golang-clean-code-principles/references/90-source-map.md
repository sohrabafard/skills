# Source Map — Where These Principles Come From, and When to Re-Verify

## Source priority

1. Repository code and repo-local `AGENTS.md`/`CLAUDE.md` in the target service — always wins for current
   behavior.
2. The kit design contract: `D:/Sohrab/Project/docs/idea/alaa-go-chi-framework.md` (Revision 3+) and, once the
   kit repo exists, its `CONTRACTS.md` — wins for every kit-owned shape this skill cites (envelope, env keys,
   metric names, pooling lanes, readiness severities, seeder contract).
3. The consumer designs that exercised the principles:
   `D:/Sohrab/Project/docs/idea/news-service-go-architecture.md` (Rev 4+),
   `D:/Sohrab/Project/docs/idea/notification-v2-go-architecture.md` (Rev 6+),
   `D:/Sohrab/Project/docs/idea/2026-07-05-entitlement-platform-kit-adoption.md`.
4. The origin document of this skill:
   `D:/Sohrab/Project/docs/idea/alaa-golang-clean-code-principles.md` (2026-07-05).
5. Companion skills for their owned domains: `alaa-services-contract` (exact platform shapes),
   `alaa-trust-gateway-auth` (header semantics), `alaa-observability-soc` (signal model), `alaa-golang`
   (Go depth).

## Facts most likely to rot (re-verify against source 2 before relying on them)

- **Identity types** — currently `X-Project-Id` = UUIDv7, `X-User-Id` = int64 `users.id`. A platform identity
  change invalidates P3's examples.
- **Pooling lanes** — currently `PG_DSN` (pooled) + `PG_MIGRATE_DSN` (direct), `PG_SCALE_TIER` bands. A pgkit
  redesign invalidates P6's corollary.
- **Kit-owned metric names and env keys** — the concrete lists live in the framework doc / `CONTRACTS.md`;
  P10/P11 cite the rule, not a frozen list.
- **Provider idempotency examples** (Bale `request_id`, Mediana none) — provider contracts evolve; the
  provider skills (`alaa-bale-provider`, `alaa-sms-provider-mediana`) are their source of truth.

## Freshness triggers

Re-open the kit framework doc and update this skill when any of these happen: a kit major version; a change to
the canonical envelope, envelope codec, or outbox DDL; a new readiness severity; a change to trusted-header
types; a new kit package that absorbs a concern currently listed as service-local.

## Durable content (safe to trust without re-checking)

The thirteen principles themselves — kit-first discipline, declared route posture, single-parse trust context,
errors-as-values, ports/adapters, transactional outbox, idempotency-by-construction, explicit wire shapes,
owned goroutines, boot-time config, bounded observability, boundary-true testing, contracts-over-reach-ins —
are architectural invariants of this platform, not version-sensitive facts.
