# Focused verification contract

Test strategist: test_contract, configured gpt-6-sol/medium, observed serving identity unknown. Read-only design; no test execution in that lane. Writers own focused checks, independent verifier owns combined native gates.

| Failure | Minimal discriminating check | Proof and limit |
|---|---|---|
| SQL CLI skips vendor DDL before S8 | OPTIMIZE TABLE signoz_traces.distributed_signoz_index_v3 FINAL through CLI/run must exit 1 with S8; nonvendor control must not receive S8 | In-process checker behavior; not ClickHouse execution |
| Missing sorting key yields clean | Synthetic complete DESCRIBE with sorting-key evidence absent must return unavailable/finding, never 0; wrong prefix remains a separate red case | Synthetic schema fixture; not installed schema |
| Intentional dead link contaminates production URL collection | Red test fixture excluded from production collection, real reference URL retained | Offline collector behavior |
| Link self-test depends on public DNS | Stub deterministic judge/transport results; keep regular real-network gate separate | Offline self-test is not link availability |
| Vector product resolver accepts draft/prerelease or vdev | Numeric higher draft/prerelease, nightly and vdev excluded; only-nonstable returns unknown/null | Offline resolver, not release availability |
| Speculative Cargo fallback or develop chart masquerades as stable | Published product release and released chart tag provenance required; preserve appVersion distinction | Public source evidence; not consumer installed version |
| Runtime security failures masked by validation options | Existing confinement/undersized-buffer red fixtures, green fixture and vector test with exact installed binary; warning fixture when validation logic changes | Actual local Vector process required; missing binary is unavailable proof |

Exact existing check names are in the plan. Run Python with -B and BelowNormal, Node from the owning skill directory. Do not install tools. No live SigNoz access, schema probe, alert save/delete, benchmark or service launch. Use one cause-specific repair and one materially different retry at most; keep every failed result visible.

Acceptance evidence must name command, cwd, exit, observed diagnostic, tested HEAD and deterministic scoped content digest. Do not count a tool inspection or help call as a passed behavioral test. Unchanged focused results may be cited with their original observer/time/digest; combined source gates remain independent.
