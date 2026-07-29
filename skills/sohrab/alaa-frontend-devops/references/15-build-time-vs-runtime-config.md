# Build-Time Versus Runtime Configuration

Open this file when a configuration value differs per environment and is not known when `build` runs, or when writing a Compose variable reference for the frontend runtime container.

## The decision

A client bundle is immutable once emitted. Ask one question of every configuration value: **is this value the same for every environment that will ever receive this artifact?**

- **Yes** — it is build-time. It is compiled into the bundle. It is public. It changes only by rebuilding.
- **No** — it is runtime. It must not be compiled in, because compiling it in means one artifact per environment, and one artifact per environment means the artifact you tested is not the artifact you shipped.

A value that is build-time and secret has no valid home; see `references/35-client-bundle-security.md`.

The build-side injection mechanism — `build.env`, `build.env.clientPrefix` and its default, and which variables are allowed to reach client code — is owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/21-cli-vite-and-config.md`. Read it there; this file does not restate it.

## The three runtime mechanisms

Pick one per repository and state which one in `AGENTS.md`. Mixing two means a value can disagree with itself.

1. **Runtime config endpoint.** The serving layer exposes a small JSON document; the app fetches it before its first authenticated call. Cost: one round trip on cold start, and the document must be served `Cache-Control: no-store` or it will outlive the deploy that changed it. Use when values change without a deploy.
2. **Entrypoint-substituted placeholders.** The container entrypoint rewrites named placeholders in the emitted HTML at start-up, before the server accepts traffic. Cost: the artifact is mutated in place, so the file hash no longer identifies the content; the provenance file must record the pre-substitution digest. Use when values are fixed for the container's lifetime.
3. **Serving-layer-injected global.** The proxy or the SSR renderer injects a `<script>` defining one global object into the HTML response. Cost: it is per-response, so it cannot be cached with the HTML unless the HTML is already `no-cache`. The directive that performs the injection belongs to `/alaa-haproxy` (`$alaa-haproxy`); the decision that a value is delivered this way is this skill's.

Whichever is chosen: the app reads the value through exactly one accessor module. A component that reads the raw global or refetches the endpoint is a defect, because it makes the value's source unfindable.

## The Compose interpolation invariant

Fleet law, ratified 2026-07-28. It applies to every Compose file that starts a frontend runtime container. It is a **configuration gate on the frontend runtime container**: this skill states the invariant and asserts it; the Compose file's authorship — its services, its build stanza, its networks, its volumes — belongs to `/alaa-docker-production` (`$alaa-docker-production`).

- A **mandatory** variable is written `${VAR:?message}`. If it is unset or empty, Compose exits non-zero with `message` and the container never starts. Fail closed.
- A **deliberately optional** variable is written `${VAR:-default}`. Writing this form is a statement that the default is correct in production, not a convenience.
- A variable **whose default would silently disable a safety control** — an auth toggle, a TLS verification flag, a rate limit, a CSP source list, a signing key — is written `${VAR:?message}` with **no default permitted at all**. There is no acceptable fallback for a control that fails open.

Compose interpolation reads **the shell environment and `--env-file` (including the project `.env`) only**. It **never** reads the service-level `env_file:` key. Variables listed under `env_file:` reach the container's environment and nothing else; a `${VAR:?}` in the Compose file that depends on them fails every time. If a value is needed both for interpolation and inside the container, it must be in the `--env-file`/`.env` source, and the container must receive it by an explicit `environment:` entry.

*(Verified against https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/ and the Compose environment-variable precedence documentation, read: 2026-07-28.)*

## Asserting it

Before a Compose change to a frontend runtime container merges, run `docker compose config` with the mandatory variables unset and confirm it exits non-zero naming the missing variable. A Compose file that renders successfully with no environment at all has no mandatory variables, which for a frontend runtime container is itself the finding.

## Locale and text handling in a build step

If a build step, a generated file, or a runtime configuration value carries non-ASCII digits, the fleet's normalization rule applies and this skill does not restate it: `/alaa-input-normalization` (`$alaa-input-normalization`).
