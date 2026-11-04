# Final collected checker repair

Candidate base `8359b7b9`. The [six-file manifest](cycle2-source.sha256) covers four edited
files and two unchanged files. The Docker fixture and ref50 are byte-identical to the first
repair. No live rerun was needed. The prior independent merge and SIGTERM results cover the
unchanged runner. Cancellation during Docker creation and current 26.x runtime remain untested.

| Finding | Change and discriminating coverage |
| --- | --- |
| Quoted engine identity | Normalize bare and admitted ASCII-quoted names before deciding the engine. Unknown engine syntax refuses proof. Plain and replicated quoted aggregate engines require writers and both pass with complete proof. |
| Compound statements | Detect the unquoted `PARALLEL WITH` pair before DDL, writer or read classification. CREATE DATABASE followed by DROP and raw CREATE followed by aggregate CREATE both refuse proof. Comments containing those words stay inert. |
| Forwarded writes | Restrict nonaggregate tables in an aggregate bundle to local `MergeTree`. A Buffer declaration refuses proof even without an included insert. An actual insert through it also refuses. Raw-only named engines still receive the existing structural checks. |
| Unknown and implicit aliases | Check every explicit AS binding. Reject unknown quoting and escapes. Read projections admit atoms or one function call over atoms with an explicit output alias. Trailing clauses use a bounded grammar. Curly and escaped aliases, implicit projection aliases and nested or trailing implicit forms refuse proof. ASCII-quoted valid reads still pass. |
| Object namespace | Require unique, case-sensitive table and materialized-view names in the bundle. Include nonaggregate MVs and IF NOT EXISTS forms. Refuse mixed bare and qualified declarations that could refer to the same object. A dot inside one quoted identifier cannot stand for a qualifier. Distinct qualified names remain valid. |
| Documentation | Workload justification does not clear CH006. The documented narrow metadata-only ORDER BY exception leaves the primary key unchanged and cannot add WA's existing discriminator. |

Sources for the boundary decisions include [compound statements](https://clickhouse.com/docs/reference/statements/parallel_with),
[Buffer](https://clickhouse.com/docs/reference/engines/table-engines/special/buffer),
[24.8 identifier parsing](https://github.com/ClickHouse/ClickHouse/blob/v24.8.14.39-lts/src/Parsers/ExpressionElementParsers.cpp#L159),
[alias syntax](https://clickhouse.com/docs/reference/syntax) and [ALTER ORDER BY](https://clickhouse.com/docs/reference/statements/alter/order-by).

## Verification

All host checks used the skills root and one sequential Python 3.14.4 worker. The WA checker
ran from the read-only WA worktree. No runtime process, external system or WA file was mutated.

| Check | Exact command or evidence | Result |
| --- | --- | --- |
| Repair selectors | `python3 -B -m unittest discover -s skills/sohrab/clickhouse-performance-schema-ops/scripts -p test_review_clickhouse_ddl.py -k cycle2 -v` | Exit 0, six selected methods. [Output](cycle2-selectors.txt). |
| Bounded task suite | `python3 -B -m unittest discover -s skills/sohrab/clickhouse-performance-schema-ops/scripts -p test_review_clickhouse_ddl.py` | Exit 0, 23 methods. [Output](cycle2-unittest.txt). |
| CLI help | `python3 -B skills/sohrab/clickhouse-performance-schema-ops/scripts/review_clickhouse_ddl.py --help` | Exit 0. [Output](cycle2-help.txt). |
| Negative controls | Same isolated mutations and selectors as [initial author evidence](report.md). | Both expected exit 1, with actual checker exit 0 where 1 is required. [Index exemption](cycle2-control-blanket-exemption.txt), [omitted dimension](cycle2-control-missing-dimension.txt). |
| WA checkpoint | [No-install invocation](report.md#wa2-continuation-draft), [input hashes](cycle2-wa-identities.tsv), [audit](cycle2-wa-checker.txt). | Exit 2, 32 structural findings and four proof gaps. Byte comparison with the first repaired audit exited 0. [Per-finding disposition](wa-disposition.md). |
| Runtime source identity | Compare the fixture SHA256 with [first repair manifest](repair-source.sha256) and run `git diff --exit-code` for the fixture and ref50. | Both exit 0. Use the [first repair runtime evidence](repair-report.md) for these unchanged inputs. |
| Scoped whitespace | `git diff --check -- skills/sohrab/clickhouse-performance-schema-ops artifacts/skills-domain-upgrades-20261104/alaa-dgp8` | Exit 0. [Output](cycle2-scoped-diff.txt). |

The selector draft first exited 1 because a quoted engine test literal did not import.
The next selection exited 1 on an expected line-number mismatch for the Buffer diagnostic.
The qualification case then exposed a duplicate proof-gap diagnostic for one unsupported table
declaration. The checker now reports that refusal once. These distinct failures were corrected
before collecting the frozen results. See [import](cycle2-selectors-initial.txt),
[line assertion](cycle2-selectors-line-fix.txt) and [duplicate diagnostic](cycle2-selectors-qualification.txt).

The two WA inputs still match `cfa54adac0bea630beaa0ff2789ba772d016b37c` byte for byte, as
observed in WA worktree HEAD `3a86419f3244b6597b86ee24bf4781e3721d1d5d`. The prior WA2
continuation and recovery limits still apply. The parent owns independent retest, final
phase review, commit and issue closure.
