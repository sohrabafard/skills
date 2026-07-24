---
name: alaa-low-noise
description: Context economy and output discipline for non-trivial agent work in Claude Code and Codex. Use for broad discovery, large diffs, long logs, noisy validation, long sessions, or delegated subagent lanes, to bound both what enters the context window and what gets printed while preserving task quality, evidence, validation, and reviewability. Do not use for tiny tasks, raw-output deliverables, or as a substitute for domain skills or for /alaa-workflow ($alaa-workflow), which owns durable planning and state.
---

# Alaa Low Noise

Two levers, routinely conflated. **Context economy** governs what enters the context window at all; **output noise** governs what gets printed for the user. Context economy is the more valuable of the two, because a long tool result is charged against every later turn of the session, not only the turn it arrives in. Neither lever reduces task effort, evidence, validation, or reviewability.

A companion skill: domain skills own implementation, `$alaa-workflow` / `/alaa-workflow` owns durable planning and state, and this skill owns only these two levers — it gives no planning advice. Invocation is `/alaa-low-noise` in Claude Code and `$alaa-low-noise` in Codex; the contract is identical, and rules that depend on the runtime name it. The frontmatter owns trigger boundaries, including when not to use this skill.

## Contract

Shared by both parts: complete the real task and keep repository files as the source of truth; preserve required facts, decisions, caveats, validation, blockers, and next steps while trimming introductions, repetition, proof-of-work narration, raw dumps, and optional background first; obey an explicit request for full logs, diffs, or file contents; and follow repository conventions, using the `$alaa-workflow` / `/alaa-workflow` artifact family when that skill is active rather than a competing one.

### Part 1 — Context economy: what enters the window

- Treat every tool result as a recurring cost rather than a one-turn cost, and decide on that basis.
- Search or inventory before reading, then read the bounded slice around the match; read a whole file only when safe editing requires the whole file.
- Do not re-read without a new reason. Your own edit, a failed check, or a changed hypothesis qualifies; re-confirming what is already in context does not.
- Prefer a targeted tool result to a raw dump: a scoped search with a few lines of context, a changed-file list, or a count beats `cat`, a full tree, or an unbounded log.
- Batch independent reads and searches into one turn where the runtime supports it, and prefer one well-chosen query to several exploratory ones.
- Route bulky output to a path instead of into the window: capture it, inspect only the failing or relevant slice, and keep the path.
- Keep subagent returns tight so the parent's context stays clean. Children return findings, counts, verdicts, or artifact paths — never transcripts, full diffs, or raw logs — and the parent owns synthesis.

### Part 2 — Output noise: what gets printed

- Report only milestones, blockers, scope changes, validation outcomes, and useful artifact paths, and never duplicate status the harness already surfaces.
- Bound terminal output: no unbounded file, tree, manifest, or log dumps. Prefer purpose-built tools, changed-file lists, diff stats, and path-scoped diffs.
- Retain an artifact only when it helps the user inspect or resume; summarize the outcome, name the path, and remove throwaway files when that is safe. Implementation stays in normal repository files, never in temp, shell-history, or off-repo state.
- Finish with changed paths, reasons, validation results, and remaining risks or blockers instead of a large pasted diff.
- On sandbox, refresh, locking, quoting, or command-length failures, retry only the essential failed work serially and with bounded output. Under Codex, invoke `$alaa-codex-runtime-ops` first; it is Codex-only, with no Claude Code equivalent.

## Model calibration

Verbosity defaults, narration cadence, and instruction literalness differ per model, so a concision rule tuned for one family can be inert on another. One fact is universal: reasoning effort controls thinking volume, not answer length — lowering effort does not shorten output, and length needs its own instruction. Read `references/model-output-profiles.md` for per-model profiles and documented calibration language.

## References

Read only when needed:

- `references/model-output-profiles.md` when tuning verbosity for a model, or when length or narration does not match the instruction given.
- `references/noise-control-patterns.md` for search, read, diff, and log-capture patterns in both runtimes.
- `references/workflow-integration.md` when `$alaa-workflow` / `/alaa-workflow`, repo-local state, or delegated lanes are active.
- `references/90-source-map.md` when behavior depends on current tool, shell, runtime, or model guidance.

## Check

Confirm that task quality and evidence survived, that what entered context was bounded and justified, that what was printed stayed proportionate, that edits remain reviewable, and that workflow or domain ownership was not duplicated.
