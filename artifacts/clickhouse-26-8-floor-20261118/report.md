# ClickHouse skill: rewrite and prune on the 26.8 LTS floor

Date: 2026-11-18. Task: `alaa-nxn10`. Skill: `skills/sohrab/clickhouse-performance-schema-ops`.

## Outcome

The skill now targets one release floor, ClickHouse 26.8.39.19 (26.8 LTS), set by the owner on
2026-11-18. It gained two capabilities and lost every rule that served an older server or recorded
the state of one repository at one commit.

| Measure | Before | After |
| --- | --- | --- |
| `SKILL.md` plus `references/`, source words | 14,956 | 13306 |
| reference files | 12 | 13 |
| scripts | 3 | 2 |

New capabilities, which are the reason two files and the body grew:

1. **Topology.** `references/25-topology-and-replication.md`: single node, replicas with Keeper,
   copies without Keeper, one DDL file for both declared modes, quorum and consistency decisions.
2. **Client lanes.** `references/85-access-and-configuration.md` now covers the Vector sink, the Go
   `chkit` lane and a PHP read lane over HTTP.
3. **Defaults at the floor.** `references/90-source-map.md` holds one table of defaults read from
   the floor binary, which replaces per-file version history.

## Evidence used

- Floor binary: image `clickhouse/clickhouse-server:26.8.39-alpine`, digest
  `sha256:96e3f95c3110fd50626c3f45e060aa4ad5ca0f1169cd00c89d6aaf5a946c85f9`. `clickhouse local`
  reported version 26.8.39.19. Defaults, setting descriptions, engine lists and system-table columns
  were read from it on 2026-11-18.
- Official pages read on 2026-11-18: replication, Keeper, `Distributed`, `Replicated` database,
  HTTP interface, permissions for queries, insert deduplication on retries, third-party client
  libraries, and the packages index (LTS head 26.8.39.19, stable head 26.10.5.57).
- Repositories read on 2026-11-18: `alaa-go-chi` at `6abc1d4` (`chkit`, `configkit`), `wa` at
  `953dc32` (image pins, sink batch values, decision sections 1, 3, 5, 10, 15.1, 29, 30 and 31),
  `deploy` (image pins only).
- Prompting sources: `alaa-prompting-guide references/60-skill-authoring.md` in full; the GPT-6 and
  Fable 5.2 references were searched for rules on skill text, not read in full.

Not verified: no ClickHouse server was started, no replica pair was built, asynchronous-insert
deduplication on a plain `MergeTree` table was not observed, and no agent run was observed with the
new text. The four repository checkers are static checks.

## Stale facts corrected

The previous skill text was measured at `wa` commit `5bbe3c2`. `wa` has since changed these, and the
skill now follows the current text:

| Fact | Previous skill text | `wa` at `953dc32` |
| --- | --- | --- |
| `DECISIONS.md` section 29 | counts and sums from `wa_raw` are billed and must be exact | superseded on 2026-11-03: ingest is best-effort telemetry, numbers are approximate and excluded from billing and settlement |
| `DECISIONS.md` section 30, reason | a commercial record that a settlement needs | historical heatmaps and growth rates need the history |
| database reset | scoped to local use by section 15.1 | section 31 adds an environment gate and an interactive confirmation; no agent can run it |

## Pruned-rule ledger

Each row is a deliberate removal. Restore a row from Git history of the named file when its reason
stops holding.

