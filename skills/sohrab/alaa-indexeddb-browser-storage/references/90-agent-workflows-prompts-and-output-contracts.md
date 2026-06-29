# Agent workflows, prompt patterns, and output contracts

## Agent behavior principles

For GPT-style and Claude-style coding agents:

- Use precise role, scope, and stop criteria.
- Gather enough context, then act; do not over-search once the path is clear.
- Use progressive disclosure: load only relevant reference files.
- Prefer checklists and decision records for complex storage work.
- Make assumptions explicit when a detail is missing and not blocking.
- Verify code changes with tests or deterministic checks.
- For current browser/version facts, refresh official sources and cite/record them.
- Never hide uncertainty about browser-specific behavior; convert uncertainty into feature detection and tests.

## Default task workflow

For any IndexedDB feature request:

```text
1. Classify the feature.
2. Identify data classes and source of truth.
3. For Alaa, identify the SDK/gateway client and prove storage code will not own token attach, refresh, trusted headers, or authz decisions.
4. Select capability tiers and fallback behavior.
5. Design schema/object stores/indexes.
6. Define quota budget and cleanup policy.
7. Define security/privacy rules.
8. Define migration/multi-tab plan.
9. Define sync/offline/conflict behavior if relevant.
10. Implement with short transactions and feature detection.
11. Test with unit + browser matrix.
12. Add observability and operational notes.
```

## Output contract: architecture answer

Use this structure:

```markdown
## Decision

## Data and source of truth

## Browser capability tier and fallback

## IndexedDB design

### DB
### Object stores
### Indexes
### Record schemas

## Quota / persistence / eviction

## Security and privacy

## Migration and multi-tab

## Sync / conflict / recovery

## Testing and observability

## Risks and open decisions
```

## Output contract: code review

```markdown
## Review result

## Confirmed issues

## Browser compatibility risks

## Quota/eviction risks

## Security/privacy risks

## Migration/concurrency issues

## Patch recommendation

## Required tests
```

## Output contract: implementation plan

```markdown
## Goal

## Assumptions

## Files to change

## Schema changes

## Capability detection

## Write/read paths

## Cleanup and quota handling

## Migration path

## Tests

## Rollout and telemetry
```

## Prompt pattern: feature design

```text
Use $alaa-indexeddb-browser-storage.
Design an IndexedDB feature for [feature].
Constraints:
- supported browsers: [list]
- data classes: [draft/cache/outbox/etc]
- offline requirement: [none/basic/critical]
- sensitive data: [yes/no]
- expected records/bytes: [estimate]
For Alaa, keep protected calls behind @alaa/sdk or @alaa/sdk-vue and do not store trusted gateway headers or authz decisions.
Return a decision record, schema, quota plan, fallback tiers, security notes, and test matrix. Do not write implementation code unless necessary.
```

## Prompt pattern: implementation

```text
Use $alaa-indexeddb-browser-storage.
Implement [feature] in this repo.
Before editing, inspect current storage utilities and AGENTS.md.
Use feature detection, short transactions, quota handling, and migration-safe schema changes.
Do not store tokens/secrets, decoded JWT claims, trusted gateway headers, or authz decisions.
Use the approved Alaa SDK/gateway path for protected sync; do not call service-local authz paths or OpenFGA from browser storage.
Add or update tests for fresh install, upgrade, quota error, and unavailable storage.
Summarize files changed and remaining risks.
```

## Prompt pattern: browser compatibility audit

```text
Use $alaa-indexeddb-browser-storage.
Audit this IndexedDB code for Chrome/Edge, Firefox, Safari/iOS, private mode, and embedded webview differences.
Search official sources if making current compatibility claims.
Return: capability gaps, fallback plan, test matrix, and recommended code changes.
```

## Prompt pattern: quota/resilience audit

```text
Use $alaa-indexeddb-browser-storage.
Audit storage quota and eviction resilience for [feature].
Check budgets, cleanup order, QuotaExceededError handling, persistence request timing, private-mode behavior, and user-visible recovery.
Return concrete patch suggestions and tests.
```

## Prompt pattern: security audit

```text
Use $alaa-indexeddb-browser-storage.
Review local browser storage for secrets, decoded JWT claims, trusted gateway headers, PII, entitlement authority, authz/OpenFGA decisions, cache poisoning, logout purge, shared-device risk, and XSS exposure.
Return must-fix issues, acceptable data classes, and a revised storage policy.
```

## Clarification policy

Ask clarifying questions only when a missing detail changes the safety or architecture materially, such as:

- whether data is secret/PII
- whether offline persistence is critical
- required browser support including Safari/iOS/webview
- expected data volume
- whether server has idempotency/conflict APIs

If not blocking, proceed with explicit assumptions and mark them as assumptions.

## Agent anti-patterns

- Jumping straight to Dexie/raw IDB code without data classification.
- Assuming IndexedDB quota is "unlimited".
- Assuming `navigator.storage.estimate()` is exact.
- Promising offline durability in private mode.
- Implementing a feature only tested in Chrome.
- Storing auth tokens because "IndexedDB is not localStorage".
- Storing decoded JWT claims, trusted gateway headers, or `X-Access` as local context.
- Calling `authz-sidecar`, `entitlement-spoa`, OpenFGA, or service-local protected routes directly from browser storage sync.
- Using user-agent checks as primary logic.
- Ignoring `blocked`/`versionchange`.
- Running fetch inside a transaction.
- Treating local entitlement cache as authoritative.
- Omitting cleanup and quota tests.

## Review rubric

Score each from 0 to 2:

| Area | 0 | 1 | 2 |
|---|---|---|---|
| Source of truth | unclear | partially defined | server/client boundaries explicit |
| Security | secrets/PII risk | partial controls | classification + purge + validation |
| Compatibility | Chrome-only | some fallback | capability tiers + tests |
| Quota | ignored | catches errors | budgets + cleanup + UX |
| Migration | ad hoc | upgrade works one path | tested multi-version + blocked handling |
| Transactions | unsafe awaits | mostly safe | short, batched, transaction-complete-aware |
| Offline/sync | fragile | retry basic | idempotent, bounded, conflict-aware |
| Observability | none | errors only | privacy-safe metrics and runbooks |

Require score 2 for security and quota before production storage-heavy rollout.
