# Response Tests

Read this file when writing or reviewing the assertions on a request.

`assets/response-tests-post-response.js` is the skeleton. Fill it in per request.

## The test that is not a test

`alaa-testing-strategy` (`/alaa-testing-strategy`, `$alaa-testing-strategy`) owns test
design, including the rule that a test must name the broken implementation it defends
against. Read that skill for the rule; this file applies it to a Postman request and owns
the Postman-specific minimum below, which that skill explicitly cedes.

`pm.test('works', () => pm.response.to.have.status(200))` passes against a handler that
returns an empty body, returns another tenant's record, returns the previous version of
the resource, or returns a placeholder string. It proves the route is routed, nothing
more.

Before keeping an assertion, name one broken implementation it would catch. If none
comes to mind, the assertion is decoration and the real one has not been written yet.

## The minimum every request asserts

Five assertions, on every request item that has a real response:

1. **Status.** The exact expected status, compared with `eql`. When a route legitimately
   returns one of several statuses, assert membership in that explicit set rather than
   loosening to "not an error".
2. **Envelope shape.** The platform's success envelope, and for an error example the
   platform's error shape. `alaa-services-contract` owns both — assert what that skill
   declares and report drift rather than asserting the drift. Trigger it as
   `/alaa-services-contract` in Claude Code or `$alaa-services-contract` in Codex.
3. **Content type.** `Content-Type` includes `application/json` for a JSON route. This
   catches a handler that fell through to an HTML error page with a `200`, which no
   status assertion catches.
4. **The correlation header.** `X-Request-Id` is present on the response.
   `alaa-services-contract` makes it mandatory on every response, in that skill's
   `references/20-operational-and-observability-contract.md`, which makes its absence a contract failure
   and not a nicety.
5. **The field this request exists to produce.** The one value the caller came for,
   asserted so a wrong value fails and not only an absent one. For a create, that the
   returned identifier is present and well-formed. For a list, that the collection is
   an array and that its first element carries the fields the caller reads. For a
   state change, that the returned state is the new state and not the old one.

Add beyond the five only what this route's contract defines: pagination fields, a
location or retry header, an idempotency replay marker, an ETag, a rate-limit header.

## Assertions to keep out

- Whole-response snapshots, unless the repository already treats the exact payload as
  the contract.
- Response-time budgets, unless the repository has a stated latency contract for this
  route. A time assertion that fails on a loaded laptop trains people to ignore red
  tests.
- Assertions on a secret's value. Assert that a token variable is non-empty and is not
  still a placeholder; never assert its content.
- Assertions on a field the route does not return. It fails for the wrong reason and
  reads as a broken route rather than a broken test.

## Portable assertion form

Write assertions as `pm.expect(pm.response.code).to.eql(200)` and
`pm.expect(pm.response.headers.has('X-Request-Id')).to.be.true`.

`pm.response.code` is the numeric status on both sides and is the property to compare
against a number. **`pm.response.status` is not a second spelling of it:** it is the reason
phrase, a string such as `OK`, on both sides. Comparing it to `200` always fails.
`50-insomnia-compatibility-and-free-plan-rules.md` carries the source citation and the
version the claim was read at.

The chai-style chain also survives import, but only for the members Insomnia registers.
`pm.response.to.have.status(200)` and `pm.response.to.have.header('X-Request-Id')` both
work; `50-insomnia-compatibility-and-free-plan-rules.md` lists the complete registered set
and the validator warns on any member outside it. Prefer the `pm.expect` form anyway, for a
reason that is about failure messages rather than portability: `pm.expect` takes a message
argument, so a failure names what was being checked instead of only reporting a mismatched
value. Existing collections using a registered chain member are correct and need no change.

## Where tests go

Item-level `event` with `listen: "test"`, one event per scope, `script.exec` as an
array of lines. `42-scripts-and-state-capture.md` owns the placement rules and the
reason a second `test` event in one scope is a portability defect.

A request that both captures state and asserts contract keeps both in that single
`test` event: capture first, then assert, so a failed assertion does not prevent a
capture the next request needs.

## Mechanical gate

```shell
python3 "$SKILL_DIR/scripts/validate_postman_artifacts.py" path/to/collection.json \
  --env path/to/environment.json \
  --require-tests \
  --require-correlation-assertion
```

`--require-tests` fails a request with no `pm.test` in its executable scripts.
`--require-correlation-assertion` fails a request whose tests never reference
`X-Request-Id`. `60-validation-and-output-contract.md` holds the full flag set and the
exit codes.
