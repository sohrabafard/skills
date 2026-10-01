# HAProxy 3.4.6 skill package archive

This archive contains the scope, source evidence, review rationale, and verification records for the HAProxy and Lua skill package update. The [final verification report](./verification/final-report.md) owns final verdicts, status, command results, snapshot identity, and proof limits.

## Read order

1. Read the [final verification report](./verification/final-report.md) for the authoritative outcome and observed gates.
2. Read the [workflow plan](./20261001-120000_haproxy-346.md) and [checkpoint](../../docs/agents/20261001-120000_haproxy-346-state.md) for the task scope, acceptance criteria, and phase history.
3. Read [review evidence](./review-evidence.md) for reviewer findings and their rationale.
4. Read [build evidence](./build-evidence.md), the [source manifest](./source-manifest.json), and both package [source registers](../../skills/sohrab/alaa-haproxy/references/SOURCES.md) and [Lua source register](../../skills/sohrab/alaa-haproxy-lua/references/SOURCES.md) for versioned claims and their sources.
5. Read the [gateway reference](./gateway-reference.md) for the bounded, read-only integration inspection and its snapshot limits.

## Scope and proof limits

The package change covers HAProxy 3.4.6 guidance and the corresponding Lua references, examples, and checkers. This archive records no gateway edits. Gateway observations are tied to the captured intake snapshot; a later read observed concurrent edits in other gateway areas. The intake byte comparison therefore does not describe the complete current gateway tree.

Package checks and cached-image inspection do not establish gateway image construction, consumer compatibility, reload or drain behavior, rollout, rollback, or deployment. Use the final verification report for the observed scope and outcome; do not infer a broader release or deployment result from the archived focused checks.
