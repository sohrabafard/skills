# Pagination And Limits As The Consumer Sees Them

Read this before documenting any route that returns a collection, and before documenting any
request field that accepts more than one value.

**Not owned here.** The pagination mechanism — ordering tuples, the index, the continuation
predicate, the cursor codec, the page-size default and ceiling, the reversal tests — is
`alaa-keyset-pagination` (`/alaa-keyset-pagination`, `$alaa-keyset-pagination`). The wire keys,
the prohibition on offset, the reject-don't-clamp rule, and the five conditions that permit an
admin offset table are `alaa-services-contract` (`/alaa-services-contract`,
`$alaa-services-contract`) `references/25-end-to-end-flow-and-boundaries.md`. Why an unbounded
result set is a defect at all is `alaa-algorithms-data-structures`
(`/alaa-algorithms-data-structures`, `$alaa-algorithms-data-structures`). On any conflict about
a key name, a bound, or whether offset is allowed, those skills win. This file fixes what the
pack emits so a consumer can page correctly from the document alone.

## Five statements per list route

**1. The declared mode**, exactly one of `keyset`, `offset`, or `none`, written as
`x-pagination` on the operation and repeated in prose in the endpoint document. A list route
emitted with no declared mode is an unresolved route. `offset` is only writable when the
route's own documentation already records the five-condition exception; `none` is only writable
for a collection bounded by schema rather than by tenant data.

**2. The `limit` parameter's declared maximum equals the value the route enforces**, read from
the FormRequest rule or validator that rejects an over-maximum request, cited by path and line.
A document that declares a maximum the code does not enforce, or enforces a maximum the
document does not declare, is a defect: a consumer that trusts the document receives a `400` it
was told could not happen. This is the pack's own check and no other skill performs it.

**3. A saved example for the rejection.** One over-maximum `limit` request with its actual
status and `code` from the running service or a passing test. The rule that the service rejects
rather than clamps belongs to the contract skill; the pack's obligation is the example that
proves this route obeys it.

**4. A saved example showing both cursor keys in both states** — one page where the forward
cursor is a string and one where it is `null`, and the same for the backward cursor. The
always-present rule is the contract's; the examples are the pack's, and they are what stops an
SDK author from writing a presence check.

**5. The cursor's opacity, stated in the SDK notes as an instruction to the client**: hold the
cursor as an opaque string, echo it back unchanged in `cursor`, and never parse, construct,
persist beyond the session, log, or derive a page number from it. No example, error body, or
schema in the pack contains a decoded cursor or a description of its fields.

## Laravel expression

- The cursor and page-size parameters arrive as query parameters validated by a FormRequest.
  The pack cites the rule lines that accept `cursor` and `limit`, and cites the absence of
  `page`, `per_page`, `offset`, and `skip` in that same rule set. Validation mechanics are in
  the service repository's own `laravel-best-practices/rules/validation.md`, which this
  repository does not own; ours wins on any conflict.
- The pack cites the paginator call site, so a reader can see which component produced the
  shape being documented. Which paginator is acceptable, and why Laravel's native
  `cursorPaginate` is not, is `alaa-keyset-pagination references/60-per-stack.md`.
- **A list route whose result set grows with tenant data and whose code calls no paginator is
  not documented as `x-pagination: none`.** Writing `none` there converts a service defect into
  a published promise that the collection is bounded, and every consumer then builds a client
  that loads the whole table. Report the route, its path, and the absent paginator to the
  repository owner, and treat the route as unresolved for the emission gate in `SKILL.md`.

## Other consumer-visible bounds

Page size is not the only limit a client hits. Every request field that accepts more than one
value carries its own bound in the pack: the minimum and maximum element count, whether
duplicates are rejected, the element's form, and the `code` returned when the bound is
exceeded — each read from the validator, not from the field's name. A batch field documented
without its bound produces a client that sends a thousand elements and discovers the limit in
production.

Response-side bounds belong here too: any array in a response that the service truncates
states the truncation limit and how a consumer retrieves the remainder. An array that is
neither bounded nor paginated is a finding for the repository owner, not a documented shape.

Platform-level limits a consumer must respect but the repository does not fix — a published
gateway quota, a burst allowance — are not invented here. They carry the
`NEEDS_BACKEND_CONFIRMATION` marker under the entry condition in `SKILL.md`, and the pack
states the observable client behaviour instead: which status the consumer will see, and that it
honours the retry hint the error envelope carries.
