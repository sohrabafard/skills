# Authorized Installation and Updates

Activation inspects role availability; it never installs or updates agents. Obtain explicit authorization for target paths before invoking any installer. `install-skills.md` at the repository root owns installation locations; /alaa-prompting-guide owns current runtime discovery and precedence facts.

## Source prerequisites

Test design and execution and legacy runner entrypoints require the separately available sibling `alaa-testing-strategy`. Preserve its `references/100-test-execution.md`, `references/110-execution-resources.md`, `references/120-result-classification.md` and canonical runners. A missing owner or runner is a blocking unavailable dependency, never implicit installation authority; a companion installation needs its own authorization.

Keep the complete orchestrator source beside `alaa-prompting-guide`, or pass its root explicitly: the third agent-installer argument or the second skill-installer argument. Validation fails with exit `2` when the canonical policy owner cannot be loaded. Never substitute a local copy of model policy.

The agent installer accepts only its own resolved canonical `agents/` directory. It rejects an alternate source directory before target writes, even when that directory's sibling canonical source validates. Source TOMLs under `agents/` are transport-neutral templates that a plain copy cannot install. Before writing to the target, every installer validates model-neutral policy roles, role grants, generated reviewer wrappers and the source manifest; a source failure leaves the destination untouched. Materialization then resolves the live parent MCP inventory, keeps each transport discriminator, applies exact per-role grants, disables unassigned or unknown servers, and validates the resolved definitions. Missing inventory or transport information fails closed.

## Explicit agent installation

From this skill directory, after authorization:

```bash
./scripts/install-agents.sh
```

The default target is `~/.codex/agents`. The installer changes only managed agent files, its lock and staging files, and the version and inventory sentinels. It replaces differing managed files and preserves unrelated agents and configuration. Source control owns rollback versions. Inspect current runtime discovery before claiming the new roles are active.

To install the complete skill and its agents after authorization, use `scripts/install-skill.sh`. For isolated target inspection, pass an agent target as its third argument. Neither command installs the model-policy owner; it stays a required separate sibling or explicitly supplied source.

## Reproducible source checks

```text
python3 scripts/render_agents.py --write
python3 scripts/render_agents.py --check
python3 scripts/validate_pack.py
```

The renderer preserves both correctness-review profiles from `assets/reviewer-contract.md`, adds standalone implementation and planner wrappers from their shared contracts and the metadata-only `assets/profile-wrappers.json`, then writes the version and hash manifest. Canonical policy registers task-selected roles; all-role projections omit both model and effort pins without changing authority. Actual task controls must be explicitly supplied and verified at dispatch. `--check` never writes. Exit `0` is clean, `1` is findings or drift, and `2` is unavailable proof; either nonzero blocks installation and completion.

## Materialization proof without installation

```text
python3 scripts/check_agent_grants.py --materialize agents <new-empty-scratch-directory>
```

Inspect only that fresh directory. This validates grants against the live parent inventory. It neither installs nor proves model availability, effective parent sandbox overrides, runtime identity or task quality; record those evidence levels separately.

## Installed-set check

```bash
python3 scripts/check_agent_grants.py --resolved-agents-dir ~/.codex/agents
```

The command reads every `*.toml` in the directory and checks three things. The set of agent names must equal the catalog set, so a missing role or an unmanaged agent file fails. Each role must carry the required `sandbox_mode` declaration. Each role's `mcp_servers` overrides must match the live MCP inventory and the catalog grant for that role. Exit `0` is clean, `1` is findings, and `2` means the checker could not run.

The command does not compare an installed file with its source, so content drift outside the checked fields stays invisible. To detect that drift, run the materialization proof above and compare the scratch files with the installed files. The command does not prove model availability or runtime identity.

## Upgrade contract

Version 5 renames `alaa-implementer-sol` to `alaa-implementer-astra` without a source alias, so update dispatch callers. The installers preserve files absent from the new source, so installation alone does not retire an old role. During an explicitly authorized upgrade, materialize the new wrapper with the supported installer, and archive the old managed wrapper outside the agent discovery directory under that upgrade's target-path authority. Verify the new role and the absence of the retired role before claiming activation.

Since version 4, a report puts the verdict, status or opening outcome first, then configured and requested settings, then separately observed runtime identity. Unknown observations stay unknown, and verdict vocabularies are unchanged. The deep role ID keeps workload and authority compatibility and supplies no model or effort. Review depth and actual task controls are separate decisions. Do not dispatch standard and deep profiles concurrently for one scope.

Report missing, stale or unavailable required roles; there is no silent fallback or implicit installation. A changed MCP inventory requires an authorized rematerialization. Never change global runtime configuration as an installation repair.
