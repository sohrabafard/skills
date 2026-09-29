# The `shaka.util.Error` taxonomy and the complete code list

All rows `verified` at v5.2.3, read 2026-07-28, from `lib/util/error.js` (1,287 lines) and
`docs/tutorials/errors.md`. **155 codes exist at v5.2.3.**

Retry shape, backoff, ceilings and degradation are doctrine owned by `/alaa-reliability-sla`. This file owns which Shaka mechanism handles which category and what each
code means.

## Structure

When interpreting a Shaka error instance, read [Structure and categories](./70-error-taxonomy-and-codes/10-structure-and-categories.md) for fields, severity, category handling, and recoverability limits.

## Categories and the mechanism that handles each

When interpreting a Shaka error instance, read [Structure and categories](./70-error-taxonomy-and-codes/10-structure-and-categories.md) for fields, severity, category handling, and recoverability limits.

## The complete code list

When mapping a Shaka code, read the [Complete code catalog](./70-error-taxonomy-and-codes/20-complete-code-catalog.md) for the verified v5.2.3 values and historical 4058 caveat.

## Reading `error.data`

When handling errors or inspecting their data, read [Error data and handling paths](./70-error-taxonomy-and-codes/30-error-data-and-handling-paths.md) for safe fields and all event/callback/promise paths.

## The four error paths — you need all of them

When handling errors or inspecting their data, read [Error data and handling paths](./70-error-taxonomy-and-codes/30-error-data-and-handling-paths.md) for safe fields and all event/callback/promise paths.

## Mapping a code to a user-facing message

When presenting an error to a user, read [User-facing mapping](./70-error-taxonomy-and-codes/40-user-facing-mapping.md) for code-based mapping and its default requirement.
