# The Normalization Contract

The whole rule, in the form every implementation must satisfy. Read this before changing
any implementation, and before answering "does this character fold?" for any character.

```
text  = NFC(fold_decimal_digits(value))
typed = NFC(strip_display_separators(text(value)))
```

## 1. The fold

**Fold every code point of Unicode general category `Nd` to its ASCII digit, one code
point in and one code point out, and fold nothing else.**

Membership is derived from the category table at runtime. It is never read from a list of
digit families written into the source: a written list is always one Unicode release short,
and the two enforcement points then disagree exactly when their lists differ. The shipped
browser package carries 75 hand-listed family zeros today, eight of which are unassigned
under Unicode 14.0.0 — proof that the list and the category have already drifted apart.

The ASCII value of an `Nd` code point is derived, not tabulated. The Unicode Standard
requires the ten decimal digits of a script to be encoded contiguously and in ascending
order from zero, so within a maximal run of adjacent `Nd` code points a code point's value
is its offset from the start of the run, modulo ten. Runs longer than ten exist:
`U+1D7CE`-`U+1D7FF` is five mathematical digit families packed end to end, which is why the
offset is taken modulo ten and never clamped. Checked against `unicodedata.digit()` for all
660 `Nd` code points of Unicode 14.0.0: 62 maximal runs, every length a multiple of ten,
zero mismatches.

**Never widen the predicate.** `\p{N}`, `str.isdigit()`, `Character.isDigit`,
`unicode.IsNumber`, `is_numeric` and `ctype_digit` each accept a set that is either wider
or narrower than `Nd`, and the wide ones reach category `No`. `x²` folded to `x2` is a
different statement. Name the category in the source — `\p{Nd}`, `unicode.Is(unicode.Nd, r)`,
`unicodedata.category(c) == "Nd"` — so a reviewer can see which set was meant.

## 2. What is deliberately not folded

| Character | Category | Why it stays |
| --- | --- | --- |
| `U+066B` ARABIC DECIMAL SEPARATOR, `U+066C` ARABIC THOUSANDS SEPARATOR | `Po` | **The trap.** `١٬٢٣٤` is one thousand two hundred thirty-four. Map `U+066C` to `,` and a parser that reads `,` as a decimal point returns `1.234` — a 1000x error, silent, in a price or a score. Map `U+066B` to `.` and the same error runs inverted. In a phone field, `U+066C` to `,` manufactures the two-numbers-in-one-field shape the phone rule refuses. Leave both and let validation reject: `unexpected_characters` is a diagnosable error, a wrong number is not. |
| `U+00B2 U+00B3 U+00B9 U+2070 U+2074`-`U+2079`, the subscripts, `①②`, `½ ⅓` | `No` | They are presentation forms and numerals, not positional decimal digits. Folding them changes what the text says. |
| `Ⅰ Ⅱ Ⅲ` | `Nl` | Same. |
| `U+060C` ARABIC COMMA, `U+061B` ARABIC SEMICOLON, `U+061F` ARABIC QUESTION MARK | `Po` | Their ASCII counterparts carry parsing meaning in CSV, in lists, and in "two numbers in one field". Mapping `،` to `,` manufactures a delimiter. |
| `U+064A` yeh, `U+0643` kaf, and every other yeh, kaf, heh and hamza form | `Lo` | Folding a letter rewrites Arabic-language content into a word nobody wrote, and it is not reversible: `كتاب عربي` is Arabic, not badly-typed Persian, and `news` and `content` carry Arabic quotations. Letter folding is a **search-key** rule: confine it to a derived index column, never the stored value. |
| `U+0640` TATWEEL | `Lm` | Pure decoration, so deleting it is tempting — but this contract only maps in `text` mode, and a deletion changes rendered glyph runs. Strip it in a search key if you want one. |
| `U+200C` ZWNJ, in `text` mode | `Cf` | Orthographically significant in Persian: `می‌رود` is not `میرود`. Live content depends on it. It is removed in `typed` mode only, where the whole field is one number. |

## 3. The two modes

