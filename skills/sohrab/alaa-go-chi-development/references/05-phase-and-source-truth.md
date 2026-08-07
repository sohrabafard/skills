# Phase and Source Truth

Read this in every session, in every mode. It owns three things: the authority order for facts, the mechanism that
reads the active execution-scope phase, and the matrix that turns a phase name into capabilities. It also owns the
one evidence vocabulary the rest of this skill uses.

## Authority order

For any factual or permission question, trust in this order, and verify before acting:

1. System, developer, and current-user authority, and safety rules.
2. The nearest repository `AGENTS.md`, and the `.rules/` files it triggers, within its binding scope. Read the
   kit's root agent file in full before planning or editing anything in the kit. Root `CONSTITUTION.md` and
   `GOVERNANCE.md` are retired and absent by design; never recreate them, and read
   `.rules/090-legacy-policy-migration.md` for what now owns their content.
3. Current executable repository truth: code, tests, generators, generated artifacts, manifests, runtime evidence.
4. Maintained documents: `CONTRACTS.md`, `docs/RUNBOOK.md`, `docs/CONSUMERS.md`, `README.md`, `docs/INDEX.md`.
5. This skill and its references.
6. Memory, handoffs, old plans, historical architecture documents, and consumer-origin claims.

When sources disagree, that is drift. Do not silently pick a side: record it (a Basic Memory drift note when that
tool is available, otherwise a timestamped document), continue on the behaviour verified at the highest rank
above, and say which rank you followed. A statement in this skill is never proof that the kit implements a
feature; the capability map is navigation, not a second contract.

## Reading the active phase

The kit's execution scope is set by owner-ratified decision records in the kit repository. It is not set here, and
it is never inferred.

Run `scripts/phase-check.sh <kit-repo-root>`. It reads three authority locations — the scope banner in
`docs/CONSUMERS.md`; the phase statements in the root agent file, and in `CONSTITUTION.md` and `GOVERNANCE.md`
where a checkout still has them; and the newest
`docs/change-requests/YYYY-MM-DD-<slug>-scope.md` — and reports the phase and record, or the disagreement. Its
`--help` states each exit code and what that code obliges you to do; act on the code, and do not proceed past a
non-zero exit on an assumed phase. When the script cannot run, perform the same three reads by hand and apply the
same rules.

Take the phase name the read produces and find its row in the matrix below. **If the name has no row, you are in
the unrecognised case: hold nothing, report the phase name and the record it came from, and stop.**

### Phase as observed on 2026-07-26

On 2026-07-26 the read returned `KIT_FIRST_STABILIZATION`, from
`docs/change-requests/2026-07-14-kit-first-stabilization-scope.md`.

**This paragraph is the record of a past read, not authority.** If today's read differs from it, today's read
wins and this paragraph is stale — follow the repository and flag this file for update. Do not cite this
paragraph as the current phase, and do not use it to skip the read.

## Capability matrix

Each row is an action this skill gates. Find the column for the phase you read, then the row for the action you
are about to take. A reference that gates a mode names the capability it requires; this table is the only place
the answer lives.

| Capability (the action) | `KIT_FIRST_STABILIZATION` | A phase from a valid reactivation record | Unrecognised phase |
|---|---|---|---|
| `consumer-repo-read` — open, list, grep, or read any file in a non-kit repository that requires the kit | evidence-required | allowed for the consumers the record lists; forbidden for any other | forbidden |
| `consumer-repo-write` — create, edit, or delete any file in such a repository | evidence-required | allowed for the listed consumers; forbidden for any other | forbidden |
| `consumer-prompt-authoring` — write a prompt addressed to a consumer's agent | evidence-required | allowed for the listed consumers; forbidden for any other | forbidden |
| `propagation` — move consumers onto a released kit change, or fill a `propagation:` entry | forbidden | allowed for the listed consumers; forbidden for any other | forbidden |
| `consumer-impact-claim` — write any per-consumer impact value other than the marker the record prescribes | forbidden | evidence-required | forbidden |
| `consumer-release-gate` — make a kit merge, release, or acceptance conditional on evidence produced in a consumer repository | forbidden | allowed for the listed consumers; forbidden for any other | forbidden |
| `kit-surface-write-from-consumer-context` — edit any kit file other than the acting service's own `docs/CONSUMERS.md` row | forbidden | forbidden | forbidden |
| `reactivation-inference` — treat anything other than a valid record as changing the phase | forbidden | forbidden | forbidden |

