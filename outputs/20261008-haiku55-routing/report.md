# Claude model routing and verification consolidation

The final local update adds plan-first model selection to both orchestrators and automatic mechanical implementation profiles while preserving normal workhorse and exceptional routes. Claude Code 5.2.0 has 28 executable agents and 31 canonical profiles; Codex 5.2.0 has 27 agents and 30 profiles. Exact pins remain in the [Claude model policy](../../skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json) and [Codex model policy](../../skills/sohrab/alaa-prompting-guide/assets/codex-model-policy.json).

## Plan-first model selection

For Claude Code, select directly among Sonnet medium/high for settled implementation and Opus medium/high for increasing unresolved judgment; no trial ladder is required. Haiku 5.5 medium is also eligible for automatic mechanical work, alongside its bounded lighter roles. Haiku 4.5 is forbidden as an active model, and unavailable profiles fail closed. Fable 5.1 remains exceptional, requiring recorded applicable Opus-high inadequacy after context, specification, tools, and decomposition are addressed, or explicit lane selection.

For Codex, Sol medium/high remains the direct workhorse route; Luna medium is now automatic for qualifying mechanical changes, with no separate lane-selection request. The automatic Luna and Haiku routes require a finite enumeration of existing files, settled design, no semantic discretion, an exact transformation, explicit exclusions, and cheap discriminating checks. File count alone is not a limit; any unmet predicate returns the work to the normal workhorse route. Astra remains exceptional for documented Sol-high inadequacy or explicit selection. Planning uses a strong workhorse at medium/high for the uncertainty it must resolve; planner effort does not carry into implementation. No local model calibration or speed claim is made.

## Verification behavior

Both orchestrators use one owned aggregate check inventory. A grouped check covers children only when scope, flags, and environment match; uncovered checks remain separate, and independent verification and review keep their authority. Re-run affected checks when inputs change. This consolidation does not guarantee faster runs.

## Role migration and limits

The Opus implementation role remains active; `alaa-implementer-fable` is a separate exceptional route. The archived Opus-named role file is historical evidence, not a role to retire. No installation, commit, publication, live model run, account/access check, benchmark, or deployment occurred. Availability and calibration were not tested live.

## Completion states

- `IMPLEMENTED`: PASS; source changes and the required local checks are recorded.
- `MERGE_CANDIDATE`: PASS; the reviewed, frozen candidate is verified locally. No merge was requested.
- `RELEASE_CANDIDATE`: NOT REQUESTED.
- `PUBLISHED`: NOT REQUESTED.

The release review is `READY-WITH-CONDITIONS`; future activation still requires authorization and target control, version, mapping, and loaded-role checks. Correctness and instruction review approved the 23 static cases; bounded repair was approved. Fourteen affected checks passed, with prior unchanged checks retained. The source snapshot remained unchanged at `0f1196eb1124212d4f9c39b2465b3676043ec35e67b15a29aa041a7d7ce85e12` (2,173 files). No installation, commit, or live calibration occurred. See the [Phase 7 coverage summary](verification/phase7-finalcoverage-summary.json), [plan-first cases](plan-first-routing-cases.md), [independent review](review.md), [implementation record](implementation.md), [source evidence](source-evidence.md), [plan](docs/_agent_plans/20261008-140000_haiku55-routing.md), and [checkpoint](docs/agents/20261008-140000_haiku55-routing-state.md).

## Reusable context

The verification-consolidation rule is now in its canonical paired gate policy, and source capability facts are in the prompting guide. No additional reusable-memory candidate was admitted; no memory write was requested or made.
