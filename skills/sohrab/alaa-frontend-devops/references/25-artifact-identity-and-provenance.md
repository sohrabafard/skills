# Artifact Identity and Provenance

Open this file when you cannot answer "which commit produced the bundle currently serving production", or when adding a build metadata file, an image label, a version endpoint, or a sourcemap upload step.

## The chain

`SKILL.md` states the requirement. The chain it needs has three links, not one: the commit, the lockfile state that commit resolved to, and the toolchain that ran. A commit alone is insufficient, because a dependency range can resolve differently on two days and a toolchain can change with no commit at all.

## The provenance file

Every build emits one JSON file beside the artifact, at `<client-asset-root>/../build-info.json`, containing exactly these keys:

| Key | Value | Why it is needed |
|---|---|---|
| `commit` | the full 40-character commit SHA | the only durable link from bytes to source |
| `ref` | the branch or tag the pipeline ran on | distinguishes a hotfix build from a release build of the same tree |
| `builtAt` | ISO 8601 UTC timestamp | orders two builds of the same commit |
| `nodeVersion` | `process.version` of the build | a toolchain change with an unchanged commit is otherwise invisible |
| `packageManager` | the `name@version` that installed | same |
| `lockfileHash` | SHA-256 of the lockfile as installed | proves the dependency graph, which the commit alone does not when a range resolved differently |
| `buildMode` | `spa`, `pwa`, or `ssr` | three modes emit three different trees from one commit |

The file is emitted by the build step, not by the publish step, so that an artifact copied out of an image carries it. It is served, so an operator can fetch it from a running deployment; it is `Cache-Control: no-cache`, for the same reason `index.html` is.

Nothing secret goes in this file. It is served publicly, which makes it subject to `references/35-client-bundle-security.md`. A commit SHA and a lockfile hash are not secrets; an internal registry URL, a build machine hostname, and a CI job token are.

## Image labelling

The runtime image carries `org.opencontainers.image.revision` set to the same commit SHA and `org.opencontainers.image.created` set to the same timestamp. Two identifiers that can disagree are worse than one, so they are written from the same values that produced `build-info.json`, in the same step.

Where those labels are written in the Dockerfile is `/alaa-docker-production` (`$alaa-docker-production`)'s ground. That the values must exist and must match the provenance file is this skill's gate.

## Sourcemap policy

State one of these two in `AGENTS.md` and enforce it in the artifact gate.

- **Not emitted.** No `.map` file is produced for a production build. Stack traces from production are minified and are decoded only by rebuilding the exact commit. Cheapest, and it is the live `client` posture today: the emitted production tree contains zero `.map` files (`read: 2026-07-28`).
- **Emitted and uploaded, never served.** Maps are produced, uploaded to the error-tracking backend as part of the release, then deleted from the artifact before publish. The gate asserts that no `.map` file exists under the published asset root.

A third state — maps emitted and served publicly — is not a policy. It publishes the original source, which puts the whole of `references/35-client-bundle-security.md` back in play, and it is what happens by default when nobody chooses.

## Traceability at runtime

An SSR deployment exposes the provenance values on one unauthenticated endpoint returning the same JSON as `build-info.json`. A static deployment relies on the file itself being fetchable. Either way, the operator's first command during an incident is a fetch of that document, and the playbook in `references/45-deploy-failure-playbook.md` starts there.

## Retention and alerting

How long provenance records are kept, and whether a deploy emits an event to the observability stack, belongs to `/alaa-observability-soc` (`$alaa-observability-soc`). This skill requires that the values exist in the artifact; it does not decide where they are stored afterwards.
