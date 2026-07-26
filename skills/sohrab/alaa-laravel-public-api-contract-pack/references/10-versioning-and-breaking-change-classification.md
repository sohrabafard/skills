# Versioning And Breaking-Change Classification

Read this when a route is added, removed, renamed, or has its request or response shape
changed, and when deciding what a version bump on the pack means.

**Not owned here.** What a contract surface is, the removal procedure, and the window
minimums are `alaa-services-contract` (`/alaa-services-contract`, `$alaa-services-contract`)
`references/22-failure-load-and-deprecation-contract.md`. It wins on every disagreement
about a surface definition, a window length, or a field name. This file classifies a change
so the agent knows which window applies, and fixes how a Laravel repository expresses and
emits the decision.

## Three classes, decided by an observable

Classify every change into exactly one. The class selects the window; it does not shorten it.

**Additive.** A new route; a new response field; a new optional request field whose omission
reproduces the previous behaviour; a new `code` appended to the committed registry.
Observable: no existing field changed its type, its nullability, its unit, or its meaning,
and no previously accepted request is now rejected. A consumer built against the previous
pack keeps passing its own tests without a code change.

**Breaking.** Removing or renaming a route, a response field, a request field, an error
`code`, or a header. Changing a field's type, its unit, or its identifier form. Making a
response field nullable that was never null. Making an optional request field required, or
changing a default. Changing which status an existing outcome returns. Changing a route's
pagination mode. Narrowing an accepted value set. Observable: a request that succeeded
before now fails, or a response a consumer parsed before now fails its parser.

**Breaking only for a strict parser.** Adding a member to an existing enum or discriminator;
adding a `code` a closed error union does not carry; adding a response field a generated
client rejects as an unknown property. Observable: the change is additive by the test above,
and a client that models the field as a closed set stops compiling. These are listed in the
pack's changes entry under their own heading so the SDK owner decides, and they take the
same window as a breaking change when a published consumer is known to model the set as
closed.

**Consequence, stated once:** the emitted OpenAPI never sets `additionalProperties: false`
on a response schema. That single keyword converts every additive response change in this
service's future into a breaking one for every generated client.

## Which window applies

A breaking change to a surface a public client can observe takes the publicly-observable
window; one to a surface only first-party services observe takes the first-party window; one
to a group the pack marks `reserved` takes the zero-day window. The day counts, the
announcement record, and the notification steps are in
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. Do not
restate a number here, and do not start a window from the date the code changed: it runs from
the announcement date recorded in that skill's owning reference file.

## Laravel expression

- One route group per served major: `Route::prefix('v3')->group(...)`. The version segment
  appears in the group declaration and nowhere else. Observable:
  `php artisan route:list --json` shows exactly one `/vN/` segment in every public route URI,
  and no controller or route literal repeats the segment.
- **A public route with no version segment** is resolved from the repository's declared
  default — a config key that is read, or a documented statement in the repository's own
  `AGENTS.md`. When the repository declares no default, that route's version is unresolved
  and the emission gate in `SKILL.md` refuses. Do not treat the absence of a segment as
  version 1.
- Two majors served at once are two groups with two controller namespaces. One controller
  class reachable from two version groups is forbidden: a change made for the new major
  silently changes the old one, which is a breaking change nobody announced. Observable: no
  `action` value in `route:list --json` appears under two version prefixes.
- Route mechanics beyond this — group syntax, binding, middleware ordering — are in the
  service repository's own `laravel-best-practices/rules/routing.md`, which this repository
  does not own and which is re-pulled between runs. On any conflict with a rule here or in
  `alaa-services-contract`, ours wins.

## What the emitted artifacts record

- `openapi.yaml` `info.version` is the pack's `contract_version`, identical to
  `contract.meta.json`. The API major lives in the path segment, or in `x-api-version` on the
  operation when the path carries none.
- Every non-operational operation carries an explicit `deprecated: true` or
  `deprecated: false`. Absence is not "not deprecated"; it is unresolved.
- A deprecated operation also carries `x-sunset-date: YYYY-MM-DD`, copied from the removal
  date recorded by the owning reference file in `alaa-services-contract`, never computed
  locally from today's date.
- A route the contract records as non-idempotent carries `x-idempotent: false`. That is the
  OpenAPI-legal spelling of the `idempotent: false` record required by
  `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`; both
  spellings mean the same route, and `references/20-write-semantics-and-idempotency.md` owns
  what else that route must state.
- A deprecation is regenerated, not annotated in one place: the Postman request's
  documentation block carries the sunset date and the replacement operation, and the SDK input
  notes mark the method deprecated. Collection and environment generation is
  `alaa-postman-collections` (`/alaa-postman-collections`, `$alaa-postman-collections`).
  Observable: `scripts/contract_pack_audit.py` reports no `openapi_postman_divergence`.

## Proving it

Run the audit command named in the emission gate in `SKILL.md`. Exit `4` and exit `5` are the
two codes the rules in this file can trigger: a version spelled twice, and a version or
deprecation field left unresolved. The script's `--help` holds every code and its obligation.
