---
name: alaa-low-noise
description: "Use when Codex work risks context bloat or terminal spam: repo-wide search, many files, large logs or diffs, long-running CLI/App sessions, or tasks that should externalize bulky transient state to repo-local files while preserving normal Git diffs and Codex app review visibility."
---




# Purpose
Keep Codex CLI and Codex app execution complete, correct, and reviewable while minimizing terminal noise and context waste.

This skill is about low output, not low effort:
- still gather enough context
- still implement the real fix
- still validate when validation is required
- still preserve user visibility into the final code diff

Use it to reduce chatter, repeated dumps, and context-window blowups without weakening the agent.

# Design targets
This skill is intentionally aligned with modern Codex guidance:
- keep the skill focused on one job
- prefer imperative instructions over bulky embedded references
- use progressive disclosure: keep the live context lean and move bulky transient state to files only when useful
- prefer dedicated tools over raw shell when the harness provides them
- batch coherent edits instead of repeated micro-edits
- preserve normal Git-based review flows in Codex app and related tools

# When to use
Use this skill when one or more of these are true:
- the task spans many files or a large repository area
- you need repo-wide search, inventory, or pattern audits
- logs, diffs, or command output may be large
- the task is long-running and needs intermediate notes, inventories, or captured output
- you are working in PowerShell or another shell where noisy output and quoting mistakes are easy to trigger
- context pressure is already visible through repeated file dumps, repeated diffs, or repeated status chatter

## When NOT to use
Do not use this skill when:
- the task is tiny and ordinary output will already be compact
- the user explicitly asks for full raw logs, full diffs, or full file contents
- the main task is vendor-source forensics where raw large excerpts are the deliverable

# Instruction precedence
If instructions conflict, follow this order:
1. explicit user instructions for the current task
2. repo-local `AGENTS.md`
3. this skill
4. general best practices

If a higher-precedence instruction requires more output, do that work and keep the rest of the flow as low-noise as possible.

# Core operating model
## 1) Low-noise means low-output, not low-work
Never use this skill as a reason to:
- skip root-cause analysis
- skip relevant files
- skip validation that a higher-precedence rule requires
- hide blockers, risks, or behavior changes

The goal is to reduce what gets printed, not reduce what gets done.

## 2) Search first, read surgically
Prefer this discovery sequence:
1. locate with search
2. inspect only the relevant excerpts
3. read the full file privately only when needed for a safe edit
4. summarize what matters instead of dumping what you read

Preferred patterns:
- use `rg` or equivalent fast search first
- request bounded excerpts around matches
- avoid opening unrelated files "just in case"
- avoid re-reading the same file repeatedly without new information

## 3) Externalize bulky transient state to repo-local files when useful
If the task produces large intermediate artifacts, do not stream them into the terminal by default.

Examples:
- large inventories
- long test or build logs
- migration or refactor plans
- captured diagnostics
- structured state needed across a long task

Preferred approach:
- write bulky transient state to a repo-local path
- print only the path plus a short summary
- keep the artifact scoped and clearly named
- use existing repo conventions first

Good repo-local locations when the repo already uses them:
- the repo-level docs/_agent_plans/ directory for task plans
- the repo-level docs/agents/ directory for durable continuation state
- the repo-level .codex/state/ directory for machine-oriented transient state
- `reports/` or `artifacts/` for captured logs or inventories

If the repo has no convention, choose a small repo-local scratch location instead of OS temp for any artifact the user may need to inspect.

## 4) Preserve Git diff and Codex app review behavior
Codex app review is based on repository Git state, not just the assistant's narration.

Because of that, never use low-noise tactics that hide the real work from the repo diff.

Required invariants:
- final deliverable changes must land in normal repository files
- do not keep the real implementation only in shell history, clipboard steps, or OS temp files
- do not bypass normal repo edits just to keep the terminal quiet
- if you create analysis or helper artifacts that matter to the user, keep them repo-local so they remain inspectable
- if a transient artifact has no lasting value and repo policy allows cleanup, remove it before finishing

Low-noise should make review cleaner, not make review impossible.

## 5) Prefer summary views over raw dumps
Prefer:
- counts
- short file lists
- narrow excerpts
- targeted diffs
- concise validation summaries

Avoid by default:
- full file dumps
- full folder dumps
- giant unified diffs
- repeated status restatements
- repeated command output pasted again after it was already seen

## 6) Batch coherent work
Read enough context to make a coherent edit, then apply the edit cleanly.

Prefer:
- one bounded search pass
- one focused read pass
- one coherent edit pass
- one targeted validation pass when needed

Avoid thrashing:
- repeated tiny edits to the same area
- repeated re-reading of the same file without new evidence
- printing a preamble before every small tool call

# Tooling rules
## Prefer dedicated tools when available
If the harness offers dedicated read/search/edit/diff tools, use them before falling back to raw shell.

Use shell for:
- commands that genuinely require the shell
- validation flows that are simpler or more reliable in shell
- file moves or environment operations that dedicated tools do not cover

## Keep shell output bounded
Forbidden by default:
- unbounded `cat`
- unbounded `Get-Content`
- unbounded `type`
- printing `node_modules`, build outputs, or coverage trees unless explicitly required

Preferred patterns:
- locate with `rg -n`
- then request a narrow excerpt
- use summary diffs first, detailed diffs only for the specific file that matters

## Parallelize independent inspection
When the harness supports parallel tool calls, use them for independent searches or reads.

Examples:
- searching several patterns at once
- reading several disjoint files at once
- collecting line counts and file locations together

Do not parallelize overlapping writes.

# Reading pattern
Use this order whenever possible:
1. `rg -n "pattern" <paths>`
2. bounded excerpt around the match
3. full-file private read only if required to edit safely
4. concise summary of findings

If you must inspect a large config or generated manifest, capture only the sections relevant to the decision you need to make.

# Editing pattern
- prefer targeted edits over whole-file rewrites
- preserve existing formatting and import order unless correctness requires change
- avoid broad cleanup or reformatting while using this skill
- keep the write set as small as correctness allows
- add brief comments only when they materially improve readability

# Validation pattern
When validation is required or useful:
- start with the smallest meaningful check
- if output is long, redirect or capture it to a repo-local file
- report the command, the outcome, and the path to any saved log
- surface only the key failures or warnings in the terminal summary

Examples:
- store a long build log under `artifacts/` and summarize the failing step
- save a repo-wide audit under `reports/` and report the top findings only

# Reporting pattern
Keep updates and final reporting high-signal.

Prefer reporting:
- what changed
- why it changed
- what was validated
- what remains blocked or risky
- where large supporting artifacts were written

Avoid reporting:
- every command verbatim
- full raw logs unless asked
- long restatements of unchanged context

# Anti-patterns
Do not:
- prove you read a file by dumping it
- paste a repo-wide diff when a file list or targeted diff is enough
- print large generated folders by default
- create huge scratch artifacts outside the repo when the user may need to inspect them
- hide final work in temporary files that never become repo edits
- confuse low-noise with low-transparency
- silently skip validation just because the logs are large

# Quick checklist
- I kept the task complete, not partial.
- I searched before reading.
- I bounded reads and diffs.
- I externalized bulky transient state only when it helped.
- I kept user-relevant artifacts repo-local.
- I preserved normal Git diff and Codex app review visibility.
- I summarized the important evidence instead of dumping it.
