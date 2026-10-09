# Custom agent installation receipt

Status: **partial**. The updated Claude orchestrator agents and Codex agents are installed and hash checked. Claude `alaa-rule-writer` remains blocked because its current owner requires plugin packaging, while this checkout/runtime has no matching plugin package or supported local build/install entrypoint. The existing loose Claude wrapper was preserved and is not represented as current.

## Managed installation scope

- Claude Code user agent directory: `CLAUDE_AGENT_HOME` (`CLAUDE_AGENT_HOME`). Installed 29 files directly from `skills/sohrab/alaa-cc-orchestrator/agents/*.md`. The independent parent postcheck confirmed all 29 match source bytes.
- Codex user agent directory: `CODEX_AGENT_HOME` (`CODEX_AGENT_HOME`). Installed 33 orchestrator roles through `Install-AlaaCodexAgents.ps1` materialization and the one documented `alaa-rule-writer.toml` file. A fresh materialization postcheck matched all 33 installed orchestrator files; the separate rule-writer matches its source.
- The installer reported 33 resolved Codex agents across 7 live MCP servers. It did not modify runtime settings files.
- Before writes, 63 differing existing managed files were backed up: 29 Claude and 34 Codex. Backup root: `CACHE_ROOT/codex-agent-install-backups/20261009`. The directory also contains one baseline metadata file with source identities and settings hashes. No secret values were recorded.

## Verification

- `python -B skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py` — PASS, 29 agents, version 5.3.0.
- `python -B skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_grants.py` — PASS, 29 roles.
- `python -B skills/sohrab/alaa-prompting-guide/scripts/check_rule_writer_grants.py` — PASS.
- `skills/sohrab/alaa-codex-orchestrator/scripts/Install-AlaaCodexAgents.ps1` — PASS, 33 installed/updated after validating 33 templates and live materialized grants.
- `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_grants.py --materialize skills/sohrab/alaa-codex-orchestrator/agents CACHE_ROOT/codex-agent-install-postcheck-20261009` — PASS; all 33 materialized hashes match installed files.
- `python -B skills/sohrab/alaa-prompting-guide/scripts/check_codex_model_policy.py --agent-root "$env:USERPROFILE\.codex\agents"` — PASS, 34 model-neutral agents.
- `python -B skills/sohrab/alaa-prompting-guide/scripts/check_claude_model_policy.py` against the 29 installed source roles — PASS.
- The same Claude policy checker over the entire user agent directory — FAIL only for the pre-existing `alaa-rule-writer.md`: it has executable model and effort defaults. It was left unchanged because the current rule requires plugin-root packaging and forbids installing this wrapper into the loose user agent directory.
- `claude --version` reported 2.1.294. `codex --version` reported 0.162.0 with non-fatal access warnings while cleaning/creating temporary PATH aliases.
- Parent independent read-only postcheck confirmed 34 Codex files and 29 Claude files match expected installed definitions.

Settings hashes were unchanged:

| File | Before SHA-256 | After SHA-256 |
|---|---|---|
| `CODEX_HOME/config.toml` | `05425792c8f69f7f0df2e263f86877afcb576f1c50132b03f68b41f776d0055c` | `05425792c8f69f7f0df2e263f86877afcb576f1c50132b03f68b41f776d0055c` |
| `CLAUDE_HOME/settings.json` | `89df3a00cec3ef582fe369bea3390974b58239dab957168c36c46ecc9f600d6f` | `89df3a00cec3ef582fe369bea3390974b58239dab957168c36c46ecc9f600d6f` |

Source identity: Git HEAD `7b51799c428bcdc15a09ad145112b5cd42bef1e8`; prior source evidence `outputs/20261009-task-model-routing/source-final.json`, SHA-256 `85aaa99663ee63e28f3cd606328d55d84e23995b9c8ae5cfedf98feac15bdbce`. Per-file source and installed hashes are in [receipt.json](receipt.json), with portable path prefixes and backup paths.

## Claude rule-writer blocker

Current `/alaa-prompting-guide` says Claude `alaa-rule-writer` ships from a plugin-root `agents/` directory and explicitly forbids a `~/.claude/agents` wrapper ([SKILL.md](../../skills/sohrab/alaa-prompting-guide/SKILL.md)). `install-skills.md` likewise says “nothing to run” for Claude and that rebuilding/reinstalling the plugin is the update path (lines 230–234). The bounded source lookup found no plugin manifest/build/install artifact for this agent in the scoped checkout or user plugin store. Therefore no supported updated Claude package could be installed, and the older active loose file remains a policy conflict until its plugin owner supplies a package path.

Installed files do not prove this running chat reloaded them or that a future task dispatch uses the configured model. Those runtime outcomes remain unverified.



