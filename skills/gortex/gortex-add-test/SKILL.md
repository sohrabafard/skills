---
name: gortex-add-test
description: "Add tests for under-tested code and coverage gaps."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Add Tests with Gortex

1. Localize the behavior with `explore`.
2. Confirm the specific gap with `change({operation: "tests", source: {symbols: ["<id>"]}})`. Use repository-wide `analyze({kind: "untested"})` or path-scoped `analyze({kind: "coverage_gaps", options: {path_prefix: "<path>"}})` only for broader coverage discovery.
3. Inspect callers with `relations({operation: "callers", target: {symbol: "<id>"}})` and request targets with `change({operation: "tests", source: {symbols: ["<id>"]}})`.
4. Add the narrowest test with `edit({operation: "file", target: {file: "<existing test path>"}, ...})`; use operation `write` for a new test file.
5. Run the test, then require `change` operations `detect` and `guards`.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
