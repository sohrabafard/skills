# Agent orchestration for PHP / Laravel work

## Contents
- Single agent first
- When to split into subagents
- Preferred orchestration pattern
- Parallel local work
- Good PHP / Laravel split patterns
- Validation and review
- Anti-patterns
- Official references

## Single agent first
Start with one clear local plan.

Use a single agent when:
- the task is small or medium
- the immediate next step is blocked on one local inspection
- one agent can still hold the codebase context comfortably
- splitting would create more coordination cost than speed

A multi-agent workflow is justified when independent tracks exist or prompt and tool complexity are beginning to reduce quality.

## When to split into subagents
Use subagents only when both of these are true:
- the user explicitly asks for subagents, delegation, or parallel agent work, or the environment policy clearly allows it
- the work can be decomposed into bounded subtasks that materially help the main task

Good reasons to split:
- independent repository discovery questions
- separate implementation slices with disjoint write scopes
- independent validation or review passes
- external research that can run while the main agent keeps coding locally

Bad reasons to split:
- the task is trivial
- the very next action is blocked on the delegated result and no other meaningful local work exists
- multiple subagents would touch the same files without clear ownership
- the goal is only to sound busy rather than reduce cycle time or improve quality

## Preferred orchestration pattern
Prefer a manager pattern for coding tasks.

That means:
- one main agent keeps plan ownership, repository context, and final synthesis
- subagents behave like tools, workers, or focused reviewers
- the main agent integrates the results and stays responsible for the final answer and final diff

Prefer decentralized handoffs only when one agent truly should give up control to another specialist. For most repo coding tasks, the manager pattern is safer and easier to keep coherent.

## Explicit authorization and role palette
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

## Parallel local work
Use parallel local work for independent operations.

In Codex desktop:
- use `multi_tool_use.parallel` for independent developer-tool calls
- parallelize read-only inspections such as file reads, searches, directory listings, or unrelated validation commands
- fan out first, then synthesize once in the main agent

Do not parallelize:
- overlapping writes
- commands that mutate shared state in conflicting ways
- tools that explicitly should not run in parallel
- steps where one command depends on the output of another

## Good PHP / Laravel split patterns

### Discovery fan-out
Use separate subagents for questions such as:
- routes, controllers, requests, and resources
- services, DTOs, repositories, and policies
- tests, docs, and existing conventions

### Implementation fan-out
Use separate subagents only when write scopes are disjoint, for example:
- worker A owns Form Requests and Resources
- worker B owns Services, DTOs, or Strategies
- worker C owns tests or documentation

### Validation fan-out
Use separate passes for:
- independent review of changed files
- verifying route-to-resource consistency
- checking whether new abstractions actually reduced duplication

## Validation and review
While subagents run:
- continue non-overlapping local work
- do not busy-wait
- do not duplicate the delegated work locally

For tricky changes, use a fresh subagent as an independent reviewer or forward-check. Give the minimum context needed and inspect the resulting reasoning, diff, or artifacts rather than leaking the intended answer.

## Standard delegated lane workflow
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

## Reusable subagent prompt templates
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

## Anti-patterns
- spawning subagents for every task by habit
- delegating the immediate blocking step and then waiting idle
- sending vague, open-ended, overlapping assignments
- letting multiple agents edit the same files without ownership boundaries
- using subagents to bypass safety, approval, or repository policy
- parallelizing `apply_patch`, `js_repl`, or any tool that forbids parallel execution
- asking subagents to solve the same unresolved question redundantly

## Official references
This guidance is aligned with:
- OpenAI's practical guidance to start with a single agent first and add multi-agent orchestration only when the task structure justifies it
- OpenAI's manager vs decentralized orchestration patterns for agent systems
- OpenAI prompt guidance to keep instructions explicit and tool-oriented
- OpenAI evaluation guidance to validate workflow behavior, not just final text
