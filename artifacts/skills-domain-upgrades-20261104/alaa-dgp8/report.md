# Aggregate checker source delivery

The checker compares every admitted aggregate writer's stored grouping dimensions with the full
`ORDER BY`. It applies CH006 and CH007 to the explicit sparse index or the full implicit index.
CH010 reports an omitted merge dimension. CH011 identifies unavailable proof and takes exit
precedence over findings. A qualifying shorter prefix still has to pass the existing index guards.
Raw key obligations remain unchanged. No engine or table is exempted from its applicable checks.

## Candidate and evidence

The parent checkpointed the frozen source at `0ee59aa0` on base
`9433e292db9f995a149439e7d2cd6d4b6a758e3f`. See [source SHA256](source.sha256).
The checker accepts one complete DDL/writer bundle and repeatable actual read-query paths. Its
lexical subset cannot establish bundle completeness, query execution, deployed binding or pruning.
There is no dependency addition, workload simulation, enum exception or runtime mutation of WA.

| Check | Command or evidence | Exit and interpretation |
| --- | --- | --- |
| Original defect | [Baseline invocation and input hashes](baseline.json), [original output](baseline-checker.txt) | 1, 29 findings. Aggregate width/tail obligations incorrectly treated merge identity as a raw sort key. |
| CLI regression | `python3 -B -m unittest discover -s skills/sohrab/clickhouse-performance-schema-ops/scripts -p test_review_clickhouse_ddl.py -v` | 0, ten tests in [focused output](focused-unittest.txt). |
| CLI help | `python3 -B skills/sohrab/clickhouse-performance-schema-ops/scripts/review_clickhouse_ddl.py --help` | 0, [exit and proof contract](checker-help.txt). |
| Scratch negative controls | Copy checker and unittest file to a fresh scratch directory per control. Run `python3 -B -m unittest discover -s "$scratch" -p test_review_clickhouse_ddl.py -k "$selector"`. | Expected exit 1 for each selected test. See [index exemption](control-blanket-exemption.txt) and [missing dimension](control-missing-dimension.txt). |
| Physical merge proof | `timeout 180s python3 -B skills/sohrab/clickhouse-performance-schema-ops/scripts/test_aggregate_merge_semantics.py --image sha256:1ffa82edee000a42c09313bd9f1293d94c570aee74babc1b3ca9983a35fa597b` | 0, [fixture evidence](merge-runtime.txt). |
| WA checkpoint | No-install invocation below. [Input identity](wa-input-identities.tsv), [checker output](wa-checker.txt), [each original finding and new diagnostics](wa-disposition.md). | Expected exit 2, 32 findings and two proof gaps. |
| Scoped whitespace | `git diff --check -- skills/sohrab/clickhouse-performance-schema-ops artifacts/skills-domain-upgrades-20261104/alaa-dgp8` | 0, [evidence](scoped-diff-check.txt). |

Commands used Python 3.14.4 and one sequential host worker from the skills root. WA audit ran from
the read-only WA worktree. The runtime capacity check found 32 logical CPUs with full affinity,
uncapped CPU and memory cgroups and 9,568 MiB available RAM. Local Docker reported Linux, 32 CPUs
and 46,283,280,384 bytes RAM. The disposable instance used 4 CPUs, 2 GiB RAM, zero additional swap,
a bounded data tmpfs, no published ports, no host binds and network mode none. Startup polling had
a 120-second readiness deadline within the 180-second command envelope. The image was already
cached and started with `--pull never`. Client and server reported 24.8.14.39.

The first fixture run returned 1 because default `optimize_on_insert` aggregated broken rows
within each batch before the physical merge test. [Initial output](merge-runtime-initial.txt).
The retry explicitly disabled insert-time aggregation in both fixtures. Each had two active parts,
four physical rows and grouped totals A=5/B=18 before merge. `OPTIMIZE FINAL` left one active part
in each. The good fixture kept two rows with A=5/B=18. The broken fixture held one row totaling 23.
No survivor label was asserted. The fixture container and its writable state were removed on both
runs. This proves the tested 24.8 physical merge behavior. Source qualification for the 26.7+
server guard follows the [upstream change](https://github.com/ClickHouse/ClickHouse/pull/108087)
and the [accepted release ledger](../alaa-te30/report.md). Current 26.x runtime was unrun.

The index mutant guarded both width and tail checks with `not is_aggregate`. Selector
`aggregate_effective_index_implicit_and_long_explicit` failed both subcases with actual exit 0
where exit 1 was required. The identity mutant assigned `missing = set()` in `check_aggregate`.
Selector `aggregate_missing_dimension_with_qualifying_prefix` failed with actual exit 0 where exit
1 was required. Both copies were isolated and cleaned. The source candidate never contained a mutant.

Not written: a second parser-only suite would duplicate the CLI decision assertions. A replicated
runtime merge fixture would require Keeper and prove topology behavior outside this task. Running
the actual WA DDL or querying WA data would cross the read-only boundary. The independent code,
instruction/domain and verification gates belong to the phase owner. Local commit and issue closure
are pending those gates. The phase boundary and final Phase 7 remain inherited.

Round 1 changed the admitted SQL grammar and the fixture cleanup. See
[first repair verification](repair-report.md) and [final repair verification](cycle2-report.md)
for the frozen inputs and exact evidence.

## WA2 continuation draft

Use the accepted checker from the skills source checkout. From the intended WA checkout run:

```bash
python3 -B "${SKILLS_CHECKOUT:?set the skills source checkout}/skills/sohrab/clickhouse-performance-schema-ops/scripts/review_clickhouse_ddl.py" \
  clickhouse/ddl/001_init.sql clickhouse/ddl/002_agg.sql
```

The two inputs at audited WA HEAD `3a86419f3244b6597b86ee24bf4781e3721d1d5d` were byte-identical
to checkpoint `cfa54adac0bea630beaa0ff2789ba772d016b37c`. This validates only those input files.
Reconcile the current WA integration HEAD and issue ownership before editing.

Expected audit exit is 2. Eighteen Nullable findings and four raw key findings remain WA-owned.
Seven aggregate width/tail findings apply to the full implicit sparse indexes. Justify any proposed
shorter explicit prefix with actual target SQL via `--read-query FILE`. Verify pruning on the
target runtime. Preserve the complete merge identity in `ORDER BY`.

Add the independent `object_type` dimension to the three affected content rollup merge identities
under the WA schema owner. Resolve both computed `event_date` bindings and both additive source
ALTERs against the effective source schemas and settings. Include all real writers and rebuilds.
Keep the source ALTERs in the reviewed evidence. They are unsupported proof forms in this checker.

Select a rebuild or replacement with the schema owner. Metadata-only `MODIFY ORDER BY` cannot add
the existing `object_type` column or change the primary key. Recompute from trustworthy
pre-aggregation history with proven range coverage. Compare measures by tenant, date, ID and
`object_type` against source-grain results. Missing coverage or any discrepancy blocks cutover.
Apply the approved writer pause and drain or prove a disjoint live boundary. Define rollback
limits before switching readers. Neither upgrading nor switching back recreates lost history.
Verify the effective dimension guard, including compatibility settings, on the target.

Keep the consumer's phase review boundary and final Phase 7. The checker delivery does not accept
WA2, resolve EO-59 or authorize a rollout.
