# Store Adapter: Hindsight

Mechanics for the server-backed store. None of it is policy, and none of it survives a change of store.
Hindsight is a 0.x product on a roughly weekly release cadence, which is why it lives in this one file and not
in `SKILL.md`: a release can invalidate this page without touching a single rule elsewhere in the skill.

## Version pin

`hindsight-api` **0.8.6**, published 2026-07-29. Re-derive before trusting it, and expect it to have moved:

```bash
curl -s https://pypi.org/pypi/hindsight-api/json \
  | python3 -c "import json,sys;d=json.load(sys.stdin);v=d['info']['version'];print(v,d['releases'][v][0]['upload_time_iso_8601'])"
```

0.8.5 shipped 2026-07-22 and 0.8.6 seven days later, so a pin written from memory is usually one patch behind.
Cross-check against the vendored specification, whose `info.version` must agree with the pin:

```bash
python3 -c "import json;print(json.load(open('openapi.json'))['info']['version'])"
```

## Banks

One bank, `alaa-memory`. Every API path is bank-scoped and there is no cross-bank query, so a second bank
partitions knowledge permanently rather than organising it.

Leave the bank's display `name` unset. A narrator line derived from the bank name enters the extraction
prompt and pollutes entity attribution. 0.8.6 adds an explicit override — the request schema carries
`agent_name`, described as `Narrator override (memory owner) primed in the prompt.` — so the practice stands
but the reason is now "set the override, or set nothing", not "there is no override". The upstream discussion
issue commonly cited for this is closed; do not cite it as open.

## Ingest

```
POST /v1/default/banks/{bank_id}/memories
```

The request body carries `items`, and `items` is the only required field. Per item, only `content` is
required; the fields that matter here are `timestamp`, `tags`, `document_id`, `update_mode`,
`observation_scopes`, and `metadata`.

- `async` defaults to **false**, meaning the call waits for completion. Set it true only for bulk work where
  you will confirm the result separately.
- `document_tags` at the request level is **deprecated**; put tags on each item instead.
- `timestamp` accepts an ISO 8601 datetime, or omission (which defaults to now), or the literal string
  `"unset"` to store without any timestamp for timeless material. It records when the content *occurred*, not
  when it was sent.

Re-derive the whole shape rather than trusting this list:

```bash
python3 -c "import json;s=json.load(open('openapi.json'))['components']['schemas'];print(s['RetainRequest']['required'],list(s['MemoryItem']['properties']))"
```

## `document_id` is both the upsert key and the concurrency primitive

Providing a `document_id` upserts: an existing document with that ID, and all memories derived from it, are
deleted before the new content is processed. Omitting it assigns a random UUID per request, so re-ingesting
the same content creates duplicate memories.

Therefore: **every write from a script carries a deterministic `document_id`.** Derive it from the source
identity — the note permalink, the drift identifier, the repository path — never from a timestamp or a random
value. This is what makes an import re-runnable and what makes two agents writing the same knowledge converge
instead of duplicating. `update_mode` is `replace` by default, which reprocesses from scratch; `append`
concatenates onto the existing document and requires a `document_id`.

## Only tags are filterable at recall

`metadata` is stored and returned but is not a recall filter axis. A lifecycle field carried in `metadata` is
invisible to the query that needs it. This is the mechanical reason the drift registry stays in git — see
`references/drift-management.md`.

`tags_match` takes `any`, `all`, `any_strict`, `all_strict`, or `exact`, and the default is the trap:

- `any` (default) returns memories with at least one matching tag **plus every untagged memory**.
- `all` returns memories with every specified tag **plus every untagged memory**.
- `all_strict` returns memories with every specified tag and **excludes** untagged memories.

So a filtered recall that means "only the tagged ones" must pass `all_strict`. Using the default returns
effectively the whole bank, which reads as a working query returning irrelevant results rather than as an
error.

When a drift pointer is retained, encode the lifecycle in tags, not metadata: `drift` plus one of
`drift:open`, `drift:analyzed`, `drift:decided`, `drift:fixing`, `drift:resolved`. Recall it with both tags
and `all_strict`. Changing the lifecycle means re-retaining the document under the same `document_id`.

## Migrating history requires a custom import script

The official Claude Code and Codex plugins never send `timestamp`. A plugin-driven import therefore stamps
every historical record with the moment of import, which collapses the entire history into one instant. Since
supersession resolves conflicting statements by recency, a flattened history makes that resolution arbitrary:
the store can no longer tell which of two contradicting facts came later, and two machines' histories no
longer interleave correctly.

