<?php

declare(strict_types=1);

namespace Alaa\Support\Input;

/**
 * Canonical PHP implementation of the Alaa input-boundary normalization contract.
 *
 * Owner: the skill `alaa-input-normalization`. Copy this file into a repository unchanged
 * except for the namespace, so that the result of `scripts/normalization-conformance.sh`
 * still describes the copied code. Fix a defect here first and re-propagate it.
 *
 * Two modes, one pipeline:
 *
 *   text  = NFC(foldDecimalDigits(value))   every string, including free text
 *   typed = NFC(stripDisplaySeparators(text(value)))   one field that holds one number
 *
 * Both modes are total and idempotent. Normalization never rejects and never throws:
 * rejection is validation, and it runs after this.
 *
 * Requires ext-mbstring, and requires `Normalizer` — which reaches this fleet through
 * `symfony/polyfill-intl-normalizer` because no image installs ext-intl. Declare
 * `symfony/polyfill-intl-normalizer` in the consuming repository's composer.json as a
 * direct dependency: it is present in every composer.lock today only transitively, and a
 * transitive dependency can be dropped by an unrelated upgrade.
 */
final class InputNormalization
{
    /**
     * Category test only. `\p{Nd}` is Decimal_Number and excludes category No, so the
     * superscripts, the circled digits, the fractions and the Roman numerals are not
     * digits here: folding `x²` to `x2` changes what the text says. Never widen this to
     * `\p{N}` and never use `ctype_digit` or `is_numeric` as a substitute.
     */
    private const DECIMAL_NUMBER = '/^\p{Nd}$/u';

    /**
     * The display-separator categories, owned by `alaa-bale-provider` and
     * `alaa-sms-provider-mediana` and reproduced here for `typed` mode only. Match by
     * category and never by a written-out list of characters: an enumeration is always
     * one character short of the next change in a display layer.
     */
    private const SEPARATOR_CATEGORY = '/^[\p{Cf}\p{Zs}\p{Zl}\p{Zp}\p{Pd}]$/u';

    /**
     * The whitespace control characters: exactly the intersection of Python's
     * `str.isspace()` with general category Cc. Written out because Cc also holds
     * characters that are not separators, so the category alone is the wrong test, and
     * because PCRE's `\s` covers a different set.
     *
     * @var list<int>
     */
    private const WHITESPACE_CONTROLS = [0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x1C, 0x1D, 0x1E, 0x1F, 0x85];

    /**
     * These five stay written out because no Unicode category names them precisely
     * enough: Ps and Pe hold every bracket pair in Unicode, and Po holds the comma and
     * the semicolon, which separate two numbers rather than group the digits of one.
     *
     * @var list<string>
     */
    private const LITERAL_SEPARATORS = ['(', ')', '.', '_', '/'];

    /** The global rule for any string field, including free text. */
    public static function text(string $value): string
    {
        return self::composeNfc(self::foldDecimalDigits($value));
    }

    /**
     * The rule for a field whose entire value is one number or one code.
     *
     * NFC is applied a second time after separator removal because removing a format
     * character can bring a base character and a combining mark together, and the output
     * of this method is required to be in NFC.
     */
    public static function typed(string $value): string
    {
        return self::composeNfc(self::stripDisplaySeparators(self::text($value)));
    }

    /** Dispatch by mode name, for a caller that carries the mode as data. */
    public static function normalize(string $value, string $mode): string
    {
        return $mode === 'typed' ? self::typed($value) : self::text($value);
    }

    /**
     * Fold every Unicode decimal digit to its ASCII equivalent, one code point in and one
     * code point out.
     */
    public static function foldDecimalDigits(string $value): string
    {
        // A string that carries no non-ASCII decimal digit is returned by the fold
        // unchanged, because ASCII digits map to themselves. Skipping the walk here is a
        // shortcut through the same answer, not a second rule.
        if (preg_match('/(?=\p{Nd})[^0-9]/u', $value) !== 1) {
            return $value;
        }

        $folded = '';

        foreach (self::codePoints($value) as $character) {
            $codePoint = mb_ord($character, 'UTF-8');

            $folded .= self::isDecimalNumber($codePoint)
                ? self::asciiDigitFor($codePoint)
                : $character;
        }

        return $folded;
    }

