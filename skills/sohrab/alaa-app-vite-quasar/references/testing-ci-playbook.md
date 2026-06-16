# Testing and CI Playbook

Use this reference when adding tests, changing test harnesses, or preparing production validation for Quasar CLI with Vite.

## 1. Testing extension policy

Prefer current specific Quasar testing extensions:

```bash
quasar ext add @quasar/testing-unit-vitest
quasar ext add @quasar/testing-e2e-cypress
```

Use Jest only if the repo already uses it heavily or there is a specific reason.

Do not use the deprecated umbrella `@quasar/testing` extension for new setup.

## 2. Test layers

Minimum useful layers for Alaa frontend apps:

1. Type/lint checks
2. Unit tests for composables/services/stores
3. Component tests for interactive Quasar components
4. E2E smoke tests for critical flows
5. Production mode build tests for each supported Quasar mode
6. PWA/SSR-specific checks when those modes exist

## 3. Suggested scripts

Adapt names to the repo convention.

```json
{
  "scripts": {
    "dev": "quasar dev",
    "build": "quasar build",
    "build:pwa": "quasar build -m pwa",
    "build:ssr": "quasar build -m ssr",
    "lint": "eslint .",
    "typecheck": "vue-tsc --noEmit",
    "test:unit": "vitest run",
    "test:unit:watch": "vitest",
    "test:e2e": "cypress run",
    "validate": "pnpm run lint && pnpm run typecheck && pnpm run test:unit && pnpm run build"
  }
}
```

Do not overwrite existing scripts without checking CI references.

## 4. Unit test style

Correct composable test:

```ts
import { describe, expect, it } from 'vitest'
import { normalizeCourseTitle } from '@/services/course/normalizeCourseTitle'

describe('normalizeCourseTitle', () => {
  it('trims and collapses whitespace', () => {
    expect(normalizeCourseTitle('  ریاضی   دوازدهم  ')).toBe('ریاضی دوازدهم')
  })
})
```

Wrong:

```ts
it('works', () => {
  expect(true).toBe(true)
})
```

## 5. Component tests with Quasar

Mount components with required plugins, router, pinia, and Quasar context. Follow the repo's existing test utility if one exists.

Correct pattern:

```ts
import { mount } from '@vue/test-utils'
import { Quasar } from 'quasar'
import { createTestingPinia } from '@pinia/testing'
import CourseCard from '@/components/course/CourseCard.vue'

const wrapper = mount(CourseCard, {
  global: {
    plugins: [
      Quasar,
      createTestingPinia({ stubActions: false })
    ]
  },
  props: {
    course: { id: 1, title: 'Physics' }
  }
})
```

Wrong:

```ts
mount(CourseCard) // fails or silently misses Quasar/plugin behavior
```

## 6. E2E smoke tests

Prioritize flows that prove production readiness:

- app loads in production build
- login/logout if in scope
- course page/list opens
- checkout/payment start if in scope with test env
- PWA update prompt if PWA changed
- SSR page returns rendered HTML if SSR changed

Do not make E2E tests depend on unstable external production services unless the repo already has a strategy for it.

## 7. CI validation by task type

Small UI component change:

```bash
<pm> run lint
<pm> run typecheck
<pm> run test:unit -- --runInBand # if applicable
<pm> run build
```

PWA change:

```bash
<pm> run lint
<pm> run typecheck
<pm> quasar build -m pwa
# run Lighthouse or app-specific PWA smoke test on production build when available
```

SSR change:

```bash
<pm> run lint
<pm> run typecheck
<pm> quasar build -m ssr
node dist/ssr/index.js
# curl key routes if shell/network is available
```

Dependency or Quasar upgrade:

```bash
<pm> install --frozen-lockfile
<pm> quasar info
<pm> run lint
<pm> run typecheck
<pm> run test:unit
<pm> run build
<pm> quasar build -m pwa   # if PWA exists
<pm> quasar build -m ssr   # if SSR exists
```

## 8. Reporting validation honestly

Correct final report:

```md
Validation run:
- pnpm run lint: passed
- pnpm run typecheck: passed
- pnpm run test:unit: failed in existing test X unrelated to this change
- pnpm quasar build -m pwa: not run; PWA mode is not present in repo
```

Wrong final report:

```md
Everything should work.
```
