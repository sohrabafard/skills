# Code-intelligence usage baseline, 2026-11-15

Scope: Claude Code transcripts under the user's Claude projects directory, modified in the seven days
before 2026-11-15 (1,083 files). Codex sessions were counted coarsely only. Every script is read-only.

## Scripts

Run each from the repository root with `python3 -I`. The first takes an optional day count.

- `tool_usage.py [days]`: tool calls by scope, agent type, worktree and target type.
- `availability_and_nudge.py`: tool availability in subagents, nudge follow-through, prompt-hook cost.
- `reachability.py`: whether routing instructions reach subagents; re-reads after a CodeGraph call.

## Baseline

| Measure | Value |
|---|---|
| Subagent tool calls that were shell | 26,538 of 33,387 |
| Shell search and read calls, main plus subagents | 20,251 |
| Of those, naming a code file | 7,338 |
| CodeGraph MCP calls, main plus subagents | 297 |
| Subagent runs with five or more calls that used CodeGraph at least once | 162 of 954 |
| Symbolic Serena calls | 0 |
| Subagent contexts holding the routing `SKILL.md` body | 2 of 982 |
| Subagent contexts holding the CodeGraph server instructions | 981 of 982 |
| Nudges followed by a CodeGraph call within three calls | 111 of 3,212 |
| CodeGraph calls followed by a re-read of a returned file | 94 of 294 |
| `codegraph_explore` result size, median characters | 24,799 |
| Prompt-hook injections, deduplicated; median characters | 552; 9,535 |
| Codex `exec` calls with shell search or read, against CodeGraph (coarse) | about 5,800 against about 350 |

Operation sizes for one symbol in one Laravel repository, CodeGraph 1.6.2: `explore` 24,952 characters,
`explore --max-files 3` 24,478, `query --limit 5` 674, `callers --limit 10` 1,287, `node` 1,825.

## Limits

- The shell classifier reads the first real command of each call. The read bucket includes `ls`, `wc`
  and `jq`.
- The re-read measure matches file basenames in the next eight calls.
- One week, one workstation. Compare a later week with the same scripts before drawing a trend.

## Changes made from this baseline

Routing skill operation card and lane-worktree rule; plain-name routing preload in Claude roles and
the matching instruction in Codex roles; `CODEGRAPH_MCP_TOOLS` in both runtimes; a gate in front of the
vendor prompt hook; scoped `codegraph.json` files. The commits of 2026-11-15 hold the detail.
