## 1. Refresh before answering

```bash
node <skill-dir>/scripts/check-upstream-versions.mjs
node <skill-dir>/scripts/check-upstream-versions.mjs --help
node <skill-dir>/scripts/check-upstream-versions.mjs --self-test
```

Exit codes: `0` clean, `2` one or more packages could not be fetched (the rest are still printed), `3` bad usage. Treat `2` as "could not run", never as "clean". Manual fallback when the script cannot run:

```bash
npm view @quasar/app-vite dist-tags
npm view "@quasar/app-vite@^2" version
npm view quasar version
npm view vite version
npm view vue version
npm view vue-router version
npm view pinia version
npm view workbox-build version
```

Yarn repos may use `yarn info <pkg> version`; the script is preferred because its summary is package-manager-neutral.

Authority, highest first: (1) the repo — `quasar.config`, `package.json`, lockfile, boot/SSR/PWA files, tests; the **installed** `@quasar/app-vite` decides the line; (2) official Quasar docs and the CLI-Vite upgrade guide; (3) official Vite/Vue/Router/Pinia/Workbox docs; (4) npm registry metadata, GitHub releases, changelogs; (5) community material as troubleshooting leads only. A community example never overrides installed-version or official guidance.

Recheck official sources whenever the question contains "latest", "current", "upgrade", "migration", "security", "CVE", or "breaking"; whenever Quasar CLI, Vite, Vue, Router, Pinia, Workbox, Node, or the package manager changes; whenever SSR middleware, the PWA service worker, the BEX bridge, Electron/Capacitor packaging, or a config format changes; and whenever dev and production disagree.
