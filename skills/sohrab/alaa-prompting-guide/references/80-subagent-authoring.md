# Subagent Authoring and Dispatch

A subagent is a second agent with its own context window, tool set and authority, not a second opinion from the same agent. Define one by pinning four things and letting the runtime enforce them. Prompt one by sending lane facts only, because the definition already owns the role. This file covers Claude Code markdown agents and Codex agent TOMLs.

## When a subagent is the right tool

When you must choose between an inline instruction, a skill, a script and a subagent, read `references/60-skill-authoring.md` *Should this be a skill at all?*; it holds the test and the three conditions that justify a subagent. The condition that nothing else satisfies, judgment by an agent that did not produce the work, is the subject of *Authority boundaries beat instructions* below.

## Definition files

### Claude Code: markdown with YAML frontmatter

Project agents live in `.claude/agents/`, user agents in `~/.claude/agents/`; both directories are scanned recursively, and identity comes only from the `name` field, not the path. Project directories are discovered by walking up from the working directory; when more than one nested directory defines the same `name`, the definition closest to the working directory wins. Managed definitions deployed by administrators take precedence over project and user definitions with the same name. Both directories are watched, so an edit takes effect on the next delegation without a restart.

Only `name` and `description` are required. The documented optional fields are `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `autoCompactWindow`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `omitClaudeMd`, `effort`, `isolation`, `color`, `initialPrompt`, and `experimental`. An unrecognized field is ignored without an error. The field list and that rule were verified 14 November 2026; several fields are version-gated. The markdown body below the frontmatter becomes the subagent's system prompt, and only that: a subagent receives its own system prompt plus basic environment details, not the full Claude Code system prompt and not the parent's conversation history.

`alaa-reviewer` is the worked example. Its model-neutral metadata are checked against `assets/claude-model-policy.json`. It declares `tools: Read, Glob, Grep, Bash` and a `skills:` list preloading the clean-code and security references the reviewer must apply. `Write` and `Edit` are absent. The description states the role and ends with the boundary: "Never edits or fixes." Native tools, Bash command permissions and MCP grants must all preserve that boundary; omitting Write and Edit alone is insufficient.

### Codex: standalone TOML

Personal agents live in the active Codex home `agents/` directory (`~/.codex/agents/` by default), project agents in `.codex/agents/`, one file per agent. Required keys are `name`, `description`, and `developer_instructions`. Optional keys are `nickname_candidates`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and `skills.config`. `sandbox_mode` accepts `"read-only"` and `"workspace-write"`, and inherits from the parent when omitted.

**`skills.config` is not the Codex equivalent of Claude's `skills:` preload; never use it as one.** It is `[ { path = "…", enabled = true } ]`, an enable or disable override naming a directory that contains a `SKILL.md`. It selects which skills an agent may use and never injects one into the agent's context. Each entry carries a filesystem path, so a committed definition would hard-code one machine's layout. Codex documents no per-agent preload. Where a Codex lane must apply doctrine, name the files in `developer_instructions` and let the lane read them from the installed skills path.

Managed Codex authority roles omit executable model and effort pins. `assets/codex-model-policy.json` checks their identity and capability contract. Explicit task spawn controls require a verified compatible runtime. A stale or custom TOML pin overrides the caller's settings; read `references/11-codex-runtime-features.md` before you assume an override.

The two runtimes express the same four decisions with different key names. A cross-runtime pack ships both files from one `agents/` directory and installs the right one per runtime.

## The four things every definition pins

**One role with a hard authority boundary.** An agent that reviews *and* fixes will fix, because the model resolves ambiguity toward action. Pick the verb and enforce it in configuration.

**Task control realization without role defaults.** Managed definitions omit both model and effort. The delegating parent supplies explicit task controls from its runtime orchestrator's allocation procedure, and the capability policy checks that they are supported. Verify the loaded definitions and the effective overrides separately from the observed identity. A pair changes no role authority. Main-session configuration remains external.

**The tools it may use.** Claude Code grants every tool available to subagents when `tools` is omitted, so omission grants everything, usually wrongly. `disallowedTools` subtracts from the inherited pool when a narrow allowlist would be brittle. Codex expresses the coarser cut through `sandbox_mode`.

**A rigid output contract the caller can parse.** Covered below.

## Authority boundaries beat instructions

Restrict tools through configuration, then verify the effective boundary. A native read-only sandbox does not restrict server-side MCP mutation, and Bash can expose writes even when the native edit tools are omitted. Inspect the parent overrides and the effective grants, and withhold mutation-capable tools before you claim a read-only boundary. Prose describes the intended authority but cannot prove it.

Current Claude prompting guidance supports removing generic, repeated self-check reminders. It does not authorize removing a required test, an unresolved-failure check or another role's acceptance responsibility. Judge each instruction by the responsibility it enforces; a model upgrade alone cannot make a verification step redundant.

An independent verifier must stay, because **no lane may approve its own change**. That is a structural property of the pipeline, not a request for more diligence. In the orchestrator packs, `alaa-verifier`, `alaa-reviewer` and the specialists are authority boundaries, and a gate is never skipped because the work already looks verified. Keep focused implementer validation and independent acceptance gates. Remove repeated checks only when no change, failure or unresolved concern justifies them. A distinct checker has an authority-boundary purpose when it owns independent acceptance criteria.

A second agent with no independent acceptance responsibility is redundant. A reviewer or verifier evaluating another lane against its own declared gate remains an authority boundary.

## Output contracts

The orchestrator must route on a subagent's return without re-reading the work, so the output format is a machine interface and must be as rigid as one. It has four elements:

1. **A fixed first-line verdict token.** `alaa-reviewer` mandates a first line of exactly `VERDICT: APPROVED`, `VERDICT: APPROVED-WITH-NITS`, or `VERDICT: CHANGES-REQUESTED`. A fixed position and a closed vocabulary let the caller branch on a token, which makes the review gate mechanical.
2. **Findings with severity and confidence.** `alaa-reviewer` requires one finding per line with file:line, severity `blocker|major|minor|nit`, confidence 0–1, the failure, the evidence and a concrete fix. Per-finding severity and confidence let the *caller* filter; otherwise the agent filters, and a finding it withholds never reaches the pipeline. So instruct the reviewer to report everything it finds, including low-confidence items, and let the downstream step rank.
3. **An evidence section.** `GATE EVIDENCE` in the reviewer's contract lists the files, diffs, commands, tests and documents actually inspected. It turns "I reviewed it" into a checkable claim the lead can audit against real tool results.
4. **An explicit statement of what was not assessed.** `RISKS`, residual concerns, unrun checks and boundary conflicts. Without it, a clean verdict on a partial pass looks like a clean verdict on a full one.

Keep contracts non-overlapping across the roster. `alaa-reviewer`'s definition disclaims the adversarial lens explicitly, so no two agents half-own one judgment and leave a gap between them.

## Configuration and observed identity

Record requested role, model, and effort separately from observed runtime model and effort.
When the host does not expose an observed value, report `unknown`; never repeat a pin as proof
of identity. Flag only observable mismatches. Put metadata after a required first-line verdict,
so a report cannot demand two different first lines. A replacement-only contract, including
`alaa-rule-writer`, emits no metadata; its caller records requested settings in the roster.

Model resolution differs by runtime. Read `references/11-codex-runtime-features.md` for Codex
pin precedence and `references/41-claude-code-runtime-features.md` for Claude configuration.
Neither runtime's precedence proves the model that actually served a response.

## Task model and effort independent of authority role

For the actual task choice, read the runtime orchestrator's allocation procedure. For capability and source evidence, read `references/90-model-selection.md`; it also states what selects no pair. The matching `alaa-codex-orchestrator references/model-effort-policy.md` or `alaa-cc-orchestrator references/model-effort-policy.md` owns the normalization of omitted fields. Accept its resolved defaults before you validate capabilities and controls. Both normalized controls must be explicit and realized. When the configured control resolution is verified, an unresolved serving identity can remain unknown. No normal dispatch requires paid calibration.

## Prompting a subagent once defined

A Claude Code subagent starts with a fresh, isolated context window: it does not see the conversation history, the skills already invoked or the files already read. Only a fork inherits the parent. Everything the lane needs must therefore be in the dispatch, and nothing else.

The dispatch carries **lane facts only**: the one concrete outcome; the owned files and modules; explicit exclusions; acceptance criteria; the exact verification commands with working directory and timeout; dependencies on other lanes; and the explicit task model and effort with control-resolution evidence. A compact dispatch suffices when no durable plan is admitted. The dispatch does not carry the role, the tool inventory, the general engineering philosophy or decorative examples, because the definition owns them and restating them dilutes both. Measure quality after you change a dispatch.

Name the *one* skill the lane needs rather than pre-loading every clean-code skill into every lane. Use one agent per owned lane. Add independent review or verification through the declared gate triggers, not through an unbounded request to double-check.

## Delegation polarity

When you calibrate how readily a lane should delegate on a given target model, read `references/06-invocation-and-composition.md`; it owns the polarity rule and the per-model bias.

Claude Code enables subagent nesting by default, up to three layers below the main conversation (verified 14 November 2026). A definition that omits `tools` inherits `Agent`. A role that must not fan out omits `Agent` from `tools` or lists it in `disallowedTools`; `references/41-claude-code-runtime-features.md` owns the caps.

## Defects and fixes

| Defect | Symptom | Fix |
|---|---|---|
| Boundary stated only in prose | A reviewer edits files | Remove write tools from `tools`, or set `sandbox_mode = "read-only"` |
| `tools` omitted "for flexibility" | Agent inherits everything and wanders | List the tools the role needs; use `disallowedTools` when an allowlist is brittle |
| Free-form output | Orchestrator re-reads the work to route on it | Fixed first-line verdict token from a closed vocabulary |
| Findings without severity or confidence | Agent self-filters; findings never reach the caller | Require severity and confidence per finding; instruct it to report everything and let the caller rank |
| No coverage statement | A clean verdict on a partial pass looks like a full pass | Require an explicit "not assessed" or residual-risk section |
| Overlapping roles | Two agents half-own a judgment; a gap opens between them | Disclaim the adjacent lens by name in each definition |
| Redundancy mistaken for a gate | An agent spawned to double-check another agent | Delete it; keep only boundaries where a different agent judges a different agent's work |
| Repeated verification without cause | Same check repeated despite no change or unresolved concern | Remove the repetition; retain focused tests and independent gates |
| Role restated in the dispatch | Long dispatch, diluted lane facts | Dispatch carries outcome, scope, exclusions, criteria, commands, dependencies — nothing else |
| Untested escalation | Model and effort changed without diagnosing failure | Repair missing context/tool/spec facts first; change one factor at a time |
| Invented runtime identity | Configured pins reported as observations | Separate requested and observed values; unknown stays unknown |
| Wrong delegation polarity | Swarm on one runtime, single-threaded on the other | Cap where the default over-delegates; authorize where it under-delegates |

## Checklist

1. The work genuinely needs a separate context, a different tool set or an authority boundary; otherwise it is an inline instruction, a skill or a script.
2. The definition uses only documented keys for its runtime, and the required keys are present.
3. One role, one verb, and `tools`, `disallowedTools` or `sandbox_mode` enforce the boundary, not a sentence. Effective permissions and MCP grants are checked.
4. Managed roles are model-neutral; each task explicitly supplies both supported controls and verifies their effective realization without changing authority.
5. The description states when to delegate to this agent and where its lens ends relative to adjacent agents.
6. The output contract fixes a first-line verdict token, per-finding severity and confidence, an evidence section and an explicit statement of what was not assessed.
7. Requested and observed identity are separate; unknown values stay unknown and verdict ordering is preserved.
8. Focused implementer checks and independent gates survive; redundant repeated checking is removed.
9. Dispatch text carries lane facts only and names the one skill the lane needs.
10. Delegation follows current runtime authority and a concrete independent scope; model-specific tuning is source-backed.

## Caveats

Codex pin precedence and shared authority and identity guidance were refreshed 25 September 2026. The Claude nesting default and frontmatter field list were refreshed 14 November 2026. `references/41-claude-code-runtime-features.md` owns current Claude selection precedence. Remaining runtime facts keep their 24 July 2026 verification and must be refreshed before use:

- Claude Code subagent frontmatter fields: several are gated on specific minor versions, including background-by-default and extended-thinking inheritance; check against the running version.
- Codex agent TOML `sandbox_mode`: values beyond `"read-only"` and `"workspace-write"`, and whether a new agent file needs a restart, are unverified.
- Agent-local `skills.config`: `openai/codex` issue 14161 reported it ignored in both directions. The issue is closed against PR 14806, but which released Codex version carries the fix is unverified. Re-check before you rely on a per-agent override; the schema above was read on 8 August 2026.
- Effort-level availability depends on the model, in both runtimes.

## Sources

- [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Subagents (Codex)](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
