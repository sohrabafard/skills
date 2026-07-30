# VRL transforms

Verified against Vector `0.57.0` / VRL `0.34.0` on 2026-07-30.

## Fallibility is the whole subject

Most VRL mistakes are one mistake: not knowing whether an expression can fail.

| Form | Behaviour | Can `??` follow it? |
| --- | --- | --- |
| `f(x)` | Returns an error value on failure | **Yes** — this is what `??` is for |
| `f!(x)` | **Aborts the program** on failure | **No** — the right side is unreachable |
| `.path` | A path lookup never fails; a missing field is `null` | **No** — there is no error to coalesce |
| `a, err = f(x)` | Two-value form; you branch on `err` | Not applicable |

**`??` coalesces errors, not null.** That single sentence explains every instance of
the defect below. Verified directly:

```
.out = string(.missing) ?? "DEFAULTED"   -> { "out": "DEFAULTED" }    # string() errors, ?? fires
.out = .missing ?? "DEFAULTED"           -> error[E651]               # path lookup cannot fail
.out = string!(.level) ?? "DEFAULTED"    -> error[E651]               # string! aborts, never errors
```

### error[E651] is a compile error, and this skill shipped six of them

Diagnostic 651, *"unnecessary error coalescing operation"*, stops compilation:
*"the left-hand operation is infallible, and so the right-hand value after `??` is
never reached."* Before Batch 8 all three shipped templates failed `vector
validate` on it. The pattern was `string!(x) ?? "default"` — the `!` makes the call
infallible, so the default is dead code and the config does not compile.

**Rule:** to default a value, use the fallible form and coalesce:
`string(.service) ?? "unknown"`. Reach for `f!` only where an abort is genuinely
the behaviour you want, which on a telemetry path it usually is not — an aborted
`remap` drops the event.

**Rule:** to default a possibly-absent field, test for it. `??` cannot do it,
because a missing path is `null` and not an error:

```coffee
# Wrong: compiles as E651, and would not default anything if it did compile.
.ts = .timestamp ?? now()

# Right:
.ts = if exists(.timestamp) { .timestamp } else { now() }
```

The wrong form is the more dangerous of the two defects, because it *looks* like
timestamp defaulting. Fixing only the diagnostic — deleting the `??` — leaves
events with no timestamp.

`assets/fixtures/red-e651.yaml` is a committed fixture asserting the checker still
catches this class.

## Constraints, not preferences

"Keep programs short" is a preference an agent can satisfy while writing something
unmaintainable. These are checkable:

- **One responsibility per `remap`.** A transform either normalises, or enriches,
  or routes — not two. Reason: `vector test` asserts on a transform's output, so a
  transform that does two things cannot have either one tested in isolation.
- **Name a transform for what it produces, not what it consumes.** `normalize` and
  `enrich`, not `process_demo_logs`. Reason: the name appears in
  `component_errors_total` labels and in `vector top`, where you are reading it to
  find out what broke.
- **Every fallible call is either coalesced with `??`, branched on with the
  two-value form, or deliberately `!`-aborted with a comment saying why.** Reason:
  the default in a review is otherwise unknowable from the code.
- **Every non-trivial transform has a test covering the absent, wrong-type and
  malformed input cases.** Reason: those are the inputs that produced the code.

## Idioms worth having

Safe JSON parse — the two-value form, so a non-JSON message does not abort:

```coffee
parsed, err = parse_json(.message)
if err == null && is_object(parsed) {
  .structured = parsed
}
```

Redaction driven by a field-name list. `exists()` takes a path literal, so a
name-driven loop must use `get`, which is fallible and returns null for an absent
field:

```coffee
for_each(["token", "password", "authorization", "api_key"]) -> |_i, field| {
  current = get(., [field]) ?? null
  if current != null {
    . = set!(., [field], "[REDACTED]")
  }
}
```

Redacting one example field is not a policy. What must never be logged is owned by
`/alaa-observability-soc` (`$alaa-observability-soc`); the field **names** are owned
by `/alaa-services-contract` (`$alaa-services-contract`).

## Sharp edges

- Hyphenated and dotted field names need quoted access: `."trace-id"`.
- A `remap` that aborts drops the event. If the event matters more than the
  enrichment, branch instead of aborting.
- `parse_regex` accepts a dynamic pattern as of VRL 0.34.0. A pattern built from
  event data is an injection surface and a cost risk; prefer a fixed pattern.
- `parse_cef` gained `strict`, default `true`.
- A panic on inputs of 65,535 bytes or more was fixed in VRL 0.34.0. If you are
  pinned below it and parse large payloads, that is a crash you can still hit.
- Per-event VRL cost multiplies by throughput. When a transform's cost must be
  stated as a bound rather than measured, that is
  `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).

## Reading internal metrics from VRL

`get_vector_metric`, `find_vector_metrics` and `aggregate_vector_metrics` exist as
of 0.53.0 and are current on 0.57.0. If a program indexes histogram buckets
directly, note that internal histograms went from 20 to 26 buckets in 0.53.0 and
every index shifted — see `80-version-and-upgrade-deltas.md`.
