# Optional Prompt Generation

Create a same-stem prompt pack only when the user explicitly requests reusable prompts.

## Freshness gate

Before resolving any runtime, model, agent feature, or skill-trigger syntax:

1. Load `$alaa-prompting-guide` / `/alaa-prompting-guide`.
2. Verify the current official OpenAI and Anthropic documentation relevant to the selected runtimes.
3. Record the resolved implementer runtime/model, reviewer runtime/model, effort levels, source URLs, and verification date in the generated pack.
4. Leave a visible `NEEDS_LIVE_VERIFICATION` marker when live verification cannot be completed. Never guess.

**Resolved values belong in the generated prompt pack with their verification date, and never in stable skill text.** This is the rule that keeps this skill from decaying. A model name or effort level written into a reference file is wrong the next time either vendor ships, and it will be copied forward long after it stopped being true — into packs where nobody re-checked it, because it looked authoritative. Stable workflow files name the decision and point at its owner; only the dated pack carries the answer. Model and effort choices come from `$alaa-prompting-guide` / `/alaa-prompting-guide` and its `references/50-effort-and-thinking.md`, never from memory and never from a value copied out of an older prompt pack. Model and effort are two questions, not one; resolve them separately.

## Roles

- `implementer`: makes the in-scope change, validates it, and reports blockers.
- `independent reviewer`: inspects the resulting artifact or diff without inheriting the implementer's conclusions.
- `documenter` (optional): aligns repository documentation with the shipped phase. Include only when the phase alters behavior, APIs, configuration, or operations; route Ala-style documentation through `$alaa-repo-docs` / `/alaa-repo-docs`.

Choose the current runtime and model for each role only after the freshness gate, and use the trigger syntax that runtime accepts — `$name` in Codex, `/name` in Claude Code.

When a phase runs through `$alaa-codex-orchestrator` (Codex) or `/alaa-cc-orchestrator` (Claude Code), these prompts feed that pack's role lanes; do not restate its dispatch machinery, review gate, or role agent definitions. Each pack carries a 21-role catalog for its own runtime — core lanes plus conditionally gated specialists — with a model and effort pinned per role. Those pins belong to the packs, they move whenever the model landscape moves, and this file deliberately does not mirror them: read `references/90-model-selection.md` in `$alaa-prompting-guide` / `/alaa-prompting-guide` for the current pin summary and the catalog's shape. A prompt pack keeps only the three durable roles above and never redefines or re-pins that catalog. Model choices inherit the packs' default-down rule: tier escalation is earned by a named criterion of decision density, never by surface sensitivity or goal importance, and when it is unclear whether a lane qualifies it does not.

Build such prompts under the invocation-and-composition rules of `$alaa-prompting-guide` / `/alaa-prompting-guide` (its `references/06-invocation-and-composition.md`): the orchestrator trigger opens the message with the exact installed name, the session role is the orchestrator with an explicit do-not-implement negative, implementation verbs live in lane rules, and any `/goal` text stays a compact bounded condition sent separately.

## Compact prompt shape

Each role prompt contains:

1. Outcome.
2. Read-first context.
3. Scope and authority.
4. Validation.
5. Done condition.
6. Blocked condition.

The read-first section must carry the handoff-package facts that bear on this lane: the confirmed facts with how they were verified, the approaches already ruled out and why, and the environment notes and traps that apply to the surfaces this role owns. The executing agent has no shared context — it sees this prompt and the files it names, and nothing else. Copy the facts in rather than pointing at a conversation it never had. A prompt that omits them buys a rediscovery, or a repeat of an experiment that already failed. Field semantics are in `references/context-continuity.md`.

Start from `assets/phase-prompts-template.md`. Keep each role prompt at or below 250 words by default. Add only task-specific constraints that affect correctness. Put detailed checklists in the plan or read-first sources; do not repeat the plan, repository instructions, generic engineering advice, or the other role's prompt. Exceed the limit only when the user explicitly requests an exhaustive standalone prompt.

## Delegation in prompts

`SKILL.md` owns which work may be delegated. What belongs in the prompt is the consequence: when a prompt authorizes delegation, it names the owned surfaces and who owns integration, because the executing agent cannot ask.

## Bootstrap metadata

The initializer accepts optional `--implementer-runtime`, `--implementer-model`, `--reviewer-runtime`, `--reviewer-model`, `--verified-on`, and repeatable `--verification-source` values. Supply all runtime/model values together after live verification. Without them, the generated pack remains an explicit draft. `--documenter-runtime` and `--documenter-model` are optional, must be supplied together, and require the implementer/reviewer metadata; omitting them marks the documenter role as not included.