| # | Removed | Was in | Reason |
| --- | --- | --- | --- |
| P1 | Compatibility with ClickHouse 24.8: the "WA2 compatibility" paragraph, the 24.8 proof instruction for the aggregate guard, "do not inherit those defaults on 24.8", and the "Version scope" fixture statement | `90`, `20` section 6, `30`, `80` | Owner decision 2026-11-18: no server below the floor is supported |
| P2 | `scripts/test_aggregate_merge_semantics.py`, a Docker fixture pinned to 24.8.14.39 | `scripts/` | Below the floor, and the floor rejects the tested mistake at `CREATE`. Moved to `_to_delete/20261118-clickhouse-26-8-floor/` |
| P3 | Upgrade checks for the 26.7 and 26.8 lines, and the dual-hash bridge with `insert_deduplication_version=compatible_double_hashes` | `90` | Every server starts at the floor; the WA database is rebuilt empty. Restore if a populated server below 26.7 must ever be upgraded in place |
| P4 | Six "reported, not fixed" findings about `wa` at commit `5bbe3c2`, and "The worked instance" section | `20` sections 2 and 3, `40`, `30`, `15` | Instance state at a stale commit; `wa` is rebuilt on the floor. The rules stay. The findings are in "Handoff to `wa`" below |
| P5 | File and line citations into `wa` and `alaa-go-chi`, replaced by file paths | all references | The lines had already moved: the `readonly` pin was cited at `chkit/config.go:128-132` and is at line 139; the lane keys were cited at `configkit/keys.go:51-55` and are at lines 120-124 |
| P6 | The six-step description of the `wa` Vector topology | `30` | Duplicate of `vector-rust-observability-pipelines references/75-ala-ingest-pipeline.md`, which owns it |
| P7 | "Where the evidence is" system-table list, "Sharp edges that recur", "Using community sources" | `60` | The list is model default knowledge and is in the diagnostic template; each sharp edge duplicated a rule in `20`, `30`, `50` or `80`; the community-source rule lives in `90` |
| P8 | "Use the narrowest numeric type" with its example | `20` section 2 | Default model behaviour |
| P9 | Long verbatim quotations from official pages where the rule and a source row carry the same decision | `20`, `50`, `60` | Duplicate of `90`; thresholds and the load-bearing quotations stay |
| P10 | Release history of insert deduplication across 26.1, 26.2 and 26.3 | `30` | Replaced by the defaults at the floor |
| P11 | The "Unverified" note on the defaults of `max_execution_time`, `max_result_rows` and both overflow modes | `90` | Resolved from the floor binary: `0`, `0`, `throw`, `throw` |
| P12 | Pointer to the runtime orchestrators for multi-agent plans, and the file path after the model-and-effort pointer | `SKILL.md` | Not a ClickHouse decision; the global routing rule owns it. The pointer to `/alaa-prompting-guide` stays |
| P15 | Source links to the 24.8 native-client source file and to the deduplication-hash migration pull request | `90` | They served P1 and P3 only |
| P16 | "Its owner assigned that to the reliability owner" as a statement about backup | `10` | Reworded to what the decision log says today |
| P13 | The Redis comparison in readiness severity, the `docs/CONSUMERS.md` quotations, the `DECISIONS.md` section 1 quotation | `70`, `80`, `50` | Narration; the rule and the source path stay |
| P14 | Second call form `($name)` beside each `/name` | all files | `skills/sohrab/AGENTS.md`: one call form, converted in a file edited for another reason |

## Behaviour changes and additions

| # | Change | Where | Note |
| --- | --- | --- | --- |
| A1 | Version floor: no compatibility branch; a pin below the floor is a defect to report | `SKILL.md`, `90` | Owner decision |
| A2 | Name the declared topology mode before choosing an engine | `SKILL.md` rule 2 | Source: `alaa-services-contract references/15-deployment-and-runtime-contract.md` |
| A3 | Replicated tables: `ENGINE = ReplicatedMergeTree` with no arguments under the server default path, in place of a hand-written Keeper path | `25`, `assets/templates/merge_tree_template.sql` | Defaults read from the floor binary |
| A4 | A two-replica design needs a third Keeper voter; Keeper is a write dependency only | `25` | Quorum arithmetic is stated without an official page; marked in `90` |
| A5 | Insert quorum and sequential reads are owner-ratified decisions; no quorum is proposed for `wa` unless its owner asks | `25` | New |
| A6 | Copies without Keeper: named primary, rebuild after an outage, reproducible numbers from the primary only | `25` | New |
| A7 | A service-side `INSERT` is a new ingest path that needs the table owner's ratification | `30` | New policy; see "Owner decisions" |
| A8 | Async inserts are on by default at the floor; the second remedy is reworded | `30` | Floor binary |
| A9 | Size the deduplication window over the writer's whole retry horizon, buffered replay included; the table owner ratifies the window; check that the writer's insert mode uses it | `30`, `25` | New sizing rule. The synchronous case was observed on the floor binary; the asynchronous case is unverified |
| A10 | A change to an existing table reaches a deployment only through drop and recreate. Local instance freely; a shared environment only with the table owner's explicit approval; on `wa` only through the gated, interactive `--re-init` | `10` | Positive form of the `IF NOT EXISTS` trap, with its authority limit |
| A17 | WA numbers are approximate and never presented as exact | `15` | Follows current `DECISIONS.md` section 29 |
| A11 | Change a nullable dimension in the table and in the transform together | `20` section 2 | Derived from the removed `wa` finding |
| A12 | "Never enable `allow_dimensions_outside_sorting_key` to make a `CREATE` pass" | `20` section 6 | Stronger wording of "keep the guard enabled for new designs" |
| A13 | PHP read lane: server-side profile and grant, bound parameters, header credentials, HTTP 200 is not success, no `session_id`, no client retry | `85` | New; ClickHouse maintains no PHP client |
| A14 | Proof rows for a deduplication window or quorum and for a move to `Replicated*`; a rollback row for that move | `80` | New |
| A15 | Templates: mode-aware engine comment, a deduplication-window setting in place of the default `index_granularity`, `finish_time` in the mutation query, a replica query | `assets/templates/` | Column names confirmed on the floor binary |
| A16 | "Single node today, cluster later" moved from `10` to `25` and rewritten | `10`, `25` | Relocation with its own reason: topology is one topic |

