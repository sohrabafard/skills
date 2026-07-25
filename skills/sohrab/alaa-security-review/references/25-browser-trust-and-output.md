# Output Encoding, Browser Trust, And What Leaves The Service

Read when the change puts user-supplied content in a browser, touches a raw-HTML or sanitiser path, changes a cookie, CSP, or CSRF control, or newly returns identifiers, error detail, or personal data to a client.

## Context-aware output encoding

**Every value that reaches a browser is encoded for the exact context it lands in, by the framework's context-aware escaping.** The five contexts are HTML text, an HTML attribute value, a JavaScript string literal, a URL component, and a CSS value. They require different encodings, and a review of an interpolation names which context it examined.

One escaping function applied uniformly is not context-aware. HTML-escaping a value that lands inside a `javascript:` URL, inside an unquoted attribute, or inside a `<script>` block does not prevent execution, because the browser is not parsing HTML at that point.

Flag when: a value is escaped once and reused in a second context; a value is placed in an unquoted attribute; a server-rendered page embeds a JSON blob inside `<script>` without escaping `<`, `/`, and U+2028/U+2029; a URL is assembled by concatenation rather than through the platform's URL builder with per-component encoding.

## Raw HTML: exactly one path

**Exactly one code path in the repository renders untrusted HTML, and it runs the platform's sanctioned sanitiser.** On the frontend that is DOMPurify through `@alaa/sanitize-html` at the trust boundary (`/alaa-services-contract` owns the package boundary; this rule owns the invariant).

Two things are stop-the-line item 18, not P1 hardening:

- a second raw-HTML path added alongside the sanctioned one, because the sanitiser's guarantee is a property of there being one door
- a hand-written sanitiser - a regex, a tag blocklist, a string replace, an attribute stripper. HTML parsing is not a regular language, and every hand-rolled sanitiser in production history has been bypassed.

Sanitise on output, at the point of render, not only on input at write time. An input-time sanitiser is bypassed by any other writer to the same field - an import, a migration, an admin tool, a queue consumer - and by any later change to the sanitiser's own rules, which then apply to new rows only.

Flag every appearance of `v-html`, `dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, jQuery `.html()`, Blade `{!! !!}`, Twig `|raw`, Go `template.HTML`, Jinja `|safe`, `Markup()`, or any `SafeString` cast, on a value whose provenance is not a server-controlled constant. Each one is either the single sanctioned path or a finding.

## DOM sinks

Flag a request-derived or storage-derived value reaching: `eval`, `new Function`, `setTimeout` or `setInterval` with a string body, an assignment to `location`, `location.href`, or `window.open`, an `iframe` `src` or `srcdoc`, an `on*` attribute set from data, a dynamically constructed `<script src>` or `import()`, a framework's dynamic component name or dynamic template resolution, or a `postMessage` handler that acts on `event.data` without checking `event.origin` against an allowlist.

## Cookies

Every cookie that carries or contributes to authentication sets `HttpOnly`, `Secure`, and `SameSite` **explicitly**, with the `SameSite` value chosen and the reason recorded - `SameSite=None` requires `Secure` and a stated cross-site need. A cookie relying on a framework default is reported as not determined until the effective value is read from configuration.

Scope each cookie to the narrowest `Path` and host that works, and set `Domain` only when a subdomain genuinely needs the cookie: a `Domain` cookie is readable by every subdomain, so one compromised or user-controlled subdomain reads the session.

## Content Security Policy

A response that renders untrusted content carries a CSP whose script sources do not include `unsafe-inline` or `unsafe-eval`, and which does not admit script from a wildcard host. Where a strict policy is not achievable in the current application, the review records it as a finding with its severity and the reachable consequence - never as an accepted absence, and never omitted.

`object-src 'none'`, `base-uri 'self'`, and `frame-ancestors` are set, because each closes a bypass that script-source restrictions do not: plugin content, base-tag hijacking of every relative URL, and framing for clickjacking.

## CSRF

**Any state-changing request authenticated by an ambient credential requires an anti-CSRF control.** Ambient means the browser attaches it without the page's script choosing to: a cookie, HTTP basic or digest auth, or a TLS client certificate.

The acceptable controls are a per-session anti-CSRF token verified on every unsafe method, or `SameSite=Strict`/`Lax` combined with an `Origin` header check on every unsafe method. Where the second is chosen, the `Origin` check treats a missing `Origin` as a rejection, not as a pass.

An endpoint authenticated only by a bearer credential that page script must attach deliberately does not need a CSRF token. The review states which of the two models the endpoint uses, and flags an application that mixes both on the same route - a route that accepts either a cookie or a bearer token has the cookie's CSRF exposure regardless of the token.

Flag when: `GET` performs a state change; a CSRF exemption list has grown to include a state-changing route; a token is validated against a value the same request supplied twice (double-submit with no server-side binding).

## Frontend trust boundary

A component that renders never holds a credential. No page component, widget, or shared UI package holds an access token, a refresh credential, a step-up proof, or the ability to produce a trusted internal header; those live in the host and its SDK layer. A component that needs identity-derived data receives it as an input from the host.

Flag when: a rendering component reads a token from browser storage, a cookie, or a global; a public client sends an internal header whose name the trust boundary is documented to strip from client input (stop-the-line item 7); a credential is written to `localStorage` or `sessionStorage`, both of which are readable by any script that runs on the origin, including one injected through the single raw-HTML path.

## What a response may contain

- **Identifiers.** Every identifier in a response, URL, or log is either a value whose enumeration reveals nothing an authorized caller may not already know, or an unguessable server-generated public identifier. A sequential primary key in a client-visible position is a finding whose severity comes from what enumerating it reveals: P2 where the endpoint enforces per-object authorization and the id leaks only row counts and creation order, P0 where authorization is by possession of the identifier. Replacing an identifier is never the fix for a missing authorization check; the authorization check is the fix, and the identifier change is hardening on top of it.
- **Error detail.** A response carries a stable error code and a message safe for the caller. Stack traces, framework versions, SQL text, file paths, internal hostnames, and dependency error strings do not cross the boundary. The full detail is written to the structured log, correlated by the request id that the response does carry.
- **Uniform failure.** Authentication and authorization failures return one response shape and one code per class, for every cause. Nothing in the status, body, headers, or response time distinguishes an expired credential from a bad signature from an unknown key from an unknown subject. Likewise a missing object and an unauthorized object return the same response, so the endpoint is not an existence oracle - and the same rule covers login, password reset, invitation, and account-lookup endpoints, where a distinguishable response enumerates the user base.
- **Personal data.** A response returns the fields the caller's role in the product requires, chosen by an explicit per-endpoint output shape, not by serialising a model. Flag a serializer that emits every column, a `toArray()` on a model reaching a response, an eager-loaded relation whose fields were never chosen, and a debug or diff field that echoes prior values.
- **Logs, metrics, traces.** Personal data is masked or omitted at the call site; credentials and secrets are covered once, by the secrets rule in `50-credentials-and-cryptography.md`. No identifier of a person or tenant appears in a metric label, because label cardinality makes it permanent and queryable by anyone with dashboard access; use structured log fields or trace attributes when correlation is operationally required. `/alaa-observability-soc` owns the signal shape.
