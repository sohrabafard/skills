# Phone normalisation and the shared conformance corpus

Read this when you are turning a user-entered number into a recipient string, when you are writing or changing a normaliser in any language, or when the Mediana and Bale renderings of one number disagree.

## One input form, two wire forms

The platform holds one input form: an Iranian mobile number as a subscriber types it. Each channel renders it differently.

| Channel | Wire form | Example |
|---|---|---|
| Mediana / IPPanel Edge | `+989xxxxxxxxx` | `+989123830000` |
| Bale Safir | `989xxxxxxxxx` | `989123830000` |

The two forms differ by one character, and that character decides whether a message is delivered. **A shared normalisation function that does not take the target channel as a parameter is a defect.** It has to guess, and a guess renders one channel's number for the other: the vendor rejects it in the lucky case, and in the unlucky case a differently-shaped value passes validation and the OTP goes somewhere it should not. Take the channel as an argument, return the channel's form, and let the call site name the channel it is sending to.

## What the client actually sends

This section records the evidence the separator rule rests on. It was read out of the Alaa `client` project on 2026-07-28; the paths are relative to that repository's root.

The `/login` route renders `src/pages/login.vue`, then `src/auth/AuthLoginPage.vue` and `src/auth/AuthLoginPanel.vue`. Two fields on that page carry a phone number, and they reach the backend by two different paths.

**The login mobile field** is an `AdsInput` at `src/auth/AuthCredentialsPanel.vue:4`-`18`, bound to the flow's `mobile` ref with `maxlength="11"`, `inputmode="numeric"` and `pattern="[0-9]*"`. The only separator character the page puts on screen beside it is the ASCII space `U+0020`, in the placeholder `0912 345 6789` at `src/i18n/fa/auth/login.ts:10` and `src/i18n/en-US/auth/login.ts:10`; both files were checked byte by byte and neither space is a non-ASCII one. Reading direction is handled entirely in CSS — `unicode-bidi: isolate` at `packages/design-system-vue/src/styles/templates/_input.scss:40` and `:48`, with the direction class chosen at `packages/design-system-vue/src/templates/AdsInput/AdsInput.vue:65`-`79` — so no bidi control character is inserted into the value. The number echoed back on the OTP step (`src/auth/AuthOtpPanel.vue:5`, message `auth.otp.sentTo` at `src/i18n/*/auth/login.ts:22`) is a plain interpolation that adds nothing. The Persian copy on the same page does carry `U+200C` at `src/i18n/fa/auth/login.ts:15` and `:26`, in words rather than inside a number.

That field cannot deliver a separator to a provider. Every path out of it passes the value through `normalizeDigitsOnly()` (`packages/digit-normalizer/src/index.ts:152`-`154`, which folds localized digits and then deletes everything that is not an ASCII digit): the OTP request at `src/auth/useAuthCredentialsStep.ts:166`-`167`, the OTP verification at `:213`-`215`, and the persisted mid-flow snapshot on both write and read at `src/auth/authFlowStatePolicy.ts:80`-`81` and `:142`-`149`.

**The profile-completion `contact.phone` field is the path that does reach a provider.** The same `/login` page runs a required profile-completion step (`src/auth/AuthLoginPage.vue:19`, enabled at `src/auth/profileCompletion/defaultProfileCompletion.ts:174`-`179`), and that step includes a `tel` field `contact.phone` at `:50`-`54`. Its value leaves the browser through `src/auth/profileCompletion/profilePolicy.ts:147`-`149` and `:209`-`211`, which call `normalizeDigitsToAscii` and nothing else: localized digits are folded to ASCII and **every separator survives**. That input carries no `maxlength` (`src/auth/profileCompletion/ProfileCompletionPanel.vue:22`-`33`), so a pasted `0912 383 0000`, a typed `0912/383/0000`, and a value carrying `U+00A0` or `U+2028` are all stored verbatim. The app-wide middleware at `src/boot/digit-normalizer.ts:12`-`16` rewrites digits in place as the user types and removes no separator at all.

So a stored Alaa phone number can hold any character a person or an editor puts between its digits, and a later notification to that number is a provider call. **The normaliser is the component that has to absorb display separators**, because it is the last place before the wire that sees the raw value.

## What the normaliser does, in order

