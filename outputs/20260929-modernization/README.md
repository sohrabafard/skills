# Sohrab modernization archive - 2026-09-29

This directory preserves the completed modernization task's plans, research, snapshots, reviews,
test evidence and historical helper scripts. It is not part of the installed workflow skill.

## Read order for the next upgrade

1. Read the [completed plan](docs/_agent_plans/20260929-120000_sohrab-modernization.md) and
   [checkpoint](docs/agents/20260929-120000_sohrab-modernization-state.md) for scope, decisions and limits.
2. Read [the per-skill assessment](assessment.json) for the affected skills; consult their named
   research and implementation evidence when rechecking a finding or source.
3. Read [the completion report](completion-report.json) and [final status gates](final-status-gates.json)
   for outcomes, remaining consumer-specific uncertainties and links to the detailed receipts.
4. Use [the final source manifest](candidate-8.sha256) and [snapshot metadata](candidate-8.json)
   to identify the tested source. Compare current files before citing historical test results.

For new work, use the current workflow skill to create a new task family. Keep this completed
archive as history; do not turn its completed checklist into the next upgrade's active plan.

## Relocation and historical paths

The former repository-relative prefix was
`skills/sohrab/alaa-workflow/outputs/20260929-modernization/`.
Its current replacement is `outputs/20260929-modernization/`.
Apply that mapping when locating evidence named in old commands or reports. Internal relative
links and the repository-relative source paths in the manifests retain their meanings.

All 265 original files moved without content changes. [The relocation manifest](relocation-manifest.json)
records their relative paths, sizes and SHA-256 hashes. Old timestamps, commands, failures and
snapshot exclusions remain historical facts; they were not rewritten as new validation results.

Repository rules ignore raw `*.log` files, so a future clone may contain receipts without those
local logs. Treat a missing log as unavailable evidence; do not infer a new passing result.

The historical `capture_candidate.py` and `run_candidate7_gates.py` assume the old directory
depth and can overwrite task evidence. Do not run them for a new upgrade. Use the current
repository and owning-skill validators with the new task's paths and evidence directory instead.

Return to the [upgrade evidence index](../README.md).
