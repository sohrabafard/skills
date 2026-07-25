# Mock Servers

Read this file when a mock server is requested, or when deciding whether one is worth
defining for a collection.

## What a mock server is here

A Postman mock server is a hosted URL bound to one collection and, optionally, one
environment. A request to it is matched against the collection's **saved examples**, and
the matched example's status, headers, and body are returned.

That makes the mock a derived artifact. The saved examples are the thing being built;
the mock is a way to serve them. Every rule in
`41-response-contract-and-error-coverage.md` therefore applies unchanged, and none of
them is relaxed to make a mock more convenient. An example authored to make a mock
behave nicely, but which contradicts the shipped contract, has broken the contract to
fix the mock.

## When a mock is worth defining

Define one when at least one of these is true:

- a frontend needs to build against a route before the backend implements it, and the
  contract is already agreed
- a consumer needs a stable endpoint for an integration test that must not depend on a
  running backend
- a security or resilience test needs a specific error response reproduced on demand

Do not define one when:

- a real local environment already serves the routes, and the mock would become a second
  source of truth to keep in step
- the collection's examples do not yet cover the route's real responses; fix the coverage
  first, because the mock can only serve what the examples contain
- the value being sought is documentation. Postman's generated documentation already
  renders saved examples without a mock server existing.

A mock is never required for the collection to be complete. Correctness must not depend
on one existing, on its URL, or on its call volume, because mock-server call volume is
metered per Postman plan and a committed artifact cannot assume any plan.

## How an example drives the mock

Postman's matching algorithm filters and scores the collection's examples in this order.
Each step has a consequence for how examples must be authored.

1. **Method.** Examples whose method differs from the incoming request are removed. An
   example whose `originalRequest.method` disagrees with its own request item can
   therefore be unreachable.
2. **Mock control headers,** processed in this order: `x-mock-response-code` filters by
   status, `x-mock-response-id` selects one example by its UID, `x-mock-response-name`
   selects one by its name. This is why an example's name is an addressable identifier
   and must be distinct and stable: renaming an example breaks every caller that
   requested it by name.
3. **URL path,** scored by similarity rather than matched exactly. A path built from
   `{{variables}}` scores against whatever the caller actually sends, so an example whose
   URL still carries an unresolved placeholder segment can score below an unrelated
   example.
4. **Query parameters,** which adjust the score.
5. **Headers and body,** filtered or scored only when `x-mock-match-request-headers` or
   `x-mock-match-request-body` enables it.

When several examples tie at the highest score, Postman sorts them by ID and returns the
first one with a `200` status; if none of the tied examples is a `200`, it returns the
first in that sorted order. Two rules follow directly:

- **Every mocked request has a `2xx` example.** Without one, a caller sending an ordinary
  request can receive an error example as the default response, and the mock looks like a
  broken backend.
- **An error example is reached deliberately,** by `x-mock-response-code` or
  `x-mock-response-name`. Document that header and value in the request's `## Errors`
  table so a consumer can reproduce the error without guessing.

## Variables inside a mocked example

A `{{variable}}` in an example's body or headers resolves only from the environment the
mock server is linked to. When the mock has no linked environment, or the environment
does not declare the name, the caller receives the literal `{{name}}` text in the
response body — which is a silent failure, because the response is still a valid `200`.

Therefore:

- every variable referenced inside a saved example is declared in the environment the
  mock is linked to, under the same name
- a committed environment's base URL variable keeps pointing at the real host. Point a
  developer's local copy at the mock URL when they want the mock; never commit the mock
  URL as the default, because a collection whose committed default is a mock silently
  stops testing the real service.

## Naming

Name the mock server after the collection and the purpose, such as
`<collection> Mock (frontend preview)`. The name is how a reader tells it apart from a
real environment in a dropdown, and an unnamed or generically named mock is the reason
someone runs a suite against a mock and reports the results as real.

## Insomnia

Postman mock servers are not imported by Insomnia; they have to be recreated there. The
saved examples that drive the mock are also not imported —
`50-insomnia-compatibility-and-free-plan-rules.md` has the source and the consequence.
So a mock server is a Postman-side convenience only, and a collection whose usefulness
depends on a mock is not portable to Insomnia by any configuration.
