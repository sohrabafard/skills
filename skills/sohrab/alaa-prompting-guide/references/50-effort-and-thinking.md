# Effort and Thinking: A Cross-Model Decision Procedure

This file owns the question "how hard should this model think, and how do I know?" It applies to every model in scope and to both runtimes. Read the target model's own reference for the levels it actually supports; read this file for how to choose among them.

## The two levers do different jobs

**Model** selects the *kind* of judgment available. **Effort** selects *how much search* that judgment performs before it answers.

Do not assume raising effort makes one model equivalent to another. Their trade-off is empirical: compare one variable at a time against the same task and acceptance criteria.

Choose the model from the kind of judgment the task requires. Choose the effort from how much search that judgment needs. Then verify, because both choices are empirical.

## What effort does not control

Effort controls thinking volume. It does not control response length, and on the current Claude flagship the documentation says so explicitly. This matters because the natural reflex when a model's answers run long is to lower effort, and that reflex fails: it produces a shallower answer of roughly the same length. Response length, written-deliverable length, and progress-update cadence are all prompt-controlled and need their own explicit instructions. Read `references/21-opus-5-5.md` for current calibration guidance.

Effort also does not control scope. A model that widens the task beyond what was asked is not thinking too hard; it is missing a scope constraint. Fix that in the prompt.

## Thinking: keep it on, lower the effort instead

Use the registered model capability snapshot and refresh its API documentation before changing
thinking controls. Current model references own modes and exceptions. Haiku 5.5 supports effort and adaptive thinking; its API disabled-thinking exception does not transfer to Claude Code. Historical Haiku 4.5 uses extended thinking without effort. These API controls are not interchangeable Claude Code settings.

For effort-enabled models, compare lower supported effort as a cost lever. Measure retrieval,
tool-use reliability and task quality; report unsupported controls instead of substituting
them. Read `references/36-haiku-5-5.md` for current Haiku controls.

Do not carry manual thinking budgets into current adaptive models. Historical Haiku 4.5 is the extended-thinking exception. The value `adaptive` names a thinking mode, never an effort. Neither `ultra` nor
`ultracode` is a Claude API effort value; harness orchestration modes require separate proof.

## Choosing a starting level

Each family has a documented starting point, and the numbers are not the same across models, which is why "use high effort" is meaningless advice across vendors. This file does not restate them — a second copy is the first one to go stale. Read the target model's own reference (`references/21-opus-5-5.md`, `references/31-sonnet-5-5.md`, `references/42-fable-5-1.md`, `references/36-haiku-5-5.md`, `references/12-gpt-6.md`) for the levels it supports, its default, and its recommended starting point for coding and agentic work.

Every family gives the same meta-instruction and it is the most important sentence in this file: **an effort level inherited from a previous model generation is an untested assumption, not a tuned setting.** Revalidate current guidance and preserve unrun calibration status; a task selection does not require an experiment.

## The decision procedure

1. **Classify missing facts before judgment.** Retrieve or clarify absent context, tool capability or product intent; a stronger model does not supply missing evidence.
2. **Plan with the appropriate strong-workhorse profile.** Clear scope/contracts/constraints fit medium planning; resolving interacting uncertainties to form the plan fits high. Use verified compatible lead controls or a real read-only planner.
3. **Select implementation directly from the completed plan.** Record outcome, scope, settled/open decisions, failure/invariant reasoning and exact registered profile/reason. Planning effort and implementation effort are independent. Runtime routing matrices own workload admission; canonical policies own pins.
4. **Reserve exceptional implementation for evidence or explicit direction.** Require applicable high-effort workhorse inadequacy after correcting context/specification/tools and considering decomposition, or explicit user selection. Complexity, sensitivity, file/failure count and imagined insufficiency alone do not qualify. Prior applicable evidence may suffice; no trial ladder, synthetic benchmark or replay is required.
5. **Keep selection and calibration separate.** Controlled comparisons vary one factor at a time with task/context/tools/acceptance held constant; compare cost only among passing runs. Local profile rationales remain unrun until measured. A task selection does not require a new experiment.
6. **Realize the actual controls.** Verify runtime availability, caps and override precedence. A custom profile may ignore caller model/effort; prose never changes the running configuration. Reassess only at existing material-scope/fix-follow-up boundaries and preserve completed work and independent gates.

