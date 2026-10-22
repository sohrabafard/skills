---
name: gortex-cross-repo-usage
description: "Find who uses a symbol across all consumer repos."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Find Cross-Repository Usage with Gortex

1. Confirm tracked repositories with `workspace({operation: "repos"})`.
2. Resolve the provider symbol with `search({operation: "symbols", query: "<name>", options: {repo: "<provider>"}})`.
3. Call `relations({operation: "usages", target: {symbol: "<id>"}})` and group results by repository.
4. Add `analyze({kind: "cross_repo", options: {repo: "<provider>"}})` for repository boundaries and `analyze({kind: "contracts", options: {action: "bridge", mode: "impact", symbol: "<id>"}})` for wire-level consumers.
5. Report indexed coverage and name any untracked repositories as an explicit gap.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
