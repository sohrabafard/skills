# Noise Control Patterns

Concrete patterns for both levers. The first two sections govern what enters the context window; the rest govern what gets printed and where bulk output lives. Patterns are runtime-neutral unless a section names a runtime.

## Table of contents

- Discovery and bounded reads
- Runtime notes: Claude Code and Codex
- Diff and reporting patterns
- Large-log capture patterns
- PowerShell notes
- Bash notes
- When the user wants raw output

## Discovery and bounded reads

Work down this order and stop at the first step that answers the question:

1. Search or inventory to locate the relevant path, symbol, or line range.
2. Read the bounded excerpt around the match.
3. Read the full file only when safe editing requires the whole file.
4. Summarize the result, not the material.

Prefer:

- `rg -n "pattern" <paths>` to locate before reading.
- `rg -n -C 3 "pattern" <paths>` when the surrounding lines decide the answer.
- `rg -c "pattern" <paths>` or a file list when the question is "how widespread is this."
- a changed-file list instead of a full folder dump.
- one well-chosen query instead of several exploratory ones.

Avoid by default:

- full-file dumps to prove a file was inspected;
- full directory trees, especially of generated output;
- re-reading a file with no new reason — an edit you made, a failed check, or a changed hypothesis is a reason, confirming what is already in context is not;
- pulling a large result into the window when a count, a path, or a slice answers the question, since that result is re-read on every later turn.

## Runtime notes: Claude Code and Codex

**Claude Code.** Prefer the file and search tools over shelling out: a search tool returning matching paths or matching lines is cheaper and more structured than `rg` piped through the terminal, and a read with an explicit offset and limit is cheaper than `cat` plus mental filtering. Read only the range you need. Dispatch independent searches in a single turn so they run concurrently. When a question needs a wide sweep across many files, delegate it to a subagent and require the return to be findings or paths rather than excerpts — the sweep then costs the subagent's context instead of the parent's.

**Codex.** Discovery mostly runs through the shell, so boundedness has to be expressed in the command itself: scope every search to real paths, keep `-C` context small, and pipe through `head`/`tail` or `Select-Object` rather than emitting whole files. Codex-specific sandbox, refresh, locking, quoting, and command-length failures belong to `$alaa-codex-runtime-ops`, which has no Claude Code equivalent; retry only the essential failed work afterward, serially and with bounded output.

## Diff and reporting patterns

Prefer these reporting shapes before raw diff output:

- `git status --short`
- `git diff --stat`
- `git diff --name-only`
- `git diff -- <path>` for the one file that matters

Default final reporting answers what changed, why it changed, what was validated, what remains risky or blocked, and where any saved artifacts live. Do not paste a repository-wide unified diff unless the user asked for it.

## Large-log capture patterns

When validation or diagnostics are long, keep the bulk out of both the transcript and the context window:

1. Create or reuse a repo-local artifact directory.
2. Redirect the full command output there.
3. Read back only the tail or the failing slice.
4. Report the key outcome and the path.

Keep durable artifacts only when they help the user inspect or resume. Remove throwaway artifacts before finishing when cleanup is safe.

## PowerShell notes

```powershell
rg -n -C 3 "MyPattern" src tests
Get-Content .\path\file.txt -TotalCount 120
Get-Content .\path\file.txt | Select-Object -Last 80
```

```powershell
New-Item -ItemType Directory -Force artifacts | Out-Null
pnpm test *> artifacts\test.log
Get-Content artifacts\test.log | Select-Object -Last 80
```

Notes:

- `*>` redirects all PowerShell streams to one file.
- Prefer `Select-Object -First` or `-Last` over dumping full content.
- Use `git status --short` and `git diff --stat` before any detailed diff.

## Bash notes

```bash
rg -n -C 3 "MyPattern" src tests
sed -n '1,120p' path/file.txt
tail -n 80 path/file.txt
```

```bash
mkdir -p artifacts
pnpm test > artifacts/test.log 2>&1
tail -n 80 artifacts/test.log
```

Notes:

- Prefer `tail`, bounded `sed`, or focused `rg -C` over full `cat` output.
- Use `git diff -- path/to/file` before showing larger diffs.

## When the user wants raw output

If the user explicitly wants the full log, full diff, or full file contents, obey that request. Still improve the handoff: say whether the output is file-local or repository-wide, identify the most relevant section first, and do not mix unrelated raw outputs together.

## Caveats

Command flags and tool names here are the common cases for `rg`, `git`, PowerShell, and Bash, not a portable guarantee — verify against the shell and versions actually installed before scripting them. Tool-level guidance for Claude Code describes the general shape of its file and search tools rather than a fixed parameter surface, which changes between releases. `$alaa-codex-runtime-ops` is Codex-only by design; do not look for a Claude Code counterpart.
