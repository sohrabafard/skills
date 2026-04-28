<?php

declare(strict_types=1);

/**
 * Reference implementation extracted from comment-service.
 *
 * Purpose:
 * - encode permission ids into a compact base64url bitmap
 * - decode and test permission ids using the same bit ordering
 *
 * Contract:
 * - permission bitmap ids are 1-based
 * - auth bit_index values are zero-based and equal bitmap_id - 1
 * - bits are packed least-significant-bit first inside each byte
 * - the output uses unpadded base64url encoding
 * - invalid input decodes to an empty string or empty permission list
 *
 * Important:
 * - keep the permission-id map in generated, committed service config
 * - generate service config from alaa-permission-catalog; do not hand-maintain ids here
 * - do not assume every service shares the same permission ids or role rules
 * - the gateway projects verified prm as X-Access but does not own backend maps
 */
final class PermissionBitmap
{
    /** @param int[] $permissionIds */
    public static function encode(array $permissionIds, int $maxPermissionId): string
    {
        if ($maxPermissionId <= 0) {
            return '';
        }

        $byteCount = (int) ceil($maxPermissionId / 8);
        $bytes = array_fill(0, $byteCount, 0);

        foreach ($permissionIds as $id) {
            if ($id < 1 || $id > $maxPermissionId) {
                continue;
            }

            $index = $id - 1;
            $byteIndex = intdiv($index, 8);
            $bitIndex = $index % 8;
            $bytes[$byteIndex] |= 1 << $bitIndex;
        }

        $binary = pack('C*', ...$bytes);

        return self::base64UrlEncode($binary);
    }

    public static function has(string $bitmap, int $permissionId): bool
    {
        if ($permissionId < 1 || $bitmap === '') {
            return false;
        }

        $binary = self::base64UrlDecode($bitmap);
        if ($binary === '') {
            return false;
        }

        $index = $permissionId - 1;
        $byteIndex = intdiv($index, 8);

        if ($byteIndex >= strlen($binary)) {
            return false;
        }

        $byte = ord($binary[$byteIndex]);
        $bitIndex = $index % 8;

        return (bool) ($byte & (1 << $bitIndex));
    }

    public static function isValid(string $bitmap): bool
    {
        return self::base64UrlDecode($bitmap) !== '';
    }

    /** @return int[] */
    public static function decode(string $bitmap, ?int $maxPermissionId = null): array
    {
        if ($bitmap === '') {
            return [];
        }

        $binary = self::base64UrlDecode($bitmap);
        if ($binary === '') {
            return [];
        }

        if ($maxPermissionId === null || $maxPermissionId <= 0) {
            $maxPermissionId = strlen($binary) * 8;
        }

        $bytes = array_values(unpack('C*', $binary));
        $ids = [];
        foreach ($bytes as $byteIndex => $byte) {
            if ($byte === 0) {
                continue;
            }

            for ($bitIndex = 0; $bitIndex < 8; $bitIndex++) {
                if (!($byte & (1 << $bitIndex))) {
                    continue;
                }

                $id = ($byteIndex * 8) + $bitIndex + 1;
                if ($id > $maxPermissionId) {
                    break 2;
                }

                $ids[] = $id;
            }
        }

        return $ids;
    }

    private static function base64UrlEncode(string $data): string
    {
        return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
    }

    private static function base64UrlDecode(string $data): string
    {
        if ($data === '') {
            return '';
        }

        if (preg_match('/^[A-Za-z0-9\-_]+$/', $data) !== 1) {
            return '';
        }

        $data = strtr($data, '-_', '+/');
        $pad = strlen($data) % 4;
        if ($pad !== 0) {
            $data .= str_repeat('=', 4 - $pad);
        }

        $decoded = base64_decode($data, true);

        return is_string($decoded) ? $decoded : '';
    }
}
