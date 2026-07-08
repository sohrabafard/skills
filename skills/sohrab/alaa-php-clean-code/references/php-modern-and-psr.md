# Modern PHP, type safety, and PSR / PER baseline

## Contents
- Type-safety defaults
- Modern PHP 8.x features
- PSR / PER standards
- Error handling
- Low-level performance
- Security-sensitive handoff

## Type-safety defaults
- Use `declare(strict_types=1);` in new PHP files unless the repo clearly avoids it.
- Type parameters, returns, and properties by default.
- Prefer dedicated DTOs or value objects over structured arrays when the shape matters.
- Use union or intersection types only when the contract genuinely allows multiple shapes.
- Keep public parameter names stable if named arguments are used by callers.
- Avoid `mixed` unless it is truly the honest type.
- Prefer `DateTimeImmutable` over mutable `DateTime` in new code.

### Anti-patterns
- Relying on scalar coercion to "fix" bad inputs.
- Passing untyped arrays or `stdClass` as domain data.
- Hiding important type assumptions in comments instead of the signature.
- Renaming public parameter names casually when named arguments may be used.

## Modern PHP 8.x features

### Safe defaults
- Constructor property promotion for clear dependencies and small immutable objects.
- `readonly` properties or classes when the object should not change after construction.
- Enums plus `match` for closed sets and explicit branching.
- Attributes when the framework or a clear local contract consumes them.
- `#[Override]` when the repo PHP version and tooling support it.
- Typed class constants when the repo targets a PHP version that supports them and the constant is part of a real contract.

### Use carefully
- Named arguments:
  - good for readability in local construction
  - risky across unstable public APIs because parameter names become part of the contract
- Union and intersection types:
  - useful when the domain genuinely accepts multiple shapes
  - harmful when they merely hide muddy responsibilities
- Readonly classes:
  - useful for immutable DTOs and value objects
  - still shallow immutability; object graphs inside can still mutate
- Property hooks and asymmetric visibility:
  - use only when the repo targets PHP 8.4+ and the benefit is obvious
  - avoid as a default in framework-heavy or magic-heavy code until toolchain support and team conventions are proven

### PHP 8.5 features (when the repo targets PHP 8.5+)
PHP 8.5 (released 2025-11) is the platform baseline for new Alaa Laravel 13 services. Adopt these deliberately:

- `array_first()` / `array_last()`:
  - safe default; replaces `reset()`/`end()` pointer tricks and `$arr[array_key_first($arr)]` noise
  - returns `null` for empty arrays — keep the null path explicit
- `clone($object, ['prop' => $value])` (clone-with):
  - safe default for `with*()` methods on `readonly` DTOs and value objects; removes hand-written wither boilerplate
  - respects visibility; keep withers as named methods so call sites stay intention-revealing
- `#[\NoDiscard]`:
  - put it on methods whose return value must be checked (result objects, immutable withers, `attempt()`-style APIs)
  - fits the platform rule that rate limiters and lock attempts must check their results
- Pipe operator `|>`:
  - use carefully; good for short, linear transform chains of named functions/first-class callables
  - don't rewrite readable Collection chains or simple nested calls just to look modern; one style per file
- New `Uri` extension:
  - prefer it over ad-hoc `parse_url()` handling when the repo starts using it consistently

Do / Don't:
- ✅ Do: `public function withStatus(CommentStatus $status): self { return clone($this, ['status' => $status]); }` on a `readonly` DTO — one line, immutability preserved.
- ❌ Don't: keep writing full constructor-copy withers on 8.5 repos, or mutate a `readonly`-less DTO in place because withers felt verbose — both re-open the immutability gap clone-with closed.
- ✅ Do: `#[\NoDiscard] public function attempt(): LockResult` so an ignored lock result becomes a warning.
- ❌ Don't: chain `|>` across closures with side effects or multi-branch logic — that hides control flow that `match`/named methods show.

### Avoid by default
- Dynamic properties in new code.
- `#[AllowDynamicProperties]` as a convenience escape hatch.
- Magic-heavy abstractions that trade clarity for cleverness.

## PSR / PER standards

### Style and file rules
- Follow PSR-1 and PSR-4 by default.
- Use PSR-12 as the broad compatibility baseline.
- Treat PER Coding Style 3.0 as the modern extension of PSR-12 when the repo and tooling intentionally adopt it.
- Keep declarations and side effects separated in reusable files.

### Interop rules that matter in app code
- PSR-3:
  - prefer logger interfaces for reusable or library-like code
- PSR-11:
  - the container is for wiring, not for app code to pull dependencies from
- PSR-20:
  - prefer `ClockInterface` when time seams matter
- PSR-14:
  - relevant mainly for library or framework-interop code, not as a mandatory default in standard Laravel app code

### Anti-patterns
- Mixing symbol declarations and startup side effects in the same reusable file.
- Treating PSR-11 as permission to use a service locator.
- Adopting PER rules ad hoc when the repo formatter or linter still enforces PSR-12 only.

## Error handling
- Throw specific exceptions instead of generic `Exception`.
- Keep exception types aligned to ownership:
  - domain failures
  - validation / usage failures
  - integration or infrastructure failures
- Translate exceptions at boundaries instead of deep inside domain code.
- Preserve the previous exception when wrapping low-level failures.
- Never swallow `Throwable` silently.

### Anti-patterns
- Returning `null` or `false` for every failure mode.
- Catching and logging without rethrowing or mapping deliberately.
- Putting sensitive details into client-visible messages.
- Using exceptions for ordinary branching when local validation can express the condition clearly.

## Low-level performance
- Measure before optimizing.
- Avoid repeated `json_encode` / `json_decode` churn in hot paths.
- Avoid unnecessary array copies, large temporary arrays, and broad object graphs.
- Prefer immutable small objects for stable data.
- Be cautious with reflection, dynamic magic, and runtime configuration mutation.
- For application-level dataset traversal, prefer Laravel's `lazy`, `chunk`, `chunkById`, and `cursor` guidance in `laravel-best-practices.md`.
- For Octane or long-lived worker behavior, switch to `alaa-octane-performance`.

## Security-sensitive handoff
This skill includes only the code-level baseline:
- validate at edges
- avoid trusting client-derived IDs blindly
- never leak secrets or raw tokens in messages

For auth, tenant boundaries, injection, secrets, abuse controls, or security sign-off, read `alaa-security-review`.

## Official references
- PHP manual:
  - type declarations
  - interfaces
  - properties / readonly behavior
  - enums
  - exceptions / `Throwable`
  - attributes
  - `match`
  - `DateTimeImmutable`
- PHP-FIG:
  - PSR-1
  - PSR-4
  - PSR-11
  - PSR-12
  - PSR-20
  - PER Coding Style 3.0
