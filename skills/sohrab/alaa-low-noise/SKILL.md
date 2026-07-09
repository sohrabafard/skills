---
name: alaa-low-noise
description: Minimizes context and token waste during non-trivial Codex CLI, IDE, and app work by suppressing unnecessary terminal output, repeated file dumps, broad diffs, long logs, and status chatter while preserving task quality, evidence, and reviewability. Use for broad searches, noisy validation, large diffs, long sessions, or delegated lanes. Do not use for tiny tasks, raw-output deliverables, or as a substitute for domain skills or alaa-workflow.
---

# Alaa Low Noise

Reduce visible output, not task effort, evidence, validation, or reviewability. This is a companion skill: domain skills own implementation and `$alaa-workflow` owns durable planning and state.

## When NOT to use

Do not use this skill for tiny tasks, raw-output deliverables, or as a replacement for domain skills or `$alaa-workflow`.

## Contract

- Complete the real task and keep repository files as the source of truth. Preserve required facts, decisions, caveats, validation, blockers, and next steps; trim introductions, repetition, proof-of-work narration, raw dumps, and optional background first.
- Obey explicit requests for full logs, diffs, or file contents.
- Search or inventory before reading; use bounded excerpts, read a whole file only when safe work requires it, and do not reread without a new reason.
- Report only milestones, blockers, scope changes, validation outcomes, and useful artifact paths. Do not duplicate status already surfaced by the harness.
- Bound terminal output: avoid unbounded file, tree, manifest, and log dumps; prefer purpose-built tools, changed-file lists, diff stats, and path-scoped diffs.
- For long output, use an existing repo or workflow artifact path only when retention helps; inspect the relevant slice, summarize the result and path, and remove throwaway files when safe. Keep implementation in normal repo files, never in temp, shell-history, or off-repo state.
- Follow repo conventions. When `$alaa-workflow` is active, use its artifact family and do not create a competing plan or state system.
- Batch independent reads or searches when supported. If Windows sandbox, refresh, locking, quoting, or command-length failures occur, invoke `$alaa-codex-runtime-ops` and retry only essential failed work serially with bounded output.
- When subagents are used, the parent owns concise synthesis; children return tight findings or artifact paths, avoid shared-file chatter, and use read-only discovery or disjoint writer lanes.
- Finish with changed paths, reasons, validation, and remaining risks or blockers instead of a large pasted diff.

## References

Read only when needed:

- `references/noise-control-patterns.md` for shell, search, diff, and log-capture patterns.
- `references/workflow-integration.md` when `$alaa-workflow`, repo-local state, or delegated lanes are active.
- `references/90-source-map.md` when behavior depends on current tool, shell, or model guidance.

## Check

Confirm that task quality and evidence were preserved, output stayed bounded, edits remain reviewable, and workflow or domain ownership was not duplicated.
