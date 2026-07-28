/*
 * Canonical Alaa permission-bitmap decoder for TypeScript.
 *
 * Source of truth: the skill `alaa-permission-generator`, file
 * `assets/permission-bitmap/permission-bitmap.ts`. A service or SDK package copies this
 * file beside its generated `permission-catalog.ts` and edits nothing in it, because a
 * decoder edited per consumer is a bug fixed in one consumer and still live in the rest.
 *
 * A defect found here is fixed here and re-propagated to every consumer. After any change
 * to this file, run `scripts/bitmap-conformance.sh` in the skill and record its output; the
 * corpus at `scripts/permission-bitmap-corpus.json` is what every language must agree on,
 * and a change proved in one runtime is not proved in the others.
 *
 * The wire contract this file implements, stated once:
 *   - permission ids are 1-based, and `bit_index = bitmap_id - 1`
 *   - bits are packed least-significant-bit first within each byte, so id 1 is bit 0 of
 *     byte 0, id 8 is bit 7 of byte 0, and id 9 is bit 0 of byte 1
 *   - `permission_id = byte_index * 8 + bit_index + 1`
 *   - the bitmap travels as raw bytes in unpadded base64url
 *
 * Base64url decoding is written out here rather than delegated to `atob` or `Buffer`,
 * because the three canonical implementations must reject the same inputs, the platform
 * decoders of Go, PHP, and JavaScript do not agree on whether the unused trailing bits of
 * the final character must be zero, and `Buffer` does not exist in a browser. This file
 * requires those bits to be zero in every language, so a bitmap accepted by one consumer is
 * accepted by all of them.
 *
 * This file uses erasable syntax only, so it runs under a type-stripping runtime as well as
 * under a compiler.
 */

/**
 * Bounds decode work when a caller supplies no cap of its own. This is a fallback bound,
 * not the contract value: the cap a service enforces at its trusted-context boundary is
 * owned by `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`,
 * and a caller that has that value passes it explicitly. This constant is deliberately not
 * derived from any catalog scale, so it never needs to move when the catalog grows.
 */
export const DEFAULT_MAX_ENCODED_BITMAP_LENGTH = 1024;

/**
 * The decode error taxonomy. These codes and their precedence are part of the shared
 * contract: every canonical implementation reports the same one for the same input, and the
 * conformance corpus pins that. Precedence is empty, then invalid bound, then over-length,
 * then malformed encoding, then no known permissions.
 */
export type PermissionBitmapErrorCode =
  | "empty_bitmap"
  | "invalid_bitmap"
  | "bitmap_too_long"
  | "no_known_permissions"
  | "invalid_decode_bound";

/** A decode failure carrying a stable machine-readable code from the taxonomy above. */
export class PermissionBitmapError extends Error {
  readonly errorCode: PermissionBitmapErrorCode;

  constructor(errorCode: PermissionBitmapErrorCode, message: string) {
    super(message);
    this.name = "PermissionBitmapError";
    this.errorCode = errorCode;
  }
}

const BASE64URL_ALPHABET =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

/**
 * Unpacks an encoded bitmap into the permission ids it sets, in ascending order.
 *
 * A set bit whose id exceeds `maxPermissionId` is dropped and is not an error, so a token
 * issued against a newer catalog degrades to fewer permissions rather than failing. That is
 * also why a bitmap wider than this consumer's own map decodes rather than failing.
 */
export function decodePermissionIds(
  access: string,
  maxPermissionId: number,
  maxEncodedLength: number = DEFAULT_MAX_ENCODED_BITMAP_LENGTH,
): number[] {
  if (access === "") {
    throw new PermissionBitmapError("empty_bitmap", "Access bitmap is empty.");
  }

  if (maxPermissionId < 1 || maxEncodedLength < 1) {
    throw new PermissionBitmapError(
      "invalid_decode_bound",
      "Permission decode bound is not positive.",
    );
  }

  if (access.length > maxEncodedLength) {
    throw new PermissionBitmapError(
      "bitmap_too_long",
      "Access bitmap exceeds the permitted encoded length.",
    );
  }

  const raw = decodeUnpaddedBase64Url(access);
  const ids: number[] = [];

  for (let byteIndex = 0; byteIndex < raw.length; byteIndex += 1) {
    const byte = raw[byteIndex];

    if (byte === 0) {
      continue;
    }

    for (let bit = 0; bit < 8; bit += 1) {
      const id = byteIndex * 8 + bit + 1;

      if (id > maxPermissionId) {
        return ids;
      }

      if ((byte & (1 << bit)) !== 0) {
        ids.push(id);
      }
    }
  }

  return ids;
}

