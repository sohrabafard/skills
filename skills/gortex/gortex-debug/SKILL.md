---
name: gortex-debug
description: "Debug a bug, trace an error, or find why something fails."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Debug with Gortex

1. Localize the exact symptom with `explore({operation: "task", task: "<error and observed behavior>"})`.
2. For a literal error, call `search({operation: "text", query: "<exact text>"})`. For a name, use operation `symbols`.
3. Walk toward the cause with `relations({operation: "callers", target: {symbol: "<id>"}})` and `trace({operation: "call_chain", target: {symbol: "<id>"}})`. Use `flow` or `taint` only after resolving both `target` and `to` endpoints.
4. Confirm repository-wide error propagation with `analyze({kind: "error_surface"})`; use `options.repo` to narrow a multi-repository workspace.
5. Before fixing, run `change({operation: "impact", source: {symbols: ["<id>"]}})`. After fixing, run `change` operations `detect`, `tests`, and `guards`.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
