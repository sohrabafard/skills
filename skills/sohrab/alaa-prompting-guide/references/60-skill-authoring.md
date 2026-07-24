# Skill Authoring

A skill is an execution contract, not a document. It states who the agent is for the duration of the task, what outcome counts as done, what it may and may not touch, how it validates its own work, and when it stops. Everything in this file serves that framing: the frontmatter is how the runtime finds and loads the contract, the `description` is how the model decides the contract applies, and the body is the contract itself. Skills are portable across runtimes — Claude Code implements the Agent Skills open standard and Codex reads the same `SKILL.md` shape — so one package can serve both, with only the invocation prefix differing (`/name` in Claude Code, `$name` in Codex).

## Should this be a skill at all?

Four artifacts compete for the same job, and choosing wrong is the most common authoring defect. Decide by asking what the content is conditional on and who owns the context.

- **A plain instruction** belongs in the prompt when it applies to one task and will never be reused. Do not package a one-off.
- **An instruction file** (`AGENTS.md`, `CLAUDE.md`) holds what is true for *every* task in the repository, because it is always loaded and therefore always costs context. See `70-agent-instruction-files.md`.
- **A skill** holds a procedure or body of knowledge that applies *conditionally* — to some tasks, in some repositories — and should cost nothing until it applies. Claude Code's own guidance is explicit: a section of `CLAUDE.md` that has grown into a procedure should become a skill, because a skill's body loads only when used.
- **A subagent** is right when the work needs its own context window, its own tool set, or an authority boundary the caller cannot cross. A skill changes how the current agent behaves; a subagent creates a different agent. See `80-subagent-authoring.md`.

The test in one line: if the answer to "when does this apply?" is "always," it is an instruction file; if it is "never again," it is a prompt; if it is "sometimes, and here is the trigger," it is a skill; if it is "when someone other than me must judge it," it is a subagent.

## Layout and discovery

Both runtimes take a directory whose entrypoint is `SKILL.md`. Supporting files are optional and are loaded only when the body points to them.

```
my-skill/
├── SKILL.md          # required entrypoint: frontmatter + lean body
├── references/       # detail loaded on demand
├── scripts/          # executable code the agent runs rather than reimplements
├── assets/           # templates, fixtures, static resources
└── agents/           # agent definitions shipped with the pack (see 80-)
```

The Codex skills documentation names `scripts/`, `references/`, and `assets/` directly, plus an optional `agents/openai.yaml` for Codex UI metadata. Claude Code's documentation describes the same idea generically — "templates for Claude to fill in, example outputs, scripts Claude can execute, or detailed reference documentation" — and its worked example uses `scripts/` and `examples/`. The convention above satisfies both, which is why the orchestrator packs use it unchanged across runtimes.

Discovery differs and must not be guessed. **Claude Code** loads personal skills from `~/.claude/skills/<skill-name>/SKILL.md` and project skills from `.claude/skills/<skill-name>/SKILL.md`, walking up from the working directory to the repository root and also picking up nested `.claude/skills/` directories on demand when Claude touches files beneath them. Editing a `SKILL.md` takes effect within the running session; creating a top-level skills directory that did not exist at session start requires a restart.

**Codex** scans `.agents/skills` in the current directory, in the parent, and at `$REPO_ROOT`, then `$HOME/.agents/skills`, then `/etc/codex/skills`, then skills bundled with Codex. It also discovers user skills under `$HOME/.codex/skills` — field-verified, including on Windows where the path is `Join-Path $HOME ".codex\skills"` — even though the official page omits it. That location is the practical default for personal Codex skills here, because it sits beside `~/.codex/agents/` and keeps the whole Codex setup in one tree; reserve `.agents/skills` for skills that should travel with a specific repository. The general lesson is worth carrying: an official discovery list can be incomplete, so a path that demonstrably works is evidence, not an error to correct.

## Frontmatter

Use only keys the runtime documents. Inventing a key is silent failure, not an error.

