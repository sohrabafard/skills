---
name: alaa-crockford-base32-codecs
description: "Cross-runtime lowercase Crockford Base32 and UUIDv7 codec bundle for PHP, JavaScript, shell, and HAProxy Lua. Use when a task needs one shared pure codec for raw bytes, signed integers, UTF-8 strings, or UUIDv7 values across backend, frontend, CLI, and edge layers."
---

# Alaa Crockford Base32 Codecs

Use this skill when a task needs one shared lowercase Crockford Base32 codec contract across multiple runtimes.

This skill owns reusable pure codec helpers for PHP, JavaScript, shell, and HAProxy Lua. Keep this top-level file small and load the reference files only as needed.

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read `references/00-topic-map.md`.
3. Read `references/10-shared-codec-contract.md`.
4. Load the companion skill that owns the runtime or product boundary where the codec will be applied.
5. Copy or adapt only the asset files needed by the target repository.

## When to use

- shared lowercase Crockford Base32 encoding or decoding is required across PHP, JavaScript, shell, or HAProxy Lua
- one codec contract must stay identical across backend, frontend, CLI, and edge layers
- the task needs independent encode/decode pairs for raw bytes, signed integers, UTF-8 strings, or UUIDv7 values
- request IDs or correlation values need a lowercase human-safe Base32 form without wrapper metadata
- a repository needs copy-ready helpers instead of re-deriving Crockford Base32 or UUIDv7 behavior locally

## When NOT to use

- do not use this skill as a replacement for Ala service-contract policy, frontend architecture policy, or HAProxy operational guidance
- do not add transport or token wrapper metadata when a pure codec is enough
- do not use the Lua UUIDv7 helper for secrets or key material; it is intended for IDs and correlation values

## Companion routing

- `$alaa-php-clean-code`
  - Pair when adapting the PHP helper into a Laravel or PHP repository.
- `$alaa-frontend-developer`
  - Pair when frontend JavaScript must match the same codec contract as backend, shell, or edge code.
- `$alaa-haproxy`
  - Pair when HAProxy Lua wiring, config validation, or runtime constraints matter.
- `$alaa-services-contract`
  - Pair when these helpers are being applied as part of an Ala backend service contract task.
- `$alaa-docs-farsi`
  - Pair when README, contract docs, or usage examples need to be updated.

## Reference navigation

- topic routing and helper ownership:
  - `references/00-topic-map.md`
- shared codec contract, integer strategy, runtime notes, and bundled asset paths:
  - `references/10-shared-codec-contract.md`
- official-first source map and freshness triggers:
  - `references/90-source-map.md`

## Bundled assets

- PHP class:
  - `assets/crockford-base32/CrockfordBase32Codec.php`
- JavaScript class:
  - `assets/crockford-base32/crockford-base32-codec.mjs`
- Bash CLI helper:
  - `scripts/crockford-base32-cli.sh`
- HAProxy Lua helper:
  - `assets/haproxy/crockford-base32-codec.lua`

## Maintenance rules

- Keep this file routing-first and plain.
- Keep the shared codec contract and runtime details in `references/10-shared-codec-contract.md`.
- Keep the helper assets behavior-aligned across runtimes unless the codec contract is intentionally revised.
- When the codec contract changes, update all four runtime assets in the same effort.
