# Independent review cycle 1

Candidate aggregate source SHA-256: fb7f8e79623ec690d3a9efbbf41dfa44ba21dbeaa1487bb1adbfcdba8f479b95 (84 files). Reviewers read actual diff and new files; source writes paused. Runtime serving identity and effective role enforcement unknown for every reviewer.

## Correctness

VERDICT: CHANGES-REQUESTED. Role alaa-reviewer, configured gpt-6-sol/high.

- Major, confidence 0.99, scripts/check-signoz-sql.py:175: quoted vendor identifiers bypass S8; actual in-memory run dispatch for DROP TABLE `signoz_traces`.`distributed_signoz_index_v3` returns clean, checked 0/skipped 1. Normalize valid quoted DDL target identifiers and add CLI-negative regressions. Owner Lane S.
- Minor, confidence 0.76, references/query-language-routing.md:52: persisted SQL rule listing may survive upgrade despite current save rejection. Require version-matched acceptance evidence; listing alone remains unconfirmed. Owner Lane S.

Correctness recomputed all source hashes. Public Vector tagged upgrade guide inspected; no real Vector/ClickHouse/deployment proof. Native combined gates pending.

## Instruction contract

VERDICT: CHANGES-REQUESTED. Role alaa-instruction-reviewer, configured gpt-6-astra/high.

- Major, signoz-focused.md:24: blanket atomic exemption is invalid for changed logs/metrics/traces guides at 228/323/302 lines; independent worked examples and explanations are narrative. Cluster coherent topics inside Lane S and preserve complete SQL/schema blocks. Grade each resulting eligible document; genuine execution contracts and decision records stay exempt.
- Minor, plan:40/55/62: completed/checked phases still said not started/not run. Lead corrected stale summary sentences; final checkpoint must remain consistent.

All 84 source hashes verified. No further instruction findings. No official source fetch under native-only reviewer authority; no runtime or intermediate draft artifacts assessed.

## Security preliminary finding

Review still in progress. scripts/check-vector-configs.mjs:167 uses /confin|authority|host/i, which matches red-uri-authority.yaml in an unrelated failure diagnostic. Reviewer reproduced actual selfTest with stubbed checkGroup returning exit78 and 'Failed to load v0.58/red-uri-authority.yaml: unknown field unexpected'; failures remained zero. Require a field-specific error phrase and an in-process negative diagnostic regression. Owner Lane V. This is checker false confidence, not a claimed deployed vulnerability or actual Vector test.

## Scheduling

Runtime rejected specialist dispatches while capacity was occupied; gates are serialized, never substituted. Finished writer lanes will resume only after consolidated findings and available capacity. No installation or model configuration change is authorized.

## Security final

SECURITY VERDICT: BLOCK for the diagnostic-discrimination weakness above. Role alaa-security-reviewer, configured gpt-6-astra/high. Severity medium, high confidence; in-process reproduction proves false-positive test evidence, not a deployed exploit. Required repair: specific diagnostic class/field independent of filenames, plus offline controls rejecting unrelated errors containing authority/host/path. Other examined secret-interpolation, redaction, approved-host, TLS, field-scoped confinement and discovery-authority guidance passed source review. Actual binary tests remain unavailable.

## Observability final

OBSERVABILITY VERDICT: PASS-WITH-GAPS for source refresh. Role alaa-observability-reviewer, configured gpt-6-sol/medium.

Medium documentation gap, Vector references/65-troubleshooting.md:97: data-loss branch omits acknowledged invalid-record loss. Add buffer_discarded_events_total and bytes counters with intentional=false, then route to buffer and historical exactness/privacy owners; never add rejected payloads to telemetry. Owner Lane V.

High residual for any actual exactness consumer: counters reveal loss volume, not record identity/replay. The existing historical ingest guide already assigns the recoverability/privacy decision to consumer owners. Real deployment, drop reasons, dashboard migration and engine behavior are unproven and outside this source-only run. Source guidance must not claim end-to-end exactness.

## Release guidance final

RELEASE VERDICT: NOT-READY for the first candidate because known source findings remained open and combined native gates were pending; no additional distinct release-guidance defect. Role alaa-release-guardian, configured gpt-6-sol/medium. Released chart/appVersion/collector/database distinctions, older consumer paths, paired SigNoz upgrade and rollback caveats were inspected. Deployment inventory, real binary validation, schema/alert acceptance, rendered chart, admission, recovery/load and CI/package proof remain external/unrun. This source-only task requests no release.

## Disposition

All source findings accepted for fix cycle 1. Lane S: quoted SQL target normalization with discriminating CLI controls; current-version alert acceptance caveat; cluster the three narrative query guides. Lane V: diagnostic-class discrimination plus offline wrong-diagnostic controls; explicit acknowledged-invalid-record loss troubleshooting and safe escalation. Lead: workflow phase summary consistency. No additional source scope, model policy, install, dependency, consumer or deployment change.
