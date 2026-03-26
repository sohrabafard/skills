# Proxies, Public Path, and Remote Assets

Use this file when the task touches reverse proxies, remote asset bases, cache headers, or production asset serving.

## Public path discipline

- Prefer one source of truth for the browser asset base.
- If the app can serve assets remotely, treat base-path changes as deployment-critical.
- Do not silently diverge SSR, PWA, manifest, and chunk URL assumptions.

## Reverse proxy checks

- Verify the proxy preserves the intended asset paths.
- Verify the proxy does not accidentally cache SSR HTML like immutable assets.
- Verify compression settings do not corrupt or mis-serve built files.
- Verify path rewrites do not strip or duplicate the asset prefix.

## Cache header rules

- Hashed browser assets can be long-lived and immutable.
- HTML and SSR responses should follow the project’s shorter cache policy.
- Do not apply one cache policy to every response type.

## Remote asset checklist

- Confirm the asset origin and path prefix are computed correctly for deployed environments.
- Confirm browser-visible URLs point to the expected origin.
- Confirm offline or service worker behavior does not assume a different asset base.
- If the task changes remote asset behavior, include rollback and smoke-check steps.

## Common symptoms

- app shell loads but chunks 404
- CSS loads from one origin while JS loads from another
- service worker or manifest still points at the old asset base
- direct deep links work but hard refresh loses assets
