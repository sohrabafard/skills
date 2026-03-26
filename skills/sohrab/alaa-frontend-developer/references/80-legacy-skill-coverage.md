# Legacy Skill Coverage

This pack replaces the previous frontend skill cluster and folds the high-value shared-doc content into a portable routing-first structure.

## Deleted skill mapping

- `alaa-frontend`
  - Primary coverage:
    - `10-contract-and-boundaries.md`
    - `50-qa-and-verification.md`
    - `60-design-browser-debug-and-ux.md`

- `javascript-pro`
  - Primary coverage:
    - `20-vue-js-ssr-patterns.md`

- `pwa-service-worker-maintainer`
  - Primary coverage:
    - `30-pwa-sw-and-offline.md`

- `qa-expert`
  - Primary coverage:
    - `50-qa-and-verification.md`

- `vue-expert`
  - Primary coverage:
    - `20-vue-js-ssr-patterns.md`

- `performance-engineer`
  - Primary coverage:
    - `40-performance-and-realtime.md`

- `verify-runbook`
  - Primary coverage:
    - `50-qa-and-verification.md`

- `websocket-engineer`
  - Primary coverage:
    - `40-performance-and-realtime.md`

## Folded shared-doc topic mapping

- `REPO_CONTRACT.md`
  - Folded into:
    - `10-contract-and-boundaries.md`

- `PACKAGES_GUIDE.md`
  - Folded into:
    - `10-contract-and-boundaries.md`

- `VUE_SSR_PATTERNS.md`
  - Folded into:
    - `20-vue-js-ssr-patterns.md`

- `PWA_SW_CONTRACT.md`
  - Folded into:
    - `30-pwa-sw-and-offline.md`

- `PWA_RUNBOOK.md`
  - Folded into:
    - `30-pwa-sw-and-offline.md`

## Search aliases

If a task mentions old terms such as:

- `hydration mismatch`
- `offline fallback`
- `SKIP_WAITING`
- `fonts-runtime`
- `deep watch`
- `AbortController`
- `WebSocket reconnect`
- `verification runbook`

route to the new reference file instead of trying to resurrect the deleted local skill.
