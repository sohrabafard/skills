# Frontend security — the Vue binding

**`/alaa-security-review` (`$alaa-security-review`) owns the threat classes, the sanctioned sanitiser, the
fail-closed rule, CSP, and cookie policy.** **`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) owns
the trust boundary.** **`/alaa-permission-generator` (`$alaa-permission-generator`) owns the permission
bitmap contract and the canonical TypeScript decoder.** This file states only what that means for the shape
of Vue code, and it restates none of their rules.

Read it before writing `v-html`, rendering content a user or third party supplied, reading a permission in
a component or a guard, adding a `VITE_` variable, building a cache or storage key, or parsing or
formatting an identifier.

## `v-html` and untrusted content

`v-html` sets `innerHTML`. A string reaching it executes as markup, including `<script>` in some contexts,
`on*` attributes, `javascript:` URLs, and `<img onerror>`. Vue's interpolation (`{{ }}`) escapes; `v-html`
by definition does not, which is the entire reason it exists.

The binding:

- **Prefer not rendering HTML at all.** Text interpolation, a component that renders structured data, or a
  Markdown renderer configured to emit a restricted node set solves most cases that reach for `v-html`.
- **Exactly one code path in the repository renders untrusted HTML, and it runs the platform's sanctioned
  sanitiser.** That path and that sanitiser are named by
  `/alaa-security-review` (`$alaa-security-review`), `references/25-browser-trust-and-output.md`. Adding a
  second raw-HTML path is a finding even if the second path also sanitises, because the guarantee is a
  property of there being one door.
- **A hand-written sanitiser is never written here** — no regex, no tag blocklist, no string replace, no
  attribute stripper.
- Sanitise at the point of render, not only at write time. An input-time sanitiser is bypassed by every
  other writer to the same field: an import, a migration, an admin tool, a queue consumer.
- `v-html` never receives a value derived from a route param, a query string, `localStorage`, a
  `postMessage` payload, or an API field whose provenance you have not established.

Every occurrence of `v-html`, `innerHTML`, `outerHTML`, `insertAdjacentHTML`, or a dynamic component name
built from data is either the one sanctioned path or a finding to report.

## A client-side permission check is a UI hint, never an authorization decision

A browser may decode its **own** access token to derive UI capability state — which buttons to show, which
routes to offer. That is all it may derive.

The binding, and every clause of it is load-bearing:

- **The decode never gates a security decision.** The gateway and the owning service stay authoritative,
  and a deny response is the only authoritative answer. A screen that hides a button must still expect the
  action to be refused, and must handle that refusal as a real outcome rather than an impossible one.
- **Name the function so the boundary is unmissable.** The live `client` uses
  `decodeUnverifiedUiAuthorization`, and the naming is the point: a reviewer reading the call site can see
  that the value is unverified without opening the definition.
- **The decoder is imported, never rewritten.** The canonical TypeScript decoder, the bitmap layout, the
  fingerprint, and the generated permission maps belong to
  `/alaa-permission-generator` (`$alaa-permission-generator`). A second decoder in application code is a
  finding.
- **It fails closed and it is bounded.** Malformed input grants nothing and throws nothing; unknown,
  deprecated, and reserved bits grant nothing, so a token issued against a newer catalog degrades to fewer
  hints. The decoded bitmap length is capped — the live `client` caps it at 512 bytes — and the cap exists
  so a crafted token cannot make the browser allocate without limit. Do not remove a cap to fit a larger
  catalog; the catalog scale is the owner's decision.
- **A valid token with an empty bitmap is a legitimate ready state.** It never invalidates the session and
  never logs the user out.
- **Never send a gateway-owned authorization header from a client.** Decoding a claim from your own token
  is not the same as asserting a trusted header, and
  `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) wins on any conflict.
- Application code compares against generated permission constants, never a raw string and never a bit id.

Route `meta` declares posture and guards read it (`50-quasar-vite-pinia-contract.md`). A guard's conclusion
is a routing decision, not an authorization decision, and the same rules above apply to it unchanged.

## Secrets and `VITE_*`

**Every `VITE_*` value is public.** Vite inlines it into the client bundle at build time, so it ships to
every user and is readable in devtools. An API key, a shared secret, a signing key, a database credential,
or an admin token in a `VITE_*` variable is a disclosed secret from the moment it builds, and rotating the
variable does not un-ship the bundles already served.

Anything secret is held server-side and reached through an endpoint. Environment access stays behind one
typed config module (`50-quasar-vite-pinia-contract.md`), which makes the full list of what ships readable
in one file.

## Tenant and user scope in every key

**Every cache key, storage key, and in-memory memo key includes the user or tenant scope.** Without it, a
second account signing in on the same browser reads the first account's cached data, and the bug looks like
a backend authorization failure while the server never saw the request.

The same applies to a service-worker cache, to `localStorage` and `sessionStorage`, and to IndexedDB
(`/alaa-indexeddb-browser-storage`, `$alaa-indexeddb-browser-storage`). Clear or partition scoped storage
on sign-out and on account switch. Which key names are used is
`/alaa-services-contract` (`$alaa-services-contract`).

## Identifiers

Identifiers are encoded and decoded through the shared codec, never with a local
`toUpperCase`/`replace`/`slice` approximation:
`/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`).

Its `scripts/codec-conformance.sh` is **run, not reasoned about.** When a change touches identifier
formatting, parsing, display, or validation, execute the script and report its observed output. A statement
that the implementation "matches the contract" without that run is not evidence, and the class of bug it
catches — a canonicalisation difference between two services — is invisible until two systems disagree
about whether two ids are the same id.

## Input normalization

**A validator or a formatter never enumerates characters. An enumerated character list is a defect class,
not a fix.** Two rounds of "add the missing character to the list" preceded the settled category rule, and
each round shipped believing the list was now complete.

The binding:

- Every free-text and numeric input field is normalized **on submit**, through the shared implementation,
  before the value is sent. The submit pipeline is where it runs
  (`43-behavioral-patterns.md`, Pipeline).
- A hand-rolled `replace`, a per-field regex, or a component-local digit map is a finding, even when it
  passes the case in front of you.
- **A `str.isdigit()`-style check is forbidden**, in every language and in its JavaScript equivalents,
  because it accepts non-ASCII digits: a Persian or Arabic-Indic digit passes the check and then fails
  arithmetic, comparison, or the backend's parser, far from where it entered.
- The browser normalizing is not sufficient on its own. Every backend service normalizes again in
  middleware, and the two must agree byte for byte.

**The rule itself, the canonical implementations, and the conformance corpus belong to
`/alaa-input-normalization` (`$alaa-input-normalization`).** Do not write a folding table, a digit map, or
a character class here or in application code — cite the owner and call its implementation.

Input length limits (`maxlength`) and other field constraints are values, and values are
`/alaa-services-contract` (`$alaa-services-contract`).
