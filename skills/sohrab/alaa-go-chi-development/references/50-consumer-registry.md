# Consumer Registry — `docs/CONSUMERS.md` in the Kit Repository

The registry is the single inventory of every service built on (or migrating to) the kit, and the iteration set
for kit impact analysis, propagation, and platform audits. A service missing from it gets no impact analysis, no
propagation prompt, and no audit coverage — it will be broken silently by the first incompatible kit change.
Registration is a law, not a courtesy. The registry records inventory; it is **not** execution authority by itself
— the active phase ([05](05-phase-and-source-truth.md)) decides what may be done with a row.

## Where and who may edit

- File: `docs/CONSUMERS.md` in the **alaa-go-chi repository**. If absent, the first registering agent creates it
  from `assets/templates/consumers-registry.md`.
- This is the only kit-repo file a consumer agent may edit, and only its **own** row. Registration is explicitly
  not a kit change: no `CONTRACTS.md` entry, no version bump, no owner review.
- Never delete another service's row — mark it `retired`. Rows are current-state; history lives in git.

## Row contract

| Field | Meaning |
|---|---|
| `service` | canonical service name (`news`, `notif`, `entitlement-api`, `tusd`, `wa-api`, …) |
| `status` | `planned` → `bootstrapping` → `active`; migrations: `planned-migration` → `migrating` → `active`; also `paused`, `retired` |
| `repo` | repo path/URL an agent can use to locate the code |
| `kit_version` | the `git.alaatv.com/vk/alaa-go-chi` version pinned in `go.mod` (`—` until first pin) |
| `contracttest` | `passing` / `failing` / `local_ci_smoke_passed; runner_contract_pending` / `not-wired` / `not-current` |
| `surfaces` | kit packages the service actually consumes — honest, not aspirational |
| `agent_notes` | one line: architecture doc pointer, migration inventory, or standing caveat |
| `registered` / `updated` | dates (`YYYY-MM-DD`) |

## During KIT_FIRST_STABILIZATION

- Every row stays `paused`/inventory-only; `contracttest` evidence is `not-current`; notes carry exactly
  `NOT_ASSESSED_KIT_FIRST` and the do-not-inspect/propagate marker.
- Do not open a consumer repo to refresh version, surfaces, or status; historical values remain, clearly marked
  non-current.
- Adding a newly discovered row is allowed only from already-authorized kit-side evidence — do not inspect the
  consumer to fill fields; use `NEEDS_CONFIRMATION`.

## After explicit reactivation

- **Register** in the first session that builds or migrates a service on the kit — before writing service code.
- **Update your own row** in the same session as every kit-version bump, status transition, or contracttest state
  change, from verified live evidence only. A registry that lags reality misleads the owner's impact survey —
  worse than no data, because it looks like data.
- **Kit owner / auditor**: correct rows proven stale; add `NEEDS_CONFIRMATION`-flagged rows for discovered
  unregistered consumers.

Registry changes never replace change requests, compatibility analysis, or release evidence.
