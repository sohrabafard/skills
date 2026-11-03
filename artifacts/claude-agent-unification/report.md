# Claude personal-agent unification

Verified on 2026-11-03. Plan: `beads:alaa-1khq`; final phase: `alaa-1khq.1`.

## Delivered

- `472e2e40` adds the shared personal-agent installer, writer-only migration, compatibility entry point and focused tests.
- `730c74e6` documents the shared installation and preserves the Codex commands.
- The original plugin installer is retained under `_to_delete/20261103-claude-rule-writer-plugin/`, byte-identical to its prior source.
- The prompting guide routes installation to the root guide; the canonical agent definition is unchanged.

## Verification and review

- [Independent focused verification](verification.md): all 17 tests and seven dispatched checks passed.
- [Final gates](final-gates.md): all four root checkers, documentation links and size grades, preserved source/vendor spans, Codex commands and nine shell examples passed.
- Parent correctness review: APPROVED. Instruction reviewer: APPROVED. Security reviewer: PASS.
- Release reviewer: READY-WITH-CONDITIONS; the documentation and scoped migration checks below satisfy its conditions.
- Documentation grades: root guide 99 lines YELLOW; agent guide 66 YELLOW; specialist guide 43 GREEN.
  The root keeps installer data and navigation together; the agent guide keeps installation and recovery in one owner.

## Authorized WSL migration

The parent ran the reviewed installer with `--only alaa-rule-writer --apply` after preview and acceptance.
The personal agent already matched the canonical source and was not rewritten.
The complete legacy plugin moved from `<Claude home>/skills/alaa-rule-writer` to
`<Claude home>/alaa-agent-backups/install-c94wt58t/alaa-rule-writer`.

- Before/after snapshots compared file SHA-256, size, entry type, symlink target and relative path for 600 protected entries.
- All protected personal agents, other plugin trees and selected settings/registry files remained unchanged.
- The archived plugin matches the complete pre-migration snapshot; the original discovery path is absent.
- A fresh `claude plugin list --json` process lists the same other 18 enabled plugins and no rule-writer plugin.
- The personal directory retains 30 agent files, including the canonical writer.
- A subsequent writer-only preview reports only `unchanged`, with no archival action.

Restart an existing Claude session to refresh discovery. Actual model delegation, skill preloading and every other plugin's runtime behavior were not exercised.
The installer guarantees atomic replacement per file, not a whole-pack transaction or hostile-writer/power-loss safety.

## Completion

`IMPLEMENTED`: proven. `MERGE_CANDIDATE`: proven. `RELEASE_CANDIDATE`: not requested. `PUBLISHED`: not requested.
Local installation was explicitly authorized and verified; no push, remote synchronization or publication occurred.
Curation: no additional admitted memory candidates. The requested installation policy is already owned by source and documentation.
