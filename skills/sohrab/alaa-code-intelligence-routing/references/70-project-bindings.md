# Project bindings and Serena configuration

Project bindings are always-loaded declarations. Keep them short: invoke the global routing skill, name locally enabled surfaces, preserve the same-worktree requirement, and name native proof. The routing table remains in `/alaa-code-intelligence-routing` in Claude Code or `$alaa-code-intelligence-routing` in Codex.

## Laravel binding source

Use `project-setup/stacks/laravel/.ai/guidelines/30-alaa-code-intelligence.md`. Laravel Boost composes every file under `.ai/guidelines/` into one marker-fenced block in the generated agent instructions, replacing that block in place on each install or update while leaving text outside it untouched. So the binding is authored once in the guidelines directory and never hand-edited inside the generated block, where the next update would overwrite it. Do not maintain parallel hand-edited copies in `AGENTS.md` and `CLAUDE.md`.

## Non-Laravel binding source

Merge `project-setup/stacks/none-laravel/AGENTS.binding.md` once into root `AGENTS.md`. Import that file from `CLAUDE.md` with the supplied bridge when the repository uses that pattern.

## Serena client context

Serena's client context, not only its project file, decides which tools it exposes. A context written
for a coding client withholds the file-read, file-create, directory-listing, and shell tools the client
already owns and sandboxes; a context written for a chat client leaves them enabled. Passing the wrong
one is not cosmetic — it re-exposes duplicate surfaces outside the client's permission model and gives
every lane a second way to reach the filesystem.

Select the context by the client that speaks MCP to the server, not by the window that client runs
inside. A coding client hosted inside a chat application is still the coding client, and the config file
the registration lives in is the reliable signal: a project MCP file belongs to the coding client, and
the chat application's own config file belongs to the chat client. The same machine may hold both
registrations with different contexts, and they do not conflict.

Take the context name from the installed version's list rather than an older guide, and confirm the
effective tool set after activation. Aliases are retired between releases; a context that once resolved
may now resolve elsewhere or fail.

## Serena language-selection policy

The installed Serena version owns the project schema. Generate `.serena/project.yml` first, then merge only the list items from this pack under the language-selection key Serena generated. Existing installations may expose different key names during a migration; never create both keys and never rename a generated key from a stale guide.

A language list selects semantic backends, not every repository file type. Each additional backend may add prerequisites, startup, indexing, memory, and background-process cost.

1. Enable a backend only for a recurring known-symbol, reference, hierarchy, diagnostics, or semantic-edit question.
2. Start with the one material language whose semantics the project needs.
3. Do not add Markdown, YAML, shell, or configuration languages merely for repository coverage.
4. Select a backend on the project's own need, not to mirror another tool. Where a stack skill names a language-server interface of its own, enabling the semantic backend for that language is still correct when the project wants one uniform semantic surface — the stack interface then becomes the fallback for when the backend is absent or unhealthy. Record which one the project expects to answer, so a reader can tell a real gap from a misconfiguration.
5. Add one backend only after naming the missing guarantee, verifying health, and accepting observed resource cost.
6. Remove a backend when its recurring semantic requirement no longer exists.

## Serena `initial_prompt`

Use the single fragment under `project-setup/serena/initial-prompt/`. It invokes this skill and defers owner selection, duplicate-retrieval prevention, fallback, and proof routing to the repository binding and skill. Do not copy the routing table into the prompt.
