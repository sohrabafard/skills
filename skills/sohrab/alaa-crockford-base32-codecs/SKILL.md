---
name: alaa-crockford-base32-codecs
description: "Lowercase Crockford Base32 and UUIDv7 codec bundle shipping four byte-identical implementations for PHP, JavaScript, bash, and HAProxy Lua, plus a harness proving they still agree. Use when one shared pure codec must encode or decode raw bytes, unbounded signed integers, UTF-8 strings, or UUIDv7 values identically across backend, frontend, CLI, and edge layers, when a request ID or correlation value needs a lowercase human-safe Base32 form with no wrapper metadata, or when a repository would otherwise re-derive Crockford alias folding, padding-bit rules, or UUIDv7 layout locally. Do not use it for HAProxy configuration or Lua-at-the-edge engineering, which belong to alaa-haproxy-lua; for public identifier policy, which belongs to alaa-services-contract; for trusted-header policy, which belongs to alaa-trust-gateway-auth; or as a source of secrets or key material, for which none of these generators is cryptographically suitable."
---

# Alaa Crockford Base32 Codecs

Four implementations of one lowercase Crockford Base32 wire format, and the harness
that keeps them identical.

## Router

| You are about to | Read |
| --- | --- |
| encode or decode bytes, integers, strings, or UUIDv7 values, or look up an asset path, an exact error message, the integer grammar, or a randomness or clock source | `references/10-shared-codec-contract.md` |
| edit any implementation, the alphabet, the aliases, the padding-bit rule, or the UUIDv7 layout | that same contract, then run `scripts/codec-conformance.sh` |
| judge whether a UUIDv7, RFC 9562, runtime crypto, Lua, or HAProxy Lua claim is still current | `references/90-source-map.md` |

## Rules

- Change all four implementations in one effort, then run `scripts/codec-conformance.sh` and record its output, because a change proved in one runtime is not proved in the other three.
- Ship nothing while the harness reports a disagreement; the four files are one wire format and a partial fix splits it.
- Copy assets unchanged except for the PHP namespace, so the harness result still describes the copied code.
- Treat every non-zero exit from `scripts/crockford-base32-cli.sh` as a rejection and pass the failure on, because an empty or fallback substitute turns a rejected input into a wrong identifier downstream.
- Use these UUIDv7 generators for correlation identifiers only, never for secrets or key material, because not every path uses a cryptographic PRNG.

## When NOT to use

- The value must be unguessable: a secret, a token, a session identifier, a password reset code. None of
  these generators is cryptographically secure. Use a CSPRNG.
- The task is HAProxy configuration or Lua-at-the-edge engineering rather than the codec those layers
  share.
- The task is deciding which identifier a public surface exposes, or which headers a trust boundary
  accepts, rather than encoding bytes that decision already settled. The companion routing below names
  each owner.

## Companion routing

- `/alaa-haproxy-lua` (`$alaa-haproxy-lua`): Lua execution model, `lua-load` choice, edge error visibility.
- `/alaa-php-clean-code` (`$alaa-php-clean-code`): adapting the PHP class into a PHP repository.
- `/alaa-frontend-developer` (`$alaa-frontend-developer`): matching this contract in frontend JavaScript.
- `/alaa-services-contract` (`$alaa-services-contract`): public identifier policy and envelope shapes.
- `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`): trusted-header policy on a generated request ID.
- `/alaa-security-review` (`$alaa-security-review`): an identifier here becoming a trust or authorization input.
- `/alaa-testing-strategy` (`$alaa-testing-strategy`): what the harness proves and what it leaves unproved.
- `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md`: the bar these assets clear.
