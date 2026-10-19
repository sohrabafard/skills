from pathlib import Path
import re

ROOT = Path('skills/sohrab')
changed = {}

def read(skill, name):
    p = ROOT / skill / name
    return p, changed.get(p, p.read_text(encoding='utf-8'))

def replace(skill, name, old, new):
    p, s = read(skill, name)
    assert s.count(old) == 1, (str(p), old[:100], s.count(old))
    changed[p] = s.replace(old, new)

F = 'alaa-frontend-developer'
Q = 'alaa-quasar-app-vite-v3'
V = 'alaa-vue-typescript-clean-code'
D = 'alaa-frontend-devops'
U = 'alaa-ui-ux-design-system'

# A19: use the already canonical output boundary, not an input-only prohibition.
replace(F, 'references/25-frontend-security.md',
'''- `v-html` on a value that any user, tenant or third party can influence is prohibited. Render as text, or
  sanitize with a maintained library at the single boundary where the value enters the app — never in
  the template, and never twice.''',
'''- Render user-, tenant- or third-party-controlled content as text. If raw HTML is required, use the
  single sanctioned rendering path in `alaa-security-review references/25-browser-trust-and-output.md`
  under Raw HTML: exactly one path. Sanitize immediately before render; input sanitization alone cannot
  cover other writers or later sanitizer changes. The Vue binding is
  `alaa-vue-typescript-clean-code references/72-frontend-security-binding.md`.''')

# A20: both local network-only assertions yield to the established strategy owner.
replace(F, 'references/30-pwa-sw-and-offline.md',
'''Navigation HTML is network-only; offline navigation falls back to a controlled offline page; runtime
caching is narrowly scoped; the update flow uses `SKIP_WAITING`, `clientsClaim()` and exactly one reload
on `controllerchange`; a custom InjectManifest worker keeps exactly one `self.__WB_MANIFEST`. The
authoritative statement of those five mechanisms is the Quasar skill's file above — this list exists so
you can tell when a diff has left the contract. Repo-local rules win where they differ.''',
'''Before assessing navigation, caching, update lifecycle or InjectManifest behavior, read
`alaa-quasar-app-vite-v3 references/30-service-worker-excellence.md`: section 1 owns the navigation
strategy, and sections 4 and 8 own lifecycle and wiring. Compare the diff with that contract; repo-local
rules win where they differ.''')
replace(F, 'references/30-pwa-sw-and-offline.md',
'''emits. Either navigation HTML is being cached when it must be network-only, or the deploy removed the
previous build's assets. The frontend half is the caching strategy; the retention half is''',
'''emits. Compare navigation caching with the strategy selected under Quasar reference 30 section 1 above;
also check whether deployment removed the previous build's assets. The frontend half is the caching
strategy; the retention half is''')

# A22: one explicit exception owner, rather than a wildcard exemption.
replace(F, 'references/48-config-and-environment.md',
'''- Never read `import.meta.env` from more than one module. One typed config module reads it; everything
  else imports from that module.''',
'''- Project-injected values are read through one typed config module; consumers import its validated
  values. Framework-owned build constants may be read directly where needed: Vite's `BASE_URL`, `MODE`,
  `DEV`, `PROD`, `SSR`, and Quasar constants verified against the installed app-vite line. This is no
  blanket `QUASAR_*` exemption: custom `defineEnv` and prefixed project values still use the module.
  Keep member reads static for build replacement. Sources: [Vite env](https://vite.dev/guide/env-and-mode)
  and [Quasar env](https://quasar.dev/quasar-cli-vite/handling-process-env/), read: 2026-10-18.''')
