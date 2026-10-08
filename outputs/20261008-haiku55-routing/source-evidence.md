# Source evidence - 8 October 2026

The lead verified these official sources before ratifying the lane; this writer reused that research rather than duplicating retrieval.

- effort: https://platform.claude.com/docs/en/build-with-claude/effort (verified 2026-10-08); Generation-specific supported effort values; Haiku 5.5 supports effort, historical Haiku 4.5 does not.
- model-config: https://code.claude.com/docs/en/model-config (verified 2026-10-08); Provider mapping, version gates, overrides and fallback.
- subagents: https://code.claude.com/docs/en/sub-agents (verified 2026-10-08); Full-ID metadata and version-dependent precedence.
- haiku-launch: https://www.anthropic.com/claude-haiku-5-5 (verified 2026-10-08); Announced workloads; vendor claims are not local calibration.
- haiku-migration: https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide (verified 2026-10-08); Exact ID, effort, adaptive thinking and disabled/manual API boundaries.
- haiku-prompt: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5 (verified 2026-10-08); Explicit retrieval, checking, completion and bounded dispatch guidance.

Exact Haiku ID claude-haiku-5-5; efforts low/medium/high/xhigh/max, default medium; Code >=2.1.293. API thinking may be disabled through high; Code prevents switching it off. Manual budgets unsupported. Active routing is local starting policy, not a vendor comparative ranking. Profiles remain unrun. No live models, account/access checks, installation, model-quality benchmark or latency measurement ran. Prior Opus/Fable snapshots retain their own source dates.

## Sonnet correction - 8 October 2026

The user clarified that omission did not exclude Sonnet 5.5. Lead-confirmed sources reused without duplicate browsing:

- https://www.anthropic.com/claude-sonnet-5-5: efficient coding; Opus stronger on complex sustained judgment.
- https://platform.claude.com/docs/en/models/sonnet-5-5/overview: exact ID claude-sonnet-5-5; API default high.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 and https://platform.claude.com/docs/en/build-with-claude/effort: medium for well-specified agentic work, high for harder/longer work; five supported effort levels.
- https://code.claude.com/docs/en/model-config: minimum Claude Code 2.1.284.

Eight roles restore Sonnet with existing medium/high efforts. These pins remain unrun hypotheses, not calibrated comparative rankings. Four Haiku, five Fable and seven Opus profiles (including lead) are preserved. No live models, access checks or installation ran.

## Phase 4 - Latest user steering and current catalog

On 2026-10-08 the user required replacing every active Haiku 4.5 selection with Haiku 5.5 and restoring `alaa-implementer-opus`. These are local routing requirements, not claims of model superiority. Preserve the Haiku availability gate and do not silently downgrade.

