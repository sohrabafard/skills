// Package inputnorm is the canonical Go implementation of the Alaa input-boundary
// normalization contract.
//
// Owner: the skill `alaa-input-normalization`. Copy this file into a repository unchanged
// except for the package clause, so that the result of
// `scripts/normalization-conformance.sh` still describes the copied code. Fix a defect
// here first and re-propagate it.
//
// Two modes, one pipeline:
//
//	text  = NFC(FoldDecimalDigits(value))            every string, including free text
//	typed = NFC(StripDisplaySeparators(text(value))) one field that holds one number
//
// Both modes are total and idempotent. Normalization never rejects and never returns an
// error: rejection is validation, and it runs after this.
//
// Requires golang.org/x/text/unicode/norm, which this fleet already depends on
// (news/go.mod carries v0.38.0). The standard library has no NFC.
package inputnorm

import (
	"strings"
	"unicode"
	"unicode/utf8"

	"golang.org/x/text/unicode/norm"
)

// Mode selects one of the two rules.
type Mode string

const (
	// ModeText is the global rule for any string field, including free text.
	ModeText Mode = "text"
	// ModeTyped is the rule for a field whose entire value is one number or one code.
	ModeTyped Mode = "typed"
)

// separatorCategories are the display-separator categories, owned by
// `alaa-bale-provider` and `alaa-sms-provider-mediana` and reproduced here for typed mode
// only. Match by category and never by a written-out list of characters: an enumeration
// is always one character short of the next change in a display layer.
var separatorCategories = []*unicode.RangeTable{
	unicode.Cf,
	unicode.Zs,
	unicode.Zl,
	unicode.Zp,
	unicode.Pd,
}

// whitespaceControls is exactly the intersection of Python's str.isspace() with general
// category Cc: the tab, the line feed, the vertical tab, the form feed, the carriage
// return, the four information separators and U+0085. It is written out because Cc also
// holds characters that are not separators, so the category alone is the wrong test, and
// because unicode.IsSpace covers a different set.
var whitespaceControls = map[rune]struct{}{
	0x09: {}, 0x0A: {}, 0x0B: {}, 0x0C: {}, 0x0D: {},
	0x1C: {}, 0x1D: {}, 0x1E: {}, 0x1F: {}, 0x85: {},
}

// literalSeparators stay written out because no Unicode category names them precisely
// enough: Ps and Pe hold every bracket pair in Unicode, and Po holds the comma and the
// semicolon, which separate two numbers rather than group the digits of one.
var literalSeparators = map[rune]struct{}{
	'(': {}, ')': {}, '.': {}, '_': {}, '/': {},
}

// isDecimalNumber reports whether r is in Unicode general category Nd.
//
// The category is named in the source rather than reached through unicode.IsDigit,
// because "digit" is the ambiguity this contract exists to remove: category Nd excludes
// category No, so the superscripts, the circled digits, the fractions and the Roman
// numerals are not digits here. Folding x² to x2 changes what the text says. Never widen
// this to unicode.IsNumber, which is category N and does reach No.
func isDecimalNumber(r rune) bool {
	return r >= 0 && r <= unicode.MaxRune && unicode.Is(unicode.Nd, r)
}

// asciiDigitFor returns the ASCII digit for one Nd code point, derived from the category
// table rather than read from a hand-written family list.
//
// The Unicode Standard requires the ten decimal digits of a script to be encoded
// contiguously and in ascending order from zero, so within a maximal run of adjacent Nd
// code points the value of a code point is its offset from the start of the run, modulo
// ten. Runs longer than ten exist — U+1D7CE-U+1D7FF is five mathematical digit families
// packed end to end — which is why the offset is taken modulo ten and not clamped.
func asciiDigitFor(r rune) rune {
	familyStart := r

	for familyStart > 0 && isDecimalNumber(familyStart-1) {
		familyStart--
	}

	return '0' + (r-familyStart)%10
}

func isDisplaySeparator(r rune) bool {
	if unicode.IsOneOf(separatorCategories, r) {
		return true
	}

	if _, found := whitespaceControls[r]; found {
		return true
	}

	_, found := literalSeparators[r]

	return found
}

// FoldDecimalDigits folds every Unicode decimal digit to its ASCII equivalent, one code
// point in and one code point out.
//
// A string that is not valid UTF-8 is not text, and this contract does not repair it: it
// is returned unchanged and validation rejects it. Ranging over invalid UTF-8 would yield
// U+FFFD for each bad byte and so would insert, and this contract never inserts.
func FoldDecimalDigits(value string) string {
	if !utf8.ValidString(value) {
		return value
	}

	var folded strings.Builder

	folded.Grow(len(value))

	for _, r := range value {
		if isDecimalNumber(r) {
			folded.WriteRune(asciiDigitFor(r))

			continue
		}

		folded.WriteRune(r)
	}

	return folded.String()
}

// StripDisplaySeparators removes every display separator. Used by typed mode only, never
// by text mode.
func StripDisplaySeparators(value string) string {
	if !utf8.ValidString(value) {
		return value
	}

	var kept strings.Builder

	kept.Grow(len(value))

	for _, r := range value {
		if !isDisplaySeparator(r) {
			kept.WriteRune(r)
		}
	}

	return kept.String()
}

// composeNFC composes to NFC, never NFKC.
//
// NFKC folds the fullwidth digits and the superscripts to ASCII by a second, different
// rule, so "what is folded" would have two answers, and it rewrites Arabic presentation
// forms and ligatures — the letter folding this contract refuses.
func composeNFC(value string) string {
	return norm.NFC.String(value)
}

// NormalizeText is the global rule for any string field, including free text.
func NormalizeText(value string) string {
	return composeNFC(FoldDecimalDigits(value))
}

// NormalizeTyped is the rule for a field whose entire value is one number or one code: a
// mobile number, an OTP, a national code, a postal code.
//
// NFC is applied a second time after separator removal because removing a format
// character can bring a base character and a combining mark together, and the output of
// this function is required to be in NFC.
func NormalizeTyped(value string) string {
	return composeNFC(StripDisplaySeparators(NormalizeText(value)))
}

// Normalize dispatches by mode, for a caller that carries the mode as data.
func Normalize(value string, mode Mode) string {
	if mode == ModeTyped {
		return NormalizeTyped(value)
	}

	return NormalizeText(value)
}

// HasNonASCIIDecimalDigits reports whether a string still carries a non-ASCII decimal
// digit.
//
// For diagnostics and tests only. Never use it to reject input: a value that fails this
// check has not been normalized yet, which is a defect in the caller rather than in the
// user's typing.
func HasNonASCIIDecimalDigits(value string) bool {
	for _, r := range value {
		if isDecimalNumber(r) && (r < '0' || r > '9') {
			return true
		}
	}

	return false
}
