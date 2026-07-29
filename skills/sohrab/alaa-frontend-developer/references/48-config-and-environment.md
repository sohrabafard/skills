# Configuration and Environment

How a frontend build and a frontend runtime get their values, and what the app must do with them before
it renders anything.

Which mechanism a repo uses — an inlined build-time constant, a runtime-fetched config document, a
templated placeholder in `index.html` — is decided by `/alaa-frontend-devops`
(`$alaa-frontend-devops`) `references/15-build-time-vs-runtime-config.md`, and the serving and public-path
half is `references/30-serving-caching-and-public-path.md` there. The Vue-shaped rule for reading a
`VITE_*` value in a component is `/alaa-vue-typescript-clean-code`
(`$alaa-vue-typescript-clean-code`) `references/72-frontend-security-binding.md`. This file states what
the application owes.

## Build-time and runtime are different values with different lifetimes

A `VITE_*` variable is **inlined into the bundle at build time**. It is not configuration: it is a
constant, it is public, and changing it requires a rebuild and a redeploy. Anything that must differ
between two deployments of the same artifact is runtime configuration and cannot be a `VITE_*` variable —
otherwise the artifact is not the same artifact, and `/alaa-frontend-devops` (`$alaa-frontend-devops`)
`references/25-artifact-identity-and-provenance.md` no longer holds.

Consequences the frontend must respect:

- Never put a secret in a `VITE_*` variable. See `25-frontend-security.md`.
- Never branch on an environment name (`if (env === 'production')`) to change behaviour. Name the
  capability instead, and let the value carry it.
- Never read `import.meta.env` from more than one module. One typed config module reads it; everything
  else imports from that module.

## Validate at the boundary, fail fast

The config module validates every injected value at boot, before the app mounts and before SSR renders:
presence, type, and shape — a URL parses, a number is a number, an enum is one of its members. A missing
or malformed value stops startup with a message naming the variable. It does not fall back to a silent
default and it does not surface three screens later as an undefined origin in a request.

A default is only permitted where the fallback is safe in production. A default that is convenient in
development and wrong in production is a defect that ships quietly.

## The single public-path source of truth

The app's public or base path has exactly one source, read through the config module and validated at
boot. Asset paths derive from it; no second copy is written in a component, a router, a service worker
template, or a stylesheet. A change to it is deploy-critical —
`/alaa-frontend-devops` (`$alaa-frontend-devops`) `references/30-serving-caching-and-public-path.md`.

## Values that belong to another owner

`STORAGE_*` and every object-storage endpoint, region and bucket default is consumed as given, never
branched on in code: `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) and
`/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`). Timeouts and retry budgets come from
`/alaa-reliability-sla` (`$alaa-reliability-sla`). Field limits and endpoint paths come from
`/alaa-services-contract` (`$alaa-services-contract`). The frontend's obligation is to make each of them
one validated value, not a literal repeated across call sites.

## Feature flags

A flag is read through the same config module and has a defined value when the flag source is
unreachable — the safe side of the flag, decided when the flag is created, not at the call site. A flag
is removed when the rollout completes; a flag that has been permanently on for two releases is dead code
holding a branch open. A flag never gates a security decision: that is an authorization decision and it
belongs on the server — `25-frontend-security.md`.

## Verification

Prove a configuration change by starting the app with the value absent and with the value malformed, and
observing that startup fails with the naming message. A config change verified only on the happy path has
not been verified.