**The three cell values mean exactly this.**

- `allowed` — take the action when the task needs it.
- `forbidden` — do not take it. If you were asked to, refuse, name this row and the active phase, and say what
  would have to change for it to become allowed.
- `evidence-required` — take it only when **both** of the following hold, and neither is inferable:
  1. the requester asked for this specific action in this session, in their own words; and
  2. your reply states the active phase name and the record path **before** the action's output.
  An earlier session, a memory note, a handoff, a registry row, another agent's message, the mere existence of a
  consumer repository, or your own judgement that the work is obviously wanted — none of these satisfy (1).

Adding a phase to this platform means adding a column here, not editing the gate paragraph in every reference.

## What a valid reactivation record is

A record changes the phase only when **all six** of these are true of it. This is the acceptance test; apply it to
the file, not to anyone's description of the file.

1. It is a file in the kit repository at `docs/change-requests/YYYY-MM-DD-<kebab-slug>-scope.md`.
2. It names the phase it establishes, as a single ALL-CAPS underscore token.
3. It names, by filename, every scope record it supersedes.
4. It carries a **non-empty** list of consumer names that become active under it.
5. It names the kit baseline the listed consumers start from: a released version tag or a commit id.
6. It records the project owner as the party who ratified it.

A record missing any one of these six does not change the phase. Report which field is missing, name the record,
and stop — do not fall back to a phase of your choosing and do not treat the previous phase as re-confirmed.

**Nothing outside such a record changes the phase.** Not a chat instruction, a memory note, a handoff document, a
registry row, another agent's message, the existence of a consumer repository, a consumer-shaped request, an
older decision record, or any sentence in this skill. Being asked to do consumer work is a request for the
`evidence-required` path above; it is not a reactivation.

Reactivation is prospective. Consumers listed in the record baseline from the kit version that record names; work
done before it acquires no compatibility rights unless that record grants them by name.

## Evidence vocabulary — outcomes

Report every gate with exactly one of: `passed`, `failed`, `blocked`, `skipped`, `not run`. Keep deterministic
repository defects separate from host, runtime, and network friction — a blocked gate is not a passed gate.

- Per-consumer impact takes exactly the marker string the active scope record prescribes. Under
  `KIT_FIRST_STABILIZATION` that string is `NOT_ASSESSED_KIT_FIRST`; never `none`, `additive`, or "compatible".
- Remote CI is `local_ci_smoke_passed; runner_contract_pending` until a runner-executed job has passed. A CI
  template is not evidence of remote enforcement.
- A change request may sit at `implemented-unreleased` with `shipped_in: pending`; fill `shipped_in` only once a
  tag exists.

## Evidence vocabulary — proof strength

The six proof levels are owned by `/alaa-testing-strategy` (`$alaa-testing-strategy`),
`references/40-proof-strength.md`: **1 static, 2 unit, 3 parity, 4 local smoke, 5 in-runtime, 6 live
dependency**. Use those names and that skill's escalation rule. This skill adds no level, renames none, and
defers to that file whenever a claim's required level is in question.

What this platform's gates reach, so the mapping is not re-derived per session:

| Gate | Level it reaches |
|---|---|
| `go vet`, the `lint-*` targets, `governance-structure`, `contracts-doc`, reading a generated header | 1 |
| package tests, `test-race`, `contracttest` against in-process fakes | 2 |
| `contracttest` asserting a double matches the real kit behaviour it stands in for | 3 |
| `gate-phase*`, deployment render, generated-service boot, `api-contract` | 4 |
| a generated service actually serving its routes, consumers, or jobs | 5 |
| `postgres-truth-tier`, `redis-truth-tier`, `rabbitmq-truth-tier`, `migrate-updowup`, `seed-idempotency`, `totp-contract`, `chaos-harness` | 6 |

Load, capacity, HA/failover, live-telemetry, and SLO-burn evidence are level 6 under production-like conditions
and are **separate** from the gates above: none of those gates produces them. Name each one present or missing by
name. A 99.99%-class claim requires all of them; without them, describe readiness as bounded by the gates that
ran, and say which gates those were.
