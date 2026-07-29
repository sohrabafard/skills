/**
 * Canonical TypeScript implementation of the Alaa input-boundary normalization contract.
 *
 * Owner: the skill `alaa-input-normalization`. Copy this file into a repository unchanged
 * except for the import path it is reached by, so that the result of
 * `scripts/normalization-conformance.sh` still describes the copied code. A defect is
 * fixed here first and re-propagated; a fix applied only where the bug surfaced leaves
 * every other copy running the bug.
 *
 * Two modes, one pipeline:
 *
 *   text  = NFC(foldDecimalDigits(value))
 *           The global rule for every string, including free text. Every Unicode
 *           general-category-Nd code point folds to its ASCII 0-9 equivalent, one code
 *           point in and one code point out. Nothing is deleted, nothing is inserted, no
 *           letter is rewritten.
 *
 *   typed = NFC(stripDisplaySeparators(text(value)))
 *           The rule for a field whose whole value is one number or one code: a mobile
 *           number, an OTP, a national code, a postal code.
 *
 * Both modes are total and idempotent. Normalization never rejects and never throws:
 * rejection is validation, and it runs after this.
 */

/**
 * Category test only. `\p{Nd}` is Decimal_Number and excludes category No, so the
 * superscripts, the circled digits, the fractions and the Roman numerals are not digits
 * here: folding `x²` to `x2` changes what the text says. Never widen this to `\p{N}`.
 */
const DECIMAL_NUMBER = /^\p{Nd}$/u;

/**
 * The display-separator categories, owned by `alaa-bale-provider` and
 * `alaa-sms-provider-mediana` and reproduced here for `typed` mode only. Match by
 * category and never by a written-out list of characters: an enumeration is always one
 * character short of the next change in a display layer.
 */
const SEPARATOR_CATEGORY = /^[\p{Cf}\p{Zs}\p{Zl}\p{Zp}\p{Pd}]$/u;

/**
 * The whitespace control characters. This closed set is exactly the intersection of
 * Python's `str.isspace()` with general category Cc — the tab, the line feed, the
 * vertical tab, the form feed, the carriage return, the four information separators and
 * U+0085 — and it is written out because JavaScript's `\s` covers a different set: it
 * omits U+001C-U+001F and includes U+FEFF. Cc holds characters that are not separators,
 * so the category alone is the wrong test.
 */
const WHITESPACE_CONTROLS = new Set([
  0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x1c, 0x1d, 0x1e, 0x1f, 0x85,
]);

/**
 * These five stay written out because no Unicode category names them precisely enough:
 * Ps and Pe hold every bracket pair in Unicode, and Po holds the comma and the
 * semicolon, which separate two numbers rather than group the digits of one.
 */
const LITERAL_SEPARATORS = new Set(["(", ")", ".", "_", "/"]);

const isDecimalNumber = (codePoint: number): boolean =>
  codePoint >= 0 &&
  codePoint <= 0x10ffff &&
  DECIMAL_NUMBER.test(String.fromCodePoint(codePoint));

/**
 * Return the ASCII digit for one Nd code point, derived from the category table rather
 * than read from a hand-written family list.
 *
 * The Unicode Standard requires the ten decimal digits of a script to be encoded
 * contiguously and in ascending order from zero, so within a maximal run of adjacent Nd
 * code points the value of a code point is its offset from the start of the run, modulo
 * ten. Runs longer than ten exist — U+1D7CE-U+1D7FF is five mathematical digit families
 * packed end to end — which is why the offset is taken modulo ten and not clamped.
 *
 * This derivation was checked against `unicodedata.digit()` for all 660 Nd code points of
 * Unicode 14.0.0: 62 maximal runs, every length a multiple of ten, zero mismatches.
 */
const asciiDigitFor = (codePoint: number): string => {
  let familyStart = codePoint;

  while (familyStart > 0 && isDecimalNumber(familyStart - 1)) {
    familyStart -= 1;
  }

  return String((codePoint - familyStart) % 10);
};

const isDisplaySeparator = (character: string): boolean => {
  const codePoint = character.codePointAt(0);

  if (codePoint === undefined) {
    return false;
  }

  return (
    SEPARATOR_CATEGORY.test(character) ||
    WHITESPACE_CONTROLS.has(codePoint) ||
    LITERAL_SEPARATORS.has(character)
  );
};

/**
 * Fold every Unicode decimal digit to its ASCII equivalent, one code point in and one
 * code point out.
 *
 * `for...of` over a string iterates code points, not UTF-16 code units. Iterating with
 * `charCodeAt` or an index over `.length` splits the surrogate pair of an astral digit
 * such as U+1D7CE and produces mojibake; the corpus pins five astral families for
 * exactly that reason.
 */
export const foldDecimalDigits = (value: string): string => {
  let folded = "";

  for (const character of value) {
    const codePoint = character.codePointAt(0) as number;

    folded += isDecimalNumber(codePoint) ? asciiDigitFor(codePoint) : character;
  }

  return folded;
};

/** Remove every display separator. Used by `typed` mode only, never by `text` mode. */
export const stripDisplaySeparators = (value: string): string => {
  let kept = "";

  for (const character of value) {
    if (!isDisplaySeparator(character)) {
      kept += character;
    }
  }

  return kept;
};

/**
 * The global rule for any string field, including free text.
 *
 * NFC and never NFKC. NFKC folds the fullwidth digits and the superscripts to ASCII by a
 * second, different rule, so "what is folded" would have two answers, and it rewrites
 * Arabic presentation forms and ligatures — the letter folding this contract refuses.
 */
export const normalizeText = (value: string): string =>
  foldDecimalDigits(value).normalize("NFC");

/**
 * The rule for a field whose entire value is one number or one code.
 *
 * NFC is applied a second time after separator removal because removing a format
 * character can bring a base character and a combining mark together, and the output of
 * this function is required to be in NFC.
 */
export const normalizeTyped = (value: string): string =>
  stripDisplaySeparators(normalizeText(value)).normalize("NFC");

export type NormalizationMode = "text" | "typed";

/** Dispatch by mode name, for a caller that carries the mode as data. */
export const normalize = (value: string, mode: NormalizationMode): string =>
  mode === "typed" ? normalizeTyped(value) : normalizeText(value);

/**
 * Report whether a string still carries a non-ASCII decimal digit.
 *
 * For diagnostics and tests only. Never use it to reject input: normalization is total
 * and a field that fails this check has not been normalized yet, which is a defect in the
 * caller rather than in the user's typing.
 */
export const hasNonAsciiDecimalDigits = (value: string): boolean => {
  for (const character of value) {
    const codePoint = character.codePointAt(0) as number;

    if (isDecimalNumber(codePoint) && (codePoint < 0x30 || codePoint > 0x39)) {
      return true;
    }
  }

  return false;
};
