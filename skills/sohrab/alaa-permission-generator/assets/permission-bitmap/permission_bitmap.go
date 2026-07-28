// Canonical Alaa permission-bitmap decoder for Go.
//
// Source of truth: the skill `alaa-permission-generator`, file
// `assets/permission-bitmap/permission_bitmap.go`. A service copies this file into the
// package that holds its generated `permissions_gen.go` and changes exactly one thing:
// the package clause, so it matches the target directory name. Nothing else in this file
// is edited locally, because a decoder edited per service is a bug fixed in one service
// and still live in the rest.
//
// A defect found here is fixed here and re-propagated to every consumer. After any change
// to this file, run `scripts/bitmap-conformance.sh` in the skill and record its output;
// the corpus at `scripts/permission-bitmap-corpus.json` is what every language must agree
// on, and a change proved in one runtime is not proved in the others.
//
// The wire contract this file implements, stated once:
//   - permission ids are 1-based, and `bit_index = bitmap_id - 1`
//   - bits are packed least-significant-bit first within each byte, so id 1 is bit 0 of
//     byte 0, id 8 is bit 7 of byte 0, and id 9 is bit 0 of byte 1
//   - `permission_id = byte_index*8 + bit_index + 1`
//   - the bitmap travels as raw bytes in unpadded base64url
//
// Base64url decoding is written out here rather than delegated to `encoding/base64`,
// because the three canonical implementations must reject the same inputs and the
// platform decoders of Go, PHP, and JavaScript do not agree on whether the unused
// trailing bits of the final character must be zero. This file requires them to be zero
// in every language, so a bitmap accepted by one service is accepted by all of them.
package authz

import (
	"errors"
	"sort"
	"strings"
)

// DefaultMaxEncodedBitmapLength bounds decode work when a caller supplies no cap of its
// own. It is a fallback bound, not the contract value: the cap a service enforces at its
// trusted-context boundary is owned by
// `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`, and a
// service that has that value passes it to the `WithLimits` entry points. This constant is
// deliberately not derived from any catalog scale, so it never needs to move when the
// catalog grows.
const DefaultMaxEncodedBitmapLength = 1024

// The decode error taxonomy. These four errors and their precedence are part of the shared
// contract: every canonical implementation returns the same one for the same input, and the
// conformance corpus pins that. Precedence is empty, then invalid bound, then over-length,
// then malformed encoding, then no known permissions.
var (
	ErrEmptyAccessBitmap   = errors.New("access bitmap is empty")
	ErrInvalidAccessBitmap = errors.New("access bitmap is not strict unpadded base64url")
	ErrAccessBitmapTooLong = errors.New("access bitmap exceeds the permitted encoded length")
	ErrNoKnownPermissions  = errors.New("access bitmap contains no known permissions")
	ErrInvalidDecodeBound  = errors.New("permission decode bound is not positive")
)

const base64URLAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

// PermissionMap is the generated id-to-name map a service holds. Its only legitimate
// source is the committed generated artifact.
type PermissionMap map[int]string

// Set is a decoded permission set keyed by permission name, so a check is a single hash
// lookup rather than a scan. Never compare by bitmap id in application code.
type Set map[string]struct{}

// Has reports whether the set grants the named permission.
func (s Set) Has(permission string) bool {
	_, ok := s[strings.TrimSpace(permission)]

	return ok
}

// Names returns the granted permission names in sorted order, for logging and tests.
func (s Set) Names() []string {
	names := make([]string, 0, len(s))
	for name := range s {
		names = append(names, name)
	}
	sort.Strings(names)

	return names
}

// DecodePermissionBitmap unpacks an encoded bitmap into the permission ids it sets, under
// the default encoded-length cap. It exists with this signature so the generated
// `Decode` compiles against it unchanged.
func DecodePermissionBitmap(access string, maxPermissionID int) ([]int, error) {
	return DecodePermissionBitmapWithLimits(access, maxPermissionID, DefaultMaxEncodedBitmapLength)
}

