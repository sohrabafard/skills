# Dispatch controls, CodeGraph gate and review follow-ups (2026-11-17)

Beads issue: `alaa-m2qgf`, discovered from `alaa-5h8xt`. Base: `main` at `1ab9bb73`. This record is dated evidence; verify current facts before you reuse a conclusion.

## Request

The pack owner relayed three statements of a lead agent that ran an orchestrated task in another repository, and asked for an assessment and the right fix:

1. The lead gave no model in its dispatches, because the allocation rule sits in `references/routing-matrix.md` and the lead never read it.
2. Lanes used CodeGraph almost never and searched with the shell.
3. Three proposals: turn the CodeGraph hint into a gate; a requirement-to-test table per lane with a conformance reviewer; a bootstrap script for a lane worktree and a short allocation table in `SKILL.md`.

The owner also answered the open items of the [8.0.0 record](../agent-roles-by-stack-20261117/report.md).

## Measured

Claude Code transcripts on this workstation. The scripts are in `outputs/20261115-code-intelligence-usage/`; the dispatch count used a one-off script.

| Measure | Value | Window |
|---|---|---|
| Subagents whose tool list held a CodeGraph tool | 1,463 of 1,618 | seven days |
| Subagents whose context held the CodeGraph server instructions | 1,614 of 1,618 | seven days |
| Nudges followed by a CodeGraph call within three calls | 62 of 2,309 | seven days |
| CodeGraph MCP calls by subagents | 58 of 18,587 tool calls | two days |
| Shell search and read calls by subagents | 8,709 | two days |
| Agent dispatches with no model parameter | 209 of 557 | two days |
| Agent dispatches with no effort parameter | 400 of 557 | two days |
| Dispatches to managed roles in sessions that invoked an orchestrator skill, with both controls | 32 of 166 | two days |

Reading: the tool and its instructions reach almost every subagent, and the agents still search with the shell. More instruction text is therefore not the fix for code intelligence. For the dispatch controls the rule existed but only in a reference file.

## Decisions

| Decision | Source |
|---|---|
| Dispatch controls: text only, in the skill body and in one block of the global instruction files; no hook | Owner, this session |
| CodeGraph: a gate per agent, bounded | Owner, this session |
| Incidental file: defined by the acceptance criteria | Owner, this session |
| Control mismatch outside the block causes: one report line, the lane continues | Owner, this session |
| Local merge into `main` and reinstall of both runtimes | Owner, this session |
| Codex resolved-roster check accepts the two roles that other skills own | Owner statement that two other skills manage them |
| "High-effort workhorse" becomes "the strongest non-exceptional model of the table at `high` effort or above" | Lead; step 4 of the same section already sets this bar |
| No conformance reviewer per lane | Lead. The implementation contract already maps each criterion to a test and returns `INCOMPLETE` otherwise; a reviewer per lane is the cycle the owner removed |
| No bootstrap script in this pack | Lead. It is specific to the other repository and belongs there |

## Changes in this repository

Both packs are at version 8.1.0.

- `SKILL.md` *Dispatch controls*: the short form of the fit table, one model and one ordinary effort for each row. `scripts/check_agent_contracts.py` `dispatch_controls_failures` fails when the short form and the fit table disagree; a probe with a changed model and a changed effort confirmed that it fails.
- Every definition: a `CONTROL MISMATCH:` line for an observed pair other than the dispatched one, outside the three block causes. `references/agent-catalog.md` *Return header* states the lead's action.
- `references/routing-matrix.md`: the incidental-file definition and the exceptional-model wording.
- Codex `scripts/check_agent_grants.py`: `EXTERNAL_ROLES`. The resolved check exits `0` on the installed directory and still exits `1` when a retired role file is present (probed with a copy of the directory).

## Changes outside this repository

Source: the setup pack in the documentation repository, `vibe coding/setup`. Installed copies: the Claude and Codex homes.

- `hooks/codegraph-nudge.py`, one script for both runtimes. Until an agent has made one CodeGraph call, a shell search or read of indexed code is denied, at most twice for that agent; afterwards the hook nudges as before. It never blocks a file with a non-code extension, a repository without an index, or a command that first changes into such a repository. It fails open. Fifteen behaviour cases passed against the script before it was copied.
- Claude Code `settings.json`: one more `PreToolUse` entry, for `mcp__codegraph__.*`, so that the hook sees a CodeGraph call.
- Codex `hooks.json`: a `PreToolUse` entry for `Bash|mcp__codegraph__.*`. Codex passes no agent identifier to this event (hooks page, read 2026-11-17), so the count is per session. Codex skips a new or changed hook until the user trusts it with `/hooks`.
- `CLAUDE.md` and `AGENTS.md`: a *Subagent dispatch controls* block between its own markers. It points at the skill's short table and holds no model name. The CodeGraph block is unchanged.

Hook facts were read on 2026-11-17 from the Claude Code hooks page (`agent_id` and `agent_type` in the input inside a subagent; `permissionDecision: "deny"` shows its reason to the model; tool events fire inside subagents) and from the Codex hooks page (regex matcher; the same deny shape; no agent identifier on `PreToolUse`).

## Limits

- No session has run with the gate or the short table yet. Remeasure with the same scripts after a week: nudge follow-through, CodeGraph calls by subagents, and dispatches without a control.
- The gate classifies by file extension. A code search whose pattern holds a dot and that names no code file passes ungated.
- A dispatch made by the Workflow tool does not pass through the Agent call and is not covered by the text rule's measurement.
- The Codex input shape for a shell command was taken from the hooks page; no Codex session exercised the hook.
