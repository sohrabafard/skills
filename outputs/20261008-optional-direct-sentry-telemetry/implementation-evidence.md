# Optional Direct Sentry Telemetry - Implementation Evidence

- Agent: `policy_implementation`, role `alaa-implementer`; configured gpt-6.1-sol/high; requested override none; observed model/effort and runtime enforcement unknown. Workspace-write authority is scoped by parent assignment.
- Baseline: current `main`, HEAD `aa32353c7c38cf1700077f61d2f007128186f9de`; no branch or commit effect.
- Candidate: five skill references only; final source diff 42 insertions, 40 deletions. Sources frozen for independent gates.

## Prerequisite Read Coverage

Before source editing, read both affected SKILL files and `agents/openai.yaml`, all SOC references 00/10/20/30/40/50/60/70/80/90, and all services-contract references 00/05/10/15/16/20/21/22/23/24/25/26/27/28/30/32/35/40/50/60/65/90/95 plus all seven nested 26 references. Large reference 95 was read in contiguous batches, not replaced by a summary. `rg --files` inventory confirms neither skill contains scripts. Repository and first-party AGENTS, skill routing map `README.fa.md`, workflow, prompting, low-noise and prompting compression contract were read before writes. Excluded vendor files, live service repositories and external vendor capability verification: they are outside this prose change, and July capability statements retain their existing dated caveat.

## Draft and Compression Equivalence

Draft acceptance was the explicit user policy: optional direct SDK logs/traces; simultaneous duplicate delivery permitted; sensitive operators disable direct logs/traces while retaining exceptions and Vector/Collector; no new filtering, inspection or duplication approval. Compressed implementation places those clauses once in SOC 60, using pointers in 10/30/50. Platform trace sampling is scoped in 30 without changing any numeric default/ceiling. SOC 50 owns topology; contract 21 owns endpoint values and points back for placement. Privacy, fail-open, exception coverage, SDK exception before-send, scope reset, profiling and dated vendor caveats remain. Only legacy dual invocation forms inside already edited files were normalized, as required by repository rules. Parent review found one positional-bullet reference; it now names the exception-coverage requirement explicitly.

## Focused Validation

All commands ran at repository root, lightweight/default resource policy; no CPU-heavy runner required.

- Preparation: `python skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261008-020835_optional-direct-sentry-telemetry.md` exit 0 before source edits.
- Final source whitespace: `git diff --check -- skills/sohrab/alaa-observability-soc/references/10-signal-model.md skills/sohrab/alaa-observability-soc/references/30-quantitative-budgets.md skills/sohrab/alaa-observability-soc/references/50-telemetry-pipeline.md skills/sohrab/alaa-observability-soc/references/60-sentry-and-profiling.md skills/sohrab/alaa-services-contract/references/21-alaa-platform-observability-directive.md` exit 0; only Git CRLF-to-LF notices.
- Reconciled workflow validation initially exit 1: completed Phase A lacked a scoped snapshot. One cause-specific repair supplied actual HEAD and SHA-256 manifest; retry exit 0: "Validation completed without blocking errors (profile: resumable)."
- Broad skill gates and independent instruction review unrun by this lane; parent-dispatched gates own them. No runtime, SDK, Vector/Collector configuration or live deployment validation claimed.

## Frozen Source Manifest

Manifest digest: SHA-256 `9ab91e7dec7f4d948be91caa6201ab3205528d1561179bd4398512124c307e85`. Compute over sorted relative paths, each followed by one space and lowercase file-byte SHA-256, joined by LF with no final LF, encoded UTF-8.

| Path | File-byte SHA-256 |
|---|---|
| skills/sohrab/alaa-observability-soc/references/10-signal-model.md | db2138d63676af6f7ebbb6bb0271837b13d7717715bd54565eaa354ac79d4482 |
| skills/sohrab/alaa-observability-soc/references/30-quantitative-budgets.md | deec8d941c44334ddd15e20b85609c2edcc978b3ff20bade5692f3fbb6c14b6d |
| skills/sohrab/alaa-observability-soc/references/50-telemetry-pipeline.md | ec2c63b3dac83b93e85e1cf46d99e3b8f9928c33a45921c0cb977c656edb95a2 |
| skills/sohrab/alaa-observability-soc/references/60-sentry-and-profiling.md | b6a8c4d0a58f1c42f848c1d161280d52401f14ae12a6f0a5acfd519e845da73c |
| skills/sohrab/alaa-services-contract/references/21-alaa-platform-observability-directive.md | 9f3ee47e807b7450b204d28b7d28094e10ae907449c87e4001c60773d394f0d9 |
