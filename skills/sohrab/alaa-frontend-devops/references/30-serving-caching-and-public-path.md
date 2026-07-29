# Serving, Caching, and Public Path

Open this file when changing `publicPath`, an asset base, a CDN origin, or a path prefix that appears in a browser URL, or when deciding the `Cache-Control` policy for a response class.

This file states **policy**. The directive that implements a policy on the edge — the header block, the compression settings, the path rewrite, the cache rule — is written by `/alaa-haproxy` (`$alaa-haproxy`). This skill decides what the policy is because the policy follows from how the build names its files; that skill decides how it is expressed and it decides no policy.

## Public path is a single source of truth

The browser asset base is declared in exactly one place, `quasar.config.*`'s `build.publicPath`. Any other file needing an asset URL reads `import.meta.env.BASE_URL`. No file re-derives the base from `location`, from an environment variable read at runtime, or from a string literal.

A change to `publicPath` is a delivery-critical change: it changes every URL in the emitted HTML and in the precache manifest simultaneously. It ships with a stated rollback file before it merges, per `references/40-verification-and-rollback.md`.

SSR, PWA, the web app manifest, and chunk URLs all derive from that one value. When they disagree, the app shell loads and the chunks 404 — the first row of `references/45-deploy-failure-playbook.md`.

## Cache policy by response class

The policy is derived, not chosen. A file whose name contains a content hash cannot change contents without changing name, so it can be cached forever. A file whose name is stable must be revalidated, because its contents change on every deploy.

| Response class | Policy | Why |
|---|---|---|
| files under the client asset root whose filename carries a content hash, per `references/10-build-contract-and-artifacts.md` | `public, max-age=31536000, immutable` | content-hashed; a new build emits a new name |
| hashed fonts, images, and media under the client asset root | same | same |
| `index.html` and every SSR HTML response | `no-cache` | it is the document that names which hashed files to load |
| the service worker script and the precache manifest | `no-cache` | a cached service worker pins the previous asset base until its cache entry expires |
| `build-info.json` | `no-cache` | it must describe the deployment being served right now |
| the runtime config endpoint, if used | `no-store` | it exists precisely to change without a rebuild |

Applying one policy to every response type is the defect this table exists to prevent. `no-cache` means revalidate, not "do not cache"; `no-store` means do not write it down at all.

Un-hashed files must not be served from the client asset root. If a build emits one, that is an artifact-contract failure caught by gate 6, not a serving problem to be worked around with a header.

## Proxy obligations

These are obligations the serving layer must satisfy. The directives are `/alaa-haproxy` (`$alaa-haproxy`)'s to write.

- The asset path prefix arrives at the origin unchanged: no rewrite strips it, and no rewrite duplicates it.
- HTML responses are not stored under the immutable policy that applies to hashed assets.
- Compression is applied by content type, and the response body is byte-identical after decompression to the file on disk. A compression setting that alters bytes breaks Subresource Integrity, per `references/35-client-bundle-security.md`.
- Deep links resolve to the SPA or SSR entry, and a hard refresh on a deep link returns the same document as a client-side navigation to it.

## Remote asset origin

When browser assets are served from an origin other than the application host, this skill decides three things: that the origin is used, that the base matches the emitted URLs, and that the origin's contents are a superset of the currently-referenced hashed files during the overlap window of a deploy.

The bucket, its lifecycle rules, its access policy, its retention of superseded hashed files, and any invalidation call belong to the object-storage owner: `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) for a MinIO-backed origin and `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) for an ArvanCloud-backed one. The live `client` frontend pipeline uploads the extracted client asset tree to a MinIO bucket and serves it through a CDN host (`read: 2026-07-28`), so lifecycle questions about superseded assets go to the MinIO skill.

The single rule this skill will not delegate: **hashed assets from the previous release are not deleted until no served HTML references them.** A lifecycle rule that expires them on the deploy that supersedes them produces the half-propagated-CDN failure, and there is no header that recovers from it.

## Service worker

A deploy that changes the asset base must invalidate the precache manifest. The service-worker implementation, its update flow, and the precache manifest's generation belong to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/32-pwa-injectmanifest-guard.md`. The obligation that a base change reaches the manifest in the same build is this skill's.
