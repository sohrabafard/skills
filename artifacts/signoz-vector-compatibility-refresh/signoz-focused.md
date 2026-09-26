# Lane S focused evidence

Observer: signoz (alaa-implementer-sol), configured gpt-6-astra/high; serving identity unknown. Frozen 2026-09-26T05:40:29.150550Z, HEAD 3a62cbb615e0180458ebedd4bc9a0794c17c1e60. Scope: skills/sohrab/alaa-signoz-clickhouse-docs, 51 files including new fixtures.

Digest: 0668c4737f35a1a6e2d36ead81ad1a03c53897a58583b64d0a1c65abe7d34bcc. Method: lexicographically sorted repository-relative POSIX paths; each UTF-8 manifest row is file SHA-256, two spaces, path, LF; hash the manifest. This writer-specific method differs from the lead combined snapshot method.

All commands below used the skill directory, Python -B, PowerShell process priority BelowNormal. Tier: focused. Results are writer-observed, not independent acceptance.

| Command (prefix python -B) | Exit | Result | Proof |
|---|---:|---|---|
| scripts/check-signoz-links.py --self-test | 0 | 10 assertions | Offline checker unit |
| scripts/check-signoz-schema.py --self-test | 0 | 5 cases | Synthetic fixture unit |
| scripts/check-signoz-sql.py --self-test | 0 | 19 cases | Checker unit, including actual run dispatch |
| scripts/check-signoz-sql.py --skill-dir . | 0 | 18 statements, 16 fragments skipped, 0 findings | Static example checks |
| scripts/check-signoz-schema.py --describe-dir test/fixtures/schema/green | 0 | 0 findings, 19 optional notes | Synthetic fixture, not installed schema |
| scripts/check-signoz-links.py --skill-dir . --concurrency 2 --timeout 15 | 0 | 35 references, 30 unique URLs | Public link reachability only |
| scripts/check-signoz-sql.py --sql test/fixtures/sql/vendor-ddl.sql | 1 | Expected S8 rejection | Negative CLI control PASS |
| scripts/check-signoz-sql.py --sql test/fixtures/sql/nonvendor-ddl.sql | 0 | Skipped outside owned vendor scope | Scope control |

All three --help calls exited 0; these are CLI inspections, not behavioral checks. Link self-test was rerun after its assertion-count reporting was corrected; final result above belongs to final script. Pre-repair reproductions are retained in the verification contract and preflight; they are not passes of this candidate.

Changed: 14 tracked files plus two SQL fixtures. Release ledger in references/90-versions.md covers 13 application releases v0.135.1 through v0.143.0. It separates released chart/app/collector/database pins, upstream ClickHouse stable/LTS and unknown consumers. Alert evidence remains unconfirmed; recorded status checking does not establish deployment identity, version, age, type or actual acceptance.

Documentation classification: references/00-topic-map.md GREEN (33 lines), test/fixtures/schema/README.md GREEN (22). Other changed Markdown is EXEMPT-ATOMIC: skill execution contract, ordered evidence selection, per-signal schema/query contract, compatibility decision record, or integrated alert-surface gate. No narrative size exemption is inferred solely from location.

Not run: real SQL, installed schema, alert acceptance, consumer compatibility runtime or activation. No live discovery or installation. Independent review/security/native acceptance remain pending.
