# Final persisted-format compatibility review

VERDICT: COMPATIBLE-WITH-MIGRATION

Independent observer: final_schema_review, alaa-api-contract-reviewer; requested gpt-6.1-sol/medium, configured neutral, serving identity unknown. Read-only lane restriction; reviewer reported workspace-write runtime sandbox, not enforced read-only isolation. No writes or tests performed.

Candidate: HEAD 1a0799de71254427973f1253d80b846fea9acf10 plus phase3-candidate.json product SHA-256 ec745fd082cf3050b25b89dca7b2693cb3a3eb78c73804997c08448324309f90.

## Verdict details

- Initializer line 250 intentionally rejects formerly valid default/phased local creation with misuse exit 2. Callers require adopted Beads/binding; direct single-phase callers retain local via --profile direct. This restriction is documented and tested.
- New hierarchy families emit schema 3 with current_task/current_subtask strings and the none sentinel. Existing schema-2 families require no automatic conversion. Old consumers cannot safely execute new families.
- No additional actionable compatibility defect found within the inspected scope.

## Compatibility window and rollout

- Upgrade initializer, validator, templates, workflow instructions and both orchestrator consumers together before producing/executing hierarchy families (task-tracking.md, Helper boundary and compatibility).
- Preserve existing local, flat Beads and unmarked families until explicit migration. Destination binding, mappings, acceptance/evidence and cutover owner must be verified; old authority becomes read-only.
- Rollback freezes new marked families. Older validators may treat schema 3 as legacy under auto detection; apparent validation success cannot authorize downgraded execution.
- Deprecated aliases retain one transition period without a dated sunset; this candidate removes none.
- Both orchestrators consume whole-engagement boundary and cursor; nested invocations cannot reset them.

## Evidence and limits

Inspected scoped old/new workflow initializer/validator, five templates, tests, task-tracking, lifecycle/continuity/integration references and both orchestrators' gate contracts. Consumer discovery covered those packs and repository scripts; installed/external consumers remain unverified.

No material transition-spec/test drift found. Historical fixtures reconstruct prior families; they do not execute old installed consumers. No fresh tests ran. Offline structure proves no live Beads registration, authority or readiness.

Parent disposition: accept documented source-format/CLI transition within the explicitly requested hierarchy change. No installation or live migration is authorized. The final commit/release notes must disclose the command-contract change. Broader correctness and instruction gates remain separate.
