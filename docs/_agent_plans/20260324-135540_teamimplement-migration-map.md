## Goal

Draft the exact migration map from `skills/sohrab/teamimplement/SKILL.md` into:
- `skills/sohrab/alaa-workflow/SKILL.md`
- `skills/sohrab/alaa-php-clean-code/references/agent-orchestration.md`

The target outcome is:
- preserve the useful subagent-orchestration details from `teamimplement`
- remove the conflicting `.planning/*` convention
- remove the hardcoded browser/mobile QA loop
- keep delegation optional and explicitly user-authorized
- align the resulting guidance with current GPT-5.4-era OpenAI guidance and the repo's existing skill hierarchy

## Assumptions

- The user wants to keep the best orchestration ideas from `teamimplement`, not the skill itself in its current form.
- `you can use subagent` counts as explicit user authorization to delegate.
- `alaa-workflow` remains the plan and coordination anchor for non-trivial work.
- `agent-orchestration.md` remains the detailed operational guide for how to use subagents safely and effectively.
- `teamimplement` is expected to be retired after migration unless a later decision keeps it as a thin compatibility wrapper.

## Constraints

- Do not keep `.planning/PLAN.md` or `.planning/phase-{n}/PLAN.md` as active conventions.
- Do not force a multi-agent workflow by default.
- Do not require the main agent to refuse planning/coding/review work.
- Do not hardcode browser/mobile/DevTools QA as a general completion step.
- Keep guidance explicit, non-contradictory, and easy for GPT-5.4 to follow.
- Preserve repo-local hierarchy: user instruction > repo/global AGENTS > `alaa-workflow` > specialist references/prompts.

## Closest existing patterns

- `skills/sohrab/alaa-workflow/SKILL.md`
  - owns long-task planning and `docs/_agent_plans/*`
  - already defines shared-state safety for concurrent work
- `skills/sohrab/alaa-php-clean-code/references/agent-orchestration.md`
  - already says single-agent first
  - already prefers manager-pattern orchestration
- `skills/sohrab/clickhouse-performance-schema-ops/SKILL.md`
  - treats multi-agent behavior as optional, domain-scoped guidance
- `skills/sohrab/vector-rust-observability-pipelines/SKILL.md`
  - same optional multi-agent pattern

## Phases (with dependencies)

### Phase 1 — Classify `teamimplement` content
- Inputs:
  - `skills/sohrab/teamimplement/SKILL.md`
  - `skills/sohrab/alaa-workflow/SKILL.md`
  - `skills/sohrab/alaa-php-clean-code/references/agent-orchestration.md`
- Output artifacts:
  - move/keep/drop matrix
- Validation:
  - confirm every meaningful `teamimplement` rule lands in one of: keep, rewrite-and-move, or drop
- Status:
  - Completed
- Parallel-safe:
  - Yes

### Phase 2 — Define exact migration targets
- Inputs:
  - Phase 1 matrix
  - repo skill hierarchy
  - official OpenAI guidance
- Output artifacts:
  - exact insertion targets and proposed replacement text
- Validation:
  - confirm no new rule contradicts `single-agent first` or `docs/_agent_plans/*`
- Status:
  - Completed
- Parallel-safe:
  - Yes

### Phase 3 — Apply edits in a later execution cycle
- Inputs:
  - this migration map
- Output artifacts:
  - edited `alaa-workflow`
  - edited `agent-orchestration.md`
  - deleted or retired `teamimplement`
- Validation:
  - skill reads cleanly
  - no `.planning/*` references remain
  - delegation guidance is explicit and optional
- Status:
  - Completed
- Parallel-safe:
  - No, because the target files will likely be touched in the same cycle

## Parallel-safe work split

- Safe parallel lane A:
  - refine the `alaa-workflow` delegated-execution section
- Safe parallel lane B:
  - refine `agent-orchestration.md` role palette, task templates, and review loop
- Not parallel-safe:
  - final wording pass across both files
  - removal of `teamimplement`
  - README or skill-map updates, if added later

## Commands to run

- `Get-Content -Raw 'skills\sohrab\teamimplement\SKILL.md'`
- `Get-Content -Raw 'skills\sohrab\alaa-workflow\SKILL.md'`
- `Get-Content -Raw 'skills\sohrab\alaa-php-clean-code\references\agent-orchestration.md'`
- `python 'C:\Users\CIT\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'D:\Sohrab\Project\skills\skills\sohrab\teamimplement'`
- Optional after applying edits:
  - `rg -n "\.planning/PLAN\.md|\.planning/phase-|teamimplement" skills docs`

## Files touched (append-only log)

