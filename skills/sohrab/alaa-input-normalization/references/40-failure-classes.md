# Failure Classes

What each way of getting this wrong looks like in production. Every one of these is either
silent or reported far from its cause, which is why the fix is a contract and a harness
rather than a patch at the place it surfaced.

## A. The fold is missing on one side

**Symptom: a user sees a validation error about a value they can read as correct.** A
Persian OTP `۱۲۳۴۵` sent to Laravel's `digits:5` fails twice over: the rule's character class
is byte-wise with no `/u`, and its length check is `strlen`, which counts bytes, so a
five-digit Persian OTP is measured as ten. The message says "must be 5 digits" about a value
the user can see is five digits.

**Symptom: a phone number is rejected by an SMS provider hours after it was accepted by the
form.** The value was stored with its separators or its Persian digits, and the failure
appears in a notification worker in a different service, with no trace back to the form that
accepted it.

**Where to look:** the field's submit path first, then the service's middleware registration.
An alias registered and applied to no route is the fleet's most common instance — grep the
route files for the alias before believing the middleware runs.

## B. The fold is present but the predicate is wider than `Nd`

**Symptom: `x²` is stored as `x2`, `½` as `1/2`-ish nonsense, a Roman numeral as digits.** A
fold written against `\p{N}`, `str.isdigit()`, `Character.isDigit` or `unicode.IsNumber`
reaches category `No`. The corpus catches this on the superscript, circled-digit, fraction
and Roman-numeral cases.

**Symptom: an acceptance filter and the fold disagree.** A component filters input with
`\p{Nd}` and folds with a hand-written family table, so a digit family the table does not
list passes the filter and is sent to the server unfolded — a non-ASCII "digit" in a field
the client believed it had cleaned.

## C. The fold is present but the predicate is narrower than `Nd`

**Symptom: one user's digits work and another's do not, and nobody can reproduce it.** A
two-family fold handles Arabic-Indic and Persian and drops Devanagari, Bengali, Thai, NKo,
fullwidth and every astral family. It is invisible until a user with a different keyboard
layout arrives.

**Symptom: the browser folds a family the backend does not.** The two sides derive
membership from different Unicode versions, or one derives and the other lists. Eight code
points in the shipped browser table are unassigned under Unicode 14.0.0.

## D. The two sides pick different Unicode normalization forms

Every consequence is silent:

- A `max:5000` rule measures different lengths, so a comment the browser accepted the server
  rejects, or the reverse.
- A unique index or an equality comparison sees two strings that render identically as
  different values: a duplicate row, a failed idempotency lookup, a cache miss on every
  request.
- A hash or a signature over the field differs, so an idempotency key derived from content
  stops matching.
- **The conformance harness reports what looks like a digit bug.** The implementations agree
  on the fold and differ only in composition, and the mismatch line shows two strings that
  render identically. The harness's own self-test carries this vector for that reason.

## E. NFKC was used instead of NFC

**Symptom: characters this contract deliberately preserves come back changed, and the
"what folds" question has two answers.** NFKC folds the fullwidth digits and the superscripts
to ASCII by its own rule, and rewrites Arabic presentation forms and ligatures. A reviewer
then cannot tell whether a given character changed because of the digit rule or the
normalization form.

## F. Iteration by code unit or by byte

**Symptom: mojibake in a field that contained an astral digit**, `U+1D7CE` and the other
mathematical, Adlam, Osmanya and segmented families. A JavaScript implementation that walks
`charCodeAt` over `.length`, or a PHP one using `strlen`/`str_replace` instead of `preg_*`
with `/u` and `mb_*`, splits the surrogate pair or the UTF-8 sequence and emits replacement
characters. The corpus pins five astral families.

## G. Keys were folded along with values

**Symptom: a field silently disappears from a request.** A traversal that folds object keys
renames `field۱` to `field1`, and the validator reports the original name as missing while
the payload visibly contains it.

## H. Something was deleted in `text` mode

**Symptom: Persian words are subtly wrong in stored content.** Deleting ZWNJ turns `می‌رود`
into `میرود`, a different word; mapping ZWNJ to a space is worse. Deleting or mapping
tatweel, hamza or a combining mark rewrites Arabic orthography. `text` mode maps digits and
does nothing else; every deletion belongs to `typed` mode, where the whole field is one
number.

## I. An Arabic numeric separator was mapped to ASCII

**Symptom: a number is wrong by a factor of 1000, and nothing logs an error.** `١٬٢٣٤` is
1234; map `U+066C` to `,` and a parser reading `,` as a decimal separator returns `1.234`.
In a phone field the same mapping manufactures the two-numbers-in-one-field shape the phone
rule rejects. Leave both separators and let validation reject the field.

## J. The harness was made green by editing the corpus

**Symptom: none, ever, until production.** This is the failure class with no observable
signature, which is why the rule is absolute: when an implementation disagrees with the
corpus, fix the implementation. A corpus edit is a contract change and needs the
ratification path in `references/50-corpus-and-harness.md`.

## K. A green harness was read as a broader claim than it is

**Symptom: a character nobody tested reaches production and behaves differently on the two
sides.** A green run proves that every runtime that executed produced the exact bytes the
corpus requires, for the cases the corpus carries, on the Unicode data those runtimes
happened to have. It proves nothing about an input the corpus does not carry, and nothing
at all about a skipped runtime.

## Two contract-adjacent failures owned elsewhere

- **A repair instead of a rejection.** Left-padding a national code to ten with zeros, or
  stripping a `+` unconditionally from a phone number, turns a rejectable value into a wrong
  one. Normalization never repairs; rejection rules belong to `/alaa-bale-provider`
  (`$alaa-bale-provider`) and `/alaa-sms-provider-mediana` (`$alaa-sms-provider-mediana`).
- **A UI that asks the user to type English numbers.** Owned by
  `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`); its presence means the fold is
  missing, so fix the fold and delete the message.
