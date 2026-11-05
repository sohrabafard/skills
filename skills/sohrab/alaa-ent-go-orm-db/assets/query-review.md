# Query and index decision record

Fill relevant sections with observed project facts.

## Workload

| Query ID and call site | Predicates and joins | Ordering and limit | Volume / selectivity / frequency | Evidence source |
| --- | --- | --- | --- | --- |
| Q1 | Actual SQL shape | Stable order | Unknown where unmeasured | SQL / trace / code path |

## Projection contract

| Query ID | Response / computation fields and reasons | Identity / tenant / cursor / association fields | Omitted wide or sensitive fields | Actual SQL checked? |
| --- | --- | --- | --- | --- |
| Q1 | Required columns | Internal dependencies | Intentional omissions | Observed / unavailable |

## Index decisions

| Index / invariant | Exact keys, directions, predicate and INCLUDE | Queries served and why | Existing overlap | Write / storage cost | Evidence status |
| --- | --- | --- | --- | --- | --- |
| I1 | Ent definition and reviewed SQL | Q IDs and access path | Keep / replace / no change | Measured or estimated | Proposed / plan-observed / measured |

## Validation and rollout

Record Go/Ent/PostgreSQL versions, dataset/parameter classes, plans, checks, and result-contract comparisons.
State transaction boundaries, lock/time budgets, authorized environment, and recovery procedure.
Separate measured improvement from expected improvement. List unrun checks and the next safe action.
