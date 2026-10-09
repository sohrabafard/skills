# Agentic economy upgrade

Date: 2026-10-09  
Source status: `MERGE_CANDIDATE`; independent source inventory passed.  
Parent-owned plan and documentation closeout is tracked separately. Release and publication were not requested.

This change updates four first-party skills: `alaa-workflow`, `alaa-prompting-guide`, `alaa-codex-orchestrator`, and `alaa-cc-orchestrator`. Both orchestrators now identify as version 5.3.0.

## What changed

- Plans persist decisions, dependencies, ready parallel sets, resource conflicts, and integration barriers. The runtime's observed capacity controls dispatch; the workflow defines neither a fixed writer ceiling nor a new scheduler.
- After tasks are finalized and compatible work is consolidated, one allocation pass selects the role, model, effort, and priority for each task. Balanced is the default; changes reallocate affected remaining tasks only.
- Verification evidence is attributed to its outcome, input, and observer. Later phases and agent changes can reuse still-valid evidence; changed inputs invalidate affected checks. Independent acceptance remains required.
- Canonical model policy distinguishes official selector guidance from local role admission and uncalibrated routing hypotheses. Claude guidance covers Haiku, Sonnet, Opus, and Fable; Sonnet retains medium/high routes, and Mythos is excluded. Source profiles add six Codex combinations and Claude Haiku-high for bounded, longer or stricter work. Existing role authority and safety grants remain in force.

The full selection policy is in the [canonical model-selection reference](../../skills/sohrab/alaa-prompting-guide/references/90-model-selection.md). Implementation sources are documented in the [workflow](./workflow-implementation.md), [prompting policy](./policy-implementation.md), and [paired orchestrator](./orchestrator-implementation.md) reports. The dated [official source evidence](./source-evidence.md) and [model-selection snapshot](./official-model-selection.md) preserve vendor recommendations separately from local policy.

## Verification and review

The [independent verifier summary](./verification/candidate/summary.json) records 14/14 outcomes passing: five corrected checks ran after the checker fix, and nine unchanged results were reused. The earlier two pack-validator failures remain in the raw evidence and are resolved by those post-fix passes. The 75-test workflow result was reused because its 16 source hashes were unchanged.

Independent [correctness](./reviews/correctness.md) and [instruction](./reviews/instructions.md) reviews are approved. The [release review](./reviews/release.md) is ready with conditions; independent source verification discharged its source-packaging condition. Installation, runtime activation, account access, live calibration, comparative quality, and measured savings remain unverified.

Installation instructions and installed copies remain unchanged: the existing guide already documents policy dependencies and runtime discovery, and this work did not include rollout or installation.

The aggregate source inventory covered 249 files. Closure observed no changes during verification, and the two unrelated `alaa-services-contract` files matched their initial hashes. Detailed inputs, decisions, and verification artifacts are linked from the [durable plan](./docs/_agent_plans/20261009-090000_agentic-economy.md).

## Compression measurement

`SKILL.md` bodies were counted by whitespace splitting against the recorded baseline. The four bodies changed from 10,256 to 7,928 words (22.70% fewer body words). This static count does not establish token or latency savings.

| Skill | Before | After |
|---|---:|---:|
| `alaa-workflow` | 1,662 | 1,588 |
| `alaa-prompting-guide` | 1,439 | 873 |
| `alaa-codex-orchestrator` | 3,609 | 2,751 |
| `alaa-cc-orchestrator` | 3,546 | 2,716 |

The report is the archive's reader-facing summary. The plan, implementation records, source tables, and machine-readable verification evidence remain their own complete artifacts.

## Later authorized installation

After this source report, the user authorized both runtime installations. The [installation receipt and postcheck](installation/README.md) record 33 Codex and 29 Claude definitions installed successfully, with backups and preserved unrelated settings. This does not establish loaded-session activation or live model behavior.
