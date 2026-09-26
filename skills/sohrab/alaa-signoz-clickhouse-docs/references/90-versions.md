# Versions and Compatibility Evidence

Read before stating versions, selecting release-specific syntax/APIs or assessing upgrades.
This file owns version facts; topic references own query procedures.

## Snapshot: 2026-09-26

| Evidence level | Observed value | Official source |
|---|---|---|
| Latest stable SigNoz application | `v0.143.0`, released 2026-09-23 | [release](https://github.com/SigNoz/signoz/releases/tag/v0.143.0) |
| Released SigNoz Helm chart / appVersion | `0.143.0` / `v0.143.0` | [Chart.yaml](https://raw.githubusercontent.com/SigNoz/charts/signoz-0.143.0/charts/signoz/Chart.yaml) |
| Collector image in that chart | `v0.144.11` | [values.yaml](https://raw.githubusercontent.com/SigNoz/charts/signoz-0.143.0/charts/signoz/values.yaml) |
| ClickHouse server image in that chart | `25.12.5`; dependency chart version `24.1.18` is not the server version | same released chart and values |
| Upstream ClickHouse stable / LTS | `26.9.2.8` / `26.8.11.7`, package dates 2026-09-22 | [official packages](https://packages.clickhouse.com/) |
| Previous skill snapshot | application `v0.135.0`, collector `v0.144.6`, ClickHouse `25.12.5`, upstream `26.7`; recorded 2026-07-30 from then-current main | historical provenance, not an installed pin |
| Local consumer application / collector / ClickHouse / chart | `UNKNOWN`; no version-matched deployment evidence supplied, no live discovery authorized | none |
| Installed schema, API permissions and SQL alert acceptance | `UNVERIFIED`; alert record remains `unconfirmed` | `../assets/alert-surface.json` |
| Supported consumer range | no new minimum imposed; preserve existing paths and select by observed version/schema | vendor support window not established by these sources |

The cached GitHub `releases/latest` pages initially returned application/chart `0.142.1`.
Release listings, the newer tag, GitHub release API and tagged chart files agreed on the selection above. Do not resolve freshness by trusting one redirect.
Chart version, appVersion, collector and database image are independent facts even when numbers match.
Never upgrade a consumer merely to match this ledger.

## Release-qualified decisions

- **Application/collector coupling:** the [upgrade guide](https://signoz.io/docs/operate/migration/upgrade-0-143/)
  requires collector `v0.144.11` for application `v0.143.0`. If that cannot be supplied,
  the vendor says to remain on `v0.142.x`. Custom trace pipelines need both
  `signozspanmapper` and `signozllmpricing`; defining processors alone does not activate them.
  Route topology/redaction decisions to `/alaa-observability-soc`; this skill authorizes no upgrade.
- **Session migration:** that guide changes the default to opaque sessions and requires a new login.
  Retaining JWT requires explicit `SIGNOZ_TOKENIZER_PROVIDER=jwt` and
  `SIGNOZ_TOKENIZER_JWT_SECRET`; absent JWT secrets block startup. Never log or invent a secret,
  and do not infer that service-account API keys use the session token format.
- **AI attribute movement:** that guide moves legacy prompt/output fields to
  `gen_ai.input.messages`/`gen_ai.output.messages`. Reconcile saved queries across the cutover;
  historical spans can retain old keys. Do not duplicate sensitive message payloads merely to
  preserve a query. Back up the Metastore and inspect required upgrade stops in an authorized upgrade.
- **Field evolution:** Query Builder semantic-name resolution starts in the reviewed
  `v0.138.0` trace release; `v0.143.0` prefers resource context for ambiguous filter keys.
  Raw SQL does not inherit that resolver: confirm exact stored keys, context, type and populated
  columns. `query-language-routing.md` owns the disambiguation procedure.
- **Panels and APIs:** dashboard v1 editor/variable retirement lands in `v0.141.0`, backend removal
  in `v0.143.0`. Query-result shapes remain separate from dashboard JSON contracts; retain old
  consumer shapes for old installs and use a release-matched v2 schema for new automation.
  New heatmap/text/area capabilities do not make an existing timeseries SQL example their schema.
- **Alert history:** the [migration guide](https://signoz.io/docs/alerts-management/migrate-alert-history-api-v1-to-v2/)
  dates v2 availability to `v0.118.0`; `v0.135.1` moves the UI to v2. Yet
  [RegisterRoutes at v0.143.0](https://raw.githubusercontent.com/SigNoz/signoz/v0.143.0/pkg/query-service/app/http_handler.go)
  still registers the four v1 POST history routes and `GET /api/v1/rules`.
  Deprecation is confirmed; a removal release is not. `query-language-routing.md` owns migration
  shapes and the independent deployment SQL-alert gate.
- **ClickHouse gap:** the chart still ships the older server; current upstream syntax is not
  automatically available there. New `26.9` JSON bracket paths, `LIMIT` boundaries, external
  DISTINCT and token features are described in the [release](https://clickhouse.com/blog/clickhouse-release-26-09),
  and `26.8` pipelined SQL/text tokenizers in its [release](https://clickhouse.com/blog/clickhouse-release-26-08).
  Do not transplant these into baseline queries or change vendor indexes. Confirm `SELECT version()`
  through authorized evidence before using a new function, syntax or setting.

## Released schema evidence

Collector tag `v0.144.11`, read 2026-09-26:

- [traces migrations](https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/v0.144.11/cmd/signozschemamigrator/schema_migrator/traces_migrations.go):
  preserved bucket/resource sorting prefix; migrations add JSON `scope`, `attributes` and
  `attributes_promoted`. They are optional probes, never a new floor for older consumers.
- [logs migrations](https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/v0.144.11/cmd/signozschemamigrator/schema_migrator/logs_migrations.go):
  JSON body columns and bloom-index expressions remain version-dependent; `UpItems` and `DownItems`
  are opposite directions, so a drop in rollback code is not a forward removal.
- [metrics migrations](https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/v0.144.11/cmd/signozschemamigrator/schema_migrator/metrics_migrations.go):
  sample flags and reduced-series families remain; infer neither target presence nor full layout
  from an ALTER/MV occurrence. Preserve rollup/exponential-histogram discovery gates.

Source confirms released definitions, not completed migrations on a target. Database overrides,
retention, 1800-second bucket width/resource retention margin and optional tables need target
confirmation. `GET /api/v1/version`, `SELECT version()`, `SHOW TABLES`, `DESCRIBE TABLE` and
sorting-key evidence are read-only methods for a separately authorized session. Without them,
keep the literal `UNVERIFIED SCHEMA` label required by the skill. Synthetic TSV fixtures test
column-name and sorting-key assertions only; they are not real DESCRIBE output or type validation.

## Release coverage since the previous snapshot

All entries in these thirteen releases were reviewed on 2026-09-26. Rows map related changes
to owning guidance; omission reasons follow. Omissions prove neither deployment equivalence
nor permission to drop older paths.

| Released source | Relevant delta and owning guidance |
|---|---|
| [v0.135.1](https://github.com/SigNoz/signoz/releases/tag/v0.135.1), 07-31 | History UI v2 -> alert lifecycle above; telemetry-resource authz -> deployment-specific authorization; panel query/default fixes -> preserve panel-owned query and variables |
| [v0.136.0](https://github.com/SigNoz/signoz/releases/tag/v0.136.0), 08-05 | `search()`, DateTime64 aggregation, Delta sum semantics, comparator enum, dashboard migration retry -> signal references and query routing; FGA flag removal -> never infer access from old UI |
| [v0.136.1](https://github.com/SigNoz/signoz/releases/tag/v0.136.1), 08-05 | Reduced-metric local-table query fix/JSON parsing -> metrics target-table gate; does not authorize local-only cluster queries |
| [v0.137.0](https://github.com/SigNoz/signoz/releases/tag/v0.137.0), 08-12 | PromQL native translation/NaN filtering, normalized metric compatibility removal, semconv families, saved-view changes -> metrics/routing gates; dashboard FGA and legacy APIs -> version-specific permission/API checks |
| [v0.137.1](https://github.com/SigNoz/signoz/releases/tag/v0.137.1), 08-14 | JSON log responses, `search()` editor, missing-label warnings, last-observed fix reverted -> logs/metrics references; password-reset revocation -> no session-format/access assumption |
| [v0.138.0](https://github.com/SigNoz/signoz/releases/tag/v0.138.0), 08-19 | Trace semantic names, typed metric filters, JSON body parse default, query-type cache key -> context/type checks; service-account role API -> release-matched authorization |
| [v0.139.0](https://github.com/SigNoz/signoz/releases/tag/v0.139.0), 08-26 | Same-name fields split by type, semconv services, stacking, log timestamp/body fixes -> explicit context/type and panel shape; nested service-account role API removal -> no guessed API lifecycle |
| [v0.140.0](https://github.com/SigNoz/signoz/releases/tag/v0.140.0), 09-02 | `/prometheus` API, trace scope fields, JSON query decoding, exponential histogram resolution -> metrics/traces routing; disabled-alert firing fix -> discovery never assumes notification safety |
| [v0.141.0](https://github.com/SigNoz/signoz/releases/tag/v0.141.0), 09-09 | Dashboard v1 retirement, field/quick-filter APIs, notification v2 create, refresh/filter fixes -> panel/API and field checks above; ingestion FGA -> authorization owner |
| [v0.141.1](https://github.com/SigNoz/signoz/releases/tag/v0.141.1), 09-09 | Trace-funnel Viewer enforcement -> deployment-specific authorization; explorer code split omitted as internal refactor |
| [v0.142.0](https://github.com/SigNoz/signoz/releases/tag/v0.142.0), 09-16 | Heatmap/text specs, notification v2 APIs, AI alerts, gated JSON trace reads, FGA/TLS, password-format secrets -> routing/version gates; no SQL-alert or installed-TLS inference |
| [v0.142.1](https://github.com/SigNoz/signoz/releases/tag/v0.142.1), 09-17 | JSON trace attribute bag, quoting, webhook Bearer handling, bulk-filter override removal -> stored-column/API checks; no local settings override |
| [v0.143.0](https://github.com/SigNoz/signoz/releases/tag/v0.143.0), 09-23 | AI mapping/pricing, opaque sessions, rotation/revocation/JWT fixes, resource precedence, v1 dashboard/Prometheus-provider removal, dynamic-variable/error-query fixes -> decisions above; no query language or authorization upgrade inferred |

UI styling, storybook/CI/test maintenance, package bumps, analytics instrumentation, onboarding,
billing/licensing, provider-specific channel configuration and cloud integrations are not implemented
here: they neither define this skill's raw SQL nor grant deployment authority. Their API/security
implications remain subject to release-matched docs. No upstream security fix is claimed deployed.
Collector configuration, chart rollout and data migration execution remain outside this source refresh.

## Proof boundary

Run the three checker self-tests, the local SQL examples and green schema fixtures. The link
self-test is offline; run the normal link checker separately for reachability. Missing sorting-key
evidence is exit 2; a changed prefix is exit 1. `S8` must reach the actual file/run dispatch for
vendor DDL; the nonvendor control remains outside this skill's gate. These are static/fixture
claims only. Native runtime SQL, consumer upgrade, live schema, alert acceptance and installation
activation require separate authorized evidence; none is supplied by this ledger.

Local refresh checks on 2026-09-26 passed: links offline self-test (10 assertions), schema
self-test (5 cases), SQL self-test (21 cases), SQL examples (18 checked, 16 skipped), and
green schema fixture (0 findings, 19 optional-table/column notes). The normal link gate
reached 30 unique official URLs across 35 references. The vendor OPTIMIZE CLI fixture
returned the required exit 1/S8; quoted identifiers have separate dispatch regressions.
Both plain and quoted nonvendor controls returned exit 0/out of scope.
