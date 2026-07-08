# alaa-go-chi Consumers

<!--
This file lives at docs/CONSUMERS.md in the alaa-go-chi repository.
It is the single registry of every service built on (or migrating to) the kit, and the iteration set for
kit impact analysis and platform audits. Rules: see the alaa-go-chi-development skill,
references/50-consumer-registry.md. This is the ONLY kit-repo file a consumer agent may edit.
Never delete another service's row — mark it `retired`. Keep rows current-state; history lives in git.
-->

| service | status | repo | kit_version | contracttest | surfaces | agent_notes | registered | updated |
|---|---|---|---|---|---|---|---|---|
| news | planned | <created via `alaa-go-chi new service news`> | — | not-wired | (all scaffold defaults) | `docs/news-service-go-architecture.md` Rev 4 | YYYY-MM-DD | YYYY-MM-DD |
| notif | planned | <created via `alaa-go-chi new service notif`> | — | not-wired | (all scaffold defaults) | `docs/notif-service-go-architecture.md` Rev 6 | YYYY-MM-DD | YYYY-MM-DD |
| entitlement-api | planned-migration | entitlement-platform/services/entitlement-api | — | not-wired | pgkit (pooling-model donor) | `docs/2026-07-05-entitlement-platform-kit-adoption.md`; migrate after news+notif | YYYY-MM-DD | YYYY-MM-DD |
| tusd | planned-migration | tusd | — | not-wired | — | upload platform; migrate after news+notif; expect ProviderFacing gaps → change requests | YYYY-MM-DD | YYYY-MM-DD |

Status vocabulary: `planned` → `bootstrapping` → `active`; existing services: `planned-migration` → `migrating`
→ `active`; also `paused`, `retired`.
