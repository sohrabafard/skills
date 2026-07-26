# Consumer Registry — `docs/CONSUMERS.md` in the Kit Repository

The registry is the single inventory of every service built on, or migrating to, the kit, and the iteration set
for impact analysis, propagation, and audits. A service missing from it gets no impact analysis, no propagation
prompt, and no audit coverage, and will be broken silently by the first incompatible kit change. Registration is
a law, not a courtesy.

The registry records inventory. It is **not** execution authority: a row never grants permission to open, edit,
validate, or prompt the repository it names. Only the capability matrix in
[05-phase-and-source-truth](05-phase-and-source-truth.md) decides that, and it decides it independently of what
any row says.

**Capability required: none to write your own row; `consumer-repo-read` to refresh a row from live evidence.**

## Where and who may edit

- The file is `docs/CONSUMERS.md` in the **alaa-go-chi repository**. If it is absent, the first registering agent
  creates it from `assets/templates/consumers-registry.md`.
- This is the only kit-repo file a consumer agent may edit, and only its **own** row. Registration is explicitly
  not a kit change: no `CONTRACTS.md` entry, no version bump, no owner review.
- Never delete another service's row — mark it `retired`. Rows are current state; history lives in git.

## Row contract

| Field | Meaning |
|---|---|
| `service` | canonical service name |
| `status` | `planned` → `bootstrapping` → `active`; migrations: `planned-migration` → `migrating` → `active`; also `paused`, `retired` |
| `repo` | a repository path or URL an agent can use to locate the code |
| `kit_version` | the `git.alaatv.com/vk/alaa-go-chi` version pinned in `go.mod`, or `—` until the first pin |
| `contracttest` | `passing` / `failing` / `local_ci_smoke_passed; runner_contract_pending` / `not-wired` / `not-current` |
| `surfaces` | the kit packages the service actually consumes — honest, not aspirational |
| `agent_notes` | one line: architecture-doc pointer, migration inventory, or a standing caveat |
| `registered` / `updated` | dates, `YYYY-MM-DD` |

## Keeping rows honest under a phase that blocks inspection

When the `consumer-repo-read` cell does not allow you to open a consumer, a row's `kit_version`, `contracttest`,
`surfaces`, and `status` are **historical values that were true when last verified**. Do not refresh them, do not
delete them, and do not silently treat them as current: the `contracttest` column carries `not-current`, or its
last-verified date, so a reader can tell evidence from memory. Every `agent_notes` entry carries the marker
string the active scope record prescribes.

Adding a newly discovered row in that state is allowed only from evidence already in the kit repository; fill
what you cannot verify with `NEEDS_CONFIRMATION` rather than inspecting the consumer.

A row whose `status` claims more than its `contracttest` evidence supports is a finding for `40-` — a registry
that lags reality misleads the owner's impact survey, and is worse than no data because it looks like data.

## When inspection is allowed

- **Register** in the first session that builds or migrates a service on the kit, before writing service code.
- **Update your own row** in the same session as every kit-version bump, status transition, or `contracttest`
  state change, from verified live evidence only.
- **Kit owner and auditor:** correct rows the evidence proves stale, and add `NEEDS_CONFIRMATION`-flagged rows
  for discovered unregistered consumers.

A registry change never replaces a change request, a compatibility analysis, or release evidence.
