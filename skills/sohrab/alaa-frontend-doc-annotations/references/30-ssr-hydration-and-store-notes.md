# SSR, Hydration, and Store Notes

Use this file when the annotated code touches SSR, hydration, store lifecycle, or frontend auth.

## SSR notes worth capturing

- browser-only APIs must stay out of SSR render paths
- request-scoped state must not leak through module globals
- server-side auth bridging must stay server-side only

## Hydration notes worth capturing

- deterministic rendering matters
- client-only measurement or viewport logic should be marked as post-mount behavior
- unstable ordering or random values in render paths should be called out if the file relies on them being avoided

## Store notes worth capturing

- explain how state is injected, hydrated, or replaced
- explain why a store action runs on server, client, or both
- explain cross-file assumptions between boot logic, route loading, and store state

## Auth notes worth capturing

- mark server-only token handling clearly
- note whether a fetch wrapper runs in SSR, client, or both
- note which auth assumptions come from gateway, BFF, or cookie-backed flows
