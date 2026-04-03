<?php

declare(strict_types=1);

namespace App\Support\Encoding;

use InvalidArgumentException;

/**
 * Shared lowercase Crockford Base32 helpers plus no-conflict typed tokens.
 *
 * Typed tokens use one lowercase Crockford prefix so mixed integer, string,
 * UUIDv7, and raw-byte values stay reversible without out-of-band type hints.
 */
final class CrockfordBase32TokenCodec
{
    private const ALPHABET = '0123456789abcdefghjkmnpqrstvwxyz';
    private const TYPE_BYTES = 'b';
    private const TYPE_INTEGER = 'n';
    private const TYPE_STRING = 's';
    private const TYPE_UUID_V7 = 'v';

    private function __construct()
    {
    }

    public static function encodeBytes(string $binary): string
    {
        if ($binary === '') {
            return '';
        }

        $buffer = 0;
        $bitCount = 0;
        $encoded = '';
        $length = strlen($binary);

        for ($index = 0; $index < $length; $index++) {
            $buffer = ($buffer << 8) | ord($binary[$index]);
            $bitCount += 8;

            while ($bitCount >= 5) {
                $bitCount -= 5;
                $encoded .= self::ALPHABET[($buffer >> $bitCount) & 31];
                $buffer &= (1 << $bitCount) - 1;
            }
        }

        if ($bitCount > 0) {
            $encoded .= self::ALPHABET[($buffer << (5 - $bitCount)) & 31];
        }

        return $encoded;
    }

    public static function decodeBytes(string $encoded): string
    {
        $normalized = self::normalizeEncoded($encoded);

        if ($normalized === '') {
            return '';
        }

        $buffer = 0;
        $bitCount = 0;
        $decoded = '';
        $length = strlen($normalized);

        for ($index = 0; $index < $length; $index++) {
            $value = strpos(self::ALPHABET, $normalized[$index]);

            if ($value === false) {
                throw new InvalidArgumentException(sprintf('Invalid Crockford Base32 character [%s].', $normalized[$index]));
            }

            $buffer = ($buffer << 5) | $value;
            $bitCount += 5;

            while ($bitCount >= 8) {
                $bitCount -= 8;
                $decoded .= chr(($buffer >> $bitCount) & 255);
                $buffer &= (1 << $bitCount) - 1;
            }
        }

        if ($bitCount > 0 && $buffer !== 0) {
            throw new InvalidArgumentException('Invalid Crockford Base32 payload padding bits.');
        }

        return $decoded;
    }

    public static function encodeBytesToken(string $binary): string
    {
        return self::TYPE_BYTES . self::encodeBytes($binary);
    }

    public static function decodeBytesToken(string $token): string
    {
        return self::decodeBytes(self::extractPayload($token, self::TYPE_BYTES));
    }

    public static function encodeInt(int $value): string
    {
        return self::TYPE_INTEGER . self::encodeBytes(self::packSignedInt64($value));
    }

    public static function decodeInt(string $token): int
    {
        $binary = self::decodeBytes(self::extractPayload($token, self::TYPE_INTEGER));

        if (strlen($binary) !== 8) {
            throw new InvalidArgumentException('Integer token payload must decode to exactly 8 bytes.');
        }

        return self::unpackSignedInt64($binary);
    }

    public static function encodeString(string $value): string
    {
        return self::TYPE_STRING . self::encodeBytes($value);
    }

    public static function decodeString(string $token): string
    {
        return self::decodeBytes(self::extractPayload($token, self::TYPE_STRING));
    }

    public static function generateUuidV7(): string
    {
        $bytes = random_bytes(16);
        $milliseconds = (int) floor(microtime(true) * 1000);

        for ($index = 5; $index >= 0; $index--) {
            $bytes[$index] = chr($milliseconds & 255);
            $milliseconds >>= 8;
        }

        $bytes[6] = chr((ord($bytes[6]) & 15) | 112);
        $bytes[8] = chr((ord($bytes[8]) & 63) | 128);

        return self::bytesToUuid($bytes);
    }

    public static function generateUuidV7Token(): string
    {
        return self::encodeUuidV7(self::generateUuidV7());
    }

