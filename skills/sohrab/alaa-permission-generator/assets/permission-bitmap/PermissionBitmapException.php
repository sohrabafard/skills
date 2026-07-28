<?php

declare(strict_types=1);

/*
 * Canonical Alaa permission-bitmap decode failure for PHP.
 *
 * Source of truth: the skill `alaa-permission-generator`, file
 * `assets/permission-bitmap/PermissionBitmapException.php`. A service copies this file
 * beside `PermissionBitmap.php` and changes exactly one thing: the namespace, so it matches
 * the target directory under PSR-4. Nothing else in this file is edited locally, because a
 * decoder edited per service is a bug fixed in one service and still live in the rest.
 */

namespace Alaa\Support\Authorization;

use RuntimeException;

/**
 * Carries a stable machine-readable error code from the shared decode taxonomy, so a caller
 * can branch on the failure without matching on message text.
 */
final class PermissionBitmapException extends RuntimeException
{
    private function __construct(
        public readonly string $errorCode,
        string $message,
    ) {
        parent::__construct($message);
    }

    public static function emptyBitmap(): self
    {
        return new self(PermissionBitmap::ERROR_EMPTY, 'Access bitmap is empty.');
    }

    public static function invalidBitmap(): self
    {
        return new self(
            PermissionBitmap::ERROR_INVALID,
            'Access bitmap is not strict unpadded base64url.',
        );
    }

    public static function bitmapTooLong(): self
    {
        return new self(
            PermissionBitmap::ERROR_TOO_LONG,
            'Access bitmap exceeds the permitted encoded length.',
        );
    }

    public static function noKnownPermissions(): self
    {
        return new self(
            PermissionBitmap::ERROR_NO_KNOWN,
            'Access bitmap contains no known permissions.',
        );
    }

    public static function invalidDecodeBound(): self
    {
        return new self(
            PermissionBitmap::ERROR_INVALID_BOUND,
            'Permission decode bound is not positive.',
        );
    }
}
