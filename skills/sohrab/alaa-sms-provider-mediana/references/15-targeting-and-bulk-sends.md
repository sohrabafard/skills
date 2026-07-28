# Mediana / IPPanel Edge — targeting and bulk sends

Read this when the audience is a segment rather than a list of numbers you already hold: `phonebook`, `keyword_phonebook`, `postal_code`, `country`, `geolocation`, and `job`.

## The approval gate

**Do not build, trigger, or test a live send in any mode on this page until product, legal or compliance, and the account owner have each approved this specific campaign and its data source, and the approval is recorded in the change.** These modes send to people who never gave this service their number: the vendor resolves the audience from its own demographic and phonebook data, so the recipient count is unknown at request time and unbounded in practice. A mistake here is an unrecallable message to strangers, and the only signal you get back is one outbox id.

Building a payload, a fixture, or a unit test against these shapes is allowed without approval. Sending one is not. `scripts/validate_mediana_payload.py` warns on every mode on this page for exactly this reason.

No Alaa command family carries any of these modes today (`alaa-services-contract references/27-notification-service-contract.md:88-90`), so a first use also needs a new command family before it needs a payload.

## Provenance

- Documentation repository: `https://github.com/ippanelcom/Edge-Document`
- Rendered documentation: `https://ippanelcom.github.io/Edge-Document/docs/`
- **read: unverified as of 2026-07-27.** No session that produced or revised this file had network access to those URLs.

Every numeric id below — postal codes, province, county and city ids, job category ids, operator ids, and the Persian-calendar year values in the age fields — is account data or vendor reference data. None of it is verified here. Resolve each from the panel before a send, and mark anything you cannot resolve `NEEDS_MEDIANA_CONFIRMATION`.

## `phonebook`

`params` is an array; each element selects contacts from one phonebook in one of two ways.

| `type` | Required in the element | Meaning |
|---|---|---|
| `all` | `phonebook_ids` (array of id strings), optional `start` and `size` | every contact in the listed phonebooks, optionally windowed |
| `detail` | `phonebook_id` (single id string) and `number_ids` (array of id strings) | only the listed contacts in one phonebook |

- Match `type` to its own key set: `all` takes `phonebook_ids`, `detail` takes `phonebook_id` plus `number_ids`. Sending `phonebook_ids` with `type: "detail"` is accepted and the selection silently widens.
- Treat `start` and `size` as a window over an ordering the vendor owns and does not document. Do not use them to paginate a campaign across requests, because a contact added between requests shifts the window and is either sent twice or skipped.

## `keyword_phonebook`

`params` is an array of objects, each carrying `phonebook_id`. `message` carries placeholders that resolve against phonebook fields, in the same brace form as the `keyword` file mode. Placeholder tokens are account-specific; the rules in `references/12-multipart-and-file-sends.md` apply unchanged.

## `postal_code`

Each `params` element selects a demographic slice.

| Field | Shape | Notes |
|---|---|---|
| `bank` | string | the vendor data set to draw from, for example `all` |
| `postal_code` | integer | the postal-code prefix for the area |
| `gender` | integer | vendor-coded; resolve from the panel |
| `age_from`, `age_to` | integer | Persian-calendar birth years, not ages |
| `mci`, `irancell`, `other` | object of `start` and `size` | how many numbers to draw from each operator |

`other_recipients` may carry an explicit recipient array alongside the demographic selection.

- Set `size` to `0` for an operator you do not want. Omitting the operator object entirely is not documented as equivalent, and the difference is a live campaign either way.
- Read `age_from` and `age_to` as birth years in the Persian calendar. Passing an age in years selects a birth cohort from the first century of that calendar and matches nobody, or matches the wrong cohort.

## `country`

Each `params` element carries `bank`, an optional `pre` operator prefix, `province_id`, `county_id`, `city_id`, `gender`, `age_from`, `age_to`, and the `mci`, `irancell` and `other` window objects. The `start` and `size` semantics and the Persian-calendar year rule are the same as `postal_code`.

## `geolocation` — Country V2

| Field | Shape |
|---|---|
| `province_id`, `county_id`, `city_id` | integer |
| `pre` | string operator prefix, for example `"912"` |
| `gender` | integer |
| `from_age`, `to_age` | integer, Persian-calendar birth years |
| `operator` | array of `{start, size, id}` |

- The field names differ from `country`: this mode uses `from_age` and `to_age`, and it replaces the three named operator objects with one `operator` array. Copying a `country` payload into `geolocation` produces a request with no age filter and no operator window.
- The Country V2 documentation shows `sending_type: "geolocation"` in the request body while one parameter table still says `country`. Send the request-body value, `geolocation`, and treat the table row as a documentation defect until a committed fixture proves otherwise. `[source: rendered documentation, read: unverified as of 2026-07-27]`

## `job`

Each `params` element carries `main_category_id`, `sub_category_id`, and an `operator` array of `{start, size, id}`.

Operator ids given by the documentation: `1` for MCI, `2` for Irancell, `13` for others. `[source: rendered documentation, read: unverified as of 2026-07-27]` The `geolocation` and `job` modes share this id set; `postal_code` and `country` name the same operators as object keys instead.

## Response

Every mode here returns the standard `data`/`meta` envelope described in `references/10-send-contract.md`. The outbox ids identify the batch, not the recipients, so the audience a campaign actually reached is only visible in the panel's reports. Record the exact `params` you sent alongside the outbox ids, because the payload is the only local evidence of who was targeted.
