# Store Adapter: Basic Memory

Mechanics for the file-backed store. Everything here dies with the store; nothing here is policy. The policy
is in `SKILL.md`, `references/knowledge-shape.md`, and `references/drift-management.md`.

## Version pin

`basic-memory` **0.22.1**, published 2026-06-13. Re-derive before trusting it:

```bash
curl -s https://pypi.org/pypi/basic-memory/json \
  | python3 -c "import json,sys;d=json.load(sys.stdin);v=d['info']['version'];print(v,d['releases'][v][0]['upload_time_iso_8601'])"
```

PyPI is the authoritative surface. The GitHub Releases page trails it, so a pin taken from Releases reads
stale.

## `bm status --wait` is a compatibility no-op; stop treating it as a barrier

On 0.22.1 `--wait` still blocks until indexing settles. On the development branch it does not: the command
prints `status --wait is a compatibility no-op for event-based project indexing`, `--wait` is documented as
`Compatibility flag; returns the current project-index observation`, and `--timeout` as
`Compatibility option for --wait`. Re-derive:

```bash
curl -s https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/src/basic_memory/cli/commands/status.py \
  | grep -n "compatibility"
```

Consequences, and these are the rules:

- Never treat the exit code of `bm status --wait` as a health signal. On a release where the flag is a no-op
  it returns immediately and successfully whether or not indexing has finished, so a script that gates on it
  is asserting nothing.
- Never use it as a barrier before reading a note you just wrote. Indexing is event-driven; the barrier that
  actually works is reading the note back and checking it contains what you wrote.
- The three shipped store scripts call `bm status` for its report only. None of them fails on it, and none of
  them should be changed to.

## Commands

```powershell
bm reindex -p alaa-memory
bm doctor
bm schema validate architecture --project alaa-memory
bm schema diff architecture --project alaa-memory
bm format --project alaa-memory
bm orphans --project alaa-memory
bm status --project alaa-memory
```

`basic-memory sync` does not exist. It was removed, and `bm reindex -p PROJECT` replaced it — `reindex` lives
in `commands/db.py`, not in a module of its own, which is why it is hard to find. Confirm the whole command
surface at a tag:

```bash
curl -s https://raw.githubusercontent.com/basicmachines-co/basic-memory/v0.22.1/src/basic_memory/cli/commands/__init__.py
```

A schema-versus-usage report from `bm schema diff` is metadata maintenance, not contract drift. Do not open a
drift record for it.

## Search and context

```powershell
bm tool search-notes "notification command contract" --hybrid --project alaa-memory
bm tool search-notes --status needs_review --project alaa-memory
bm tool build-context memory://alaa-notification-contracts --project alaa-memory
bm tool read-note memory://alaa-notification-contracts --include-frontmatter --project alaa-memory
bm tool recent-activity --timeframe 7d --project alaa-memory
```

Individual sub-flags on `bm tool` move between releases. Confirm the ones you rely on with
`bm tool search-notes --help` before writing them into a script, rather than copying them from here.

Unlike the server-backed store, this one *can* filter on arbitrary frontmatter fields — that is what
`vendor/basic-memory/memory-metadata-search/SKILL.md` is for. So a lifecycle field such as `drift_status` is
queryable here. That does not move the drift registry into the store: the reason it lives in git is the
enforced audit trail, not queryability, and a registry that moves stores whenever the query surface changes is
a registry nobody can rely on. See `references/drift-management.md`.

Search on a vault of a few thousand notes has been reported upstream as taking several seconds to over ten,
which is why `SKILL.md` sets a five-second recall budget and makes recall fail open: on this store the budget
is expected to be exceeded, and the fail-open path is the normal path, not the exception. Background:
`https://github.com/basicmachines-co/basic-memory/issues/980`. That issue's current state was not re-checked
when this file was written; check it before citing it as open.

## The MCP transport binds to every interface by default

```powershell
bm mcp --project alaa-memory --transport streamable-http --host 127.0.0.1 --port 8000
```

`--host 127.0.0.1` is load-bearing and must not be dropped. The default is `0.0.0.0`, documented as
`use 0.0.0.0 to allow external connections`, and the endpoint carries **no authentication**. Omitting the flag
therefore publishes unauthenticated read and write access to the whole vault to every host on the network.
Re-derive the default:

```bash
curl -s https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/src/basic_memory/cli/commands/mcp.py \
  | grep -n -A2 "host: str"
```

Bind beyond loopback only behind something that authenticates, and treat that as an exception requiring
`/alaa-security-review` (`$alaa-security-review`). The default transport is `stdio`, which has no listening
socket and is the right choice unless a remote client genuinely needs HTTP.

For a Codex CLI client over stdio:

```powershell
codex mcp add basic-memory bash -c "uvx basic-memory mcp --project alaa-memory"
```

## Concurrency

The store is files on a disk, so two agents writing the same note is last-writer-wins with no warning and no
merge. There is no locking to rely on. The practical rules: one agent owns a note during a task; an agent that
must update a note it did not read this session re-reads it immediately before writing; and a note written by
a hook goes to a capture directory with a unique filename rather than to an existing note.

## Vendored pack

The pack is an upstream subtree under `vendor/basic-memory` and is never edited. Route into it for mechanics:
`references/skill-boundaries.md` lists all of its skills, their paths, and which are gated.

## Windows is the target platform

The shipped scripts run on Windows PowerShell and on PowerShell 7. Two consequences that have already caused
defects here: `Set-Content -Encoding UTF8` writes a byte-order mark on Windows PowerShell 5.1 and none on
PowerShell 7, and a mark immediately before a YAML frontmatter delimiter can break the parse — the shipped
scripts write frontmatter through a mark-less UTF-8 encoder instead. Path exclusion globs written with
backslashes match nothing on a non-Windows host, so the checkers normalise separators before comparing.
