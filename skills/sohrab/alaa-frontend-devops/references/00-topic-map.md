# Topic Map

The single router for this skill. Every row names an observable situation. Match your situation, open that one file, and stop.

## Routes

| You are about to… | Read |
|---|---|
| change `publicPath`, an asset base, a CDN origin, or a path prefix that appears in a browser URL | `references/30-serving-caching-and-public-path.md` |
| decide the `Cache-Control` policy for a response class, or explain why a chunk was served stale | `references/30-serving-caching-and-public-path.md` |
| add, remove, or reorder a check that can block a merge or a release for a frontend repository | `references/20-ci-gates-and-predicates.md` |
| change the install command, the lockfile handling, the Node version, or a CI cache key input | `references/20-ci-gates-and-predicates.md` |
| introduce a configuration value that differs per environment and is not known when `build` runs | `references/15-build-time-vs-runtime-config.md` |
| write or change a Compose variable reference for the frontend runtime container | `references/15-build-time-vs-runtime-config.md` |
| answer "which commit produced the bundle currently serving production" and find you cannot | `references/25-artifact-identity-and-provenance.md` |
| add a build metadata file, an image label, a version endpoint, or a sourcemap upload step | `references/25-artifact-identity-and-provenance.md` |
| add a third-party script tag, a CSP directive, an `integrity` attribute, or any new value read from the environment at build time | `references/35-client-bundle-security.md` |
| assert what a build must emit and where, before packaging or uploading it | `references/10-build-contract-and-artifacts.md` |
| close out a delivery change and say what you validated | `references/40-verification-and-rollback.md` |
| face a live symptom: a failed deploy, chunks that 404, an `index.html` pointing at assets that are gone, a service worker serving the previous base, two pipelines publishing at once, or a release that must be undone | `references/45-deploy-failure-playbook.md` |
| decide whether a rule belongs to this skill or to another owner, or need the file path inside that owner's skill | `references/90-companion-boundary.md` |
| assert a version, a security posture, or a "current behaviour" claim that this skill does not already state | `references/00-source-map.md` |

## Verification shapes

Use this table to pick which gates apply to the build mode in the task. Each row's gates and predicates are in `references/20-ci-gates-and-predicates.md`; the assertions are executed by `scripts/verify-artifact-contract.mjs`.

| Build mode | Gates that must pass before the artifact is published |
|---|---|
| SPA | emitted HTML references only assets that exist; every emitted chunk filename is content-hashed; no secret-shaped value in any chunk; provenance file present |
| PWA | the SPA gates, plus: the precache manifest lists only assets that exist, and a change to the asset base invalidates the precache manifest |
| SSR | the SPA gates applied to the client sub-tree, plus: the SSR runtime entry exists at the declared path, and the client manifest resolves entirely inside the client asset root |
| package-consumer | the assets each workspace package declares are present in the final client asset output. Whether they are reachable from an entry is `/alaa-mono-package` (`$alaa-mono-package`), `references/30-assets-css-and-ssr-client-assets.md` |
