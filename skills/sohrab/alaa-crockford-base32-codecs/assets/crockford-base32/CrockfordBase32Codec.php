<?php

declare(strict_types=1);

namespace App\Support\Encoding;

use InvalidArgumentException;

/**
 * Pure lowercase Crockford Base32 codecs for bytes, integers, strings, and UUIDv7 values.
 *
 * Wire format owner: skill `alaa-crockford-base32-codecs`,
 * `references/10-shared-codec-contract.md`. Change this file only together with the
 * JavaScript, shell, and HAProxy Lua implementations, then run
 * `scripts/codec-conformance.sh` from that skill.
 *
 * Integer strategy:
 * - positive integers encode as their minimal unsigned Crockford Base32 digits
 * - negative integers encode as `-` plus the minimal unsigned magnitude
 * - zero always encodes as `0`
 */
final class CrockfordBase32Codec
{
    private const ALPHABET = '0123456789abcdefghjkmnpqrstvwxyz';

    private function __construct()
    {
    }

    /**
     * Encode raw bytes as lowercase Crockford Base32 without padding.
     *
     * Pass raw binary, not hexadecimal text. Use `hex2bin()` first when the caller
     * holds a hex string.
     */
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

    /**
     * Decode lowercase or alias-normalized Crockford Base32 into raw bytes.
     */
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

    /**
     * Encode one signed integer as sign plus minimal unsigned Crockford Base32 digits.
     *
     * Pass magnitudes above PHP's native integer range as decimal strings so no
     * precision is lost before the codec sees the value.
     */
    public static function encodeInt(int|string $value): string
    {
        [$isNegative, $magnitude] = self::normalizeIntegerInput($value);
        $encoded = self::encodeUnsignedDecimalToBase32($magnitude);

        if (! $isNegative || $encoded === '0') {
            return $encoded;
        }

        return '-' . $encoded;
    }

    /**
     * Decode one signed Crockford Base32 integer into canonical base-10 text.
     */
    public static function decodeInt(string $encoded): string
    {
        [$isNegative, $magnitude] = self::splitSignedEncodedInteger($encoded);
        $decimal = self::decodeUnsignedBase32ToDecimal($magnitude);

        if (! $isNegative || $decimal === '0') {
            return $decimal;
        }

        return '-' . $decimal;
    }

    /**
     * Encode one UTF-8 string as lowercase Crockford Base32.
     */
    public static function encodeString(string $value): string
    {
        if (! self::isValidUtf8($value)) {
            throw new InvalidArgumentException('Text input is not valid UTF-8.');
        }

        return self::encodeBytes($value);
    }

    /**
     * Decode one Crockford Base32 payload back into a UTF-8 string.
     */
    public static function decodeString(string $encoded): string
    {
        $decoded = self::decodeBytes($encoded);

        if (! self::isValidUtf8($decoded)) {
            throw new InvalidArgumentException('Decoded payload is not valid UTF-8.');
        }

        return $decoded;
    }

    /**
     * Generate one canonical UUIDv7 string from `random_bytes` and the system clock.
     */
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

    /**
     * Encode one canonical UUIDv7 string as lowercase Crockford Base32.
     */
    public static function encodeUuidV7(string $uuid): string
    {
        $bytes = self::uuidToBytes($uuid);
        self::assertUuidV7Bytes($bytes);

        return self::encodeBytes($bytes);
    }

