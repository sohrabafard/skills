# Preflight evidence

Observed 2026-09-26 in the repository root. Lead owns this evidence directory.

## Workspace

- `git rev-parse --show-toplevel`: expected skills repository.
- `git branch --show-current`: main.
- `git rev-parse HEAD`: 3a62cbb615e0180458ebedd4bc9a0794c17c1e60.
- `git status --short --untracked-files=no`: clean before execution.
- Scoped status: no target skill modifications; three pre-existing untracked files in the selected workflow family.
- Full untracked status warned that retired scratch directories in `_to_delete/20260804-agent-lessons-validation-artifacts/` were inaccessible. Scoped status and tracked status succeeded; no cleanup or permission change.
- Current checkout retained because scopes have clear ownership and integration is not requested. No commit or branch change.

## Prior migration and roles

Researcher `prior_evidence` verified commit 7b22342f651a379e88104f3cd6116a2b7d94ca6b is an ancestor of current HEAD. `docs/gpt6-agent-migration.md` and `docs/claude-model-migration.md` record source migrations; runtime identity and calibration remain unproven. No migration repeated.

The installed Codex definitions for implementer-sol, reviewer, instruction-reviewer, security-reviewer and verifier are byte-identical to their source under `skills/sohrab/alaa-codex-orchestrator/agents/`. Analogous Claude definitions also match. Canonical configured pins: implementer-sol/instruction-reviewer/security-reviewer Astra high; reviewer Sol high; verifier Luna low. Requested lead GPT-6 Astra is separate from observed identity, which is unknown.

Drift record: installed Codex version sentinel reports 3.6.0, source VERSION reports 4.0.0. Owner: orchestrator installation, outside approved source scope. Impact: installed-pack readiness is unproven, but matching selected source definitions and active callable roles allow scoped work. Recovery: separately authorized installer validation/update, not part of this run. Status: open, no installation attempted.

Installed TOMLs retain grant-template markers without explicit MCP server blocks. Native parent sandbox is workspace-write; effective role isolation, MCP restrictions, parent overrides and serving identity cannot be proven here. Agents obey scope restrictions; no enforcement claim.

## Retrieval and environment

- Native text/configuration/Git evidence selected for this known prose/checker surface. CodeGraph directory exists, but no unknown structural source question required it.
- Hindsight official recall tools unavailable; recall failed open. Local Codex memory supplied only the migration commit lead, verified above. No memory writes authorized or performed.
- Official Codex role documentation refreshed: https://learn.chatgpt.com/docs/agent-configuration/subagents (2026-09-26); active host role schema decides callable profiles. This is not serving identity evidence.
- `Get-Command vector,node,python -ErrorAction SilentlyContinue`: node and Python resolved; Vector did not resolve on this PowerShell PATH. Other installed/cached binary availability remains a separate question.
- A read-only PowerShell command failed parsing because a Bash brace-list was used. Cause-specific repair used explicit separate paths/commands and succeeded. No source change or environment repair.

## Authority and proof

No install, dependency upgrade, live discovery, benchmark, provider/cluster/production access, commit, merge, publication, deletion or global configuration change. Public official document reads are permitted. Each writer owns one target skill only; only the lead updates workflow and this directory. Static checks and synthetic fixtures cannot prove installed SigNoz schema, target alert support, real delivery behavior or runtime activation.
