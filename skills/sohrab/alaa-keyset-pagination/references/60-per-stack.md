# Per-stack implementation

The decision is the same in every stack; only the mechanism differs. Language idiom belongs to the language skills — `alaa-laravel-architecture` and `alaa-php-clean-code` (`/alaa-php-clean-code`, `$alaa-php-clean-code`), `alaa-golang` (`/alaa-golang`, `$alaa-golang`). This file owns only what pagination requires of each.

## Laravel

**Rule: `cursorPaginate()` is not the shipped paginator on an Ala list route.**

This is a constraint, not a preference, and it rests on framework source rather than reputation. Verified 2026-07-25 against `laravel/framework` branch `13.x` and the official docs; exact files and URLs are in `90-source-map.md`. Four failures, any one of which is disqualifying:

1. **The cursor is unsigned.** `Illuminate\Pagination\Cursor::encode()` is `base64_encode(json_encode(...))` with the URL-safe substitutions applied and padding stripped. There is no HMAC, no encryption, and no integrity field anywhere in `src/Illuminate/Pagination/`. The decoded values are bound straight into the query's `where` clauses. This alone violates the platform contract's requirement that a cursor be signed and opaque.
2. **It emits the forbidden `OR` expansion, not a row-value comparison.** Laravel's own query-builder test suite asserts the generated SQL for a two-column cursor as `where ("test" > ? or ("test" = ? and ("another" > ?)))`. On PostgreSQL under `ORDER BY ... LIMIT`, that shape degrades to a filter over a full index scan — measured at 173,475 buffers against 13 for the row-value form. The predicate also nests one level deeper per ordering column and rebinds each prefix value, so the binding count grows quadratically.
3. **It does not add a tie-breaker to an existing ordering.** `ensureOrderForCursorPagination` injects the primary key only when the query has *no* ordering at all. `User::orderBy('name')->cursorPaginate()` emits `where ("name" > ?)` with no `id` component — precisely the non-unique ordering that silently skips every row sharing the boundary value, because the comparison is strict.
4. **It throws on a null ordering value.** A null in the cursor reaches `where($column, '>', null)`, which fails `invalidOperatorAndValue` and raises `InvalidArgumentException: Illegal operator and value combination.` Page one succeeds and the *next* page 500s, so the defect ships. Open since 2021 as `laravel/framework#38220`; no null handling exists in `13.x`.

Laravel's own documentation states the constraint that follows from points 3 and 4, and has stated it unchanged since 8.x: cursor pagination *"requires that the ordering is based on at least one unique column or a combination of columns that are unique. Columns with `null` values are not supported."* The platform rules in this skill are that requirement made enforceable rather than advisory.

**What to use instead.** A service-level keyset paginator, shared across the service's routes, that:

- resolves the allowlisted sort mode to its ordering tuple server-side;
- builds the predicate as a row-value comparison via a parameterised `whereRaw` over the ordering columns — the column list comes from the sort allowlist, never from the request, so no identifier is interpolated from client input;
- selects `limit + 1` rows to determine whether a further page exists, then trims to `limit` before serialising;
- derives `next_cursor` and `prev_cursor` from the trimmed page's own boundary rows;
- encodes and signs through the one shared cursor codec described in `30-cursor-format-integrity-and-context.md`.

`simplePaginate()` and `paginate()` are equally unavailable on a list route: both are offset paginators.

Exports and internal traversals use `chunkById` or `lazyById`, never `chunk()` — see `10-route-mode-and-sort-allowlist.md`.

## Go

Go has no framework paginator to reject, so the risk is the opposite one: each service hand-builds a slightly different cursor and the fleet ends up with several formats. The obligation is therefore **one shared package**, not one implementation per service.

The package owns: the cursor struct and its version, encode and decode with signature verification before parsing, the sort-mode registry mapping a mode name to its ordering tuple, the row-value predicate builder, and the `limit + 1` fetch-and-trim.

Two Go-specific correctness points:

- **Build the predicate with a placeholder row constructor**, `WHERE (published_at, id) < ($1, $2)`, and pass the values as parameters. Never format the tuple into the SQL string, even from a value the service itself produced — a formatted timestamp reintroduces the timezone and precision mismatches that the parameterised path avoids, and the pattern gets copied to a route where the value is client-derived.
- **Round-trip the ordering values through the cursor before comparing them.** A `time.Time` serialised to RFC 3339 and parsed back must produce the identical database comparison result; where the column is `timestamptz` with microsecond precision, a codec that truncates to seconds moves the boundary and repeats or drops rows sharing that second. Assert this in the codec's own tests, not only in route tests.

Both stacks emit the same wire surface, defined in `40-wire-contract-limits-and-errors.md`. A client must not be able to tell which stack served a list route.
