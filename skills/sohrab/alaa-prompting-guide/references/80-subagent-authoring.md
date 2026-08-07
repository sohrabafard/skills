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

`alaa-reviewer` is the worked example. Its frontmatter pins `model: opus`, `effort: xhigh`, `tools: Read, Glob, Grep, Bash`, and a `skills:` list preloading the clean-code and security references the reviewer must apply. Note what is absent: `Write` and `Edit`. The description states the role and closes with the boundary in three words — "Never edits or fixes." The `tools` list makes that true whether or not the model reads the sentence.

### Codex: standalone TOML

Personal agents live in `~/.codex/agents/`, project agents in `.codex/agents/`, one file per agent. Required keys are `name`, `description`, and `developer_instructions`. Optional keys are `nickname_candidates`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and `skills.config`. `sandbox_mode` accepts `"read-only"` and `"workspace-write"`, and inherits from the parent when omitted.

**`skills.config` is not the Codex equivalent of Claude's `skills:` preload, and reaching for it as one is the mistake to avoid.** It is `[ { path = "…", enabled = true } ]`: an enable/disable override naming a directory that contains a `SKILL.md`. It selects which skills an agent may use; it never injects one into the agent's context the way a preload does, and each entry carries a filesystem path, so a committed definition would hard-code one machine's layout. Codex documents no per-agent preload at all. Where a Codex lane must apply doctrine, name the files in `developer_instructions` and let it read them from the installed skills path.

`alaa-implementer-sol` is the worked example: `model = "gpt-5.6-sol"`, `model_reasoning_effort = "high"`, `sandbox_mode = "workspace-write"`, and a `developer_instructions` heredoc carrying the role, the skills to apply per ecosystem, the scope rule ("Edit only declared scope; report boundary conflicts instead of crossing them"), the design discipline, the identity line, and a seven-part output contract. The write authority is granted in configuration, not requested in prose — and the read-only agents in the same pack differ from it by exactly one key.

The two runtimes express the same four decisions with different key names. A cross-runtime pack ships both files from one `agents/` directory and installs the right one per runtime.

## The four things every definition pins

**One role with a hard authority boundary.** An agent that reviews *and* fixes will fix, because fixing feels like progress and the model resolves ambiguity toward action. Pick the verb and enforce it in configuration.

**A model and effort appropriate to the role.** Pinned in the definition so every dispatch inherits the same tier and a caller cannot accidentally run a security review on a cheap tier.

**The tools it may use.** Claude Code inherits every tool available to subagents when `tools` is omitted, so omission is a decision to grant everything — usually the wrong one. `disallowedTools` subtracts from the inherited pool when a narrow allowlist would be brittle. Codex expresses the coarser cut through `sandbox_mode`.

**A rigid output contract the caller can parse.** Covered below.

## Authority boundaries beat instructions

A reviewer told not to write is a reviewer that will not write most of the time. A reviewer whose `tools` list contains no write tool is a reviewer that *cannot* write, and the difference is the difference between a strong default and a guarantee. The same holds for `sandbox_mode = "read-only"` under Codex. Prefer configuration to prose wherever the runtime offers a key, and use prose only for the part configuration cannot express.

The same principle keeps an independent verification gate alive even though most self-checking instructions are redundant. Anthropic's Opus 5 guidance is unambiguous that explicit re-check instructions — "double-check your answer," "re-verify before responding," "include a final verification step," "use a subagent to verify" — cause over-verification and should be removed, because the model already catches and fixes its own mistakes. Those instructions are redundant and must go.

An independent verifier is a categorically different thing, and must not go. It exists because **no lane may approve its own change** — a structural property of the pipeline, not a request for more diligence. The orchestrator packs state this directly: `alaa-verifier`, `alaa-reviewer`, and the specialists are authority boundaries, and a gate is never skipped on the grounds that the work already looks verified. The test that separates the two cases: if the same agent that produced the artifact is being asked to look at it again, delete the instruction; if a *different* agent with fresh context and no stake in the outcome is being asked to judge it, keep the gate. Removing the first is a tightening. Removing the second is a loss of control.

The corollary is that a subagent whose only job is to double-check another subagent's output is not a boundary — it is redundancy wearing a boundary's clothes, and both packs list it as an anti-pattern.

## Output contracts

A subagent's return value is consumed by an orchestrator that must route on it without re-reading the work. That makes the output format a machine interface, and it should be as rigid as one. Four elements:

1. **A fixed first-line verdict token.** `alaa-reviewer` mandates a first line of exactly `VERDICT: APPROVED`, `VERDICT: APPROVED-WITH-NITS`, or `VERDICT: CHANGES-REQUESTED`. Fixed position and a closed vocabulary mean the caller branches on a token rather than on an interpretation of a paragraph, which is what makes the review gate mechanical instead of conversational.
2. **Findings with severity and confidence.** `alaa-reviewer` requires one finding per line carrying file:line, severity `blocker|major|minor|nit`, confidence 0–1, the failure, the evidence, and a concrete fix. Severity and confidence on each finding are what let the *caller* filter; without them the agent filters, and a finding it withholds is one the pipeline never sees. This is why the reviewer is instructed to report everything it finds, including low-confidence items, and let the downstream step rank.
3. **An evidence section.** `GATE EVIDENCE` in the reviewer's contract: the files, diffs, commands, tests, and documents actually inspected. This converts "I reviewed it" into a checkable claim and is what allows the lead to audit every reported claim against a real tool result.
4. **An explicit statement of what was not assessed.** `RISKS`, residual concerns, unrun checks, boundary conflicts. Absence of a finding means nothing unless coverage is stated; without this section, a clean verdict on a partial pass is indistinguishable from a clean verdict on a full one.

