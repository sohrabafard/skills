---
name: gortex-safe-edit
description: "Preview an edit's blast radius on the shadow graph before writing."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Make a Safe Edit with Gortex

1. Localize with `explore` and inspect `read({operation: "editing_context", target: {file: "<path>"}})`.
2. Run `change({operation: "impact", source: {symbols: ["<id>"]}})` before editing.
3. Choose `edit` operation `file`, `symbol`, or `batch`. Preview with `dry_run: true`; after review, repeat the same guarded request with `dry_run: false`. Use `change({operation: "simulate", source: {steps: "<WorkspaceEdit JSON array>"}})` for a multi-step semantic edit.
4. Run `change` operations `detect`, `tests`, `guards`, and `contract`. Signature verification belongs before mutation with the proposed signature.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
