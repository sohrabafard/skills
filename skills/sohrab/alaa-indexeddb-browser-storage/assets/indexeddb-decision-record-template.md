# IndexedDB decision record — <feature>

Date: `<ISO date>` · Owner: `<name>` · Status: `proposed | accepted | rejected | superseded`

Every `<...>` is filled before review. A blank row is a finding, not a default.

## Context and decision

- What the user can do that they could not before: `<...>`
- What is stored on the device, in one sentence: `<...>`
- Decision: `<...>`

## Data classification

Classes come from `assets/data-classification-policy.yaml`, not from prose.

| Field or record | Class | Source of truth | Lifetime | Recoverable from the server? |
|---|---|---|---|---|
| `<...>` | `<...>` | `<...>` | `<...>` | `<yes / no — if no, name the user-visible recovery>` |

Answered explicitly:

- Any secret, token, decoded JWT claim, trusted gateway header, permission bitmap or
  authorization decision stored? **`<must be: no>`** — `references/61-authority-boundary.md`.
- Does anything branch on a stored value to decide what a user may do? **`<must be: no>`** — if yes,
  that is an authorization decision: `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).
- Any `pii_moderate_high` field stored? `<if yes, name the review under /alaa-security-review
  ($alaa-security-review) and its outcome>`
- Any user-entered text stored or compared? `<if yes, name where it is normalized —
  /alaa-input-normalization ($alaa-input-normalization)>`

## Capability tiers

| Tier | What this feature does | What the user is told |
|---|---|---|
| 0 | `<...>` | `<no offline language>` |
| 1 | `<...>` | `<...>` |
| 2 | `<...>` | `<...>` |
| 3 | `<...>` | `<...>` |

## Schema

- Database and version: `<registered name>` — names are `/alaa-services-contract`
  (`$alaa-services-contract`)
- Object stores: `<...>`

| Index | Key path | The read it serves | Stated bound |
|---|---|---|---|
| `<...>` | `<...>` | `<...>` | `<O(log n + k) / ...>` |

- Every key-path segment verified against the record type: `<yes — name the type>`
- Every user-scoped store has an `accountKey`-prefixed index: `<yes>`
- Record types: `<...>`

## Quota, budget and eviction

- Budget file: `<path to the filled storage-budget-policy.md>`
- Estimated records and bytes per account after one year: `<...>`
- Cleanup order when the cap is reached: `<...>`
- When persistence is requested, and what the UI says when it is refused: `<...>`
- What the user sees the moment the browser deletes the whole origin: `<...>`

## Migration and concurrency

- New database version and the branch added: `<...>`
- Upgrade path from the oldest supported version: `<...>`
- What a second open tab sees, and the blocked UX: `<...>`
- Does the service worker touch these stores? `<if yes, it opens with no version argument —
  references/41-multitab-versionchange-and-locks.md>`
- Cross-context jobs and the Web Lock name each holds: `<...>`

## Failure classes

| Class | What this feature does | What the user sees |
|---|---|---|
| quota exceeded | `<...>` | `<...>` |
| origin evicted | `<...>` | `<...>` |
| upgrade blocked | `<...>` | `<...>` |
| transaction aborted | `<...>` | `<...>` |
| storage unavailable, private mode | `<...>` | `<...>` |

## Proof

Levels are `/alaa-testing-strategy` (`$alaa-testing-strategy`); lanes are
`assets/browser-test-matrix.yaml`.

| Level | Test | What it does not bound |
|---|---|---|
| 2 | `<...>` | any real engine |
| 4 | `<...>` | `<...>` |
| 5 | `<lane>` | anything beyond that device |

## Telemetry

Event names are `/alaa-services-contract` (`$alaa-services-contract`); requirement levels and
gates are `/alaa-observability-soc` (`$alaa-observability-soc`).

| Event | Registered? | Level | Fields, all bucketed and payload-free |
|---|---|---|---|
| `<...>` | `<yes>` | `<...>` | `<...>` |

## Consequences and open decisions
