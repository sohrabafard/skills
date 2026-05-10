---
name: alaa-low-noise
description: Use this companion skill when Codex work in the CLI, IDE extension, or Codex app risks wasting context or terminal budget through broad search, repeated file dumps, long logs, large diffs, manual status chatter, or long-running sessions. It keeps the run quiet and reviewable by favoring targeted search, bounded reads, repo-local artifacts for bulky transient state, and concise reporting while preserving normal repository edits and Git-based review visibility. Do not use it for tiny tasks, when the user explicitly wants raw full output, or as a substitute for domain skills or `alaa-workflow` planning.
---

# Alaa Low Noise

This skill enforces output discipline, not effort reduction.

It is a companion skill. It does not own architecture, stack decisions, or durable workflow planning.

## Core contract

- Complete the real task. Suppress output, not diligence.
- Keep the repository as the source of truth. Final implementation must land in normal repo files.
- Prefer targeted evidence over raw dumps.
- Externalize bulky transient state only when it improves continuity or inspection.
- Obey explicit user requests for full raw output even when it is noisy.

## Use this skill when

- Search or read scope is broad.
- Logs, validation output, or generated inventories may be large.
- The final diff may be large enough that pasting it would waste context.
- The session is long enough that repeated narration would become noise.
- PowerShell or shell quoting and output habits are likely to create avoidable spam.
- Subagents or parallel lanes would otherwise flood the parent thread with discovery output.

## When NOT to use

- The task is tiny and ordinary output is already naturally compact.
- Raw logs, a full diff, or full file contents are the actual deliverable.
- A narrow domain skill can handle the task directly without notable output risk.

## Operating rules

### 1) Search first, read surgically

- Search before full-file reads.
- Prefer bounded excerpts around matches.
- Read the full file privately only when needed for a safe edit.
- Do not re-open the same file without a new reason.

### 2) Keep commentary sparse

- Do not narrate every command, search, or tiny edit.
- Do not emit ritualized proof-of-work text.
- Surface only milestone-level updates, blockers, scope changes, validation outcomes, and artifact paths.
- If the surface already provides commentary or reasoning summaries, do not duplicate them with extra manual chatter unless the user asked.

### 3) Prefer repo-local artifacts for bulky transient state

- Use existing repo conventions first.
- If `$alaa-workflow` is active, inherit its artifact family and naming rules instead of inventing new ones.
- Otherwise prefer existing repo-local scratch paths such as `artifacts/` or `reports/`.
- Never hide the real implementation in OS temp files, shell history, or off-repo notes.
- Remove throwaway artifacts before finishing if they have no lasting value and repo policy allows cleanup.

### 4) Preserve reviewability

- Prefer changed-file lists, concise diff stats, or file-local diffs over repo-wide dumps.
- Do not paste giant unified diffs into chat unless the user asked for them.
- Keep the final answer focused on what changed, why it changed, what was validated, and where any saved artifacts live.

### 5) Bound shell output

- Avoid unbounded `cat`, `type`, `Get-Content`, folder trees, or generated manifest dumps.
- Redirect long validation output to repo-local files and summarize only the meaningful lines.
- Prefer dedicated tools over raw shell whenever the harness provides them.
- Batch independent searches or reads in parallel when the environment supports it.
- If a parallel read or search fails because of Windows sandbox setup or refresh errors, switch to `$alaa-codex-runtime-ops`, rerun only the failed or essential read serially, and keep the retry output bounded.

### 6) Stay companion-oriented

- Combine this skill with domain skills for implementation rules.
- Combine this skill with `$alaa-workflow` for long-horizon plans, resume state, handoffs, or delegated execution.
- Combine this skill with `$alaa-codex-runtime-ops` when the noise risk comes from Windows sandbox, shell, locked-file, or command-length recovery.
- Do not invent a second planning system when workflow artifacts already exist.

## Subagent Strategy

If subagents are used:

- The parent owns concise synthesis and the final report.
- Discovery-heavy lanes should return findings through owned artifacts or tight summaries, not raw logs.
- Child lanes should avoid spamming shared coordination files or repeated terminal narration.
- Prefer read-only explorer lanes for broad search and reserve writer lanes for disjoint edits.

## Reference navigation

- Read `references/noise-control-patterns.md` for concrete Bash and PowerShell patterns for search, excerpting, diffing, and log capture.
- Read `references/workflow-integration.md` only when pairing with `$alaa-workflow`, repo-local state artifacts, or delegated lanes.
- Read `references/90-source-map.md` when output behavior depends on current tool, shell, or model-use guidance.

## Quick self-check

- I reduced output, not diligence.
- I searched before reading deeply.
- Bulky transient output lives in repo-local artifacts only when it helps.
- Final edits remain visible in normal repo diffs.
- I did not duplicate workflow ownership or domain-skill ownership.
