<?php

declare(strict_types=1);

/*
 * Canonical Alaa permission-bitmap decoder for PHP.
 *
 * Source of truth: the skill `alaa-permission-generator`, file
 * `assets/permission-bitmap/PermissionBitmap.php`. A service copies this file and
 * `PermissionBitmapException.php` into the namespace that holds its generated
 * `config/permissions.php` reader, and changes exactly one thing: the namespace, so it
 * matches the target directory under PSR-4. Nothing else in this file is edited locally,
 * because a decoder edited per service is a bug fixed in one service and still live in the
 * rest.
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
 * Base64url decoding is written out here rather than delegated to `base64_decode`, because
 * the three canonical implementations must reject the same inputs and the platform decoders
 * of Go, PHP, and JavaScript do not agree on whether the unused trailing bits of the final
 * character must be zero. This file requires them to be zero in every language, so a bitmap
 * accepted by one service is accepted by all of them.
 */

namespace Alaa\Support\Authorization;

/**
 * Decodes the trusted access bitmap into the permission names this service knows.
 */
final class PermissionBitmap
{
    /**
     * Bounds decode work when a caller supplies no cap of its own. This is a fallback bound,
     * not the contract value: the cap a service enforces at its trusted-context boundary is
     * owned by `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`,
     * and a service that has that value passes it explicitly. This constant is deliberately
     * not derived from any catalog scale, so it never needs to move when the catalog grows.
     */
    public const DEFAULT_MAX_ENCODED_LENGTH = 1024;

    /**
     * The decode error taxonomy. These codes and their precedence are part of the shared
     * contract: every canonical implementation reports the same one for the same input, and
     * the conformance corpus pins that. Precedence is empty, then invalid bound, then
     * over-length, then malformed encoding, then no known permissions.
     */
    public const ERROR_EMPTY = 'empty_bitmap';

    public const ERROR_INVALID = 'invalid_bitmap';

    public const ERROR_TOO_LONG = 'bitmap_too_long';

    public const ERROR_NO_KNOWN = 'no_known_permissions';

    public const ERROR_INVALID_BOUND = 'invalid_decode_bound';

    private const BASE64URL_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';

    /**
     * Unpacks an encoded bitmap into the permission ids it sets, in ascending order.
     *
     * A set bit whose id exceeds $maxPermissionId is dropped and is not an error, so a token
     * issued against a newer catalog degrades to fewer permissions rather than failing. That
     * is also why a bitmap wider than this service's own map decodes rather than failing.
     *
     * @return list<int>
     *
     * @throws PermissionBitmapException
     */
    public static function decodeIds(
        string $access,
        int $maxPermissionId,
        int $maxEncodedLength = self::DEFAULT_MAX_ENCODED_LENGTH,
    ): array {
        if ($access === '') {
            throw PermissionBitmapException::emptyBitmap();
        }

        if ($maxPermissionId < 1 || $maxEncodedLength < 1) {
            throw PermissionBitmapException::invalidDecodeBound();
        }

        if (strlen($access) > $maxEncodedLength) {
            throw PermissionBitmapException::bitmapTooLong();
        }

        $raw = self::decodeUnpaddedBase64Url($access);

        $ids = [];

        foreach ($raw as $byteIndex => $byte) {
            if ($byte === 0) {
                continue;
            }

            for ($bit = 0; $bit < 8; $bit++) {
                $id = $byteIndex * 8 + $bit + 1;

                if ($id > $maxPermissionId) {
                    return $ids;
                }

                if (($byte & (1 << $bit)) !== 0) {
                    $ids[] = $id;
                }
            }
        }

        return $ids;
    }

