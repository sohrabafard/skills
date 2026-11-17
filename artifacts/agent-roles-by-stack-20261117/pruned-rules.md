# Pruned and changed rules (2026-11-17)

Each row is a rule that this change removed, merged or deliberately changed in the two orchestrator packs. To restore one, copy the old text from the retired file or from commit `e0e1adc2`. The specialist lanes keep their own rows in `ledger-a.md`, `ledger-b.md` and `ledger-c.md` beside this file.

## Every managed definition

| Old text | Change | Reason | Where the behaviour lives now |
|---|---|---|---|
| "Report metadata after the first line: AGENT; CONFIGURED (definition), REQUESTED (dispatch) and OBSERVED model/effort. ... Flag an observable mismatch." | Removed | Owner direction. The lead never branched on these lines and holds the same facts in its dispatch | The lead's roster, from its allocation record (`SKILL.md` *Final report*) |
| "an omitted field is not a block: report it as omitted under REQUESTED" | "an omitted field is not a block" kept; the report half removed | No report line exists any more | Same sentence |
| "block this lane: report it and stop", with its three causes | Kept verbatim | Feeds `STATUS: BLOCKED` | `Task controls:` |
| "Runtime: a read-only role uses Bash only to inspect and to run authorized checks." and "A read-only role stays read-only even where a tool can write." | Merged into one sentence, for read-only roles only | Stated three to four times per file | Last sentence of `Effective authority:` |
| The same two sentences in write-capable roles (implementation contract, documenter, verifier, browser-qa, performance-profiler) | Removed | They address a read-only role | The role's own authority list |

## Implementation contract

| Old text | Change | Reason | Where the behaviour lives now |
|---|---|---|---|
| Output item "3. Skills: each skill you loaded before the first edit, and each required skill you loaded late or not at all" | Removed; the residual-risks item now names each required skill the lane did not load. A skill loaded late is no longer reported | Owner direction. Nothing consumed the list of loaded skills | Output item 6 |
| "Engineering baseline": the PHP, Vue, Go, infrastructure and Ala-style skill lists | Removed | A lane of one stack carried every other stack's list | The stack binding of each role; the dispatch `<skills>` for the generic role and for an incidental file |
| "Ala-style repository, whatever the language: also /alaa-services-contract ... and /alaa-trust-gateway-auth" | Go and Laravel roles apply both, preloaded. Frontend and HAProxy load each by a stated condition. Delivery preloads the contract skill only. The generic role loads what the dispatch names | Owner-approved preload rule; see the report for the trade-off | Stack bindings |
| "When none is recorded or one does not hold, read your profile's section in `routing-matrix.md`." | Removed | The lead records the predicates in the dispatch; the read cost every lane a start-up search | `references/delegation-prompts/30-implementation.md` |
| "Never upgrade your own profile." | Removed | A lane cannot change its role, model or effort | None: no behaviour |
| Design method: "Where the lane touches them, reason about trust boundaries, consistency, idempotency, concurrency and races, partial failure, retry semantics, data loss, degraded dependencies and observability." | Removed | A generic concern list with no threshold or stop condition; the stack and contract skills state the concrete rules | The role's skills |
| Design method: "operability" in the list of what the design keeps | Removed with the list above | Same | Same |
| "After editing, inspect the full diff and its callers." | Kept, moved into the "Finish the lane" execution rule. It now binds every lane, not only a lane that settles a design decision | One rule about finishing | Execution rules |
| "Start no subagent: the lead owns every dispatch." (Claude contract) | Removed; "Return work that needs another lane to the lead." kept | The tool list denies the spawn | Frontmatter `disallowedTools` |
| Binding ending: "load its owner from the Engineering baseline below first" | "load the skill the dispatch names for it first" | The baseline is gone | The dispatch |
| Go binding: "This condition narrows the Go line of the Engineering baseline below." | Removed | The line it narrowed is gone | None: no behaviour |
| Infrastructure binding: Ansible, standalone Makefile and shell owners | Moved to the lead | These lanes run on the generic role | `references/routing-matrix.md` *Stack-bound roles* |
| Infrastructure binding: "Change a generated file only through its owner source", "Prove the change with the supplied render, diff, lint or dry-run commands, and never apply it to a running environment", and the unlisted-surface rule | Moved into the shared contract after the review | Lanes on the generic role lost them with the binding | Execution rules, for every implementation lane |

## Routing

| Old text | Change | Reason | Where the behaviour lives now |
|---|---|---|---|
| One role identity for each fit row (the mechanical, bounded, workhorse and exceptional identities) | Removed | The fit table already selects the pair; the identity selected nothing | Fit table |
| "The lane is not admitted to the mechanical or the bounded semantic branch" as a condition of a stack-bound role | Removed | Every fit row now runs on the role of its stack | *Stack-bound roles* |
| "Use `alaa-planner-high` when forming the plan requires resolving interacting uncertainties." | Replaced: such a plan selects a later fit row on `alaa-planner` | One planner body | *Planning profile selection* |
| Codex: "`alaa-reviewer` or the compatible `alaa-reviewer-deep` identity" | One reviewer; the fit table selects the pair of a deep review | One reviewer body | *Correctness review depth* |

## Kept on purpose

- Every `Verification:` rule of the implementation contract. The checkers pin them, and they state the owner's rule against repeated broad checks.
- The `Task tracking:` block and the `Output rule:`. Both landed on 2026-11-17 by owner decision.
- "An exceptional-model admission comes only from the lead's recorded task allocation."

## Lead corrections to the lane ledgers

- `ledger-b.md`: the test strategist row for "Map every acceptance criterion to at least one observable check" is void. The lead restored the bullet.
- `ledger-c.md`: the observability row for "dashboards" and "runbooks" is void. The lead restored both words.
- `ledger-c.md`: the verifier pair is unchanged by its lane, but it lost its two misaddressed read-only sentences in the shared-block step above.
- `ledger-b.md`: the researcher sentence "deepen only where evidence changes the answer" bounded search depth; its row calls it no behaviour. It stays removed.
