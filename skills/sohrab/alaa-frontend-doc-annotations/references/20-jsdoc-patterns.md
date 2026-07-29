# JSDoc block shapes and the tag contract

Read this when writing a block, or when choosing a tag.

## File-level header

Write a file header when the file registers a side effect at import time, is imported by a boot file or a
router guard, branches on an SSR flag, or exports a symbol used by three or more feature folders. Do not
write one on a file that only exports types, or on a barrel that only re-exports.

A header states, in this order: what the file owns, why it exists separately from its neighbour, and the
constraint a caller must respect. It may carry `@see` pointing at the module that would otherwise hold this
code. It never restates the export list, which the code already holds.

## Function-level block

**Write a JSDoc block on every exported function, exported arrow-const, store action and composable.** For
a non-exported function, write one only when its behavior depends on a precondition the caller must
satisfy, and state that precondition in the first line.

The first line is a sentence in the present indicative naming what the call does: "Recomputes the UI
capability snapshot for a token." Not "This function is used to..." and not "Helper for...".

## The tag contract

A block documents three things beyond its behavior: what shipped, how it is operated, and how it fails.
Each has a tag, and each tag has a condition that makes it mandatory.

| Tag | Write it when | Content rule |
|---|---|---|
| `@param` | The parameter's name does not state its meaning, its unit, its timezone, its encoding, or the effect of `null` | Name the constraint the caller must satisfy. **Never a type in a TypeScript context** — see below |
| `@returns` | The return value has a state the name does not carry: a frozen object, an empty-but-valid result, a value that is `null` on a legitimate path | State which states are legitimate. An empty result that is not an error is stated here or it will be treated as one |
| `@throws` | The function can throw, or deliberately cannot | `@throws {TypeError} when ...`, or the sentence "Never throws; malformed input yields `<value>`." **`@throws` is prose to TypeScript** — nothing compiles it, so it is exactly the class this skill owns |
| `@deprecated` | The symbol still exists and must not gain new callers | `@deprecated since <version>; use `<replacement>`. Removed when <observable condition>.` A `@deprecated` with no replacement and no removal condition is a complaint |
| `@since` | The symbol is part of a published package surface | The version the symbol first shipped in, taken from the package's own version, never guessed |
| `@example` | The call has a non-obvious shape: an options object, an ordering requirement, a cleanup the caller owns | One runnable call, not a paragraph. If cleanup is the caller's, the example shows the cleanup |
| `@see` | A fact lives in another module or another skill | The symbol name or the skill name. Never a Stack Overflow or issue-tracker URL (`ANN501`) |

## The run-phase line

**Every exported fetch wrapper, store action and composable that can execute during SSR carries a JSDoc
line stating exactly one of `runs: server`, `runs: client`, or `runs: both`.** A wrapper without that line
is a finding of the annotation pass. This is the single fact a caller cannot recover by reading the
function, because it depends on who imports it.

## Types belong to the type checker

In a `.ts` file or a `<script lang="ts">` block, **never write `@param {Type}` or `@returns {Type}`.** The
type is in the signature; a JSDoc copy of it is a second source of truth that no tool compares against the
first. Verified against `vue-tsc` 3.3.6 on TypeScript 6.0.3: JSDoc types in a `.ts` file are read and
silently discarded, so a wrong one produces no diagnostic at all. The checker asserts this as `ANN401`.

In a JavaScript module, `@param {Type}` is the only type information that exists and is therefore required
on every exported function — but it is only *checked* under `checkJs` or a `// @ts-check` pragma. Which of
those the repo has, and what that means, is `references/50-checkable-annotations.md`.

## Inline comments

Use an inline comment only where the reasoning is not recoverable from the code. Two lines maximum. A
comment that carries an SSR, hydration, store, auth or security assumption uses a prefix from the closed
five-item set — `references/30-ssr-hydration-and-store-notes.md` and
`references/40-security-and-trust-annotations.md` state which prefix carries which claim, and the closed set
is what makes `grep` a complete index rather than a sample.

## Anti-patterns

- Explaining syntax. `// increment i` on `i++`.
- Restating a type that the signature already carries.
- A paragraph inside a function body; move it to the function block or the file header.
- A comment apologising for confusing code instead of naming the boundary that makes it confusing. If the
  code needs an apology it needs an extraction, which is
  `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`), not a comment.
- A block auto-generated from the signature: `@param token - The token.` carries nothing.
