# Language providers and capability limits

This reference teaches agents to identify the active provider and its capability limits.
Installation, configuration changes and rollback belong to operator documentation.
Vue's compound-provider gap and acceptance contract live in [Vue integration](vue.md).

## Evidence boundary

Source inspection on 2026-10-22 covered Gortex release
[v0.64.8](https://github.com/zzet/gortex/releases/tag/v0.64.8), commit
`af1438b6d84a2c870572a28ec62a21b94fda98fa`, and main
`76c080e56da3547f2b464522fd6acbe0accaa25e`. They have the same relevant
registry/override restrictions described below. These are reviewed baselines, not
permanent installation pins. Resolve the current suitable release at execution;
reinspect changed interfaces before using a newer one. No provider was installed,
initialized or exercised by this source review.

## Selected providers

Enable only languages needed by tracked repositories. A provider entry selects a
logical registry identity; it does not install that executable. The checked
[Gortex registry](https://github.com/zzet/gortex/blob/v0.64.8/internal/semantic/lsp/registry.go)
contains these invocation contracts:

| Language | Logical provider | Executable and argument contract | Acquisition/package boundary |
|---|---|---|---|
| Go | `gopls` | `gopls` | Reuse the existing Go installation; verify it before considering an upgrade. |
| PHP | `phpactor` with explicit override | `phpantom_lsp --stdio` | PHPantom release binary; do not install Phpactor as the selected implementation. |
| Python | `pyright` | `pyright-langserver --stdio` | npm package `pyright`, through pnpm/Nexus. |
| Lua | `lua-language-server` | `lua-language-server` | LuaLS complete platform archive, including its resource files. |
| Bash | `bash-language-server` | `bash-language-server start` | npm package `bash-language-server`, through pnpm/Nexus. |
| YAML | `yaml-language-server` | `yaml-language-server --stdio` | npm package `yaml-language-server`, through pnpm/Nexus. |
| JSON/JSONC | `vscode-json-language-server` | `vscode-json-language-server --stdio` | npm package `vscode-langservers-extracted`, through pnpm/Nexus. |
| TypeScript/JavaScript | `typescript-language-server` | `typescript-language-server --stdio` | Node companion, using the target checkout's TypeScript SDK. This alone adds no Vue integration. |
| Vue | No built-in `.vue` registry provider in the reviewed Gortex release | Official Vue LS plus a coordinated TypeScript companion | Follow the integration gap in [Vue integration](vue.md); do not claim that installing binaries enables Gortex Vue semantics. |

Basedpyright is an alternative to evaluate, not an additional default. If selected
later, verify its executable, configuration and diagnostic behavior, then deliberately
override the known Python provider. Installing another server does not prove Gortex
will select it, and silently falling back to another implementation is not acceptance.

Upstream package metadata inspected on 2026-10-22 reported pyright 1.1.414,
bash-language-server 5.8.1, yaml-language-server 2.0.0,
vscode-langservers-extracted 4.10.0 and LuaLS 3.19.2. These values establish review
provenance only; check the effective installed versions before relying on these capabilities. In particular,
[typescript-language-server 6.0.2](https://registry.npmjs.org/typescript-language-server/6.0.2)
requires Node >=22.22.2. The previously observed WSL Node 22.22.1 does not satisfy
that requirement. An engine mismatch must stop installation; do not disable engine
checks or change application dependencies to accommodate a global LSP.

## PHPantom connection contract

Reviewed PHPantom release:
[0.11.1](https://github.com/PHPantom-dev/phpantom_lsp/releases/tag/0.11.1), commit
`1756b1f920c1290d4c4fdd4d2c902fad53a75cd3`. Its Linux release archive retains the
`unknown-linux-gnu` filename convention even though its installation documentation
states that the Linux binary is statically linked. Choose the architecture-specific
release asset and verify the published digest; do not derive an internal mirror URL.

The provider override has four relevant values: `name` remains `phpactor`, `enabled`
is true, `command` is the installed PHPantom executable's absolute Linux path, and
`args` is the nonempty list containing `--stdio`. The executable is PHPantom, not
Phpactor; the logical name retains the registered `.php` route. Inspect effective runtime configuration to confirm this mapping; this skill does not provision it.

Why the nonempty argument matters: Gortex's
[`SpecWithOverridesConnect`](https://github.com/zzet/gortex/blob/v0.64.8/internal/semantic/lsp/registry.go)
replaces inherited arguments only when the replacement list has elements.
`args: []` leaves Phpactor's `language-server` argument in place. PHPantom's
[CLI source](https://github.com/PHPantom-dev/phpantom_lsp/blob/0.11.1/src/main.rs)
accepts `--stdio` explicitly. A new arbitrary logical name such as `phpantom` does
not register extensions in the static router; changing the executable of the known
PHP spec is the supported configuration route being proposed.

The reviewed provider setup passes `rootUri` and workspace folders from the resolved
workspace root. PHPantom's
[startup handler](https://github.com/PHPantom-dev/phpantom_lsp/blob/0.11.1/src/backend/startup.rs)
reads that root and advertises definition, type definition, implementation,
references, call hierarchy, prepare-rename/rename and code actions. It supports pull
diagnostics for clients advertising that capability and push diagnostics otherwise.
No special initialization options are needed for its basic stdio connection.

These are server capabilities, not proof that every corresponding operation is
exposed by Gortex or safe for a specific PHP construct. Check the selected Gortex
operation's language restrictions separately. Never route a PHP rename through a
Go-only refactor merely because PHPantom advertises rename. Native Laravel/PHP
checks remain the proof for the application's behavior.

Each worktree must get its own actual root, Composer metadata, autoload files and
vendor dependencies. Missing dependencies limit resolution. Do not substitute a
sibling checkout's vendor tree or initialize every provider against the main
checkout. PHPantom syntax/type observations do not establish the state of the
Docker-hosted Laravel application; runtime evidence belongs to Boost in that
application's execution environment.

## Router, lifecycle and degradation

The reviewed [shared server setup](https://github.com/zzet/gortex/blob/v0.64.8/internal/serverstack/shared_server.go)
registers known specs and auto-registers available providers unless disabled.
Declaring a short enabled list is therefore not necessarily an allowlist. Use the
effective disabled-provider policy to avoid activating unrelated
servers found on PATH. `tsgo` normally has higher precedence than the Node
TypeScript provider; it is not an interchangeable Vue companion.

Gortex's router keys provider workspaces by spec and workspace. LSP processes may
therefore multiply by active provider/worktree even though the graph daemon is
shared. Initialization, LRU/idle eviction and checkout admission are separate
lifecycle layers; inspect effective workspace capacity and idle settings when diagnosing degraded results.
Eviction, missing executables, incomplete dependencies or capacity denial must be
reported as degraded/incomplete evidence, not as no references or no diagnostics.

The reviewed [LSP tool dispatch](https://github.com/zzet/gortex/blob/v0.64.8/internal/mcp/tools_lsp.go)
checks the static extension registry before selecting a provider. A missing route
produces `no_lsp_for`; an arbitrary custom provider entry cannot bypass that early
return. Generic document open/change/close handling exists in the
[provider implementation](https://github.com/zzet/gortex/blob/v0.64.8/internal/semantic/lsp/provider.go),
but this does not coordinate two servers or make a missing extension route work.

Provider acceptance must distinguish executable discovery, initialization,
capability advertisement, a real symbol/reference answer, a guarded supported
write and same-checkout native proof. Record each observed layer; do not promote a
successful version command or handshake to end-to-end capability evidence.
