# Mode CR — Change Requests and Baseline Proposals

Two document types carry every consumer→kit need. They are the *only* channel: a consumer never edits the kit,
and the kit owner never acts on verbal/chat-only requests — if it isn't a file, it didn't happen. The human
platform owner physically carries these files between agents, so each document must be **fully self-contained**:
the kit-owner agent reading it has none of your session context.

## Which document type?

| Situation | Document | Template |
|---|---|---|
| A kit-owned surface has a bug, a limitation, a missing option, a behavior you need changed or extended | **Kit change request** | `assets/templates/kit-change-request.md` |
| A feature/logic that does not exist in the kit but could serve ≥2 consumers (or is platform-shaped by nature) | **Baseline proposal** | `assets/templates/baseline-proposal.md` |

Unsure which? If the surface already exists in the kit → change request. If you would be creating something
new → baseline proposal.

## Non-negotiable rules for both types

1. **One file per feature/bug.** Never batch three needs into one document — the kit owner must be able to
   accept one and reject another independently. If two needs are truly inseparable, say so explicitly in both
   files with cross-links.
2. **Timestamped name:** `YYYY-MM-DD-<kebab-slug>.md`, date = authoring date (real date, from the environment,
   never invented). Examples: `2026-07-08-httpkit-webhook-raw-body-access.md`,
   `2026-07-09-shared-rate-limiter-baseline.md`.
3. **Location:** authored in the **consumer repo** under `docs/kit-change-requests/`. (The kit owner archives a
   copy with a decision in the kit repo — that half is the owner's job, `references/30-*`.) Two exceptions:
   if the consumer repo does not exist yet (design-phase work from an architecture doc), or the document
   originates from a platform audit, author it directly in the kit repo under `docs/change-requests/` with
   `requesting_service` naming the (future) service — this matches the kit's existing advisory-note convention
   and is not a violation of law 1, because it creates a request document, not a kit change.
4. **Evidence, not opinion.** Every claim about current kit behavior cites a kit file path (and line/symbol when
   useful) or a failing test/command output. Every claim about your need cites your service's architecture doc
   section or code path. Anything you could not verify is marked `NEEDS_CONFIRMATION` — an invented "the kit
   currently does X" poisons the kit owner's analysis.
5. **No pre-written kit patches.** Propose the *contract* you need (signature, behavior, config key, DDL), not a
   diff of kit internals. The kit owner designs the implementation with whole-platform visibility you don't have.
6. **Declare blast radius honestly.** State what you know about other consumers' exposure (from `CONSUMERS.md`
   and public docs) and mark the rest `unknown` — never assert "this breaks nobody" without basis.
7. **Severity is operational, not emotional:**
   - `blocking` — your service cannot ship a committed feature without it (includes: a kit minor broke contracttest).
   - `high` — shippable with a KIT-WRAP, but the wrap is risky or duplicates logic.
   - `normal` — improvement; you can wait a release.
8. **File it the same day** you discover the need — especially when you also write a `KIT-WRAP`. A wrap without
   a filed document is a silent fork, the exact failure mode this platform refuses.

## What happens next (so you set expectations correctly)

The kit owner will: verify your evidence against kit code, survey **all** registered consumers for impact,
classify the change per `GOVERNANCE.md` (patch/minor/major/deprecation), and either implement it (updating
`CONTRACTS.md` + docs + contracttest in the same change), amend it (you get a decision note explaining what
changed and why), or reject it with reasons. If the change is breaking-but-necessary, the owner also prepares
update prompts for every affected consumer. Your job afterward: consume the new version per
`references/10-consumer-development.md` §5 and delete the corresponding `KIT-WRAP`.

## Quality bar (self-review before handing the file over)

- Could an agent with zero context on your service implement/decide from this file alone?
- Does every "currently" statement have a path/test citation?
- Is the requested contract stated precisely enough to be contracttest-able?
- Did you check the kit's existing `docs/` for a prior request/decision on the same topic (search first —
  duplicate requests waste the owner's cycle)?
- Run-twice/idempotency, observability, and security implications addressed (or explicitly n/a)?
