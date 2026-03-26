# Performance and Realtime

Use this file for performance work, hydration cost, Web Vitals, memory leaks, and realtime UI behavior over WebSocket or SSE.

## Performance workflow

### 1. Establish the baseline

Define:

- affected route or view
- device class
- network profile
- SSR first load vs client navigation

### 2. Identify the dominant bottleneck

Choose the main bucket before optimizing:

- server / TTFB / SSR render time
- client / hydration / JS execution / long tasks
- network / chunking / waterfalls / blocking assets
- UI / layout thrash / large DOM / heavy watchers

### 3. Apply the smallest measurable fix

Typical safe wins:

- route-level code splitting
- dynamic imports for heavy features
- fewer deep watchers and broad reactive dependencies
- stable computed inputs and fewer template allocations
- virtualized lists or tables when the surface justifies it
- image or font loading improvements that do not break SSR or SW boundaries

## Realtime rules

### Strict lifecycle boundary

- never open a socket or SSE stream at module scope
- never connect during SSR render
- connect on the client lifecycle only
- disconnect on unmount and route teardown

### Recommended state machine

- `idle`
- `connecting`
- `open`
- `reconnecting`
- `closed`
- `error`

### Reconnect discipline

- exponential backoff
- max delay cap
- jitter to avoid herd behavior
- offline awareness when practical

### Message handling

- parse JSON safely
- validate message shape before mutating UI state
- ignore unknown message types safely and log at debug level when useful
- never trust payloads as HTML

### Observability hooks

- expose connection state for UI and diagnostics
- log connect, disconnect, and reconnect attempts at the right environment level
- avoid leaking sensitive payloads into production logs

## Common failure signatures

- reconnect storms:
  - usually missing backoff, duplicate listeners, or server-close loops
- memory growth after repeated navigation:
  - usually leaked listeners or connections
- poor INP or jank after hydration:
  - often too much client work on first route or heavy watchers
- "perf fix" attempts that hide real build issues:
  - sometimes a missing chunk or asset-path bug masquerades as slow load

## Verification checks

- connect and disconnect across route changes
- reconnect after network drop
- no duplicate event handling after navigating away and back
- CPU and memory stay stable over time
- targeted perf check for the bottleneck you actually changed

## Pairing guidance

- Quasar component/layout-specific performance issues:
  - Pair with `$quasar-skill-packe`
- Package-output or asset-contract performance regressions:
  - Pair with `$monorepo-packages-contract-guard`
- Formal verification plan:
  - Also load `50-qa-and-verification.md`
