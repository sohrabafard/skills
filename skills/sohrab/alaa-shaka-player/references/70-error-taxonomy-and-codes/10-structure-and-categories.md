For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## Structure

| Field | Type | Notes |
|---|---|---|
| `severity` | `shaka.util.Error.Severity` | `RECOVERABLE = 1`, `CRITICAL = 2` |
| `category` | `shaka.util.Error.Category` | see below |
| `code` | `shaka.util.Error.Code` | see the list |
| `data` | `Array<*>` | The constructor's rest args. **Per-code shape, undocumented in general.** |
| `handled` | boolean | Initialised `false`; set `true` in a failure callback to stop propagation. |
| `message` | string | Compiled: `'Shaka Error <code>'`. Debug/uncompiled: `'Shaka Error CATEGORY.CODE_NAME (data)'`. |

**The critical subtlety, stated verbatim in the source:**

> *"The `@extends {Error}` annotation below is a type-only declaration for the Closure Compiler; this
> class does **not** actually extend the native `Error` at runtime… In particular,
> `(new shaka.util.Error(...)) instanceof Error` is **`false`**. This is intentional: it lets
> application code tell an unhandled native error apart from a Shaka-specific error by checking
> `instanceof Error` before checking `instanceof shaka.util.Error`."*

So **check `instanceof Error` first**. A value that passes it is a Shaka crash, not a Shaka error.

Severity, verbatim:

- `RECOVERABLE`: *"An error occurred, but the Player is attempting to recover from the error. If the
  Player cannot ultimately recover, it still may not throw a CRITICAL error. For example, retrying for
  a media segment will never result in a CRITICAL error (the Player will just retry forever)."*
- `CRITICAL`: *"A critical error that the library cannot recover from. These usually cause the Player
  to stop loading or updating. **A new manifest must be loaded to reset the library.**"*


## Categories and the mechanism that handles each

| Name | Value | Which Shaka mechanism handles it |
|---|---|---|
| `NETWORK` | 1 | The retry domain: `retryParameters`, the cancelable `retry` event, `streaming.failureCallback`. |
| `TEXT` | 2 | Survivable when `streaming.ignoreTextStreamFailures = true`. |
| `MEDIA` | 3 | `VIDEO_ERROR` (3016) is recovered via `streaming.allowMediaSourceRecoveries`. |
| `MANIFEST` | 4 | Load-time. Mostly terminal for the load. |
| `STREAMING` | 5 | `streaming.failureCallback`. |
| `DRM` | 6 | `drm.failureCallback` + `retryLicensing()`. |
| `PLAYER` | 7 | Lifecycle. Mostly terminal. |
| `CAST` | 8 | Session-level. |
| `STORAGE` | 9 | Offline. Terminal for that operation. |
| `ADS` | 10 | Ads fail independently of content — preserve that with a watchdog (`55-…`). |

> **There is no upstream field or table marking a category "recoverable".** Recoverability is
> expressed **per error instance** via `error.severity`, and it is **mutable** — the default streaming
> failure callback literally assigns `error.severity = RECOVERABLE` before retrying. Any statement of
> the form "category X is recoverable" is an `inferred` claim, not a documented fact. `not documented`
> — searched `lib/util/error.js`, `docs/tutorials/errors.md`, `externs/shaka/error.js` on 2026-07-28;
> no recoverability table exists.
