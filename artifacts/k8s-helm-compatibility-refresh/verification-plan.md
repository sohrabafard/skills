# Independent verification plan

Run from the repository root after writer completion and source freeze. Use
BelowNormal process priority, one bounded command per invocation, sequential
execution, Python `-B`, no installation or cluster access. Each command has a
120-second limit; freshness has a 60-second limit. Save logs and exact command,
exit, timestamp, tier and proof limit under `verification/` in this directory.
No source changes or automatic retries. Report failures to the lead.

## Affected source gates

1. `python -B skills/sohrab/alaa-k8s-helm/scripts/check_versions.py --self-test`
2. `python -B skills/sohrab/alaa-k8s-helm/scripts/check_versions.py`
3. `python -B scripts/validate_sohrab_skill_pack.py`
4. `python -B scripts/check_skill_index.py`
5. `python -B scripts/check_fleet_references.py`
6. `python -B scripts/check_lifecycle_contract.py`
7. `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py`
8. `git diff --check`

The plan's workflow-validator gate is already BLOCKED after the allowed retry
budget; see `workflow-validation.md`. Do not repeat it in this lane or count it as
passed. Any final workflow changes remain unvalidated by that gate.

## Local chart evidence

Installed Helm is 4.2.3. Do not install other versions. Use the local synthetic
fixture `artifacts/k8s-helm-compatibility-refresh/chart-smoke`. The lead copied
Chart.yaml, values.yaml and values.schema.json from committed chart-good, and
clean.yaml into templates/workloads.yaml. The original chart-good template is
only a comment, so rendering it alone would not exercise manifest validation.

- Run `helm lint` with its own `values.yaml`.
- Run `helm template fixture` with that chart and its own `values.yaml`, once
  per documented authoring minor (1.34.0, 1.35.0, 1.36.0, 1.37.0), using
  `--kube-version`; save rendered files to this lane's artifact directory.
- Run `python -B skills/sohrab/alaa-k8s-helm/scripts/check_manifests.py` against
  each rendered file, and its `--self-test` when its diagnostic text changes.

Rendering a selected `.Capabilities.KubeVersion` is local template evidence,
not a supported client/server pairing or cluster admission proof. In particular,
Helm 4.2.3's supported client/server band ends at 1.36. No Helm 3/4.3 runtime proof.

Check touched Markdown links with the existing docs checker using explicit
`--files` paths. Skill instructions and workflow records are semantically atomic
artifacts; do not split them or treat a narrative line budget as an instruction
compression mandate. Record physical line counts and exemptions separately.

Source frozen manifest identifies the candidate; compare after verification.
Missing external schema/cluster/other Helm runtime checks remain explicitly unrun.
