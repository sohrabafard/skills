# Install agents

## Install subagents

Run from the repository root.

```bash
# Claude world — once, applies to every project
mkdir -p ~/.claude/agents
cp skills/sohrab/alaa-cc-orchestrator/agents/*.md ~/.claude/agents/

# Codex world — materialize the live MCP grants before installing role definitions
bash skills/sohrab/alaa-codex-orchestrator/scripts/install-agents.sh
```

Claude source version 5.0.0 keeps `alaa-implementer-opus` and adds `alaa-implementer-fable` with separate admission. Inspect installed roles before a future explicitly authorized update; the wildcard copy above updates present source wrappers but does not prove activation or remove unrelated files. Do not retire Opus. Read `skills/sohrab/alaa-cc-orchestrator/references/model-effort-policy.md` and its routing owner before dispatch. This source update does not install or retire agents on your machine.

The Codex `agents/*.toml` files are transport-neutral templates. The installer resolves the live
MCP inventory, validates each role's exact grant, and installs the materialized definitions. A
plain copy leaves grants unresolved. Installation changes the user-level agents directory and
requires explicit authorization; this guide does not install agents by itself.

For the `alaa-rule-writer`, read [Install the rule-writer agent](50-rule-writer.md) for its Claude
plugin and Codex file procedures.

## Managed implementation and planning profiles

Before an authorized installation, generate and validate each affected orchestrator's standalone wrappers with its `scripts/render_agents.py --write` and aggregate validator. Edit `assets/implementation-contract.md`, `assets/planner-contract.md` or wrapper metadata, never generated bodies; model/effort pins come only from `/alaa-prompting-guide`. Existing reviewer rendering remains managed. Register all new implementation/planner files through the existing install procedure; source generation is not installation. Confirm actual host availability, configured controls, override precedence and grants before dispatch. A requested profile that cannot be realized blocks; do not silently substitute a model or effort.