1. Fold every code point of Unicode general category `Nd` to its ASCII digit, one to one, and enumerate no digit family: an enumerated list is a defect class rather than a fix, and this step covered two families only until 2026-07-28. Category `No` is excluded, so a superscript digit is not folded and an input carrying one is still rejected by step 5. The fold, its canonical implementations and its corpus are owned by `/alaa-input-normalization` (`$alaa-input-normalization`); call that implementation rather than writing a digit table.
2. Remove every display separator, using the category rule stated in the next section.
3. Reject an input that is empty once the separators are gone, because a value with no digits names no recipient.
4. Reject anything that still contains a character other than a digit or a leading `+`, naming the offending code points.
5. Match `^(?:\+98|0098|98|0|)(9\d{9})$` and reject anything that does not. This accepts the five forms a subscriber actually types and rejects landlines, foreign numbers, sender labels, malformed international prefixes, and every wrong length.
6. Render the captured ten digits behind the channel's prefix.

Never use a language's built-in "is this a digit" test to validate a number; test against an explicit ASCII digit pattern instead. Python's `str.isdigit()` returns `True` for Persian-Indic, Arabic-Indic and superscript digits, so a check built on it passes a six-character Persian-Indic string and the superscripts `U+00B2 U+00B3 U+2074` as valid input -- which is how a validator ends up less strict than the prose warning about the same input.

## The display-separator rule

**Match whitespace, format and dash characters by Unicode general category, and never by a written-out list of characters.** Scope: this rule governs recipient normalisation for the Mediana channel and the Bale channel. A written-out list is always one character short of the next change in a display layer, and the history of these two skills is the proof: the Bale enumeration already carried the space, the tab, the newline and `U+00A0` and still rejected `U+2028`, `U+3000`, `U+000B` and every narrow space, which is how the two providers came to disagree on four inputs after their first two disagreements had been fixed.

A character is display formatting, and not a digit of the number, when its category is one of these five:

| Category | Class | Members that arrive in practice |
|---|---|---|
| `Cf` | Format | ZWNJ, ZWJ, the bidi marks, the bidi isolates and overrides, the word joiner, the BOM, `U+206F` |
| `Zs` | Space | `U+00A0`, `U+1680`, `U+2000`-`U+200A`, `U+2007`, `U+202F`, `U+205F`, `U+3000` |
| `Zl` | Line | `U+2028` |
| `Zp` | Paragraph | `U+2029` |
| `Pd` | Dash | `U+002D`, `U+2010`-`U+2015`, `U+FF0D` |

Match the whitespace control characters with `str.isspace()` rather than with their category, because category `Cc` also holds characters that are not separators. `str.isspace()` covers the tab, the line feed, the vertical tab, the form feed, the carriage return, the four information separators and `U+0085`, and it covers nothing else inside `Cc`.

Four separators stay written out, as `()._/`, because no Unicode category names them precisely enough to be matched by one: `Ps` and `Pe` hold every bracket pair in Unicode, and `Po` holds the comma and the semicolon, which separate two numbers rather than group the digits of one.

Keep a comma in the string so that the shape check rejects the input, because a comma means the caller passed two numbers in one field and that input has to be refused rather than silently concatenated into a recipient nobody entered.

## The solidus ruling

**Strip the solidus `/` from a recipient number, in both providers.** Scope: recipient normalisation only; it says nothing about `from_number`, pattern codes, or any other field.

The solidus is not a display artefact, so the category rule above does not reach it and it was decided on its own merits. Both readings were weighed. Against stripping: no legitimate formatter emits `/` between the digits of a phone number, so refusing it costs nothing that a formatter produces. For stripping: `0912/383/0000` is a shape a person types by hand, and the evidence recorded above shows that the value which actually reaches a provider comes from an unmasked free-text field that a person types into, so what a formatter produces is not the population that governs. Refusing it therefore rejects a legitimate caller with an error they cannot diagnose from the number they can see.

Accepting it costs no safety, and that is what settles it. Removing the solidus cannot fabricate a recipient: `09123830000/09123830001` concatenates to 22 digits and is refused by the same length check that already refuses the same two numbers separated by a space, and `http://example/09123830000` keeps its letters and is refused by the digit check. The corpus pins both of those.

## The international-prefix rule

**Accept a leading `+` or a leading `00` only when the country code `98` follows it.** Scope: recipient normalisation for both channels. Accepting either one unconditionally turns a malformed number into a well-formed one: `+9123830000` and `009123830000` carry no country code at all, and `+09123830000` carries the domestic trunk zero in the position the country code belongs in. `MSISDN_RE` enforces this here; the Bale validator enforces the same set with an explicit prefix test, and each of those four shapes is a corpus case now.

