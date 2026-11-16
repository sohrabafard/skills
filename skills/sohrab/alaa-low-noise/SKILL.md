---
name: alaa-low-noise
description: Context economy and output discipline for non-trivial agent work in Claude Code and Codex. Use for broad discovery, large diffs, long logs, noisy validation, long sessions, or delegated subagent lanes, to bound both what enters the context window and what gets printed while preserving task quality, evidence, validation, and reviewability. Do not use for tiny tasks, raw-output deliverables, or as a substitute for domain skills or for /alaa-workflow, which owns durable planning and state.
---

# Alaa Low Noise

Bound what enters the context and what gets printed. Never bound the work: task effort, evidence, validation and reviewability stay whole. Both runtimes share this contract unless a rule names its runtime.

## First rules

These four rules save the most context. Each tool result costs context again on every later turn.

1. **Bound each command's output at its source.** Use a quiet flag, a filter, a count or `tail`. Never dump an unbounded file, tree, manifest, diff or log.
2. **Search or inventory before you read, then read the bounded slice around the match.** Read a whole file only when safe editing requires it. Stop at the first step that answers the question.
3. **Save bulky output to a file and report its path.** Bulky output is logs, diffs, inventories and generated data. Save it to an authorized file, and inspect only its failing or relevant slice. Reason: terminal output is gone when the session ends.
4. **Never paste output to prove that a command ran.** Report the command, the result, the one line that mattered and the path to the rest.

**Default command-output budget: about 40 lines per command that enters the context.** Larger output goes to a file, and you read only its failing or relevant slice. Required evidence that exceeds it stays.

A dispatched lane carries its own output rule in its agent definition. The lead names this skill in a dispatch only for a discovery-heavy or log-heavy lane.

## Contract

- Trim introductions, repetition, proof-of-work narration, raw dumps and optional background first. Never trim required facts, decisions, caveats, validation, blockers or next steps.
- Obey an explicit request for full logs, diffs or file contents. A stricter repository validation policy also wins.
- When `/alaa-workflow` is active, use its artifact family, not a competing one.
- Keep long-running work observable through bounded calls and the updates that the host requires. Do not infer a universal watchdog timeout.

### Part 1 — Context economy: what enters the window

- Re-read only for a new reason: your own edit, a failed check or a changed hypothesis.
- Use a scoped search with a few context lines, a changed-file list, a count, a diff stat or a path-scoped diff. Prefer one well-chosen query to several exploratory ones.

### Part 2 — Output noise: what gets printed

- Put reviews, assessments, explanations and advice in the reply. Create a file for a read-only or advisory request only on explicit request or under an admitted plan. For plan admission and its exceptions, read `alaa-workflow references/artifact-lifecycle.md`. Report an admitted plan by its canonical reference and a file artifact by its path.
- When you shorten output, keep required checklists, resume context and the phase and task skill bindings.
- Where a person follows the run, write a one-line opening and a one-line update every few tool calls. An unattended lane needs neither. Beyond those lines, report only milestones, blockers, scope changes, validation outcomes and useful artifact paths. Never duplicate status that the harness already shows.
- **Default progress budget: 12 lines of prose and excerpts up to 20 lines.** It applies to progress reports, not to requested deliverables or required findings. Required content that exceeds it stays.
- Do not narrate a plan before you run it, unless the user must decide something first. The opening line of an attended run is not such a plan.
- Do not restate a file that you just wrote or edited. Name its path and what changed.
- Finish with changed paths, reasons, validation results, and remaining risks or blockers, written for a reader who saw no tool call. Never paste a large diff instead.
- Keep an artifact only when it helps the user inspect or resume. Remove throwaway files before you finish, when that is safe. Keep implementation in normal repository files, never in temp, shell-history or off-repo state. Leave nothing durable only in the conversation.
- On a sandbox, refresh, locking, quoting or command-length failure, retry only the essential failed work, serially and with bounded output. Under Codex, first invoke `/alaa-codex-runtime-ops`; that recovery skill is Codex-only.

## When NOT to use

- The whole task fits in one read and one edit. This discipline then costs more context than it saves.
- The deliverable is raw output: a full log, a complete file or a requested verbatim dump.
- The question belongs to a domain skill.
- The need is durable planning and state through compaction and handoff. `/alaa-workflow` owns that work.

## References

- `references/noise-control-patterns.md`: you are about to choose a search, read, diff or log-capture command.
- `references/workflow-integration.md`: `/alaa-workflow`, repo-local state or delegated lanes are active.
- `references/model-output-profiles.md`: output length or narration needs tuning. A model-specific claim goes to `/alaa-prompting-guide`.
- `references/90-source-map.md`: behavior depends on current tool, shell, runtime or model guidance.
