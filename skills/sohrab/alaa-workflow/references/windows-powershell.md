# Windows and PowerShell Notes

Use this reference when the task runs in the Codex app on Windows 11 with native PowerShell.

## Operating stance

- Prefer PowerShell-safe examples first.
- Prefer `rg` for fast search when it is available.
- Avoid Unix-only one-liners when the thread is clearly running in native Windows mode.
- If the environment is WSL, containerized Linux, or a remote Linux shell, switch examples accordingly and record that choice in the plan.

## Common command patterns

### Search files and text

```powershell
rg --files
rg "tenant_id|project_id|TODO" .
```

Fallback:

```powershell
Get-ChildItem -Recurse -File
Select-String -Path .\* -Pattern "tenant_id|project_id|TODO" -Recurse
```

### Read file content

```powershell
Get-Content -Raw .\path\to\file.ext
```

### Create directories safely

```powershell
New-Item -ItemType Directory -Force -Path .\docs\_agent_plans | Out-Null
New-Item -ItemType Directory -Force -Path .\docs\agents | Out-Null
New-Item -ItemType Directory -Force -Path .\.codex\state | Out-Null
```

### Validate JSON state files

```powershell
Get-Content -Raw .\.codex\state\task.json | ConvertFrom-Json | Out-Null
```

### Append a log line

```powershell
Add-Content -Path .\docs\agents\20260405-143015_task-state.md -Value "- 2026-04-05T14:35:10Z - Validation passed"
```

## Artifact bootstrap examples

### Create a parent plan, phase prompts, continuation state, and machine state

```powershell
python .\.agents\skills\alaa-workflow\scripts\init_workflow_files.py --task "refine tenant-aware queue retry flow" --with-state
```

By default this creates:

- `docs/_agent_plans/<stem>.md`
- `docs/_agent_plans/<stem>__phase-prompts.md`
- `docs/agents/<stem>-state.md`
- `.codex/state/<stem>.json` when `--with-state` is set

### Create a child lane plan and state next to an existing parent plan

```powershell
python .\.agents\skills\alaa-workflow\scripts\init_workflow_files.py --task "frontend lane for queue status UI" --lane frontend --parent-plan .\docs\_agent_plans\20260405-143015_queue-retry-flow.md --with-state
```

### Validate workflow artifacts

```powershell
python .\.agents\skills\alaa-workflow\scripts\validate_workflow_files.py --plan auto --state auto
```

### Validate a specific plan and its phase prompt pack

```powershell
python .\.agents\skills\alaa-workflow\scripts\validate_workflow_files.py --plan .\docs\_agent_plans\20260405-143015_queue-retry-flow.md --state .\.codex\state\20260405-143015_queue-retry-flow.json --phase-prompts auto --continuation auto
```

## Worktree examples

The plan should fix branch names, not worktree directory names. The user chooses the directory.

```powershell
git worktree add ..\my-chosen-ui-worktree -b feat/example-ui-lane
git worktree add ..\my-chosen-api-worktree -b feat/example-api-lane
```

Integration later happens from the parent branch after the user has reviewed or committed lane branches.

## Quoting guidance

- Use single quotes for literal PowerShell strings when interpolation is not needed.
- Use double quotes only when interpolation or escape sequences matter.
- Pass full paths directly to Python scripts instead of wrapping complex shell pipelines around them.

## Windows-specific judgment calls

- In the Codex app on Windows, native PowerShell is a first-class path and should be the default for local threads.
- If you are using the Codex CLI or IDE extension on Windows and the repository expects Linux-first tooling, WSL may be the smoother execution path. Record that choice in the plan.
- If the repository clearly expects Linux tooling only, record that fact in the plan before switching to WSL or container-based commands.
- If a command changes files broadly, prefer a script or narrow patch over shell-heavy rewrite commands.
- If a validation command is slow or noisy, run it at phase boundaries and record the summary in state instead of pasting raw output.