    public static function encodeUuidV7(string $uuid): string
    {
        $bytes = self::uuidToBytes($uuid);
        self::assertUuidV7Bytes($bytes);

        return self::TYPE_UUID_V7 . self::encodeBytes($bytes);
    }

    public static function decodeUuidV7(string $token): string
    {
        $bytes = self::decodeBytes(self::extractPayload($token, self::TYPE_UUID_V7));

        if (strlen($bytes) !== 16) {
            throw new InvalidArgumentException('UUIDv7 token payload must decode to exactly 16 bytes.');
        }

        self::assertUuidV7Bytes($bytes);

        return self::bytesToUuid($bytes);
    }

    /**
     * @return array{type: 'bytes'|'int'|'string'|'uuidv7', value: string|int}
     */
    public static function decodeToken(string $token): array
    {
        $prefix = strtolower($token[0] ?? '');

        return match ($prefix) {
            self::TYPE_BYTES => ['type' => 'bytes', 'value' => self::decodeBytesToken($token)],
            self::TYPE_INTEGER => ['type' => 'int', 'value' => self::decodeInt($token)],
            self::TYPE_STRING => ['type' => 'string', 'value' => self::decodeString($token)],
            self::TYPE_UUID_V7 => ['type' => 'uuidv7', 'value' => self::decodeUuidV7($token)],
            default => throw new InvalidArgumentException(sprintf('Unsupported typed token prefix [%s].', $prefix)),
        };
    }

    private static function normalizeEncoded(string $encoded): string
    {
        $normalized = strtolower(str_replace('-', '', $encoded));

        return strtr($normalized, [
            'i' => '1',
            'l' => '1',
            'o' => '0',
        ]);
    }

    private static function extractPayload(string $token, string $expectedPrefix): string
    {
        if ($token === '') {
            throw new InvalidArgumentException('Typed token cannot be empty.');
        }

        $prefix = strtolower($token[0]);

        if ($prefix !== $expectedPrefix) {
            throw new InvalidArgumentException(sprintf('Expected token prefix [%s], got [%s].', $expectedPrefix, $prefix));
        }

        return substr($token, 1);
    }

    private static function packSignedInt64(int $value): string
    {
        return pack(
            'N2',
            ($value >> 32) & 0xFFFFFFFF,
            $value & 0xFFFFFFFF,
        );
    }

    private static function unpackSignedInt64(string $binary): int
    {
        $parts = unpack('Nhigh/Nlow', $binary);

        if ($parts === false) {
            throw new InvalidArgumentException('Unable to unpack the signed 64-bit payload.');
        }

        $high = (int) $parts['high'];
        $low = (int) $parts['low'];

        if ($high < 0x80000000) {
            return ($high << 32) | $low;
        }

        $complementHigh = (~$high) & 0xFFFFFFFF;
        $complementLow = (~$low) & 0xFFFFFFFF;
        $magnitude = ($complementHigh << 32) | $complementLow;

        return -($magnitude + 1);
    }

    private static function uuidToBytes(string $uuid): string
    {
        $normalized = strtolower($uuid);

        if (! preg_match('/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/', $normalized)) {
            throw new InvalidArgumentException('UUID must be in canonical 8-4-4-4-12 hexadecimal form.');
        }

        $hex = str_replace('-', '', $normalized);
        $bytes = hex2bin($hex);

        if ($bytes === false) {
            throw new InvalidArgumentException('Unable to decode UUID hex.');
        }

        return $bytes;
    }

    private static function bytesToUuid(string $bytes): string
    {
        $hex = bin2hex($bytes);

        return sprintf(
            '%s-%s-%s-%s-%s',
            substr($hex, 0, 8),
            substr($hex, 8, 4),
            substr($hex, 12, 4),
            substr($hex, 16, 4),
            substr($hex, 20, 12),
        );
    }

    private static function assertUuidV7Bytes(string $bytes): void
    {
        if ((ord($bytes[6]) >> 4) !== 7) {
            throw new InvalidArgumentException('UUID payload must be version 7.');
        }

        if ((ord($bytes[8]) & 0xC0) !== 0x80) {
            throw new InvalidArgumentException('UUID payload must use the RFC 4122 variant bits.');
        }
    }
}
