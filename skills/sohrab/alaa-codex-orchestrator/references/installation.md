# Authorized Installation and Updates

Activation inspects role availability; it never installs or updates agents. Obtain explicit authorization for target paths before invoking any installer. `install-skills.md` at the repository root owns installation locations.

## Source prerequisites

- The sibling `alaa-testing-strategy` must be available with its `references/100-test-execution.md`, `references/110-execution-resources.md`, `references/120-result-classification.md` and canonical runners. A missing owner or runner blocks the work and grants no installation authority; a companion installation needs its own authorization.
- Keep the complete orchestrator source beside `alaa-prompting-guide`, or pass its root explicitly: the third agent-installer argument or the second skill-installer argument. Validation fails with exit `2` when the canonical policy owner cannot be loaded. Never substitute a local copy of model policy.
- The agent installer accepts only its own resolved canonical `agents/` directory and rejects an alternate source directory before any target write.
- Source TOMLs under `agents/` are transport-neutral templates that a plain copy cannot install. Before the first target write, every installer validates the model-neutral policy roles, role grants, generated reviewer wrappers and the source manifest; a source failure leaves the destination untouched. Materialization then resolves the live parent MCP inventory, keeps each transport discriminator, applies exact per-role grants, disables unassigned or unknown servers, and validates the resolved definitions. Missing inventory or transport information fails closed.

## Explicit agent installation

From this skill directory, after authorization:

```bash
./scripts/install-agents.sh
```

The default target is `~/.codex/agents`. The installer changes only managed agent files, its lock and staging files, and the version and inventory sentinels. It replaces differing managed files and preserves unrelated agents and configuration. Inspect current runtime discovery before claiming the new roles are active.

To install the complete skill and its agents after authorization, use `scripts/install-skill.sh`. For isolated target inspection, pass an agent target as its third argument. Neither command installs the model-policy owner.

## Reproducible source checks

```text
python3 scripts/render_agents.py --write
python3 scripts/render_agents.py --check
python3 scripts/validate_pack.py
```

The renderer writes both correctness-review profiles from `assets/reviewer-contract.md`, the implementation and planner wrappers from their contracts and `assets/profile-wrappers.json`, and the version and hash manifest. `--check` never writes. Exit `0` is clean, `1` is findings or drift, and `2` is unavailable proof; either nonzero blocks installation and completion.

## Materialization proof without installation

```text
python3 scripts/check_agent_grants.py --materialize agents <new-empty-scratch-directory>
```

Inspect only that fresh directory. This validates grants against the live parent inventory. It neither installs nor proves model availability, effective parent sandbox overrides, runtime identity or task quality.

## Installed-set check

```bash
python3 scripts/check_agent_grants.py --resolved-agents-dir ~/.codex/agents
```

The command reads every `*.toml` in the directory and checks three things:

- the set of agent names equals the catalog set, so a missing role or an unmanaged agent file fails;
- each role carries the required `sandbox_mode` declaration;
- each role's `mcp_servers` overrides match the live MCP inventory and the catalog grant for that role.

Exit `0` is clean, `1` is findings, and `2` means the checker could not run. The command does not compare an installed file with its source. To detect content drift outside the checked fields, run the materialization proof above and compare the scratch files with the installed files.

## Upgrade contract

- The installers preserve files absent from the new source, so installation alone does not retire a renamed or removed role. During an explicitly authorized upgrade, materialize the new wrapper with the supported installer, and archive the old managed wrapper outside the agent discovery directory under that upgrade's target-path authority. Verify the new role and the absence of the retired role before claiming activation.
- Report missing, stale or unavailable required roles; there is no silent fallback or implicit installation.
- A changed MCP inventory requires an authorized rematerialization.
- Never change global runtime configuration as an installation repair.
