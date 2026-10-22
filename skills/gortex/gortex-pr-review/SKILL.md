---
name: gortex-pr-review
description: "Graph-grounded review of a pending change or PR."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Review a Change with Gortex

1. Project the working tree with `change({operation: "detect", source: {scope: "unstaged"}})`; use `staged` or `compare` only when that is the requested review scope.
2. Build review context with `review({operation: "run", source: {scope: "<scope>"}})` and operation `diff_context` when per-file context is needed.
3. Require `change` operations `guards`, `tests`, and `contract`. When the proposed signature is known, run operation `verify` before mutation.
4. Check wire boundaries with `analyze({kind: "contracts", options: {action: "check"}})` when APIs or events changed.
5. Report only actionable findings with severity, `file:line`, evidence, consequence, and correction. State an explicit clean verdict when none remain.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
