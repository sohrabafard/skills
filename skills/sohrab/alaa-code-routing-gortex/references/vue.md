# Vue integration: current gap and bounded implementation plan

**Full Vue integration through Gortex is not ready in the reviewed release.**
Installing official language-server packages, initializing a server, or extracting
symbols from an SFC's script block does not close the gap. This reference owns the
Vue capability boundary and proposed adapter acceptance. Installation and configuration belong to operator documentation, outside this skill.

## Reviewed baseline and checkout evidence

On 2026-10-22, source inspection covered Gortex
[v0.64.8](https://github.com/zzet/gortex/tree/v0.64.8)
(`af1438b6d84a2c870572a28ec62a21b94fda98fa`) and main
`76c080e56da3547f2b464522fd6acbe0accaa25e`. Official Vue Language Tools' stable
release was [v3.3.13](https://github.com/vuejs/language-tools/tree/v3.3.13).
These identify evidence, not permanent installation pins. Recheck the selected
release's contracts before changing the integration status.

The inspected Windows `client` checkout had the following facts; none proves the
WSL checkout has installed dependencies or generated configuration:

- `<repo>/package.json` and `<repo>/pnpm-lock.yaml`: Vue 3.5.43, TypeScript 6.0.3,
  vue-tsc 3.3.13, Quasar app-vite 3.10.2; 17 package manifests under `packages/`.
- `<repo>/tsconfig.json` extends `.quasar/tsconfig.json` and excludes
  `packages/*/src`. The generated config includes the Vue Router Volar plugins
  `vue-router/volar/sfc-route-blocks` and `vue-router/volar/sfc-typed-router`.
- `<repo>/packages/design-system-vue/tsconfig.json` and
  `<repo>/packages/player-vue/tsconfig.json` include their own `src/**/*.vue` and
  TypeScript sources. Both contained SFCs. Root-app success is not package coverage.

The official stack is `@vue/language-server`, `@vue/typescript-plugin`, the actual
checkout's compatible TypeScript SDK, and a companion that implements the selected
Vue LS protocol. Keep the Vue server/plugin on a compatible release pair and record
both versions. Do not upgrade the application's lockfile, compiler plugins or
TypeScript to make a global language server install. Check companion Node engines
through [the provider reference](lsp.md).

## Eight required links in the integration

| Requirement | Evidence in the reviewed Gortex release | Remaining requirement |
|---|---|---|
| 1. Register and route `.vue` | The static registry has no `.vue` extension or Vue spec. The MCP LSP path returns before custom-provider fallback when no spec exists. | Register the extension and correct `vue` language ID, and connect both graph enrichment and LSP action dispatch. YAML alone is insufficient. |
| 2. Initialize Vue and TypeScript companion | Known-provider overrides pass command/args/env; no coordinated Vue pair or per-worktree plugin/SDK setup is wired. | Initialize both participants with the target checkout's SDK, official plugin location, Vue language acceptance and matching protocol. |
| 3. Forward private TypeScript messages | Generic JSON-RPC handlers exist; the provider does not install Vue's private forwarding handlers. | Correlate `tsserver/request` with the correct companion, return `tsserver/response`, and bound timeout/cancellation per workspace. |
| 4. Synchronize buffers | Gortex has single-provider open/change/close and version tracking. It does not fan Vue buffers out to a companion pair. | Synchronize content/version/open/close on both sides, including external file changes, simulation rollback and reconnect. |
| 5. Select monorepo project | No Vue-specific project resolution is connected. | Resolve the correct tsconfig through the companion, including generated Quasar config and each SFC package. Invalidate config/dependency changes. |
| 6. Map virtual positions | No end-to-end Vue semantic route is connected. Script extraction is not virtual-code mapping. | Use the official stack's source mapping and preserve original `.vue` URIs/ranges at the Gortex boundary; reject unmappable edits. |
| 7. Definition, references, diagnostics, rename | `.vue` fails the registry gate for the inspected LSP action path. No complete template/cross-file behavior is established. | Exercise original-source template and `.ts`/`.vue` operations and expose only mutations Gortex can guard and apply safely. |
| 8. Isolate concurrent worktrees | Gortex has provider/workspace keys and checkout views, but no Vue compound-provider state. | Key both child servers, project caches, pending requests and buffers to the actual worktree; prove no cross-view reads or writes. |

Evidence owners:
[Gortex registry](https://github.com/zzet/gortex/blob/v0.64.8/internal/semantic/lsp/registry.go),
[provider registration](https://github.com/zzet/gortex/blob/v0.64.8/internal/serverstack/shared_server.go),
[LSP tool dispatch](https://github.com/zzet/gortex/blob/v0.64.8/internal/mcp/tools_lsp.go),
[provider lifecycle](https://github.com/zzet/gortex/blob/v0.64.8/internal/semantic/lsp/provider.go),
[Vue server protocol](https://github.com/vuejs/language-tools/blob/v3.3.13/packages/language-server/lib/server.ts).

## Protocol and version traps

Vue LS 3.3.13 emits `tsserver/request` with the flat payload
`[requestId, command, args]` and consumes `tsserver/response` as `[id, result]`.
Its project selection asks the companion for `_vue:projectInfo`, then reads the
reported config and Vue compiler options. The Node TypeScript companion needs the
Vue plugin registered with its package location and `languages: ["vue"]`; its
`tsserver.path` must refer to the worktree's TypeScript library or `tsserver.js`.
See the [Vue server source](https://github.com/vuejs/language-tools/blob/v3.3.13/packages/language-server/lib/server.ts)
and [TypeScript LS initialization contract](https://github.com/typescript-language-server/typescript-language-server/blob/v6.0.2/docs/configuration.md).

[Serena's Vue adapter](https://github.com/oraios/serena/blob/abb0a0f01b94bc8050086f0fb860077d17730324/src/solidlsp/language_servers/vue_language_server.py)
is an architectural reference for dual-server initialization, indexing/synchronizing
Vue files, routing requests and cleanup. It is not a dependency to install. Its
reviewed defaults target an older Vue stack, and its notification handler uses
nested request/response arrays. Do not copy that payload shape into a 3.3.13
adapter: use the selected Vue server's source and protocol fixtures. Its existence
also does not establish support for this monorepo or for every mutation.

Three distinct technologies must remain separate:

- [Vue PR 6129](https://github.com/vuejs/language-tools/pull/6129) was merged and
  changes the language-tools repository's build/test TypeScript dependency to a
  native bridge. It does not make bare Gortex `tsgo --lsp --stdio` a Vue companion.
- Gortex's `tsgo` provider has higher default TS/JS precedence than the Node
  provider. A future Vue pair must select its tested companion explicitly, rather
  than accepting whichever executable is first available.
- [Vue PR 6170](https://github.com/vuejs/language-tools/pull/6170) was open/unmerged
  at inspection. It proposes Vue v4, TypeScript 7.1 content mappers and a different
  API-session connection. It changes compiler configuration and replaces vue-tsc.
  This is neither the installed client's TS 6 contract nor a drop-in v3 forwarding
  fix. Do not migrate the client as part of global LSP setup.

## Bounded future adapter plan

This is a proposed separately authorized engineering task. Do not implement a fork,
bridge or patches merely to finish workstation setup.

1. Add a Vue provider specification and action routing in Gortex's registry/shared
   server layer. Define explicit selection when `.ts` and `.vue` participate in
   the same project. Keep the existing non-Vue provider behavior covered.
2. Add a compound provider under `internal/semantic/lsp/` that owns the Vue and
   TypeScript processes, SDK/plugin resolution and private message forwarding.
   Reuse the router's actual workspace identity; never use process-global mutable
   SDK paths. Budget both processes and report capacity refusal without an
   incompatible fallback.
3. Extend document/project lifecycle handling for the pair. Synchronize revisions,
   file events and generated-config changes; preserve per-worktree buffers and
   source-position mapping. Reconnect must replay state or mark results unavailable.
4. Connect supported definition/reference/diagnostic operations and guarded
   WorkspaceEdit handling to the existing MCP/mutation path. Filter/validate edit
   destinations against the resolved worktree; never bypass receipts/hash guards
   with a direct companion write. Unsupported refactors remain explicit.
5. Ship focused protocol/conformance tests, then the acceptance scenarios below.
   Keep installation/configuration examples behind the supported status until
   those gates pass. Prefer an upstream contribution over an indefinitely carried
   local patch when the owner approves implementation.

Maintenance includes a tested Vue/plugin/TypeScript/Node/companion matrix, private
protocol changes, virtual-document mapping, watcher/reconnect races and process
budget accounting. These are coupled integration costs, not a one-line registry
entry. Any native-TypeScript/v4 path needs its own compatibility review.

## Deferred acceptance and current fallback

A future integration is accepted only after all of these work through Gortex, with
same-checkout native checks and no unrelated-file edits:

- Navigate from template component use to its definition; cover imported
  composables, props and emits.
- Find references across two SFCs and in both directions between `.ts` and `.vue`.
- Introduce a known template type error and observe its diagnostic; correct it and
  observe the diagnostic disappear without a daemon restart.
- Preview and apply a supported rename across relevant uses; preserve an unrelated
  symbol with the same spelling. Verify original SFC edit positions and receipts.
- Cover the root application and both SFC packages, including Vue Router compiler
  plugins and generated Quasar configuration from that same checkout.
- Run two worktrees with divergent branches/buffers concurrently. Verify distinct
  results, correct mutation targets, stale-hash rejection and bounded lifecycle
  behavior through idle eviction, capacity refusal and reconnect.

Until then, use bounded native source inspection for unresolved Vue questions and
the checkout's own Vue/TypeScript checks for proof. Gortex may still contribute
supported structural evidence elsewhere, but label SFC/template reference coverage
incomplete. Native checks, an IDE result or a standalone Vue LSP session do not
prove Gortex integration. No final agent acceptance tests are run during setup
preparation; their execution is deferred until installation is complete.
