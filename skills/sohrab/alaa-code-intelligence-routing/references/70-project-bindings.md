# Project bindings and Serena configuration

Project bindings are always-loaded declarations. Keep them short: invoke the global routing skill, name locally enabled surfaces, preserve the same-worktree requirement, and name native proof. The routing table remains in `/alaa-code-intelligence-routing` in Claude Code or `$alaa-code-intelligence-routing` in Codex.

## Laravel binding source

Use `project-setup/stacks/laravel/.ai/guidelines/30-alaa-code-intelligence.md`. Laravel Boost copies that source into generated agent instructions. Do not maintain parallel hand-edited copies in `AGENTS.md` and `CLAUDE.md`.

## Non-Laravel binding source

Merge `project-setup/stacks/non-laravel/AGENTS.binding.md` once into root `AGENTS.md`. Import that file from `CLAUDE.md` with the supplied bridge when the repository uses that pattern.

## Serena language-selection policy

The installed Serena version owns the project schema. Generate `.serena/project.yml` first, then merge only the list items from this pack under the language-selection key Serena generated. Existing installations may expose different key names during a migration; never create both keys and never rename a generated key from a stale guide.

A language list selects semantic backends, not every repository file type. Each additional backend may add prerequisites, startup, indexing, memory, and background-process cost.

1. Enable a backend only for a recurring known-symbol, reference, hierarchy, diagnostics, or semantic-edit question.
2. Start with the one material language whose semantics the project needs.
3. Do not add Markdown, YAML, shell, or configuration languages merely for repository coverage.
4. Do not add a backend that duplicates a semantic owner named by the stack skill; `/alaa-golang` or `$alaa-golang`, for example, owns Go semantics through gopls.
5. Add one backend only after naming the missing guarantee, verifying health, and accepting observed resource cost.
6. Remove a backend when its recurring semantic requirement no longer exists.

## Serena `initial_prompt`

Use the single fragment under `project-setup/serena/initial-prompt/`. It invokes this skill and defers owner selection, duplicate-retrieval prevention, fallback, and proof routing to the repository binding and skill. Do not copy the routing table into the prompt.
