# Modernization merge audit - 2026-09-30

When upgrading after the modernization merge, read this audit with the
[original upgrade archive](../20260929-modernization/README.md) for the integration correction.

The merge `841057985ee7ae8e40302b864ee1909e310f5be7` preserved the entire feature tree
from `82a66c98b`; its only additions were four files introduced by main-side commit
`6af1d7eb804083aa8faa8c1e92b6b58a1e616ac5`. Both parents descend from `0e9681c82`,
and their changed paths do not overlap.

Those four files duplicate canonical references and are absent from the skill manifest.
The IndexedDB pack validator reported exactly four unlisted-file findings before repair.
Their original bytes are retained under
[`_to_delete/20260930-idb-merge-duplicates/`](../../_to_delete/20260930-idb-merge-duplicates/).

All filenames below are relative to the skill's `references/80-testing-and-proof-levels/`.
For current instructions, follow the [canonical router](../../skills/sohrab/alaa-indexeddb-browser-storage/references/80-testing-and-proof-levels.md).

| Retired file | Canonical replacement |
|---|---|
| `10-proof-levels.md` | `10-required-scenarios.md` |
| `20-required-scenarios.md` | `20-quota-reproduction.md` |
| `30-quota-reproduction.md` | `30-debug-surfaces.md` |
| `40-debug-and-performance.md` | `40-performance-budgets.md` and `50-release-checklist.md` |

The replacements contain the same ordered text tokens, including every checklist item.
Retirement preserves the canonical source, router, examples and manifest unchanged.
[Validation evidence](validation.json) records the move hashes and observed gate results.
Historical candidate hashes are not a claim that the current tree equals that earlier snapshot.

Return to the [upgrade evidence index](../README.md).
