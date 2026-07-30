# Secrets, redaction, and the config trust boundary

Verified against Vector `0.57.0` on 2026-07-30. Trust-boundary review for a new
destination or a new credential path belongs to `/alaa-security-review`
(`$alaa-security-review`); this file states how Vector expresses the decision.

## Rule 1 — credentials never come from `${VAR}` interpolation

**Vector 0.57.0 disabled environment-variable interpolation by default, and the
resulting failure is fail-open.** A config containing:

```yaml
auth:
  strategy: basic
  user: ${CLICKHOUSE_USER}
  password: ${CLICKHOUSE_PASSWORD}
```

passes `vector validate` with exit 0 on 0.57.0 — observed directly — and then
authenticates with the literal 22-character string `${CLICKHOUSE_PASSWORD}`. Any
string is a valid password, so nothing in the type system or the validation step
objects. The pipeline appears configured, appears validated, and cannot connect.

The same change fails **loudly** wherever the value has to satisfy a format:
`endpoint: ${CH_ENDPOINT}` produces `x invalid uri character` and exit 78. So the
breakage is silent precisely where the value is a secret, and noisy where it is not.
That asymmetry is why this gets its own rule rather than a line in an upgrade note.

**Use a secret backend.** Declare it once and reference it:

```yaml
secret:
  clickhouse:
    type: exec
    command: ["/usr/local/bin/fetch-clickhouse-secret"]

sinks:
  out_clickhouse:
    auth:
      strategy: basic
      user: "SECRET[clickhouse.user]"
      password: "SECRET[clickhouse.password]"
```

Verified: this validates on 0.57.0, and the backend command is **not executed
during `vector validate`** — so validation stays safe to run in CI, and a missing
backend does not turn into an accidental credential fetch.

If an environment variable genuinely is the only available source, then
interpolation must be re-enabled explicitly with
`--dangerously-allow-env-var-interpolation` or
`VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true`, **on every command that
reads the config** — `vector`, `vector validate`, and `vector test` each take the
flag. The flag is named "dangerously" by upstream because interpolation splices the
value in verbatim, including characters that change the config's structure. The old
`--disable-env-var-interpolation` flag and `VECTOR_DISABLE_ENV_VAR_INTERPOLATION`
were removed in 0.57.0, so a runbook carrying either will fail.

**Also deprecated in 0.57.0:** `${VAR}` and `SECRET[backend.key]` placeholders in
*structural* positions of a config — as a key, or where a block is expected — will
be removed in a future release. Keep placeholders in value positions only.

## Rule 2 — templated routing identifiers carry a literal prefix

Vector 0.57.0 confines every routing template: object keys, file paths, HTTP header
values, and table or stream names. The rendered value must stay inside the literal
prefix the template declares.

```
table: "{{ tenant }}"        -> rejected at startup, exit 78
table: "logs_{{ tenant }}"   -> accepted
```

This is a security control. Its purpose is to stop an attacker-influenced event
field from redirecting a write, and it is the mitigation that pairs with the
ClickHouse SQL-injection fix in the same release, where `database` and `table`
became server-side `Identifier` query parameters instead of client-side escaped
strings.

`dangerously_allow_unconfined_template_resolution: true` disables confinement for a
sink and sets `vector_security_confinement_disabled{component_type=...}` to `1`.
Treat that metric being `1` as an open finding with an owner, not a configuration
choice. Runtime confinement failures increment
`component_errors_total{error_type="confinement_failed"}`.

**Minimum version for any pipeline with a templated `database` or `table` is
0.57.0.** Below it, the identifier is an injection surface and confinement does not
exist to bound it.

## Rule 3 — redaction is a named field list, not an example

`.token` alone is an example. A redaction step must enumerate every field the
sources can carry that must not reach a destination:

```coffee
for_each(["token", "password", "authorization", "api_key", "secret", "set_cookie"]) -> |_i, field| {
  current = get(., [field]) ?? null
  if current != null {
    . = set!(., [field], "[REDACTED]")
  }
}
```

Two ownership boundaries, and this skill owns neither:

- **What must never be logged** is `/alaa-observability-soc`
  (`$alaa-observability-soc`): *"Secrets, credentials, tokens, session values, raw
  PII, unrestricted payloads, and customer-private content never enter logs, span
  attributes, metric labels, alert annotations, Sentry contexts, or SOC exports.
  Emit a stable internal reference an authorised human can resolve in the source
  system instead."*
- **The field names themselves** are `/alaa-services-contract`
  (`$alaa-services-contract`).

Redact in the pipeline as defence in depth, never as the primary control: an event
that should not contain a secret should not have been emitted with one. Place the
redaction transform **before** any fanout, so no sink can receive the unredacted
form.

`skip_unknown_fields` interacts with this badly. It silently discards fields the
destination table does not declare, which means a field you believed was being
redacted may simply have been dropped at one destination and delivered at another.
See `40-clickhouse-sink.md`.

## Rule 4 — the config file is itself a secret-bearing artifact

- `vector validate` output can echo config content in diagnostics. Do not paste
  validation output from a config with inlined credentials into a ticket.
- With a `secret:` backend, the config file contains references rather than values,
  so it is safe to commit. That is the second reason to prefer it over
  interpolation.
- Vector's observability API (`vector top`, `vector tap`) exposes event contents.
  `vector tap` on a pre-redaction component shows unredacted events. Bind the API
  to localhost and treat access to it as equivalent to log-read access.
- On tenancy: all tenants report into one shared SigNoz and everyone with access is
  authorised to see every tenant's telemetry, because seeing it is how they fix it.
  Sensitive projects get a separate SigNoz address selected by an environment
  variable. So per-tenant redaction is not the isolation mechanism — address
  selection is. See `40-clickhouse-sink.md`.

## TLS

Set `tls.verify_certificate: true` explicitly on every network sink. It is the
value you want and stating it makes a later change reviewable rather than invisible.
