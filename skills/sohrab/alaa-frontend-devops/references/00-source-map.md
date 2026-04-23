# Source Map

Use this file when frontend delivery guidance depends on current tool behavior, release notes, security posture, or deployment semantics.

## Source Priority

Prefer sources in this order:

1. Repo-local files: `package.json`, lockfile, CI workflow, Dockerfile, Compose files, proxy config, and deploy docs.
2. Official framework and tool docs:
   - Quasar CLI with Vite docs: https://quasar.dev/quasar-cli-vite/
   - Quasar upgrade guide: https://quasar.dev/quasar-cli-vite/upgrade-guide/
   - Vite docs and migration guide: https://vite.dev/
   - Vue docs and release policy: https://vuejs.org/
   - Workbox docs: https://developer.chrome.com/docs/workbox
3. Official release and package metadata:
   - npm registry data for `vue`, `quasar`, `@quasar/app-vite`, `vite`, and `workbox-build`
   - upstream GitHub releases and changelogs when package metadata is not enough
4. Platform docs for the deployment target: GitHub Actions, GitLab CI, Docker, Nginx, HAProxy, Kubernetes, CDN, or hosting vendor docs.
5. Community posts, StackOverflow answers, and issue comments only as troubleshooting clues.

## Freshness Triggers

Re-check official sources before changing advice when the task includes:

- "latest", "current", "upgrade", "migration", "security", "CVE", "breaking change", or "release"
- Node, Vite, Quasar CLI, Workbox, or SSR runtime version bumps
- cache behavior, public path, CDN asset base, service-worker update flow, or remote asset serving
- Docker base-image changes, lockfile changes, CI image changes, or package-manager changes
- production-only SSR failures, hydration mismatch after deploy, or missing chunks after release

## Community Troubleshooting Boundary

Use community material to find possible failure modes, not as the source of final guidance.

Good use:

- finding a known proxy timeout symptom
- identifying a common CDN cache-invalidation mistake
- discovering a package-manager edge case to verify locally

Bad use:

- changing Node or Quasar support policy based on a forum answer
- copying a Dockerfile workaround without checking official image and package docs
- treating a single GitHub issue comment as proof of current behavior

## Small Anti-Pattern

Anti-pattern: fixing missing chunks by disabling cache everywhere.

Better path: verify `publicPath` or asset base, immutable hashed assets, HTML cache policy, service-worker update semantics, and rollback behavior. A cache bypass can hide the real artifact-contract bug and make the next release harder to debug.