replace(F, 'references/48-config-and-environment.md',
'''The app's public or base path has exactly one source, read through the config module and validated at
boot. Asset paths derive from it; no second copy is written in a component, a router, a service worker''',
'''The app's public or base path has exactly one source. A framework-generated `BASE_URL` may be read
directly under the exception above; a project/runtime base is read through the config module and validated
at boot. Asset paths derive from that source; no second copy is written in a component, a router, a service worker''')
replace(V, 'references/50-quasar-vite-pinia-contract.md',
'''- Keep environment access behind one typed config module rather than reading `import.meta.env` across the
  codebase; the env type declaration is in `24-typescript-project-and-antipatterns.md`.''',
'''- Read project-injected values through one typed config module. The narrow framework-constant exception
  is owned by `alaa-frontend-developer references/48-config-and-environment.md`; it grants no exemption
  to custom variables. Env type declarations are in `24-typescript-project-and-antipatterns.md`.''')
for file in ['references/10-build-contract-and-artifacts.md', 'references/30-serving-caching-and-public-path.md']:
    replace(D, file, 'Any other file needing an asset URL reads `import.meta.env.BASE_URL`',
            'Asset consumers read framework-generated `import.meta.env.BASE_URL` under the constant exception in\n  `alaa-frontend-developer references/48-config-and-environment.md`' if '10-' in file else
            'Asset consumers read framework-generated `import.meta.env.BASE_URL` under the constant exception in\n`alaa-frontend-developer references/48-config-and-environment.md`')

# A23: deliberate ownership relocation preserves two distinct historical measurements.
replace(F, 'references/41-lighthouse-and-web-vitals.md',
'''Defaults for an initial route, compressed: JS < 300 KB, CSS < 100 KB, above-fold images < 500 KB, fonts <
100 KB subset, third-party < 200 KB, total < 1.5 MB. Repo rules override the numbers.''',
'''Defaults for an initial route, compressed: JS < 300 KB, CSS < 100 KB, above-fold images < 500 KB,
third-party < 200 KB, total < 1.5 MB. Font subset and total-transfer ceilings have different scopes;
read `alaa-ui-ux-design-system references/45-render-and-asset-budgets.md` under Font bytes for both.
Repo rules override the numbers.''')
replace(U, 'references/45-render-and-asset-budgets.md',
'''- **150 KB total transferred** for first-party fonts on the initial route.''',
'''- **150 KB total transferred** for first-party fonts on the initial route.
- The initial route's **compressed subset font bytes stay < 100 KB** (the existing Lighthouse budget
  relocated here). This measures the subset payload; the 150 KB ceiling measures all first-party font
  transfer on that route. Record both scopes; satisfying one does not waive the other.''')
replace(U, 'references/05-rtl-and-persian.md',
'''- **Byte budget.** Persian faces are heavy. Ship at most three weights per family in `woff2` only, subset to the Arabic and Latin ranges plus U+200C, with a total first-party font budget of **150 KB** transferred for the initial route and no more than two `<link rel="preload">` font files. Drop `woff` entirely unless the repo's browser-support matrix names a browser that lacks `woff2`. Measure with the transferred size in the network panel, not the file size on disk.''',
'''- **Byte budget.** Before choosing Persian font weights, subsets or preloads, read `45-render-and-asset-budgets.md` under Font bytes for the ceilings and format/support exception. Persian subsets include Arabic and Latin plus U+200C. Measure transferred size in the network panel, not file size on disk.''')

# A39: selected package manager, repository scripts and installed executables only.
replace(V, 'references/60-validation-gates.md',
'''Read `package.json` first and prefer the repository's own scripts. The authoring lane's focused set:''',
'''Read `package.json` and the lockfile first; use that manager's existing scripts. In Quasar repositories,
`alaa-quasar-app-vite-v3 SKILL.md` Version rules owns manager selection. Below, `<pm>` means that manager;
for a direct tool call use its installed-local execution form, never a downloading package runner.
The authoring lane's focused set:''')
replace(V, 'references/60-validation-gates.md',
'''npm run typecheck                          # or: npx vue-tsc --noEmit
npm run lint
npm run test -- related --run <changed files>   # only when the test script runs bare `vitest`
npx vitest related --run <changed files>        # otherwise, with the test script's own config flags
npm run build''',
'''<pm> run typecheck                         # or the installed-local vue-tsc --noEmit
<pm> run lint
<pm> run test <forwarded related --run arguments>  # only for a bare vitest test script
<local-exec> vitest related --run <changed files> <test-script config flags>  # otherwise
<pm> run build''')
replace(V, 'references/60-validation-gates.md',
'''`npm run test` without a filter''', '''`<pm> run test` without a filter''')
replace(V, 'references/60-validation-gates.md', '`npm run build` runs the same', '`<pm> run build` runs the same')

