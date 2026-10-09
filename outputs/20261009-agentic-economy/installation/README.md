# Authorized custom-agent installation

Date: 2026-10-09. Status: INSTALLED; post-install audit PASS.

The user explicitly requested installation for both runtimes after the source upgrade. The four relevant skill directories in both user homes are existing symbolic links to this repository, so their references and canonical policies required no additional copy.

- Claude: 29 managed Markdown definitions installed into `~/.claude/agents` using the repository's documented copy procedure after source validation.
- Codex: 33 managed definitions installed into `~/.codex/agents` by `Install-AlaaCodexAgents.ps1`; live MCP grants were materialized, not copied from portable templates.
- Both source packs validated. The installed Codex version sentinel is 5.3.0.
- Before replacement, 57 existing managed files/sentinels were backed up under the cache backup root, in `alaa-agent-install/20261009-agentic-economy-01`. Its manifest records original hashes; it also identifies previously absent role names through comparison with the receipt.
- Unrelated agents, rule-writers and runtime configuration were preserved. The receipt records matching before/after configuration hashes; no staging residue remained.

The post-install audit independently read all installed definitions: exact bytes for Claude, exact non-MCP semantics plus live grant validation for Codex. All seven MCP inventory entries matched the recorded fingerprint. Observed CLI versions were Claude Code 2.1.294 and Codex CLI 0.162.0. No CLI upgrade or model request ran.

Evidence: [installation wrapper](install-authorized-agents.ps1), [receipt](receipt.json), and [post-install audit](post-install.json). Managed backup content stays in the local cache, outside the repository; evidence contains hashes only.

Disk installation and grant consistency are verified. Loaded-session discovery, account/model access, serving identity and comparative behavior remain untested. Existing sessions may still expose the earlier loaded definitions; inspect roles in a fresh session before using a new profile.

This follow-up does not alter the source-upgrade snapshot or imply a Git commit, release or publication.
