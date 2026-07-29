# Testing and CI for a Quasar app

You are about to add a test, change a test harness, or decide which commands prove a change. This file owns two things only: the **Quasar harness** and the **Quasar-shaped regressions** no other skill can write. Everything else is routed.

**Test design is not this skill's ground.** What makes a test worth having, the layer it belongs in, doubles, flake, coverage, failure-mode-first design, and the six proof levels — 1 static, 2 unit, 3 parity, 4 local smoke, 5 in-runtime, 6 live dependency — are `/alaa-testing-strategy` (`$alaa-testing-strategy`), `references/10-what-makes-a-test.md`, `references/20-layers.md`, `references/40-proof-strength.md`, `references/70-failure-mode-first.md`, `references/80-evidence-and-reporting.md`. Read the layer set there; do not re-derive it here.

**Stack versus platform.** This skill owns **gates and predicates** — what must be true before a Quasar change ships — and emits **no provider YAML**. Provider expression is `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`), which owns the YAML and decides no gate. Pipeline, container, and deploy execution for this frontend are `/alaa-frontend-devops` (`$alaa-frontend-devops`). The shell blocks below are the gate predicates in runnable form; translating them into a pipeline is the platform skill's job.

## 1. Harness

```bash
quasar ext add @quasar/testing-unit-vitest
quasar ext add @quasar/testing-e2e-cypress
```

- **Use Jest only when `package.json` already declares a Jest dependency.** Otherwise use `@quasar/testing-unit-vitest`.
- Never add the deprecated umbrella `@quasar/testing` to a new setup.
- App-Extension compatibility with app-vite v3 is UNVERIFIED here; check each extension's changelog live before adding it to a v3 repository — `references/80-upstream-deltas-and-live-checks.md` §6.

## 2. Gates — what must be true before a Quasar change ships

| Gate | Predicate | Applies when |
| --- | --- | --- |
| Static | lint and `vue-tsc --noEmit` exit 0 | always |
| Unit | the changed composable, service, or store has a test that fails without the change | always |
| Component | the component mounts with the Quasar, router, and Pinia plugins it needs, and the assertion is about behaviour | a component changed |
| Mode build | every mode present in the repository builds | any config, boot, or mode change |
| SSR render | the built SSR server starts and returns a 2xx with expected markup for one route per layout | the SSR mode exists |
| Hydration | no hydration mismatch warning on the routes covered by the SSR gate | the SSR mode exists |
| Service-worker update | an already-installed worker is replaced and the app reaches the new build without a manual cache clear | the PWA mode exists and the change touched `src-pwa/` |
| Offline | each route marked "works offline" in the degradation matrix renders with the network disabled | the PWA mode exists |

A gate that could not run is reported as not run, with the reason. It is never reported as passed.

## 3. The three Quasar-shaped regressions

These do not exist in a generic frontend test suite, and they catch the failures this skill exists to prevent.

**SSR render regression.** Build the SSR bundle, start it, request one route per layout, and assert the response status and a marker string that only server-rendered markup contains. This catches a boot file that throws only on the server, a module-global leak that appears on the second request, and a render path that a client-only test never executes. Issue the second request with a different session to catch cross-request state.

```bash
<pm> quasar build -m ssr
node dist/ssr/index.js &
# assert: status 2xx, expected markup present, and a second request with a
# different session does not return the first session's data
```

**Hydration-mismatch assertion.** Load the same route in a browser against the running SSR server and fail the test on any hydration mismatch warning in the console. A mismatch is a warning, not an error, so it passes every test that only asserts on rendered output; asserting on the console is what makes it a regression. Keep the assertion on the console message, not on a screenshot.

**Service-worker update regression.** Load the app so a worker installs, deploy or serve a second build, reload, and assert that the app reaches the new build and that no request for a hashed chunk returns 404. This catches the unconditional `skipWaiting` chunk-404 hazard and a broken `controllerchange` guard — `references/30-service-worker-excellence.md` §4. Pair it with an offline assertion: `context.setOffline(true)`, then assert the offline shell for a "works offline" route and the offline fallback for a "hard fails" route, from the matrix in `references/34-frontend-failure-and-degradation.md` §3.