# B11: preserve the unique auth-memory posture; delegate persistence and Cache Storage contents.
replace(F, 'SKILL.md',
'''4. **No token in persistent browser storage.** Do not add a new write of an access token to `localStorage` or `sessionStorage`; hold it in a module-scoped variable owned by exactly one auth module.''',
'''4. **Auth-state storage.** Apply `alaa-indexeddb-browser-storage references/61-authority-boundary.md` for credential-persistence prohibitions; hold the access token in a module-scoped variable owned by exactly one auth module.''')
replace(Q, 'references/34-frontend-failure-and-degradation.md',
'''**Structured offline data is not a service-worker concern.** Cache Storage holds Request/Response pairs only; drafts, progress, outbox rows, and cursors are''',
'''**Before choosing an offline store, apply `references/30-service-worker-excellence.md` section 2 for Cache Storage's contents boundary.** Drafts, progress, outbox rows, and cursors are''')
replace(Q, 'SKILL.md',
'''Structured offline data — drafts, progress, outbox, cursors — is `/alaa-indexeddb-browser-storage`; a service worker owns only Request/Response caches.''',
'''For offline-store boundaries, apply `references/30-service-worker-excellence.md` section 2; structured data belongs to `/alaa-indexeddb-browser-storage`.''')

# B12 / O13 / O6: move the complete manual runbook, then make applicability explicit.
p, s = read(F, 'references/50-qa-and-verification.md')
manual = s[s.index('- **Install and first load**'):s.index('## Accessibility smoke')].strip()
manual = manual.replace('navigation stays network-only or\n  network-first as the contract says.',
                        'navigation follows `references/30-service-worker-excellence.md` section 1.')
replace(Q, 'references/75-testing-ci-playbook.md', '## 4. Test style',
'''### Manual service-worker runbook

Run against the production build when PWA exists and the change affects its worker, registration,
cache/asset base, update flow or offline behavior. For InjectManifest edits, the minimum verification in
`references/32-pwa-injectmanifest-guard.md` section 6 also applies, including remote assets when present.

''' + manual + '\n\n## 4. Test style')
replace(F, 'references/50-qa-and-verification.md',
    s[s.index('## Mandatory SSR and hydration checks'):s.index('## Accessibility smoke')],
'''## SSR and hydration checks

| Applies when | Required proof |
|---|---|
| SSR exists and the change affects server render, initial markup/data, boot, routing, auth or locale/timezone output | No first-load crash; no hydration warning or client-only initial-DOM drift; no duplicate SSR/client request; stable list keys; affected formatted output stays deterministic across timezones (`55-i18n-locale-and-rtl.md`). |

Select proof for the changed surface through `05-proof-and-tests.md`. A static-only change with no
affected SSR path does not trigger these runtime checks; an owed check with no runner remains blocked.

## Service-worker verification

When PWA exists and a change affects its worker, registration, cache/asset base, update flow or offline
behavior, run `alaa-quasar-app-vite-v3 references/75-testing-ci-playbook.md` section 3: automated regressions
and the complete manual runbook. It owns applicability and scenarios; use the production build.

''')

