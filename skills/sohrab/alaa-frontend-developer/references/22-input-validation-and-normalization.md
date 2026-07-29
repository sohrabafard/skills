# Input Validation and Normalization — the frontend binding

The normalization form itself is not here. Which characters fold, what `text` and `typed` mode mean, the
canonical implementations, the corpus and the harness all belong to `/alaa-input-normalization`
(`$alaa-input-normalization`): `references/10-normalization-contract.md` for the form,
`references/20-browser-binding.md` for where the fold runs in a Vue application,
`references/40-failure-classes.md` when a value arrived wrong, and
`assets/input-normalization/input-normalization.ts` for the implementation to copy.

This file states only what a frontend engineer owes at the input boundary.

## The three obligations

1. **Every free-text field declares a length cap.** A `maxlength` on the control and the same number in
   the validator. A field whose cap exists only in the backend validator sends the user a rejection after
   the submit instead of preventing it, and a field with no cap anywhere is an unbounded write.
   The number is not chosen here: field limits belong to `/alaa-services-contract`
   (`$alaa-services-contract`) `references/10-core-service-contract.md`.
2. **Every submit path folds before it sends.** Call the canonical implementation on the value being sent,
   for every string field on the form — not the keystroke handler alone, and not the component alone. A
   value can enter the model by paste, autofill, WebOTP, a restored draft, a deep link or a rehydrated
   snapshot, and only the submit path sees all of them.
3. **Never write a character list.** No per-field regex, no digit map, no `replace` chain, no
   `strtr`-style table. An enumerated list is a defect class: it will be missing a code point, and the
   next one is found in production. If a character gets through, fix the canonical implementation and add
   the case to the corpus — that route is `/alaa-input-normalization` (`$alaa-input-normalization`)
   `references/50-corpus-and-harness.md`.

## Client normalization is a convenience, never the contract

The browser fold exists so the user sees ASCII as they type and so a client-side length check measures the
same string the server will. The enforcement point is backend middleware. A screen that assumes the server
receives a folded value because the form folded it is wrong: an HTTP client, a forked package copy, or a
service with no browser on its write path all bypass it.

The consequence for frontend design: **never build a client-side rule the server does not also hold.** A
uniqueness check, a length check, or a format check that only the browser performs is a UX affordance
with no authority.

## What a component must not do

- Reject a value because it still contains a non-ASCII digit. Normalization is total — it never rejects,
  never throws and never repairs. A field still holding one has not been folded yet, which is a defect in
  the caller.
- Show an error message asking the user to type English digits. Its presence in a UI means the fold is
  missing.
- Normalize instead of validating. Fold first, then validate the folded value.

## Validation shape

Validate on the value that will be sent, after the fold, with the same predicate the server uses where the
server publishes one. Surface a field-level error tied to the control, not a page-level banner; the error
copy and its placement belong to `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`)
`references/15-designed-failure-states.md`.

Rendering a value back in Persian digits is a display decision, owned by `/alaa-ui-ux-design-system`
(`$alaa-ui-ux-design-system`) `references/05-rtl-and-persian.md`. A rendering choice never substitutes for
folding at the input boundary.

## Untrusted input beyond shape

A value that passes length and format checks can still be hostile once it is rendered, put in a URL, or
used as a key. That is `25-frontend-security.md` here and `/alaa-security-review`
(`$alaa-security-review`) `references/20-untrusted-input.md` for the threat classes.
