# Subagent Authoring and Dispatch

A subagent is a second agent with its own context window, tool set and authority. A definition pins four things, and the runtime enforces them. A dispatch sends lane facts only, because the definition owns the role. This file covers Claude Code markdown agents and Codex agent TOMLs.

To choose between an inline instruction, a skill, a script and a subagent, read `references/60-skill-authoring.md` *Should this be a skill at all?*.

## Definition files

### Claude Code: markdown with YAML frontmatter

- **Location.** Project agents live in `.claude/agents/`, user agents in `~/.claude/agents/`. Both are scanned recursively and watched, so an edit takes effect on the next delegation without a restart.
- **Identity** comes only from the `name` field, not the path. Project directories are discovered by walking up from the working directory; when nested directories define the same `name`, the one closest to the working directory wins. A managed definition deployed by an administrator wins over a project or user definition of the same name.
- **Fields** (sub-agents page, 14 November 2026; the list was confirmed again 16 November 2026). Required: `name` and `description`. Optional: `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `autoCompactWindow`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `omitClaudeMd`, `effort`, `isolation`, `color`, `initialPrompt` and `experimental`. An unrecognized field is ignored without an error. Several fields are version-gated; check them against the running version.
- **Body.** The markdown below the frontmatter is the subagent's whole system prompt. A subagent receives that prompt plus basic environment details, not the full Claude Code system prompt and not the parent's conversation history.

`alaa-reviewer` is the worked example. It declares `tools: Read, Glob, Grep, Bash` and a `skills:` list that preloads the doctrine every review applies; `Write` and `Edit` are absent. Its description states the role and ends with the boundary: "Never edits or fixes." Its model-neutral metadata are checked against `assets/claude-model-policy.json`.

### Codex: standalone TOML

- **Location.** Personal agents live in the `agents/` directory of the active Codex home (`~/.codex/agents/` by default), project agents in `.codex/agents/`, one file per agent.
- **Keys.** Required: `name`, `description`, `developer_instructions`. Optional: `nickname_candidates`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`. Use only keys the target host supports.
- `sandbox_mode` accepts `"read-only"` and `"workspace-write"` and inherits from the parent when omitted.
- **`skills.config` is not the Codex equivalent of Claude's `skills:` preload; never use it as one.** It is `[ { path = "…", enabled = true } ]`, an enable or disable override that names a directory containing a `SKILL.md`. It selects which skills an agent may use and injects none. Each entry carries a filesystem path, so a committed definition would hard-code one machine's layout. Codex documents no per-agent preload: where a Codex lane must apply doctrine, name the files in `developer_instructions` and let the lane read them from the installed skills path.
- Managed Codex authority roles omit model and effort pins; `assets/codex-model-policy.json` checks their identity and capability contract. A stale or custom TOML pin overrides the caller's settings; read `references/11-codex-runtime-features.md` before you assume an override.

A cross-runtime pack ships both files from one `agents/` directory and installs the right one per runtime.

## The four things every definition pins

1. **One role with a hard authority boundary.** An agent that reviews and fixes will fix, because the model resolves ambiguity toward action. Pick the verb and enforce it in configuration. The description states when to delegate to this agent and where its lens ends against adjacent agents.
2. **No model or effort default.** A managed definition omits both. The delegating parent supplies explicit task controls from its runtime orchestrator's allocation procedure, and the capability policy checks that they are supported. A pair changes no role authority.
3. **The tools it may use.** Claude Code grants every tool available to subagents when `tools` is omitted. `disallowedTools` subtracts from the inherited pool when a narrow allowlist would be brittle. Codex makes the coarser cut through `sandbox_mode`. A role that must not fan out omits `Agent` from `tools` or lists it in `disallowedTools`; `references/41-claude-code-runtime-features.md` owns the nesting and concurrency caps.
4. **An output contract the caller can parse.** See *Output contracts*.

## Authority boundaries beat instructions

- **Restrict tools through configuration, then verify the effective boundary.** Prose describes the intended authority and proves nothing. A native read-only sandbox does not restrict server-side MCP mutation, and Bash can expose writes when the native edit tools are omitted. Before you claim a read-only boundary, inspect the parent overrides and the effective grants, and withhold mutation-capable tools.
- **No lane approves its own change.** That is a structural property of the pipeline, not a request for more diligence. In the orchestrator packs, `alaa-verifier`, `alaa-reviewer` and the specialists are authority boundaries, and a gate is never skipped because the work already looks verified.
- **The authority test for a check.** Judge each verification instruction by the responsibility it enforces. Current Claude guidance supports removing generic, repeated self-check reminders. It authorizes no removal of a required test, an unresolved-failure check or another role's acceptance responsibility, and a model upgrade makes no verification step redundant.
  - Keep focused implementer validation and independent acceptance gates.
  - Remove a repeated check only when no change, failure or unresolved concern justifies it.
  - A second agent with no independent acceptance responsibility is redundant. A reviewer or verifier that judges another lane against its own declared gate is an authority boundary.

