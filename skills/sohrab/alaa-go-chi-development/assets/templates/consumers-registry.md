# alaa-go-chi Consumers

<!--
Lives at docs/CONSUMERS.md in the alaa-go-chi repository. The single registry of every service built on, or
migrating to, the kit, and the iteration set for impact analysis and platform audits. Rules:
alaa-go-chi-development references/50-consumer-registry.md. The ONLY kit-repo file a consumer agent may edit, and
only its own row. Never delete another service's row — mark it `retired`. Rows are current state; history is git.

The Current Execution Scope section below is a POINTER, not a policy: it names the owner-ratified scope record
that governs, and nothing else. What that record permits is resolved at session start by the reading procedure in
references/05-phase-and-source-truth.md. Do not restate a phase's rules here — a copy here goes stale the moment
the owner ratifies a new record, and a stale copy is read as authority.
-->

## Current Execution Scope

Governed by `change-requests/<YYYY-MM-DD-slug>-scope.md`. That record names the active phase, the consumers it
lists, and the baseline they start from. Read it, and the capability matrix in the
`alaa-go-chi-development` skill, before treating any row below as authority to do anything. A row is inventory; it
is never execution authority.

| service | status | repo | kit_version | contracttest (last verified) | surfaces | agent_notes | registered | updated |
|---|---|---|---|---|---|---|---|---|
| <service> | <status> | <path/URL> | <pin or —> | <evidence + date, or `not-current`> | <kit packages actually consumed> | <one line: arch doc, caveat, and the marker string the active scope record prescribes> | YYYY-MM-DD | YYYY-MM-DD |

Status vocabulary: `planned` → `bootstrapping` → `active`; existing services: `planned-migration` → `migrating` →
`active`; also `paused`, `retired`.
Contracttest vocabulary: `passing` / `failing` / `local_ci_smoke_passed; runner_contract_pending` / `not-wired` /
`not-current`.
