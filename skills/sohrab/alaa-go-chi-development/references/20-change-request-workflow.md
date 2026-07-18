# Change Requests and Baseline Proposals

Two document types carry every consumer→kit need. They are the **only** channel: a consumer never edits the kit,
and the kit owner never acts on verbal/chat-only requests — if it isn't a file, it didn't happen. Each document must
be fully self-contained: the reader has none of your session context.

## Which document type?

| Situation | Document | Template |
|---|---|---|
| A kit-owned surface has a bug, limitation, missing option, or behavior you need changed/extended | **Kit change request** | `assets/templates/kit-change-request.md` |
| New behavior that is platform-shaped or could serve ≥2 consumers | **Baseline proposal** | `assets/templates/baseline-proposal.md` |

Unsure? If the surface already exists in the kit → change request. If you would be creating something new →
baseline proposal.

## Non-negotiable rules

1. **One file per independently decidable topic.** Never batch needs — the kit owner must be able to accept one and
   reject another. Truly inseparable needs cross-link each other explicitly.
2. **Timestamped name:** `YYYY-MM-DD-<kebab-slug>.md`, date = real authoring date from the environment, never
   invented. Example: `2026-07-18-baseline-rediskit.md`.
3. **Location.** During active consumer work: `<consumer-repo>/docs/kit-change-requests/` (the kit owner archives a
   copy on intake). Design-phase, audit-originated, or kit-first-phase requests: directly in the kit repo under
   `docs/change-requests/`. Creating a request document is never a kit change.
4. **Evidence, not opinion.** Every claim about current kit behavior cites a kit file path/symbol, a test name, or a
   command you ran with its output, against a named `kit_version_observed`. Every claim about your need cites your
   architecture doc section or code path. Mark anything unverified `NEEDS_CONFIRMATION` — an invented "the kit
   currently does X" poisons the owner's analysis.
5. **Propose a contract, not a patch.** State the shape you need (signature, behavior, env key + default, DDL, error
   code, metric) precisely enough to be contracttest-able, plus the backward-compatibility boundary. The kit owner
   designs the implementation with whole-platform visibility you don't have.
6. **Cover operations.** Address security/privacy, idempotency/data consistency, concurrency/resources,
   observability/cardinality, migration/rollback, and testability — or state n/a explicitly.
7. **Declare blast radius honestly** (phase-aware — see below). Never assert "breaks nobody" without basis.
8. **Severity is operational:** `blocking` (a committed feature cannot ship; includes a kit minor breaking
   contracttest) / `high` (shippable behind a risky or duplicating KIT-WRAP) / `normal` (can wait a release).
9. **File the same day** you discover the need — especially when you also write a `KIT-WRAP`. A wrap without a filed
   document is a silent fork.
10. **Search first.** Check the kit's `docs/change-requests/` for a prior request or recorded (possibly negative)
    decision on the same topic; re-opening a settled decision requires new evidence.

## Phase-aware impact

During `KIT_FIRST_STABILIZATION`: do not inspect consumers or claim `none`/`additive`/`action-required`; the
decision records every registered consumer as `NOT_ASSESSED_KIT_FIRST`, and historical requesting-service context
creates no execution scope. After explicit reactivation: the kit owner surveys the live registry prospectively and
records verified per-consumer impact; inaccessible evidence is `NEEDS_CONFIRMATION`, never guessed.

## Lifecycle

The original request is permanent — decisions are appended, never replace it:

`filed/proposed → under-review → accepted | accepted-amended | rejected | deferred → implemented → shipped`

During kit-first, accepted work may sit at `implemented-unreleased` with `shipped_in: pending` until a real tag
exists. Implementation always moves code, tests, `CONTRACTS.md`, generated artifacts, docs/runbook, classification,
and the decision record together.

## What happens next (set expectations correctly)

The kit owner will verify your evidence against kit code, apply the phase gate (survey consumers only when
reactivated), classify per `GOVERNANCE.md`, and accept/amend/reject/defer with an appended decision block. If the
change ships and propagation is active, you receive an update prompt; your job afterward is to upgrade per
[15-debug-upgrade-migrate](15-debug-upgrade-migrate.md) and delete the corresponding `KIT-WRAP`.

## Quality bar (self-review before handing over)

- Could an agent with zero context on your service decide and implement from this file alone?
- Does every "currently" statement carry a path/test/command citation and the observed kit version?
- Is the requested contract precise enough to be contracttest-able, with its compatibility boundary stated?
- Are operations (security, idempotency, concurrency, observability, rollback) addressed or explicitly n/a?
- Did you search existing requests/decisions first?