## Output contracts

The orchestrator routes on a subagent's return without re-reading the work, so the output format is a machine interface. It has four elements:

1. **A fixed first-line verdict token.** `alaa-reviewer` mandates a first line of exactly `VERDICT: APPROVED`, `VERDICT: APPROVED-WITH-NITS` or `VERDICT: CHANGES-REQUESTED`. A fixed position and a closed vocabulary let the caller branch on a token.
2. **Findings with severity and confidence.** `alaa-reviewer` requires one finding per line with file:line, severity `blocker|major|minor|nit`, confidence 0–1, the failure, the evidence and a concrete fix. Tell the reviewer to report everything it finds, low-confidence items included, and let the caller rank: a finding the agent withholds never reaches the pipeline.
3. **An evidence section.** `GATE EVIDENCE` lists the files, diffs, commands, tests and documents actually inspected, so the lead can audit the claim against real tool results.
4. **What was not assessed.** `RISKS`, residual concerns, unrun checks and boundary conflicts. Without it, a clean verdict on a partial pass reads as a clean verdict on a full one.

Keep contracts non-overlapping across the roster: each definition disclaims the adjacent lens by name, as `alaa-reviewer` disclaims the adversarial lens, so no two agents half-own one judgment.

## Configuration and observed identity

- The caller records the requested role, model and effort in its roster, from its own dispatch. A definition asks the agent for no model or effort line: the agent can rarely observe either, and the caller already holds both.
- An agent reports a control only when runtime evidence shows that the requested pair cannot be realized. It then blocks its lane, after the required first-line token.
- When the host exposes no observed value, the serving identity is `unknown`. Never repeat a pin as proof of identity.
- Model resolution differs by runtime: read `references/11-codex-runtime-features.md` for Codex pin precedence and `references/41-claude-code-runtime-features.md` for Claude. Neither precedence proves which model served a response.

## Task model and effort

| Question | Read |
|---|---|
| The task choice | The runtime orchestrator's allocation procedure |
| Capability and source evidence, and what selects no pair | `references/90-model-selection.md` |
| Normalization of omitted fields | `alaa-codex-orchestrator references/model-effort-policy.md` or `alaa-cc-orchestrator references/model-effort-policy.md`. Accept its resolved defaults before you validate capabilities and controls |

Both normalized controls must be explicit and realized. Verify the loaded definitions and the effective overrides separately from the observed identity. When the configured control resolution is verified, an unresolved serving identity can stay unknown. No normal dispatch requires paid calibration.

## Prompting a defined subagent

A Claude Code subagent starts with a fresh context window: it sees neither the conversation history, nor the skills already invoked, nor the files already read. Only a fork inherits the parent.

- **The dispatch carries lane facts only:** the one concrete outcome; the owned files and modules; explicit exclusions; acceptance criteria; the exact verification commands with working directory and timeout; dependencies on other lanes; and the explicit task model and effort with control-resolution evidence. A compact dispatch suffices when no durable plan is admitted.
- **It carries no role, tool inventory, engineering philosophy or decorative example.** The definition owns them, and a restatement dilutes both.
- **Name the one skill the lane needs.** Never preload every clean-code skill into every lane.
- **Use one agent per owned lane.** Add independent review or verification through the declared gate triggers, not through an unbounded request to double-check.
- After you change a dispatch, measure quality.
- For how readily a lane should delegate on a target model, read `references/06-invocation-and-composition.md`.

## Caveats

Codex pin precedence and the shared authority and identity guidance were refreshed 25 September 2026. Other runtime facts with no date above keep their 24 July 2026 verification; refresh them before use:

- Claude Code frontmatter fields gated on minor versions include background-by-default and extended-thinking inheritance.
- Codex `sandbox_mode` values beyond `"read-only"` and `"workspace-write"`, and whether a new agent file needs a restart, are unverified.
- Agent-local `skills.config`: `openai/codex` issue 14161 reported it ignored in both directions. The issue is closed against PR 14806, but which released Codex version carries the fix is unverified. Re-check before you rely on a per-agent override; the schema above was read on 8 August 2026.
- Effort-level availability depends on the model, in both runtimes.

## Sources

- [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Subagents (Codex)](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
