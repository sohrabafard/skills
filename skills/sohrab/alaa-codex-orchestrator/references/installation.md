# Authorized Installation and Updates

Activation inspects role availability; it never installs or updates agents. Obtain explicit authorization for target paths before invoking any installer. `install-skills.md` at the repository root owns installation locations; /alaa-prompting-guide owns current runtime discovery and precedence facts.

## Source prerequisites

Test design/execution and legacy runner entrypoints require the separately available sibling `alaa-testing-strategy`. Preserve its `references/100-test-execution.md`, `references/110-execution-resources.md`, `references/120-result-classification.md` and canonical runners. A missing owner or runner is a blocking unavailable dependency, never implicit installation authority; obtain authorization for any companion installation.

Keep the complete orchestrator source beside `alaa-prompting-guide`, or pass its root explicitly (the third agent-installer argument or the second skill-installer argument). Validation fails with exit `2` when the canonical policy owner cannot be loaded. Never substitute a local copy of model policy.

The agent installer accepts only its own resolved canonical `agents/` directory. An alternate source directory is rejected before target writes, even when its sibling canonical source validates. Source TOMLs under `agents/` are transport-neutral templates and cannot be installed by plain copy. All installers validate model-neutral policy roles, role grants, generated reviewer wrappers, and the source manifest before writing to the target. A source failure leaves the destination untouched. Materialization then resolves the live parent MCP inventory, retains each transport discriminator, applies exact per-role grants, disables unassigned or unknown servers, and validates resolved definitions. Missing inventory or transport information fails closed.

## Explicit agent installation

From this skill directory, after authorization:

```bash
./scripts/install-agents.sh
```

The default target is `~/.codex/agents`. The installer changes only managed agent files, its lock/staging files, and the version/inventory sentinels. It replaces differing managed files and preserves unrelated agents and configuration. Source control owns rollback versions; inspect current runtime discovery before claiming the new roles are active.

To install the complete skill and its agents after authorization, use `scripts/install-skill.sh`. For isolated target inspection, pass an agent target as its third argument. The model-policy owner remains a required separate sibling or explicitly supplied source; these commands do not install it automatically.

## Reproducible source checks

```text
python3 scripts/render_agents.py --write
python3 scripts/render_agents.py --check
python3 scripts/validate_pack.py
```

The renderer preserves both correctness-review profiles from `assets/reviewer-contract.md`, adds standalone implementation/planner wrappers from their shared contracts and metadata-only `assets/profile-wrappers.json`, then writes the version/hash manifest. Canonical policy registers task-selected roles; all-role projections omit both model and effort pins without changing authority. Actual task controls must be explicitly supplied and verified at dispatch. `--check` never writes. Exit `0` is clean, `1` is findings/drift, and `2` is unavailable proof; either nonzero blocks installation and completion.

## Materialization proof without installation

```text
python3 scripts/check_agent_grants.py --materialize agents <new-empty-scratch-directory>
```

Inspect only that fresh directory. This validates grants against the live parent inventory; it neither installs nor proves model availability, effective parent sandbox overrides, runtime identity, or task quality. Record those evidence levels separately.

## Upgrade contract

Version 5 renames `alaa-implementer-sol` to `alaa-implementer-astra` without a source alias. Update dispatch callers. During an explicitly authorized installed upgrade, materialize the new wrapper with the supported installer and archive the old managed wrapper outside the agent discovery directory under that upgrade's target-path authority. The current installers preserve files absent from the new source; installation alone therefore does not retire the old role. Verify the new role and absence of the retired role before claiming activation.

Version 4 changes final-report parsing: verdict/status or opening outcome is first, followed by configured/requested settings and separately observed runtime identity. Unknown observations remain unknown. Existing verdict vocabularies remain unchanged. The deep role ID preserves workload/authority compatibility and supplies no model or effort. Review depth and actual task controls are separate decisions. Do not dispatch standard and deep profiles concurrently for one scope.

Missing, stale, or unavailable required roles must be reported; there is no silent fallback or implicit installation. A changed MCP inventory requires an authorized rematerialization. Never change global runtime configuration as an installation repair.
