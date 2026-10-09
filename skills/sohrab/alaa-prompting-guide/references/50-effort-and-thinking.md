# Effort and Thinking: A Cross-Model Decision Procedure

Owns effort selection across supported models/runtimes. The target model reference owns its levels; this file owns choosing among them.

## The two levers do different jobs

**Model** selects judgment; **effort** selects search depth. Choose from the lane's remaining decisions and required search, then verify. Higher effort proves no cross-model equivalence: comparisons vary one factor against the same task and acceptance.

## What effort does not control

Response length, deliverable length, update cadence and scope require explicit prompt controls. Effort can change tokens and tool behavior; lowering it is not a reliable substitute for output/scope constraints. Read the target model reference for observed workload-specific effects.

## Thinking: keep it on, lower the effort instead

Use the registered model capability snapshot and refresh its API documentation before changing
thinking controls. Current model references own modes and exceptions. Haiku 5.5 supports effort and adaptive thinking; its API disabled-thinking exception does not transfer to Claude Code. Historical Haiku 4.5 uses extended thinking without effort. These API controls are not interchangeable Claude Code settings.

For effort-enabled models, compare lower supported effort as a cost lever. Measure retrieval,
tool-use reliability and task quality; report unsupported controls instead of substituting
them. Read `references/36-haiku-5-5.md` for current Haiku controls.

Do not carry manual thinking budgets into current adaptive models. Historical Haiku 4.5 is the extended-thinking exception. The value `adaptive` names a thinking mode, never an effort. Neither `ultra` nor
`ultracode` is a Claude API effort value; harness orchestration modes require separate proof.

## Choosing a starting level

Read the target's reference for supported levels, default and workload starting point; shared effort names do not imply shared search depth. An inherited effort is untested: refresh guidance and retain unrun status. Selection requires no experiment.

## The decision procedure

1. **Classify missing facts before judgment.** Retrieve or clarify absent context, tool capability or product intent; a stronger model does not supply missing evidence.
2. **Plan with the appropriate strong-workhorse profile.** Clear scope/contracts/constraints fit medium planning; resolving interacting uncertainties to form the plan fits high. Use verified compatible lead controls or a real read-only planner.
3. **Allocate implementation once after plan finalization**, through `references/90-model-selection.md`. Record scope, settled/open decisions, invariant/failure reasoning and the exact source-row/priority/profile reason. Its priority procedure owns when a concrete consequence justifies higher quality; that does not prove greater complexity. Planning and worker effort are independent. Runtime matrices own admission; canonical policies own pins.
4. **Admit exceptional implementation through its runtime's route.** Codex's exact source-matched branch follows `references/90-model-selection.md`; outside it require applicable high-effort workhorse inadequacy after context/spec/tool correction and consideration of decomposition, or explicit user model selection. Claude Fable keeps that inadequacy/explicit-selection boundary. Complexity, sensitivity, file/failure count and imagined inadequacy alone do not qualify. Reuse prior applicable evidence; no trial ladder, synthetic benchmark or replay.
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

Before raising effort, resolve prompt bloat and missing context. Vendor lean-prompt results support evaluating shorter prompts; they prove no local quality or cost gain. Better retrieval addresses absent evidence.

## Anti-patterns

- Carrying an effort level forward from a previous model generation without revalidating current guidance and honestly retaining unrun calibration status; task selection does not require an experiment.
- Disabling thinking to control cost instead of lowering effort, then writing repair instructions for the resulting behavior.
- Treating lower effort as a reliable verbosity or scope control instead of specifying the required output and boundaries.
- Arbitrary model/effort escalation from a vague importance or sensitivity label; documented consequence may select quality priority only through the allocation owner.
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