# B13: merge body-only triggers before dropping duplicate routers; preserve ordered SW safety.
p, body = read(F, 'SKILL.md')
ownership = body[body.index('| The subject is'):body.index('## Non-negotiable gates')]
ownership = ownership.replace('Two owners appear to apply: `references/70-companion-skill-routing.md`.\n\n','')
replace(F, 'references/00-topic-map.md', '## Good first searches',
'''## Additional mandatory matches

Read every matching row, even when the user named only one surface.

| The diff touches | Also read |
|---|---|
| SSR, hydration, a router guard, a store, a boot file or any browser-only API | `20-vue-js-ssr-patterns.md` |
| A formatter, or a date, number or currency formatted during SSR | `22-input-validation-and-normalization.md` for input formatters; `55-i18n-locale-and-rtl.md` for SSR output |
| A trace-context header, client event or error report | `47-frontend-observability.md` |
| A UI symptom caused by backend query shape, exact-count cost or missing aggregation | `45-api-and-data-shaping.md` |
| An animation, transition or CSS feature with uncertain support | `alaa-ui-ux-design-system references/70-motion-contract.md` and `alaa-ui-ux-design-system references/72-modern-css-baseline-tiers.md`; reduced motion is a blocking gate |
| Lighthouse, PageSpeed, Web Vitals, LCP/INP/CLS/TBT or a score target | `41-lighthouse-and-web-vitals.md` for weighted investigation order and production/mobile/three-run/median proof |

## Companion ownership routes

''' + ownership + '\n## Good first searches')
replace(F, 'SKILL.md',
    body[body.index('## Ownership — one table, route and never restate'):body.index('## Non-negotiable gates')], '')
p, body = read(F, 'SKILL.md')
replace(F, 'SKILL.md', body[body.index('## Router'):body.index('## Workflow and maintenance')],
'''## Router

Before choosing an owner or acting on a changed frontend surface, read `references/00-topic-map.md` for
all matching mandatory reads and companion routes.

''')
replace(F, 'SKILL.md', 'The ownership table below names the owner and the file for each.',
        'The topic map names the owner and file for each.')
replace(F, 'references/70-companion-skill-routing.md', 'The routing table itself is in `SKILL.md`.',
        'The routing table itself is in `00-topic-map.md`.')
replace(F, 'references/70-companion-skill-routing.md', 'the owner named in the `SKILL.md` table',
        'the owner named in the `00-topic-map.md` table')
replace(Q, 'references/00-topic-map.md',
        '`30-service-worker-excellence.md`, `32-pwa-injectmanifest-guard.md` |',
        '`32-pwa-injectmanifest-guard.md` first, then `30-service-worker-excellence.md` |')
replace(Q, 'references/00-topic-map.md',
'''| choose a caching strategy, write or edit `src-pwa/sw/custom-sw.*`, ship an update prompt, or debug a stale page after deploy | `30-service-worker-excellence.md` |''',
'''| choose a caching strategy, write or edit a custom service worker or InjectManifest, ship an update prompt, or debug a stale page after deploy | `32-pwa-injectmanifest-guard.md` first for custom-worker/InjectManifest edits, then `30-service-worker-excellence.md`; verify install, update and offline |''')
replace(Q, 'references/00-topic-map.md',
'''| render on the server: `ssrContext`, `preFetch`, cookie-to-header auth, SEO meta, or a hydration mismatch you must fix | `31-ssr-pwa-and-security.md` |''',
'''| touch SSR, `ssrContext`, `preFetch`, router, store, boot, middleware, SEO, auth or a hydration mismatch | `31-ssr-pwa-and-security.md` |''')
replace(Q, 'references/00-topic-map.md',
'''| add or change a mode (`quasar dev -m ...`), or hit a "module not found" that appears in one mode only | `35-platform-modes.md` |''',
'''| touch any platform mode, or hit a "module not found" that appears in one mode only | `21-cli-vite-and-config.md`, then `35-platform-modes.md` |''')
replace(Q, 'references/00-topic-map.md',
'''| call an API the browser gates behind a prompt: microphone, camera, screen, geolocation, notifications, clipboard read, wake lock, sensors, Bluetooth/USB/NFC | `45-browser-apis-and-permissions.md` |''',
'''| call an API the browser gates behind a prompt: microphone, camera, screen, geolocation, notifications, clipboard read, wake lock, sensors, Bluetooth/USB/NFC | `45-browser-apis-and-permissions.md` for the gesture/primer, denial recovery and expiring-grant contract |''')
p, body = read(Q, 'SKILL.md')
replace(Q, 'SKILL.md', body[body.index('3. **`references/00-topic-map.md`'):body.index('## Companion boundary')],
'''3. Before acting on a Quasar surface, read `references/00-topic-map.md` for every matching route and
   mandatory pairing, in its stated order.

''')
replace(Q, 'references/91-agent-authoring-and-dual-runtime.md',
        'one pointer to the router, mandatory pairings, companion boundary',
        'one triggered pointer to the external router and its mandatory pairings, companion boundary')

