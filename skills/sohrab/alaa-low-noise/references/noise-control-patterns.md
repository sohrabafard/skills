# Noise Control Patterns

## Table of contents

- Search and excerpt patterns
- Diff and reporting patterns
- Large-log capture patterns
- PowerShell notes
- Bash notes
- When the user wants raw output

## Search and excerpt patterns

Prefer discovery in this order:

1. Search or inventory.
2. Bounded excerpt near the match.
3. Full-file read only if required for safe editing.
4. Concise summary.

Prefer:

- `rg -n "pattern" <paths>`
- `rg -n -C 3 "pattern" <paths>`
- changed-file lists instead of full folder dumps
- counts plus a short file list when an audit is broad

Avoid by default:

- full-file dumps to prove you inspected a file
- full directory trees for generated output
- repeated reads of the same file without new evidence

## Diff and reporting patterns

Prefer these reporting shapes before raw diff output:

- `git status --short`
- `git diff --stat`
- `git diff --name-only`
- `git diff -- <path>` for the one file that matters

Default final reporting should answer:

- what changed
- why it changed
- what was validated
- what remains risky or blocked
- where any saved artifacts live

Avoid pasting a repo-wide unified diff unless the user explicitly asked for it.

## Large-log capture patterns

When validation or diagnostics are long, keep them repo-local and summarize the important evidence.

Typical flow:

1. Create or reuse a repo-local artifact directory.
2. Redirect the full command output there.
3. Read back only the tail or the failing slice.
4. Mention the path and the key outcome.

Keep durable artifacts only if they help the user inspect or resume. Remove throwaway artifacts before finishing when cleanup is safe.

## PowerShell notes

Use bounded reads and quiet redirects.

Examples:

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
- Prefer `Select-Object -First` or `-Last` instead of dumping full content.
- Use terse commands such as `git status --short` and `git diff --stat` before any detailed diff.

## Bash notes

Examples:

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

If the user explicitly wants the full log, full diff, or full file contents, obey that request.

Still improve the handoff quality when possible:

- say whether the output is file-local or repo-wide
- identify the most relevant section first
- avoid mixing unrelated raw outputs together
