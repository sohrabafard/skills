# Round 1 aggregate checker repair

The six-file repair is frozen over checkpoint `0ee59aa0`. See [source hashes](repair-source.sha256).
This is author evidence for the collected independent findings in [checker reviews](../checker-reviews.md).
The checker's proof scope remains the supplied SQL. Unsupported SQL in that bundle now blocks a
clean aggregate result.

| Finding | Repair and direct proof |
| --- | --- |
| Phantom MV and hidden INSERT | Shared nested block and `//` comment scanning preserves statement boundaries. A nested-comment MV cannot supply writer proof. A `//` comment cannot swallow the following direct write. |
| Global alias shadowing | Check aliases throughout the read SELECT, including nested expressions and ORDER BY. A possible target-column alias blocks prefix proof. |
| Stale writer or source schema | Aggregate proof admits a bounded set of statements. ALTER, DROP and other mutations receive CH011 even when the object is a writer or its source. |
| Skipped alternate writer or indirect write | Refuse unadmitted CREATE DEFINER form, table-function INSERT, prefixed INSERT and DETACH. Keep simple inserts into declared raw tables. |
| Leading BOM and zero tables | Decode UTF-8 with optional initial BOM. Require at least one checked table declaration. |
| Skipped quoted column | Return CH011 for a column outside the admitted identifier grammar. Keep CH005 and other structural findings for parsed columns. |
| Fixture cancellation | Announce and label the exact disposable container before launch. Catch SIGTERM and remove that named and labeled fixture within the reserved deadline. |
| Instruction and migration | Scope width and tail to raw ORDER BY or the effective aggregate sparse index. Preserve all merge dimensions. Document bare parameter types, effective guard compatibility and trustworthy historical recovery. |

The lexer and global alias changes follow the [24.8 lexer](https://github.com/ClickHouse/ClickHouse/blob/v24.8.14.39-lts/src/Parsers/Lexer.cpp#L310)
and [ClickHouse alias semantics](https://clickhouse.com/docs/reference/syntax).
The rebuild constraints follow [ALTER ORDER BY](https://clickhouse.com/docs/reference/statements/alter/order-by)
and the [26.7 guard implementation](https://github.com/ClickHouse/ClickHouse/pull/108087).

## Commands and outcomes

Use the skills root for host commands. The WA audit uses the read-only WA worktree. Python
3.14.4, one sequential host worker, Docker Linux 32 CPUs, no effective host CPU/memory cgroup cap,
and 11,486 MiB available RAM at preflight. Runtime runs were sequential on the same cached 24.8
digest and 4 CPU / 2 GiB / network-none boundary.

| Check | Exact command or reference | Result |
| --- | --- | --- |
| Repair selectors | `python3 -B -m unittest discover -s skills/sohrab/clickhouse-performance-schema-ops/scripts -p test_review_clickhouse_ddl.py -k repair -v` | Exit 0, seven selected methods. [Output](repair-selectors.txt). |
| Task CLI suite | `python3 -B -m unittest discover -s skills/sohrab/clickhouse-performance-schema-ops/scripts -p test_review_clickhouse_ddl.py` | Exit 0, 17 methods. [Output](repair-unittest.txt). |
| Help | `python3 -B skills/sohrab/clickhouse-performance-schema-ops/scripts/review_clickhouse_ddl.py --help` | Exit 0. [Output](repair-help.txt). |
| Negative controls | Same isolated mutation and selector commands as [round 1 evidence](report.md). | Both expected exit 1. [Index exemption](repair-control-blanket-exemption.txt) and [omitted dimension](repair-control-missing-dimension.txt). |
| Runtime merge | `timeout 180s python3 -B skills/sohrab/clickhouse-performance-schema-ops/scripts/test_aggregate_merge_semantics.py --image sha256:1ffa82edee000a42c09313bd9f1293d94c570aee74babc1b3ca9983a35fa597b` | Exit 0, physical merge reproduced and exact fixture cleaned. [Output](merge-runtime-repair.txt). |
| Runtime SIGTERM | `timeout 180s python3 -B artifacts/skills-domain-upgrades-20261104/alaa-dgp8/probe-cancellation.py skills/sohrab/clickhouse-performance-schema-ops/scripts/test_aggregate_merge_semantics.py sha256:1ffa82edee000a42c09313bd9f1293d94c570aee74babc1b3ca9983a35fa597b` | Probe exit 0, runner exit 143, exact fixture absent after cancellation. [Output](merge-cancellation.txt). |
| WA audit | Same no-install command in [WA continuation](report.md#wa2-continuation-draft). | Exit 2, 32 structural findings and four proof gaps. [Hashes](repair-wa-identities.tsv), [output](repair-wa-checker.txt), [dispositions](wa-disposition.md). |
| Scoped whitespace | `git diff --check -- skills/sohrab/clickhouse-performance-schema-ops artifacts/skills-domain-upgrades-20261104/alaa-dgp8` | Exit 0. [Output](repair-scoped-diff.txt). |

The initial byte comparison of repaired and pre-repair WA output returned 1. The repaired audit
adds two CH011 lines for actual additive source-table ALTERs. The second comparison asserted both
expected lines and exact equality of the remaining output. It exited 0. The input hashes still
match checkpoint `cfa54adac0bea630beaa0ff2789ba772d016b37c`. Checkout HEAD
`3a86419f3244b6597b86ee24bf4781e3721d1d5d` identifies where those bytes were observed. The two
new proof gaps require review of effective source schemas and mutations. Neither gap proves a
schema defect or permits dropping the ALTERs from the evidence.

The fixture allows 120 seconds for readiness and 150 seconds for work. Cleanup reserves at most
18 seconds inside the 180-second wrapper. Both normal and cancelled runs used the cached digest,
no pull, no ports, no host binds, no shared data and no network. If the process is killed without
a catchable signal, use the exact `fixture container:` name from its output. Verify its
`alaa.fixture.aggregate-merge` label value equals that exact name on the same local Docker engine.
Remove only that verified fixture with `docker rm --force --volumes "$fixture_name"`, then verify
the exact name and label return no container. The SIGTERM test exercised the live cleanup path.
Uncatchable termination and current 26.x runtime were not exercised.

The parent owns independent retest, phase review, commit and issue closure. There is no WA or
deployment mutation, external sync, package installation or WA2 acceptance.
