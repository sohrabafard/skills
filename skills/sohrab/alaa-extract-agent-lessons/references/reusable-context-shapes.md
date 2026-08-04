# Reusable Context Shapes

Read this file only after a candidate passes the admission gate in `SKILL.md`. The fields below shape a
candidate before routing. They do not replace the repository owner's contract or the note schema owned by
`alaa-memory-os`.

## Common provenance envelope

Every retained candidate carries:

- **Kind:** decision interface, judgment rubric, or knowledge card.
- **Scope and trigger:** where it applies and the observable condition that makes it relevant.
- **Reusable content:** the rule, rubric, or knowledge in its shortest lossless form.
- **Value case:** the worse decision, misjudgment, hidden constraint, or repeated discovery cost expected if the
  candidate is absent.
- **Provenance:** exact source pointer plus what that source established.
- **Authority:** verified fact, explicit user or team judgment, inferred advisory pattern, or proposal.
- **Confidence and unknowns:** what is established and what remains unverified.
- **Owner and destination:** active workflow handoff, canonical repository surface, durable memory, or promotion
  candidate.
- **Freshness or invalidation:** what change, date-sensitive condition, or contradiction requires re-checking it.

Authority and confidence are independent. An explicit preference can be authoritative for one user and still
have narrow scope; a source-backed fact can have high confidence and still expire when a dependency changes.

## Decision interface

Use when a future condition must select what happens next:

- **Trigger:** observable activation condition.
- **Inputs:** facts required before deciding.
- **Classification:** distinctions that must not be collapsed.
- **Decision:** rule that selects the next action.
- **Action:** smallest safe response.
- **Proof:** evidence required before claiming success.
- **Stop or fallback:** when to stop, report blocked, split scope, or use a bounded substitute.
- **Anti-pattern:** tempting behavior that creates false confidence or wasted work.

## Judgment rubric

Use when several outputs could be correct and the missing context is how the user, team, or product judges
quality:

- **Decision question:** what is being evaluated or chosen.
- **Signals:** observable qualities or context that affect the judgment.
- **Priorities:** what good work optimizes first, in order when order matters.
- **Tradeoffs:** what may be sacrificed, and what must not be traded away.
- **Boundaries and exceptions:** where this judgment does not apply or another owner wins.
- **Calibration anchors:** accepted or rejected cases and their reasons, only when they encode a distinction not
  already clear from the rubric.
- **Evaluation:** how a future agent can demonstrate alignment without pretending taste is an objective fact.

Preserve the deciding rationale. A bare "the user liked this" is history; "the user chose the denser layout
because scan speed mattered more than whitespace for this admin surface" is reusable judgment with a scope.

## Knowledge card

Use when non-obvious context changes reasoning without directly selecting an action or defining quality:

- **Claim:** concise non-obvious fact or operating context.
- **Why it matters:** the future decision or failure it affects.
- **Applicability:** project, product, team, environment, or fleet scope.
- **Verification:** canonical source and how it was checked.
- **Best reference:** the highest-fidelity code, test, specification, mockup, artifact, or source pointer when a
  rich reference carries the knowledge better than prose.
- **Consequence:** what a future agent must account for after recalling it.
- **Invalidation:** the change that makes the card stale or wrong.

If current repository code or documentation can answer the fact cheaply, store a pointer or update the owner;
do not create a second source of truth.

## Semantic compression test

A candidate is strong, concise, and useful only when a future agent can consume it without the originating
chat and answer all four questions: where does it apply, what distinction changes, why does that distinction
matter, and how can it be re-verified? Rewrite or reject a candidate that depends on pronouns, chronology, or
unstated context from the conversation.

Compression is lossless with respect to the future decision. Remove narration, repeated examples, and
incidental commands; retain the scoped claim or rubric, the deciding rationale, the contrast that separates
acceptable from unacceptable behavior, and the invalidation condition. If removing the candidate would not
predictably worsen a choice, an evaluation, reasoning, or discovery cost, it is not valuable context.

## Classification test

Ask in order:

1. Does the candidate tell the agent which action to take under observable conditions? Use a decision interface.
2. Does it tell the agent how to distinguish better from worse among acceptable options? Use a judgment rubric.
3. Does it supply non-obvious context needed before either choice? Use a knowledge card.
4. If none applies, reject it as incident history, status, or generic advice.

Split a candidate only when two forms have independent reuse. Otherwise choose the form carrying the main value
and place the supporting fact or rationale inside it.

## Compression rules

- Keep one reusable idea per candidate.
- Lead with a concrete subject and claim; do not open with session history or a generic lesson label.
- Preserve exact rationale, scope, caveats, counterexamples, and invalidation conditions.
- Remove chronology, narration, incidental command names, transient counts, and raw error text.
- Keep an identifier only when it is itself a stable contract or necessary source pointer.
- Keep examples only when they encode a real boundary or measured gap; decorative examples constrain future
  exploration and add no reusable knowledge.
- Never generalize one person's explicit judgment into team or fleet policy without evidence and authority.

## Design basis

The [context-engineering source supplied for this change](https://x.com/trq212/status/2080710971228918066)
supports progressive disclosure, model judgment over blanket constraints, skills that encode team or product
opinions and knowledge, and rubrics as references for evaluating taste. The source motivates these forms; the
admission and authority rules above remain this pack's contract.
