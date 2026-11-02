# Checkers And Hooks

Two kinds of script ship with this skill, and they obey opposite exit-code contracts. Confusing them is the
failure this file exists to prevent. The host is WSL Linux: checkers run with `python3`, hooks with `bash`.

## The checker contract

Every checker exits:

- `0` — ran to completion, no findings.
- `1` — ran to completion, findings to report.
- `2` — could not run: the vault path does not resolve, a required tool is absent, input is unreadable.

The third code is the one that matters. A checker whose "could not run" is indistinguishable from its "clean"
is worse than no checker at all, because a gate built on it reads a missing tool as a pass and keeps reporting
green while checking nothing. A `2` is a failed gate, never a pass.

Run the checker in normal mode against the real vault and read `--help` first. Report the observed exit code.
Set `SKILL_DIR` to the installed skill directory. Run one command per subcommand.

```bash
python3 "$SKILL_DIR/scripts/alaa_memory_vault_check.py" --help
python3 "$SKILL_DIR/scripts/alaa_memory_vault_check.py" linkcheck --vault-path "$ALAA_MEMORY_VAULT"
python3 "$SKILL_DIR/scripts/alaa_memory_vault_check.py" staleness --vault-path "$ALAA_MEMORY_VAULT"
```

The checker reads strict UTF-8 only. It accepts a freshness stamp only as `YYYY-MM-DD` with an optional time suffix.
It reports any other form as an unparseable date.
An unreadable directory or an undecodable note exits `2`.
`/alaa-testing-strategy` owns test design beyond this rule.

## Checker inventory

One script, `scripts/alaa_memory_vault_check.py`, with two subcommands. Both read note frontmatter and the file
system, call no store command, and change nothing except an optional `--out-file` report. The vault root is
`--vault-path`, else `ALAA_MEMORY_VAULT`; an invalid selected path exits `2` and never falls through to another
vault. No machine-specific default is supplied.

| Subcommand | Asserts | Bound |
|---|---|---|
| `linkcheck` | Every wiki link resolves to a note filename, title, alias, or permalink. With `--strict-hygiene`, every note also has an incoming link and a `## Relations` section; without it only a broken link is a finding, because a correct, findable orphan is no defect and a checker that exits `1` on every real vault gets switched off. | One name-to-note index, then one constant-time lookup per link: linear in notes plus links. |
| `staleness` | Every path in `canonical_source_paths` still resolves, `last_verified` (or `last_curated`) is an ISO date no older than `--max-age-days` (default 90), and a note of a source-derived type carries both fields. Relative source paths resolve against `--source-root`, else `ALAA_SOURCE_ROOT`, else the vault. | Linear in notes; one existence test per recorded path. |

The staleness checker makes the staleness rule enforceable: `canonical_source_paths` and `last_verified` were
required fields with nothing checking them, which is the same as advisory. Both subcommands skip `.obsidian/`
and `archive/`.

## Hook scripts are exempt, and inverting their exit codes breaks them

`scripts/precompact_checkpoint.sh` and `scripts/session_start_context.sh` are Claude Code hooks. Their
protocol contradicts the checker contract:

- `0` — success. Output handling is event-specific; never assume JSON reaches the agent.
- `2` — **blocking error**. Stdout and JSON are ignored; stderr reaches the agent as an error.
- anything else, including `1` — non-blocking error. Execution continues; stderr appears as a hook error
  notice to the user.

A hook must exit `0` on success and never exit `2` unless it intends to block. Both shipped hooks always
exit `0`. Do not "fix" them to `0/1/2`. Confirm semantics at `https://code.claude.com/docs/en/hooks` before
changing either script.

Official hook semantics were checked at https://code.claude.com/docs/en/hooks on 2026-10-12
America/Los_Angeles (UTC date 2026-10-13): an access date, not a publication date. `SessionStart` stdout
enters session context; the event cannot block. `PreCompact` discards `systemMessage` and `continue`;
compatibility JSON emission proves no model reminder delivery. Refresh event-specific semantics before
changing or registering hooks.

`precompact_checkpoint.sh` is a nonwriting compatibility entrypoint that exits 0. It reads no payload,
transcript or vault, writes no vault/checkpoint and invokes no adapter. Its emitted owner pointer
proves no continuity; /alaa-workflow must record continuity proactively through its own admitted artifacts.

`session_start_context.sh` reads repository drift counts and emits conditional owner pointers. It copies
no recall budgets, drift decisions, note policy or active workflow state. A missing/unreadable drift path
is unknown, not zero drift. If the task touches counted contracts, inspect their records through
`references/drift-management.md` before planning. Keep this hook fast; it runs every session.

## Registering the hooks

Editing a settings file is a shared-configuration change. Do not apply it on the user's behalf:
`/alaa-controlled-ops` owns that action, and the user applies it themselves. Replace the placeholder path with
the absolute path of the installed skill's `scripts/` directory.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          { "type": "command", "command": "bash /path/to/session_start_context.sh" }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "manual",
        "hooks": [
          { "type": "command", "command": "bash /path/to/precompact_checkpoint.sh" }
        ]
      }
    ]
  }
}
```

`PreCompact` matches on `manual` or `auto`; register both entries to cover automatic compaction, which is the
case that actually loses context. Confirm the current matcher values and the settings shape against the hooks
documentation above before applying, because this schema is upstream and moves.

## Script rules

- Write frontmatter without a byte-order mark: a mark immediately before the opening `---` can break the YAML
  parse on the reader that later loads the note.
- For an authorized capture outside these nonwriting hooks, use a unique filename; timestamps alone can
  collide within a second and overwrite evidence.
- Do not create a temporary directory inside the repository, and do not locate files by walking a fixed number
  of parent directories from the script.
