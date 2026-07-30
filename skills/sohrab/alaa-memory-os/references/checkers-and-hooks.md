# Checkers And Hooks

Two kinds of script ship with this skill, and they obey opposite exit-code contracts. Confusing them is the
failure this file exists to prevent.

## The checker contract

Every checker exits:

- `0` — ran to completion, no findings.
- `1` — ran to completion, findings to report.
- `2` — could not run: the vault path does not resolve, a required tool is absent, input is unreadable.

The third code is the one that matters. A checker whose "could not run" is indistinguishable from its "clean"
is worse than no checker at all, because a gate built on it reads a missing tool as a pass and keeps reporting
green while checking nothing. Both shipped checkers previously failed this in both directions at once, which is
why the contract is stated here rather than assumed.

## Every assertion has a red fixture

A checker that has only ever been observed to pass is decoration. Before any checker is allowed to report
clean, each assertion it makes must be shown to fail on an input that violates it, in a fixture committed
beside the script.

- `test/fixtures/red-vault/` — violates every assertion at once: a broken wiki link, a note nothing links to, a
  note with no Relations section, a recorded source path that does not exist, and a `last_verified` far past
  the threshold.
- `test/fixtures/green-vault/` — satisfies every assertion.

Each checker takes `-SelfTest`, which runs it against both fixtures and asserts the exit codes rather than the
report text. Report text is prose and drifts; the exit code is the contract.

`test/run-tests.ps1` runs every self-test. A target that exits `2` is recorded **BLOCKED, not FAIL**, and the
harness then exits `2` — because "the checker could not run" and "the checker found a problem" call for
different human actions, and collapsing them loses the distinction the contract just created.
`/alaa-testing-strategy` (`$alaa-testing-strategy`) owns test design beyond this rule.

## Checker inventory

| Script | Asserts | Bound |
|---|---|---|
| `scripts/alaa_obsidian_linkcheck.ps1` | Every wiki link resolves to a note filename, title, alias, or permalink; every note has an incoming link; every note has a Relations section. | Builds one name-to-note index, then one constant-time lookup per link: linear in total links. The earlier version scanned every note for every link, which is quadratic and unusable on a vault of a few thousand notes. |
| `scripts/alaa_memory_staleness.ps1` | Every path in `canonical_source_paths` still resolves, and `last_verified` is no older than the threshold. | Linear in notes; one file-existence test per recorded path. |

The staleness checker is the one that makes the staleness rule enforceable. `canonical_source_paths` and
`last_verified` were required fields with nothing checking them, which is the same as advisory.

## Store-side scripts

`scripts/alaa_memory_health.ps1`, `scripts/alaa_memory_reindex.ps1`, and `scripts/alaa_memory_post_task.ps1`
are store-specific and thin. They follow the same contract, with one discrimination that the earlier versions
collapsed: **a missing store binary or an unreachable store exits `2`; a store that ran and reported a problem
exits `1`.** Previously every path used `throw`, so both exited `1` and a CI gate could not tell "no tool
installed" from "validation failed".

They share `scripts/_common.ps1`, which owns vault-root resolution, boundary validation on that path, store
invocation that returns only an exit code, and the exit mapping. Store invocation is the reason the module
exists: a PowerShell function returns its whole output stream, so a helper that runs a command and then
`return $code` hands the caller an array of output lines with the code appended. Comparing that array against
zero is a filter, not a comparison, and it is truthy whenever the command printed anything — which made the
earlier health check report failure on every clean run.

## Hook scripts are exempt, and inverting their exit codes breaks them

`scripts/precompact_checkpoint.ps1` and `scripts/session_start_context.ps1` are Claude Code hooks. The hook
protocol assigns its own meanings, and they contradict the checker contract:

- `0` — success. Stdout is parsed for the hook's JSON output; JSON is only processed on exit 0.
- `2` — **blocking error**. Stdout and JSON are ignored and stderr is fed back to the agent as an error.
- anything else, including `1` — non-blocking error. Execution continues and stderr surfaces as a hook error
  notice to the user.

So a hook must exit `0` on success, and must never exit `2` unless it intends to block. Both shipped hooks
always exit `0`, including from their error handler. Do not "fix" them to `0/1/2`. Confirm the semantics at
`https://code.claude.com/docs/en/hooks` before changing either script.

For `SessionStart` specifically: stdout is added to the session context — it is one of the few events where
that happens rather than going to the debug log — and the event cannot block. Keep the hook fast, because it
runs on every session.

## Registering the hooks

These two scripts previously shipped with no registration path at all, so nobody could install them from the
skill. The snippets below are the missing half.

Editing a settings file is a shared-configuration change. Do not apply it on the user's behalf:
`/alaa-controlled-ops` (`$alaa-controlled-ops`) owns that action, and the user applies it themselves.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          { "type": "command", "command": "pwsh -NoProfile -File C:\\path\\to\\session_start_context.ps1" }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "manual",
        "hooks": [
          { "type": "command", "command": "pwsh -NoProfile -File C:\\path\\to\\precompact_checkpoint.ps1" }
        ]
      }
    ]
  }
}
```

`PreCompact` matches on `manual` or `auto`; register both entries to cover automatic compaction, which is the
case that actually loses context. Confirm the current matcher values and the settings shape against the hooks
documentation above before applying, because this schema is upstream and moves.

## Windows is the target, and these are the traps already hit here

- Write frontmatter with a mark-less UTF-8 encoder. `Set-Content -Encoding UTF8` emits a byte-order mark on
  Windows PowerShell 5.1 and none on PowerShell 7, and a mark immediately before the opening `---` can break
  the YAML parse on the reader that later loads the note.
- Normalise path separators before comparing. Exclusion globs written with backslashes match nothing on a
  non-Windows host, which silently widens the checked set instead of failing.
- Never build a filename from a timestamp alone. Two hook firings inside the same second produce the same name
  and one silently overwrites the other; the shipped hook appends a short random suffix.
- Do not create a temporary directory inside the repository, and do not locate files by walking a fixed number
  of parent directories from the script.
