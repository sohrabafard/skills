# Client Bundle Security

Open this file before adding a third-party script tag, a CSP directive, an `integrity` attribute, or any new value read from the environment at build time.

## What the premise costs

`SKILL.md` states the premise. What it costs in practice: an emitted chunk is archived by caches and crawlers outside your control, so removing it later does not unpublish it; and a value bundled into minified code is recoverable with a plain text search, so obfuscation buys nothing. Everything below follows.

## What must never enter a bundle

No value in any of these classes may appear in an emitted client chunk, in the emitted HTML, in the web app manifest, in the service worker, in a sourcemap, or in `build-info.json`:

- a credential of any kind: password, API key, bearer token, session secret, database URL with credentials, CI job token, registry token
- a private key or a signing key, symmetric or asymmetric
- an internal hostname, internal IP range, or internal service path that is not reachable from the public internet
- a customer identifier or any personal data belonging to someone other than the current user

Values that **are** allowed to be build-time and public, because they are already visible to any user: the public API base URL, a public project identifier, a feature flag default, a CSP source list, a public analytics or error-reporting DSN, and the provenance values in `references/25-artifact-identity-and-provenance.md`.

## The mechanism that enforces it

The build injects into client code only those environment variables whose names carry the client prefix. That prefix and its default are owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/21-cli-vite-and-config.md`; read the mechanism there.

This skill's gate is the output-side check, because the mechanism can be bypassed by a plugin, a `define`, an inlined literal, or a variable that was given a prefixed name by mistake. `scripts/verify-artifact-contract.mjs` scans every emitted chunk for the *values* of non-prefixed build environment variables and for secret-shaped literals, and exits non-zero naming the file and the offset. Passing the mechanism is not evidence; passing the gate is.

When the gate fires, the finding is a leaked-credential incident, not a build bug. Classify the exposure, decide rotation, and decide disclosure through `/alaa-security-review` (`$alaa-security-review`). Rotate before reverting: the value is already published and a revert does not unpublish it.

## Content Security Policy

The policy is this skill's because it is a property of what the build emits; the header emission is `/alaa-haproxy` (`$alaa-haproxy`)'s.

- A hashed-asset bundle needs no `'unsafe-inline'` and no `'unsafe-eval'` for scripts. `script-src 'self'` is achievable, because every script the build emits is an external file under the asset root. If a CSP for a frontend build contains `script-src ... 'unsafe-inline'`, an inline script is being emitted; find it and move it into a module.
- `style-src` may need `'unsafe-inline'` while a framework injects styles at runtime. Record that dependency on the same line as the directive so it is revisited, rather than left as folklore.
- Every remote origin the app talks to appears in `connect-src`, every media origin in `media-src`, and every image origin in `img-src`. Adding a remote asset origin without adding it to the policy produces a failure that is invisible in development and total in production.
- When assets are served from a remote origin, that origin appears in `script-src` and `style-src` too, or the hashed chunks will not load.
- Prefer the response header over the `<meta http-equiv>` form; the meta form cannot express `frame-ancestors` or `report-uri`, and it applies only after parsing begins. The live `client` SPA ships its policy as a build-time `<meta http-equiv="Content-Security-Policy">` with a build-time image-source list (`read: 2026-07-28`), so a change to an image origin there requires a rebuild.

## Subresource Integrity

SRI is for resources this build did not emit. Applying it to your own hashed chunks buys nothing, because the content hash in the filename already binds name to bytes, and a rebuild would then require rewriting every integrity attribute.

Apply `integrity` to every `<script>` and `<link rel=stylesheet>` that loads from an origin you do not control. Rules that hold today (`read: 2026-07-28`, https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity):

- The hash algorithm is `sha256`, `sha384`, or `sha512`; the browser uses the strongest one present.
- A cross-origin resource with `integrity` also needs `crossorigin="anonymous"` and an `Access-Control-Allow-Origin` response header, or it loads in `no-cors` mode and SRI cannot be evaluated.
- On mismatch the browser refuses the resource and reports a network error. Plan for the failure: a third-party script guarded by SRI must not be on the critical rendering path.

## Third-party scripts

Every third-party script tag in the emitted HTML is a party that can read every token in the page and every keystroke in every form. Before one is added, record in the merge request: who the vendor is, what URL is loaded, whether the URL is versioned or floating, whether SRI is applied, and what breaks if it is removed. A floating URL from a third party with no SRI is a standing permission for that vendor to run arbitrary code on your users; if it is accepted, it is accepted by `/alaa-security-review` (`$alaa-security-review`), not by the person adding the tag.

Threat classification, exposure severity, disclosure, and rotation policy are `/alaa-security-review` (`$alaa-security-review`)'s. What the artifact may contain and what the gate asserts are this skill's.
