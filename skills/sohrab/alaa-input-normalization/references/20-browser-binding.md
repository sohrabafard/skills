# The Browser Binding

Where the fold runs in a Vue/Quasar application, and the one standing rule that keeps it
from being rewritten by hand every time a new character shows up.

**Read first:** the browser fold is a convenience, not the contract. It exists so the user
sees ASCII as they type and so a client-side length check measures the same string the
server will. A backend that trusts it has no contract at all —
`references/30-backend-middleware-binding.md` is the enforcement point.

## The standing rule: a validator or a formatter never enumerates characters

**An enumerated character list is a defect class, not a fix.** Two rounds of "fix the
enumerated list" preceded this rule, and both shipped: the phone validators first carried a
list holding the space, the tab, the newline and `U+00A0`, and still rejected `U+2028`,
`U+3000`, `U+000B` and every narrow space — which is how the two providers came to disagree
on four inputs *after* their first two disagreements had been fixed.

So when a character gets through:

- **Do not** add it to a list, a regex character class, a `replace` chain, or a `strtr` map.
- **Do** find which Unicode property the character has that the rule should have named, fix
  the canonical implementation in `assets/input-normalization/` to test that property, add
  the character to `scripts/normalization-corpus.json` as a case, and run
  `scripts/normalization-conformance.sh`.

The one place characters are written out is where no Unicode property names them precisely
enough — the literal separators `()._/` and the whitespace controls — and each of those
carries the reason it is written out, in the source, beside the list.

## Where the fold runs

The submit pipeline, on the value being sent, for every string field on the form. Not the
keystroke handler alone, and not the component alone.

- **On submit** is the load-bearing point: the value that leaves the application is folded,
  whatever route it took into the model — typing, paste, autofill, WebOTP, a restored draft,
  a deep link, a persisted state snapshot.
- **On input** is optional and cosmetic. The shipped `client` package installs a
  capture-phase `input` listener application-wide so digits become ASCII as the user types.
  It rewrites digits in place and removes no separator, so **it does not make a submit-path
  fold unnecessary**.
- **A displayed value may be rendered in Persian digits**; that is a rendering decision owned
  by `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`). A rendering choice never
  substitutes for folding at the input boundary.

Mode per field: `typed` for a field that holds one number or one code — mobile, OTP,
national code, postal code — and `text` for everything else. Choose the mode where the field
is declared, not where it is submitted, so a reviewer reading the field sees its mode.

## The three defects live in the fleet today

1. **`client/src/auth/profileCompletion` — `contact.phone` reaches the backend with its
   separators.** The submit path folds digits and strips nothing, so `0912 383 0000`,
   `0912/383/0000`, a pasted `U+00A0` and a bidi mark from an RTL editor all survive. The
   value is stored as that user's phone number and rejected by a provider hours later, in a
   different service. The field also has no `maxlength`, and the generic input loop it
   renders through binds a fixed attribute set that cannot carry one. An RFC exists at
   `client/docs/change-requests/20260727-093000_profile-completion-phone-reaches-the-backend-with-its-separators.md`;
   extend or supersede it rather than filing a duplicate. The fix is `typed` mode on that
   field, not a separator list.
2. **`AdsCodeInput` accepts by category and folds by table.** The OTP component filters with
   `\p{Nd}` (category-derived, correct) and then folds with a 75-entry hand-written family
   table. Any `Nd` code point the table does not list is accepted by the filter and survives
   the fold unfolded, and is then sent to the server as a non-ASCII "digit". One predicate,
   one fold, one source of membership.
3. **Two forked copies of the browser package.** `client/packages/digit-normalizer` and
   `entekhabat-front/packages/alaa-digit-normalizer` are byte-different and semantically
   identical, and nothing binds them: no shared package, no corpus, no harness. That is
   exactly the condition that produced the provider disagreements. Both become copies of
   `assets/input-normalization/input-normalization.ts`.

## What not to write in a component

- A per-field regex, a digit map, or a `replace` chain. Call the canonical implementation.
- A check that rejects a value because it contains a non-ASCII digit. Normalization is total:
  a field that still holds one has not been normalized yet, which is a defect in the caller
  rather than in the user's typing.
- An error message asking the user to type English numbers. The fold makes that message
  unnecessary, and its presence in a UI means the fold is missing.
- A `str.isdigit()`-style acceptance test in any language or JavaScript equivalent. See
  `references/10-normalization-contract.md` for the predicate that is correct.

Caret position: a caret-preserving in-place rewrite is a UX detail, not part of the
contract, and the shipped package already implements one. The submit fold must run whether
or not the in-place rewrite did.

## Companions

- `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`): the submit pipeline
  shape, the composable boundary, and where a form's values are assembled.
- `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`): the input components, their
  RTL behaviour, and digit rendering.
- `/alaa-services-contract` (`$alaa-services-contract`): `maxlength` and every other value.
