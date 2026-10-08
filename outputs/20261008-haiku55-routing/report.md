# Claude model routing and verification consolidation

The final local source routes Claude work across four models and consolidates repeated verification scheduling while preserving independent acceptance gates. Final snapshot `994cc8ead494a4cfef0f94cd6831b93cb67997e2db97d904223ee357a7d52782` passed all nine checks. The six-check Phase 3 pass belongs to an older snapshot and is historical evidence only.

## Model routing

| Model | Profiles | Initial effort assignment |
|---|---|---|
| Sonnet 5.5 | 8: researcher; implementer, test strategist, dependency auditor, accessibility reviewer, performance profiler, observability reviewer, release guardian | Medium for researcher; high for the other seven |
| Haiku 5.5 | 4: explorer, verifier, documenter, browser QA | Medium |
| Opus 5.5 | 8, including the lead | Medium for lead and specification; high for implementation, review, and specialist roles |
| Fable 5.1 | 5 difficult-judgment profiles | High |

The policy contains 25 profiles including the lead, 24 projections including the rule writer, and 23 Claude Code agents. Haiku 4.5 is forbidden as an active model; Haiku 5.5 availability fails closed. These effort assignments are unrun hypotheses, not measured quality or speed rankings. Calibration and latency measurement were not run. The [source record](source-evidence.md) links the dated official capability and model sources.

## Verification behavior

The paired orchestrators now use one owned aggregate check inventory. A grouped check may cover its children only when scope, flags, and environment match; uncovered checks remain separate, and the independent verifier and reviewer retain their authority. Re-run checks when relevant inputs change. This consolidation does not guarantee faster runs.

## Role migration and limits

The Opus implementation role is active again. `alaa-implementer-fable` is a separate exceptional route for difficult unresolved implementation judgment; the archived Opus-named file is historical only. No installation, commit, publication, live model run, account/access check, benchmark, or deployment occurred.

## Completion states

- `IMPLEMENTED`: PASS; source changes and the required local checks are recorded.
- `MERGE_CANDIDATE`: PASS; the reviewed, frozen candidate is verified locally. No merge was requested.
- `RELEASE_CANDIDATE`: NOT REQUESTED.
- `PUBLISHED`: NOT REQUESTED.

The release review is `READY-WITH-CONDITIONS`: any future authorized activation must verify provider mapping, version, overrides, availability, and loaded roles. Review decisions are recorded in the [independent review](review.md). See also the [implementation record](implementation.md), [final nine-check summary](verification/final-summary.json), [historical Phase 3 summary](verification/sonnet-summary.json), [plan](docs/_agent_plans/20261008-140000_haiku55-routing.md), and [checkpoint](docs/agents/20261008-140000_haiku55-routing-state.md).

## Reusable context

The verification-consolidation rule is now in its canonical paired gate policy, and source capability facts are in the prompting guide. No additional reusable-memory candidate was admitted; no memory write was requested or made.
