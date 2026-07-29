# Source map — what a comment may cite

Read this when deciding where a fact written into a comment comes from.

## The source ladder is not stated here

The official-first source priority for Vue, Quasar, Vite and MDN is
`/alaa-frontend-developer` (`$alaa-frontend-developer`) and
`/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`), `references/05-sources-and-freshness.md`.
Follow it. This file holds only the two rules that are specific to comments.

## Freshness triggers

Re-check the official source before writing or updating a comment that contains any of these words, or that
describes any of these behaviors:

- the literal words `currently`, `latest`, `deprecated`, `removed`, `safe`, `unsupported`, `browser behavior`
- Vue lifecycle, hydration, reactivity, watcher, Suspense or SSR behavior
- Quasar SSR, PWA, boot-file or platform-mode semantics
- Vite transform, import, env, asset-URL or dev-server behavior
- a web API with security or compatibility sensitivity: storage, cookies, service workers,
  `BroadcastChannel`, WebOTP, WebRTC, media APIs

A comment carrying one of those words and no re-check is the same defect class as a `SECURITY NOTE:` with a
stale `verified:` date — see `references/60-staleness-and-verification.md`.

## No community citation inside code

**A comment never cites Stack Overflow, an issue tracker, a blog post, a Reddit thread or a Discord
message.** The checker asserts this as `ANN501` over `stackoverflow.com`, the Stack Exchange network,
`reddit.com`, `medium.com`, `dev.to`, GitHub `issues`/`pull`/`discussions` URLs, GitLab `issues`/
`merge_requests` URLs, and Jira-style `/browse/KEY-123` paths.

Community material is a hypothesis, not a source. Verify the behavior against the repository, the official
documentation or a focused local reproduction, then write the durable constraint you verified.

Anti-pattern:

```js
// Workaround for Vue bug from StackOverflow.
```

Better:

```js
// SSR NOTE: keep this client-only because SSR cannot read browser storage.
```

The second states the durable constraint, carries a prefix from the closed set so it is greppable, and does
not pin the code to an unverified external anecdote.

## Citing a cross-service fact

A comment asserting a fact that lives in another service — a header name, a route, a claim key, a status
string — names `/alaa-services-contract` (`$alaa-services-contract`) as the source rather than restating the
value inline. The full rule and its reason are in
`references/40-security-and-trust-annotations.md`.
