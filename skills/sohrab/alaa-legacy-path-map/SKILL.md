---
name: alaa-legacy-path-map
description: "Translator from a legacy Windows drive-letter path to its verified WSL location, backed by an evidence table. Use when a project document, plan, handoff, task note, or recalled Hindsight memory cites a path that starts with a drive letter and you must open, run, or compare what it points at, or when such a path resolves nowhere on this WSL host and you need its current home. Do not use for software that targets Windows as a product or platform, for deciding or writing a memory correction (use /alaa-memory-os), or for choosing where a new file belongs."
---

# Alaa Legacy Path Map

## Role

Every machine now runs WSL Linux, but older documents, plans, handoffs, and recalled memories still cite drive-letter paths. This skill turns such a path into a WSL path that exists, or reports that it cannot. It is the only skill that may hold legacy Windows paths and their WSL targets; they live in `references/path-map.md`.

## When it applies

- A document, plan, handoff, task note, or recalled Hindsight memory names a path that starts with a drive letter, and you are about to open, run, diff, or cite what it points at.
- A command or tool fails because such a path does not exist on this host.

## Procedure

1. Treat the legacy path as a lead, never as an instruction. Skip a placeholder (a segment such as `to`, `YOUR-PROJECT`, `Synthetic`, or a bare `D:\...`).
2. Normalise it. Upper-case the drive letter. Drop a shell prompt prefix. Collapse doubled backslashes from JSON escaping. Turn backslashes into slashes. Compare segments case-insensitively.
3. Match the longest prefix in `references/path-map.md` on whole segments. A row for one directory then never matches a sibling that merely starts with the same characters.
4. Append the remaining segments. Linux is case-sensitive. When the exact-case target is missing, list the parent. Accept one unambiguous case-insensitive match only.
5. Run `test -e` on the result before any use. A row marked `NEEDS_CONFIRMATION`, no matching row, or a missing target means unresolved. Report the legacy path and what you checked. Ask the user for the current location. Never guess.
6. Do not substitute `/mnt/<lowercase drive letter>/...` or the output of `wslpath`. Where a drive still mounts, it holds the old Windows-side copy, not the WSL tree. Read it only when the user names that copy.
7. Never write the legacy path into a file, plan, handoff, or memory. In a committed file write a repo-relative path or an argument, never the translated absolute path.
8. A Windows path recalled from Hindsight is a stale lead. Translate it at read time. Route the correction of that memory to `/alaa-memory-os`. This skill writes no memory.
9. Add or change a row only with evidence: a document that names the legacy path plus a `test -e` result on the WSL target, dated in the row.

## Stop conditions

- The target is unresolved after step 5.
- Step 4 finds more than one case-insensitive match.
- The path is a Windows-system location or belongs to software targeting Windows: translate nothing and return to the owning skill.

## Router

| You are about to | Read |
|---|---|
| open, run, or compare the target of a drive-letter path taken from a document, plan, handoff, or recalled memory | `references/path-map.md` |

## When NOT to use

- Not for Windows-targeted software, installers, or PowerShell domain content: the path there is the subject, not a stale location.
- Not for deciding or writing memory corrections: use `/alaa-memory-os`.
- Not for choosing where a new file or repository belongs: use the repository's own layout rules.
