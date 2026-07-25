# Scripts And State Capture

Read this file when a request needs a value that an earlier response produced, or
when writing any script into the collection.

`assets/token-capture-post-response.js` is the worked template. Fill it in; do not
paste a hand-written variant per request, and do not restate its comments in a
request description.

## The rule this file exists for

No value is ever copied by hand between two requests in the same collection.

A login or token request captures the token in its own post-response script and
writes it to the variable the next request already references. A create request
captures the new resource's public identifier the same way. Sending the login request
and then sending any dependent request must work with no manual step in between.

A collection that requires a developer to paste a token into a variable is
incomplete, and the missing capture is the defect — not the developer's workflow.

## Which variable scope to write

This decision decides whether a secret reaches git. It is not a style choice.

- **Write with `pm.environment.set(name, value)`** for every credential, every session
  identifier, and every value that differs per developer. The environment file is the
  per-developer artifact and is committed with placeholders only, so a captured value
  lives in the developer's local environment and never in a committed file.
- **Write with `pm.collectionVariables.set(name, value)`** only for a non-secret value
  that is genuinely identical for every developer and every environment. Postman's
  `pm.collectionVariables.set` mutates the collection in place, so whatever it wrote
  is present the next time that developer exports the collection. Ask one question
  before using it: if this value were committed inside the collection JSON, would that
  be safe? If the answer is no, it is an environment variable.
- **Never write a captured value with `pm.globals.set`.** Globals are workspace-wide,
  are not part of either committed artifact, and Insomnia does not support them —
  `50-insomnia-compatibility-and-free-plan-rules.md` has the source.

**Read** with `pm.variables.get(name)`. It resolves through the scope chain and returns
the highest-precedence value, so a script keeps working when a variable later moves
between collection and environment scope. Both Postman and Insomnia document a
`variables.get`; `collectionVariables.get` is not documented on the Insomnia side.

Every variable a script writes is declared in the committed collection or the
committed environment before the script ships. A capture that writes to an undeclared
name populates a variable no request reads.

## Where a script goes

The executable location for a request script is the request item's own top-level
`event` array, with `script.exec` as an array of one string per line.

Never place a script under `request.event`. That field is outside the v2.1 request
schema: clients display the JSON and never execute it, so the capture silently never
runs and the next request fails on a stale variable.

At most one `prerequest` event and one `test` event per scope. Postman permits an
array, but Insomnia's importer takes the first matching listener per scope and drops
the rest, so a second `test` event is executable in Postman and absent in Insomnia.

Choose the narrowest scope that keeps the behaviour findable:

- collection scope for setup or assertions that genuinely apply to every request
- folder scope for logic bounded to one service or one context
- item scope for this request's own captures and assertions

## What a capture script must do

The template encodes all six. Each one corresponds to a failure that is silent
without it.

1. **Guard on an explicit success status.** `if (pm.response.code === 200)` or an
   equivalent explicit check. Without it, an intentional error response overwrites a
   working token with `undefined` and every later request fails for the wrong reason.
2. **Parse the body defensively.** Wrap `pm.response.json()` in a `try`; a non-JSON
   error body must not throw inside the script and abort the remaining assertions.
3. **Skip empty values.** Do not write `undefined`, `null`, or an empty string over an
   existing value.
4. **Fail loudly when extraction fails.** Report the missing field through a failing
   `pm.test` that names the field and its JSON path. A swallowed failure leaves the
   previous value in place, which is worse than no value: the next request sends a
   stale token and returns a misleading `401`.
5. **Update every rotated value on every rotation.** A refresh route that returns a new
   access token and a new refresh token writes both. Writing only the access token
   leaves the next refresh using a consumed token.
6. **Never log or assert the secret's value.** Assert that the variable is non-empty and
   is not still a placeholder. `console.log(token)` puts the token in a shared console
   transcript and in a screenshot.

Correlation-only values such as a request id or a traceparent are the one exception to
the success guard: they are captured on error responses too, because that is exactly
when someone needs them to find the request in the logs.

## Never hardcode a credential

In a committed collection or environment, these are all defects:

- an `Authorization` header whose value is a literal token instead of `Bearer {{access_token}}`
- an `auth.bearer` token value that is a literal instead of a `{{variable}}`
- a real token, password, API key, or signed URL in a request body, a saved example, or
  a script
- a real credential as a variable's committed value

The positive replacement in every case: reference a variable, declare that variable in
the environment with a placeholder value, and populate it from a capture script or from
the developer's own local edit. `30-variables-auth-and-environments.md` owns the
placeholder and secret-typing rules for the environment file.

## Script APIs to use and to avoid

Use `pm.test`, `pm.expect`, `pm.response`, `pm.request`, `pm.variables`,
`pm.environment`, `pm.collectionVariables`, and `pm.cookies`.

Avoid, because they either have no meaning outside Postman or do not survive import:

- the deprecated `postman.*` interfaces, including `postman.setEnvironmentVariable`
  and `postman.setNextRequest`
- `pm.globals.*`
- `pm.vault.*`, `pm.require`, `pm.state`, `pm.datasets`, and `pm.visualizer`
- `pm.execution.setNextRequest`, `pm.execution.skipRequest`, and
  `pm.execution.runRequest` as anything the collection's correctness depends on; they
  change behaviour only under the Collection Runner, so a plain Send produces a
  different result

Prefer ordinary collection order plus captured variables over runner control. When a
scenario truly needs run ordering, keep it additive: the collection still works
request-by-request without it.

## Dependency audit before closing

For every `{{variable}}` that appears in a request URL, header, query, or body, prove
one of two things:

- an earlier request in this collection populates it with an executable, success-guarded
  script, or
- it is operator input, declared in the environment with a placeholder, and its
  `## Flow position` block says so.

A variable that is neither is a manual copy step the collection has not admitted to.
Replace a hardcoded fixture identifier with the captured value whenever a producing
request exists.

## Mechanical gate

```shell
python3 "$SKILL_DIR/scripts/validate_postman_artifacts.py" path/to/collection.json \
  --env path/to/environment.json \
  --require-success-guarded-captures \
  --require-token-capture
```

`--require-token-capture` fails a request whose saved success example contains a token
field but whose scripts write no token variable. `60-validation-and-output-contract.md`
holds the full flag set and the exit codes.
