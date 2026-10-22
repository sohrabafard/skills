---
name: gortex-guide
description: "Gortex reference: available tools, graph schema, and workflow."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Gortex Guide

Use this sequence for codebase work:

1. `explore({operation: "task", task: "<goal or bug>"})` — localize the task and obtain the working set.
2. `search({operation: "symbols", query: "<name>"})` or `search({operation: "text", query: "<literal>"})` — resolve a precise anchor.
3. `read({operation: "source", target: {symbol: "<id>"}})` — read only the source needed.
4. `relations({operation: "usages", target: {symbol: "<id>"}})` or `trace({operation: "call_chain", target: {symbol: "<id>"}})` — follow verified graph edges.
5. `change({operation: "impact", source: {symbols: ["<id>"]}})` — assess a planned change.
6. Apply with `edit` or `refactor`, then run `change` operations `detect`, `guards`, and `tests`.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