// DecodePermissionBitmapWithLimits unpacks an encoded bitmap into the permission ids it
// sets. Call this form from the trusted-context boundary with the contract-owned cap.
//
// A set bit whose id exceeds maxPermissionID is dropped and is not an error, so a token
// issued against a newer catalog degrades to fewer permissions rather than failing. That
// is also why a bitmap wider than this service's own map decodes rather than failing.
func DecodePermissionBitmapWithLimits(access string, maxPermissionID int, maxEncodedLength int) ([]int, error) {
	if access == "" {
		return nil, ErrEmptyAccessBitmap
	}
	if maxPermissionID < 1 || maxEncodedLength < 1 {
		return nil, ErrInvalidDecodeBound
	}
	if len(access) > maxEncodedLength {
		return nil, ErrAccessBitmapTooLong
	}

	raw, err := decodeUnpaddedBase64URL(access)
	if err != nil {
		return nil, err
	}

	ids := make([]int, 0)
	for byteIndex, b := range raw {
		if b == 0 {
			continue
		}
		for bit := 0; bit < 8; bit++ {
			id := byteIndex*8 + bit + 1
			if id > maxPermissionID {
				return ids, nil
			}
			if b&(1<<uint(bit)) != 0 {
				ids = append(ids, id)
			}
		}
	}

	return ids, nil
}

// DecodePermissionSet resolves an encoded bitmap to the permission names this service
// knows, under the default encoded-length cap. It carries exactly the signature the
// generated `Decode` calls, so the generated file compiles against this file unchanged.
//
// It fails closed when zero known permissions resolve, which is the server-side rule. A
// browser client deriving unverified UI hints uses the TypeScript implementation's
// hint entry point instead, where an empty set is a legitimate ready state.
func DecodePermissionSet(access string, permissions map[int]string, maxPermissionID int) (Set, error) {
	return DecodePermissionSetWithLimits(access, permissions, maxPermissionID, DefaultMaxEncodedBitmapLength)
}

// DecodePermissionSetWithLimits resolves an encoded bitmap to permission names under an
// explicit encoded-length cap. Call this form from the trusted-context boundary, once per
// request, and store the result on the trusted-context object every later check reads.
func DecodePermissionSetWithLimits(
	access string,
	permissions map[int]string,
	maxPermissionID int,
	maxEncodedLength int,
) (Set, error) {
	ids, err := DecodePermissionBitmapWithLimits(access, maxPermissionID, maxEncodedLength)
	if err != nil {
		return nil, err
	}

	set := make(Set)
	for _, id := range ids {
		name, ok := permissions[id]
		if !ok || strings.TrimSpace(name) == "" {
			continue
		}
		set[name] = struct{}{}
	}
	if len(set) == 0 {
		return nil, ErrNoKnownPermissions
	}

	return set, nil
}

// HasPermission answers the single question most call sites ask, and fails closed on every
// decode error. Use it only where the per-request decoded set is genuinely unavailable;
// the request path decodes once and reads the stored set.
func HasPermission(access string, permissionName string, permissions PermissionMap) bool {
	set, err := DecodePermissionSet(access, map[int]string(permissions), MaxPermissionIDIn(permissions))
	if err != nil {
		return false
	}

	return set.Has(permissionName)
}

// MaxPermissionIDIn returns the highest id present in the supplied map. The generated file
// supplies its own `MaxPermissionID()`, which is per-file rather than per-catalog; this
// helper exists for callers holding a map directly.
func MaxPermissionIDIn(permissions PermissionMap) int {
	highest := 0
	for id := range permissions {
		if id > highest {
			highest = id
		}
	}

	return highest
}

// decodeUnpaddedBase64URL decodes strict unpadded base64url into raw bytes.
//
// It rejects any character outside the unpadded base64url alphabet, which rejects padded
// input because `=` is outside that alphabet; it rejects a length congruent to 1 modulo 4,
// which no base64 encoding produces; and it rejects a final character whose unused
// low-order bits are not zero, so one encoded form maps to one byte string.
func decodeUnpaddedBase64URL(encoded string) ([]byte, error) {
	if len(encoded)%4 == 1 {
		return nil, ErrInvalidAccessBitmap
	}

	out := make([]byte, 0, len(encoded)*6/8)
	accumulator := 0
	bits := 0

	for _, symbol := range encoded {
		value := strings.IndexRune(base64URLAlphabet, symbol)
		if value < 0 {
			return nil, ErrInvalidAccessBitmap
		}

		accumulator = accumulator<<6 | value
		bits += 6

		if bits >= 8 {
			bits -= 8
			out = append(out, byte(accumulator>>uint(bits)))
			accumulator &= 1<<uint(bits) - 1
		}
	}

	if bits > 0 && accumulator != 0 {
		return nil, ErrInvalidAccessBitmap
	}

	return out, nil
}