    /**
     * Decode one Crockford Base32 UUID payload back into canonical UUIDv7 text.
     */
    public static function decodeUuidV7(string $encoded): string
    {
        $bytes = self::decodeBytes($encoded);
        self::assertUuidV7Bytes($bytes);

        return self::bytesToUuid($bytes);
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

    /**
     * Validate UTF-8 per RFC 3629.
     *
     * Overlong forms, surrogate code points, and code points above U+10FFFF are
     * rejected so this helper matches `TextDecoder(fatal)` and Python `str` exactly.
     * The check is written without mbstring or PCRE UTF mode so a minimal PHP build
     * behaves identically.
     */
    private static function isValidUtf8(string $bytes): bool
    {
        $index = 0;
        $length = strlen($bytes);

        while ($index < $length) {
            $first = ord($bytes[$index]);

            if ($first < 0x80) {
                $following = 0;
                $lower = 0x80;
                $upper = 0xBF;
            } elseif ($first >= 0xC2 && $first <= 0xDF) {
                $following = 1;
                $lower = 0x80;
                $upper = 0xBF;
            } elseif ($first === 0xE0) {
                $following = 2;
                $lower = 0xA0;
                $upper = 0xBF;
            } elseif ($first >= 0xE1 && $first <= 0xEC) {
                $following = 2;
                $lower = 0x80;
                $upper = 0xBF;
            } elseif ($first === 0xED) {
                $following = 2;
                $lower = 0x80;
                $upper = 0x9F;
            } elseif ($first >= 0xEE && $first <= 0xEF) {
                $following = 2;
                $lower = 0x80;
                $upper = 0xBF;
            } elseif ($first === 0xF0) {
                $following = 3;
                $lower = 0x90;
                $upper = 0xBF;
            } elseif ($first >= 0xF1 && $first <= 0xF3) {
                $following = 3;
                $lower = 0x80;
                $upper = 0xBF;
            } elseif ($first === 0xF4) {
                $following = 3;
                $lower = 0x80;
                $upper = 0x8F;
            } else {
                return false;
            }

            if ($index + $following >= $length) {
                return false;
            }

            for ($offset = 1; $offset <= $following; $offset++) {
                $continuation = ord($bytes[$index + $offset]);
                $minimum = $offset === 1 ? $lower : 0x80;
                $maximum = $offset === 1 ? $upper : 0xBF;

                if ($continuation < $minimum || $continuation > $maximum) {
                    return false;
                }
            }

            $index += $following + 1;
        }

        return true;
    }

    /**
     * @return array{0: bool, 1: string}
     */
    private static function normalizeIntegerInput(int|string $value): array
    {
        $text = (string) $value;

        // `\A` and `\z` anchor the whole subject. `$` would accept a trailing newline
        // and let that byte reach the decimal long division as an extra digit zero.
        if (preg_match('/\A-?[0-9]+\z/', $text) !== 1) {
            throw new InvalidArgumentException('Integer input must be a canonical base-10 integer.');
        }

        $isNegative = str_starts_with($text, '-');
        $magnitude = ltrim($isNegative ? substr($text, 1) : $text, '0');
        $magnitude = $magnitude === '' ? '0' : $magnitude;

        return [$isNegative && $magnitude !== '0', $magnitude];
    }

    /**
     * @return array{0: bool, 1: string}
     */
    private static function splitSignedEncodedInteger(string $encoded): array
    {
        if ($encoded === '') {
            throw new InvalidArgumentException('Integer payload cannot be empty.');
        }

        $isNegative = str_starts_with($encoded, '-');
        $magnitude = $isNegative ? substr($encoded, 1) : $encoded;
        $magnitude = self::normalizeEncoded($magnitude);

        if ($magnitude === '') {
            throw new InvalidArgumentException('Integer payload cannot be empty.');
        }

        if (strlen($magnitude) > 1 && $magnitude[0] === '0') {
            throw new InvalidArgumentException('Integer payload must use a minimal Crockford Base32 representation.');
        }

        return [$isNegative, $magnitude];
    }

    private static function encodeUnsignedDecimalToBase32(string $decimal): string
    {
        if ($decimal === '0') {
            return '0';
        }

        $digits = [];
        $value = $decimal;

        while ($value !== '0') {
            [$value, $remainder] = self::divideDecimalStringByInt($value, 32);
            $digits[] = self::ALPHABET[$remainder];
        }

        return strrev(implode('', $digits));
    }

    private static function decodeUnsignedBase32ToDecimal(string $encoded): string
    {
        $decimal = '0';
        $length = strlen($encoded);

        for ($index = 0; $index < $length; $index++) {
            $value = strpos(self::ALPHABET, $encoded[$index]);

            if ($value === false) {
                throw new InvalidArgumentException(sprintf('Invalid Crockford Base32 integer character [%s].', $encoded[$index]));
            }

            $decimal = self::multiplyDecimalStringByIntAndAdd($decimal, 32, $value);
        }

        return $decimal;
    }

    /**
     * @return array{0: string, 1: int}
     */
    private static function divideDecimalStringByInt(string $decimal, int $divisor): array
    {
        $carry = 0;
        $quotient = '';
        $length = strlen($decimal);

        for ($index = 0; $index < $length; $index++) {
            $carry = ($carry * 10) + (int) $decimal[$index];
            $digit = intdiv($carry, $divisor);

            if ($quotient !== '' || $digit !== 0) {
                $quotient .= (string) $digit;
            }

            $carry %= $divisor;
        }

        return [$quotient === '' ? '0' : $quotient, $carry];
    }

    private static function multiplyDecimalStringByIntAndAdd(string $decimal, int $multiplier, int $addend): string
    {
        $carry = $addend;
        $digits = [];

        for ($index = strlen($decimal) - 1; $index >= 0; $index--) {
            $value = ((int) $decimal[$index] * $multiplier) + $carry;
            $digits[] = (string) ($value % 10);
            $carry = intdiv($value, 10);
        }

        while ($carry > 0) {
            $digits[] = (string) ($carry % 10);
            $carry = intdiv($carry, 10);
        }

        return strrev(implode('', $digits));
    }

    private static function uuidToBytes(string $uuid): string
    {
        $normalized = strtolower($uuid);

        if (preg_match('/\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\z/', $normalized) !== 1) {
            throw new InvalidArgumentException('UUID must be in canonical 8-4-4-4-12 hexadecimal form.');
        }

        $hex = str_replace('-', '', $normalized);
        $bytes = hex2bin($hex);

        if ($bytes === false) {
            throw new InvalidArgumentException('UUID must be in canonical 8-4-4-4-12 hexadecimal form.');
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
        if (strlen($bytes) !== 16) {
            throw new InvalidArgumentException('UUID payload must contain exactly 16 bytes.');
        }

        if ((ord($bytes[6]) >> 4) !== 7) {
            throw new InvalidArgumentException('UUID payload must be version 7.');
        }

        if ((ord($bytes[8]) & 0xC0) !== 0x80) {
            throw new InvalidArgumentException('UUID payload must use the RFC 4122 variant bits.');
        }
    }
}
