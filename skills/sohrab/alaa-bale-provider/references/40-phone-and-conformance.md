# Phone normalisation and the shared conformance harness

Read this when writing or reviewing phone normalisation for any Alaa messaging channel, when a `code 8`
`InvalidPhone` appears in production, or when changing either provider validator.

## One platform input form, two wire forms

Alaa accepts one input form from users and renders it differently for each channel.

| Channel | Wire form | Example |
|---|---|---|
| Bale Safir | `989xxxxxxxxx`, no plus sign | `989123830000` |
| Mediana / IPPanel | `+989xxxxxxxxx`, with a plus sign | `+989123830000` |

The two differ by exactly one character, and that character decides whether the message is delivered.

`SKILL.md` states the rule that a normaliser must take the target channel as a parameter. The signature is
`normalize(raw, channel)`, and the channel is supplied by the call site that already knows which provider
it is calling.

**Exactly one normaliser serves each channel.** A second implementation anywhere in a service — a helper
that prepends `98`, a template filter, a hand-written `ltrim` in a controller — is a divergence waiting to
happen, and `code 8` in production is what it looks like when it does.

## What the client actually sends

This section records the evidence the separator rule below rests on. It was read out of the Alaa `client`
project on 2026-07-28; the paths are relative to that repository's root.

The `/login` route renders `src/pages/login.vue`, then `src/auth/AuthLoginPage.vue` and
`src/auth/AuthLoginPanel.vue`. Two fields on that page carry a phone number, and they reach the backend by
two different paths.

**The login mobile field** is an `AdsInput` at `src/auth/AuthCredentialsPanel.vue:4`-`18`, bound to the
flow's `mobile` ref with `maxlength="11"`, `inputmode="numeric"` and `pattern="[0-9]*"`. The only separator
character the page puts on screen beside it is the ASCII space `U+0020`, in the placeholder `0912 345 6789`
at `src/i18n/fa/auth/login.ts:10` and `src/i18n/en-US/auth/login.ts:10`; both files were checked byte by
byte and neither space is a non-ASCII one. Reading direction is handled entirely in CSS —
`unicode-bidi: isolate` at `packages/design-system-vue/src/styles/templates/_input.scss:40` and `:48`, with
the direction class chosen at `packages/design-system-vue/src/templates/AdsInput/AdsInput.vue:65`-`79` — so
no bidi control character is inserted into the value. The number echoed back on the OTP step
(`src/auth/AuthOtpPanel.vue:5`, message `auth.otp.sentTo` at `src/i18n/*/auth/login.ts:22`) is a plain
interpolation that adds nothing. The Persian copy on the same page does carry `U+200C` at
`src/i18n/fa/auth/login.ts:15` and `:26`, in words rather than inside a number.

That field cannot deliver a separator to a provider. Every path out of it passes the value through
`normalizeDigitsOnly()` (`packages/digit-normalizer/src/index.ts:152`-`154`, which folds localized digits
and then deletes everything that is not an ASCII digit): the OTP request at
`src/auth/useAuthCredentialsStep.ts:166`-`167`, the OTP verification at `:213`-`215`, and the persisted
mid-flow snapshot on both write and read at `src/auth/authFlowStatePolicy.ts:80`-`81` and `:142`-`149`.

**The profile-completion `contact.phone` field is the path that does reach a provider.** The same `/login`
page runs a required profile-completion step (`src/auth/AuthLoginPage.vue:19`, enabled at
`src/auth/profileCompletion/defaultProfileCompletion.ts:174`-`179`), and that step includes a `tel` field
`contact.phone` at `:50`-`54`. Its value leaves the browser through
`src/auth/profileCompletion/profilePolicy.ts:147`-`149` and `:209`-`211`, which call
`normalizeDigitsToAscii` and nothing else: localized digits are folded to ASCII and **every separator
survives**. That input carries no `maxlength` (`src/auth/profileCompletion/ProfileCompletionPanel.vue:22`
-`33`), so a pasted `0912 383 0000`, a typed `0912/383/0000`, and a value carrying `U+00A0` or `U+2028` are
all stored verbatim. The app-wide middleware at `src/boot/digit-normalizer.ts:12`-`16` rewrites digits in
place as the user types and removes no separator at all.

So a stored Alaa phone number can hold any character a person or an editor puts between its digits, and a
later notification to that number is a provider call. **The normaliser is the component that has to absorb
display separators**, because it is the last place before the wire that sees the raw value.

## The normalisation contract