Contracts must also be non-overlapping across the roster. `alaa-reviewer`'s definition ends by disclaiming the adversarial lens explicitly, which prevents two agents from both half-owning the same judgment and leaving a gap between them.

## The identity line

Every agent in both production packs opens its final report with one line naming itself, its model, and its effort — `AGENT: alaa-reviewer | MODEL: Opus 5 | EFFORT: xhigh` — and is instructed that if the session is actually running a different model or effort than the pin, it must state the real values and flag the difference.

This matters because every layer between the pin and the run can silently change it. Claude Code resolves a subagent's model from an environment variable, then a per-invocation parameter, then the frontmatter, and skips any value excluded by an organization's `availableModels` allowlist, falling back to the inherited model. An agent pinned to `opus` can therefore run on something else with nothing in the transcript saying so. The identity line makes that visible at the only moment it can be caught, and the orchestrator's roster — one line per dispatched agent, with the self-reported identity and any mismatch flagged — turns a per-agent report into a per-goal audit.

## Choosing model and effort per role

`50-effort-and-thinking.md` owns the full decision procedure. The short version is three rules.

**Pick the model from the kind of judgment required**, not from the importance of the task. Design decisions, security reasoning, and adversarial review need the top tier; mechanically applying an already-ratified decision does not, on any surface, because sensitive surfaces already receive top-tier scrutiny at the gates.

**Pick the effort from how much search that judgment needs.** A deterministic command run is low; a wide investigation is high. Both runtimes expose effort as the primary cost and latency control — Claude Code's `effort` field accepts `low`, `medium`, `high`, `xhigh`, and `max` with availability depending on the model, and Anthropic's Opus 5 guidance names `xhigh` as the recommended starting point for coding and agentic work.

**Change the model rather than raising effort past a tier's ceiling.** A lane that needs more than its model's ceiling does not need a higher effort on that model; it needs the next model up. Both packs encode this as a hard rule — Sonnet's ceiling is `high` in the Claude pack, Terra's is `high` and Luna's is `medium` in the Codex pack — and both list "raise the effort instead of changing the model" as an anti-pattern, alongside pinning anything at `max`.

Record the named criterion wherever a pin is escalated, and when uncertain, do not escalate.

## Prompting a subagent once defined

A Claude Code subagent starts with a fresh, isolated context window: it does not see the conversation history, the skills already invoked, or the files already read. The only exception is a fork, which inherits the parent. Everything the lane needs must therefore be in the dispatch — and nothing else should be.

The dispatch carries **lane facts only**: the one concrete outcome; the owned files and modules; explicit exclusions; acceptance criteria; the exact verification commands with working directory and timeout; and dependencies on other lanes. It does not carry the role, the tool inventory, the general engineering philosophy, or decorative examples. The definition already owns those, and restating them dilutes both — the Codex pack states this as a measured effect, not a preference: leaner prompts outperform padded ones on this model generation, so dispatch bloat is a quality regression as well as an expense.

Two dispatch rules follow from the same place. Name the *one* skill the lane needs rather than pre-loading every clean-code skill into every lane. And send one agent per lane — never several agents for the same lane, and never an agent whose job is to check another agent's output.

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
| Self-verification instructions | "Re-check before responding" in the definition | Remove; the model already does this, and the instruction compounds |
| Role restated in the dispatch | Long dispatch, diluted lane facts | Dispatch carries outcome, scope, exclusions, criteria, commands, dependencies — nothing else |
| Effort raised past the ceiling | A mid-tier model at maximum effort on a top-tier problem | Change the model; record the escalation criterion |
| Silent model drift | Reports look fine, results do not match the tier | Require the identity line and audit it in the roster |
| Wrong delegation polarity | Swarm on one runtime, single-threaded on the other | Cap where the default over-delegates; authorize where it under-delegates |

## Checklist

1. The work genuinely needs a separate context, a different tool set, or an authority boundary — otherwise it is an inline instruction, a skill, or a script.
2. The definition uses documented keys only for its runtime, and required keys are present.
3. One role, one verb, and the boundary is enforced by `tools` / `disallowedTools` / `sandbox_mode` rather than by a sentence.
4. Model and effort are pinned from the judgment required and the search needed, with no tier run past its ceiling and nothing pinned at `max`.
5. The description states when to delegate to this agent and where its lens ends relative to adjacent agents.
6. The output contract fixes a first-line verdict token, per-finding severity and confidence, an evidence section, and an explicit statement of what was not assessed.
7. The identity line is mandated, with instructions to flag any mismatch against the pin.
8. No self-verification instruction survives; every remaining gate is a different agent judging a different agent's work.
9. Dispatch text carries lane facts only, and names the one skill the lane needs.
10. Delegation language matches the target model's documented default bias — cap or authorize, never both, never neither.

## Caveats

Verified 24 July 2026. Values that move between releases:

- Claude Code subagent frontmatter fields — several are gated on specific minor versions, including background-by-default and extended-thinking inheritance; check against the running version.
- Codex agent TOML `sandbox_mode` — values beyond `"read-only"` and `"workspace-write"`, and whether adding an agent file requires a restart, are unverified.
- Agent-local `skills.config` — `openai/codex` issue 14161 reported it ignored in both directions, so neither `enabled = false` nor `enabled = true` took effect per agent. The issue is closed against PR 14806, but which released Codex version carries the fix is unverified. Re-check before relying on a per-agent override; the schema above was read on 8 August 2026.
- Effort-level availability — depends on the model, in both runtimes.

## Sources

- [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Subagents (Codex)](https://developers.openai.com/codex/subagents)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
