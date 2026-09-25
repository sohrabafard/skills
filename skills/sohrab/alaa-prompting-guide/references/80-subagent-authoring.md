# Subagent Authoring and Dispatch

A subagent is a second agent with its own context window, its own tool set, and its own authority — not a second opinion from the same one. Defining one well is a matter of pinning four things and letting the runtime enforce them; prompting one well is a matter of sending lane facts and nothing else, because the definition already owns the role. This file covers both, for Claude Code markdown agents and Codex agent TOMLs.

## When a subagent is the right tool

Four mechanisms overlap here, and the cost of choosing wrong is high in both directions — an unnecessary subagent multiplies latency and tokens, a missing one collapses an authority boundary.

- **An inline instruction** is right when the current agent has the context and the authority to do the work and would finish in a handful of tool calls. Delegating that is pure overhead.
- **A skill** is right when you want to change *how the current agent behaves* for a class of task. Skills and subagents compose: a subagent definition can preload skills so the specialist carries the same clean-code rules the lead would have applied.
- **A deterministic workflow script** is right when the steps are fixed and the judgment content is zero. A script that runs the same four commands in the same order is more reliable than any agent asked to run them, and it costs no tokens.
- **A subagent** is right when at least one of three conditions holds: the work would flood the caller's context with search results, logs, or file contents it will never reference again; the work needs a *different tool set* than the caller has, particularly a narrower one; or the work must be judged by something that is not the thing that produced it.

The third condition is the one that cannot be satisfied any other way, and it is the subject of the authority-boundary section below.

## Definition files

### Claude Code: markdown with YAML frontmatter

Project agents live in `.claude/agents/`, user agents in `~/.claude/agents/`; both directories are scanned recursively, and identity comes only from the `name` field, not the path. Project directories are discovered by walking up from the working directory, and when more than one nested directory defines the same `name`, the definition closest to the working directory wins. Managed definitions deployed by administrators take precedence over project and user definitions with the same name. Both directories are watched, so an edit takes effect on the next delegation without a restart.

Only `name` and `description` are required. The documented optional fields are `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`, and `initialPrompt`. The markdown body below the frontmatter becomes the subagent's system prompt — and only that: a subagent receives its own system prompt plus basic environment details, not the full Claude Code system prompt and not the parent's conversation history.

`alaa-reviewer` is the worked example. Its model and effort metadata are checked against `assets/claude-model-policy.json`; it declares `tools: Read, Glob, Grep, Bash` and a `skills:` list preloading the clean-code and security references the reviewer must apply. Note what is absent: `Write` and `Edit`. The description states the role and closes with the boundary in three words — "Never edits or fixes." Native tools, Bash command permissions, and MCP grants must all preserve that boundary; omitting Write and Edit alone is insufficient.

### Codex: standalone TOML

Personal agents live in `~/.codex/agents/`, project agents in `.codex/agents/`, one file per agent. Required keys are `name`, `description`, and `developer_instructions`. Optional keys are `nickname_candidates`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and `skills.config`. `sandbox_mode` accepts `"read-only"` and `"workspace-write"`, and inherits from the parent when omitted.

**`skills.config` is not the Codex equivalent of Claude's `skills:` preload, and reaching for it as one is the mistake to avoid.** It is `[ { path = "…", enabled = true } ]`: an enable/disable override naming a directory that contains a `SKILL.md`. It selects which skills an agent may use; it never injects one into the agent's context the way a preload does, and each entry carries a filesystem path, so a committed definition would hard-code one machine's layout. Codex documents no per-agent preload at all. Where a Codex lane must apply doctrine, name the files in `developer_instructions` and let it read them from the installed skills path.

The executable Codex pin for each role is owned by `assets/codex-model-policy.json` and checked
against its TOML wrapper. `alaa-implementer-sol` retains its historical role identifier for
compatibility; it denotes difficult implementation, not a model promise. Custom TOML model and
effort pins override dispatch parameters. Read `references/11-codex-runtime-features.md` before
selecting a different profile or relying on parent inheritance.

The two runtimes express the same four decisions with different key names. A cross-runtime pack ships both files from one `agents/` directory and installs the right one per runtime.

## The four things every definition pins

