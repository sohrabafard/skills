# Validation and testing

Verified against Vector `0.57.0` on 2026-07-30.

## The flag set that actually catches things

Use this:

```bash
vector validate --skip-healthchecks --deny-warnings vector.yaml
```

**Do not use `--no-environment` as your validation command.** It disables component
checks, and several of Vector 0.57.0's most important config errors *are* component
checks. Observed on the same four files, changing only the flags:

| Fixture | `--skip-healthchecks` | `--no-environment` |
| --- | --- | --- |
| `assets/fixtures/green-minimal.yaml` | exit 0 | exit 0 |
| `assets/fixtures/red-e651.yaml` | exit 78 | exit 78 |
| `assets/fixtures/red-unconfined-template.yaml` | **exit 78** | **exit 0** |
| `assets/fixtures/red-undersized-disk-buffer.yaml` | **exit 78** | **exit 0** |

So an unconfined routing template and an undersized disk buffer both validate
**clean** under `--no-environment`. Upstream lists the first as a known issue:
*"`vector validate --no-environment` doesn't catch unconfined routing templates …
run `vector validate` without that flag to catch confinement issues before
startup."*

`--no-environment` has one legitimate use: checking syntax and VRL compilation on a
machine where the config's `data_dir` does not exist and cannot be created. It is a
weaker check, and calling it "validated" is the mistake.

Two preconditions for the real check, both environmental rather than defects:

- The `data_dir` named in the config must exist and be writable, or validation
  reports `x data_dir "/var/lib/vector" does not exist`. `VECTOR_DATA_DIR` does
  **not** override the config value — verified.
- `--skip-healthchecks` avoids reaching the network. Without it, validation tries
  to contact every sink.

`scripts/check-vector-configs.mjs` handles both by copying each config to an OS
temp directory with `data_dir` rewritten, so component checks run on any machine
without needing `/var/lib/vector` to exist and without writing inside the
repository.

## `--deny-warnings` earns its place

Some Vector warnings are silent-data-loss defects. The clearest one:

```
WARN vector::config: Source has acknowledgements enabled by a sink, but
acknowledgements are not supported by this source. Silent data loss could occur.
```

A config that emits this looks durable and is not. Treating it as a finding rather
than as console noise is the whole point, so the shipped checker runs with
`--deny-warnings` by default and offers `--allow-warnings` for the cases where a
warning genuinely is informational.

**The trap `--deny-warnings` sets, and it is a real one.** An unconsumed `route`
output is a warning, so it becomes exit 78 under the flag. Observed on 0.57.0, same
config, flags the only difference:

```
vector validate --skip-healthchecks
  ~ Transform "route_events._unmatched" has no consumers      EXIT=0

vector validate --skip-healthchecks --deny-warnings
  x Transform "route_events._unmatched" has no consumers      EXIT=78
```

Every `route` transform has an implicit `_unmatched` output, so **a `route` whose
default leg goes nowhere fails a `--deny-warnings` gate** — including a config that
deliberately discards unmatched events. Do not resolve this by dropping the flag,
which also un-gates the acknowledgement warning above. Resolve it by wiring
`_unmatched` to something that makes the discard visible: a `log_to_metric` counter,
or a dead-letter sink where policy allows one. If the leg genuinely must be
discarded and cannot be counted, that is the narrow case for `--allow-warnings` on
that config, recorded with its reason — and `75-ala-ingest-pipeline.md` rule 5 states
why a counter is the floor rather than the answer.

## Unit tests must be passed together with the config that defines the transform

`vector test` resolves transforms across the whole config set it is given. A test
file that references a transform defined elsewhere fails alone:

```
$ vector test assets/templates/vector-tests.yaml
Failed to build test 'happy path ...':
  Invalid extract_from target: 'normalize' does not exist
EXIT=78
```

That failure reads like a broken test and is actually a missing argument. Pass both:

```bash
vector test assets/templates/vector-basic.yaml assets/templates/vector-tests.yaml
```

## Test the failure classes, not the happy path

A suite that only proves the good input works cannot distinguish a correct
transform from one that has silently lost its defaulting logic. For every
transform, cover the inputs that made you write the code:

- the field is **absent**
- the field is present with the **wrong type** — a level arriving as an integer
- the payload is **malformed** — non-JSON text into `parse_json`
- the field name needs **quoting** — hyphenated keys
- the event must be **dropped**, asserted with `no_outputs_from[]`, which is the
  only way to prove a routing or filtering transform discarded something

`assets/templates/vector-tests.yaml` ships five cases in this shape and all five
fail if the `string!` to `string` correction is reverted. Test design in general
belongs to `/alaa-testing-strategy` (`$alaa-testing-strategy`).

Current unit-test schema keys, verified: `tests[].name`, `inputs[].insert_at`,
`inputs[].type`, `inputs[].log_fields`, `outputs[].extract_from`,
`outputs[].conditions[].type: vrl`, `conditions[].source`,
`outputs[].expected_event_count`, `no_outputs_from[]`, and the `assert!` /
`assert_eq!` functions.

`expected_event_count` was added in 0.56.0 and asserts how many events an output
emitted. It is the assertion for a transform whose *count* is the behaviour — an
`unnest` that explodes one request into N events, or a filter expected to keep
exactly two of five. `no_outputs_from[]` proves a leg emitted nothing;
`expected_event_count` proves a leg emitted the right number, which is the case
between "nothing" and "something" that neither of the other assertions covers.

Verified by running it on 0.57.0 in both directions. The second case is the one that
proves it, because a key Vector did not recognise but silently ignored would pass the
first on its own:

```
outputs[].expected_event_count: 1, one event emitted  ->  test ... passed   EXIT=0
outputs[].expected_event_count: 7, one event emitted  ->  EXIT=78
    expected 7 events from transforms ["t"], but received 1
```

## Iterating on a snippet

```bash
vector vrl -i event.json -o '.level = downcase(string(.level) ?? "info")'
```

`-p/--program` takes a **file path**; an inline program is the positional argument.
Passing a program string to `--program` fails with `io error: Filename too long`,
which does not look like the argument mistake it is. `-o/--print-object` prints the
modified event rather than the final expression.

## Exit codes

`vector validate` and `vector test` both exit **78** (`EX_CONFIG`) on findings and
`0` when clean. 78 is not 1, so any wrapper must map it rather than pass it through.

The scripts this skill ships honour the fleet contract instead:

| Exit | Meaning |
| --- | --- |
| `0` | clean |
| `1` | findings |
| `2` | could not run — Vector absent, network unreachable, checker error |

`2` exists because a gate that cannot distinguish "the tool is missing" from
"nothing is wrong" treats every broken CI runner as a pass. The shell script this
replaced exited `127` when Vector was absent and `1` on a usage error, so a wrong
argument list and a broken pipeline config were indistinguishable to any caller.

## Run the checkers

```bash
node scripts/check-vector-configs.mjs              # every shipped template + unit tests
node scripts/check-vector-configs.mjs --self-test  # prove the checker still detects the red fixtures
node scripts/check-vector-configs.mjs my.yaml      # any config of your own
node scripts/check-upstream-version.mjs            # version drift against upstream
node scripts/check-upstream-version.mjs --self-test
```

Both take `--help`. Both are Node `.mjs` so they run on Windows, where the previous
`bash` script could not run at all.

Run `--self-test` whenever you change a checker. A green checker with no red
fixture is decoration: it proves only that it found nothing, not that it can find
anything.
