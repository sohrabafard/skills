# Legacy Skill Coverage

This pack replaces the previous frontend skill cluster and folds the high-value shared-doc content into a portable routing-first structure.

## Deleted skill mapping

- `alaa-frontend`
  - Primary coverage:
    - `10-contract-and-boundaries.md`
    - `50-qa-and-verification.md`
    - `60-browser-debug.md` (design/UX portions moved to `$alaa-ui-ux-design-system`)

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

- `ssr-auth-guard`
  - Primary coverage:
    - `21-ssr-auth-and-session-patterns.md`
    - `20-vue-js-ssr-patterns.md`

- `api-designer`
  - Primary coverage:
    - `45-api-and-data-shaping.md`
    - `10-contract-and-boundaries.md`

- `database-optimizer`
  - Primary coverage:
    - `45-api-and-data-shaping.md`
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

## Portable companion replacements

- Previous workspace-local frontend delivery guidance
  - Portable replacement:
    - `$alaa-frontend-devops`

- Previous workspace-local frontend annotation guidance
  - Portable replacement:
    - `$alaa-frontend-doc-annotations`

- Previous workspace-local workspace-package contract guidance
  - Portable replacement:
    - `$alaa-mono-package`

## Search aliases

If a task mentions old terms such as:

- `hydration mismatch`
- `BFF`
- `token-mediating backend`
- `silent refresh`
- `localStorage`
- `offline fallback`
- `SKIP_WAITING`
- `fonts-runtime`
- `deep watch`
- `AbortController`
- `WebSocket reconnect`
- `problem details`
- `ETag`
- `If-None-Match`
- `sparse fields`
- `N+1`
- `verification runbook`

route to the new reference file instead of trying to resurrect the deleted local skill.