## Owner decisions still open

1. **A7.** Confirm that a Go or PHP service must post events to the pipeline source and may not
   `INSERT` directly without ratification.
2. **PHP lane.** Choose the PHP client library, and register the lane's environment keys in
   `alaa-services-contract`. The skill names neither.
3. **Deduplication on WA.** Decide whether the raw tables set a deduplication window on the
   rebuild. Section 29 accepts duplicates on ingest and leaves the table-side choice open.
4. **Checker tests.** `scripts/test_review_clickhouse_ddl.py` stays, because it tests checker code
   that did not change. Retire it if the skill-testing ban covers it.

## Handoff to `wa` for its rebuild on the floor

The removed findings, restated as work for the owning repository:

1. Move the image pin from 24.8 to the floor in `Dockerfile` and `.gitlab-ci.yml`. `deploy` pins
   24.8 too, in its development infrastructure Compose file and in `scripts/manual-release.sh`.
2. Add `object_type` to the merge key of the three content-grained rollups. At the floor the
   aggregate-dimension guard can reject those tables at `CREATE`.
3. Review the eighteen `Nullable` columns of the raw tables. Four are repeated low-cardinality
   dimensions (`device_os`, `device_browser`, `network_effective_type`, `session_locale`); the
   replacement is `LowCardinality(String) DEFAULT ''` with `?? ""` in the transform.
4. Shorten the nine-column sort keys of the raw tables, and serve identifier-first reads with a
   projection or a rollup.
5. Decide the deduplication window of the raw tables in `single-node` mode (owner decision 3). If
   it is set, prove it with the real sink, because async inserts are the default at the floor.
6. Confirm the effective `async_insert` and `wait_for_async_insert` of the sink identity; async
   inserts are on by default at the floor.
7. Add the tenant predicate and a time bound to `samples/verification_queries.sql` before anyone
   reuses a query from it.
8. Keep one DDL file that applies in both declared modes.

`wa` has added tables since `5bbe3c2`; items 2 to 4 were measured there and must be re-read against
the current DDL.

## Statements in other skills that the upgrade will make stale

Not edited, because their owning skill records the current `wa` deployment:
`vector-rust-observability-pipelines references/75-ala-ingest-pipeline.md` says "a single 24.8 node
with no Keeper" and carries a 24.8 comment in its re-measure commands. Update both when `wa` moves
to the floor.

## Gates

The four repository checkers ran from the repository root on 2026-11-18. The first run gave
validator exit 1 with four findings: two cross-skill paths split from their skill name by a line
wrap, the `short_description` length, and the description length. After one repair all four exited
0. They ran again on the final text of each commit:

| Command | Exit on the final text |
| --- | --- |
| `python3 scripts/validate_sohrab_skill_pack.py` | 0 |
| `python3 scripts/check_skill_index.py` | 0 |
| `python3 scripts/check_fleet_references.py` | 0 |
| `python3 scripts/check_lifecycle_contract.py` | 0 |

No independent subagent review and no skill self-test ran, by owner instruction. One advisor pass
read the session after the first commit; its findings are the second commit.

## Size

Source words in `SKILL.md` plus `references/`, counted with `wc -w`:

| File | Before | After |
| --- | --- | --- |
| `SKILL.md` | 762 | 869 |
| `00-topic-map.md` | 346 | 362 |
| `10-authority-and-change-path.md` | 1236 | 821 |
| `15-fleet-clickhouse-boundary.md` | 882 | 530 |
| `20-table-design.md` | 1945 | 1169 |
| `30-ingest-and-parts.md` | 1126 | 961 |
| `40-query-tuning-and-read-lane.md` | 828 | 519 |
| `50-mvs-projections-and-ttl.md` | 1340 | 961 |
| `60-operations-and-diagnostics.md` | 1124 | 662 |
| `70-failure-and-degradation.md` | 979 | 789 |
| `80-proof-and-validation.md` | 1915 | 1726 |
| `85-access-and-configuration.md` | 1108 | 1132 |
| `90-source-map.md` | 1365 | 1583 |
| `25-topology-and-replication.md` (new) | 0 | 1222 |
| **Total** | 14956 | 13306 |

The total fell by 11 percent with the new topology file included. The twelve files that existed before fell from 14956 to 12084 words, 19 percent.
