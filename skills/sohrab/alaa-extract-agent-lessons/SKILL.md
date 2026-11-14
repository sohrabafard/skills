---
name: alaa-extract-agent-lessons
description: "Reusable-context curation for substantial agent work and conversations. Use when /alaa-workflow invokes a curation scan or the user requests reusable lessons to extract evidence-backed decision interfaces, judgment rubrics, and durable knowledge cards from explicit user or team decisions, accepted or rejected work with reasons, non-obvious product or team knowledge, verified surprises, costly detours, validation failures, or coordination bottlenecks. Keep active candidates in alaa-workflow and publish only authorized durable knowledge through alaa-memory-os. Do not use for raw logs, status, active plans, speculative advice, obvious repository facts, or one-off workarounds."
---

# Alaa Extract Agent Lessons

Curate the smallest reusable context that changes future decisions, judgments, or reasoning.

## Scan contract

/alaa-workflow `references/context-curation.md` owns scan timing, intermediate/final distinctions, evidence stability, candidate location and reopening consequences. Consume its selected scan scope and recording destination. Create no second phase schedule, handoff schema or task state here.

Intermediate scans assess only evidence since the previous recorded boundary. Final scans reconcile engagement evidence and provisional candidates, merge duplicates, and return each disposition. If no candidate passes admission, return an empty result. Never manufacture a lesson to satisfy a gate.

## When NOT to use

Do not use for ordinary status, raw transcripts/logs, secrets, active plan/phase state, unsupported impressions, obvious repository facts maintained by code/docs, or advice that cannot change a future decision or evaluation. A one-off incident stays in task evidence.

## Admission gate

Keep a candidate only when every answer is yes:

1. **Provenance:** Is there an exact source: an explicit user/team judgment, verified artifact/source, observed result, or clearly labelled inference from repeated evidence?
2. **Counterfactual value:** Without it, is a future agent likely to choose or judge materially worse, miss a consequential constraint, or repeat meaningful discovery cost? Reject novel but inert information.
3. **Reuse:** Is the choice, evaluation, or knowledge likely to recur for this project, product, team, or fleet beyond the originating incident?
4. **Novelty and recoverability:** Is it absent from authoritative code, docs, skills, and searched memory, or does it materially correct/refine them? When the owner answers cheaply, retain a pointer or promotion rather than a competing explanation.
5. **Scope and authority:** Can it state who/what it is authoritative for without turning preference into fact, inference into rule, or project lesson into fleet doctrine?
6. **Safety and stability:** Can it be retained without prohibited content or volatile task state, with a source pointer and invalidation or freshness condition where needed?

Reject or merge candidates failing any gate.

An explicit user correction or choice evidences that user's or team's judgment within its stated scope, not universal correctness. Patterns inferred from accepted/rejected work stay advisory and labelled inferred.

A caution candidate holds an action back. It must state its scope and its reason; reject it when either is missing. When the agent keeps the action through approval, write "ask for approval before <exact action>", not "never <action>", because a "never" rule blocks routine work the task needs. Keep "never" only for a true invariant, with its reason. When the reason of a caution no longer holds, reject the candidate. When that caution is already published, report it to /alaa-memory-os as a candidate for status `stale`, with the expired reason and its evidence; that owner keeps the write authority.

## Choose the reusable form

- **Decision interface:** a repeatable condition must select an action, check, fallback, escalation, or stop.
- **Judgment rubric:** a future agent must evaluate quality, taste, tradeoffs, or competing acceptable options.
- **Knowledge card:** a non-obvious fact or operating context changes reasoning without prescribing a procedure or quality judgment.

| You are about to | Read | Decision owned there |
|---|---|---|
| Shape a candidate that passed admission | `references/reusable-context-shapes.md` | Common provenance, three reusable forms, compression and classification; not a memory-note schema. |

## Route the result

1. Return engagement-local candidates to the workflow-selected location under /alaa-workflow `references/context-curation.md`. Link its canonical record. Do not duplicate active state.
2. When repository code, docs, an instruction file or an existing skill owns the knowledge, promote through that owner only within task authority. Otherwise return a source pointer or promotion candidate naming its owner. Ordinary source-owned facts are not competing durable explanations. If a final scan discovers an authorized repository promotion after evidence freeze, return `pipeline reopen required` to workflow. Do not change closed evidence.
3. Before drafting controlling content for a prompt, skill, agent, `AGENTS.md` or `CLAUDE.md`, invoke /alaa-prompting-guide for authoring/compression. This lane grants no new promotion authority.
4. Before authorized durable publication, invoke /alaa-memory-os. It alone owns search-before-create, note shape, adapters, write authority, drift and prohibited content. Scan deduplication remains here. Do not repeat a sufficient admission memory search.
5. If publication is unauthorized, unavailable or lacks terminal confirmation, return admitted candidates to workflow as not persisted, with the reason. Keep valid candidates despite a store outage.

## Output and stop conditions

Report:

- scanned boundaries
- retained candidates by form
- each candidate's provenance, authority and destination
- merged/rejected candidates, each with a short reason
- notes created, updated, reported as `stale` candidates, or deliberately unwritten
- promotion or drift still needing an owner

Stop successfully when every admitted candidate has one form, scoped authority, source pointer,
destination, no prohibited content, and a reported disposition. An empty retained set qualifies.
A `pipeline reopen required` verdict leaves the workflow open.

Stop blocked only when a required source cannot be inspected, an authorized drift record cannot be written, or a mandatory owner rejects the handoff. Do not loop extraction or memory searches for reassurance. /alaa-memory-os owns bounded search-before-create.
