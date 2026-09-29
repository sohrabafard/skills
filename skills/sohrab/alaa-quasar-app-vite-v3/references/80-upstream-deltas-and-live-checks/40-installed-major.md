For exact version provenance and live-source authority, use [authority and API lookup](../05-authority-and-api-lookup.md); do not infer an unrecorded verification date from this split.

## 3. Detect the installed major before any shape advice

Read `package.json` and the lockfile before giving config, boot, env, alias, SSR, PWA, BEX, Electron, or Capacitor advice. A declared range is not proof of the installed version.

| Signal | `^2.x` maintenance | `^3.x` production |
| --- | --- | --- |
| Wrapper import | `#q-app/wrappers` | `#q-app` |
| Config extensions | `.js` `.mjs` `.ts` `.cjs` | `.js` `.ts` only |
| Constants | `process.env.MODE`, `process.env.DEV`, ... | `import.meta.env.QUASAR_MODE`, `import.meta.env.QUASAR_DEV`, ... |
| Env config | `build.envFolder`, `build.envFiles` | `build.env.folder`, `build.env.file`, `build.env.clientPrefix` |
| Defines | `build.rawDefine`, `build.env` injection | `build.define`, `build.defineEnv` |
| Aliases | `src/`, `components/`, `boot/`, `stores/`, `app/`, ... | `@/` only |
| CLI bundler for `/src-*` | esbuild | Rolldown |
| Custom service-worker folder | `/src-pwa/` | `/src-pwa/sw/` |
| SSR server | Express scaffold | Hono / Express / Fastify / Koa choice |
| Node floor | 18+ | 22+ (registry floor `22.22.0`) |

The exact `sourceFiles.pwaServiceWorker` default is owned by `references/32-pwa-injectmanifest-guard.md`; read it there rather than restating it.

✅ Do — report the detected line and use only its shapes. ❌ Don't — mix `#q-app/wrappers` and `#q-app`; each breaks the other line.

```ts
import { defineBoot } from '#q-app/wrappers' // breaks v3
import { defineBoot } from '#q-app'          // breaks v2
```

If the repo is greenfield and no line exists yet, state the assumption explicitly and use v3.
