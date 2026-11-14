---
name: alaa-low-noise
description: Context economy and output discipline for non-trivial agent work in Claude Code and Codex. Use for broad discovery, large diffs, long logs, noisy validation, long sessions, or delegated subagent lanes, to bound both what enters the context window and what gets printed while preserving task quality, evidence, validation, and reviewability. Do not use for tiny tasks, raw-output deliverables, or as a substitute for domain skills or for /alaa-workflow, which owns durable planning and state.
---

# Alaa Low Noise

Bound context input and printed output while preserving task effort, evidence, validation and
reviewability. Both runtimes share this contract unless a rule names its runtime. Domain skills own
implementation. `/alaa-workflow` owns durable planning and state.

## Contract

Apply these rules to both parts:

- Complete the real task. Keep repository files as the source of truth.
- Preserve required facts, decisions, caveats, validation, blockers, and next steps.
- Trim introductions, repetition, proof-of-work narration, raw dumps, and optional background first.
- Obey explicit requests for full logs, diffs, or file contents.
- Follow repository conventions. When `/alaa-workflow` is active, use its artifact family, not a competing family.
- Keep long-running work observable through bounded calls and concise updates required by the active host.
- Batch independent reads, searches and checks when safe and supported. Keep dependent operations and mutations sequential.
- Do not infer a universal watchdog timeout. Do not narrate every command.

Repository validation policy owns stricter invocation requirements.

### Part 1 — Context economy: what enters the window

- Treat each tool result as a recurring cost when choosing retrieval.
- Search or inventory before reading. Then read the bounded slice around the match. Read a whole file only when safe editing requires it.
- Re-read only for a new reason. Examples include your own edit, a failed check, or a changed hypothesis. Reconfirming content already in context does not qualify.
- Prefer a scoped search with a few context lines, a changed-file list, or a count over raw dumps. Examples of raw dumps include `cat`, a full tree, or an unbounded log.
- Prefer one well-chosen query to several exploratory queries.
- Capture bulky output in a file. Inspect only its failing or relevant slice. Keep the path.

### Part 2 — Output noise: what gets printed

Save bulky working material such as logs, diffs, inventories and generated data to an authorized
file. Report its path instead of printing it. Terminal output costs tokens and context on later
turns and disappears when the session ends.

**Deliver the answer and preserve admitted plans.** Put reviews, assessments, explanations and advice in the reply.
For execution-plan admission and exceptions, read `alaa-workflow references/artifact-lifecycle.md`.
Persist the admitted plan and position in the medium the workflow selects. Report its canonical
reference with a concise outcome. Report file paths for file artifacts. Outside admission,
create a file for a read-only or advisory request only on explicit request. `/alaa-repo-docs` owns
documents. When shortening output, keep required checklists, resume context and phase and task skill bindings.

- Where a person follows the run, write a one-line opening and a one-line update every few tool calls. An unattended lane needs neither. Beyond those lines, report only milestones, blockers, scope changes, validation outcomes, and useful artifact paths. Never duplicate status already surfaced by the harness.
- Bound terminal output. Do not dump unbounded files, trees, manifests, or logs. Prefer purpose-built tools, changed-file lists, diff stats, and path-scoped diffs.
- **Default progress budget: 12 lines of prose and excerpts up to 20 lines.** Apply this budget to progress reports, not requested deliverables or required findings. Preserve required content that exceeds the default. Put bulky working material in an authorized artifact.
- Retain an artifact only when it helps the user inspect or resume. Summarize its outcome and name its path. Remove throwaway files before finishing when safe. Keep implementation in normal repository files, never in temp, shell-history, or off-repo state.
- Finish with changed paths, reasons, validation results, and remaining risks or blockers. Write the final report so that a reader who saw no tool call understands it. Do not paste a large diff instead.
- On sandbox, refresh, locking, quoting, or command-length failures, retry only the essential failed work. Retry serially with bounded output. Under Codex, first invoke `/alaa-codex-runtime-ops`. That recovery skill is Codex-only. It has no Claude Code equivalent.

#### The three leaks

These actions feel like diligence but add noise. Use their replacements:

1. **Narrating a plan before execution:** State a plan only when the user must decide something before it runs. Otherwise, run it and report the outcome; the next action shows the plan. The one-line opening of an attended run is not a narrated plan.
2. **Pasting output to prove a command ran:** Report the command, the result, the one line that mattered, and the path to the rest. The outcome is evidence; the transcript is not.
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

- `references/noise-control-patterns.md` when you are about to choose a search, read, diff, or log-capture command in either runtime.
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
