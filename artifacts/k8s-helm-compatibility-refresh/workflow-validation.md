# Workflow validation evidence

Observed 2026-09-26, repository root, BelowNormal PowerShell, Python `-B`.

Command (both attempts):
`python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260925-220655_k8s-helm-compatibility-refresh.md`

1. Exit 1: completed Phase 1 lacked a recognized content snapshot. One repair
   captured a deterministic 57-file SHA-256 manifest and added HEAD/digest evidence.
2. Exit 1 after the repair: same `plan.phase-snapshot` finding. The retry evaluated
   changed plan contents, not a flake-detection repetition. Read-only diagnosis found
   the validator also requires a literal `path` or `paths` token followed by a value
   (validator lines 258-261); `relative path/content manifest` does not match.

Disposition: BLOCKED after the authorized repair/retry budget. No third invocation
or second repair for this operation. Source work and independent checks continue.
Recovery: in a separately authorized retry, replace the snapshot description's path
phrase with `paths skills/sohrab/alaa-k8s-helm/** scripts/validate_sohrab_skill_pack.py
scripts/check_skill_index.py scripts/check_fleet_references.py scripts/check_lifecycle_contract.py`,
preserve the observed HEAD/digest/manifest, then run the exact validator command.
This is a workflow-record formatting defect, not a skill-source failure. The content
snapshot itself exists and is not being treated as a validator PASS.
