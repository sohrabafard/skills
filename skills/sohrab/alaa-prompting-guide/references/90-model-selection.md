# Model Selection and Companion Routing

## Active model routing

For Codex, read `references/12-gpt-6.md` and the exact role profile in
`assets/codex-model-policy.json`. That file alone owns executable Codex pins and rationales;
this page does not reproduce them. Use `references/50-effort-and-thinking.md` before changing
one. A historical GPT-5.6 comparison does not authorize a production exception.

For Claude Code, `assets/claude-model-policy.json` alone owns role pins, rationales,
escalation criteria and calibration status. Apply its legacy-replacement rule in `notes` before selection; historical capability snapshots cannot override it. Use current model references for prompting and
`references/41-claude-code-runtime-features.md` for activation limits. Historical references never select current profiles.

## Decision helper

1. **Pick the runtime first.** It determines trigger syntax, harness features, and which model families are even available. Codex defaults to the GPT-6 family; Claude Code means the Claude family.
2. **Within Claude Code**, select the registered role profile. Use the registered Haiku, Sonnet, Opus or Fable role profile; none is an automatic fallback. Historical Sonnet 5 and Haiku 4.5 snapshots authorize no active profile. Restricted models and announced future generations receive no inferred default profile.
3. **Within Codex**, use the registered profile for the role; bounded evidence, routine engineering, and difficult judgment are distinct workloads, with exact pins owned by the policy JSON.
4. **Choose effort separately**, using `references/50-effort-and-thinking.md`. Model and effort are different questions and answering them together produces bad answers to both.
5. **Select directly from the grounded plan.** Read the runtime orchestrator routing matrix, then the exact canonical profile. Classify missing facts for retrieval/clarification before planning. Planning uses strong-workhorse medium/high based on the judgment needed to make the plan; high planning can produce cheap implementation. Ordinary and demanding implementation use their registered workhorse variants. Exceptional implementation requires applicable high-effort workhorse inadequacy after correcting context/specification/tools and considering decomposition, or explicit user direction; complexity or sensitivity alone is insufficient. Reuse applicable prior evidence without a mandatory trial ladder, synthetic benchmark or replay. Record the exact profile and reason before dispatch.
6. **Verify actual controls.** Inline planning requires verified compatible configured controls; otherwise use a registered read-only planner. Pinned custom profiles can override caller controls; prose cannot change the running model. The parent ratifies and owns the durable plan.
7. **Match delegation polarity to the target's bias** before writing delegation language for any model — read `references/06-invocation-and-composition.md` for the rule.
8. **Use the runtime's own `/goal`** for a durable objective; the implementations share a name and nothing else — read `references/11-codex-runtime-features.md` or `references/41-claude-code-runtime-features.md` for which is which.
9. **Route durable multi-phase engagements** with plan, state, and phase artifacts to `/alaa-workflow` rather than duplicating that machinery.

## Companion routing

`/alaa-codex-orchestrator` (Codex) and `/alaa-cc-orchestrator` (Claude Code) are the production multi-agent orchestration packs, each carrying a conditionally routed role catalog for its runtime: core lanes (spec analyst, explorer, researcher, test strategist, implementer with a separate escalated implementer, independent verifier, failure analyst, reviewer, documenter) plus conditionally gated specialists (adversarial review, architecture, security, migration, API contract, dependency audit, accessibility, browser QA, performance, observability, release).

The catalog is a menu rather than a fleet — a typical goal fires three to five roles, because every specialist is gated on a stated condition. Breadth costs nothing per run; imprecise triggers do.

Claude pins are read from `assets/claude-model-policy.json`; executable frontmatter is a checked projection, never a second policy. Standard and deep reviewer scopes share the existing reviewer profile; scope breadth alone does not create a second executable identity.

Codex pins and calibration status are read from `assets/codex-model-policy.json`; the catalog owns role triggers, not a second model policy.

In both packs the lead never implements or runs heavy suites itself, the verifier executes commands under a low-priority resource policy, and no lane approves its own change. Prefer these packs over hand-writing a fan-out; the lead is always the session's own model.

Other companions:

- `/alaa-workflow`: durable multi-phase plans, phase prompts, resumable state, and the implementation-plus-review cadence.
- `/openai-docs`: freshest GPT-6 and Codex guidance when this skill is stale. Use official Anthropic docs for Claude gaps.
- `/alaa-low-noise`: broad prompt research, validation, or long tool-heavy sessions.

## Caveats

Benchmark claims, relative pricing, effort defaults, and the capability ordering among current models are vendor-stated and time-sensitive — a single release can invalidate any ranking here. Re-check `references/00-source-map.md` and the live model pages before treating any ranking here as current.
