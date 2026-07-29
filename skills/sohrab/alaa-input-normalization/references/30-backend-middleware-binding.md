# The Backend Middleware Binding

**This is the contract.** Every backend service normalizes every request it accepts, in
middleware, before validation. Not per form request, not per controller, not per field, and
never on the assumption that a browser already did it.

Why the middleware and not the browser: `content` and `news` have no browser on their write
surface at all — those descriptions arrive from tooling and from the controlled-ops catalog
import — a second frontend ships a forked copy of the browser package that nothing binds,
and any HTTP client can post directly. A rule enforced only where a browser happens to run
is not enforced.

## Traversal, identical in every service

1. **Recurse** into nested objects and arrays. A flat pass over top-level keys cannot reach
   `contact.phone`, which is where the fleet's live phone defect lives.
2. **Values only, never keys.** Folding a key renames a field.
3. **Strings only.** Leave numbers, booleans and nulls untouched: a JSON number cannot carry
   a Persian digit.
4. **`text` mode for every string.** `typed` mode only for the fields a per-service list
   names, by name, in one place a reviewer can read.
5. **Before validation**, so `max:255`, `max:5000` and `digits:5` measure the folded value.
6. **The same sources every time**: JSON body, form body, and query string. State whether
   route parameters and headers are included and keep that answer the same across services;
   the fleet's default is that they are not, because a route parameter is matched against a
   pattern and a header is a protocol value.

## Laravel

Extend `Illuminate\Foundation\Http\Middleware\TransformsRequest`. It is the framework's own
recursive, global, value-only request transformer — `TrimStrings` is a subclass of it — so it
already walks nested arrays and JSON bodies and rewrites `$request->all()` in place, and
reusing it removes the traversal from the list of things that can differ between services.

```php
final class NormalizeRequestInput extends TransformsRequest
{
    /** @var list<string> the only fields that get typed mode, named here and nowhere else */
    protected array $typedFields = ['mobile', 'code', 'national_code'];

    protected function transform($key, $value)
    {
        if (! is_string($value)) {
            return $value;
        }

        return in_array($this->fieldName($key), $this->typedFields, true)
            ? InputNormalization::typed($value)
            : InputNormalization::text($value);
    }
}
```

Register it globally, before validation, and before `TrimStrings` where that exists:

| Repository | Registration point | Note |
| --- | --- | --- |
| `auth` | `bootstrap/app.php`, `withMiddleware` | Has the alias `convert` for `ModifyRequestInputMiddleware`, which is applied to no route and is dead code. Replace it; do not extend it. |
| `content`, `comment-service`, `notification`, `assessment-service` | `bootstrap/app.php`, `withMiddleware` | `assessment-service` has no `app/Http/Middleware/` directory yet. |
| `vod` | `bootstrap/app.php` | Same dead `convert` alias. |
| `ticket` | **`app/Http/Kernel.php`** | Laravel 10 shape; its `bootstrap/app.php` only binds the kernel. |

Declare the dependency the fold needs. `Normalizer` reaches this fleet only through
`symfony/polyfill-intl-normalizer`, which is present in every `composer.lock` transitively
and in no `composer.json` directly: **no image on the fleet installs `ext-intl`.** Add
`symfony/polyfill-intl-normalizer` to the consuming repository's `composer.json` as a direct
dependency, because a transitive dependency can be dropped by an unrelated upgrade and the
symptom would be a fatal error on the first request carrying a combining mark. Note also
that the polyfill's Unicode data may lag ICU, which is why the harness prints the version.

What the existing Laravel helpers do, and why they are not this: `CharacterCommon::convertToEnglish()`
folds two literal digit families and two HTML-entity forms and nothing else;
`CharacterCommon::normalizeFa()` rewrites Arabic letters, deletes hamza and tatweel, and
turns ZWNJ into a space — a search-key transformation applied to stored values. Neither is
this contract. `normalizeFa()` on name mutators is a name-matching decision that predates
this contract and stays out of its scope; do not extend it and do not call it from the new
middleware.

## Go, chi, and the kit

Put the implementation in `alaa-go-chi`, not in each service: `news` and `notif` have no
handlers yet and inherit whatever the kit ships, and `tusd` and the entitlement services
would otherwise each carry a copy.

Two seams, and they cover different traffic:

- **`httpkit`'s middleware chain** (`recover -> correlation -> otelSpan -> accessLogMetrics
  -> bodyGovernor -> next`) — attach immediately inside the body governor, which already
  caps the body at `MaxBodyBytes`, so the fold never reads an unbounded body. This is the
  seam that can also cover query strings and form posts.
- **`BindWith[T]`**, the single place every handler's JSON body is decoded — normalizing
  there is cheaper than re-buffering the body in a middleware, but it covers JSON bodies
  only.

Pick one per service and record which, because "both" means a value is folded twice — which
is harmless, the fold is idempotent — and "neither" is invisible. The Go implementation needs
`golang.org/x/text/unicode/norm`; the fleet already depends on it (`news/go.mod` carries
`v0.38.0`) and the standard library has no NFC.

## The gateway is out of scope, and this is the ruling rather than an omission

Do not attempt to normalize at the edge. Re-opening this costs the same investigation twice:

- Every registered HAProxy Lua action in the gateway is an `http-req` action reading and
  writing **headers and variables only**. There is no `http-buffer-request`, no filter, and
  no body access anywhere in the configuration.
- To rewrite a body HAProxy must buffer the whole request, bounded by `tune.bufsize`, which
  turns a streaming proxy into a store-and-forward one and breaks large uploads and the
  `tusd` path outright.
- HAProxy's Lua is 5.3/5.4 with **no Unicode support in the standard library**: no NFC and
  no category table. Reproducing an `Nd` fold there means shipping and maintaining a fifth
  generated table, which is the divergence the harness exists to prevent.
- The edge cannot see a form-encoded body's structure, a multipart body, or a compressed
  body without decompressing it.

What the gateway can do: nothing about normalization. What it must not do: fold headers it
forwards, because a trusted header is a protocol value and `/alaa-trust-gateway-auth`
(`$alaa-trust-gateway-auth`) owns it.

## Companions

- `/alaa-laravel-architecture` (`$alaa-laravel-architecture`): middleware ordering and where
  a global transformer belongs in a Laravel request lifecycle.
- `/alaa-go-chi-development` (`$alaa-go-chi-development`): `httpkit`, the Phase-0 chain, and
  how a kit change reaches the services.
- `/alaa-haproxy-lua` (`$alaa-haproxy-lua`): what the edge can and cannot execute.
- `/alaa-services-contract` (`$alaa-services-contract`): the field limits validation enforces
  after this runs.
