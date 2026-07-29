# Build Contract and Artifacts

Open this file to state or assert what a build must emit and where, before that output is packaged or uploaded.

## The contract

The build contract is three values plus one shape. State all four in the repository's `AGENTS.md`; this skill asserts them, it does not invent them per task.

- **SSR runtime entry.** `dist/ssr/index.js`. The SSR server bundle sits under `dist/ssr/server/`.
- **Client asset root.** `dist/ssr/client/assets` for an SSR build; `dist/spa/assets` for SPA; `dist/pwa/assets` for PWA.
- **Browser asset base.** Declared in exactly one place, `quasar.config.*`'s `build.publicPath`. Any other file needing an asset URL reads `import.meta.env.BASE_URL` and never re-derives it.
- **Emitted asset shape.** Every emitted JS and CSS file under the client asset root has a content hash in its filename: a trailing token of at least 8 url-safe characters, separated from the stem by `-` or `.`. Vite and Rolldown emit `name-<hash>.js` (`createHostSdk-8LNd2MeL.js`, `read: client 2026-07-28`); older toolchains emit `name.<hash>.js`. Both satisfy the contract; `vendor.js` does not. This is the precondition that makes an immutable cache header safe, so it is a build assertion and not a serving preference.

Changing any of the four requires editing `AGENTS.md` in the same commit. A merge request that moves an artifact path without that edit fails the gate in `references/20-ci-gates-and-predicates.md`.

*(Values read from the live `client` repository, 2026-07-28. In an SSR build the client entry HTML is not emitted as a file: `dist/ssr/render-template.js` renders it and `dist/ssr/quasar.manifest.json` is the asset manifest. Assert the manifest, not an `index.html`, for SSR.)*

## Assertions on the emitted tree

These are the assertions `scripts/verify-artifact-contract.mjs` executes. Run it; do not re-implement it by eye.

1. The SSR runtime entry exists at the declared path when the build mode is SSR.
2. Every `src`, `href`, and `modulepreload` URL in the emitted HTML, and every entry in the client manifest, resolves to a file that exists on disk under the client asset root.
3. No emitted asset path escapes the client asset root, and every absolute URL in the emitted HTML matches the declared base.
4. No secret-shaped value appears verbatim in any emitted client chunk. See `references/35-client-bundle-security.md` for what counts.
5. Every emitted JS and CSS filename carries a content hash.
6. A provenance file sits beside the artifact. See `references/25-artifact-identity-and-provenance.md` for its contents.

## Server-only code must not be reachable from the client

Server-only modules must not be reachable from the client entry graph. Assert it by scanning every emitted client chunk for the server entry's exported symbol names and for any module specifier that only resolves under the `node` condition. Keep server-only code reachable from the SSR entry alone.

This is an assertion on the *output*. Whether a module is in the graph at all is decided by `/alaa-mono-package` (`$alaa-mono-package`), `references/10-package-boundary-and-entrypoints.md`.

## Package assets in the final output

A workspace package's assets and CSS must be present in the final client asset output. This skill asserts presence in the output tree; it does not decide reachability.

Whether a package asset is reachable from an entry — the `exports` map, `sideEffects`, the static-specifier rule — belongs to `/alaa-mono-package` (`$alaa-mono-package`), `references/30-assets-css-and-ssr-client-assets.md`. When the assertion here fails, the diagnosis is almost always there.

## Failure modes this contract catches

- `publicPath` or base-path drift between local and deployed environments.
- The publish step uploading a folder that the build did not populate.
- The runtime image receiving a partial output tree with the browser assets omitted.
- Package assets emitted outside the client asset root.

For what to do when one of these is live in production, go to `references/45-deploy-failure-playbook.md`.
