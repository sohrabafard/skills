# Mediana / IPPanel Edge — multipart and file sends

Read this when a CSV or XLSX file supplies the recipients or the per-recipient text: `file`, `peer_to_peer_file`, and `keyword`.

## Provenance

- Documentation repository: `https://github.com/ippanelcom/Edge-Document`
- Rendered documentation: `https://ippanelcom.github.io/Edge-Document/docs/`
- **read: unverified as of 2026-07-27.** No session that produced or revised this file had network access to those URLs.

Column names, accepted extensions, row limits and file-size limits are account-specific and are **unverified** here. Confirm them against the panel or a committed fixture before a first send, and record what you confirmed.

## The three modes

| `sending_type` | Content type | Required form fields | Optional | What the file supplies |
|---|---|---|---|---|
| `file` | `multipart/form-data` | `sending_type`, `from_number`, `message`, `files[]` | `other_recipients[]`, `send_time` | the recipient list |
| `peer_to_peer_file` | `multipart/form-data` | `sending_type`, `from_number`, `files[]` | `send_time` | one recipient and one message per row |
| `keyword` | `multipart/form-data` | `sending_type`, `from_number`, `message`, `files[]` | `send_time` | values for the placeholders in `message` |

`[source: rendered documentation, read: unverified as of 2026-07-27]`

Runnable curl commands for all three are in `references/20-examples-and-rejects.md`.

## Encoding rules

- Encode these three as `multipart/form-data` form fields, never as a JSON body. The API rejects a JSON body on a file mode, and the rejection names the missing file rather than the wrong content type, which sends debugging in the wrong direction.
- Send the file part under the literal field name `files[]`, including the brackets.
- Send `Accept: application/json` so the error path returns the same `data`/`meta` envelope as the JSON modes; without it an error may arrive as HTML that your parser reports as a malformed body.
- Repeat `other_recipients[]` once per extra recipient rather than sending a comma-joined string, because a joined string is accepted as one malformed recipient.
- Validate a multipart send in tests against a JSON-equivalent metadata object, then assert the form encoding separately. `scripts/validate_mediana_payload.py` checks the metadata only, and says so in its output.

## The `peer_to_peer_file` row contract

```csv
recipient,message
09123456789,Your appointment is confirmed for Sunday
09123456788,Your appointment is confirmed for Monday
```

- Normalise every recipient column value through `scripts/validate_mediana_payload.py --normalize` before the file is written, not after it is uploaded. A file is opaque to the request validator, so an unnormalised row fails at the vendor with no local signal.
- Reject the whole file when any row fails normalisation. A partial upload sends some messages and hides the rest, and there is no per-row rejection report to reconcile against.

## The `keyword` placeholder contract

- `message` carries placeholders in braces, for example `Your balance is {ex_C}`, and the uploaded file supplies a column per placeholder.
- Placeholder tokens are account-specific identifiers, not free text. Take them from the panel or from a committed fixture, and mark them `NEEDS_MEDIANA_CONFIRMATION` when neither exists, because an unknown placeholder is substituted as empty and the recipient receives a sentence with a gap.

## Before any file mode is sent

- Check that the file exists, that its extension is one the account accepts, that its size is under the account limit, and that its header row matches the mode's expected columns. Do all four before the request is built, because the vendor's rejection does not distinguish them.
- Generate an outreach file only from data the user named in this session, and write nothing else into it. A generated recipient list is a disclosure of the user base, and it is not recoverable once uploaded.
- Every file mode reaches many recipients at once, so the approval gate in `references/15-targeting-and-bulk-sends.md` applies to all three modes here as well.
