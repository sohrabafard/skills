# Interactive Decision Workflow

Read this for every CREATE, UPDATE, or RATIFY operation. Repository evidence answers facts;
the user answers only material owner decisions that evidence cannot establish.

## Ask/no-ask filter

Ask a question only when all conditions hold:

1. Current repository evidence and a still-valid prior constitution do not answer it.
2. The answer materially changes scope, authority, trust/security posture, mandatory
   validation, exception policy, ownership, status, or ratification.
3. Omitting the topic or recording a non-blocking factual TODO would make the constitution
   unsafe, misleading, internally inconsistent, or impossible to ratify.
4. The user is able to make or route the decision.

Do not ask about detectable stacks, files, commands, routes, modules, current behavior,
existing contracts, or numeric limits already owned by a canonical source. Do not ask for
optional preferences merely because the template contains a placeholder.

## Question budget

- Ask at most three questions in the initial batch.
- Ask at most one follow-up question, and only if an answer creates a new blocking conflict.
- Never exceed four total questions in one run.
- If more gaps exist, prioritize authority/scope, security/trust, mandatory validation,
  and ratification. Convert lower-priority gaps to structured TODOs and use DRAFT.
- After `Decide later`, stop further nonessential questions; ask only what is necessary to
  prevent an unsafe or incoherent draft.
- Pause after presenting questions. If the runtime times out or resumes without an answer,
  classify the unanswered decision as DEFERRED; never auto-select the recommendation.

## Required question shape

Use the runtime's structured multiple-choice question tool when available; otherwise render
the same structure in chat. Ask one decision per question and provide 2-3 mutually exclusive
options:

1. Put the recommended option first and suffix its label with `(Recommended)`.
2. Give one sentence explaining why repository evidence and trade-offs support it.
3. Give each alternative one sentence describing its impact.
4. Include `Decide later` or the exact equivalent in the user's language. Explain that it
   creates a DRAFT/NON_BINDING constitution and defers AGENTS.md/CLAUDE.md binding.
5. Allow a free-form alternative when the runtime supports it; do not duplicate an automatic
   `Other` option supplied by the UI.

Do not invent a recommendation. When evidence is insufficient or the choice is primarily a
business decision, make `Decide later (Recommended)` the honest recommendation and explain
what evidence or owner decision is missing.

## Decision outcomes

Record selected answers in internal working state and the final response. Put an answer in
CONSTITUTION.md only when it creates a durable rule or an unresolved blocking decision.

- `COMPLETE`: every essential question was answered and no decision was deferred.
- `DEFERRED`: the user selected `Decide later`, did not answer, or the question budget left
  an essential owner decision unresolved.

For each deferred decision, record:

```text
TODO(<stable-id>): <decision still required>; reason: owner selected Decide later or the
evidence cannot decide it; owner: <role or UNKNOWN>; blocking: yes.
```

`DEFERRED` forces DRAFT/NON_BINDING. Do not create, update, or activate a constitution
adapter/import in AGENTS.md or CLAUDE.md.

## Automatic finalization contract

The canonical first message explicitly authorizes this branch:

- `COMPLETE`: when every essential question was answered without deferral, or evidence left
  no essential question, finish both writing passes, record the launcher plus answer summary
  as the owner finalization decision, set BINDING, and align thin root bindings in the same
  run. Do not ask a redundant final approval question.
- `DEFERRED`: leave DRAFT/NON_BINDING and do not bind.

For a request that does not contain equivalent conditional finalization intent, completion
alone is not ratification; ask for explicit approval or leave the result DRAFT.

## Existing BINDING constitution edge case

Never silently replace or demote an active BINDING constitution with an unresolved draft.
If an UPDATE introduces a deferred material change, ask one essential transition question:
`Preserve current binding baseline (Recommended)`, `Replace with draft`, or `Decide later`.
`Decide later` preserves the existing file and bindings unchanged and reports the proposed
decision gap. Replacing an active binding baseline requires explicit approval and a
repository-supported history/supersession path.

## Draft handoff

The final response for DRAFT must list unresolved IDs, state that no binding was performed,
and include this paste-ready continuation prompt:

```text
From the repository root, finalize `CONSTITUTION.md`. Ask only the unresolved decisions in
Section 13, with options and evidence-backed recommendations. If I answer all of them without
deferring any, finalize the constitution as BINDING and align the thin root `AGENTS.md` and
`CLAUDE.md` bindings; otherwise keep it DRAFT and unbound.
```