**One role with a hard authority boundary.** An agent that reviews *and* fixes will fix, because fixing feels like progress and the model resolves ambiguity toward action. Pick the verb and enforce it in configuration.

**A model and supported effort appropriate to the role.** Read the runtime's structured policy
and check executable metadata against it. Pins express intent; check version-dependent
overrides and observed identity before claiming they took effect. Omit effort for models
without that parameter.

**The tools it may use.** Claude Code inherits every tool available to subagents when `tools` is omitted, so omission is a decision to grant everything — usually the wrong one. `disallowedTools` subtracts from the inherited pool when a narrow allowlist would be brittle. Codex expresses the coarser cut through `sandbox_mode`.

**A rigid output contract the caller can parse.** Covered below.

## Authority boundaries beat instructions

Use configuration to restrict tools, then verify the effective boundary. A native read-only
sandbox does not restrict server-side MCP mutation; Bash may also expose writes despite omitted
native edit tools. Inspect parent overrides and effective grants, and withhold mutation-capable
tools before claiming read-only. Prose describes the intended authority but cannot prove it.

Current Claude prompting guidance supports removing generic, repeated self-check reminders.
It does not authorize removing a required test, unresolved-failure check or another role's
acceptance responsibility. Judge each instruction by the responsibility it enforces; a model
upgrade alone cannot establish that a verification step is redundant.

An independent verifier is a categorically different thing, and must not go. It exists because **no lane may approve its own change** — a structural property of the pipeline, not a request for more diligence. The orchestrator packs state this directly: `alaa-verifier`, `alaa-reviewer`, and the specialists are authority boundaries, and a gate is never skipped on the grounds that the work already looks verified. Keep focused implementer validation and independent acceptance gates. Remove repeated checks only when no change, failure, or unresolved concern justifies them. A distinct checker has an authority-boundary purpose when it owns independent acceptance criteria.

A second agent with no independent acceptance responsibility is redundant. A reviewer or verifier evaluating another lane against its own declared gate remains an authority boundary.

## Output contracts

A subagent's return value is consumed by an orchestrator that must route on it without re-reading the work. That makes the output format a machine interface, and it should be as rigid as one. Four elements:

1. **A fixed first-line verdict token.** `alaa-reviewer` mandates a first line of exactly `VERDICT: APPROVED`, `VERDICT: APPROVED-WITH-NITS`, or `VERDICT: CHANGES-REQUESTED`. Fixed position and a closed vocabulary mean the caller branches on a token rather than on an interpretation of a paragraph, which is what makes the review gate mechanical instead of conversational.
2. **Findings with severity and confidence.** `alaa-reviewer` requires one finding per line carrying file:line, severity `blocker|major|minor|nit`, confidence 0–1, the failure, the evidence, and a concrete fix. Severity and confidence on each finding are what let the *caller* filter; without them the agent filters, and a finding it withholds is one the pipeline never sees. This is why the reviewer is instructed to report everything it finds, including low-confidence items, and let the downstream step rank.
3. **An evidence section.** `GATE EVIDENCE` in the reviewer's contract: the files, diffs, commands, tests, and documents actually inspected. This converts "I reviewed it" into a checkable claim and is what allows the lead to audit every reported claim against a real tool result.
4. **An explicit statement of what was not assessed.** `RISKS`, residual concerns, unrun checks, boundary conflicts. Absence of a finding means nothing unless coverage is stated; without this section, a clean verdict on a partial pass is indistinguishable from a clean verdict on a full one.

Contracts must also be non-overlapping across the roster. `alaa-reviewer`'s definition ends by disclaiming the adversarial lens explicitly, which prevents two agents from both half-owning the same judgment and leaving a gap between them.

## Configuration and observed identity

Record requested role, model, and effort separately from observed runtime model and effort.
When the host does not expose an observed value, report `unknown`; never repeat a pin as proof
of identity. Flag only observable mismatches. Put metadata after a required first-line verdict,
so a report cannot demand two different first lines. A replacement-only contract, including
`alaa-rule-writer`, emits no metadata; its caller records requested settings in the roster.