**Claude Code.** Every field is optional; only `description` is recommended, and `name` defaults to the directory name. The documented fields are `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, and `shell`. Four earn their place in most production skills: `disable-model-invocation: true` for a skill that must only ever run when a human types `/name`; `allowed-tools` to pre-approve exactly the commands the body tells the agent to run; `paths` to restrict automatic activation to matching files; and `context: fork` to run the skill in a subagent context.

**Codex.** `SKILL.md` must include `name` and `description`. Codex documents no larger frontmatter surface for skills, so anything beyond those two keys is unverified for that runtime — put the behavior in the body instead of a speculative key.

Because Claude Code tolerates extra keys it does not recognize and Codex requires the two it does, a cross-runtime skill should carry `name` and `description` and add Claude-only keys deliberately, knowing they are inert under Codex.

## The description is the highest-leverage line in the file

Neither runtime loads your body to decide whether to load your body. Both build a listing of names and descriptions and match against that. Claude Code caps each entry's combined `description` plus `when_to_use` at 1,536 characters and shortens entries further when the whole listing exceeds its budget, which scales at 1% of the model's context window; Codex budgets the listing at at most 2% of the context window, or 8,000 characters when the window is unknown. Both truncate from the end, which is why both sets of docs give the same instruction: front-load the key use case and the trigger words.

A description that only says what a skill does under-triggers, because the model has no phrase to match a user's actual request against. A description that only says "use when" over-triggers, because nothing tells the model where the boundary is. Write all three parts:

1. **What it is**, in one noun phrase, first, so truncation cannot remove it.
2. **When to use it**, in the verbs a user would actually type, not the verbs you would use to describe your own architecture.
3. **When not to use it**, including the name of the alternative when one exists. This is the part authors skip and the part that stops over-triggering.

The two production packs are worked examples. `alaa-cc-orchestrator` (639 characters) opens with "Production-grade multi-agent coding orchestration for Claude Code," then lists the trigger verbs a user says out loud — "build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work" — then declares the activation side effect, then closes with two negatives: "Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization" and "Route durable multi-phase plan/state engagements to `/alaa-workflow`." That last clause is the strongest form of a negative available, because naming the alternative gives the model somewhere to go instead of somewhere not to go. `alaa-codex-orchestrator` (564 characters) is the same contract with the runtime-specific paths swapped. Both sit comfortably inside the 1,536-character cap, so nothing is ever truncated away.

Declaring side effects in the description is not decoration. A skill whose activation writes files must say so where the model reads before deciding, not only in the body it reads after.

## Progressive disclosure

The body is always paid for; a reference is paid for only when read. Claude Code states the cost plainly: once a skill loads, its content stays in context across turns, so every line is a recurring token cost. Split accordingly.

**In the body:** the role and its authority limits; the operating modes; the decision procedure the agent walks every time; the pipeline or phase order; stop conditions; safety rules; and one-line pointers naming each reference and the condition under which to read it.

**In a reference:** anything consulted rather than followed — lookup tables, per-ecosystem command matrices, failure taxonomies, catalogs of roles or triggers, long worked examples, and installation detail. If the agent needs it in one run out of five, it is a reference.

The pointer is what makes this work. `Read references/failure-taxonomy.md when a check fails` costs one line and buys the whole file conditionally. A body that instead inlines the taxonomy pays for it on every run of every task, including the four in five that never fail a check.

Scripts deserve the same treatment for a different reason: a script is deterministic where a regenerated implementation is not. Ship the script, reference its path from the body, and pre-approve it with `allowed-tools` under Claude Code so it runs without prompting.

## Lean is a measured quality property, not an aesthetic one

OpenAI's current-model guidance reports that configurations with leaner system prompts improved evaluation scores by roughly 10–15% while reducing total tokens by 41–66% and cost by 33–67%. The scores went *up*. That inverts the intuition that more instruction buys more compliance: on this generation, padding is a quality regression that also costs money, and trimming is not a budget exercise you trade against correctness.

The same guidance names the specific things to cut — repeated instructions, redundant examples, and bloated tool descriptions — and gives the rule that replaces them: state each instruction once, keep the policy in one place and state each rule once, expose only tools relevant to the task, and keep examples only where they encode a real product requirement or correct a measured gap. Anthropic's Opus 5 guidance points the same direction from a different angle: explicit "double-check your answer" and "include a final verification step" instructions now cause over-verification and should be removed, because the model already does it.

Apply this to skills directly. A rule stated in the body and again in a reference is stated twice and should be stated once, in whichever file owns it. A section that restates the pipeline in prose after the pipeline has been given as numbered steps is a duplicate. A reassuring paragraph explaining why the skill is good is pure cost.

## Anatomy of a strong body

A complete contract answers these, each once:

- **Role.** Who the agent is while the skill is active, and — where it matters — who it is not. The orchestrator packs open with "The session model leads; narrow subagents inspect, implement, verify, challenge, and document."
- **Goal and success criteria.** The outcome, in checkable terms. If two readers would define "done" differently, the criteria are not yet criteria.
- **Constraints.** Preserved behavior, out-of-scope work, invariants that must survive.
- **Authority and side-effect limits.** What the agent may do without asking, and the enumerated list of what requires explicit permission. Bound installation, network, and destructive authority by name; the orchestrator packs limit auto-install authority to "this pack's named agent files" and say so explicitly.
- **Tool usage.** Which tools for which job, and which are forbidden. Do not describe tools the task does not need.
- **Retrieval rules.** When to consult repository state, when to fetch live docs, and which sources outrank which.
- **Validation.** The commands or checks that produce evidence, and the rule that a claim without an observed result is not reported as done.
- **Output format.** What the final report contains and in what order.
- **Stopping conditions.** Both halves: when to stop successfully, and when to stop and report a partial or blocked state. A skill with only the first half runs until something breaks.
- **Failure behavior.** What to do when a step fails — retry once, fall back, or report. The orchestrator packs' bootstrap is a model of this: "One attempt only. If installation fails for any reason, do not troubleshoot or retry mid-goal: state the failure in one line and continue."

An anti-pattern list at the end is optional but cheap and effective, because it converts the defects you have actually seen into a checklist the model can match its own behavior against.

## Defects and fixes

| Defect | Symptom | Fix |
|---|---|---|
| Description never triggers | The skill only ever runs when typed manually | Front-load a noun phrase and add the user's own trigger verbs; check the entry is not being truncated by the listing budget |
| Description over-triggers | The skill loads on unrelated requests | Add explicit negatives and name the alternative skill; make the scope noun narrower; add `disable-model-invocation: true` if it should only ever be manual (Claude Code) |
| Body duplicates a reference | Same rule in two files, drifting apart | Assign one owner per rule; leave a one-line pointer where the rule used to be |
| Instruction stated more than once | Long body, degraded compliance | State each rule once — this measurably raises scores, not just lowers cost |
| Skill tries to be a whole workflow | Body sprawls into phases, state files, resumable plans | Split it, and route the durable multi-phase part to a workflow skill by name in the description |
| Missing stopping conditions | Runs past the goal, or loops on an unreachable bar | Define both success-stop and blocked-stop; cap fix cycles by number |
| No failure behavior | Agent troubleshoots mid-goal instead of reporting | State the retry budget and the fallback in one sentence |
| Unbounded authority | Destructive or external action taken without asking | Enumerate what proceeds freely and what requires permission; scope installation authority to named files |
| Invented frontmatter key | Silently ignored | Use only documented keys; put behavior in the body when the runtime documents no key for it |

## Checklist

1. The artifact passes the "should this be a skill" test rather than belonging in an instruction file, a prompt, or a subagent.
2. Frontmatter uses documented keys only, and any Claude-only key is deliberate and known to be inert under Codex.
3. The `description` front-loads what it is, gives the user's own trigger verbs, states at least one negative, names the alternative where one exists, and declares any activation side effect.
4. The description fits the listing cap with room to spare, and the key use case survives truncation.
5. The body carries role, goal, success criteria, constraints, authority limits, tool usage, retrieval rules, validation, output format, stop conditions, and failure behavior — each stated once.
6. Every rule has exactly one owning file; references are named with the condition that triggers reading them.
7. No duplicated instruction, no decorative example, no explanation of why the skill is worth having.
8. Deterministic work is shipped as a script and pre-approved rather than described in prose.
9. Trigger syntax in any example matches the runtime: `/name` for Claude Code, `$name` for Codex.
10. Version-sensitive claims in the body carry a source or are marked unverified.

## Caveats

Verified against live documentation on 24 July 2026. Time-sensitive: the 1,536-character per-entry cap and the 1%-of-context listing budget in Claude Code, and the 2%-or-8,000-character listing budget in Codex, are current values with configurable settings behind them and should be re-checked before being quoted. The Claude Code frontmatter surface carries per-version notes (several fields require specific minor versions) and grows between releases. Codex documents no skill frontmatter keys beyond `name` and `description`; treat anything else as unverified for that runtime. The 10–15% / 41–66% / 33–67% figures are OpenAI's published measurement for the current model generation and are not a general law — re-verify on the next generation.

## Sources

- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [How Claude remembers your project (Claude Code)](https://code.claude.com/docs/en/memory)
- [Skills (Codex)](https://developers.openai.com/codex/skills)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
