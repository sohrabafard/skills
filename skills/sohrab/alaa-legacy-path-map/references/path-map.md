# Legacy path map

Observed on one WSL host on 2026-11-02 with `test -e` and `ls`. Every row is a lead: step 5 of `SKILL.md` re-tests the target before use. Matching is by whole segments, longest prefix first.

Status values:

- `MAPPED`: the WSL target exists and the cited documents name the same sub-paths.
- `INFERRED`: the WSL target exists, but only a match of contents, not a document, ties it to the legacy path. Open the target, and state in your report that the identity is inferred.
- `NEEDS_CONFIRMATION`: no WSL target was found. Ask the user. Do not guess.

## Mapping

| Legacy prefix | WSL target | Status | Evidence |
|---|---|---|---|
| `D:\Sohrab\Project` | `/home/sohrab/project` | MAPPED (prefix only) | Most frequent drive-letter path in the project documents, agent memory, Hindsight repository, and this repository. These cited sub-paths passed `test -e` under the target: `skills`, `docs`, `agent-memory`, `hindsight`, `alaa-task-hub`, `auth`, `content`, `comment-service`, `client`, `raw`, `alaa-go-chi`, `alaa-filterable-laravel`. These cited sub-paths failed `test -e`: `vk-postman`, `signoz-mcp`, `signoz`, `shecan`, `research`, `mikrotik`, `meet`, `live`, `laravel-base`, `interactive-video`, `dashboard`, `alaa-guard`, `gitlab-ci-local-harness`, and the placeholder `YOUR-PROJECT`. Any other sub-path is unverified. The prefix maps. Each full target still passes step 5 of `SKILL.md`. |
| `D:\Sohrab\hindsight` | `/home/sohrab/project/hindsight` | INFERRED | The Hindsight setup guide under the project documents gives this path as an example install location ("for example") and cds into it and into `scripts`; the target holds `scripts/`. The identity rests on that match. The guide's `codex-home` sub-path failed `test -e`. |
| `D:\Sohrab\hindsight-agent-memory` | `/home/sohrab/project/hindsight` | INFERRED | The README of the target repository cites this name as its own location: `README.md` lines 691 and 697 and `README-fa.md` lines 184 and 190 cd into it and set `codex-home` under it. The target holds `scripts/Initialize-Hindsight.ps1`, which that README runs from there. No directory of this name exists under `/home/sohrab` or `/home/sohrab/project`. The `codex-home` sub-path failed `test -e`. |
| `D:\Sohrab\Worktrees` | none | NEEDS_CONFIRMATION | Cited once, in the project documents' personal memory notes. `git worktree list` in this repository shows the main checkout only; no `Worktrees` directory under `/home/sohrab` or `/home/sohrab/project`. |
| `D:\Sohrab\documents` (for example `D:\Sohrab\documents\agent-reference`) | none | NEEDS_CONFIRMATION | Cited as `D:\\Sohrab\\Documents\\agent-reference` by `hindsight/config.example.json` line 121 (case differs). `/home/sohrab/{documents,Documents}`, `/home/sohrab/project/{documents,Documents}`, `/home/sohrab/project/docs/agent-reference`, and `/home/sohrab/project/agent-reference` failed `test -e`. |
| `D:\hindsight-operations` | none | NEEDS_CONFIRMATION | Operations directory cited by the Hindsight README and its backup scripts. `/home/sohrab/project/hindsight` has `backups/` and `logs/`, but no document equates them with this directory. |
| `D:\wsl-backups` | none | NEEDS_CONFIRMATION | Cited by the WSL install guide as the Windows-side home for exported distro archives. The archives belong on the Windows side by design, so a WSL-native target would be a new decision, not a translation. On the observed host `/mnt/d/wsl-backups` exists and holds Ubuntu `.tar` exports; it is the old-drive copy, readable only when the user names it. |
| `C:\Users\CIT\.claude` | `/home/sohrab/.claude` | MAPPED | Cited as the installed-skills location by agent-memory notes. Tie to this user: the Codex configuration document lists project entries under `c:\users\cit\documents\codex` whose names refer to the Sohrab project directory. The target exists with a `skills/` directory. |
| `C:\Users\CIT\.codex` | `/home/sohrab/.codex` | MAPPED | Cited by agent-memory notes and the Codex configuration document, with the same tie to this user as the row above. The target exists with `skills/` and `memories/`. |
| `C:\Users\CIT` (any other sub-path, including `AppData` and `Documents`) | none | NEEDS_CONFIRMATION | No WSL equivalent found. `/mnt/c/Users/CIT` does not exist on the observed host. |
| `C:\Users\Alaa-AI`, `C:\Users\Alaa`, `C:\Users\alaa`, `C:\Users\operator` | none | NEEDS_CONFIRMATION | Windows profile names of other accounts or machines. No document states that they belong to the user whose WSL home is `/home/sohrab`. |
| `V:\spec-kit\quasar` | none | NEEDS_CONFIRMATION | Cited by a spec-kit prompt as a shell working directory. No `/mnt/v`; no `spec-kit` directory under `/home/sohrab` or `/home/sohrab/project`. The Quasar apps under `/home/sohrab/project/client` and `/home/sohrab/project/entekhabat-front` are not shown to be the same tree. |
| `V:\cache` | none | NEEDS_CONFIRMATION | Cited for Hindsight evaluation temp directories and a tooling-cache scan. No `/mnt/v`; `/home/sohrab/.cache` is the generic user cache and holds no Hindsight directory. |

## Not translated

- `C:\Windows`, `C:\Program Files`, and `C:\Program Files (x86)` locations name Windows-installed software. They have no WSL location.
- A path with a placeholder segment is an illustration, not a location. The placeholders are `to`, `YOUR-PROJECT`, `Synthetic`, `name`, and a bare `...`. Step 1 of `SKILL.md` returns "placeholder, not a location" for such a path.
- Any other drive-letter path is `NEEDS_CONFIRMATION` until `test -e` confirms a target.

## Old-drive mounts on the observed host

`ls /mnt` showed `c`, `d`, `wsl`, `wslg`; there is no `/mnt/v`. `/mnt/c` and `/mnt/d` are 9p mounts of the old Windows drives. `/mnt/d/Sohrab/Project` holds a separate Windows-side tree whose entries differ from `/home/sohrab/project` (for example an `alaa` directory with no counterpart). Treat it as a different copy, never as the translation of `D:\Sohrab\Project`. Other machines may mount nothing under `/mnt`; the table above does not depend on it.
