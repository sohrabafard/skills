# Model Selection and Companion Routing

## Active model routing

For Codex, read `references/12-gpt-6.md` and the exact role profile in
`assets/codex-model-policy.json`. That file alone owns executable Codex pins and rationales;
this page does not reproduce them. Use `references/50-effort-and-thinking.md` before changing
one. A historical GPT-5.6 comparison does not authorize a production exception.

For Claude Code, `assets/claude-model-policy.json` alone owns role pins, rationales,
escalation criteria and calibration status. Use current model references for prompting and
`references/41-claude-code-runtime-features.md` for activation limits. Historical references
never select a current profile.

## Decision helper

1. **Pick the runtime first.** It determines trigger syntax, harness features, and which model families are even available. Codex defaults to the GPT-6 family; Claude Code means the Claude family.
2. **Within Claude Code**, select the registered role profile. Compare Fable or Haiku only in an explicitly authorized, representative evaluation; neither is an automatic local fallback. Restricted models and announced future generations receive no inferred default profile.
3. **Within Codex**, use the registered profile for the role; bounded evidence, routine engineering, and difficult judgment are distinct workloads, with exact pins owned by the policy JSON.
4. **Choose effort separately**, using `references/50-effort-and-thinking.md`. Model and effort are different questions and answering them together produces bad answers to both.
5. **Diagnose before escalation.** Use unresolved judgment and observed quality gaps, after excluding missing context, broken tools and ambiguous specifications. Record the reason in the policy. A later gate does not establish that a weaker starting profile is sufficient.
6. **Match delegation polarity to the target's bias** before writing delegation language for any model — read `references/06-invocation-and-composition.md` for the rule.
7. **Use the runtime's own `/goal`** for a durable objective; the implementations share a name and nothing else — read `references/11-codex-runtime-features.md` or `references/41-claude-code-runtime-features.md` for which is which.
8. **Route durable multi-phase engagements** with plan, state, and phase artifacts to `/alaa-workflow` rather than duplicating that machinery.

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
