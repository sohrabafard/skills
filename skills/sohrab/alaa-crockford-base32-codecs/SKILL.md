---
name: alaa-crockford-base32-codecs
description: "Cross-runtime lowercase Crockford Base32, typed token, and UUIDv7 helper bundle for PHP, JavaScript, shell, and HAProxy Lua. Use when a task needs reversible no-conflict encoding or decoding for raw bytes, signed 64-bit integers, UTF-8 strings, request IDs, or UUIDv7 values, especially when the same token contract must be shared across backend, frontend, CLI, and edge layers."
---

# Alaa Crockford Base32 Codecs

Use this skill when a task needs one shared lowercase Crockford Base32 token contract across multiple runtimes.

This skill owns the reusable helper assets for PHP, JavaScript, shell, and HAProxy Lua. Keep the top-level file small and load the reference files only as needed.

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read `references/00-topic-map.md`.
3. Read `references/10-shared-token-contract.md`.
4. Load the companion skill that owns the runtime or product boundary where the helper will be applied.
5. Copy or adapt only the asset files needed by the target repository.

## When to use

- shared lowercase Crockford Base32 encoding or decoding is required across PHP, JavaScript, shell, or HAProxy Lua
- one token contract must stay identical across backend, frontend, CLI, and edge layers
- the task needs reversible no-conflict typed tokens for raw bytes, signed 64-bit integers, UTF-8 strings, or UUIDv7 values
- request IDs or correlation values need a lowercase human-safe token form
- a repository needs copy-ready helpers instead of re-deriving Crockford Base32 or UUIDv7 behavior locally

## When NOT to use

- do not use this skill as a replacement for Ala service-contract policy, frontend architecture policy, or HAProxy operational guidance
- do not create a local token variant when the shared contract in this skill already fits the task
- do not use the Lua UUIDv7 helper for secrets or key material; it is intended for IDs and correlation values

## Companion routing

- `$alaa-php-clean-code`
  - Pair when adapting the PHP helper into a Laravel or PHP repository.
- `$alaa-frontend-developer`
  - Pair when frontend JavaScript must match the same token contract as backend, shell, or edge code.
- `$alaa-haproxy`
  - Pair when HAProxy Lua wiring, config validation, or runtime constraints matter.
- `$alaa-services-contract`
  - Pair when these helpers are being applied as part of an Ala backend service contract task.
- `$alaa-docs-farsi`
  - Pair when README, contract docs, or usage examples need to be updated.

## Reference navigation

- topic routing and helper ownership:
  - `references/00-topic-map.md`
- shared token contract, runtime notes, and bundled asset paths:
  - `references/10-shared-token-contract.md`

## Bundled assets

- PHP class:
  - `assets/crockford-base32/CrockfordBase32TokenCodec.php`
- JavaScript class:
  - `assets/crockford-base32/crockford-base32-token-codec.mjs`
- Bash CLI helper:
  - `scripts/crockford-base32-cli.sh`
- HAProxy Lua helper:
  - `assets/haproxy/crockford-base32-token-codec.lua`

## Maintenance rules

- Keep this file routing-first and plain.
- Keep the typed token contract and runtime details in `references/10-shared-token-contract.md`.
- Keep the helper assets behavior-identical across runtimes unless the contract is intentionally revised.
- When the helper contract changes, update all four runtime assets in the same effort.
