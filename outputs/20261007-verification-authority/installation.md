# Authorized agent installation

After the source-only milestone, the user explicitly authorized agent installation, commit and push on 2026-10-07. This record supersedes the earlier report's installation limitation; its source-validation evidence remains unchanged.

- Codex: the official PowerShell installer validated source, materialized grants against seven live MCP servers, and updated all 23 managed definitions under the user's `.codex/agents`. Post-copy validation passed for the 23 managed installed payloads; every role body, model/effort and sandbox field matches source.
- Claude: copied the two changed implementer definitions through the documented install path under the user's `.claude/agents`; all 22 managed file hashes match source, with 20 already current. Existing unchanged source/grant validation was cited.
- The separately owned `alaa-rule-writer` was preserved. An initial post-install check over the entire Codex directory rejected that extra role; checking the exact managed roster in isolated scratch passed. No contract or gate was weakened.
- Source manifest remains `73f0652e419f6e9fb57e6958308ea363a4c621d01dde24b6d94b3c3b9d61b107`. No product test or previously valid focused gate was repeated.
- Remote preflight confirmed `origin/main` still matched base `683a0bd08d76a43fabe9951f65dcc27929628273`. The sandbox's Windows credential failure was resolved by one authorized outside-sandbox read retry.
- Installation proves installed file contents and resolved grants, not live activation, serving-model identity or future instruction compliance.

Commit and push are authorized follow-up operations; their immutable identity is the resulting Git commit and remote ref, reported after the remote check. No tag or release was requested.
