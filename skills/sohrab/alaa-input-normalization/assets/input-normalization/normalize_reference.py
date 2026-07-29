#!/usr/bin/env python3
"""Canonical Python implementation of the Alaa input-boundary normalization contract.

Owner: the skill `alaa-input-normalization`. This is the fourth canonical implementation
and the one `scripts/normalization-corpus.json` was generated from, so every expected
value in that corpus was produced rather than asserted. The other three implementations
sit beside this file: `input-normalization.ts`, `InputNormalization.php` and
`input_normalization.go`. `scripts/normalization-conformance.sh` drives all four over the
one corpus, and a change to any of them is proved only by that harness.

Two modes, one pipeline:

    text  = NFC(fold_decimal_digits(s))
            The global rule. Every Unicode decimal digit (general category Nd) folds to
            its ASCII 0-9 equivalent, one code point in, one code point out. Nothing is
            deleted, nothing is inserted, no letter is rewritten. Then NFC.

    typed = NFC(strip_display_separators(text))
            The typed-field rule, used for a field whose whole value is a number or a
            code: a mobile number, a national code, an OTP, a postal code. It adds the
            separator-folding rule already settled by alaa-bale-provider and
            alaa-sms-provider-mediana: Unicode categories {Cf, Zs, Zl, Zp, Pd}, plus
            str.isspace(), plus the literal set "()._/" - never an enumerated character
            list.

Both modes are TOTAL and IDEMPOTENT. Normalization never rejects. Rejection belongs to
validation, which runs after normalization and is owned elsewhere (the phone grammar
stays with the two provider skills).

Run this file directly to verify the corpus, or to regenerate it:

    python3 normalize_reference.py --self-test         verify corpus + properties
    python3 normalize_reference.py --normalize TEXT [--mode text|typed]
    python3 normalize_reference.py --emit-corpus       rewrite the corpus

`--emit-corpus` rewrites every expectation in the corpus from this file, so run it only
when the contract itself has changed and the change is ratified. Regenerating the corpus
to make a failing implementation pass destroys the only evidence the harness produces.

The corpus and the phone-input capture are located by searching upward from this file for
a directory holding `scripts/normalization-corpus.json`, at most four levels, and can be
named outright with `--corpus` and `--phone-inputs`. Nothing here indexes a parent by
number, so moving this file one directory deeper does not silently read another corpus.

Exit codes, the same numbering as `scripts/normalization-conformance.sh`:
    0 ok    1 disagreement / property failure    2 usage    6 corpus missing or checksum
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_CORPUS = 6

CORPUS_NAME = "normalization-corpus.json"
PHONE_INPUTS_NAME = "_phone_inputs.b64"


def locate(name: str) -> Path:
    """Find one shipped file by marker, never by counting parent directories.

    Search order, each a path that is printed when nothing matches:
    beside this file, then `scripts/<name>` in this directory and in each of the four
    directories above it. A caller that knows the path passes it instead.
    """
    here = Path(__file__).resolve().parent
    candidates = [here / name, here / "scripts" / name]
    candidates += [parent / "scripts" / name for parent in list(here.parents)[:4]]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        f"{name} not found. Tried:\n  "
        + "\n  ".join(str(candidate) for candidate in candidates)
        + "\nName it outright with --corpus or --phone-inputs."
    )

# --- The digit fold -----------------------------------------------------------------
#
# Scope: Unicode general category Nd (Decimal_Number) only.
#
# Nd is the set of code points that carry a positional decimal value 0-9 in some script:
# Arabic-Indic, Extended Arabic-Indic (Persian), Devanagari, Bengali, Thai, Lao,
# fullwidth, the mathematical alphanumeric digit runs, and about seventy more families.
# unicodedata.digit() returns that value.
#
# Nd deliberately EXCLUDES category No (Other_Number), which holds the superscripts
# U+00B2 U+00B3 U+00B9 U+2070 U+2074-U+2079, the subscripts, the circled and
# parenthesised digits, the fractions and the Roman numerals. Those are presentation
# forms and numerals, not positional decimal digits, and folding them changes meaning:
# "x²" is x squared, not x2. A fold written against str.isdigit(), \p{N}, or
# unicode.IsDigit() reaches into No and is therefore wrong; a fold written against the
# Nd category does not. This is the same trap that let str.isdigit() accept
# "۱۲۳۴۵۶" as a valid OTP.
#
# NOT folded, deliberately - see references in ../normalization-facts.md:
#   U+066B ARABIC DECIMAL SEPARATOR and U+066C ARABIC THOUSANDS SEPARATOR (category Po).
#     Mapping them to "." and "," changes a number's value by a factor of 1000 the
#     moment a downstream parser reads the ASCII character with the other locale's
#     meaning. They are left alone; a numeric field rejects them at validation.
#   U+060C ARABIC COMMA, U+061B ARABIC SEMICOLON, U+061F ARABIC QUESTION MARK.
#   U+0640 ARABIC TATWEEL - pure decoration, but deleting it is a deletion, and this
#     contract only maps.
#   Arabic yeh U+064A / kaf U+0643 versus Persian yeh U+06CC / keheh U+06A9, and the
#     other yeh, kaf, heh and hamza forms. Folding a letter rewrites Arabic-language
#     content into a word nobody wrote and is not reversible.
#   U+200C ZWNJ in text mode. In Persian orthography it is significant: it is what
#     separates "می‌رود" from "میرود".
#     It is removed only in typed mode, where the whole field is a number.


def fold_decimal_digits(text: str) -> str:
    """Fold every Unicode decimal digit (category Nd) to its ASCII equivalent.

    One code point in, one code point out. Never deletes, never inserts, never touches a
    letter, a separator, or a category-No numeral. Because the mapping is 1:1 over code
    points, it cannot change the structure of a URL, an HTML tag, a markdown fence, or a
    JSON string that is written in ASCII: those contain no Nd code point outside 0-9,
    and 0-9 map to themselves.
    """
    out = []
    for character in text:
        if unicodedata.category(character) == "Nd":
            out.append(str(unicodedata.digit(character)))
        else:
            out.append(character)
    return "".join(out)


# --- The display-separator rule ------------------------------------------------------
#
# Copied verbatim in intent from alaa-bale-provider/scripts/validate_bale_payload.py:91
# -118 and alaa-sms-provider-mediana/scripts/validate_mediana_payload.py:69-96, which
# are byte-identical to each other in this block. Do not replace it with a character
# list: an enumeration is always one character short of the next display-layer change.

SEPARATOR_CATEGORIES = frozenset({"Cf", "Zs", "Zl", "Zp", "Pd"})

# Match the whitespace control characters with str.isspace() rather than the Cc
# category, because Cc also holds characters that are not separators. str.isspace()
# covers the tab, the line feed, the vertical tab, the form feed, the carriage return,
# the four information separators and U+0085, and nothing else inside Cc.

# These four stay written out because no Unicode category names them precisely enough:
# Ps and Pe hold every bracket pair in Unicode, and Po holds the comma and the
# semicolon, which separate two numbers rather than group the digits of one.
LITERAL_SEPARATORS = frozenset("()._/")


def is_display_separator(character: str) -> bool:
    """Report whether one character is display formatting rather than a digit."""
    return (
        unicodedata.category(character) in SEPARATOR_CATEGORIES
        or character.isspace()
        or character in LITERAL_SEPARATORS
    )


def strip_display_separators(text: str) -> str:
    """Remove every display separator, keeping digits, letters, and the leading plus."""
    return "".join(c for c in text if not is_display_separator(c))


# --- The two public modes ------------------------------------------------------------
#
# NFC and not NFKC. NFKC would fold the fullwidth digits and the superscripts to ASCII
# itself, silently doing part of this contract's job by a different rule, and it also
# rewrites Arabic presentation forms and ligatures - which is exactly the letter folding
# this contract refuses. NFC composes and nothing more.


def normalize_text(value: str) -> str:
    """The global rule for any string field, including free text."""
    return unicodedata.normalize("NFC", fold_decimal_digits(value))


def normalize_typed(value: str) -> str:
    """The rule for a field whose entire value is a number or a code.

    NFC is applied a second time after separator removal, because removing a format
    character can bring a base character and a combining mark together, and the output
    of this function is required to be in NFC.
    """
    return unicodedata.normalize("NFC", strip_display_separators(normalize_text(value)))


MODES = {"text": normalize_text, "typed": normalize_typed}


# --- Corpus canonicalisation ---------------------------------------------------------
#
# Identical rule to scripts/phone-conformance-corpus.json in both provider skills,
# verified by recomputation on 2026-07-28 against the digest recorded at the time,
# 7a4250cf64e730d51ef92512975e864cbcfa5da919f658e0f974c50e8d54b548. That corpus was
# re-ratified later the same day and its digest is now
# 80dcb3723e83d848236ab0cbfbfc62447eec524c62a434737d85682aa653d7dc; only one expectation
# changed, so every input carried here is unaffected.


def corpus_digest(cases: list[dict]) -> str:
    """SHA-256 of the parsed cases re-serialised with ensure_ascii=False."""
    payload = json.dumps(cases, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


CANONICALIZATION = (
    "On disk: json.dump(document, handle, ensure_ascii=True, indent=2) followed by a "
    "single trailing newline, so the file is pure ASCII, every non-ASCII character "
    "appears as a \\uXXXX escape, and a zero-width character in a case is visible in "
    "review as an escape rather than invisible as a byte. Checksum: corpus_sha256 is "
    "the lowercase hex SHA-256 of json.dumps(cases, ensure_ascii=False, sort_keys=True, "
    "separators=(',', ':')).encode('utf-8') - the parsed cases re-serialised with the "
    "real characters in UTF-8, not the on-disk escapes, so a Go, PHP, JavaScript or Lua "
    "implementation can reproduce it without reimplementing Python's escaper. Case "
    "order is part of the hashed bytes and is fixed: ascending by the tuple of Unicode "
    "code points of input, ties broken by note. Reproduce the checksum from this file "
    "alone: python3 -c \"import hashlib,json,sys; d=json.load(open(sys.argv[1],"
    "encoding='utf-8')); print(hashlib.sha256(json.dumps(d['cases'],ensure_ascii=False,"
    "sort_keys=True,separators=(',',':')).encode()).hexdigest())\" "
    "normalization-corpus.json"
)


# --- Case sources --------------------------------------------------------------------

# Every input from scripts/phone-conformance-corpus.json (both provider skills, 80
# cases, byte-identical copies verified with cmp on 2026-07-28). They are carried here
# as NORMALIZATION cases only: this corpus records what the string becomes, never
# whether it is a valid recipient. The rendering columns mediana_expected and
# bale_expected stay in the phone corpus and are not duplicated, so the 80-case phone
# corpus is referenced rather than forked.
def load_phone_corpus_inputs(path: Path | None = None) -> list[tuple[str, str]]:
    """Load the 80 phone-corpus inputs exactly, from a gzip+base64 capture of the file.

    The capture is byte-exact: it was produced by re-serialising the parsed cases of
    scripts/phone-conformance-corpus.json on 2026-07-28, when both copies were verified
    byte-identical with cmp and the digest recorded at the time,
    7a4250cf64e730d51ef92512975e864cbcfa5da919f658e0f974c50e8d54b548, was reproduced. The phone
    corpus was re-ratified later that day and now records
    80dcb3723e83d848236ab0cbfbfc62447eec524c62a434737d85682aa653d7dc: the Devanagari case moved
    from rejected to rendered. No input changed, so this capture is unaffected.
    Several inputs carry U+000B, U+0085 and bidi controls that do not survive being
    retyped, which is why they are carried as an encoded blob rather than as literals.
    """
    source = path if path is not None else locate(PHONE_INPUTS_NAME)
    payload = gzip.decompress(base64.b64decode(source.read_text()))
    return [
        (case["input"], "phone corpus: " + case["note"])
        for case in json.loads(payload)
    ]


NEW_CASES: list[tuple[str, str]] = [
    # --- digit families, one representative per family ---
    ("٠١٢٣٤٥٦٧٨٩", "Arabic-Indic U+0660-U+0669, all ten"),
    ("۰۱۲۳۴۵۶۷۸۹", "Extended Arabic-Indic (Persian) U+06F0-U+06F9, all ten"),
    ("߀߉", "NKo digits U+07C0 and U+07C9"),
    ("०९", "Devanagari digits U+0966 and U+096F"),
    ("০৯", "Bengali digits U+09E6 and U+09EF"),
    ("๐๙", "Thai digits U+0E50 and U+0E59"),
    ("໐໙", "Lao digits U+0ED0 and U+0ED9"),
    ("༠༩", "Tibetan digits U+0F20 and U+0F29"),
    ("၀၉", "Myanmar digits U+1040 and U+1049"),
    ("០៩", "Khmer digits U+17E0 and U+17E9"),
    ("᠐᠙", "Mongolian digits U+1810 and U+1819"),
    ("０９", "Fullwidth digits U+FF10 and U+FF19"),
    ("\U0001d7ce\U0001d7d7", "Mathematical bold digits U+1D7CE-U+1D7D7, astral: a JavaScript implementation that walks UTF-16 code units instead of code points splits these surrogate pairs and produces mojibake"),
    ("\U0001d7f6\U0001d7ff", "Mathematical monospace digits U+1D7F6-U+1D7FF, astral"),
    ("\U0001e950\U0001e959", "Adlam digits U+1E950-U+1E959, astral"),
    ("\U0001fbf0\U0001fbf9", "Segmented digits U+1FBF0-U+1FBF9, astral"),
    ("\U000104a0\U000104a9", "Osmanya digits U+104A0-U+104A9, astral"),
    ("۱١१１\U0001d7cf1", "Five digit families and ASCII in one string, all meaning one"),
    # --- category No: must NOT fold ---
    ("x² + y³", "Superscript two and three, category No. Folding these turns x squared into x2"),
    ("①②", "Circled digits one and two, category No"),
    ("½ ⅓", "Vulgar fractions, category No"),
    ("ⅠⅡⅢ", "Roman numerals I II III, category Nl"),
    # --- the Arabic numeric separators: the trap ---
    ("٣٫١٤", "Arabic decimal separator U+066B between digits: 3.14 in Arabic notation. The digits fold, U+066B stays, because mapping it to '.' or ',' changes the value the moment a parser reads the other locale's meaning"),
    ("١٬٢٣٤", "Arabic thousands separator U+066C: 1,234. It stays; mapping it to ',' in a phone field would manufacture the two-numbers-in-one-field shape the phone rule rejects"),
    ("۳٫۱۴٬۰", "Both Arabic numeric separators with Persian digits"),
    ("1،2", "Arabic comma U+060C between two numbers: never folded to ASCII comma"),
    ("a؛b", "Arabic semicolon U+061B: never folded"),
    # --- letters that must NOT fold ---
    ("يك", "Arabic yeh U+064A and kaf U+0643: NOT folded to Persian ی ک. Folding a letter rewrites Arabic-language content"),
    ("یک", "Persian yeh U+06CC and keheh U+06A9: already Persian, unchanged"),
    ("كتاب عربي", "An Arabic phrase (Arabic 'Arabic book'). Nothing here is a digit, so nothing changes"),
    ("مدلـــ ۹۴", "Tatweel U+0640 used to stretch a word, with Persian digits beside it: digits fold, tatweel survives"),
    ("ة ؤ ئ أ إ", "Arabic teh marbuta, waw/yeh with hamza, alef with hamza: NOT folded. auth/app/Traits/CharacterCommon.php:111-129 maps all of these; that mapping is a search-key rule, not an input-boundary rule"),
    # --- ZWNJ in several positions ---
    ("می‌رود", "ZWNJ inside a Persian word ('he goes'). Text mode keeps it: deleting it produces a different word"),
    ("‌آماده", "Leading ZWNJ before a Persian word"),
    ("آماده‌", "Trailing ZWNJ after a Persian word"),
    ("آماده‌سازی ۱۴۰۴", "ZWNJ inside a real content-service description word, with a Persian year. Same shape as content/database/seeders/VodCatalogSeeder.php:779"),
    ("۱‌۲‌۳", "ZWNJ between Persian digits: text mode keeps it, typed mode removes it"),
    ("‌", "ZWNJ alone"),
    # --- combining marks and NFC ---
    ("آ", "Arabic alef U+0627 plus combining maddah above U+0653: NFC composes to U+0622"),
    ("ؤ", "Arabic waw U+0648 plus combining hamza above U+0654: NFC composes to U+0624"),
    ("يٕ", "Arabic yeh plus combining hamza below U+0655: NFC composes to U+0625's family member"),
    ("é", "Latin e plus combining acute: NFC composes to é. Pins that the contract is NFC and not 'leave alone'"),
    ("é", "Precomposed é: already NFC, unchanged. With the previous case this pins NFC idempotence"),
    ("ا‌ٓ", "Alef, ZWNJ, combining maddah. Text mode keeps the ZWNJ so nothing composes; typed mode removes the ZWNJ and then composes, which is why typed mode applies NFC a second time"),
    ("كـ۱ٰ", "Kaf, tatweel, Persian one, superscript alef U+0670 (a combining mark that never composes)"),
    # --- URLs, code, ids ---
    ("https://vk1405.arvanvod.ir/VEwPGWPZGx/h_,144_200,240_400/master.m3u8", "An all-ASCII URL taken from content/database/seeders/VodCatalogSeeder.php:783. No Nd code point outside 0-9, so the fold is the identity here: a well-formed URL cannot be damaged"),
    ("https://example.ir/۱۴۴/master.m3u8", "A URL whose path segment is written in Persian digits. The fold rewrites it - and it has to, because a URL with Persian digits in its path is already a different URL from the ASCII one and no server serves it"),
    ("```\nconst limit = ۱۲۳;\n```", "A fenced code block containing Persian digits. The fold rewrites them. This is the one case where free-text folding is lossy, and it is lossy because the author typed a Persian digit into code that will not compile with it"),
    ("```\nconst limit = 123;\n```", "A fenced code block written in ASCII: the fold is the identity"),
    ("<p dir=\"rtl\">مدل ۹۴</p>", "An HTML fragment of the shape news bodyHtml carries (client/src/news/useNewsDetail.ts:116, rendered with v-html at client/src/news/NewsShowRoutePage.vue:55). The fold is 1:1 over code points, so tag structure and attribute quoting are untouched"),
    ("<img src=\"https://cdn.example.ir/a1b2.png\" width=\"640\">", "An HTML img tag with ASCII digits in the src and the width: identity"),
    ("01HQ3G7Z8YV2K4M6N8P0R2T4W6", "A Crockford Base32 identifier from alaa-crockford-base32-codecs: ASCII, identity"),
    ("018f7c8e-1f2a-7c3d-8e4f-5a6b7c8d9e0f", "A UUIDv7: ASCII, identity"),
    # --- adjacency, mixed script, structure ---
    ("کد ۱۲A", "Digits adjacent to a Latin letter and a Persian word, the exact string client/packages/digit-normalizer/test/digit-normalizer.test.ts:52 pins"),
    ("A۱B١2C３3", "Digits from four families wedged between Latin letters with no separators"),
    ("۱۲۳abc١٢٣", "Two digit runs from two families around an ASCII word"),
    ("سلام ۱۲۳ hello 456 مرحبا ١٢٣", "Persian, Latin and Arabic in one string with three digit families"),
    # --- separators-only and empty ---
    ("", "Empty string. Both modes return the empty string; normalization never rejects"),
    (" \t\n\r", "ASCII whitespace only: text mode keeps it, typed mode empties it"),
    ("   　  ", "Unicode separators only, one from each of Zs, Zl and Zp"),
    ("()._/", "The four literal separators plus the solidus, alone"),
    ("---–—－", "Dashes from category Pd, alone"),
    ("​‌‍⁠﻿", "Zero-width and format characters only, category Cf"),
    # --- length and idempotence pressure ---
    ("۱" * 2000, "A very long single-family digit run: 2000 code points. Pins that the fold is linear and that a max-length rule measures the folded value"),
    ("آماده‌سازی ۱۲۳۴۵ " * 200, "A very long mixed Persian sentence with ZWNJ and digits, repeated 200 times: the free-text shape a content or news description actually has"),
    ("0" * 5000, "5000 ASCII zeroes: identity, and exactly the comment-service max:5000 boundary (comment-service/app/Http/Requests/Comment/StoreCommentRequest.php:31)"),
]


def build_cases(phone_inputs: list[tuple[str, str]]) -> list[dict]:
    seen: dict[str, str] = {}
    for value, note in phone_inputs + NEW_CASES:
        if value in seen:
            continue
        seen[value] = note
    cases = [
        {
            "input": value,
            "text_expected": normalize_text(value),
            "typed_expected": normalize_typed(value),
            "note": note,
        }
        for value, note in seen.items()
    ]
    cases.sort(key=lambda case: ([ord(c) for c in case["input"]], case["note"]))
    return cases


def build_document(phone_inputs: list[tuple[str, str]]) -> dict:
    cases = build_cases(phone_inputs)
    return {
        "corpus_name": "alaa-input-normalization",
        "corpus_version": 1,
        "status": "ACTIVE",
        "owner_skill": "alaa-input-normalization",
        "purpose": (
            "One shared fixture for every implementation of the Alaa input-boundary "
            "normalization contract. The browser normalizes at submit and every backend "
            "service normalizes in middleware; a harness drives every implementation "
            "over this file and fails on any disagreement, because a document asserting "
            "parity is not evidence of it."
        ),
        "modes": {
            "text": (
                "NFC(fold_decimal_digits(input)). The global rule for any string field, "
                "including free text. Folds every Unicode general-category-Nd code point "
                "to its ASCII 0-9 equivalent, one code point in and one code point out. "
                "Deletes nothing, inserts nothing, rewrites no letter. Then NFC, never "
                "NFKC."
            ),
            "typed": (
                "NFC(strip_display_separators(text)). The rule for a field whose entire "
                "value is a number or a code - a mobile number, a national code, an OTP, "
                "a postal code. Separators are matched by Unicode general category "
                "{Cf, Zs, Zl, Zp, Pd}, plus str.isspace(), plus the literal set '()._/' "
                "- never by an enumerated character list. This block is the rule already "
                "settled by alaa-bale-provider and alaa-sms-provider-mediana."
            ),
        },
        "totality": (
            "Both modes are total and idempotent: f(x) is defined for every string and "
            "f(f(x)) == f(x). Normalization never rejects. Rejection is validation, and "
            "for a phone number validation stays with the two provider skills."
        ),
        "not_folded": [
            "Category No and Nl numerals: the superscripts, subscripts, circled digits, "
            "fractions and Roman numerals. A fold written against str.isdigit(), \\p{N} "
            "or unicode.IsDigit() reaches into them and is wrong.",
            "U+066B ARABIC DECIMAL SEPARATOR and U+066C ARABIC THOUSANDS SEPARATOR: "
            "mapping them to '.' or ',' changes a number's value by a factor of 1000 the "
            "moment a parser reads the other locale's meaning.",
            "U+060C ARABIC COMMA, U+061B ARABIC SEMICOLON, U+061F ARABIC QUESTION MARK.",
            "U+0640 ARABIC TATWEEL.",
            "Every letter: Arabic yeh U+064A and kaf U+0643 are not folded to Persian "
            "U+06CC and U+06A9, and no yeh, kaf, heh or hamza form is folded to another.",
            "U+200C ZWNJ in text mode: it is orthographically significant in Persian. It "
            "is removed only in typed mode, where the whole field is a number.",
        ],
        "relationship_to_phone_corpus": (
            "Every input from scripts/phone-conformance-corpus.json (80 cases, byte-"
            "identical in alaa-bale-provider and alaa-sms-provider-mediana, digest "
            "80dcb3723e83d848236ab0cbfbfc62447eec524c62a434737d85682aa653d7dc, ratified "
            "2026-07-28) appears here as a normalization case only. "
            "The mediana_expected and bale_expected columns are NOT duplicated here: "
            "phone rendering stays with the provider skills and their corpus is "
            "referenced, never forked. The one case that was in conflict with this "
            "contract - the Devanagari input, which this contract folds - was ratified "
            "on 2026-07-28 as rendered rather than rejected, moving the phone "
            "corpus split from 48/32 to 49/31. See references/60-provider-seam-and-open-items.md."
        ),
        "canonicalization": CANONICALIZATION,
        "corpus_sha256": "",
        "cases": cases,
    }


def write_corpus(path: Path, phone_inputs: Path | None = None) -> dict:
    document = build_document(load_phone_corpus_inputs(phone_inputs))
    document["corpus_sha256"] = corpus_digest(document["cases"])
    with path.open("w", encoding="utf-8") as handle:
        json.dump(document, handle, ensure_ascii=True, indent=2)
        handle.write("\n")
    return document


def self_test(path: Path) -> int:
    if not path.exists():
        print(f"corpus missing: {path}", file=sys.stderr)
        return EXIT_CORPUS
    document = json.loads(path.read_text(encoding="utf-8"))
    cases = document["cases"]

    recomputed = corpus_digest(cases)
    if recomputed != document.get("corpus_sha256"):
        print(
            f"corpus checksum mismatch: recorded {document.get('corpus_sha256')} "
            f"recomputed {recomputed}",
            file=sys.stderr,
        )
        return EXIT_CORPUS

    failures = 0
    for index, case in enumerate(cases):
        for mode, expected_key in (("text", "text_expected"), ("typed", "typed_expected")):
            observed = MODES[mode](case["input"])
            expected = case[expected_key]
            if observed != expected:
                failures += 1
                print(
                    f"case {index} mode {mode}: expected {expected!r} observed {observed!r}",
                    file=sys.stderr,
                )
            # idempotence
            if MODES[mode](observed) != observed:
                failures += 1
                print(f"case {index} mode {mode}: not idempotent", file=sys.stderr)
            # output is in NFC
            if unicodedata.normalize("NFC", observed) != observed:
                failures += 1
                print(f"case {index} mode {mode}: output is not NFC", file=sys.stderr)
        # the text fold never changes the code-point count
        if len(normalize_text(case["input"])) != len(
            unicodedata.normalize("NFC", case["input"])
        ):
            failures += 1
            print(f"case {index}: text mode changed the code-point count", file=sys.stderr)
        # typed output retains no display separator, and never grows
        typed = case["typed_expected"]
        if strip_display_separators(typed) != typed:
            failures += 1
            print(f"case {index}: typed output still holds a display separator", file=sys.stderr)
        if len(typed) > len(case["text_expected"]):
            failures += 1
            print(f"case {index}: typed output is longer than text output", file=sys.stderr)

    # ordering is part of the hashed bytes
    ordered = sorted(cases, key=lambda case: ([ord(c) for c in case["input"]], case["note"]))
    if [c["input"] for c in ordered] != [c["input"] for c in cases]:
        failures += 1
        print("case order does not match the canonicalisation rule", file=sys.stderr)

    if failures:
        print(f"\n{failures} failure(s).", file=sys.stderr)
        return EXIT_FAILED

    print(
        f"[OK] self-test passed: {len(cases)} cases x 2 modes, "
        f"idempotence, NFC-stability, length and separator-freedom properties, "
        f"corpus_sha256 {document['corpus_sha256'][:16]}..."
    )
    return EXIT_OK


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-corpus", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--normalize")
    parser.add_argument("--mode", choices=sorted(MODES), default="text")
    parser.add_argument("--corpus", type=Path, default=None)
    parser.add_argument("--phone-inputs", type=Path, default=None)
    args = parser.parse_args(argv)

    if args.emit_corpus:
        corpus = args.corpus if args.corpus is not None else locate(CORPUS_NAME)
        document = write_corpus(corpus, args.phone_inputs)
        print(f"{len(document['cases'])} cases, corpus_sha256 {document['corpus_sha256']}")
        return EXIT_OK
    if args.self_test:
        return self_test(args.corpus if args.corpus is not None else locate(CORPUS_NAME))
    if args.normalize is not None:
        sys.stdout.write(MODES[args.mode](args.normalize) + "\n")
        return EXIT_OK

    parser.print_help()
    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
