# Pack finalization: WSL-only, no Basic Memory, Beads-first, no fixture tests

<!-- design-body -->

## Outcome

The first-party pack in `skills/sohrab/` and the checkers in `scripts/` describe exactly one host (WSL Linux, Bash), exactly two memory modes (`local` and `hindsight`), one task authority policy (Beads whenever reachable, `local` plan tasks only when it is not), and no fixture-based test surface. One new skill maps legacy Windows paths to their WSL locations.

## Merge decision (already verified)

Commit `eb0fba92` is a merge whose tree equals the tree of `6376c2b3` (`git rev-parse` of both trees agree). PC1 contributed only a squash of `vendor/skill-temporal-developer` whose tree equals the one already merged on this machine. Nothing is kept or reverted from it.

## Decisions

| # | Decision | Reason |
|---|---|---|
| D1 | WSL is the only host. Delete dual-mode (PowerShell / Git Bash / Windows path) instructions; keep Windows text only where Windows is the subject of the skill's domain (a target platform, not the agent host). | The user migrated; other PCs migrate before use. |
| D2 | One new skill, `alaa-legacy-path-map`, owns old-Windows-path to WSL-path translation for project documents and Hindsight recall. It is the single allowed holder of legacy machine paths. | Documents and Hindsight may still advertise old paths. |
| D3 | Memory modes are `local` and `hindsight`. `store-basic-memory.md`, every Basic Memory command, hook, checker branch, README row and the `vendor/basic-memory` subtree are removed. | The user stops using Basic Memory. |
| D4 | Beads is the task authority whenever `bd` is installed and `bd where` resolves the bound workspace. Otherwise the plan runs `Task store: local`. Once Beads is reachable, every new task in any family, including a previously local one, is registered in Beads. Existing open local tasks may be migrated; a task lives in exactly one store. Beads capabilities are used to the extent the installed `bd` help verifies. | The user's rule 3. Replaces "missing binding blocks, no silent local fallback". |
| D5 | Fixture tests are removed from the project: every `--self-test` mode, every `scripts/fixtures`, `test/fixtures`, `*/scripts/fixtures`, red/green corpora, and every instruction to run them. The validation pack is the root checkers in normal mode plus each skill's own normal-mode validator. Nothing in this run executes a fixture test or `--self-test`. | The user's explicit prohibition. |
| D6 | A fixture-named path that a skill uses at runtime as an asset (a template, a sample consumed by a shipped tool in normal mode) is not a fixture test and stays. | Removing it would break shipped behaviour. |
| D7 | The Crockford Base32 cross-implementation conformance harness stays unmodified and unrun. | `skills/sohrab/AGENTS.md` requires one for multi-implementation wire formats; it is a differential corpus, not a fixture test of a checker. Reported to the user as a retained decision. |
| D8 | Nothing is deleted. Removed files move with `mv` into `_to_delete/20261102-<reason>/` at the repository root; size is confirmed with `ls -la`. Lanes do not touch the Git index; the parent stages and commits. | Repository rule; avoids index lock contention between parallel lanes. |
| D9 | Dated evidence under `outputs/`, `artifacts/`, `test-results/` and `docs/_agent_plans/` is history. It is not rewritten. | Evidence records what happened then. |
| D10 | `~/.claude/rules/*` and other files outside the repository are reported, not edited. | Outside the working tree. |

## Scope lanes (file-disjoint)

Each lane owns the listed paths for all four themes. A lane edits only its own paths, never runs `--self-test` or a fixture, never commits, and reports changed paths, moved paths, checks run and unverified items.

## Acceptance

- The four root checkers and the pack validator exit 0 in normal mode.
- No live file under `skills/sohrab/`, `scripts/`, root docs or `install-skills*` mentions Basic Memory, PowerShell as a host option, or a fixture test.
- `vendor/subtrees.json` and generated doc blocks list no Basic Memory source.
- `alaa-legacy-path-map` is registered in both indexes and passes the validator.
- `alaa-workflow` and both orchestrators state the same Beads-first policy.
- Every moved file is confirmed at its original size under `_to_delete/`.
