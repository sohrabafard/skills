---
name: alaa-extract-agent-lessons
description: "Reusable-context curation for substantial agent work and conversations. Use when /alaa-workflow invokes a curation scan or the user requests reusable lessons to extract evidence-backed decision interfaces, judgment rubrics, and durable knowledge cards from explicit user or team decisions, accepted or rejected work with reasons, non-obvious product or team knowledge, verified surprises, costly detours, validation failures, or coordination bottlenecks. Keep active candidates in alaa-workflow and publish only authorized durable knowledge through alaa-memory-os. Do not use for raw logs, status, active plans, speculative advice, obvious repository facts, or one-off workarounds."
---

# Alaa Extract Agent Lessons

Curate the smallest reusable context that changes future work. Preserve what to choose as a decision
interface, how to judge as a rubric, or what non-obvious context to know as a knowledge card. Discard the
chronology that merely happened once.

Valuable does not mean merely interesting or new. Without the candidate, a future agent must be likely to
make a worse decision, misjudge acceptable work, miss consequential context, or repeat expensive discovery.

## Scan contract

/alaa-workflow `references/context-curation.md` owns scan timing, the intermediate/final distinction,
evidence stability, candidate location and reopening consequences. Consume its selected scan scope and
recording destination; do not create a second phase schedule, handoff schema or task state here.

For an intermediate scan, assess only evidence since the previous recorded boundary. For a final scan,
reconcile the engagement evidence and provisional candidates, merge duplicates and return each disposition.
If nothing passes admission, return an empty result; never manufacture a lesson to satisfy a gate.

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

| You are about to | Read | Decision owned there |
|---|---|---|
| Shape a candidate that passed admission | `references/reusable-context-shapes.md` | Common provenance, three reusable forms, compression and classification; not a memory-note schema. |

## Route the result

1. Return engagement-local candidates to the workflow-selected location under /alaa-workflow
   `references/context-curation.md`. Link its canonical record rather than duplicating active state.
2. When repository code, docs, an instruction file or an existing skill owns the knowledge, promote through
   that owner only within task authority; otherwise return a source pointer or promotion candidate with its
   owner. An ordinary source-owned fact is not a competing durable explanation. If a final scan discovers an
   authorized repository promotion after evidence freeze, return `pipeline reopen required` to workflow
   instead of changing closed evidence.
3. Before drafting controlling content for a prompt, skill, agent, `AGENTS.md` or `CLAUDE.md`, invoke
   /alaa-prompting-guide for authoring and compression. This lane grants no new promotion authority.
4. Before authorized durable publication invoke /alaa-memory-os. It alone owns search-before-create, note
   shape, adapters, write authority, drift and prohibited content. Candidate deduplication within the scan
   remains here; do not repeat a sufficient memory search performed for admission.
5. If publication is unauthorized, unavailable or fails to reach terminal confirmation, return admitted
   candidates to workflow as not persisted with the reason. Keep valid candidates despite a store outage.

## Output and stop conditions

Report the boundaries scanned; retained candidates grouped by form; provenance, authority, and destination for
each; candidates merged or rejected with a short reason; notes created, updated, or deliberately not written;
and promotion or drift that still needs an owner.

Stop successfully when every admitted candidate has one form, one scoped authority, one source pointer, one
destination, no prohibited content, and a reported disposition, including when the retained set is empty. A returned reopening verdict
is unresolved work, not completion. Return `pipeline reopen required` when an authorized canonical repository change remains
after evidence freeze. Stop blocked only when a required source cannot be inspected, an authorized drift record
cannot be written, or a mandatory owner rejects the handoff. Do not loop extraction or memory searches for reassurance; /alaa-memory-os owns the bounded
search-before-create pass.
