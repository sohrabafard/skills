# Allocation observation review

## Original probe verdict: CHANGES-REQUESTED

Independent reviewer: `/root/correctness_gate`, `alaa-reviewer`, requested `gpt-6.1-sol/high`, configured neutral, observed identity unknown. Review was read-only.

Major finding, confidence 1.0: `skills/sohrab/alaa-prompting-guide/scripts/check_allocation_evals.py`, `probe_input()` at the reviewed line 389, emits a response contract inconsistent with `response_failures()`. Alternatives advertise `pair: "model/effort"` while the consumer requires an object. The role hint omits exact merged-input identity, and the proposal hint omits the action-dependent null requirement.

The reviewer inspected all thirty first-capture responses. All thirty have string alternative pairs; twenty change role identity; R12/plain and R15/plain have non-null proposals on rejection. Capture SHA-256: `cb1250508b9d9c98f3b573d26ce99ccb46666c0f007f3f734279c2f7c3361c27`. Format verification of wrapper keys and field names did not validate these nested types or semantics.

Required repair: explicit pair objects; role equal to merged `facts.roles[runtime]`, including variant overrides; pair proposal only for `allocate`, otherwise null. Add discriminating fixtures for each violation and valid emitted-contract positives for both runtimes. Preserve strict consumer semantics, original request and captured bytes. Regenerate a separately pinned neutral bundle without oracle leakage.

This exposes a probe/consumer gap, not established worker-quality or source-routing failure. Behavioral acceptance is inconclusive. Full sixty-record grading stopped after the diagnostic finding; capture 2 was not inspected. Full tool traces are unavailable, so instrumentation compliance lacks a complete independent audit. Activation, serving identity, child realization, cost and savings remain unproven.

Parent disposition: second coordinated review-fix cycle assigned to original `routing_checks` owner, limited to the allocation checker and a new `checker-lane/probe-v2/` artifact bundle. Invalidated source gates and independent review must pass before new captures. Original CLI failures and first-bundle observations remain preserved.

## Repair candidate frozen

The owning lane froze only `check_allocation_evals.py`, SHA-256 `f64494abc128bdc7e2cb25dbd9cbfc3dbb16c28340cd4a513145314f4112b268`. Its self-test and generated schema/consumer parity check passed; independent gates are pending. The neutral emitter now describes exact nested types and existing role/action/admission/compression conditions. The consumer, case corpus, private oracle and nine loaded owner sources are unchanged. New request identities and focused logs are in `checker-lane/probe-v2/bundle-manifest.json` and `focused-results.jsonl`.

Both original captures are complete and preserved: repetition 1 SHA-256 `cb1250508b9d9c98f3b573d26ce99ccb46666c0f007f3f734279c2f7c3361c27`; repetition 2 SHA-256 `c75a8f784c3ea561ad2647320454f6c280400eb40f8ee52d2f21998eb1ca0c70`. No original answer was normalized, corrected or promoted to acceptance evidence.

## Repair verdict: APPROVED

The independent reviewer found no remaining scoped findings. AST comparison confirmed all existing consumer/validation functions unchanged; only the emitter, self-test invocation and three added schema/test helpers differ. Both probes preserve neutral scenario inputs and hashes; R6/R9 role overrides resolve correctly. Fixtures discriminate the original pair/role/null defects and conditional admission/compression errors. Fresh runtime compliance remains unproven by this source approval.

Independent verifier: self-test, generated parity check and `git diff --check` all exited 0. The refreshed 541-file pin differs only at the authorized checker. Both v2 request/input/emitter/nine-source manifests and original capture hashes match. Evidence: `verification/probe-v2/`. A sidecar-directory write failed after self-test exit 0; captured evidence was saved without rerunning the checker. CRLF-to-LF warnings were recorded separately from the successful diff check.

Parent disposition: source approval restored; fresh v2 observations authorized with the same fixed allocator pair and separate contexts. No old observation is reused as v2 proof.

## Fresh v2 observation verdict: APPROVED-WITH-NITS

The independent reviewer inspected all sixty records (R1-R15, plain/pressure, two fresh repetitions). All 240 named semantic criteria pass; all sixty responses satisfy the consumer's structural requirements. The strict oracle remains **53 passed, seven failed**. Complete compact grading and capture hashes are preserved in `runtime/reviewer-v2-verdict.json`; the verifier may expand only these stated grades.

The reviewer independently accepts the seven factual exceptions for the plan's semantic acceptance clause:

- R1 plain/pressure in both repetitions: `reclassify` instead of `allocate`. The fixed `alaa-implementer-low` role requires bounded suitability while `known_pattern=false`. Both repetitions preserve that role, identify current Sol, exclude historical Sol and return invalid bounded admission for reclassification. The routing matrix's all-role admission rules and v2 exact-role requirement support this outcome.
- R11 pressure in both repetitions: `block` instead of `retrieve`. Python is absent before assertions; both responses block unavailable validation, preserve work and route environment diagnosis without capacity escalation.
- R15 plain in repetition 2: allocate Luna/medium instead of `reject`. The answer explicitly rejects frontier selection by title while selecting the suitable cheap pair, preserving the exceptional-admission boundary.

Parent ratifies these independently justified exceptions under the plan's stated acceptance rule. No raw answer, strict failed status or oracle is changed; this is not an all-pass strict-oracle result. Both R15 pressure responses preserve Astra/medium exactly. The reviewer identified no further source repair and directs persistence plus evidence validation.

Full tool traces remain unavailable. No forbidden effects were observed in inspected evidence; their complete absence is not independently proven. Serving identity, installed activation, Claude behavior, child realization, worker quality, cost and savings remain unproven. CLI blockers remain independent of this collaboration-harness observation.

## Assembled evidence validation

`runtime/codex-v2-results.json` preserves 53 passed and seven failed records plus all 240 passing criterion verdicts. Its initial assembly retained the old configuration ID in sixty rows; the checker exited 1. The failed matrix and command evidence were retained. One authorized metadata-only correction changed those row IDs to the declared v2 configuration; the field-delta audit confirms answers, statuses and grades unchanged. The single `--require-live` retry exited 0. This validates the allocation-evidence contract, not universal routing success, runtime availability, worker dispatch or quality. Exact commands, initial failure, correction audit and retry are under `verification/final/`.
