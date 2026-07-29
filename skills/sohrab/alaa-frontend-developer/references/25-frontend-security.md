# Frontend Security — what the browser half owes

Threat classes, review triggers and fail-closed doctrine belong to `/alaa-security-review`
(`$alaa-security-review`): `references/10-fast-gate.md` to decide whether a change needs review,
`references/25-browser-trust-and-output.md` for browser trust and output encoding,
`references/20-untrusted-input.md` for untrusted input, `references/40-authorization-and-tenancy.md` for
authorization and tenancy. The Vue-shaped mechanics of the same three surfaces are
`/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`)
`references/72-frontend-security-binding.md`. The gateway trust boundary is `/alaa-trust-gateway-auth`
(`$alaa-trust-gateway-auth`) `references/10-verification-and-ingress.md`.

This file states the frontend obligations those owners assume are met.

## The binding rule: the permission bitmap is a UI hint

A permission decoded in the browser selects what to render. It never decides what is allowed. A route
guard, a `v-if`, a disabled button and a hidden menu item are all presentation. Every action they gate is
authorized again on the server, and a request that arrives without the UI having gated it must fail there.

- Decode with the canonical decoder from `/alaa-permission-generator` (`$alaa-permission-generator`)
  `assets/permission-bitmap/permission-bitmap.ts`; the consumer contract is
  `references/typescript-consumer.md` there. Do not hand-roll bit arithmetic in a component.
- A decode comment that records a security assumption carries a verification date; the staleness contract
  is `/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`)
  `references/60-staleness-and-verification.md`.
- Step-up and re-authentication hints in the UI are `/alaa-quasar-app-vite-v3`
  (`$alaa-quasar-app-vite-v3`) `references/41-step-up-and-permission-hints.md`.

## Rendering untrusted content

- `v-html` on a value that any user, tenant or third party can influence is prohibited. Render as text, or
  sanitize with a maintained library at the single boundary where the value enters the app — never in
  the template, and never twice.
- A URL from data is validated for scheme before it becomes an `href`, a `src`, a `window.open` target or
  a router destination. `javascript:`, `data:` and `blob:` are rejected unless the feature exists
  specifically to serve them.
- `target="_blank"` carries `rel="noopener noreferrer"`.
- A filename, a tenant name, or any other data rendered into a template is text; it is never assembled
  into markup by string concatenation.
- Which content is untrusted, and how a UI signals that it is showing something it does not vouch for, is
  `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/25-untrusted-content-and-ui-authority.md`.

## Cross-origin messages

A `message` listener checks `event.origin` against an allowlist before reading `event.data`, and
`postMessage` names an exact target origin — never `'*'`. An unchecked listener is an unauthenticated
input from any page that can open a frame.

## What must never be in the client bundle

A secret, a signing key, a service credential, a database URL, or an admin endpoint that relies on being
unknown. Everything in the bundle is public the moment it ships. `VITE_*` naming, boundary validation and
what may legitimately be injected are `48-config-and-environment.md`; the shipped-bundle scan is
`/alaa-frontend-devops` (`$alaa-frontend-devops`) `references/35-client-bundle-security.md`.

## CSP and nonces

If the app serves a Content-Security-Policy, an inline `<script>` or `<style>` added by a frontend change
must carry the server-issued nonce or it silently stops executing in production while working in the dev
server. Do not relax the policy to make a change work; the policy is a server-side contract and widening
it is a `/alaa-security-review` (`$alaa-security-review`) trigger.

## Media and object URLs

A presigned or expiring media URL is a credential in a query string: it is not logged, not put in an
analytics event, and not persisted beyond its lifetime. The player-side handling is `/alaa-shaka-player`
(`$alaa-shaka-player`) `references/42-media-url-trust-and-presigned.md`; the issuing side is
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`).

## Review triggers this file hands over

A new auth flow, a new cross-origin surface, a new upload path, a change to what a permission gates, or a
new third-party script — each is a `/alaa-security-review` (`$alaa-security-review`)
`references/10-fast-gate.md` entry, not a judgement made inside the frontend change.