**`text` is the default and applies to every string in the request, including free text.**
It folds digits and applies NFC. It deletes nothing, inserts nothing, trims nothing, and
rewrites no letter.

That restraint is what makes free-text folding safe without a parser. Because the fold is a
1:1 map over code points it cannot change the code-point length of a string, and it cannot
damage an HTML tag, an attribute quote, a markdown fence, a JSON structure, a URL, or an
ASCII identifier — all of those are ASCII, and ASCII digits map to themselves. The corpus
pins this with a real `arvanvod.ir` master.m3u8 URL, a Crockford Base32 id, a UUIDv7, an
`<img>` tag and an ASCII code fence, all of which come back byte-identical.

It does change two things, and both are repairs rather than damage: a URL whose path
segment is written in Persian digits was already a URL no server serves, and a code fence
containing `const limit = ۱۲۳;` was already code that does not compile. The one genuine loss
is a document that deliberately demonstrates a non-ASCII digit; the owner's ruling accepts
that cost explicitly.

**Never do HTML-aware or markdown-aware exclusion.** Parsing markup to protect a `<code>`
element costs a parser in four languages, is unbounded work on a 5000-character comment, and
cannot be made byte-identical across runtimes. If one field must be exempt, exempt it **by
field name** in a per-service list that a reviewer can read.

**`typed` is opted into per field**, for a field whose entire value is one number or one
code: a mobile number, an OTP, a national code, a postal code. It additionally removes
display separators, matched by Unicode general category `{Cf, Zs, Zl, Zp, Pd}`, plus the
whitespace control characters, plus the literal set `()._/`. That separator rule is owned by
`/alaa-bale-provider` (`$alaa-bale-provider`) and `/alaa-sms-provider-mediana`
(`$alaa-sms-provider-mediana`); see `references/60-provider-seam-and-open-items.md` for why
it is reproduced here rather than moved.

## 4. NFC, after the fold, never NFKC

NFC composes and does nothing else. NFKC would fold the fullwidth digits and the
superscripts to ASCII by a second, different rule, so "what is folded" would have two
answers, and it also rewrites Arabic presentation forms and ligatures — the letter folding
this contract refuses.

NFC runs **after** the fold, and in `typed` mode a second time after separator removal,
because removing a format character can bring a base character and a combining mark
together and the output is required to be in NFC.

Both sides must pick the same form. Every consequence of picking differently is silent: a
`max:` rule measures different lengths on the two sides, a unique index or an equality
comparison sees two strings that render identically as different values, an idempotency key
derived from content stops matching, and the conformance harness reports what looks like a
digit bug when the implementations differ only in composition.

## 5. Properties every implementation must hold

1. **Total.** Defined for every string. Never throws, never rejects, never returns an error.
2. **Idempotent.** `f(f(x)) == f(x)`. This is what makes it safe to fold in the browser, in
   middleware, and again in a worker.
3. **Code-point iteration.** Not UTF-16 code units, not bytes. An implementation that walks
   with `charCodeAt` over `.length`, or with `strlen`/`str_replace` instead of `preg_*` with
   `/u`, splits the surrogate pair of an astral digit such as `U+1D7CE` and emits mojibake.
   The corpus pins five astral families for exactly this.
4. **Length in code points is unchanged by `text` mode**, and `typed` output never grows.
5. **Values only, never keys.** Folding an object key renames a field.
6. **Invalid UTF-8 is returned unchanged.** It is not text and this contract does not repair
   it; validation rejects it. Repairing would insert `U+FFFD`, and this contract never
   inserts. Go and PHP check explicitly; JavaScript and Python strings cannot hold it.
7. **Unicode data no older than 14.0.0**, the version the corpus expectations were produced
   under. The harness prints each runtime's version and fails one that is older.

Property 7 has a live wrinkle worth knowing: PHP can carry two Unicode data versions at
once, PCRE's for the category test and ICU's or the polyfill's for NFC. The harness prints
both when it can read them.

## 6. Order

Normalization runs **before** validation, so `max:255`, `max:5000`, `digits:5` and every
other rule measures the normalized value on both sides. Normalization never rejects;
validation does, and the phone grammar stays with the two provider skills.