# A21: one conditional requirement owner, no invented local sampling budget.
p, text = read(F, 'references/47-frontend-observability.md')
replace(F, 'references/47-frontend-observability.md',
    text[text.index('This file states what a browser client'):text.index('## Trace context to the gateway')],
'''This file owns browser transport and correlation constraints. Before adding or removing a browser signal,
apply `alaa-observability-soc references/20-instrumentation-gates.md` under Browser client signals for the
conditional requirements. Quasar reference 36 above owns emission wiring; do not recreate its allowlist here.

''')
replace(F, 'references/47-frontend-observability.md',
'''Errors are not sampled. Web Vitals and request-outcome events are sampled at the rate the observability
skill sets. A per-render or per-keystroke event is a volume incident: aggregate in the client and emit''',
'''Resolve sampling and volume budgets through the observability owner above. If the target's required rate
is unregistered, report the gap instead of inventing a rate. A per-render or per-keystroke event is a
volume incident: aggregate in the client and emit''')
p, text = read(Q, 'references/36-client-observability-contract.md')
replace(Q, 'references/36-client-observability-contract.md',
    text[text.index('## 1. What a Quasar frontend may emit'):text.index('**A user action')],
'''## 1. Applicable browser signals

Before adding or removing a signal, apply `alaa-observability-soc references/20-instrumentation-gates.md`
under Browser client signals. It owns the conditional requirement classes; this file owns their Quasar
wiring. Use the services registries above for payload names. A missing approved name is a contract gap,
not permission to invent one or silently omit an applicable signal.

''')
replace(Q, 'references/36-client-observability-contract.md',
'''- **Unhandled errors are emitted at the rate set by `/alaa-observability-soc` (`$alaa-observability-soc`)**, `references/30-quantitative-budgets.md`. Apply the sample decision once per session and reuse it, so a single session's errors are either all present or all absent; per-event sampling produces unreconstructable traces.
- **Web-vitals samples are emitted at the rate set in the same file.** A vitals sample is emitted at most once per metric per page view; the browser's own final value is the one to send.
- **Service-worker lifecycle transitions are not sampled.** They are low-volume and each one explains a class of user report.''',
'''- Resolve sampling from `alaa-observability-soc references/30-quantitative-budgets.md` and the approved
  target configuration. Missing browser-specific rates remain a contract gap; do not invent a rate.
- A web-vitals sample is emitted at most once per metric per page view; send the browser's final value.''')
replace(Q, 'references/36-client-observability-contract.md',
'''- Register the error handlers in a **boot file scoped `{ client: true }`**, so no handler is installed in the SSR process where `window` does not exist. The boot shape is `references/22-cli-cookbook-and-examples.md`.''',
'''- Register browser error handlers in a **boot entry `{ path: '<client-boot>', server: false }`**. Setting
  `client: true` alone does not exclude SSR. Pass the boot callback's Vue `app` to the browser integration;
  the installed-line shape is `references/22-cli-cookbook-and-examples.md`.''')