Applied in this order, for both channels:

1. Fold every code point of Unicode general category `Nd` to its ASCII digit, one to one. Do not
   enumerate digit families: an enumerated list is a defect class rather than a fix, and this step
   covered two families only until 2026-07-28. Category `No` is excluded, so superscript digits are not
   folded and an input carrying them is still rejected by step 5. The fold, its canonical implementations
   and its corpus are owned by `/alaa-input-normalization` (`$alaa-input-normalization`); call that
   implementation rather than writing a digit table.
2. Remove every display separator, using the category rule stated in the next section.
3. Reject an input that is empty once the separators are gone, because a value with no digits names no
   recipient.
4. Remove one leading `+` when `98` follows it, or one leading `00` when `98` follows it. Leave any other
   leading `+` or `00` in the string so that step 5 or step 6 rejects the input, because a plus sign or an
   access code in front of anything but the country code marks a number that is not in international form.
5. Reject anything that is not now ASCII digits.
6. Reduce to the ten-digit national significant number: 12 digits beginning `98`, or 11 digits beginning
   `0`, or 10 digits. Reject every other length.
7. Reject a national number that does not match `^9\d{9}$`, because it is not an Iranian mobile number.
8. Render: `98` plus the national number for Bale, `+98` plus the national number for Mediana.

Rejection is a rejection, never a repair. Padding a short number or truncating a long one produces a
syntactically valid number belonging to somebody else.

## The display-separator rule

**Match whitespace, format and dash characters by Unicode general category, and never by a written-out list
of characters.** Scope: this rule governs recipient normalisation for the Bale channel and the Mediana
channel. A written-out list is always one character short of the next change in a display layer, and the
history of these two files is the proof: an enumeration that already carried the space, the tab, the
newline and `U+00A0` still rejected `U+2028`, `U+3000`, `U+000B` and every narrow space, which is how the
two providers came to disagree on four inputs after their first two disagreements had been fixed.

A character is display formatting, and not a digit of the number, when its category is one of these five:

| Category | Class | Members that arrive in practice |
|---|---|---|
| `Cf` | Format | ZWNJ, ZWJ, the bidi marks, the bidi isolates and overrides, the word joiner, the BOM, `U+206F` |
| `Zs` | Space | `U+00A0`, `U+1680`, `U+2000`-`U+200A`, `U+2007`, `U+202F`, `U+205F`, `U+3000` |
| `Zl` | Line | `U+2028` |
| `Zp` | Paragraph | `U+2029` |
| `Pd` | Dash | `U+002D`, `U+2010`-`U+2015`, `U+FF0D` |

Match the whitespace control characters with `str.isspace()` rather than with their category, because
category `Cc` also holds characters that are not separators. `str.isspace()` covers the tab, the line feed,
the vertical tab, the form feed, the carriage return, the four information separators and `U+0085`, and it
covers nothing else inside `Cc`.

Four separators stay written out, as `()._/`, because no Unicode category names them precisely enough to be
matched by one: `Ps` and `Pe` hold every bracket pair in Unicode, and `Po` holds the comma and the
semicolon, which separate two numbers rather than group the digits of one.

Keep a comma in the string so that the length check rejects the input, because a comma means the caller
passed two numbers in one field and that input has to be refused rather than silently concatenated into a
recipient nobody entered.

## The solidus ruling

**Strip the solidus `/` from a recipient number, in both providers.** Scope: recipient normalisation only;
it says nothing about senders, pattern codes, or any other field.

The solidus is not a display artefact, so the category rule above does not reach it and it was decided on
its own merits. Both readings were weighed. Against stripping: no legitimate formatter emits `/` between
the digits of a phone number, so refusing it costs nothing that a formatter produces. For stripping:
`0912/383/0000` is a shape a person types by hand, and the evidence recorded above shows that the value
which actually reaches a provider comes from an unmasked free-text field that a person types into, so what
a formatter produces is not the population that governs. Refusing it therefore rejects a legitimate caller
with an error they cannot diagnose from the number they can see.

Accepting it costs no safety, and that is what settles it. Removing the solidus cannot fabricate a
recipient: `09123830000/09123830001` concatenates to 22 digits and is refused by the same length check that
already refuses the same two numbers separated by a space, and `http://example/09123830000` keeps its
letters and is refused by the digit check. The corpus pins both of those.

## The international-prefix rule

