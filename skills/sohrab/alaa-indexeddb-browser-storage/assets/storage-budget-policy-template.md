# Storage budget policy — <feature name>

Copy this file into the feature's directory and fill every cell. **A blank cap is not a
default; it fails review**, and `scripts/validate_skill_pack.py --check-budgets` rejects a
copy of this template that still contains `<...>` placeholders.

Every value below is a **name** owned by `/alaa-services-contract` (`$alaa-services-contract`)
and is read from configuration, never written as a literal at a call site. The retry and
timeout semantics of any value here are `/alaa-reliability-sla` (`$alaa-reliability-sla`).

- Feature: `<feature>`
- Owner: `<team or person>`
- Decision record: `<path to the ADR>`
- Capability tier required: `<0 | 1 | 2 | 3>` — below this tier the feature is not offered
- Reviewed: `<ISO date>`

## Per-class caps

| Data class | Cap (bytes or count) | Cleanup rule | Droppable under pressure | Bound |
|---|---:|---|---|---|
| `public_cache` | `<e.g. 2 MB>` | TTL replace | yes | must be stated |
| `user_private_low_risk` | `<e.g. 20 MB>` | keep most-recent N per account | no | must be stated |
| `user_generated_unsynced` | `<e.g. 50 MB>` | never silently deleted; surface to the user | **no** | must be stated |
| `analytics_outbox` | `<count and bytes>` | drop `priority: 'low'` above hardStop | low only | must be stated |
| `public_cache` (API responses) | `<e.g. 100 MB>` | LRU by `lastAccessedAt`, then TTL | yes | must be stated |
| offline media metadata | `<e.g. 5 MB>` | follows the asset | with the asset | must be stated |
| offline media assets | `<total bytes and asset count>` | user-initiated delete, or eviction | **no** — the user chose to download | must be stated |

Validation rules the reviewer checks, and the checker enforces:

1. **Every cap is a number with a unit.** "Reasonable" is not a cap.
2. **Every row has a cleanup rule.** A cap with no cleanup is a cap that is reached once and
   then blocks every subsequent write.
3. **`user_generated_unsynced` is never droppable.** If the feature needs it to be, it is not
   unsynced user work and it is classified wrongly.
4. **The sum of the caps does not exceed `hardStop`.** Otherwise one feature can exhaust the
   origin and evict another.
5. **Every row states the bound on the read that lists it** — `O(log n + k)` via an index, or a
   stated reason why `O(n)` is acceptable at this cap.

## Thresholds

| Key | Value | Notes |
|---|---:|---|
| `softStopUsageRatio` | `<default 0.85>` | stop optional prefetch and cache writes |
| `hardStopUsageRatio` | `<default 0.95>` | stop every write except user-generated unsynced work |
| `minFreeBytes` | `<default 50 MB>` | absolute floor, independent of the ratio |
| `cleanupBatchSize` | `<default 500>` | records per cleanup pass, yielding between passes |
| `writeChunkSize` | `<default 200>` | records per bulk-write transaction |

`examples/quota-manager.ts` reads these and validates them; `validateBudgetPolicy` rejects a
`hardStop` at or below `softStop`, and a ratio outside `(0, 1)`.

## What the user is told

| Situation | Copy |
|---|---|
| write succeeded | `<e.g. "Saved on this device">` |
| queued for sync | `<e.g. "Will sync when online">` |
| stored offline, persistence granted | `<e.g. "Available offline on this device">` |
| stored offline, best-effort | `<must include the removal sentence — references/70>` |
| quota exceeded on unsynced work | `<must name the cause and the remedy — references/31, class 1>` |
| asset evicted | `<must not say "error" — references/72>` |

## Eviction recovery

- What resyncs automatically: `<...>`
- What the user must redo: `<...>`
- What is lost with no recovery: `<...>` — if this row is non-empty, the ADR must say so explicitly.
