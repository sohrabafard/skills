# alaa-go-chi Consumers

<!--
Lives at docs/CONSUMERS.md in the alaa-go-chi repository. Single registry of every service built on (or migrating
to) the kit; the iteration set for kit impact analysis and platform audits. Rules:
alaa-go-chi-development references/50-consumer-registry.md. The ONLY kit-repo file a consumer agent may edit (own
row only). Never delete another service's row — mark it `retired`. Rows are current-state; history lives in git.
Keep the Current Execution Scope section synchronized with the newest owner scope decision.
-->

## Current Execution Scope

<State the active phase and its decision record. While `KIT_FIRST_STABILIZATION` is active: every row is
inventory-only and `NOT_ASSESSED_KIT_FIRST`; rows must not trigger repository inspection, edits, audits, prompts,
validation, propagation, or release gates until explicit owner reactivation. After reactivation: name the
reactivated consumer(s) and their kit baseline.>

| service | status | repo | kit_version | contracttest | surfaces | agent_notes | registered | updated |
|---|---|---|---|---|---|---|---|---|
| <service> | <status> | <path/URL> | <pin or —> | <evidence> | <kit packages actually consumed> | <one line: arch doc / caveat; during kit-first: "Inventory only; NOT_ASSESSED_KIT_FIRST; do not inspect or propagate"> | YYYY-MM-DD | YYYY-MM-DD |

Status vocabulary: `planned` → `bootstrapping` → `active`; existing services: `planned-migration` → `migrating` →
`active`; also `paused`, `retired`.
Contracttest vocabulary: `passing` / `failing` / `local_ci_smoke_passed; runner_contract_pending` / `not-wired` /
`not-current`.
