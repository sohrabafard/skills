# Stack-bound implementation roles from session evidence (2026-11-14)

Fourth engagement of the day on the orchestrator pair, after the [Fable 5.2 pack upgrade](../skill-pack-fable52-20261114/report.md), the [clarity rewrite](../skill-pack-clarity-20261114/report.md) and the [wording pass](../skill-pack-wording-20261114/report.md). Beads plan: `alaa-4x638`. This record is dated evidence; verify current repository facts before reusing a conclusion.

## Request

The pack owner asked whether more specialist agents would let the orchestrator work more precisely, gave a per-language or per-stack implementer as an example, and asked for whatever else one week of Claude Code and Codex sessions shows.

## Outcome

Both orchestrators are at pack version 5.7.0 with four new roles: `alaa-implementer-laravel`, `alaa-implementer-frontend`, `alaa-implementer-go` and `alaa-implementer-infra`. Each is generated from the shared implementation contract plus one stack binding. In Claude Code the role preloads the owning skills of its stack; in Codex, which has no preload, the role's instructions load them before the first edit. Both name the reads each surface triggers. The roles select neither model nor effort.

No other role was added. The evidence did not support one.

## Evidence and what it decided

The counts are in [evidence.md](evidence.md).

| Finding | Decision |
|---|---|
| Implementation lanes loaded the skill that owns their stack in a minority of cases: Vue 10 of 55 and 3 of 10, infrastructure 4 of 18, PHP 60 of 103 and 5 of 11 | Stack-bound roles for Laravel, frontend and infrastructure |
| A skill named as a call was loaded far more often than one named as a bare mention | The dispatch template writes each skill binding as a call |
| The implementation contract had no infrastructure line | One baseline line, and the infrastructure role's surface-to-owner list |
| Contract artifacts out of step with code in 12 of 120 classified non-pass results | A contract rule to list stale derived artifacts; the Laravel binding loads the contract-pack and Postman skills on a public-surface change |
| Lanes chased failures that predated them, or needed a test outside their scope | A `<baseline_failures>` dispatch field; the scope field names covering test files |
| Generic agents inside orchestrated runs: 7 of 221 | No routing change; role selection already works |
| Go: 4 dispatches in the week | See the next section |

### Roles that rest on thin evidence

- **Go.** Four Go dispatches in the week cannot show a gap. The role exists because the owner named per-language implementers, Go is one of the three stacks the contract already names, and without it a Go lane would be the only single-stack lane left on the generic role. Its cost is one wrapper entry per runtime.
- **Infrastructure in Codex.** Unknown: six of seven Codex infrastructure lanes have no transcript. The role rests on the Claude Code numbers and on the missing contract line.

### Considered and not added

- **A contract-artifact sync role.** The existing API contract reviewer and documenter cover the surface; the gap was that lanes did not report stale artifacts. A contract line fixes that.
- **An environment preflight role.** The failure analyst owns this; the dispatch now carries baseline failures.
- **Stack-bound reviewers.** No evidence. `alaa-reviewer` already preloads the three clean-code skills.
- **One role per stack and model.** Rejected by design: a role name selects no model, so the stack axis stays separate from the task pair.

## Design

- **One mechanism.** `assets/profile-wrappers.json` entries may carry a `binding` paragraph. `alaa-prompting-guide/scripts/profile_projection.py` inserts it before the contract's `Engineering baseline:` line. The contract stays single; an entry without a binding renders unchanged.
- **Admission.** `references/routing-matrix.md` *Stack-bound roles* admits a role when every owned file belongs to one stack family, apart from incidental files the lane record lists by path, and the lane is outside the mechanical and bounded branches. For such a lane the role replaces the generic workhorse identities.
- **Fallback.** A session started before the roles were installed does not have them. The orchestrator then records and dispatches the generic role and names the stack's skills as calls. The repository is a live symlinked install, so this text landed in the same commit as the role definitions.
- **Preload cost.** A stack-bound Claude Code role preloads six or seven skills. The largest lists carry about 78 KB of skill text. The week's median implementation lane read several million input tokens, so the preload is small beside it.

## Review outcome

| Review | Verdict | Findings | Disposition |
|---|---|---|---|
| Code (`alaa-reviewer`) | APPROVED-WITH-NITS | 2 minor, 2 nits | Repaired, except one optional checker assertion |
| Instructions (`alaa-instruction-reviewer`) | CHANGES-REQUESTED | 4 major, 7 minor, 2 nits | All repaired |
| Instructions, confirmation pass | APPROVED-WITH-NITS | 2 minor, 2 nits | All repaired; not re-read by the reviewer |

After the confirmation pass the parent made two more binding edits of the class the reviewer had already repaired, in commit `a1165c46`: the Go binding applies `/alaa-golang-clean-code-principles` only in an Ala service built on the alaa-go-chi kit, as that skill's own description scopes it; and the frontend binding gains the build-and-delivery and documentation-annotation triggers that the owner's global frontend rule names. The gates passed after them; no reviewer re-read them.

Records: `lanes/implementation.md`, `lanes/review-code.md`, `lanes/review-instructions.md`.

## Validation observed

On `main` at `4c208cbe`, and again after commit `a1165c46`, each exited `0`: the four root checkers, the installer unittest, both orchestrators' `render_agents.py --check`, `validate_pack.py`, `check_agent_grants.py` and `check_agent_contracts.py`, the three `alaa-prompting-guide` checkers, `check_execution_contracts.py`, the constitution template check and the memory checksum. No fixture, self-test or model comparison was run; the pack owner excludes them. The three `ValueError` branches of the binding guard are therefore proven only by the code reviewer's own probe.

## Installation

The pack owner authorized installation. From `4c208cbe`: the Claude Code installer created 4 files and updated 7; the Codex installer installed or updated 14 of 37. Both installers ran again after commit `a1165c46`. A final Claude Code dry run reported 34 unchanged. This proves the files are installed. A session started before the install keeps its old role list until it restarts.

## Open items for the owner

These came out of the session evidence. None was changed here. Items 1 and 4 need an owner decision, because one is a conflict of authority and the other changes a deliberate guard. Items 2, 3 and 5 are follow-up work a maintainer can do.

1. **Lanes that commit.** 145 of 209 Claude Code implementation lanes ran `git commit`. The implementer contract and the orchestrator's commit protocol say a lane never commits; the owner's global runtime rule says lanes commit locally. One of the two has to change.
2. **Omitted task controls.** The model was omitted in 508 of 714 Agent-tool dispatches and the effort in 591, although the orchestrator requires both on every dispatch. An omitted model inherits the session's model: four implementer lanes ran on Fable that way. Workflow-tool lanes carried no effort at all.
3. **Codex thread limit.** "Agent thread limit reached" stopped 11 follow-ups and 1 spawn, and 3 lanes ended on a usage limit. The pack has no rule for a fan-out cap or for re-dispatch after the limit. A rule needs the current Codex documentation first.
4. **Lane start-up cost.** A median of 26 to 32 tool calls before the first edit, and 80 of 119 Codex lanes read orchestrator files, because the contract sends every lane to the routing matrix and two policy references. Carrying the admission predicates in the dispatch would cut this, but it changes a deliberate guard.
5. **Preloading the testing doctrine in the generic implementers.** The contract makes that skill mandatory for every lane and 74 lanes never loaded it. Only the stack-bound roles preload it now.

## Not done

No push. No tag. No change to commit authority, task-control rules or Codex fan-out rules.