/**
 * Resolves an encoded bitmap to the permission names this consumer knows, as a set keyed by
 * name so a check is a single hash lookup rather than a scan.
 *
 * It fails closed when zero known permissions resolve, which is the server-side rule. A
 * browser client deriving unverified UI hints calls `decodeUnverifiedUiPermissions`
 * instead, where an empty set is a legitimate ready state.
 */
export function decodePermissionSet(
  access: string,
  namesById: Readonly<Record<number, string>>,
  maxPermissionId: number,
  maxEncodedLength: number = DEFAULT_MAX_ENCODED_BITMAP_LENGTH,
): ReadonlySet<string> {
  const set = new Set<string>();

  for (const id of decodePermissionIds(access, maxPermissionId, maxEncodedLength)) {
    const name = (namesById[id] ?? "").trim();

    if (name === "") {
      continue;
    }

    set.add(name);
  }

  if (set.size === 0) {
    throw new PermissionBitmapError(
      "no_known_permissions",
      "Access bitmap contains no known permissions.",
    );
  }

  return set;
}

/**
 * Answers the single question most call sites ask, and fails closed on every decode error.
 * Use it only where the per-token decoded set is genuinely unavailable; a consumer decodes
 * once per token change, never per component render.
 */
export function hasPermission(
  access: string,
  permissionName: string,
  namesById: Readonly<Record<number, string>>,
  maxPermissionId: number,
  maxEncodedLength: number = DEFAULT_MAX_ENCODED_BITMAP_LENGTH,
): boolean {
  try {
    return decodePermissionSet(access, namesById, maxPermissionId, maxEncodedLength).has(
      permissionName.trim(),
    );
  } catch {
    return false;
  }
}

/**
 * Derives unverified UI capability hints in a browser. It grants nothing on malformed input
 * and throws nothing, and an empty set is a legitimate ready state that must never
 * invalidate the session or log the user out.
 *
 * This is not an authorization decision. The gateway and the owning service stay
 * authoritative, and a deny response is the only authoritative answer. An SDK's
 * `decodeUnverifiedUiAuthorization(token)` extracts the `prm` claim from the client's own
 * token and delegates the bit work here.
 */
export function decodeUnverifiedUiPermissions(
  access: string | null | undefined,
  namesById: Readonly<Record<number, string>>,
  maxPermissionId: number,
  maxEncodedLength: number = DEFAULT_MAX_ENCODED_BITMAP_LENGTH,
): ReadonlySet<string> {
  if (typeof access !== "string" || access === "") {
    return new Set<string>();
  }

  try {
    return decodePermissionSet(access, namesById, maxPermissionId, maxEncodedLength);
  } catch {
    return new Set<string>();
  }
}

/**
 * Returns the highest id present in the supplied map. This is per-artifact rather than
 * per-catalog, so it is the decode bound for this consumer only: an id above it is outside
 * this consumer's decode bound even when auth issues it.
 */
export function maxPermissionIdIn(
  namesById: Readonly<Record<number, string>>,
): number {
  let highest = 0;

  for (const key of Object.keys(namesById)) {
    const id = Number(key);

    if (id > highest) {
      highest = id;
    }
  }

  return highest;
}

/**
 * Decodes strict unpadded base64url into raw bytes.
 *
 * It rejects any character outside the unpadded base64url alphabet, which rejects padded
 * input because `=` is outside that alphabet; it rejects a length congruent to 1 modulo 4,
 * which no base64 encoding produces; and it rejects a final character whose unused
 * low-order bits are not zero, so one encoded form maps to one byte string.
 */
function decodeUnpaddedBase64Url(encoded: string): Uint8Array {
  if (encoded.length % 4 === 1) {
    throw new PermissionBitmapError(
      "invalid_bitmap",
      "Access bitmap is not strict unpadded base64url.",
    );
  }

  const out = new Uint8Array(Math.floor((encoded.length * 6) / 8));
  let written = 0;
  let accumulator = 0;
  let bits = 0;

  for (let index = 0; index < encoded.length; index += 1) {
    const value = BASE64URL_ALPHABET.indexOf(encoded[index]);

    if (value < 0) {
      throw new PermissionBitmapError(
        "invalid_bitmap",
        "Access bitmap is not strict unpadded base64url.",
      );
    }

    accumulator = (accumulator << 6) | value;
    bits += 6;

    if (bits >= 8) {
      bits -= 8;
      out[written] = (accumulator >> bits) & 0xff;
      written += 1;
      accumulator &= (1 << bits) - 1;
    }
  }

  if (bits > 0 && accumulator !== 0) {
    throw new PermissionBitmapError(
      "invalid_bitmap",
      "Access bitmap is not strict unpadded base64url.",
    );
  }

  return out.subarray(0, written);
}
