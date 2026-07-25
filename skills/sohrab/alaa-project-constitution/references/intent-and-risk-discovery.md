# Intent and Risk Discovery

Read this reference for every CREATE or UPDATE, after matching archetypes in
`project-archetypes.md`. Repository inventory shows what exists; this step establishes which
obligations the project owes and how each one enters or stays out of the constitution.

## The fact/obligation seam

Two claim classes travel through this workflow and the anti-fabrication rules apply to exactly
one of them. Confusing them is what makes a constitution either dishonest or useless.

- **A repository fact** is a statement about *this* repository: what it currently runs, which
  endpoints, jobs, queues, or tables exist, which limits are configured, which contracts are in
  force, which dates and approvals were recorded. Never state a repository fact without an
  inspected source. Never infer one from a dependency name, a convention, or a plausible default.
- **A domain obligation** is a statement about what a service of this kind must guarantee.
  Prescribing that a browser client holds a Largest Contentful Paint budget, or that a queue
  consumer is idempotent, is a standard being applied — not a fact being invented. The archetype
  layer and `quality-bar.md` authorise these, and they are prescribed whether or not the code
  implements them yet.

Keep the four claim labels distinct in working state, and never write a prescription in the
voice of an observation:

| Label | Means | Can it become binding? |
|---|---|---|
| `OBSERVED` | Inspected repository truth, with a path | Yes, as a fact the constitution relies on |
| `INHERITED` | A rule from still-valid prior governance | Yes, preserved unless evidence contradicts it |
| `INFERRED_CANDIDATE` | An obligation prescribed by a matched archetype or the quality bar | **Yes.** This is the normal route for an obligation the code does not implement yet |
| `OWNER_DECIDED` | A choice the owner made in this run or a prior one | Yes |

`INFERRED_CANDIDATE` is a first-class route to binding law, not a holding pen for material that
gets pruned. What it may never do is assert current behaviour: it prescribes what must hold, and
where the current state is unknown or non-conformant, the rule is accompanied by a non-blocking
factual TODO recording the gap. These labels are working state and never appear in
CONSTITUTION.md.

## Build the project-intent model

Synthesize, in this order:

1. explicit user context and owner decisions from the current request, including any supplied
   RFP, specification, or reference material;
2. the complete prior constitution — preserved principles, TODOs, proposals, exceptions,
   canonical-source pointers, and status/version evidence;
3. repository identity, owned journeys, runtime surfaces, data flows, trust boundaries,
   deployment model, consumers, and operational expectations;
4. the matched archetypes and their mandatory obligations.

Build the prior-decision map from an existing constitution as
`update-versioning-and-binding.md` specifies, and preserve its semantic intent unless current
truth contradicts it or the owner approves a normative change.

Write a one-paragraph internal intent statement covering who the project serves, what outcome
it owns, which failure classes matter, and which qualities are load-bearing. A supplied RFP or
specification is owner-provided intent evidence and outranks inference about goals — it does not
establish repository facts.

## Expand the risk horizon

Walk the ten obligations in `quality-bar.md` for every owned journey and high-risk surface, and
walk the mandatory obligations of every matched archetype.

Every horizon that applies to an evidenced surface produces at least one dispositioned
candidate, and a horizon you set aside is set aside with a stated reason and the evidence path
that supports it rather than by silence. Not every horizon becomes a constitutional article —
the dispositions below are how one leaves — but an obligation that a matched archetype marks
mandatory becomes an article whether or not the repository implements it yet.

Use counterfactuals to make an obligation concrete: peak load, dependency outage, process
restart, duplicate delivery, concurrent writes, stale cache, network interruption, partial
rollout, expired credentials, storage exhaustion, and rollback, plus the archetype-specific
counterfactuals in `project-archetypes.md`.

Counterfactuals establish which obligations apply; they never establish what the repository
currently does. Never state an unobserved implementation as current behaviour. Never write a
numeric threshold, score, percentile, or version gate from memory: for every budget an
obligation requires, fetch the current value from its primary source, then record the value with
its source URL and verification date.

## Research the obligation's current numbers

Research is mandatory for every obligation a matched archetype marks mandatory, and for every
claim whose current value is version-sensitive. Run it after the intent model and the archetype
match are written, so each query names a surface and a failure mode rather than a topic.

Source priority and the freshness rule are owned by `freshness-source-map.md`. Record source,
verification date, applicability, and limitation for every value used.

When live verification is unavailable, write the rule with the metric named and the budget marked
unresolved through a non-blocking factual TODO. State the obligation and defer only the number.
Dropping the obligation because the number could not be fetched inverts the failure: a stated
metric with a pending value governs behaviour, and a missing rule governs nothing.

## Disposition every candidate

A practice becomes constitutional law by one of two routes and no other: a matched archetype or
the quality bar marks it mandatory, or repository evidence, still-valid prior governance, or an
explicit owner decision requires it. A practice with neither route is reported outside
CONSTITUTION.md rather than promoted because it is widely recommended.

Choose exactly one disposition per candidate:

- `REQUIRED_BY_ARCHETYPE`: a matched archetype or a quality-bar obligation makes it mandatory.
  Write the minimum durable rule, name the metric or the observable condition, and add a factual
  TODO for any value or current state still unverified. Do not wait for the code to implement it.
- `REQUIRED_BY_EVIDENCE`: repository truth or already-ratified governance proves it; retain or add
  the minimum durable rule.
- `OWNER_DECISION_REQUIRED`: credible alternatives exist and the choice changes product promise,
  security or privacy posture, compatibility, cost, data lifecycle, or operational risk. Ask
  interactively. Use this for *which* option, never for *whether* an archetype obligation applies.
- `DELEGATE_TO_CANONICAL_SOURCE`: the obligation stands, but its technical detail belongs in a
  named architecture document, contract, runbook, standard, or generated owner. The constitution
  keeps the obligation and the named owner.
- `NON_CONSTITUTIONAL_FOLLOW_UP`: a useful implementation improvement that no archetype or
  quality-bar obligation requires; report it outside CONSTITUTION.md.
- `NOT_APPLICABLE`: positive evidence places the surface outside owned scope. Record the evidence
  path. Absence of an implementation is never this evidence.
- `UNKNOWN`: inspection remains insufficient to tell whether the surface is owned; use a
  structured TODO when material.

## Coverage gate

Before writing, verify that:

- every matched archetype's mandatory obligations have a disposition, and every
  `NOT_APPLICABLE` carries an evidence path;
- each owned journey and high-risk surface was walked against the ten quality-bar obligations;
- every prescribed obligation carrying a number has a fetched value with source and date, or a
  non-blocking factual TODO in its place;
- no prescribed obligation is phrased as an observation of current behaviour;
- external sources did not overwrite repository truth or prior ratified governance;
- content for stacks and domains the project does not own was removed;
- the final constitution keeps durable project-specific rules and closed delegations only.

If discovery yields many implementation ideas that no obligation requires, keep them out of
CONSTITUTION.md and summarize the highest-value follow-ups separately in the final response.
