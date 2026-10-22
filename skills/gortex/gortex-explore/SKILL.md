---
name: gortex-explore
description: "Understand how code works or trace an execution flow."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Explore a Codebase with Gortex

1. Call `explore({operation: "task", task: "<question>"})`.
2. Read only a returned anchor with `read({target: {symbol: "<id>"}})`.
3. Choose the needed relationship (`callers`, `usages`, or `dependencies`), for example `relations({operation: "callers", target: {symbol: "<id>"}})`; use `trace({operation: "call_chain", target: {symbol: "<id>"}})` for execution order.
4. Answer with the execution path, file locations, symbol IDs, and any graph uncertainty.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
