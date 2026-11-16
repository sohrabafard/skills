# Optional Prompt Generation

Create a reusable prompt pack only on explicit request for an admitted execution family. For Markdown, use the same stem. For Beads-native work, cite the root address and the exact phase and task IDs in the requested deliverable. Create no companion plan for the pack.

## Freshness gate

Before resolving any runtime, model, agent feature, or skill-trigger syntax:

1. Load `/alaa-prompting-guide`.
2. Verify the current official OpenAI and Anthropic documentation relevant to the selected runtimes.
3. Record the resolved implementer runtime and model, the reviewer runtime and model, the effort levels, source URLs, and verification date in the generated pack.
4. Leave a visible `NEEDS_LIVE_VERIFICATION` marker when live verification cannot be completed. Never guess.

**Resolved values belong in the generated prompt pack with their verification date, and never in stable skill text,** because a model name or effort level in a reference file goes stale at the next vendor release and is then copied forward as if authoritative. Stable workflow files name the decision and point at its owner; only the dated pack carries the answer. Actual task model AND effort choices come from the active runtime orchestrator, never from role identity, memory or an older prompt pack.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Current `/alaa-prompting-guide` capabilities and mechanics inform those choices. Model and effort are two questions, not one; resolve them separately.

## Roles

- `implementer`: makes the in-scope change, validates it, and reports blockers.
- `independent reviewer`: inspects the resulting artifact or diff without inheriting the implementer's conclusions.
- `documenter` (optional): aligns repository documentation with the shipped phase. Include only when the phase alters behavior, APIs, configuration, or operations; route Ala-style documentation through `/alaa-repo-docs`.

Record the current runtime and both task-selected controls for every role only after the freshness gate, and use the trigger syntax that runtime accepts — `$name` in Codex, `/name` in Claude Code.

When a phase runs through `/alaa-codex-orchestrator` (Codex) or `/alaa-cc-orchestrator` (Claude Code), these prompts feed that pack's role lanes; do not restate its dispatch machinery, review gate, roster, or role definitions. `/alaa-prompting-guide` owns capabilities, runtime precedence and checked model-neutral projections; the runtime orchestrator selects BOTH controls from the actual task. A prompt pack keeps only the three durable roles above; the orchestrator owns role triggers and chooses the runtime profile.

Build prompts through `/alaa-prompting-guide` `references/06-invocation-and-composition.md`. Name the exact installed orchestrator, give it orchestration authority, and put implementation authority in the lane rules. The invocation owner decides goal composition for the selected surface.

## Compact prompt shape

Each role prompt contains:

1. Outcome.
2. Read-first context.
3. Scope and authority.
4. Validation.
5. Done condition.
6. Blocked condition.

Within read-first, require /alaa-testing-strategy before designing implementation or verification.

Within read-first, give the exact skill names of the selected phase or task, with their sources, load points, conditions, and absence actions, or an exact reference to its populated Skill Bindings and task overrides. Resolve these from the plan rather than writing "use relevant skills". Keep this within the six fields; `references/companion-routing.md` owns the mapping contract.

Every generated dispatch identifies the whole engagement, the current phase, task and subtask, the final phase and the declared review boundary from the plan. The reviewer prompt applies only at that boundary, and only when the runtime orchestrator's verification decision or a floor calls for a review; a nested invocation inherits the boundary. Carry the plan's phase collection and repair/retest barriers and their evidence owner. Route scheduling to `alaa-codex-orchestrator` or `alaa-cc-orchestrator` `references/verification-and-gates.md`. Never infer a new final candidate from the prompt's local phase.

For Beads-bound dispatches, resolve actor, binding, issue IDs, ownership action and the `bd` flags a lane without write or sync authority passes through `references/task-tracking.md` `## Agent identity and ownership` and `## Beads capabilities in use` before use.

The read-first section must carry the handoff-package facts that bear on this lane: confirmed facts with how they were verified, approaches ruled out and why, and the environment notes and traps for the surfaces this role owns. Copy the facts in; never point at a conversation the agent never had, because it sees only this prompt and the files it names, and an omitted fact buys a rediscovery or a repeated failed experiment. `references/context-continuity.md` owns field semantics.

Start from `assets/phase-prompts-template.md`. Keep each role prompt at or below 250 words by default. Add only task-specific constraints that affect correctness. Put detailed checklists in the plan or read-first sources; do not repeat the plan, repository instructions, generic engineering advice, or the other role's prompt. The 250-word target yields whenever exhaustive or required behavior-affecting content does not fit: exceed it rather than drop any, say so, and compress the rest as normal.

## Delegation in prompts

`SKILL.md` owns which work may be delegated. A prompt that authorizes delegation names the owned surfaces and the integration owner, because the executing agent cannot ask.

## Bootstrap metadata

The Markdown initializer accepts optional `--implementer-runtime`, `--implementer-model`, `--reviewer-runtime`, `--reviewer-model`, `--verified-on` and repeatable `--verification-source`. After source verification, supply all runtime and model values together, with `--implementer-effort` and `--reviewer-effort` for complete selected controls. Model-only legacy invocations stay draft with unresolved effort; partial effort input is rejected. Source metadata never proves effective runtime controls; the active orchestrator must verify them before every dispatch. Without these values, the pack stays an explicit draft. `--documenter-runtime` and `--documenter-model` are optional, go together and require the implementer and reviewer metadata; omitting them marks the documenter role not included. An included documenter also requires `--documenter-effort`.
