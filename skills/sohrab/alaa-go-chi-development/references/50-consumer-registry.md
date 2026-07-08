# Registry — `docs/CONSUMERS.md` in the alaa-go-chi Repository

The consumer registry is the single list of every service built on (or migrating to) the kit. It is the
iteration set for kit impact analysis (mode K) and platform audits (mode A): a service missing from this file
gets no impact analysis, no propagation prompt, and no audit coverage — it will be broken silently by the first
incompatible kit change. That is why registration is a **law**, not a courtesy.

## Where and what

- File: `docs/CONSUMERS.md` in the **alaa-go-chi repository** (not in the consumer repo).
- If the file does not exist yet, the first registering agent creates it from
  `assets/templates/consumers-registry.md`.
- This is the **only file in the kit repo a consumer agent may edit**. Registration is explicitly *not* a kit
  change: no `CONTRACTS.md` entry, no version bump, no kit-owner review needed. Everything else in the kit repo
  still requires the mode CR document channel.

## Row contract

One row per service:

| Field | Meaning |
|---|---|
| `service` | canonical service name (`news`, `notif`, `entitlement-api`, `tusd`, …) |
| `status` | `planned` → `bootstrapping` → `migrating` (existing services) → `active`; also `paused`, `retired` |
| `repo` | repo path/URL an agent can use to locate the code |
| `kit_version` | the `git.alaatv.com/vk/alaa-go-chi` version pinned in `go.mod` (`—` until first pin) |
| `contracttest` | `passing` / `failing` / `local_ci_smoke_passed; runner_contract_pending` / `not-wired` |
| `surfaces` | kit packages the service actually consumes (helps blast-radius triage; keep honest, not aspirational) |
| `agent_notes` | one line: pointer to architecture doc, migration inventory, or standing caveat |
| `registered` / `updated` | dates (`YYYY-MM-DD`) |

## When to touch it

- **Register** (add row): in the first session that builds or migrates a service on the kit — before writing
  service code, per `references/10-consumer-development.md` §0.
- **Update your own row**: on every kit version bump, status transition, or contracttest state change. Do it in
  the same session as the change it records; a registry that lags reality misleads the kit owner's impact
  survey, which is worse than no data because it looks like data.
- **Kit owner / auditor**: correct any row proven stale, and add `NEEDS_CONFIRMATION`-flagged rows for
  discovered unregistered consumers.

Keep edits append/update-only — never delete another service's row (mark `retired` instead), and never rewrite
history: the registry is current-state, and history lives in git.
