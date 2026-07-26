# Change Requests and Baseline Proposals

Two document types carry every consumer-to-kit need, and they are the **only** channel: a consumer never edits
the kit, and the kit owner never acts on a verbal or chat-only request. If it is not a file, it did not happen.
Each document is fully self-contained — the reader has none of your session context.

**Capability required: none.** Writing a request document is permitted in every phase, because it changes no
consumer and no kit surface. Filling its impact section is `consumer-impact-claim` and its filing location can be
a consumer repository; check those cells in the matrix in [05-phase-and-source-truth](05-phase-and-source-truth.md).

## Which document type

| Situation | Document | Template |
|---|---|---|
| A kit-owned surface has a bug, a limitation, a missing option, or behaviour you need changed | **Kit change request** | `assets/templates/kit-change-request.md` |
| New behaviour that is platform-shaped, or that a second service would need unchanged | **Baseline proposal** | `assets/templates/baseline-proposal.md` |

Unsure? The surface already exists in the kit → change request. You would be creating something new → baseline
proposal.

## Non-negotiable rules

1. **One file per independently decidable topic.** Never batch needs: the owner must be able to accept one and
   reject another. Needs that genuinely cannot be separated cross-link each other explicitly.
2. **Timestamped name** `YYYY-MM-DD-<kebab-slug>.md`, where the date is the real authoring date read from the
   environment and never invented. Example: `2026-07-18-baseline-rediskit.md`.
3. **Location.** When the `consumer-repo-write` cell allows it: `<consumer-repo>/docs/kit-change-requests/`, and
   the kit owner archives a copy on intake. Otherwise — design-phase, audit-originated, or written from a kit
   session — directly in the kit repository under `docs/change-requests/`. Creating a request document is never
   itself a kit change.
4. **Evidence, not opinion.** Every claim about current kit behaviour cites a kit `file:line` or symbol, a test
   name, or a command you ran with its output, against a named `kit_version_observed`. Every claim about your
   need cites your architecture document section or code path. Mark anything unverified `NEEDS_CONFIRMATION`; an
   invented "the kit currently does X" poisons the owner's analysis.
5. **Propose a contract, not a patch.** State the shape you need — signature, behaviour, env key and default,
   DDL, error code, metric — precisely enough to be `contracttest`-able, plus the backward-compatibility
   boundary. The owner designs the implementation with whole-platform visibility you do not have.
6. **Cover operations:** security and privacy, idempotency and data consistency, concurrency and resources,
   observability and cardinality, migration and rollback, and testability — or state `n/a` explicitly for each.
7. **Declare blast radius honestly**, within what the `consumer-impact-claim` cell allows. Never assert "breaks
   nobody" without a basis you can name.
8. **Severity is operational:** `blocking` — a committed feature cannot ship, which includes a kit minor breaking
   `contracttest`; `high` — shippable only behind a wrap or a duplication; `normal` — can wait a release.
9. **File the same day** you discover the need, and always the same day you write a `KIT-WRAP`.
10. **Search first.** Check `docs/change-requests/` for a prior request or a recorded decision, including a
    negative one, on the same topic. Re-opening a settled decision requires new evidence, named.

## Lifecycle

The original request is permanent; decisions are appended and never replace it.

`filed/proposed → under-review → accepted | accepted-amended | rejected | deferred → implemented → shipped`

Accepted work may sit at `implemented-unreleased` with `shipped_in: pending` until a real tag exists.
Implementation always moves code, tests, `CONTRACTS.md`, generated artifacts, docs and runbook, classification,
and the decision record together.

## What happens next

The kit owner verifies your evidence against kit code, applies the phase gate, classifies per `GOVERNANCE.md`,
and appends an accept, amend, reject, or defer decision block. If the change ships and the `propagation` cell
allows it, you receive an update prompt; your job afterwards is to upgrade per
[15-debug-upgrade-migrate](15-debug-upgrade-migrate.md) and delete the corresponding `KIT-WRAP`.

## Self-review before handing over

- Could an agent with zero context on your service decide and implement from this file alone?
- Does every "currently" statement carry a path, test, or command citation and the observed kit version?
- Is the requested contract precise enough to be `contracttest`-able, with its compatibility boundary stated?
- Are security, idempotency, concurrency, observability, and rollback each addressed or explicitly `n/a`?
- Did you search the existing requests and decisions first?
