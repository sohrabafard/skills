# Consumer Discovery, Pinning, And Secret Hygiene

Read this when creating a pack, when bumping its version, and before writing any file of the
pack to disk.

A public API contract exists for callers this service cannot deploy in lockstep with. Such a
caller needs three things the artifacts must supply on their own: a way to find the contract,
a way to pin the version it built against, and a way to learn that the version changed. This
file fixes all three, and the rule that keeps the emitted artifacts from leaking a credential.

## Discovery: `contract.meta.json` is the entry point

One machine-readable file at the pack root, and it is what a consumer, a CI job, or the next
agent reads first. These fields are required; a pack missing any of them is incomplete.

| Field | Content |
|---|---|
| `name`, `service` | the pack identifier, and the canonical service identity, whose form is owned by `alaa-services-contract` (`/alaa-services-contract`, `$alaa-services-contract`) `references/10-core-service-contract.md` |
| `contract_version` | semver over the pack, per the pinning rule below |
| `api_version` | the API major the pack documents, matching the route inventory |
| `contract_root` | the pack's own path in the repository, so the next run resolves no hedge |
| `generated_at`, `generated_from` | the timestamp, the ranked source list actually read, and the route-inspection command with the route count it returned |
| `endpoint_inventory` | every group, each with a `status` from the closed set `exists`, `not_implemented`, `reserved` |
| `uncertainty_list` | one entry per marker used, each naming its subject |
| `validation_summary` | one entry per item of the validation floor below, each `passed` or naming its blocker |

`reserved` is not decoration: it is the zero-day removal window in
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`, so a group
marked `reserved` is a surface no consumer may wire to and no SDK method may exist for. A group
whose status is `exists` while its `routes` array is empty is a contradiction the gate refuses.

## Pinning: one version, in two files, with one meaning

`contract_version` is semver over the **pack**, not over the API major. It increments by the
class in `references/10-versioning-and-breaking-change-classification.md`: major for a breaking
change, minor for an additive one, patch when only wording changed and no consumer-observable
statement did. `openapi.yaml` `info.version` carries the same value, byte-for-byte; two
spellings of one version is the defect `scripts/contract_pack_audit.py` reports as exit 4.

A consumer pins by the pair `contract_version` plus the commit SHA the pack was generated from,
both recorded in the pack. A version alone is not a pin, because a pack can be corrected in
place; a SHA alone is not a pin, because no consumer wants to read a diff to learn what changed.

## Learning that it changed

The pack carries a changes file with one dated entry per `contract_version`. Each entry names
the class from `references/10-...`, lists the affected operations by method and path, and for a
breaking change names the window class and the recorded removal date. **A `contract_version`
bump with no entry is a gate failure**, because a consumer that cannot diff two versions from
the document has to diff the service.

This is also what makes the notification step in
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md` executable: that
step requires an issue in every consuming repository, and the pack's `audience` and SDK package
target are where the list of those repositories lives. A pack that does not name its consumers
cannot satisfy a procedure that requires notifying them.

## Secret hygiene for the emitted artifacts

The typed-secret rule, the placeholder rule, and the per-developer versus shared split for the
Postman files are `alaa-postman-collections` (`/alaa-postman-collections`,
`$alaa-postman-collections`) `references/30-variables-auth-and-environments.md`, which wins on
any conflict about those files. Three rules are added here, and they are this skill's because
they cover the pack, not the collection.

**1. Provenance.** Every value in the emitted environment and every value in every saved
example is written from the route inventory, the repository's own fixtures, and its passing
tests. None is harvested from a developer's live Postman export, a browser session, an HTTP
proxy capture, or a production log. A harvested artifact carries whatever that session held: a
real bearer token, a real trusted header, a real signed media URL, a real subscriber's mobile
number. The mechanism that prevents the leak is where the value came from, not a review pass
afterwards.

**2. One scan over the whole tree, before the first file is written.** The pack emits markdown,
YAML, and JSON, and a Postman validator reads only the last of those. Scan every file of the
pack for: a JWT-shaped literal (`eyJ` followed by two dot-separated segments), an
`Authorization` value that is not an obvious placeholder, a non-placeholder value for any header
the boundary extraction in `SKILL.md` classified as trusted-injected, a hex or base64 literal of
32 characters or more that is not a documented identifier example, and a production hostname. A
hit blocks emission and is reported with its file and line. Do not resolve a hit by deleting the
line alone: replace the value with a placeholder and record why it was there, because the same
generation step will otherwise reproduce it next run.

**3. Examples are the leak surface with no variable to type.** An environment variable can be
marked secret; a response body in a markdown code fence cannot. Every saved example is
constructed from placeholder inputs and fixture outputs, and every identifier in it is a public
identifier in the form owned by
`alaa-services-contract references/25-end-to-end-flow-and-boundaries.md`. What must never
appear inside an error envelope's `meta` — exception text, SQL, internal identifiers, secrets,
PII beyond the request's own — is bound by that skill's
`references/10-core-service-contract.md`; the pack's obligation is that its saved error examples
obey it and that at least one saved `4xx` and one saved `5xx` example exist to be checked.

## Deliverables floor

Follow the repository's existing convention when one exists. Otherwise this is the floor, and fewer files
is an incomplete pack: `contract.meta.json`; README; route inventory; authentication and boundary
notes; per-endpoint request, response, error and example docs; error catalogue; pagination;
idempotency; rate limits; lifecycle; versioning plus a dated changes file; SDK input notes;
`openapi.yaml`; Postman collection and environment; validation notes. Adding is normal. Dropping
an item requires citing the evidence that the surface does not exist.

## Validation floor

Every item runs on every emission.

- `php artisan route:list --json` captured to a file
- the audit command named in the emission gate in `SKILL.md`, exiting `0`
- every JSON artifact parses; every YAML artifact parses
- the repo-native public API audit command, when one exists
- one saved `4xx` and one saved `5xx` example, plus the secret scan above
- `git diff --check`

A blocked item is recorded with its exact command and blocker. A blocked inventory means refusal.
