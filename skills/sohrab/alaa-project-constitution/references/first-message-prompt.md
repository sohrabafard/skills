# Minimal First Message

Use this from the project root. The detailed workflow lives in
`constitution-template.md` and the optional `alaa-project-constitution` skill.

If the skill is installed, prepend the matching line:

- Codex: `Use $alaa-project-constitution for this task.`
- Claude Code: `Use /alaa-project-constitution for this task.`

```text
From the project root, create or update `CONSTITUTION.md` from
`constitution-template.md`.

If `CONSTITUTION.md` already exists, read it first and preserve valid rules, concerns,
stable IDs, and history. Then read the complete template and follow its self-contained
workflow exactly, including repository-evidence discovery, module pruning, both writing
passes, thin `AGENTS.md`/`CLAUDE.md` bindings, and final validation.

Do not invent facts; use structured TODOs for missing evidence. Do not change application
code, dependencies, deployments, shared systems, or Git history.

Optional project context, priority sources, or owner decisions:
<none, or add details here>

Final response: mode/version, included and removed modules, meaningful changes, unresolved
TODOs, binding status, files changed, and validation result.
```