Service-worker interception in Playwright is experimental and Chromium-only; prefer these observable assertions over intercepting the worker.

## 4. Test style

A unit test proves behaviour:

```ts
import { describe, expect, it } from 'vitest'
import { normalizeCourseTitle } from '@/services/course/normalizeCourseTitle'
describe('normalizeCourseTitle', () => {
  it('trims and collapses internal whitespace', () =>
    expect(normalizeCourseTitle('  Advanced   Physics  ')).toBe('Advanced Physics'))
})
```

❌ Don't — `it('works', () => expect(true).toBe(true))`.

A component test mounts what the component needs, preferably through the repository's own helper:

```ts
import { mount } from '@vue/test-utils'
import { Quasar } from 'quasar'
import { createTestingPinia } from '@pinia/testing'
import CourseCard from '@/components/course/CourseCard.vue'
const wrapper = mount(CourseCard, {
  global: { plugins: [Quasar, createTestingPinia({ stubActions: false })] },
  props: { course: { id: 1, title: 'Physics' } }
})
```

❌ Don't — `mount(CourseCard)` and silently miss every plugin behaviour.

Input normalization is tested against the shared corpus owned by `/alaa-input-normalization` (`$alaa-input-normalization`), `references/50-corpus-and-harness.md`, not against ad-hoc cases written in a component test.

## 5. Suggested scripts

Adapt the names to the repository's conventions, and check what CI references before overwriting anything.

```json
{
  "scripts": {
    "dev": "quasar dev", "build": "quasar build",
    "build:pwa": "quasar build -m pwa", "build:ssr": "quasar build -m ssr",
    "lint": "eslint .", "typecheck": "vue-tsc --noEmit",
    "test:unit": "vitest run", "test:e2e": "cypress run",
    "validate": "pnpm run lint && pnpm run typecheck && pnpm run test:unit && pnpm run build"
  }
}
```

## 6. Commands by change type

```bash
# Small UI change
<pm> run lint && <pm> run typecheck && <pm> run test:unit && <pm> run build

# PWA change
<pm> run lint && <pm> run typecheck && <pm> quasar build -m pwa
# then the service-worker update and offline regressions from §3

# SSR change
<pm> run lint && <pm> run typecheck && <pm> quasar build -m ssr
node dist/ssr/index.js
# then the SSR render and hydration regressions from §3

# Dependency or Quasar upgrade
<pm> install --frozen-lockfile
<pm> quasar info
<pm> run lint && <pm> run typecheck && <pm> run test:unit && <pm> run build
<pm> quasar build -m pwa   # when the mode exists
<pm> quasar build -m ssr   # when the mode exists
```

End-to-end priorities when the budget is limited: production app load; login and logout when in scope; the primary content list and detail routes; a payment start against a test environment when in scope; the PWA update prompt after a PWA change; rendered SSR HTML after an SSR change. Avoid depending on an unstable external production service unless the repository already does.

## 7. Reporting

```md
Validation run:
- pnpm run lint: passed
- pnpm run typecheck: passed
- pnpm run test:unit: failed in existing test X, unrelated to this change
- pnpm quasar build -m pwa: not run; the PWA mode is not present in this repository
- SSR render regression: not run; no SSR mode
```

❌ Don't — report "everything should work". The evidence and reporting contract is `/alaa-testing-strategy` (`$alaa-testing-strategy`), `references/80-evidence-and-reporting.md`.

Search: `vitest`, `cypress`, `@quasar/testing-unit-vitest`, `vue-tsc --noEmit`, `mount with Quasar plugin`, `createTestingPinia`, `SSR render regression`, `hydration mismatch assertion`, `service worker update regression`, `offline assertion`, `gate`, `predicate`.