    /**
     * Resolves an encoded bitmap to the permission names this service knows, as a set keyed
     * by name so a check is a single hash lookup rather than a scan.
     *
     * It fails closed when zero known permissions resolve, which is the server-side rule. A
     * browser client deriving unverified UI hints uses the TypeScript implementation's hint
     * entry point instead, where an empty set is a legitimate ready state.
     *
     * Call this once per request, at the trusted-context boundary, and store the result on
     * the trusted-context object every later check reads. Never memoize the result anywhere
     * whose lifetime outlives the request.
     *
     * @param  array<int, string>  $namesById
     * @return array<string, true>
     *
     * @throws PermissionBitmapException
     */
    public static function decodeSet(
        string $access,
        array $namesById,
        int $maxPermissionId,
        int $maxEncodedLength = self::DEFAULT_MAX_ENCODED_LENGTH,
    ): array {
        $set = [];

        foreach (self::decodeIds($access, $maxPermissionId, $maxEncodedLength) as $id) {
            $name = trim($namesById[$id] ?? '');

            if ($name === '') {
                continue;
            }

            $set[$name] = true;
        }

        if ($set === []) {
            throw PermissionBitmapException::noKnownPermissions();
        }

        return $set;
    }

    /**
     * Reports whether a decoded set grants the named permission.
     *
     * @param  array<string, true>  $set
     */
    public static function isGranted(array $set, string $permissionName): bool
    {
        return isset($set[trim($permissionName)]);
    }

    /**
     * Answers the single question most call sites ask, and fails closed on every decode
     * error. Use it only where the per-request decoded set is genuinely unavailable; the
     * request path decodes once and reads the stored set.
     *
     * @param  array<int, string>  $namesById
     */
    public static function hasPermission(
        string $access,
        string $permissionName,
        array $namesById,
        int $maxPermissionId,
        int $maxEncodedLength = self::DEFAULT_MAX_ENCODED_LENGTH,
    ): bool {
        try {
            $set = self::decodeSet($access, $namesById, $maxPermissionId, $maxEncodedLength);
        } catch (PermissionBitmapException) {
            return false;
        }

        return self::isGranted($set, $permissionName);
    }

    /**
     * Converts the generated `config/permissions.php` array into the id-to-name map the
     * decode entry points take. The generated config is keyed by permission name and each
     * block carries `id`, `name`, and `description`.
     *
     * @param  array<string, array{id: int, name: string, description?: string}>  $config
     * @return array<int, string>
     */
    public static function namesByIdFromConfig(array $config): array
    {
        $namesById = [];

        foreach ($config as $key => $block) {
            $namesById[$block['id']] = $block['name'] ?? (string) $key;
        }

        return $namesById;
    }

    /**
     * Returns the highest id present in the generated config. This is per-file rather than
     * per-catalog, so it is the decode bound for this service only: an id above it is
     * outside this service's decode bound even when auth issues it.
     *
     * @param  array<string, array{id: int, name: string, description?: string}>  $config
     */
    public static function maxPermissionIdFromConfig(array $config): int
    {
        $highest = 0;

        foreach ($config as $block) {
            if ($block['id'] > $highest) {
                $highest = $block['id'];
            }
        }

        return $highest;
    }

    /**
     * Decodes strict unpadded base64url into raw byte values.
     *
     * It rejects any character outside the unpadded base64url alphabet, which rejects padded
     * input because `=` is outside that alphabet; it rejects a length congruent to 1 modulo
     * 4, which no base64 encoding produces; and it rejects a final character whose unused
     * low-order bits are not zero, so one encoded form maps to one byte string.
     *
     * @return list<int>
     *
     * @throws PermissionBitmapException
     */
    private static function decodeUnpaddedBase64Url(string $encoded): array
    {
        if (strlen($encoded) % 4 === 1) {
            throw PermissionBitmapException::invalidBitmap();
        }

        $out = [];
        $accumulator = 0;
        $bits = 0;

        for ($index = 0, $length = strlen($encoded); $index < $length; $index++) {
            $value = strpos(self::BASE64URL_ALPHABET, $encoded[$index]);

            if ($value === false) {
                throw PermissionBitmapException::invalidBitmap();
            }

            $accumulator = $accumulator << 6 | $value;
            $bits += 6;

            if ($bits >= 8) {
                $bits -= 8;
                $out[] = $accumulator >> $bits & 0xFF;
                $accumulator &= (1 << $bits) - 1;
            }
        }

        if ($bits > 0 && $accumulator !== 0) {
            throw PermissionBitmapException::invalidBitmap();
        }

        return $out;
    }
}