The import must be a script that sets `timestamp` per record from the source's own time — the note's
`last_verified`, or its session datetime — and sets `document_id` from the note permalink. The `document_id`
makes the import safely re-runnable, so a dry run followed by a real run is cheap.

Bulk import sequence:

1. Set `HINDSIGHT_API_ENABLE_AUTO_CONSOLIDATION=false` (default `true`, configurable per bank), so each
   retain does not trigger a consolidation pass.
2. Retain in batches with per-item timestamps and deterministic document IDs.
3. `POST /v1/default/banks/{bank_id}/consolidate` once. It accepts `observation_scopes` to consolidate only
   memories matching given tag combinations.
4. Re-enable auto-consolidation.

Keep the previous store as a read-only archive until the migrated bank has answered real questions correctly.
An import that has not been queried has not been verified.

## Security: both surfaces are open by default

This is the part that is not delegable. The API and the MCP endpoint ship unauthenticated — upstream states
that by default the MCP endpoint is open, no authentication required — and an unauthenticated memory service
reachable on a LAN is a trust boundary, not a convenience.

Mandatory before the service listens on anything:

```bash
export HINDSIGHT_API_TENANT_EXTENSION=hindsight_api.extensions.builtin.tenant:ApiKeyTenantExtension
export HINDSIGHT_API_TENANT_API_KEY=<key from the secret store, never a literal in a file>
```

Both default to unset, which means authentication is disabled. Clients then send `Authorization: Bearer` with
that key. Until both are set, bind to loopback only.

`HINDSIGHT_API_LLM_TRACE_ENABLED` defaults to **true**, and traced rows contain the full prompt and model
output, which may include sensitive memory content, retained for a day. That is a second copy of everything
the store has seen, in a local table, on by default. Set it `false` for normal operation; when it is needed
for debugging, bound it with `HINDSIGHT_API_LLM_TRACE_MAX_CHARS` and
`HINDSIGHT_API_LLM_TRACE_RETENTION_DAYS` and turn it off again afterwards.

`/alaa-security-review` (`$alaa-security-review`) owns the fail-closed doctrine and any exception to the two
rules above.

## Operational knobs, with defaults

| Variable | Default | Why it matters here |
|---|---|---|
| `HINDSIGHT_API_ENABLE_AUTO_CONSOLIDATION` | `true` | Turn off for bulk import, then consolidate once. |
| `HINDSIGHT_API_LLM_TRACE_ENABLED` | `true` | Writes full prompts locally; see above. |
| `HINDSIGHT_API_RETAIN_EXTRACTION_MODE` | `concise` | `chunks` stores chunks as-is at zero LLM cost, which is the right mode for archival import; a retain mission is ignored in that mode. Other values: `verbose`, `verbatim`, `custom`. |
| `HINDSIGHT_API_LLM_MAX_CONCURRENT` | `32` | Far too high for a shared local model server; upstream recommends `2` there. |
| `HINDSIGHT_API_RERANKER_MAX_CANDIDATES` | `300` | Caps rerank per recall; lowering it trades recall quality for latency. |

Re-derive any row:

```bash
grep -n "HINDSIGHT_API_ENABLE_AUTO_CONSOLIDATION" configuration.md
```

## Client timeouts

The client-side override `requestTimeoutSeconds` (environment variable `HINDSIGHT_REQUEST_TIMEOUT_SECONDS`)
defaults to `null`, meaning per-call defaults apply: **recall 10 s, retain 15 s**, knowledge tools 10–15 s.
The health check stays at 5 s regardless. Note the interaction with this skill's five-second recall budget:
the client will wait twice as long as the budget allows, so the budget has to be enforced by the agent
deciding to move on, not by the client timing out.

## Client integrations

A first-party Claude Code plugin exists and registers hooks on session start, prompt submit, stop, and session
end. For Codex CLI the documented gate is a feature flag, not a version: `~/.codex/config.toml` must contain
`codex_hooks = true` under `[features]`. No minimum Codex CLI version is stated in the integration or
changelog pages, so do not write one; check the flag instead.

## Vendored pack

Hindsight ships a first-party documentation pack whose `references/` tree carries the OpenAPI document, the
configuration page, and the per-endpoint pages that every claim above was checked against. If that pack is
vendored under `vendor/`, it is an upstream subtree and is never edited: this file owns the opinion and routes
into the pack for mechanics. The wrap-never-fork rule applies to it exactly as it applies to the pack behind
the current store.
