---
name: alaa-low-noise
description: Context economy and output discipline for non-trivial agent work in Claude Code and Codex. Use for broad discovery, large diffs, long logs, noisy validation, long sessions, or delegated subagent lanes, to bound both what enters the context window and what gets printed while preserving task quality, evidence, validation, and reviewability. Do not use for tiny tasks, raw-output deliverables, or as a substitute for domain skills or for /alaa-workflow ($alaa-workflow), which owns durable planning and state.
---

# Alaa Low Noise

Two levers, routinely conflated. **Context economy** governs what enters the context window at all; **output noise** governs what gets printed for the user. Context economy is the more valuable of the two, because a long tool result is charged against every later turn of the session, not only the turn it arrives in. Neither lever reduces task effort, evidence, validation, or reviewability.

A companion skill: domain skills own implementation, `$alaa-workflow` / `/alaa-workflow` owns durable planning and state, and this skill owns only these two levers — it gives no planning advice. Invocation is `/alaa-low-noise` in Claude Code and `$alaa-low-noise` in Codex; the contract is identical, and rules that depend on the runtime name it. The frontmatter owns trigger boundaries, including when not to use this skill.

## Contract

Shared by both parts: complete the real task and keep repository files as the source of truth; preserve required facts, decisions, caveats, validation, blockers, and next steps while trimming introductions, repetition, proof-of-work narration, raw dumps, and optional background first; obey an explicit request for full logs, diffs, or file contents; and follow repository conventions, using the `$alaa-workflow` / `/alaa-workflow` artifact family when that skill is active rather than a competing one.

**Silence is a failure mode, not economy.** Run one bounded command per invocation, and print a line naming the step between invocations. A watchdog ends a run that produces no output, so a long chain of commands joined into one silent invocation is killed on its silence rather than on its duration, and whatever it had not yet written is lost with it. Boundedness is an execution rule before it is an output rule. The line names the step and nothing else — this is not licence to narrate, and the budgets in Part 2 are unchanged. Where a repository's own validation-policy file states how its checks are invoked, that file outranks this rule there.

### Part 1 — Context economy: what enters the window

- Treat every tool result as a recurring cost rather than a one-turn cost, and decide on that basis.
- Search or inventory before reading, then read the bounded slice around the match; read a whole file only when safe editing requires the whole file.
- Do not re-read without a new reason. Your own edit, a failed check, or a changed hypothesis qualifies; re-confirming what is already in context does not.
- Prefer a targeted tool result to a raw dump: a scoped search with a few lines of context, a changed-file list, or a count beats `cat`, a full tree, or an unbounded log.
- Batch independent reads and searches into one turn where the runtime supports it, and prefer one well-chosen query to several exploratory ones.
- Route bulky output to a path instead of into the window: capture it, inspect only the failing or relevant slice, and keep the path.
- Keep subagent returns tight so the parent's context stays clean. Children return findings, counts, verdicts, or artifact paths — never transcripts, full diffs, or raw logs — and the parent owns synthesis.

### Part 2 — Output noise: what gets printed

**The file is the medium; the message is the pointer.** Working material — logs, diffs, inventories, command output, intermediate results, generated data, and any state a later turn or another agent will need again — is written to a file and named by its path instead of printed. The terminal is not storage: what is printed there is charged once as output tokens, charged again against context on every later turn, and gone when the session ends. This is the rule the rest of this part implements, and it is the one most often skipped while the others are obeyed.

**The answer is not working material.** A review, a plan, an assessment, an explanation, or any deliverable the user asked to receive is delivered in the reply. Writing it to a file instead creates an artifact nobody requested and hides the answer behind a path, which is a worse outcome than the verbosity this skill exists to prevent. A read-only or advisory request produces no file at all unless the user asked for one; `/alaa-workflow` (`$alaa-workflow`) owns when a repository artifact is authorized and `/alaa-repo-docs` (`$alaa-repo-docs`) owns documents, and nothing here triggers either.

- Report only milestones, blockers, scope changes, validation outcomes, and useful artifact paths, and never duplicate status the harness already surfaces.
- Bound terminal output: no unbounded file, tree, manifest, or log dumps. Prefer purpose-built tools, changed-file lists, diff stats, and path-scoped diffs.
- **Budget: 12 lines of prose per message, and no single excerpt over 20 lines.** A message past either bound has stopped being a report. Cut it to the outcome and the path, and put what was cut into the file. Apply this to the draft before sending it; a long message is not repaired by a note apologising for its length.
- Retain an artifact only when it helps the user inspect or resume; summarize the outcome, name the path, and remove throwaway files when that is safe. Implementation stays in normal repository files, never in temp, shell-history, or off-repo state.
- Finish with changed paths, reasons, validation results, and remaining risks or blockers instead of a large pasted diff.
- On sandbox, refresh, locking, quoting, or command-length failures, retry only the essential failed work serially and with bounded output. Under Codex, invoke `$alaa-codex-runtime-ops` first; it is Codex-only, with no Claude Code equivalent.

#### The three leaks

These survive every general instruction to be concise, because each one feels like diligence rather than noise. Each has one replacement, and the replacement is what to do instead — not merely what to stop doing.

1. **Narrating the plan before executing it.** What is about to happen is visible in what happens next. State a plan only when the user has to decide something before it runs; otherwise run it and report the outcome.
2. **Pasting command output to show the command ran.** The outcome is the evidence; the transcript is not. Report the result, the one line that mattered, and the path to the rest.
3. **Restating a file just written or edited.** The file is the deliverable and it can be opened. Name the path and what changed in it.

A fourth belongs to delegation: **a child returning its work instead of its findings.** That one is prevented in the dispatch rather than in the child — every dispatch carries a return shape and a line bound. `references/workflow-integration.md` owns the return contract.

## Model calibration

Verbosity defaults, narration cadence, and instruction literalness differ per model, so a concision rule tuned for one family can be inert on another. One fact is universal: reasoning effort controls thinking volume, not answer length — lowering effort does not shorten output, and length needs its own instruction. Read `references/model-output-profiles.md` for per-model profiles and documented calibration language.

## When NOT to use

- The task is small enough that the whole of it fits in one read and one edit. The discipline then costs
  more context than it saves.
- The deliverable is the raw output itself — a full log, a complete file, a verbatim dump the user asked
  for. Trimming it destroys the deliverable.
- The question is a domain question. Nothing here substitutes for the skill that owns the subject.
- The need is durable planning and state that survives compaction and handoff.
  `/alaa-workflow` (`$alaa-workflow`) owns that, and nothing here replaces it.

## References

Read only when needed:

- `references/model-output-profiles.md` when tuning verbosity for a model, or when length or narration does not match the instruction given.
- `references/noise-control-patterns.md` for search, read, diff, and log-capture patterns in both runtimes.
- `references/workflow-integration.md` when `$alaa-workflow` / `/alaa-workflow`, repo-local state, or delegated lanes are active.
- `references/90-source-map.md` when behavior depends on current tool, shell, runtime, or model guidance.

## Check

Confirm that task quality and evidence survived, that what entered context was bounded and justified, that what was printed stayed inside the budget, that nothing durable was left only in the conversation, that edits remain reviewable, and that workflow or domain ownership was not duplicated.
