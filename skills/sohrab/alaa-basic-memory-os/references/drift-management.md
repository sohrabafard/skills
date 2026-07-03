# Drift Management

Drift = a recorded mismatch between two sources of truth: doc vs code, memory vs repo, service vs service, shared architecture doc vs actual behavior.

## Core rule

Never silently pick a side when sources disagree. Record the drift, keep working on the safest verified behavior, and let the human decide.

## High-priority domains (default severity high/critical)

- SOC/observability log contracts (fields, format, destination of logs sent to the SOC server)
- Notification contracts (Notification Core, Realtime Hub, Delivery Workers, Queue/Broker payloads, routing keys)
- Auth/entitlement rules and OpenFGA tuples
- Upload lifecycle events between `tusd` and target services

## Model

- One drift note per mismatch, in `drift/`, `type: drift`, from the Drift Note Template.
- Frontmatter lifecycle: `drift_status: open → analyzed → decided → fixing → resolved`; `drift_severity: low|medium|high|critical`.
- Each affected contract/architecture/operations note gets exactly one `- [drift] see [[<drift note>]]` observation and `status: needs_review`.
- `drift/Drift Registry.md` keeps the Open drift list current.
- Relations: `part_of [[Drift Registry]]`, `conflicts_with [[<affected note>]]`, later `resolved_by`.

## Workflow (prompt pack)

1. Prompt 13 — record: verify both sides, create/update the drift note, mark affected notes, register.
2. Prompt 14 — analyze + decide: re-verify, explain impact, recommend a winning side, wait for approval, record `[decision]`, generate per-project `[todo]` fixes.
3. Prompt 15 — fix per project: apply decision to code AND docs, validate, clear the `[drift]` marker, update `last_verified`; when all projects fixed → `drift_status: resolved`, `status: archived`, remove from registry.

## Queries

```powershell
bm tool search-notes --type drift --project alaa-memory
bm tool search-notes --type drift --meta drift_status=open --project alaa-memory
bm schema validate drift --project alaa-memory
```

## Do not

- Do not fix code during prompts 13/14.
- Do not resolve a drift note while any affected project remains unfixed.
- Do not delete drift notes; archive them (audit trail).
- Do not treat `bm schema diff` output (schema-vs-usage drift) as contract drift — that is metadata maintenance.