Model resolution differs by runtime. Read `references/11-codex-runtime-features.md` for Codex
pin precedence and `references/41-claude-code-runtime-features.md` for Claude configuration.
Neither runtime's precedence proves the model that actually served a response.

## Choosing model and effort per role

Read `references/50-effort-and-thinking.md` for the decision procedure and
`assets/codex-model-policy.json` for Codex pins or `assets/claude-model-policy.json` for Claude pins. Choose by unresolved judgment and task evidence;
model and effort are different variables. A registered profile is a starting hypothesis until
comparative evidence supports it. Do not transfer an API effort, a previous generation's ceiling,
or a dispatch override assumption into a custom-agent definition.

## Prompting a subagent once defined

A Claude Code subagent starts with a fresh, isolated context window: it does not see the conversation history, the skills already invoked, or the files already read. The only exception is a fork, which inherits the parent. Everything the lane needs must therefore be in the dispatch — and nothing else should be.

The dispatch carries **lane facts only**: the one concrete outcome; the owned files and modules; explicit exclusions; acceptance criteria; the exact verification commands with working directory and timeout; and dependencies on other lanes. It does not carry the role, the tool inventory, the general engineering philosophy, or decorative examples. The definition already owns those, and restating them dilutes both — the dispatch should add task facts rather than duplicate the role contract; measure quality after changing it.

Two dispatch rules follow from the same place. Name the *one* skill the lane needs rather than pre-loading every clean-code skill into every lane. Use one agent per owned lane. Add independent review or verification through the declared gate triggers, not an unbounded request to double-check.

## Delegation polarity

When calibrating how readily a lane should delegate to subagents on a given target model, read `references/06-invocation-and-composition.md`, which owns the polarity rule and the per-model bias table.

Claude Code disables subagent nesting by default — a subagent cannot spawn subagents unless nesting is enabled — so fan-out depth is a runtime property, not only a prompting one.

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
| Untested escalation | Model and effort changed without diagnosing failure | Repair missing context/tool/spec facts first; compare one factor at a time |
| Invented runtime identity | Configured pins reported as observations | Separate requested and observed values; unknown stays unknown |
| Wrong delegation polarity | Swarm on one runtime, single-threaded on the other | Cap where the default over-delegates; authorize where it under-delegates |

## Checklist

1. The work genuinely needs a separate context, a different tool set, or an authority boundary — otherwise it is an inline instruction, a skill, or a script.
2. The definition uses documented keys only for its runtime, and required keys are present.
3. One role, one verb, and the boundary is enforced by `tools` / `disallowedTools` / `sandbox_mode` rather than by a sentence; effective permissions and MCP grants are checked.
4. Model and effort are pinned from the judgment required and the search needed, against the canonical local policy and supported runtime pairs.
5. The description states when to delegate to this agent and where its lens ends relative to adjacent agents.
6. The output contract fixes a first-line verdict token, per-finding severity and confidence, an evidence section, and an explicit statement of what was not assessed.
7. Requested and observed identity are separate; unknown values stay unknown and verdict ordering is preserved.
8. Focused implementer checks and independent gates survive; redundant repeated checking is removed.
9. Dispatch text carries lane facts only, and names the one skill the lane needs.
10. Delegation follows current runtime authority and a concrete independent scope; model-specific tuning is source-backed.

## Caveats

Codex pin precedence and shared authority/identity guidance refreshed 25 September 2026. Current Claude selection precedence is owned by `references/41-claude-code-runtime-features.md`. Remaining runtime facts retain their 24 July 2026 verification and must be refreshed before use:

- Claude Code subagent frontmatter fields — several are gated on specific minor versions, including background-by-default and extended-thinking inheritance; check against the running version.
- Codex agent TOML `sandbox_mode` — values beyond `"read-only"` and `"workspace-write"`, and whether adding an agent file requires a restart, are unverified.
- Agent-local `skills.config` — `openai/codex` issue 14161 reported it ignored in both directions, so neither `enabled = false` nor `enabled = true` took effect per agent. The issue is closed against PR 14806, but which released Codex version carries the fix is unverified. Re-check before relying on a per-agent override; the schema above was read on 8 August 2026.
- Effort-level availability — depends on the model, in both runtimes.

## Sources

- [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Subagents (Codex)](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
