# Interactive Decisions and the Canonical Launcher

Read this reference for every CREATE, UPDATE, or RATIFY operation. Repository evidence answers
facts; matched archetypes prescribe obligations; the owner answers only the material decisions
that neither of those can settle.

## The canonical launcher

"Canonical launcher" is the condition that authorises finalizing and binding without a second
approval question. It is a property of the user's request, not of the skill.

A request is a canonical launcher when it contains all four of these, in any wording or language:

1. an instruction to create or update the repository-root constitution;
2. an instruction to ask only the unresolved owner decisions;
3. an explicit conditional that finalizing and binding follow from answering every question
   without deferral;
4. an explicit alternative that a deferral leaves a draft, unbound.

`assets/first-message-prompt.md` holds the paste-ready CREATE and UPDATE launchers that satisfy
all four parts, together with the invocation syntax for both runtimes. Quote the matching launcher
from there verbatim when telling a user how to start, and use the four-part test above to judge
any other request. A request missing the conditional clause in point 3 is **not** canonical:
completion of the questions is then not authorization, and the result stays DRAFT until the owner
explicitly approves finalization.

Appending project context, priority source paths, or explicit owner decisions to a launcher does
not affect its canonical status.

## Ask/no-ask filter

Ask a question only when all four conditions hold:

1. Current repository evidence, a matched archetype's mandatory obligations, and a still-valid
   prior constitution do not answer it.
2. The answer materially changes the product or user promise, offline or degraded behaviour,
   scope, authority, trust/security/privacy posture, cost or resource commitment, data lifecycle,
   compatibility, mandatory validation, exception policy, ownership, status, or ratification.
3. Omitting the topic, or recording a non-blocking factual TODO instead, would make the
   constitution unsafe, misleading, internally inconsistent, or impossible to ratify.
4. The user is able to make or route the decision.

Do not ask about detectable stacks, files, commands, routes, modules, current behaviour, existing
contracts, research facts, or numeric limits a canonical source already owns. Do not ask for an
optional preference merely because the template contains a placeholder.

**Never ask whether a matched archetype's mandatory obligation applies.** The archetype layer
already decided that. Ask which option satisfies it when credible alternatives change a durable
promise — for example which conformance level, which support window, or whether AI crawlers are
permitted — and write the obligation itself without asking.

## Question budget

- Ask at most three questions in one batch, then pause for answers and recompute the gaps.
- Normally use no more than two batches. Ask at most one additional follow-up, and only when an
  answer creates a new blocking conflict.
- If essential gaps remain after that budget, prioritise authority and scope, product promise,
  security and privacy, data lifecycle, mandatory validation, and ratification. Convert the
  remainder to structured TODOs and leave a DRAFT rather than running an unbounded interview.
- After a `Decide later`, stop nonessential questioning; ask only what prevents an unsafe or
  incoherent draft.
- Pause after presenting questions. If the runtime times out or resumes without an answer,
  classify the unanswered decision as DEFERRED; never auto-select the recommendation.

## Required question shape

Use the runtime's structured multiple-choice question tool when available; otherwise render the
same structure in chat. Ask one decision per question with two or three mutually exclusive
options:

1. Put the recommended option first and suffix its label with `(Recommended)`.
2. Give one sentence explaining why repository evidence, a matched archetype, or the trade-off
   supports it.
3. Give each alternative one sentence describing its impact.
4. Include `Decide later`, or its exact equivalent in the user's language, and state that it
   creates a DRAFT/NON_BINDING constitution and defers AGENTS.md and CLAUDE.md binding.
5. Allow a free-form alternative when the runtime supports it; do not duplicate an automatic
   `Other` option the UI already supplies.

Do not invent a recommendation. When evidence is insufficient or the choice is primarily a
business decision, make `Decide later (Recommended)` the honest recommendation and state which
evidence or owner decision is missing.

## Decision outcomes

Record selected answers in internal working state and the final response. Put an answer in
CONSTITUTION.md only when it creates a durable rule or an unresolved blocking decision.

- `COMPLETE`: every essential question was answered and no decision was deferred.
- `DEFERRED`: the user selected `Decide later`, did not answer, or the question budget left an
  essential owner decision unresolved.

Record every unresolved item on a single physical line, in exactly this shape, because the bundled
validator matches it as one line:

```text
TODO(<stable-id>): <decision still required>; reason: <gap>; owner: <role or UNKNOWN>; blocking: yes.
```

A deferred owner decision is `blocking: yes`. An unverified number or an unknown current state
behind an obligation that is otherwise written is `blocking: no` — it records a factual gap and
does not prevent ratification, because the rule already governs.

Unapproved policy uses the same single-line discipline:

```text
PROPOSAL(<stable-id>): <candidate rule>; evidence/rationale: <why>; approval required from: <role or UNKNOWN>.
```

For CREATE or an already non-binding baseline, `DEFERRED` forces DRAFT/NON_BINDING. For an
existing BINDING baseline, `DEFERRED` preserves the canonical constitution, its version, status,
and adapters unchanged unless the owner explicitly chose `Replace with draft`. Never create,
update, or activate a draft adapter or import in AGENTS.md or CLAUDE.md.

## Automatic finalization contract

Under a canonical launcher as defined above:

- `COMPLETE` — when every essential question was answered without deferral, or evidence and the
  archetype layer left no essential question, finish both writing passes, record the launcher plus
  the answer summary as the owner's finalization decision in working state and the final response,
  record only the durable normative amendment in any existing amendment record, set BINDING, and
  align the thin root bindings in the same run. Do not ask a redundant final approval question.
- `DEFERRED` — leave a new or non-binding result DRAFT and unbound, or preserve an existing
  BINDING baseline and report the pending proposal outside it.

Without a canonical launcher, completion alone is not ratification: ask for explicit approval or
leave the result DRAFT.

## Existing BINDING constitution edge case

Never silently replace or demote an active BINDING constitution with an unresolved draft. When an
UPDATE introduces a deferred material change, ask one essential transition question with the
options `Preserve current binding baseline (Recommended)`, `Replace with draft`, and
`Decide later`. `Decide later` preserves the existing file and its bindings unchanged and reports
the proposed decision gap. Replacing an active binding baseline requires explicit approval and a
repository-supported history or supersession path.

## Draft handoff

The final response for a DRAFT lists the unresolved IDs, states that no binding was performed,
and includes this paste-ready continuation prompt:

```text
From the repository root, finalize `CONSTITUTION.md`. Ask only the unresolved decisions in the
`Unresolved Decisions` section or the unresolved IDs listed in the prior report, with options and
evidence-backed recommendations. Keep every prescribed obligation already written; resolve only
the listed decisions. If I answer all of them without deferring any, finalize the constitution as
BINDING and align the thin root `AGENTS.md` and `CLAUDE.md` bindings; otherwise keep it DRAFT and
unbound.
```
