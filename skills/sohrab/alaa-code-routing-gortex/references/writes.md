# Guarded writes and mutation recovery

Contract inspected at Gortex v0.64.8 on 2026-10-22; recheck installed tool schemas before a write. Source: [MCP writes](https://github.com/zzet/gortex/blob/v0.64.8/docs/mcp.md), [security boundary](https://github.com/zzet/gortex/blob/v0.64.8/SECURITY.md).

1. Confirm user authorization, file ownership, real repository/worktree, requested and actual view, current capability and freshness. Exact native worktree views may be writable; fallback, commit and git-ref views are read-only. Never redirect a write to the main checkout to make it succeed.
2. Read the current target and obtain the exact guard the selected tool requires. Do not manufacture a guard from a similarly named response field.
3. Use the operation's supported preview/dry-run or refactor simulation; inspect the proposed scope and language support. Preview is not commit authority or physical-write proof. Coordinate overlapping work on the same file even when sessions share the daemon.
4. Submit the mutation with its supported guard and stable mutation_id or transaction_id. Retain identifiers and receipts before another operation.
5. Inspect scoped disk diff and native proof. Report graph freshness separately; successful disk writing does not mean enrichment caught up.

| Field | Meaning / permitted use |
|---|---|
| base_sha / new_sha | Git blob SHA-1 of full file bytes; new_sha may be a prediction, including dry-run |
| content_sha256 | SHA-256 of the complete disk file |
| before_sha256 / after_sha256 | Physical reread evidence with physical_evidence=true on supported tools |
| etag | Response representation hash; not a write guard |
| mutation_id | Single-file idempotency identity |
| transaction_id | Batch idempotency identity |

`physical_evidence` is supported on read_file/edit_file/write_file/edit_symbol in the inspected release and is incompatible with dry_run. An evidence_error is not proof the write failed. Batch journal digests are not physical disk rereads. Use expected/current fields exactly as the live schema specifies; never exchange Git blob SHA-1, SHA-256 and etag.

After a timeout or disconnected client, do not blindly resubmit with a new ID. Query mutation_status using the documented operation/receipt identifier and reconcile actual disk state. A request may still run after client timeout. Same ID plus the same edit can replay its receipt; reusing it for a different edit is rejected. Receipts are in-memory and retained for 30 minutes in the inspected release; process loss/expiry requires disk reconciliation, not an invented negative status.

Keep disk outcomes (committed/not_applied/failed/in_flight) separate from graph outcomes (fresh/pending/stale/failed). Use supported require_exact/require_fresh and an RFC3339 wait_deadline where available. Stop when destination, stale guard, operation support or mutation outcome cannot be established. A graph miss never authorizes deleting a symbol.

Refactor names do not establish cross-language support. Restrict each operation to the release's supported languages and the checkout's effective LSP capabilities; Vue readiness is owned by `vue.md`. Native tests, lint, types, builds and generated-artifact checks remain the final behavioral evidence.
