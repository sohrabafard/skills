# <NNNN> — <Title>

Status: draft | reviewed | built | superseded | not-required
Trigger condition: <which of the six fired>
Owner: <person or team>   Reviewer: <who reviewed>   Date: <YYYY-MM-DD>
Supersedes: <record or none>   Superseded by: <record or none>

Keep this record to two screens. Every section below is present in every record. A section that does not
apply carries one line naming why, with the evidence that puts it out of scope.

## 1. Frame

Problem, in two sentences. The outcome this subsystem owns.
Journeys affected: <list>
From the constitution: <archetype identifiers matched, and the counterfactuals carried in>

## 2. Scope and boundary

Inside this design: <components you may change in this release>
Dependencies: <component — owner — contract consumed>
Seam: <where the writer of the data changes>
Boundary tests: data <pass/fail — evidence> | change <pass/fail — evidence> | failure <per caller>
Decision: extend <component> | new service <name>
Conditions met: <which of the five, with the evidence that settled each>

## 3. Contract

Interfaces (enumerate each kind or mark none): routes served | calls made | events emitted | events
consumed | jobs enqueued | jobs consumed | scheduled triggers | other readers or writers of this state

| Interface | Caller | Sync/async | Crosses trust boundary | Safe to repeat |
|---|---|---|---|---|

Data shapes: <field — type — absent/null meaning — unit — identifier kind>, or the path of the contract
file that carries them
Error surface: <outcome — what the caller does — retryable by the caller>
Compatibility: <per consumer — must change / need not change — when>
Platform invariants cited: <references in /alaa-services-contract — $alaa-services-contract>

## 4. Data and consistency

| Datum | Owner | Writers | Readers | How readers read it |
|---|---|---|---|---|

Read path / write path per critical journey, with staleness at each hop: <…>
Read-your-own-writes required: <where, and the mechanism>
Consistency per interaction: <interaction — model — bound / compensator / convergence trigger>
Interleavings ruled out: lost update | double effect | out-of-order | cross-tenant read — <mechanism class>
Second copies: <name — cache (key, max age, invalidation, miss and outage behaviour) | fork (winner,
reconciliation path, who runs it, drift signal)>

## 5. Failure and load

| Dependency | Classification | Caller-visible failure | Assumed load | Source of bounds |
|---|---|---|---|---|

Assumed peak per entry point: <rate, concurrency, and where the figure came from>
Growth horizon: <multiple, over what period>
First resource to saturate: <resource, and at what point>
New failure modes and the question an operator will ask: <…>

## 6. Alternatives

Candidates considered: <A, B, …> — distinct on <boundary | data owner | consistency>
Winner: <candidate> — won on <axis>, lost on <axis>
Rejected:
- <candidate> — lost on <axis>: <why> — revisit if <observable condition>

## 7. Rollout and reversal

Ship order: <what deploys first, and what must be live before it>
Mixed-version behaviour: <what the system does between the first deploy and the last>
Reversal: <what a rollback does to data already written in the new shape>
Irreversible after: <the point, or "reversible throughout">
Deprecation: <cite the procedure if a consumer-observable surface changes>

## 8. Open questions

| Question | Owner | Decision it blocks, or "blocks nothing" |
|---|---|---|
