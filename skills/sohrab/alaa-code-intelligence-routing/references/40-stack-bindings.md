# Stack and capability fit

Select an operation from the effective inventory and the active backend, never from a remembered name. An optional, beta or newly documented capability is unusable until it is exposed, supported and authorized.

CodeGraph needs a matching supported index. Serena needs the language backend configured. Boost applies only to Laravel and is optional there; PHP without Laravel uses the source and native routes. `references/10-routing-contract.md` owns eligibility, absence and fallback.

## Laravel

Boost owns the framework and runtime questions below, with or without Serena. It does not replace symbol semantics: for PHP diagnostics and navigation, use *PHP, including Laravel*. CodeGraph and Serena prove no framework convention, runtime registration or database state.

Installed Boost groups that read:

- Application info, or an existing metadata resource: installed PHP and Laravel versions, packages and models. A lockfile alone shows only the intended resolution.
- Search docs: framework convention and package guidance. Establish the installed versions first.
- Route inventory, if exposed, and the absolute-URL operation: registered routes and one resolved URL. A resolved URL does not prove route registration; the native route list observes it.
- Connection inventory and schema: the live schema. It must observe the intended environment and database. Migrations show intent only.
- Last error, log entries and browser logs: verify the application, session and time window, and redact sensitive values.

Installed Boost groups with effects:

- Database query: the tool guarantees no read-only access. Verify the installed read-only control, the driver and the task scope. Inspect the query, its credentials and its effects.
- Artisan command execution: the command inventory authorizes no execution. Boot and dependency effects apply.
- Tinker or code execution: it can mutate, whatever the expression looks like. Some versions gate tinker separately; verify the installed gate.
- Rule recording: it writes agent instructions. That is separate authorized authoring, not evidence retrieval.
- Resource commands for guidelines or skills: setup or update effects, never a fallback or proof.
- An upgrade or simplification prompt: advice inside the authorized change scope, not authority or proof.

Never infer harmlessness from a tool name or annotation: inspect what the operation does.

A framework symbol that Serena misses can lie in vendor or excluded source outside its coverage. Verify inclusion first. Otherwise keep the result unknown and, for a guidance question, select the documentation owner for the installed version.

### Independent failure domains

Classify the failed operation, not the whole provider.

- **Docs transport or service fails:** application metadata stays valid. Use version-correct official documentation.
- **Application boot fails:** docs and the directly readable installed package metadata stay valid. Another boot-dependent Artisan command is no independent fallback. Static source gives intent only. Block a live application claim that has no equivalent observation.
- **Database fails, or the connection or environment is wrong:** docs and application evidence stay valid. A live schema or query claim needs an equivalent authorized observation of the intended database. Migrations do not recover it.

When application info is unavailable, read the installed package metadata directly, and keep it apart from lockfile intent.

## CodeGraph specialized groups

- Every available CodeGraph tool is eligible within the role's grant, with or without Serena: explore, node or source, query or search, files, callers, callees, impact, context, affected tests, status or another verified operation. No explore-only allowlist exists.
- A CLI-only operation needs no MCP failure first. Neither explore nor a focused operation needs a call to the other first.
- For a tool that MCP does not list, use its CLI equivalent or report the missing surface. Change no configuration.
- Suggested affected tests select candidates. Only native execution proves that tests passed.
- Init, uninit, index, sync, unlock, daemon control, install, uninstall, upgrade and telemetry changes are lifecycle or configuration effects. Each needs its own explicit authority and is never an automatic fallback, except the lane-local `init` and `sync` that `SKILL.md` *Operation card* grants.

## Claude Code language-service tool

`SKILL.md` *Operation card* owns when to use the built-in `LSP` tool.

- It works wherever a server is configured for the file type, and it needs no Serena.
- It answers definition, references, implementations, call hierarchy, hover, document symbols and workspace symbols at a file position. Document symbols can supply that position.
- It reads only: no rename and no edit.
- Its workspace is the session's project root. For a file outside that root it resolves file-local facts only, and cross-file names stay unresolved. Check that returned paths lie inside your worktree before you rely on them.
- A role whose definition lists its tools reaches `LSP` only when that list names it.

## Serena specialized groups

- Writes: symbol-body, insert and rename operations, and backend-specific move, inline and safe-delete operations. They fall under `references/10-routing-contract.md` *Mutation uncertainty*. A safety-oriented name establishes neither authorization nor complete coverage.
- Lifecycle effects: activation, onboarding, language-server restart, project removal and dashboard opening. Check their side effects and your authority first. To identify the active project, context, modes and tools, read the configuration or the manual instructions.
- Shell, REPL and debug evaluation carry execution authority.
- An external-project query needs an explicitly named authorized target and an independently verified identity.
- Provider memories belong to the task's memory owner, not to this skill.
- Serena file and search tools add no semantic guarantee to the native ones.

## Go

Installed gopls answers definition, reference, implementation, call-hierarchy and diagnostic questions through its CLI or a connected language service, without Serena. Verify the operation against the module or workspace, the build tags, the toolchain and the file version. A configured Serena gopls backend and direct gopls are alternatives: use one. `references/45-native-tools.md` owns invocation, cost limits and dependency recipes. Routing authorizes no backend activation.

## PHP, including Laravel

- PHPantom's `analyze` CLI gives native diagnostics for symbol resolution and type coverage, without Serena or an LSP client. It does not run PHPStan and proves no complete references.
- Definition, hover and references need an exposed LSP operation or a verified equivalent, not `analyze`.
- Installed `fix`, `format` and `move` write. Each needs the matching authorized change, coverage checks and mutation reconciliation.
- The repository recipes keep their PHPStan, Pest, PHPUnit and Pint obligations.

## Python

The `pyright` CLI gives type checking and diagnostics for the configured Python environment. Navigation and rename need a connected `pyright-langserver` client or bridge that exposes them. Type checking proves neither complete references nor test success.

## Vue and Quasar

Vue or TypeScript semantics use Serena only with the correct configured backend. Add no backend merely because TypeScript exists. Authorized browser observation owns runtime UI facts.

## Other source

For unsupported or unindexed code, record the lost graph and semantic guarantees.
