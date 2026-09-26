# Accepted repair evidence

Observed 2026-09-26 by the two original owned writers. Source remains frozen for independent closure. Candidate 2 contains 109 files; aggregate SHA-256 `1a890b9bd8f908041a0d63ee32a1fce2eb1c4d67ce56911c2aac13b4e964665f`, with every file recorded in `candidate-snapshot-2.json`. This identity includes new files and does not imply runtime proof.

## SigNoz writer

Freeze: 2026-09-26T05:59:23.997423Z. Same baseline HEAD. The quoted vendor DDL fixture reproduced exit 0 / checked 0 / skipped 2 before repair. After repair it returns expected exit 1, two S8 findings, checked 2 / skipped 0. Quoted nonvendor names and string-literal decoys return exit 0 / skipped 3. Persisted alert rules are discovery clues, never current-version acceptance evidence.

Commands below ran with Python `-B`, BelowNormal priority, from `skills/sohrab/alaa-signoz-clickhouse-docs`:

| Command | Result |
|---|---|
| `python -B scripts/check-signoz-sql.py --self-test` | 0; 21 cases, no failures |
| `python -B scripts/check-signoz-sql.py --skill-dir .` | 0; 18 checked, 16 skipped, no findings |
| `python -B scripts/check-signoz-links.py --self-test` | 0; 10 assertions, no failures |
| `python -B scripts/check-signoz-sql.py --sql test/fixtures/sql/quoted-vendor-ddl.sql --json` | Expected 1; two S8 findings |
| `python -B scripts/check-signoz-sql.py --sql test/fixtures/sql/quoted-nonvendor-ddl.sql --json` | 0; negative controls preserved |

From repository root, `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files <files> --line-budget` passed for the three signal entrypoints, all 23 new children under references/logs, references/traces and references/metrics, references/00-topic-map.md, and test/fixtures/schema/README.md. All paths are beneath the SigNoz skill. Result: 25 GREEN, 3 YELLOW. YELLOW files are logs/50-panel-shapes.md (53 lines), traces/50-panel-shapes.md (55), metrics/60-counter-rate.md (56). Panel alternatives form a cohesive comparison; counter-rate keeps one complete reset-handling method and SQL block. The final topic-map correction was checked separately, exit 0, GREEN 34.

The same local-link checker without `--line-budget` passed for five atomic execution/decision contracts: SKILL.md and references/{10-docs-navigation,50-service-topology,90-versions,query-language-routing}.md. The three former oversized narrative guides are now GREEN entrypoints (19/36/23 lines). The sole skill-wide router remains references/00-topic-map.md.

Baseline executable SQL block preservation comparison: logs 8/8, metrics 11/11, traces 9/10; zero missing baseline blocks, one added optional JSON example. Unchanged schema and external-link checker inputs retain prior focused evidence in signoz-focused.md; no new external URL set was introduced by splitting.

## Vector writer

Freeze: 2026-09-26T05:59:03.3419056Z. Same baseline HEAD. Repair changes only scripts/check-vector-configs.mjs and references/50-validation-and-testing.md and references/65-troubleshooting.md. The confinement assertion requires unsuccessful status, diagnostic class PartialUriAuthority, and the fixture URI. Tagged source provenance: https://github.com/vectordotdev/vector/blob/v0.58.0/src/template/confinement.rs and https://github.com/vectordotdev/vector/blob/v0.58.0/src/sinks/http/config.rs (both HTTP 200 observed by writer).

BelowNormal Node commands from repository root:

| Command | Result |
|---|---|
| `node skills/sohrab/vector-rust-observability-pipelines/scripts/check-vector-configs.mjs --self-test-diagnostics` | 0; 10/10 offline controls: 2 positive, 8 negative |
| `node --check skills/sohrab/vector-rust-observability-pipelines/scripts/check-vector-configs.mjs` | 0 |
| `git diff --check -- skills/sohrab/vector-rust-observability-pipelines` | 0 |

Help inspection also returned 0, but is not counted as behavioral validation. Negative diagnostic controls include the reviewer's exact unrelated-error reproduction, filename/host/authority decoys, wrong class, wrong URI and successful status with diagnostic text. These are assertion tests, not fake Vector runtime proof.

Troubleshooting Class 4 now covers acknowledged invalid-record loss, both discarded-event/byte counters with intentional=false, and routes to buffer/exactness/recovery/privacy owners. Payload logging remains prohibited. References 50/65 remain atomic execution and failure-taxonomy contracts. Resolver inputs unchanged: prior nine controls and official version check remain applicable. Actual Vector execution remains ENVIRONMENT-BLOCKED: spawnSync vector.exe EPERM, regular checker exit 2. No retry or installation was attempted during this repair.
