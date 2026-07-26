# Failure Modes: Symptom, Diagnosis, Smallest Retry, Escalation

Each entry gives the symptom you observe, the diagnosis, the smallest retry that could resolve it, and what to escalate
when the retry does not. Exit-code meanings are in `references/command-surface.md`; severities are in
`references/catalog-workflow.md`. Escalation always means: stop, apply nothing further, and report the finding with its
context payload and the exact command that produced it.

## Exit `2` — `Configured source file not found: <path>`

The `source_root` in `catalog/services.json` is absolute and the sibling repository is not there, or an owner's
`source_path` is wrong. **Retry:** confirm the repository exists at `<source_root>/<owner_repo>/` and that
`source_path` names a committed file. For a `go_service_permission_map` owner the file may legitimately be absent and
the importer skips it, so this error on a Go owner means the shape is wrong, not the file. **Escalate:** name the
missing repository and the resolved path. Never edit `source_root` and never delete the service definition to make the
command pass.

## Exit `2` — an emitter refusal

`Cannot derive a valid Go package…`, `…cannot be emitted as a TypeScript identifier`, `…appears more than once in the
active catalog`, `…exceeds the client formatter print width of 80 columns`. The catalog holds data the emitter cannot
represent. **Retry:** fix the offending catalog value — shorten the key, correct it to `/^[a-z][a-z0-9_]*$/`, remove the
duplicate, or move the Go target into a directory whose name is a valid lowercase Go identifier. **Escalate:** when the
fix would change a published `permission_key`, because that is a rename — go to `references/lifecycle.md`, do not
shorten a live key in place.

## Strict drift fails **before** apply

Expected in two cases and a real defect otherwise.

- `AGGREGATE_CONSUMER_ARTIFACT_NOT_APPLIED` (warning) and `AGGREGATE_CONSUMER_MANUAL_EDIT` (error) fire because the
  consumer repository does not yet hold the newly generated file. **Retry:** none needed — this is the pre-apply state.
  Proceed to apply if the request authorizes it, then re-run `import` and `check-drift --strict`.
- `CONSUMER_PERMISSION_MISSING_FROM_AUTH` (error) after registering a new service: the catalog does not yet hold the
  permissions that service declares. **Retry:** add the entries with ids above the current maximum, regenerate.
- Any fatal — a duplicate id, a bit-index mismatch, a dangerous collision, a same-name split. **Retry:** correct
  `catalog/permissions.json`; never resolve a collision by reusing an id or remapping a consumer. **Escalate** a
  `DANGEROUS_BITMAP_COLLISION` you did not create: one id now maps to two names and deciding which name owns it is an
  ownership decision, not a fix.

## Strict drift fails **after** apply

A different situation with a different remedy: something is now wrong on disk in a service repository.

- `AGGREGATE_CONSUMER_MANUAL_EDIT` or `_STALE_METADATA` (error) — the applied file is not the generated file, or its
  count, max id, or fingerprint are stale. **Retry:** run `generate`, copy the generated file over the applied file, and
  re-run. Never hand-edit either file, and never patch the metadata constants.
- `_PERMISSION_MISSING`, `_PERMISSION_EXTRA`, `_BITMAP_ID_MISMATCH`, `_MAP_DESYNC`, `_IDENTIFIER_COLLISION`,
  `_MALFORMED` (fatal) — the applied artifact contradicts the catalog. **Retry:** the same regenerate-and-copy, once.
  **Escalate** if it recurs: a mismatch that survives a clean copy means the descriptor path and the generated path
  disagree, which produces no finding of its own — check the `generated_targets` prefix and `owner_repo` against
  `catalog/services.json` per `references/catalog-workflow.md`.
- `_PERMISSION_EXTRA` disappearing is the proof a retirement landed. See `references/lifecycle.md`.

## Applying would overwrite unrelated changes

The target file in the service repository differs from the last generated output in ways the catalog did not cause.
**Retry:** none. **Escalate:** stop before writing, report the diff, and ask. An apply is a controlled operation per
`/alaa-controlled-ops` (`$alaa-controlled-ops`); overwriting someone's uncommitted work is not recoverable from the
catalog.

## The service's bitmap semantics differ from the contract

A consumer decodes with a different bit order, a different padding rule, a different base, or a zero-based id.
**Retry:** none — do not adapt the catalog to the consumer. **Escalate:** report the divergence against
`references/shared-consumer-contract.md` and route the wire question to `/alaa-services-contract`
(`$alaa-services-contract`) and `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). Two decoders that disagree is a
security defect, not a formatting difference.

## Symptoms with no error at all — silent failures

These report success. Each is a case where a clean result means nothing.

- **A mistyped command or flag, or `--strict` on `import` or `summary`** — see `references/command-surface.md`.
  **Check:** make a new gate fail once, on purpose, and confirm exit `1`.
- **A `generated_targets` prefix or a descriptor path that disagrees with the entry** — see
  `references/catalog-workflow.md`. **Check:** the expected file exists under `generated/` with a moved mtime, and the
  applied path, the `source_path`, and the path inside `generated_targets` are one identical string.
- **`--generated=, `--catalog=`, and `--services=` are unconfined.** Each is concatenated onto the repository root as
  text, so `--generated=..` writes into sibling repositories and an absolute path is treated as relative. **Never pass
  any of the three unless the request names the path**, and never pass one to redirect output into a service repository;
  applying is a separate, authorized copy.
- **A corrupted or empty `permissions` array.** The tool substitutes the data imported from source repositories and
  reports clean, so a destroyed source of truth validates. **Check:** the entry count in
  `generated/reports/permission-catalog-summary.md` against `catalog/permissions.json` before trusting a clean run.
- **A report read straight after `generate`.** `generate` writes reports from findings computed before it ran, so the
  report describes the previous state. **Check:** run `check-drift` and read that report.
- **A reworded `notes` value.** Two fatal-to-info downgrades depend on free-text substrings in `notes`
  (`Phase 1.5 service extraction reallocation`, `Phase 2 comment canonicalization`). Rewording one turns an accepted
  finding back into a fatal one, and the wrong note on the wrong entry downgrades a genuine collision to info. **Check:**
  treat those substrings as code; never edit a `notes` value to improve its wording, and when a collision reports info,
  verify the downgrade was earned.
- **A stale committed artifact.** The tree under `generated/` is git-tracked and nothing checks freshness;
  `php tests/run.php` passes with stale output. **Check:** regenerate and confirm no file changed.

## Two frontend symptoms an agent will debug later

- *"The backend granted the permission but the UI still hides the control."* The token is an issuance-time snapshot; the
  hint updates on the next login, refresh, or reissuance. Correct behaviour, not a decoder defect.
- *"The decode returned nothing, so we logged the user out."* Wrong by construction — an empty set is a valid ready
  state. See `references/typescript-consumer.md`.
