---
name: gortex-dataflow-trace
description: "Trace where a value flows through the code."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Trace Data Flow with Gortex

1. Call `explore({operation: "task", task: "trace <value> from <source> to <sink>"})`.
2. Resolve endpoints with `search({operation: "symbols", query: "<source or sink>"})`.
3. Use `trace({operation: "flow", target: {symbol: "<source-id>"}, to: {symbol: "<sink-id>"}})`. Use operation `taint` when source/sink security semantics matter.
4. Cross-check control flow with operation `call_chain` when the data-flow graph has a gap.
5. Report each hop with its symbol ID and confidence; distinguish no path from incomplete indexing.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