- `docs/_agent_plans/20260324-135540_teamimplement-migration-map.md` — created exact migration artifact
- `skills/sohrab/alaa-workflow/SKILL.md` — added optional delegated execution mode with explicit `you can use subagent` authorization and `docs/_agent_plans/*` coordination rules
- `skills/sohrab/alaa-php-clean-code/references/agent-orchestration.md` — added role palette, delegated lane workflow, and reusable subagent prompt templates
- `skills/sohrab/teamimplement/SKILL.md` — deleted after migrating reusable guidance into existing skills

## Done / Remaining

- Done:
  - inspected `teamimplement`
  - inspected `alaa-workflow`
  - inspected `agent-orchestration.md`
  - validated `teamimplement` syntax with `quick_validate.py`
  - checked official OpenAI GPT-5 / GPT-5.4-era guidance for prompting, steerability, agent safety, and structured orchestration
  - patched `alaa-workflow` with optional delegated execution mode
  - patched `agent-orchestration.md` with reusable subagent operating guidance
  - deleted `teamimplement`
  - validated `alaa-workflow` with `quick_validate.py` in UTF-8 mode
  - confirmed no `.planning/PLAN.md`, `.planning/phase-*`, or `teamimplement` references remain under `skills/sohrab`
- Remaining:
  - optional future cleanup: refresh README or skill-map documentation only if you want the migration called out there

## Migration decision

Use a split migration:
- move workflow-governance rules into `alaa-workflow`
- move subagent operating detail and prompt templates into `agent-orchestration.md`
- drop the general-purpose browser/mobile QA loop
- delete `teamimplement` after migration

Do not:
- keep `teamimplement` as the default delegation skill
- mirror its current text into multiple files
- preserve the "create the team first" rule
- preserve the ".planning" folder convention

## Exact move / keep / drop matrix

| `teamimplement` source | Decision | Target | Notes |
| --- | --- | --- | --- |
| Lines 7-8: lead orchestrates; never writes code/plans/reviews | Rewrite and move | `agent-orchestration.md` | Keep manager pattern, drop the absolute ban on local work |
| Lines 11-18: create the whole team first | Rewrite and move | `agent-orchestration.md` | Replace with "spawn only the roles needed for the current phase/lane" |
| Line 22: phased implementation from `.planning/PLAN.md` | Rewrite and move | `alaa-workflow` | Replace path with `docs/_agent_plans/*` |
| Lines 28-33: planner/researcher stage | Rewrite and move | `agent-orchestration.md` | Keep planner/researcher lane and its deliverables |
| Lines 35-40: implementation stage with tests | Rewrite and move | `agent-orchestration.md` | Keep implementer lane and testing expectations |
| Lines 42-49: review stage and remediation loop | Rewrite and move | `agent-orchestration.md` | Keep review rubric and loopback |
| Lines 53-57: all tests/lint/review findings resolved | Split and move | `alaa-workflow` and `agent-orchestration.md` | Completion criteria stay in workflow; review finding emphasis stays in orchestration |
| Lines 59-65: QA deploy + browser/mobile loop | Drop as general rule | none | Reintroduce only in domain/UI-specific skills if needed |
| Lines 69-73: team first, delegate everything, different member each stage, phase order, `.planning` SSoT | Split and rewrite | both targets | Keep explicit authorization, manager ownership, phase order, and safe parallelization; drop the rest |

## Exact target changes

### 1) `skills/sohrab/alaa-workflow/SKILL.md`

Add one new section after `## 1) Phase design rules` and before `## 2) Minimal terminal verbosity`.

Recommended heading:

```md
## 1.1) Delegated execution mode (optional; only with explicit user authorization)
```

Recommended inserted text:

```md
Enter delegated execution mode only when the user explicitly authorizes subagents or parallel agent work, for example:
- `you can use subagent`
- `delegate this`
- `use parallel agents`
- `split this into subagents`

In delegated mode:
- keep the parent agent as the manager; the parent owns the plan, sequencing, integration, safety checks, and final synthesis
- do not pre-spawn a full team by default; spawn only the roles needed for the current phase or lane
- keep `docs/_agent_plans/<YYYYMMDD-HHMMSS>_<slug>.md` as the source of truth for sequencing and progress
- if a delegated run needs lane-specific detail, either append lane blocks to the same plan file or create child plan files under `docs/_agent_plans/`
- define lane ownership before spawning: scope, inputs, write scope, expected outputs, validation target, and merge notes
- prefer the role pattern `planner/researcher -> implementer -> reviewer` only when the task complexity justifies it
- add a verifier or remediator role only when the task needs an independent validation or remediation pass
- use browser/mobile/devtools validation only when the user explicitly requests it or the task is inherently visual/UI and repo/browser policy allows it
- do not let delegated workers broadly rewrite shared coordination artifacts; follow the shared-state safe-write protocol below
```

