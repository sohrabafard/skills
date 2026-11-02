---
name: alaa-low-noise
description: Context economy and output discipline for non-trivial agent work in Claude Code and Codex. Use for broad discovery, large diffs, long logs, noisy validation, long sessions, or delegated subagent lanes, to bound both what enters the context window and what gets printed while preserving task quality, evidence, validation, and reviewability. Do not use for tiny tasks, raw-output deliverables, or as a substitute for domain skills or for /alaa-workflow, which owns durable planning and state.
---

# Alaa Low Noise

## Introduction

This skill keeps complex work inspectable while limiting context cost and output noise. **Context economy** controls what enters the context window. **Output discipline** controls what is printed for the user. Context economy matters more because long tool results cost context on every later turn. Neither control reduces task effort, evidence, validation, or reviewability.

## Scope and ownership

This companion skill owns context economy and output discipline only. Domain skills own implementation. `/alaa-workflow` owns durable planning and state; this skill gives no planning advice. Both runtimes share this contract. Runtime-dependent rules name their surface. The frontmatter owns activation boundaries, including exclusions.

## Contract

Apply these rules to both parts:

- Complete the real task. Keep repository files as the source of truth.
- Preserve required facts, decisions, caveats, validation, blockers, and next steps.
- Trim introductions, repetition, proof-of-work narration, raw dumps, and optional background first.
- Obey explicit requests for full logs, diffs, or file contents.
- Follow repository conventions. When `/alaa-workflow` is active, use its artifact family, not a competing family.
- Keep long-running work observable through bounded calls and concise updates required by the active host.
- Batch independent reads or checks when safe. Keep dependent operations and mutations sequential.
- Do not infer a universal watchdog timeout. Do not narrate every command.

Repository validation policy owns stricter invocation requirements.

### Part 1 — Context economy: what enters the window

- Treat each tool result as a recurring cost when choosing retrieval.
- Search or inventory before reading. Then read the bounded slice around the match. Read a whole file only when safe editing requires it.
- Re-read only for a new reason. Examples include your own edit, a failed check, or a changed hypothesis. Reconfirming content already in context does not qualify.
- Prefer a scoped search with a few context lines, a changed-file list, or a count over raw dumps. Examples of raw dumps include `cat`, a full tree, or an unbounded log.
- Batch independent reads and searches into one turn where the runtime supports it. Prefer one well-chosen query to several exploratory queries.
- Capture bulky output in a file. Inspect only its failing or relevant slice. Keep the path.

### Part 2 — Output noise: what gets printed

**The file is the medium; the message is the pointer.** Save working material to a file and report its path instead of printing it. This includes logs, diffs, inventories, command output, intermediate results, generated data, and state needed by later turns or other agents. Terminal output costs output tokens and context on later turns. It is not storage and is gone when the session ends.

**Deliver the answer; preserve admitted plans.** Put reviews, assessments, explanations, and other requested advice in the reply. Before choosing an execution plan's medium, read `alaa-workflow references/artifact-lifecycle.md` for admission and its exceptions. When admitted, save the plan/checkpoint. Report their paths with a concise outcome. Outside that admission, create no files for read-only or advisory requests unless explicitly requested. `/alaa-repo-docs` owns documents. Preserve required checklists, resume context, and phase/task skill bindings when shortening output.

- Report only milestones, blockers, scope changes, validation outcomes, and useful artifact paths. Never duplicate status already surfaced by the harness.
- Bound terminal output. Do not dump unbounded files, trees, manifests, or logs. Prefer purpose-built tools, changed-file lists, diff stats, and path-scoped diffs.
- **Default progress budget: 12 lines of prose and excerpts up to 20 lines.** Apply this budget to progress reports, not requested deliverables or required findings. Preserve required content that exceeds the default. Put bulky working material in an authorized artifact.
- Retain an artifact only when it helps the user inspect or resume. Summarize its outcome and name its path. Remove throwaway files when safe. Keep implementation in normal repository files, never in temp, shell-history, or off-repo state.
- Finish with changed paths, reasons, validation results, and remaining risks or blockers. Do not paste a large diff instead.
- On sandbox, refresh, locking, quoting, or command-length failures, retry only the essential failed work. Retry serially with bounded output. Under Codex, first invoke `/alaa-codex-runtime-ops`. That recovery skill is Codex-only; it has no Claude Code equivalent.

#### The three leaks

These actions can feel like diligence. Use their replacements to avoid noise:

1. **Narrating a plan before execution:** State a plan only when the user must decide something before it runs. Otherwise, run it and report the outcome; the next action shows the plan.
2. **Pasting output to prove a command ran:** Report the result, the one line that mattered, and the path to the rest. The outcome is evidence; the transcript is not.
3. **Restating a file just written or edited:** Name its path and what changed. The file is the deliverable and can be opened.

## Model calibration

When output length or narration needs tuning, read `references/model-output-profiles.md`. It separates response, artifact, and progress controls. It routes model-specific claims to `/alaa-prompting-guide`. This skill defines no model profiles or effort policy.

## When NOT to use

- The whole task fits in one read and one edit. This discipline then costs more context than it saves.
- The deliverable is raw output: a full log, a complete file, or a requested verbatim dump. Trimming destroys that deliverable.
- The question belongs to a domain skill. This skill does not replace that owner.
- The need is durable planning and state through compaction and handoff. `/alaa-workflow` owns that work.

## References

Read only when needed:

- `references/model-output-profiles.md` when calibrating output length or narration, including routing a model-specific claim.
- `references/noise-control-patterns.md` for search, read, diff, and log-capture patterns in both runtimes.
- `references/workflow-integration.md` when `/alaa-workflow`, repo-local state, or delegated lanes are active.
- `references/90-source-map.md` when behavior depends on current tool, shell, runtime, or model guidance.

## Check

Confirm each result:

- Task quality and evidence survived.
- Context input was bounded and justified.
- Printed output followed the budget and its exceptions.
- Nothing durable remains only in the conversation.
- Edits remain reviewable.
- Workflow and domain ownership were not duplicated.