replace(Q, 'references/36-client-observability-contract.md',
'''\u2705 Do — emit the four named classes, scrub in the sender, and let every failure to emit pass silently. \u274c Don't — send `window.location.href`, retry a failed emission, or invent a field name because the registry does not have one yet.''',
'''### Sentry for SPA and SSR

Before choosing an SDK, inspect the target lockfile, installed packages, Node runtime, SSR server framework
and module format. Use the pinned `@sentry/vue` browser API; choose the matching Node/server integration
for SSR, not the browser SDK. No fleet package version or browser env-key default is registered here:
`alaa-services-contract references/21-alaa-platform-observability-directive.md` owns that authority split.

- **SPA/browser side:** initialize `@sentry/vue` from the client boot above before mount, using its `app`
  option. Route classified failures through the existing single reporting facade; do not add another
  global handler that reports the same exception. HTTP outcomes belong at the HTTP facade/interceptor;
  connection transitions at the WS/SSE lifecycle owner. A library's automatic capture does not prove
  every applicable signal is wired.
- **DSN/config:** read the approved public browser DSN, release and environment through the target's typed
  config module. A browser DSN allows event submission and can be abused; it is not a read/admin secret.
  Never let browser initialization fall back to server `SENTRY_DSN`, and never expose an auth/upload token.
  Runtime config must resolve before initialization; release identity remains available at build time.
- **SSR side:** initialize the selected server SDK at the version's documented startup point, before the
  modules it must instrument. Wire its integration to the actual SSR server framework and isolate scope
  per request; never keep user context in a shared mutable singleton. Do not copy a preload flag across
  SDK majors. Capture a render failure on the server through the existing platform exception path;
  do not report it again as a browser exception merely because HTTP returned an error.
- **Privacy:** apply `alaa-observability-soc references/60-sentry-and-profiling.md` configuration gates.
  Read the pinned SDK options before configuring collection: v11 replaces `sendDefaultPii` with
  `dataCollection` and changes defaults. A bare `sendDefaultPii: false` is no universal solution.
  Scrub error events with `beforeSend`; inspect the separate hooks and defaults of every enabled
  breadcrumb, span, log or replay path. Do not enable Pinia state capture or optional integrations by
  copying the upstream quickstart. Error-event scrubbing proves no coverage of those other paths.
- **Release proof:** source maps and their upload token follow
  `alaa-frontend-devops references/25-artifact-identity-and-provenance.md`; tokens stay in CI secrets.
  Run the controlled non-production arrival, redaction, attribution and disabled-Sentry platform-path
  checks required by the observability owner. A source-only skill edit proves no SDK installation,
  live emission, collector arrival or SSR isolation.

Official sources, read: 2026-10-18: [Vue setup](https://docs.sentry.io/platforms/javascript/guides/vue/)
([official source](https://github.com/getsentry/sentry-docs/blob/master/docs/platforms/javascript/guides/vue/index.mdx)),
[Quasar boot scoping](https://quasar.dev/quasar-cli-vite/boot-files/),
[Node SDK](https://docs.sentry.io/platforms/javascript/guides/node/),
and [JavaScript v11 migration](https://github.com/getsentry/sentry-javascript/blob/develop/MIGRATION.md).
These sources explain selection; recheck version-matched docs in the target before copying options.

Do: wire each applicable class, scrub before transport and contain emission failure.
Do not send resolved URLs, loop on a failed collector, or invent a missing registry name.''')

# In already changed Markdown only, apply the current single cross-skill call form.
for p, text in changed.items():
    text = re.sub(r'`(/[-a-z0-9]+)` \(`\$[-a-z0-9]+`\)', r'`\1`', text)
    p.write_text(text, encoding='utf-8', newline='\n')

Path('artifacts/skill-pack-optimization-20261018/lanes/UI-changed-paths.json').write_text(
    __import__('json').dumps([p.as_posix() for p in sorted(changed)], indent=2) + '\n',
    encoding='utf-8', newline='\n')
print(f'Updated {len(changed)} owned Markdown files.')
