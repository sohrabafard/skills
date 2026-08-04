---
name: alaa-extract-agent-lessons
description: "Reusable-context curation for substantial agent work and conversations. Use at signal-bearing phase boundaries and before final handoff to extract evidence-backed decision interfaces, judgment rubrics, and durable knowledge cards from explicit user or team decisions, accepted or rejected work with reasons, non-obvious product or team knowledge, verified surprises, costly detours, validation failures, or coordination bottlenecks. Keep active candidates in alaa-workflow and publish only authorized durable knowledge through alaa-memory-os. Do not use for raw logs, status, active plans, speculative advice, obvious repository facts, or one-off workarounds."
---

# Alaa Extract Agent Lessons

Curate the smallest reusable context that changes future work. Preserve what to choose as a decision
interface, how to judge as a rubric, or what non-obvious context to know as a knowledge card. Discard the
chronology that merely happened once.

Valuable does not mean merely interesting or new. Without the candidate, a future agent must be likely to
make a worse decision, misjudge acceptable work, miss consequential context, or repeat expensive discovery.

## Lifecycle

1. **Intermediate scan:** at a phase or decision boundary, scan only the evidence accumulated since the
   previous boundary when a signal below occurred. When `$alaa-workflow` / `/alaa-workflow` is active, keep
   admitted candidates in the matching handoff-package fields. Record a judgment there as the confirmed fact
   that a named user or team chose something for a stated reason; never rewrite it as a universal fact.
2. **Final gate:** after implementation, validation, review, and documentation evidence are stable, scan the
   whole engagement, merge duplicates, resolve provisional candidates, and decide each destination before the
   handoff closes.
3. **Empty result:** when nothing passes admission, report that outcome and stop. Never manufacture a lesson
   to make the gate look productive.

Signals are an explicit correction, choice, approval or rejection with a reason, an accepted tradeoff, an
accepted or rejected example whose rationale exposes a judgment boundary, a verified surprise, a costly
detour, a validation failure that changed the method, a coordination bottleneck, a high-fidelity reference
that resolves repeated ambiguity, or non-obvious product, team, or domain knowledge future work will need.

## When NOT to use

Do not use for ordinary status, raw transcripts or logs, secrets, active plan or phase state, unsupported
impressions, obvious repository facts already maintained by code or docs, or advice that cannot change a
future decision or evaluation. A one-off incident stays in the task evidence.

## Admission gate

Keep a candidate only when every answer is yes:

1. **Provenance:** Is there an exact source — an explicit user or team judgment, a verified artifact or source,
   an observed result, or a clearly labelled inference from repeated evidence?
2. **Counterfactual value:** Without it, is a future agent likely to choose or judge materially worse, miss a
   consequential constraint, or repeat meaningful discovery cost? Reject information that is novel but inert.
3. **Reuse:** Is the same choice, evaluation, or knowledge likely to recur for this project, product, team, or
   fleet rather than only for the incident that produced it?
4. **Novelty and recoverability:** Is it absent from authoritative code, docs, skills, and searched memory, or
   does it materially correct or refine them? When the owner answers it cheaply, retain a pointer or promotion
   rather than a competing explanation.
5. **Scope and authority:** Can the candidate state who or what it is authoritative for without turning a
   preference into a fact, an inference into a rule, or a project lesson into fleet doctrine?
6. **Safety and stability:** Can it be retained without prohibited content or volatile task state, with a
   source pointer and an invalidation or freshness condition where needed?

Reject or merge candidates that fail any gate.

An explicit user correction or choice is evidence of that user's or team's judgment in its stated scope. It
is not evidence that the choice is universally correct. A pattern inferred from accepted and rejected work
stays advisory and says it is inferred.

## Choose the reusable form

- **Decision interface:** a repeatable condition must select an action, check, fallback, escalation, or stop.
- **Judgment rubric:** a future agent must evaluate quality, taste, tradeoffs, or competing acceptable options.
- **Knowledge card:** a non-obvious fact or operating context changes reasoning but does not itself prescribe a
  procedure or quality judgment.

Read `references/reusable-context-shapes.md` after a candidate passes admission. It owns the common provenance
envelope, the three compact shapes, compression rules, and the classification test. These are candidate shapes,
not memory-note schemas.

## Route the result

1. Keep engagement-local candidates in the `$alaa-workflow` / `/alaa-workflow` handoff package. Do not copy
   active phase state or validation logs into memory.
2. When repository code, docs, an instruction file, or an existing skill already owns the knowledge, update or
   promote through that owner only when the task authorizes it; otherwise report a promotion candidate and the
   owning surface.
   When the final gate discovers a repository promotion after evidence was declared stable, return
   `pipeline reopen required`; do not mutate the evidence underneath completion.
3. Before drafting a promotion into a prompt, skill, agent definition, `AGENTS.md`, or `CLAUDE.md`, load
   `$alaa-prompting-guide` / `/alaa-prompting-guide`. It owns model, runtime, trigger, and artifact-authoring
   behavior.
4. Before durable publication, load `$alaa-memory-os` / `/alaa-memory-os`, search before creating, and follow
   its note shape, curation labels, adapters, drift rules, and prohibited-content list. This skill selects and
   shapes candidates; it does not own storage mechanics or memory authority.
5. If publication is unauthorized or memory is unavailable, return the curated candidates in the handoff and
   state that they were not persisted. Memory unavailability does not erase a valid candidate.

## Output and stop conditions

Report the boundaries scanned; retained candidates grouped by form; provenance, authority, and destination for
each; candidates merged or rejected with a short reason; notes created, updated, or deliberately not written;
and promotion or drift that still needs an owner.

Stop successfully when every admitted candidate has one form, one scoped authority, one source pointer, one
destination, no prohibited content, and no unresolved `pipeline reopen required` result, including when the
retained set is empty. Return `pipeline reopen required` when an authorized canonical repository change remains
after evidence freeze. Stop blocked only when a required source cannot be inspected, an authorized drift record
cannot be written, or a mandatory owner rejects the handoff. Perform at most one search-before-create pass; do
not loop through repeated extraction or memory searches for reassurance.
