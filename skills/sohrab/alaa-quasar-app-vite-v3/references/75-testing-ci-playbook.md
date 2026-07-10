# Testing and CI Playbook

Use when adding tests, changing harnesses, or validating production Quasar CLI + Vite work.

## Policy and layers

Prefer current specific extensions:

```bash
quasar ext add @quasar/testing-unit-vitest
quasar ext add @quasar/testing-e2e-cypress
```

Use Jest only when already entrenched or specifically justified; never add deprecated umbrella `@quasar/testing` for new setup.

Minimum useful layers: type/lint; unit tests for composables/services/stores; interactive component tests; critical-flow E2E smoke; production builds for each supported mode; PWA/SSR checks where those modes exist.

## Suggested scripts

Adapt names to repo conventions; never overwrite scripts before checking CI references.

```json
{
  "scripts": {
    "dev": "quasar dev", "build": "quasar build",
    "build:pwa": "quasar build -m pwa", "build:ssr": "quasar build -m ssr",
    "lint": "eslint .", "typecheck": "vue-tsc --noEmit",
    "test:unit": "vitest run", "test:unit:watch": "vitest", "test:e2e": "cypress run",
    "validate": "pnpm run lint && pnpm run typecheck && pnpm run test:unit && pnpm run build"
  }
}
```

## Test style

Unit tests must prove behavior:

```ts
import { describe, expect, it } from 'vitest'
import { normalizeCourseTitle } from '@/services/course/normalizeCourseTitle'
describe('normalizeCourseTitle', () => {
  it('trims and collapses whitespace', () => expect(normalizeCourseTitle('  ریاضی   دوازدهم  ')).toBe('ریاضی دوازدهم'))
})
```

❌ Don't — use `it('works', () => expect(true).toBe(true))`.

Component tests must mount required Quasar/router/pinia/plugins, preferably through the repo utility:

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

❌ Don't — `mount(CourseCard)` and silently miss plugin behavior.

## E2E priorities

Production app load; login/logout when in scope; course list/page; checkout/payment start with test env when in scope; PWA update prompt after PWA changes; rendered SSR HTML after SSR changes. Avoid unstable external production services unless the repo already handles them.

## CI by change

```bash
# Small UI
<pm> run lint
<pm> run typecheck
<pm> run test:unit -- --runInBand # if applicable
<pm> run build

# PWA
<pm> run lint
<pm> run typecheck
<pm> quasar build -m pwa
# run Lighthouse or app-specific PWA smoke on the production build when available

# SSR
<pm> run lint
<pm> run typecheck
<pm> quasar build -m ssr
node dist/ssr/index.js
# curl key routes if shell/network is available

# Dependency/Quasar upgrade
<pm> install --frozen-lockfile
<pm> quasar info
<pm> run lint
<pm> run typecheck
<pm> run test:unit
<pm> run build
<pm> quasar build -m pwa # if present
<pm> quasar build -m ssr # if present
```

## Honest reporting

```md
Validation run:
- pnpm run lint: passed
- pnpm run typecheck: passed
- pnpm run test:unit: failed in existing test X unrelated to this change
- pnpm quasar build -m pwa: not run; PWA mode is not present in repo
```

❌ Don't — report “Everything should work.”
