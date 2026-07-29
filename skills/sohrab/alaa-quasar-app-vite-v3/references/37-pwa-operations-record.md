# PWA operations record

You are about to ship a Quasar PWA change and hand the running result to whoever operates it. A change that alters caching, update, or offline behaviour ships with an operations record. Without it the next person to face a stale page, a white screen after deploy, or an offline complaint has to reverse-engineer the service worker to answer a support ticket.

**The record is a file in the repository, not a paragraph in a merge request.** Put it where the repo already keeps operational documents; if the repo has none, `docs/pwa-operations.md` beside `src-pwa/`. It is updated in the same change that alters the behaviour it describes, and it names the date it was last verified.

Scope: this record documents what the shipped artifact does and how it fails. Deploy pipelines, container images, and rollback mechanics belong to `/alaa-frontend-devops` (`$alaa-frontend-devops`); provider CI YAML belongs to `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`).

## 1. Required contents

| Section | What it must state | Why an operator needs it |
| --- | --- | --- |
| Workbox mode | `GenerateSW` or `InjectManifest`, and — when a `src-pwa/sw/` source exists — which one the CLI actually builds | a custom service worker present under `src-pwa/sw/` while `pwa.workboxMode` is `GenerateSW` is not shipped; the file is dead code and its rules are not in effect |
| Cache-name and version contract | every `cacheName` the app creates, what it holds, its `ExpirationPlugin` settings, and the rule by which a name changes between releases | an operator clearing "the cache" must know which names are safe to delete and which hold user-visible state |
| Precache scope | what is precached, what is excluded, and the `maximumFileSizeToCacheInBytes` and `globIgnores` in force | explains install size and why a given asset is or is not available offline |
| Update UX | the exact user-visible sequence from a new build being detected to the reload, including who sees the prompt and what it says | support cannot tell a user "reload" if the app is designed to prompt |
| Offline degradation matrix | the route-by-route table from `references/34-frontend-failure-and-degradation.md` §3 | turns "the app is broken offline" into "this route is documented as hard-fail" |
| Kill switch | the path of the kill-switch service worker, the date it was last tested, and the exact deploy step that publishes it | an untested kill switch is not a kill switch |
| Service-worker build identifier | how a running service worker's build is identified from the browser, and where that identifier appears in telemetry | a lifecycle event that cannot be tied to a build is unusable — see `references/36-client-observability-contract.md` §5 |
| Rollback boundary | how many deploy generations of hashed assets are retained, and what breaks when an older client requests a purged asset | sets the minimum retention the CDN must honour |
| Verification date and result | when install, update, and offline were last exercised, and on which browsers | separates "we believe it works" from "it worked on this date" |

## 2. Rules

- **A change to any row above updates the record in the same change.** A record whose verification date predates the current service-worker source is stale and must be treated as unverified.
- **The record states the cache names that exist, not the ones intended.** Read them from the service-worker source; a renamed cache that the record still lists under the old name causes an operator to delete the wrong one.
- **The record names what breaks, not only what works.** For each documented failure it names the smallest recovery an operator can perform without a deploy.
- **Version-sensitive claims in the record point at `references/80-upstream-deltas-and-live-checks.md`** rather than repeating a version number, so the record does not silently go stale with the toolchain.
- **The record is not a substitute for the checks.** The install, update, and offline verification set is `references/32-pwa-injectmanifest-guard.md`, and the automated regressions are `references/75-testing-ci-playbook.md`. The record states their results; it does not replace running them.

## 3. Template

```md
# PWA operations record

Last verified: <ISO date> by <name>, on <browsers>

## Build
- Workbox mode: <GenerateSW | InjectManifest>
- Service-worker source: <path, or "generated">
- Service-worker build identifier: <how to read it from the browser>

## Caches
| cacheName | Holds | Strategy | Expiration | Changes when |
|---|---|---|---|---|

## Precache
- Included: <...>
- Excluded: <globIgnores, maximumFileSizeToCacheInBytes>

## Update UX
1. <detection>
2. <what the user sees, verbatim copy>
3. <what happens on acceptance>
4. <what happens if the user declines>

## Offline matrix
| Route | Works offline / Degrades / Hard fails | Proven by |
|---|---|---|

## Kill switch
- Path: <...>
- Last tested: <ISO date>
- Deploy step: <...>

## Rollback
- Hashed-asset retention: <N deploy generations>
- Symptom when exceeded: <...>

## Known failures and smallest recovery
| Symptom | Recovery without a deploy |
|---|---|
```

✅ Do — update the record and its verification date in the change that alters caching, update, or offline behaviour. ❌ Don't — ship a service-worker change whose cache names and update prompt exist only in the source; the operator answering the support ticket does not read the source.

Search: `operations record`, `runbook`, `cacheName`, `precache scope`, `update UX`, `offline matrix`, `kill switch`, `rollback boundary`, `asset retention`, `verification date`.