## The canonical implementation

`scripts/validate_mediana_payload.py` holds the one implementation this skill endorses, as the function `normalize_msisdn(raw, channel)`, exposed on the command line:

```bash
python3 scripts/validate_mediana_payload.py --normalize '0912-383-0000'
python3 scripts/validate_mediana_payload.py --normalize '(0912) 383 0000' --channel bale
python3 scripts/validate_mediana_payload.py --normalize '0912/383/0000'
```

A value typed with Persian-Indic digits (U+06F0 to U+06F9) or Arabic-Indic digits (U+0660 to U+0669) renders identically; the corpus covers both families and this file keeps those code points out of its prose.

It prints the rendered number and exits `0`, or prints a reason to standard error and exits `1`. The reasons are a closed set: `not_a_string`, `unknown_channel`, `empty_after_cleanup`, `unexpected_characters`, `not_iranian_mobile`. Map them to your own error taxonomy; read the reason code rather than the human text beside it.

Any normaliser in the service — PHP, Go, TypeScript, SQL — must produce the same output as this one for every case in the corpus. When a language cannot match a case, change the corpus and both skills in one commit, not the one implementation that disagrees.

## The corpus

`scripts/phone-conformance-corpus.json` holds **80 cases: 49 that must render and 31 that must be rejected.** Each case is `{input, mediana_expected, bale_expected, note}`, and an expected value of `null` means the input must be rejected rather than rendered. The corpus covers the three accepted input forms, the bare national number, the `0098` access code, Persian-Indic and Arabic-Indic digits, mixed digit families, zero-width and bidirectional characters, one member of every separator category in the table above, the solidus, both wrong lengths, a landline, a foreign number, a sender label, superscript digits that must be rejected and Devanagari digits that must render, two numbers in one field separated by a space and by a solidus, a malformed international prefix in four shapes, an empty string, an ASCII whitespace-only string, a Unicode whitespace-only string, and a zero-width-only string.

The file records `corpus_sha256`: the SHA-256 of `json.dumps(cases, ensure_ascii=False, sort_keys=True, separators=(",", ":"))` encoded as UTF-8. As of this writing it is `80dcb3723e83d848236ab0cbfbfc62447eec524c62a434737d85682aa653d7dc`, set on 2026-07-28 when the Devanagari case was re-ratified from rejected to rendered and the split moved from 48/32 to 49/31. The digest covers the parsed cases rather than the on-disk `\uXXXX` escaping, so any language can reproduce it, and case order is part of the hashed bytes: accepted cases first, then rejected ones, ascending by Unicode code point of `input` within each group. The file's own `canonicalization` field states the rule and carries a one-line command that recomputes the digest from the file alone.

**The identical file ships at `alaa-bale-provider/scripts/phone-conformance-corpus.json`.** The two copies are byte-identical by design, and a difference between them is a finding rather than a local customisation. `AGENTS.md` binds this: more than one implementation of one wire format ships a conformance harness, because a document asserting that two implementations agree is not evidence that they do.

## Running the harness

```bash
python3 scripts/validate_mediana_payload.py --self-test
```

It drives the corpus through the normaliser for both channels and runs the payload cases, then prints how many of each it exercised. It exits `1` on any disagreement, naming the case index, the channel, the expected value and the observed one. It exits `4` when the corpus is missing or its checksum does not match its cases — which is the signal that the two copies have drifted, and the obligation then is to reconcile both, never to edit one.

Run it before finishing any change to a normaliser, to the corpus, to either provider skill's validator, or to any service-side phone handling that these skills govern. Run the sibling harness in the same sitting:

```bash
python3 ../alaa-bale-provider/scripts/validate_bale_payload.py --self-test
```

## What is not normalised

- `from_number` is a sender identifier. It may be a numeric line such as `+983000505` or an alphabetic label such as `+98BANK`, so recipient rules do not apply to it and the corpus deliberately rejects a label as a recipient.
- A recipient column inside an uploaded CSV or XLSX is normalised when the file is written, not when the request is built; see `references/12-multipart-and-file-sends.md`.
- A number that reaches this skill already in a channel's wire form is still passed through the normaliser, so there is exactly one code path and one place a defect can hide.
