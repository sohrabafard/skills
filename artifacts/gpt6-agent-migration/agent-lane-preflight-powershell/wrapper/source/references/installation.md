# Authorized Installation and Updates

Activation inspects role availability; it never installs or updates agents. Obtain explicit authorization for target paths before invoking any installer. `install-skills.md` at the repository root owns installation locations; /alaa-prompting-guide owns current runtime discovery and precedence facts.

## Source prerequisites

Keep the complete orchestrator source beside `alaa-prompting-guide`, or pass its root explicitly (`-PolicyRoot` in PowerShell; the third agent-installer argument or second skill-installer argument in shell). Validation fails with exit `2` when the canonical policy owner cannot be loaded. Never substitute a local copy of model policy.

Source TOMLs under `agents/` are transport-neutral templates and cannot be installed by plain copy. All installers validate policy pins, role grants, generated reviewer wrappers, and the source manifest before writing to the target. A source failure leaves the destination untouched. Materialization then resolves the live parent MCP inventory, retains each transport discriminator, applies exact per-role grants, disables unassigned or unknown servers, and validates resolved definitions. Missing inventory or transport information fails closed.

## Explicit agent installation

From this skill directory, after authorization:

```powershell
./scripts/Install-AlaaCodexAgents.ps1
```

```bash
./scripts/install-agents.sh
```

The default target is `~/.codex/agents`. The installer changes only managed agent files, its lock/staging files, and the version/inventory sentinels. It replaces differing managed files and preserves unrelated agents and configuration. Source control owns rollback versions; inspect current runtime discovery before claiming the new roles are active.

To install the complete skill and its agents after authorization, use `scripts/Install-AlaaCodexOrchestrator.ps1` or `scripts/install-skill.sh`. For isolated target inspection, pass `-TargetAgentDirectory` to the complete PowerShell installer or an agent target as the shell installer's third argument. The model-policy owner remains a required separate sibling or explicitly supplied source; these commands do not install it automatically.

## Reproducible source checks

```text
python scripts/render_agents.py --write
python scripts/render_agents.py --check
python scripts/render_agents.py --self-test
python scripts/validate_pack.py
python scripts/check_agent_grants.py --self-test
```

The renderer generates both correctness-review profiles from `assets/reviewer-contract.md`, then the version/hash manifest. `--check` never writes. Exit `0` is clean, `1` is findings/drift, and `2` is unavailable proof; either nonzero blocks installation and completion.

## Installer rejection fixtures

Run `python scripts/test_install_preflight.py --shell powershell --scratch-dir <new-scratch-directory>` and the same command with `--shell bash` and a different new directory after installer changes. Use `--executable` for an explicitly selected shell. Each checks out-of-policy pins, wrapper drift, manifest drift, and a missing policy owner against both installers; failure must precede every destination write. Evidence is retained. Exit `0` is pass, `1` regression, `2` unavailable proof; neither nonzero is a pass. These tests never target user-home paths.

If temporary-directory creation is blocked, run `python scripts/render_agents.py --self-test --self-test-dir <new-evidence-directory>` to retain the same renderer fixtures in an explicitly writable location. The directory must not exist; it is never cleaned automatically.

## Materialization proof without installation

```text
python scripts/check_agent_grants.py --materialize agents <new-empty-scratch-directory>
```

Inspect only that fresh directory. This validates grants against the live parent inventory; it neither installs nor proves model availability, effective parent sandbox overrides, runtime identity, or task quality. Record those evidence levels separately.

## Upgrade contract

Version 4 changes final-report parsing: verdict/status or opening outcome is first, followed by configured/requested settings and separately observed runtime identity. Unknown observations remain unknown. Existing verdict vocabularies remain unchanged. The deep profile is selected by role name because a custom TOML pin overrides caller model/effort values. Do not dispatch standard and deep profiles concurrently for one scope.

Missing, stale, or unavailable required roles must be reported; there is no silent fallback or implicit installation. A changed MCP inventory requires an authorized rematerialization. Never change global runtime configuration as an installation repair.