    /** Remove every display separator. Used by `typed` mode only, never by `text` mode. */
    public static function stripDisplaySeparators(string $value): string
    {
        $kept = '';

        foreach (self::codePoints($value) as $character) {
            if (! self::isDisplaySeparator($character)) {
                $kept .= $character;
            }
        }

        return $kept;
    }

    /**
     * Report whether a string still carries a non-ASCII decimal digit.
     *
     * For diagnostics and tests only. Never use it to reject input: a value that fails
     * this check has not been normalized yet, which is a defect in the caller rather than
     * in the user's typing.
     */
    public static function hasNonAsciiDecimalDigits(string $value): bool
    {
        return preg_match('/(?=\p{Nd})[^0-9]/u', $value) === 1;
    }

    /**
     * Split into code points.
     *
     * A string that is not valid UTF-8 is not text, and this contract does not repair it:
     * every implementation returns such a string unchanged and lets validation reject it.
     * Repairing it would insert U+FFFD, and this contract never inserts.
     *
     * @return list<string>
     */
    private static function codePoints(string $value): array
    {
        if (! mb_check_encoding($value, 'UTF-8')) {
            return [$value];
        }

        return mb_str_split($value, 1, 'UTF-8');
    }

    private static function isDecimalNumber(int $codePoint): bool
    {
        if ($codePoint < 0 || $codePoint > 0x10FFFF) {
            return false;
        }

        $character = mb_chr($codePoint, 'UTF-8');

        // Compare against false explicitly. `mb_chr(0x30) ?: ''` yields the empty string,
        // because the one-character string "0" is falsy in PHP, and the family-start scan
        // below then stops one code point early and folds every ASCII digit to the digit
        // before it. The conformance harness caught exactly that on its first run.
        if ($character === false) {
            return false;
        }

        return preg_match(self::DECIMAL_NUMBER, $character) === 1;
    }

    /**
     * Return the ASCII digit for one Nd code point, derived from the category table
     * rather than read from a hand-written family list.
     *
     * The Unicode Standard requires the ten decimal digits of a script to be encoded
     * contiguously and in ascending order from zero, so within a maximal run of adjacent
     * Nd code points the value of a code point is its offset from the start of the run,
     * modulo ten. Runs longer than ten exist — U+1D7CE-U+1D7FF is five mathematical digit
     * families packed end to end — which is why the offset is taken modulo ten and not
     * clamped.
     */
    private static function asciiDigitFor(int $codePoint): string
    {
        $familyStart = $codePoint;

        while ($familyStart > 0 && self::isDecimalNumber($familyStart - 1)) {
            $familyStart--;
        }

        return (string) (($codePoint - $familyStart) % 10);
    }

    private static function isDisplaySeparator(string $character): bool
    {
        if (preg_match(self::SEPARATOR_CATEGORY, $character) === 1) {
            return true;
        }

        if (in_array($character, self::LITERAL_SEPARATORS, true)) {
            return true;
        }

        return in_array(mb_ord($character, 'UTF-8'), self::WHITESPACE_CONTROLS, true);
    }

    /**
     * Compose to NFC, never NFKC.
     *
     * NFKC folds the fullwidth digits and the superscripts to ASCII by a second,
     * different rule, so "what is folded" would have two answers, and it rewrites Arabic
     * presentation forms and ligatures — the letter folding this contract refuses.
     *
     * A value `Normalizer::normalize()` cannot compose is returned unchanged, because
     * this function is total. That case is reachable only for invalid UTF-8, which the
     * fold already passes through.
     */
    private static function composeNfc(string $value): string
    {
        $composed = \Normalizer::normalize($value, \Normalizer::FORM_C);

        return is_string($composed) ? $composed : $value;
    }
}
