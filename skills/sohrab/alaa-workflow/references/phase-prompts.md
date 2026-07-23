# Optional Prompt Generation

Create a same-stem prompt pack only when the user explicitly requests reusable prompts.

## Freshness gate

Before resolving any runtime, model, agent feature, or skill-trigger syntax:

1. Load `$alaa-prompting-guide`.
2. Verify the current official OpenAI and Anthropic documentation relevant to the selected runtimes.
3. Record the resolved implementer runtime/model, reviewer runtime/model, source URLs, and verification date in the generated pack.
4. Leave a visible `NEEDS_LIVE_VERIFICATION` marker when live verification cannot be completed. Never guess.

Stable workflow files must not pin model generations or volatile runtime feature names.

## Roles

- `implementer`: makes the in-scope change, validates it, and reports blockers.
- `independent reviewer`: inspects the resulting artifact or diff without inheriting the implementer's conclusions.
- `documenter` (optional): aligns repository documentation with the shipped phase. Include only when the phase alters behavior, APIs, configuration, or operations; route Ala-style documentation through `$alaa-docs-farsi`.

Choose the current runtime and model for each role only after the freshness gate. Use the trigger syntax accepted by that runtime. When a phase runs through `$alaa-codex-orchestrator` or `$alaa-cc-orchestrator`, these prompts feed that skill's role lanes; do not restate its dispatch machinery, review gate, or role agent definitions.

## Compact prompt shape

Each role prompt contains:

1. Outcome.
2. Read-first context.
3. Scope and authority.
4. Validation.
5. Done condition.
6. Blocked condition.

Start from `assets/phase-prompts-template.md`. Keep each role prompt at or below 250 words by default. Add only task-specific constraints that affect correctness. Put detailed checklists in the plan or read-first sources; do not repeat the plan, repository instructions, generic engineering advice, or the other role's prompt. Exceed the limit only when the user explicitly requests an exhaustive standalone prompt.

## Delegation in prompts

Authorize delegation only for independent work or high-volume context isolation. Keep phases that share substantial context in the main conversation. Name owned surfaces and integration responsibility when delegation is allowed.

## Bootstrap metadata

The initializer accepts optional `--implementer-runtime`, `--implementer-model`, `--reviewer-runtime`, `--reviewer-model`, `--verified-on`, and repeatable `--verification-source` values. Supply all runtime/model values together after live verification. Without them, the generated pack remains an explicit draft. `--documenter-runtime` and `--documenter-model` are optional, must be supplied together, and require the implementer/reviewer metadata; omitting them marks the documenter role as not included.