Why this belongs here:
- this file owns planning conventions and coordination artifacts
- this is where `.planning/*` must be replaced with `docs/_agent_plans/*`
- this is where user-authorization gating should be made explicit

### 2) `skills/sohrab/alaa-php-clean-code/references/agent-orchestration.md`

Add three new sections:
- one after `## Preferred orchestration pattern`
- one after `## Validation and review`
- one before `## Anti-patterns`

#### Section A: explicit authorization and role palette

Recommended heading:

```md
## Explicit authorization and role palette
```

Recommended inserted text:

```md
Treat phrases like `you can use subagent`, `delegate`, `use parallel agents`, or equivalent wording as explicit user authorization to delegate.

When delegation is authorized, keep the manager pattern:
- the parent agent keeps repository context, plan ownership, sequencing, safety decisions, and final synthesis
- subagents act as bounded workers or reviewers

Use only the roles the task actually needs:
- `planner/researcher`
- `implementer`
- `reviewer`
- `verifier`
- `remediator`

Do not spawn a full team by habit. Start with the smallest role set that materially reduces cycle time or improves quality.
```

#### Section B: standard delegated lane workflow

Recommended heading:

```md
## Standard delegated lane workflow
```

Recommended inserted text:

```md
When you do delegate, use this order:

1. update or create the parent plan in `docs/_agent_plans/*`
2. define lane ownership:
   - task scope
   - read inputs
   - allowed write scope
   - expected outputs
   - validation target
   - merge notes
3. spawn only the role needed for the next bounded step
4. keep the parent agent doing non-overlapping work while the subagent runs
5. review the returned artifact before handing the lane to the next role
6. merge the result back into the parent plan and final synthesis

Use the following role sequence only when it helps:
- `planner/researcher -> implementer -> reviewer`

Add:
- `verifier` when an independent validation pass materially reduces risk
- `remediator` when reviewer or verifier findings need a bounded fix pass

Do not hardcode browser/mobile/devtools verification into the workflow. Use those tools only when the user explicitly requests them or the task is inherently UI/visual and policy allows it.
```

#### Section C: reusable subagent prompt templates

Recommended heading:

```md
## Reusable subagent prompt templates
```

Recommended inserted text:

```md
Use these as task templates when the user has explicitly authorized subagents.

### Planner / researcher

You are the planning and research worker for lane `{{lane_name}}`.

Context:
- Parent plan: `{{plan_path}}`
- Scope: `{{scope}}`
- Write scope: none unless explicitly granted
- Validation target: `{{validation_target}}`

Instructions:
- Read the parent plan and only the repo files needed for this lane.
- Respect repo `AGENTS.md`, active skills, and the lane boundary.
- Research locally first; use external docs only when needed.
- Produce an implementation-ready subplan for this lane.
- Call out contracts, invariants, edge cases, risks, and required tests.
- Do not edit files outside your lane.

Return:
1. assumptions
2. required file touches
3. step-by-step implementation plan
4. validation checklist
5. risks or open questions

### Implementer

You are the implementation worker for lane `{{lane_name}}`.

Context:
- Parent plan: `{{plan_path}}`
- Planner notes: `{{planner_output_ref}}`
- Allowed write scope: `{{write_scope}}`
- Validation target: `{{validation_target}}`

Instructions:
- Implement only within your write scope.
- Preserve repo conventions and public contracts unless the plan explicitly changes them.
- Add targeted tests for the happy path, relevant edge cases, and failure handling in this lane.
- If you discover a cross-lane blocker, stop and report it instead of editing outside scope.
- Append a concise completion note for the parent agent to merge into the main plan.

Return:
1. files changed
2. behavior implemented
3. validations run
4. remaining risks or blockers

### Reviewer

You are the independent reviewer for lane `{{lane_name}}`.

Context:
- Parent plan: `{{plan_path}}`
- Scope: `{{scope}}`
- Changed files: `{{changed_files}}`

Review against:
- plan adherence
- contract preservation
- concurrency or HA implications if relevant
- code quality
- test value and missing cases

Instructions:
- Prioritize findings by severity.
- Prefer behavioral and regression risks over style nits.
- Do not change files.

Return:
1. findings only, ordered by severity
2. residual risks
3. go or no-go recommendation

### Verifier

You are the validation worker for lane `{{lane_name}}`.

Context:
- Parent plan: `{{plan_path}}`
- Validation target: `{{validation_target}}`
- Changed files: `{{changed_files}}`

Instructions:
- Run the smallest meaningful validation first, then expand only if needed.
- Use browser/mobile/devtools only if explicitly authorized or inherently required by the task.
- Do not perform deployment or destructive actions unless explicitly approved.

Return:
1. commands or checks run
2. pass or fail summary
3. reproducible issues
4. next recommended fix if failing

### Remediator

You are the remediation worker for lane `{{lane_name}}`.

Context:
- Parent plan: `{{plan_path}}`
- Findings to address: `{{findings_ref}}`
- Allowed write scope: `{{write_scope}}`

Instructions:
- Fix only the approved findings in your lane.
- Preserve already-correct behavior.
- Re-run the narrowest validations that prove the fix.

Return:
1. fixes applied
2. validations re-run
3. unresolved risks, if any
```

Why this belongs here:
- this file already owns "when to split", manager pattern, and anti-patterns
- `teamimplement`'s best material is operational delegation detail, not general planning policy
- prompt templates are most useful next to the orchestration rules they instantiate

## What to drop completely

Do not migrate these ideas as global rules:
- "create the team first"
- "the parent agent never writes code, plans, or reviews"
- "every phase must use a different team member"
- "every task ends with QA members deploying and testing in browser/mobile tools"
- ".planning/PLAN.md is the single source of truth"

Reason:
- they conflict with the current repo design
- they add unnecessary rigidity
- they are more likely to hurt GPT-5.4 than help it because GPT-5 is highly steerable and sensitive to contradictory or over-specified instructions

## Why this is aligned with GPT-5.4 / current OpenAI guidance

The recommended migration follows current official guidance as of 2026-03-24:

- GPT-5.4 is now available in the API and Codex, and OpenAI positions it as stronger for coding, tool use, web search, and long-horizon professional work.
  - Source: `Introducing GPT-5.4`, published 2026-03-05
  - URL: `https://openai.com/index/introducing-gpt-5-4/`
- GPT-5-family models are highly steerable, and contradictory or vague prompts can hurt performance more than they helped earlier models.
  - Source: `GPT-5 prompting guide`
  - URL: `https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide`
- OpenAI recommends clear prompt structure, concise reusable prompt organization, and prompt/version iteration.
  - Source: `Prompting`
  - URL: `https://developers.openai.com/api/docs/guides/prompting`
- OpenAI's safety guidance for multi-agent workflows stresses prompt-injection and data-leakage risk reduction, clear developer guidance, structured data flow, and careful MCP/tool use.
  - Source: `Safety in building agents`
  - URL: `https://developers.openai.com/api/docs/guides/agent-builder-safety`

Practical interpretation for this repo:
- prefer explicit authorization over always-on delegation
- prefer a manager pattern over decentralized "nobody owns the whole task"
- use structured, role-specific prompts instead of one long generalized "team mode" prompt
- avoid contradictions such as "single-agent first" plus "must create a full team before any work"

## Recommended application order in the next patch

1. patch `skills/sohrab/alaa-workflow/SKILL.md`
2. patch `skills/sohrab/alaa-php-clean-code/references/agent-orchestration.md`
3. re-read both files together and remove duplicate wording
4. search for any remaining `.planning/*` references
5. delete `skills/sohrab/teamimplement/SKILL.md`
6. optionally refresh any skill-map or README mention if you later add one

## Validation checklist for the next patch

- `alaa-workflow` explicitly says `you can use subagent` counts as authorization
- `alaa-workflow` uses only `docs/_agent_plans/*`
- `agent-orchestration.md` contains reusable role templates
- `agent-orchestration.md` does not force delegation by default
- no general skill hardcodes browser/mobile QA loops
- no surviving instruction says the parent agent must never do local work
- no surviving instruction tells multiple agents to edit overlapping scopes without ownership

## Timeline

- 2026-03-24 10:25 UTC — Inspected `teamimplement`, `alaa-workflow`, and `agent-orchestration.md`; confirmed that `teamimplement` is structurally valid but conflicts with the existing planning path and delegation defaults.
- 2026-03-24 10:33 UTC — Reviewed current official OpenAI GPT-5 / GPT-5.4 guidance and extracted the implications most relevant to prompt structure, steerability, and multi-agent safety.
- 2026-03-24 10:35 UTC — Wrote the exact migration map with concrete insertion targets and prompt templates for the next edit cycle.
- 2026-03-24 10:46 UTC — Applied the migration to `alaa-workflow` and `agent-orchestration.md`, removed `teamimplement`, validated `alaa-workflow`, and confirmed there are no stale `.planning/*` or `teamimplement` references in `skills/sohrab`.
