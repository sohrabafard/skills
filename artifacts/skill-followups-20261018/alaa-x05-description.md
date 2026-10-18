## Goal
Verify the leak-detection oracle in the existing Octane skill.
## Scope
Read-only investigation of skills/sohrab/alaa-octane-performance/references/leak-detection-harness.md Shape A and matching framework source. Its refreshApplication scoped-binding versus leaked-singleton identity claim may need qualification; PHP lane did not verify runtime behavior and changed none of this harness.
## Acceptance Criteria
Trace actual application/container lifecycle for supported pinned versions; identify whether the oracle detects the stated leak; report source and runtime proof separately before proposing a correction.
Evidence: artifacts/skill-pack-optimization-20261018/lanes/PHP.md out-of-scope lead. Separate investigation, not a remaining acceptance item of alaa-6dh.

## Follow-up authorization
The user subsequently requested implementation of any necessary corrections and closure with evidence. That request extends the original read-only investigation scope to these bounded skill corrections.

## Findings
Confirmed false-green oracle: refreshApplication recreates singleton state. Replaced it with a same-container scoped-lifetime test and routed real-worker wiring to Shape B. On PHP 8.5.11 / Laravel 13.34.0, scoped passed, singleton and missing-reset mutants failed with tenant-a, restored scoped passed, and container recreation falsely passed.
Evidence: artifacts/skill-followups-20261018/verification.md. No live service, provider, deployment or installed-skill activation claim.
