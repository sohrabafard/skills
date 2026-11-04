# ClickHouse skill source upgrade

## Scope and release evidence

On 2026-11-04 the [official packages page](https://packages.clickhouse.com/) reported patched
stable **26.10.3.7**, released 2026-10-25, and LTS **26.8.36.3**, released 2026-10-26, for
CVE-2026-116366. Its GitHub release listing lagged the package channels. Exact GitHub
release URLs with the channel suffix returned HTTP 404 and supplied no patch-level evidence.
The [2026 changelog](https://clickhouse.com/docs/resources/changelogs/oss/2026) provides
release-line changes. The advisory and channel indexes establish patch identity and date.
Patch-only changes beyond the advisory were not independently attributed.

Reproduce the channel check without retrieving a binary. Both index pipelines exited 0.

```bash
set -o pipefail
for channel in stable lts; do
    printf '%s ' "$channel"
    curl -fsSL "https://packages.clickhouse.com/deb/dists/$channel/main/binary-amd64/Packages.gz" |
        gzip -dc |
        awk '/^Package: / { server = ($2 == "clickhouse-server") } server && /^Version: / { print $2 }' |
        LC_ALL=C sort -V | tail -n 1
done
```

The previous source map dated its documentation to 2026-07-26 with no engine version.
The review covered the incompatible-change sections of 26.7, 26.8 LTS, 26.9 and 26.10
(12, 21, 17 and 37 entries in the fetched changelog, respectively), then the matching
features and fixes for skill surfaces. Fetch the Markdown at
https://clickhouse.com/docs/resources/changelogs/oss/2026.md and inspect each release's
Backward Incompatible Change, New Feature, and applicable bug-fix sections. 26.1, 26.2, 26.3 and
26.6 supply earlier deduplication context. The review window starts at the release
preceding the previous source snapshot. An actual upgrade starting on 24.8 needs its
own full upgrade path from the deployed patch and configuration.

## Delta triage

| Line | Relevant changes checked | Routing and limits |
| --- | --- | --- |
| 26.7 | [Aggregate-dimension DDL guard](https://github.com/ClickHouse/ClickHouse/pull/108087), [dedup hash transition](https://github.com/ClickHouse/ClickHouse/pull/108361), table-readonly/rotated-log downgrade, S3 user credential resolution, object-storage backup formats, timestamp range and time casts, removed snowflake conversions, remote metadata visibility, nested dynamic/variant minmax rejection, workload scheduling and CLI echo changes. | Ref20 keeps the guard enabled for new DDL. Ref90 captures startup and rollback risks. Recheck new time and storage behavior only when a pipeline uses those paths. |
| 26.8 LTS | [Atomic local MV population](https://github.com/ClickHouse/ClickHouse/pull/108715), [projection settings](https://github.com/ClickHouse/ClickHouse/pull/113343), [mutation completion metadata](https://github.com/ClickHouse/ClickHouse/pull/113474), [lightweight UPDATE v2 patch parts](https://github.com/ClickHouse/ClickHouse/pull/103182), format/header precedence, numeric JSON timestamps, insert thread defaults, account-expiry type, access-source restrictions, feature-tier change and host-metric maps. | Refs50/60/90 qualify supported paths. Keep v1 patch parts during a mixed pre-26.8 upgrade if using lightweight updates. Use column discovery before adding fields to operators' queries. |
| 26.9 | Removed legacy analyzer selection, CatBoost and WINDOW VIEW, size-aware MergeTree compression and ZSTD(3) network default, nullable tuple key/index/TTL startup hazards, enum log schema, disk and codec gates, [incremental refreshable MV](https://github.com/ClickHouse/ClickHouse/pull/114152), expiring credentials, [definer ALTER fix](https://github.com/ClickHouse/ClickHouse/pull/119357) and v1 patch-update fix. | Refs20/50/90 route the changes. No replacement auth surface selected. Qualify native codec performance and stored metadata at the real version. |
| 26.10 | SQL constraints and login, named collections, definer rewrite grants, secure view optimizer boundary, full removal of legacy analyzer in mixed clusters, [zero-sum FINAL](https://github.com/ClickHouse/ClickHouse/pull/115032), [TTL recalculation](https://github.com/ClickHouse/ClickHouse/pull/117310), [mutation validation](https://github.com/ClickHouse/ClickHouse/pull/121419), null and array semantics, skip-index correctness for merging engines, split join thresholds, seccomp and system-log layout. | Refs20/40/50/60/85/90 route affected claims. No new join, TTL, projection, setting or migration is selected for WA. Review applicability to the actual deployment before an upgrade. |

Other changelog entries concern unselected storage, table functions, data formats, SQL
features, performance work or build targets. They do not change this skill's shipped
examples. The full notes still govern any deployment using those features.

## Compatibility and handoff

The recorded WA2 fixture is 24.8.14.39 with image digest
`sha256:1ffa82edee000a42c09313bd9f1293d94c570aee74babc1b3ca9983a35fa597b`. Its handoff is
Beads alaa-9bbj.2 at checkpoint `cfa54adac0bea630beaa0ff2789ba772d016b37c`.
The [24.8 client source](https://github.com/ClickHouse/ClickHouse/blob/v24.8.14.39-lts/programs/client/Client.cpp#L279-L285)
confirms that CLICKHOUSE_PASSWORD is a fallback when no password is already configured.
The current [native client reference](https://clickhouse.com/docs/concepts/features/interfaces/client)
also documents that explicit arguments and connection strings take precedence.
Actual accepted credentials, listener/TLS and authorization require target evidence.

The checker lane alaa-dgp8 owns merge-key analysis and its proof. New server DDL
rejection and legacy data-loss behavior are separate oracles. Review the current ref20
allowlist exception there. Enum membership or unknown-value folding alone does not prove
a functional dependency from content ID to object type. Preserve older-engine checks and
never use the current setting escape to bypass a real omitted dimension.

The changed templates introduce an explicit MV definer. On any deployment, prove the
migration identity can bind it, the source writer triggers it, and the writer is denied
direct target writes. Scope grants to each identity. This is source guidance and no
installed copy, running service, WA pin, rollout, or EO-59 decision changed.

## Verification

Commands ran from the repository root, with a single host process per gate and no
container or elevated access. The release index pipelines above ran sequentially.

- `python3 -B scripts/check_fleet_references.py --skill clickhouse-performance-schema-ops`
  exited 0, with 76 citations and three pre-existing informational target paths.
- `git diff --check -- skills/sohrab/clickhouse-performance-schema-ops artifacts/skills-domain-upgrades-20261104/alaa-te30`
  exited 0. Git emitted its configured LF-to-CRLF notices.
- `python3 -B skills/sohrab/clickhouse-performance-schema-ops/scripts/review_clickhouse_ddl.py "$tmp/merge_tree_template.sql" "$tmp/materialized_view_template.sql"`
  exited 0, with two tables and zero findings. In temporary copies, replace
  `<tenant_column>` with `project_id` and unwrap the other angle-bracket identifiers.
  The lexical checker inspects CREATE TABLE. It does not execute DDL, parse MV security
  semantics, or validate diagnostic SQL.

Independent review and pack-wide checks belong to the parent. A current-version
behavioral fixture was not run. No server, container, network or volume was created.
When authorized and available, use a disposable instance with an immutable package or
image and synthetic data. Record both client and server versions and artifact digests.
Prove MV grants and wrong-password denial, duplicate replay and partial-view recovery,
mutation completion, the 26.7+ aggregate guard, and the 26.10 zero-sum FINAL transition.
Run any older-engine case separately and record cleanup. The source upgrade does not
serve as runtime acceptance for those behaviors.

## Review repair cycle 1

Repaired the independent findings against checkpoint `044d04c1`. The current source
requires draining writers before live MV creation and holding the pause through backfill
parity, or proving complementary live/history ranges for online work. Its parity includes
the raw count state as well as unique count. Stored MV security and effective grants are
checked on initial apply and reruns. Atomic population remains gated by effective settings,
source snapshots and topology. The 26.7 hash bridge specifies both elapsed time and insert
count. The release ledger separates 26.2 dedup defaults from 26.3 async inserts. The ingest
guidance routes acknowledgement behavior to the Vector owner and requires peak-rate
measurement rather than inferring capacity or source responses from batch configuration.

The focused reference checker, scoped whitespace check and two-table rendered lexical DDL
check described above were rerun on the repaired files and exited 0. These checks do not
exercise MV cutover, grants, delivery, or the dedup bridge against a running server.