**Remove a leading `+` or a leading `00` only when the country code `98` follows it.** Scope: recipient
normalisation for both channels. Removing either one unconditionally turns a malformed number into a
well-formed one: `+9123830000` and `009123830000` carry no country code at all, and `+09123830000` carries
the domestic trunk zero in the position the country code belongs in. Each of those four shapes is a corpus
case now.

## The shared corpus

`scripts/phone-conformance-corpus.json` is the single fixture both provider skills test against. Each case
is `{"input", "mediana_expected", "bale_expected", "note"}`, and an expected value of `null` means the input
must be rejected with a non-zero exit and a stated reason.

The corpus holds **80 cases: 49 that must render and 31 that must be rejected.** It covers the three
accepted input forms, the bare national number, the `0098` access code, Persian-Indic and Arabic-Indic
digits, mixed digit families, zero-width and bidirectional characters, one member of every separator
category in the table above, the solidus, both wrong lengths, a landline, a foreign number, a sender label,
superscript digits that must be rejected and Devanagari digits that must render, two numbers in one
field separated by a space and by a solidus, a
malformed international prefix in four shapes, the empty string, an ASCII whitespace-only string, a Unicode
whitespace-only string, and a zero-width-only string.

The two copies were reconciled on 2026-07-27 from a 32-case copy here and a 47-case copy under Mediana,
whose 16 shared inputs agreed on every expected value, giving the union of 63 inputs. On 2026-07-28 the
category rule, the solidus ruling and the international-prefix rule closed the last disagreements between
the two implementations and added 17 cases, giving 80.

On 2026-07-28 the Devanagari case was re-ratified from rejected to rendered, moving the split from 48/32
to 49/31. It had been recorded as rejected while this step folded two families only; the browser package
in `client` already folds every `Nd` family, so the recorded rejection described a path no browser user
could reach. The superscript case is unaffected and still rejected, because superscripts are category
`No` rather than `Nd`.

`corpus_sha256` is now `80dcb3723e83d848236ab0cbfbfc62447eec524c62a434737d85682aa653d7dc`.

**The identical file ships in `alaa-sms-provider-mediana/scripts/`.** It is duplicated on purpose: the
`AGENTS.md` conformance rule requires that more than one implementation of one wire format ships a runnable
harness over one corpus, and duplicating a fixture is cheaper than introducing a shared package that a
third skill would then have to own. **If the two copies differ, that is the finding, not a local
customisation** — reconcile them before trusting either validator.

`corpus_sha256` is the SHA-256 of the canonical serialisation of the `cases` array:

```text
sha256(json.dumps(cases, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode('utf-8'))
```

The digest covers the *parsed* cases re-serialised with `ensure_ascii=False`, so it describes the data
rather than the escaping the file is stored in, and a Go, PHP, or JavaScript implementation can reproduce
it without reimplementing Python's JSON escaper. Case order is part of the hashed bytes and is fixed:
accepted cases first, then rejected ones, ascending by Unicode code point of `input` within each group.
The file's own `canonicalization` field states this rule and carries a one-line command that recomputes the
digest from the file alone.

The file itself is `json.dumps(document, ensure_ascii=True, indent=2)` followed by one newline, which keeps
it pure ASCII so that a zero-width character in a test case is visible in review as an escape rather than
invisible as a byte.

## Running the harness

```bash
python3 scripts/validate_bale_payload.py --self-test
```

This drives the normaliser over every corpus case for **both** channels, verifies `corpus_sha256`, and runs
the built-in payload vectors. Exit `0` is a pass. Exit `5` is a divergence in the payload vectors or the
normaliser. Exit `6` means the corpus is missing, unreadable, or fails its checksum — which is what a
hand-edit or a drift from the sibling copy looks like.

Run the sibling harness too when either file changes:

```bash
python3 ../alaa-sms-provider-mediana/scripts/validate_mediana_payload.py --self-test
```

A harness that cannot reach the sibling skill reports the skip and does not report a pass it did not
observe.

To normalise a single number by hand:

```bash
python3 scripts/validate_bale_payload.py --normalize '0912 383 0000' --channel bale
python3 scripts/validate_bale_payload.py --normalize '0912/383/0000' --channel mediana
```

## Adding a case

Add the case to `cases`, re-sort the array (accepted first, then rejected, ascending by Unicode code point
of `input` within each group), recompute `corpus_sha256`, copy the file byte-for-byte into
`alaa-sms-provider-mediana/scripts/`, and run both harnesses. A corpus edited without recomputing the
checksum fails at exit `6` on the next run, which is the intended behaviour: drift becomes a test failure
rather than a review finding.
