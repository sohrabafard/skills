---
name: gortex-quality-audit
description: "Repo-scale quality scan — dead code, hotspots, clones."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Audit Repository Quality with Gortex

1. Establish scope with `workspace({operation: "info"})` and `explore({operation: "outline"})`.
2. Run `analyze` for `health`, `dead_code`, `hotspots`, `cycles`, and `clones`.
3. Validate high-risk findings with `read` and `relations`; do not report an unverified heuristic as a fact.
4. Rank findings by evidence, impact, and remediation cost. Include exact paths, symbol IDs, and a smallest-first action plan.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
