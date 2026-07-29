# Invariant docblocks

Read this when a docblock states an invariant, or when a repository style rule says comments do not belong
outside configuration files.

## The rule this overrides, by name

`laravel-best-practices/rules/style.md`, section **"No Unnecessary Comments"** — an upstream agent skill
shipped inside a production repository at `.agents/skills/laravel-best-practices/`, not owned by that
repository and re-pulled periodically — instructs an agent to write comments only in configuration files.

**That rule is overridden.** The override is already recorded in the fleet at
`/alaa-php-clean-code` (`$alaa-php-clean-code`), `references/laravel-best-practices.md`, and at
`/alaa-octane-performance` (`$alaa-octane-performance`). This file ports the same override to frontend
code, for the same reason: applying the rule literally strips invariant docblocks, side-effect notes and
test-intent comments, which are load-bearing safety documentation rather than decoration.

The override is narrow and keeps the part of the upstream rule that is right:

- A comment explaining **what** unclear code does is still wrong. Extract the code and name the extraction
  after the comment — `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`).
- A comment stating **why** — an invariant, a provider quirk, a unit, a timezone, an encoding, a
  cross-service assumption — stays, and this skill states its shape.

A repository-local rule that forbids comments does not override this file. Cite this file by name in the
pass report when a repository rule and this one conflict, so the conflict is visible rather than resolved
silently in whichever direction the agent happened to read last.

## What an invariant docblock is

An invariant docblock states a condition that must hold and is not enforced by the type system. Four
classes appear in frontend code:

| Class | The invariant | Why the type system cannot hold it |
|---|---|---|
| Ordering | This runs after hydration; that runs before the router is installed | Order is a runtime property of the import graph |
| Cardinality | Exactly one instance of this listener, this observer, this worker exists | A type describes a value, not how many were created |
| Provenance | This value came from the gateway, not from a client-supplied field | Both are `string` |
| Unit and encoding | Milliseconds, not seconds. Base64url, not base64. UTC, not local | Both are `number` or `string` |

The block states the invariant, the consequence of breaking it, and the place that would break it. All
three: an invariant with no named consequence reads as a preference and is deleted by the next refactor.

```ts
/**
 * Frozen at module scope: exactly one instance exists per document.
 *
 * A second instance would register a second `visibilitychange` listener and double every refresh, which
 * surfaces as duplicate requests after a tab has been backgrounded twice. Constructed only by the boot
 * file; do not export the constructor.
 */
```

## The `any` docblock

`/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`),
`references/20-typescript-composition-contract.md`, permits `any` **only** with a comment and an immediate
typed wrapper. That skill states the requirement — it is a rule `tsc` and the reviewer enforce. This skill
states the shape of the comment, because nothing compiles a comment.

The block answers three questions and nothing else:

1. **Where the untyped value came from** — a third-party module with no types, a `JSON.parse`, a
   `postMessage` payload, a DOM API the lib does not model.
2. **What the wrapper guarantees** — the narrowed type it returns, and what it does when the value does not
   match, which is never "cast and hope".
3. **What would let the `any` be deleted** — the upstream types shipping, a schema validator, a generated
   client. This is the removal condition, and without it the `any` is permanent by default.

```ts
/**
 * INVARIANT: the only `any` in this module, and it never escapes this function.
 *
 * `<pkg>` ships no types for its event payload. `toPlayerEvent` narrows it to `PlayerEvent` and returns
 * `null` for anything that does not match, so a payload change degrades to a dropped event rather than an
 * undefined read at the call site. Delete this when `<pkg>` ships types or the payload gains a schema.
 */
```

A `@ts-expect-error` or `@ts-ignore` carries the same block, plus the error code it suppresses and the
condition under which the suppression is removed. A suppression with no removal condition is a permanent
hole with a temporary-looking comment on it.

## Where an invariant block is mandatory

- A module-scope mutable value in a module that can be imported during server render — the invariant is
  whether it is request-scoped. See `references/30-ssr-hydration-and-store-notes.md`.
- A hand-rolled decoder, parser or bit-walker: state the input's accepted shape, its size cap, and what
  malformed input yields. A decoder that fails closed says so, because a later reader otherwise cannot tell
  a deliberate fail-closed from a swallowed error.
- Any value that must match a value in another service. State the invariant and cite
  `/alaa-services-contract` (`$alaa-services-contract`); do not restate the value.
- A cleanup contract: what the caller must release, and what leaks if they do not.

An invariant block that asserts a security or authorization property is not merely an invariant block — it
takes the `SECURITY NOTE:` or `AUTH NOTE:` prefix and a `verified:` date on top of everything above.
`references/40-security-and-trust-annotations.md`.
