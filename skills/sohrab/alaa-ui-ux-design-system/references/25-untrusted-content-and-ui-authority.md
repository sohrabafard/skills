# Untrusted Content and UI Authority

Read this file when a component will render a value the product did not author, when a user can paste into a surface, or when the interface shows or hides something based on a permission.

Two questions, one file: *what may this component render*, and *what does the interface's appearance actually guarantee*. The answer to the second is: nothing, ever.

## 1. The UI is never an authorization decision

**Hiding or disabling a control is a presentation choice and never a security control.** It is a courtesy to the user, not a boundary. Anyone can open the console, replay the request, edit the store, or call the endpoint directly.

What follows, as design rules:

- **Never design a flow whose safety depends on a control being hidden.** If the only thing preventing an action is that the button is not rendered, the action is unprotected. The server-side boundary is owned by `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`); design as though every hidden control were visible.
- **Never hide something to keep it secret.** A value present in the DOM, in a store, in a JSON payload, or in a bundle is disclosed regardless of `display: none`, `v-if`, opacity, or z-index. If the user must not learn it, it must not reach the browser.
- **A capability hint may shape the interface and skip a request. It may not stand in for the answer.** A deny response from the server is the only authoritative answer, and the interface must render that answer well rather than assume it will never arrive. `client` states this correctly in `src/stores/authPermissions.ts`; that framing is the fleet's, and this file is where the design consequence lives.
- **The hint can be wrong or absent.** It goes stale between token refreshes, it is empty before the first token arrives, and it is unavailable during server-side rendering. Every permission-shaped surface therefore has a designed appearance for "not yet known" that is neither the granted nor the denied appearance. Which visual treatment to use is in `15-designed-failure-states.md`.

**Fake affordance, defined so it is checkable:** any control that looks actionable and cannot act, any control that looks inert and will act, and any state indicator that reports a result the system has not confirmed. Each is a blocking defect, not a polish item.

The bit meanings are owned by `/alaa-services-contract` (`$alaa-services-contract`); the decoder by `/alaa-permission-generator` (`$alaa-permission-generator`). Neither is restated here.

## 2. What a component may render from untrusted content

"Untrusted" means any value that did not originate in this repository: a request body, a URL or query parameter, an upload, a filename, a value authored by another user or another tenant, and anything read from local storage.

The default and the exceptions:

- **Default: render untrusted values as text.** Text interpolation is safe by construction; it needs no review and no allowlist.
- **Rich text is an explicit, documented exception.** A component may render untrusted markup only when (a) the content is sanitized by the repository's designated sanitizer immediately before render, (b) the component's documentation names that sanitizer, and (c) the allowed tag and attribute set is written down. `client` meets this on its one such surface: `src/news/NewsShowRoutePage.vue:55` renders through `@alaa/sanitize-html` and records the provenance in `src/model/news-provenance.ts`. A second `v-html` site added without those three conditions is a defect.
- **A server that claims to have sanitized is not sufficient.** Sanitize at render, in the browser, even when the producing service also sanitizes. The two are not one control.
- **Never build markup by concatenating an untrusted value into a template string.** Sanitizing after concatenation is not equivalent to never concatenating.
- **URLs from untrusted content** are rendered as links only after their scheme is checked against an allowlist (`https:`, `mailto:`, and the app's own relative paths). `javascript:`, `data:` and `blob:` are never linkable from untrusted content.
- **Untrusted values in attributes** — `src`, `href`, `style`, `srcdoc`, `formaction` — are the same hole as untrusted markup and get the same treatment.
- **Untrusted values inside SVG** carry script; an uploaded SVG is rendered as an image with a fixed extension check, never inlined into the document.
- **An icon or badge chosen by an untrusted value** is resolved through a closed map with a default. A component that constructs an icon name or a CSS class from user content is a defect regardless of escaping.
- **Length is a rendering input.** Every untrusted string has a designed maximum rendered length with a defined overflow treatment. A title with no bound is a layout attack.

Threat classes, review triggers, and when a change needs a security review are owned by `/alaa-security-review` (`$alaa-security-review`). Quasar-specific audit surfaces — `*-html` props, `QEditor`, upload components, user-controlled labels in custom slots — are owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`).

## 3. Paste and clipboard

Paste is an input boundary that most designs forget, and on a Persian product it is where three separate rules meet.

**On paste into a plain field:**

- Strip formatting. A paste from a word processor or a web page carries styles, fonts and colours; accepting them defeats the token system in one gesture. Take the plain-text flavour, always, for any field that is not a deliberate rich-text editor.
- Preserve U+200C (ZWNJ). It is content, not whitespace, and a trim or whitespace-collapse routine that removes it corrupts Persian text. See `05-rtl-and-persian.md` section 6.
- Do not insert or preserve bidi control characters that arrived with the pasted text; strip U+200E, U+200F and U+2066-U+2069 on paste for the reason in `05-rtl-and-persian.md` section 1.
- Digits fold to ASCII, at submit and on paste alike. The fold itself is owned by `/alaa-input-normalization` (`$alaa-input-normalization`).
- Separators are stripped for fields with a canonical form. A phone number pasted as a formatted string must reach the same canonical value as one typed digit by digit; a field that folds digits but keeps the separators produces a value that passes the length check and fails at the server.
- **Show what was accepted.** After a transforming paste, the field displays the transformed value immediately. A silent transformation the user discovers at submit is worse than a rejection.

**On paste into a rich-text editor:** the allowed tag and attribute set from section 2 applies to pasted markup exactly as it applies to fetched markup.

**On copy out of the product:**

- What is copied is what is displayed, or better. Never copy a value with invisible characters, styling wrappers, or a truncation the user cannot see.
- A copy affordance confirms visibly and briefly, and the copied value stays selectable so a failed clipboard write is recoverable by hand. `client`'s `src/auth/totp/TotpSecretCopy.vue` is the pattern: a Clipboard API write with a selection fallback.
- Never place a secret on the clipboard without saying so, and never place one there automatically.

## 4. Multi-tenant and cross-user surfaces

- Every surface that can show another tenant's or another user's content states whose it is, next to the content, without the user having to infer it from styling.
- Content authored by another user is never rendered with the product's own system chrome. A message from a user must not be able to look like a message from the product; that is a phishing surface built by design.
- Identity-bearing values a user supplied — display name, avatar, organisation name — are untrusted content under section 2 and are length-bounded under the same rule.

## Anti-patterns

- Treating a hidden button as an access control.
- A second `v-html` site added because one already exists.
- Sanitizing on the server and rendering raw in the browser because "it was already cleaned".
- Building a CSS class or icon name from user content.
- A paste handler that trims U+200C along with whitespace.
- Folding digits on paste but leaving the separators.
- A permission-shaped surface with only granted and denied appearances and nothing for "not yet known".
- Rendering another user's content in the product's own system voice.

## Pairing

- What the denied and unknown states look like: `15-designed-failure-states.md`
- The reference an error state gives the user: `28-ui-diagnosability.md`
- ZWNJ, digits and direction on the input path: `05-rtl-and-persian.md`
- Component prop design that closes these holes at the API: `55-component-library-and-governance.md`
- The fake-affordance gate: `90-quality-gates-and-review.md`
