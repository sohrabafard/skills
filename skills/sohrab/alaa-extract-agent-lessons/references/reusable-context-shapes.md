# Reusable Context Shapes

Read only after `SKILL.md` candidate admission. These fields shape candidates before routing; they replace
neither the repository owner's contract nor `alaa-memory-os`'s note schema.

## Common provenance envelope

Every retained candidate carries:

- **Kind:** decision interface, judgment rubric, or knowledge card.
- **Scope and trigger:** applicability and observable activation condition.
- **Reusable content:** rule, rubric, or knowledge in its shortest lossless form.
- **Value case:** worse decision, misjudgment, hidden constraint, or repeated discovery cost expected without it.
- **Provenance:** exact source pointer and what it established.
- **Authority:** verified fact, explicit user/team judgment, inferred advisory pattern, or proposal.
- **Confidence and unknowns:** established and unverified matters.
- **Owner and destination:** active workflow handoff, canonical repository surface, durable memory, or promotion
  candidate.
- **Freshness or invalidation:** change, date-sensitive condition, or contradiction requiring re-checking.

Authority and confidence are independent: a preference can be authoritative for one user but narrow; a
source-backed fact can be highly confident but expire when a dependency changes.

## Decision interface

Use when a future condition must select what happens next:

- **Trigger:** observable activation condition.
- **Inputs:** facts required before deciding.
- **Classification:** distinctions that must not be collapsed.
- **Decision:** rule selecting the next action.
- **Action:** smallest safe response.
- **Proof:** evidence required before claiming success.
- **Stop or fallback:** when to stop, report blocked, split scope, or use a bounded substitute.
- **Anti-pattern:** tempting behavior creating false confidence or wasted work.

## Judgment rubric

Use when several outputs could be correct and missing context determines how the user, team, or product
judges quality:

- **Decision question:** what is evaluated or chosen.
- **Signals:** observable qualities or context affecting judgment.
- **Priorities:** what good work optimizes first, ordered when order matters.
- **Tradeoffs:** what may be sacrificed and what must not.
- **Boundaries and exceptions:** where the judgment does not apply or another owner wins.
- **Calibration anchors:** accepted/rejected cases and reasons, only for distinctions not already clear.
- **Evaluation:** how a future agent demonstrates alignment without treating taste as objective fact.

Preserve deciding rationale. "The user liked this" is history; "the user chose the denser layout because
scan speed mattered more than whitespace for this admin surface" is scoped reusable judgment.

## Knowledge card

Use when non-obvious context changes reasoning without directly selecting an action or defining quality:

- **Claim:** concise non-obvious fact or operating context.
- **Why it matters:** affected future decision or failure.
- **Applicability:** project, product, team, environment, or fleet scope.
- **Verification:** canonical source and how it was checked.
- **Best reference:** highest-fidelity code, test, specification, mockup, artifact, or source pointer when a
  rich reference conveys knowledge better than prose.
- **Consequence:** what a future agent must account for after recall.
- **Invalidation:** change making the card stale or wrong.

If current repository code/docs answer the fact cheaply, store a pointer or update the owner; create no
second source of truth.

## Semantic compression test

A candidate is strong, concise and useful only when a future agent, without the originating chat, can
answer: where does it apply, what distinction changes, why does it matter, and how can it be re-verified?
Rewrite or reject candidates depending on pronouns, chronology, or unstated conversation context.

Compression preserves the future decision. Remove narration, repeated examples and incidental commands;
retain the scoped claim/rubric, deciding rationale, acceptable/unacceptable behavior distinction and
invalidation condition. If removal would not predictably worsen choice, evaluation, reasoning or discovery
cost, it is not valuable context.

## Classification test

Ask in order:

1. Does it select an action under observable conditions? Use a decision interface.
2. Does it distinguish better from worse among acceptable options? Use a judgment rubric.
3. Does it supply non-obvious context needed before either choice? Use a knowledge card.
4. Otherwise reject it as incident history, status, or generic advice.

Split only when two forms have independent reuse. Otherwise choose the form carrying the main value and
include supporting fact/rationale inside it.

## Compression rules

- Keep one reusable idea per candidate.
- Lead with a concrete subject and claim, never session history or a generic lesson label.
- Preserve exact rationale, scope, caveats, counterexamples and invalidation conditions.
- Remove chronology, narration, incidental command names, transient counts and raw error text.
- Keep identifiers only when they are stable contracts or necessary source pointers.
- Keep examples only for real boundaries or measured gaps; decorative examples constrain future exploration
  without adding reusable knowledge.
- Never generalize one person's explicit judgment into team/fleet policy without evidence and authority.

## Design basis

The [context-engineering source supplied for this change](https://x.com/trq212/status/2080710971228918066)
supports progressive disclosure, model judgment over blanket constraints, skills that encode team or product
opinions and knowledge, and rubrics as references for evaluating taste. The source motivates these forms; the
admission and authority rules above remain this pack's contract.
