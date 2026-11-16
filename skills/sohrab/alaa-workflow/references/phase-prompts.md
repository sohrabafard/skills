# Optional Prompt Generation

Create a reusable prompt pack only on explicit request, for an admitted execution family. A Markdown pack uses the plan's stem. For Beads-native work, cite the root address and the exact phase and task IDs in the requested deliverable. Create no companion plan for the pack.

## Freshness gate

Before you resolve a runtime, model, agent feature or skill-trigger syntax:

1. Load `/alaa-prompting-guide`.
2. Verify the current official OpenAI and Anthropic documentation for the selected runtimes.
3. Record in the generated pack the implementer and reviewer runtime and model, the effort levels, the source URLs and the verification date.
4. When live verification cannot be completed, leave a visible `NEEDS_LIVE_VERIFICATION` marker. Never guess.

Resolved values belong only in the dated pack, never in stable skill text, because a model name or an effort level goes stale at the next vendor release. The task model AND effort come from the active runtime orchestrator, never from role identity, memory or an older prompt pack.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Resolve model and effort as two separate questions.

## Roles

- `implementer`: makes the in-scope change, validates it and reports blockers.
- `independent reviewer`: inspects the resulting artifact or diff without the implementer's conclusions.
- `documenter` (optional): aligns repository documentation with the shipped phase. Include it only when the phase alters behavior, APIs, configuration or operations. Route Ala-style documentation through `/alaa-repo-docs`.

Record the runtime and both task-selected controls for every role only after the freshness gate.

When a phase runs through `/alaa-codex-orchestrator` (Codex) or `/alaa-cc-orchestrator` (Claude Code), these prompts feed that pack's role lanes. Never restate its dispatch machinery, review gate, roster or role definitions. A prompt pack keeps only the three roles above.

Build prompts through `/alaa-prompting-guide` `references/06-invocation-and-composition.md`. It decides goal composition and the trigger syntax that each runtime accepts. Name the exact installed orchestrator, give it orchestration authority, and put implementation authority in the lane rules.

## Compact prompt shape

Each role prompt has six fields: outcome, read-first context, scope and authority, validation, done condition and blocked condition.

The read-first field carries:

- /alaa-testing-strategy, required before designing implementation or verification;
- the exact skill names of the selected phase or task, with their sources, load points, conditions and absence actions, or an exact reference to its populated Skill Bindings and task overrides. Resolve them from the plan; never write "use relevant skills";
- the handoff-package facts that bear on the lane: confirmed facts with how they were verified, approaches ruled out and why, and the environment notes and traps for the surfaces this role owns. Copy the facts in, because the agent sees only this prompt and the files it names.

Every generated dispatch identifies the whole engagement, the current phase, task and subtask, the final phase and the declared review boundary from the plan. The reviewer prompt applies only at that boundary, and only when the runtime orchestrator's verification decision or a floor calls for a review. A nested invocation inherits the boundary; never infer a new final candidate from the prompt's local phase. Carry the plan's phase collection and repair/retest barriers and their evidence owner. Route scheduling to `alaa-codex-orchestrator` or `alaa-cc-orchestrator` `references/verification-and-gates.md`.

For a Beads-bound dispatch, resolve the actor, the binding, the issue IDs, the ownership action and the `bd` flags through `references/task-tracking.md` `## Agent identity and ownership` and `## Beads capabilities in use`.

Start from `assets/phase-prompts-template.md`. Keep each role prompt at or below 250 words by default. Add only task-specific constraints that affect correctness, and put detailed checklists in the plan or the read-first sources. When required behavior-affecting content does not fit in 250 words, exceed the target, say so, and compress the rest.

A prompt that authorizes delegation names the owned surfaces and the integration owner, because the executing agent cannot ask.

## Bootstrap metadata

The Markdown initializer accepts optional `--implementer-runtime`, `--implementer-model`, `--reviewer-runtime`, `--reviewer-model`, `--verified-on` and repeatable `--verification-source`. After source verification, supply all four runtime and model values together, with `--implementer-effort` and `--reviewer-effort` for complete selected controls. A model-only invocation stays a draft with unresolved effort; partial effort input is rejected. Without these values, the pack stays an explicit draft. `--documenter-runtime` and `--documenter-model` are optional, go together and require the implementer and reviewer metadata. An included documenter also requires `--documenter-effort`; omitting the documenter flags marks that role not included. Source metadata never proves effective runtime controls: the active orchestrator verifies them before every dispatch.