## Codex profiles and exceptions

`assets/codex-model-policy.json` is the canonical Codex role-to-model/effort policy. The
validator compares every executable pin to that file. No Codex model-tier ceiling applies:
supported levels describe capability, while a selected level is a workload hypothesis.
Default profiles never use `max` or `ultra`; this is local cost policy, not a vendor limit.
A named non-default experiment may use a supported higher level with a stated need and
recorded evidence, without changing the default profiles.

GPT-5.6 is allowed only through a matching `legacy_exceptions` entry recording profile,
model, effort, reason, scope, evidence, review condition, approver, and approval date. Evidence
must show a representative quality advantage or a verified availability constraint. Add
current target-host supported-effort evidence before registering a legacy model. No exception
is active by default. An unavailable requested model is reported; never substitute silently.

A custom TOML pin cannot be overridden by assuming a spawn parameter wins. Select a registered
profile with the required pin; if none exists, report the selection limit or obtain authority
for a configuration change. Read `references/11-codex-runtime-features.md` for precedence.

Unrun profiles remain `calibration_status: unrun`; evaluated profiles require an evidence
pointer. `references/92-agent-evaluation.md` defines the comparison corpus and evidence fields.
For Claude, `assets/claude-model-policy.json` is the separate canonical owner. Its supported
levels are capabilities, not a blanket ceiling or a recommendation to maximize effort.
Unrun is the initial calibration state; evaluated requires validated, matching runtime
comparison evidence. Read `references/41-claude-code-runtime-features.md` before relying on
model/effort override precedence or claiming activation.

## Effort is not the only cost lever

Before raising effort, check whether the real problem is prompt shape. On the current GPT generation, leaner system prompts measurably improved evaluation scores while substantially cutting tokens, which means prompt bloat degrades quality and costs money at the same time. Whether a shorter prompt or lower effort preserves quality must be measured on the target workload.

The same applies to context. A model reasoning over a poorly assembled context does not need more thinking; it needs better retrieval. Raising effort to compensate for missing facts is the most expensive way to fail, because the model will explore thoroughly and confidently in the wrong direction.

## Anti-patterns

- Carrying an effort level forward from a previous model generation without revalidating current guidance and honestly retaining unrun calibration status; task selection does not require an experiment.
- Disabling thinking to control cost instead of lowering effort, then writing repair instructions for the resulting behavior.
- Lowering effort to shorten responses. Effort is not a verbosity control.
- Raising effort because the goal is important or the surface is sensitive rather than because the lane must decide something.
- Pinning maximum effort by habit without measured quality benefit and a stated workload need.
- Treating a supported effort as proof it is appropriate, or changing model and effort together in a comparison.
- Setting an explicit thinking budget on a generation that no longer accepts one.
- Passing `adaptive` as an effort value.
- Raising effort to compensate for a bloated prompt or a badly assembled context.
- Benchmarking by effort name across vendors, where the same word denotes different amounts of work.

## Caveats

Thinking-disable constraints and the availability of manual thinking budgets are vendor-stated and time-sensitive; effort level names, per-model defaults, and starting-point recommendations are not restated here — read the target model's own file, which is the current source for its own numbers. The measured lean-prompt figures are from a specific vendor's internal testing on a specific generation and should not be generalized. Re-read the sources below before hard-coding any of these anywhere, and distinguish local pin policy from vendor capability.

## Sources

- [Effort parameter reference](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Using the latest model](https://developers.openai.com/api/docs/guides/latest-model)
