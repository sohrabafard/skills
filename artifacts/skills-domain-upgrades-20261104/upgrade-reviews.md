# Independent upgrade reviews

Review date: 2026-11-04. Candidate: `044d04c1` (base `4f60ce6f`).
These observations concern source delivery, not installed activation or WA acceptance.

All observers used separate read-only mandates in a workspace-write sandbox.
Each requested `gpt-6.1-sol/medium`; serving identity and enforcement are unknown.

## First review round

| Observer | Verdict | Findings |
| --- | --- | --- |
| `upgrade_review`, correctness and domain | CHANGES-REQUESTED | CH: dual-hash migration needs elapsed replicated window and nonreplicated insert-count window; dedup defaults began in 26.2, async default in 26.3; atomic POPULATE requires its effective setting and excludes Replicated databases; batch timeout is not a rate cap. Vector: same-basename staging overwrites an input; absent common VRL silently skips promised coverage; general plain MergeTree duplicate claim needs configuration qualification. |
| `upgrade_instruction`, instruction contract | CHANGES-REQUESTED | CH: pausing after live-view creation can duplicate backfill, including countState. Vector: trusted-config and approved-backend conditions must precede executable strict-validation examples; data_dir staging does not isolate secret resolution. |
| `upgrade_security`, security | PASS-WITH-HARDENING | Vector passes. CH low severity: IF NOT EXISTS can retain the wrong stored definer/security mode. Verify SHOW CREATE and grants after first application and reruns; migrate mismatches explicitly. |

The parent accepted the findings after source inspection. Repairs remain subject to
independent retesting and review; this record is not an acceptance verdict.

## Independent verification before repairs

Observer: `upgrade_verify`, role `alaa-verifier`. Verdict: PASS for declared checks.
Exact commands, exits and source manifests are in `upgrade-verification/`.
Six repository gates passed. Vector 0.61.0 passed two strict configurations,
five named transform cases and common VRL. ClickHouse template checks were lexical.
No current ClickHouse runtime, actual definer-grant, TLS, delivery, telemetry,
Helm or consumer rollout proof is implied.

## Source references used by reviewers

- [ClickHouse 2026 changelog](https://clickhouse.com/docs/resources/changelogs/oss/2026)
- [Deduplication default change, PR 95970](https://github.com/ClickHouse/ClickHouse/pull/95970)
- [Legacy hash removal, PR 108361](https://github.com/ClickHouse/ClickHouse/pull/108361)
- [ClickHouse view security](https://clickhouse.com/docs/reference/statements/create/view)
- [ClickHouse official packages](https://packages.clickhouse.com/)
- [Vector 0.61.0 release](https://vector.dev/releases/0.61.0/)

## Resume state

The first resume readback found expired leases with unchanged original assignees.
The user explicitly authorized those same actors to renew and continue.
No task was closed, no WA2 state changed, and Vector remains independent.

## Repair cycle 1 acceptance

Reviewed ClickHouse source: `e446fe18`. Reviewed Vector source: `efb08a44`.
The intervening `59361b45` services-contract commit is unrelated work.

- Correctness/domain observer: APPROVED both source deliveries, no remaining findings.
- Instruction observer: APPROVED Vector; APPROVED-WITH-NITS ClickHouse.
  The remaining nit suggests explicitly skipping already completed backfill ranges.
  The parent accepts it as nonblocking: required raw-count parity prevents declaring
  a duplicated backfill clean. Operators must still reconcile existing target data;
  no idempotent backfill or runtime cutover was proved by this delivery.
- Security's low-severity stored-definer concern is addressed by initial/rerun
  postcondition checks. Correctness and instruction reviews inspected the repair.
- Independent focused retests passed. Vector controls returned expected exits
  0 (bundled), 0 (valid only), 1 (malformed first same-basename input), and
  2 (missing common VRL with no adapter launch). Source hashes remained stable.
- All six final repository gates exited 0. Exact commands and bounds:
  `upgrade-verification/cycle1/final/commands.tsv`.

The evidence log's trailing blank line was mechanically trimmed after the Vector
checkpoint; the final diff gate includes that trim. No source behavior changed.
Latest ClickHouse runtime, Vector live delivery, installed activation, and WA2
acceptance remain outside these verdicts.

Both pre-existing Codex skill links resolve to the canonical directories under
`skills/sohrab/`. Source edits are therefore visible through those links. No installer
or global-link update ran, and no agent-runtime activation behavior was tested.