The current [official model catalog](https://platform.claude.com/docs/en/models/overview) and [Fable model page](https://platform.claude.com/docs/en/models/fable-5-1/overview), read on 2026-10-08, identify `claude-fable-5-1`, alongside `claude-opus-5-5`, `claude-sonnet-5-5` and `claude-haiku-5-5`. Fable 5.5 was not established by these sources. The latest user message typed 5.5 whereas the prior request specified 5.1; clarification was requested while independent work continued.

The model catalog identifies demanding reasoning, long-horizon work and observed Opus higher-effort shortcomings as reasons to consider Fable. Local role admission remains an uncalibrated policy: Sonnet for settled precise implementation; restored Opus for a concrete admitted unresolved engineering decision; Fable for documented demanding coupled stages/invariants or representative Opus higher-effort quality-gap evidence after ruling out context, tools and specification. Only one writer/profile owns a lane. Existing reassessment boundaries and independent gates remain required.

The user subsequently confirmed that Fable 5.1 was intended. The version ambiguity is resolved.

## Phase 5 - Plan-first paired-runtime selection (verified 2026-10-08)

Two independent read-only research lanes verified these current official sources. The chosen lane thresholds and strongest-model admission are local user policy; they are not measured cross-model equivalences or upstream guarantees. No paid model runs or installations occurred.

### Claude evidence

- [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5): medium for specified coding/tool work, high for harder or longer tasks; medium can check in prematurely on long work.
- [Opus prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5): start at medium; higher effort costs more reasoning time/tokens. Effort scales differ across models, so Sonnet-high is not established as equivalent to Opus-medium.
- [Model selection](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) and [model overview](https://platform.claude.com/docs/en/models/overview): everyday coding versus long agentic judgment; Fable targets demanding reasoning and cases where higher-effort Opus falls short. The selection guide mentions xhigh/max; this task deliberately sets the user-requested implementation boundary at diagnosed Opus-high inadequacy or explicit user direction. No extra trial sequence is mandated.
- [Claude Code model controls](https://code.claude.com/docs/en/model-config): medium fits scoped engineering; high can explore more edge cases and make more autonomous choices. Session controls do not authorize an agent to claim it changed its own runtime identity.
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents): named definitions support exact model and effort. Per-invocation model can override frontmatter; no documented Agent per-call effort field was established. Environment effort and organization caps may override a definition. Sonnet API default high and Code default medium differ, so use explicit pins.

### GPT and Codex evidence

- [Codex models](https://learn.chatgpt.com/docs/models): current Sol is the recommended coding/agentic workhorse, Luna fits focused repeatable work and starts at high, Astra fits hardest judgment. Medium suits planning; high suits harder multistep trade-offs.
- [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [older GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol), [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra): API effort support differs from Codex tool support. The observed dispatch schema supports the selected medium/high pairs. Older Sol availability does not justify restoring it as another default tier.
- [Codex subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents): caller/default/parent resolution precedes custom TOML application; explicit TOML model and effort pins win. Passing new caller effort to an old pinned wrapper does not realize a new profile.
- Local configured main settings differ from the source policy; neither is proof of serving identity. Real planner profiles or verified session controls are needed. No installed configuration is changed by this source task.

### Ratification

The existing plan records four direct Claude implementation pairs, narrowly bounded Luna-high plus Sol-medium/high for GPT, and strictly exceptional Fable/Astra. Planning uses Opus or Sol medium/high with one selected planner, then the lead ratifies lane decomposition and actual registered profile selection before implementation. This separates initial selection from later diagnosis and offline calibration; it creates no try/fail ladder.

### GPT implementation floor clarification

The user clarified that normal implementation should not select below Sol. The prior Luna-high mechanical route was the lead's conservative workload inference from focused/repeatable-use guidance, not an official statement that Luna substitutes for Sonnet or is a preferred ordinary implementation model. The shipped task policy therefore keeps Sol medium/high for implementation and Astra only exceptionally, while retaining lightweight non-implementation Luna roles. This is a user-selected boundary; it does not claim the vendor forbids Luna coding. Current gpt-6.1-sol is retained rather than treating the user's generic gpt-6-sol comparison as a request for the older generation.

### Final research-based GPT policy (supersedes the floor clarification)

The user clarified that their experience was input and requested the best researched structure. The official [model-selection guide](https://developers.openai.com/api/docs/guides/model-selection), checked on 2026-10-08, explicitly recommends Luna medium for small existing-file edits and Luna low for fine-grained edits. This is task-specific starting guidance, not proof of an optimal production default.

Final local policy: automatic implementation selects Sol medium/high; optional Luna medium requires explicit human selection for that lane and every bounded existing-file/settled-design/known-pattern/cheap-discriminating-check condition. This retains the documented useful case without silently changing the normal implementation quality/cost preference. Luna remains available for lightweight roles. Neither a coding ban nor cross-vendor equivalence is claimed. Actual calibration and serving identity remain unproven.

## Phase7 - User-authorized automatic mechanical work

The user's response annotations explicitly authorize Luna and Haiku5.5 for exact repeated edits, including finite batches across many files, and preserve their usefulness in existing support roles. This supersedes the prior per-lane human-request-only Luna restriction. The current local policy requires all mechanical fit predicates and preserves independent gates and command authority. Existing official capability research is reused; no new comparative benchmark, cross-family equivalence or calibrated quality claim is made.
