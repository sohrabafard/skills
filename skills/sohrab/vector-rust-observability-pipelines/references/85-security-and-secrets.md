# Secrets, redaction, and the config trust boundary

Verified against Vector `0.57.0` on 2026-07-30. Trust-boundary review for a new
destination or a new credential path belongs to `/alaa-security-review`
(`$alaa-security-review`); this file states how Vector expresses the decision.

## Rule 1 — a credential's only interpolation site is never format-unconstrained

**The defect is not interpolation. It is a credential whose only interpolation site
is format-unconstrained**, because that is the one shape in which a disabled opt-in
fails silently.

**Vector 0.57.0 disabled environment-variable interpolation by default**, and the
resulting failure mode depends entirely on what else the config interpolates. A
config whose *only* `${VAR}` is a password:

```yaml
auth:
  strategy: basic
  password: ${CLICKHOUSE_PASSWORD}
```

validates clean on 0.57.0 **and validates identically whether or not the opt-in is
set**. Observed, `vector validate --skip-healthchecks` on a `clickhouse` sink with a
literal endpoint and only the password interpolated:

```
no opt-in set                                   -> Validated, EXIT=0
VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true,
  CLICKHOUSE_PASSWORD=hunter2                   -> Validated, EXIT=0
```

Any string is a valid password, so neither the type system nor the validation step
objects, and the first case then authenticates with the literal 22-character string
`${CLICKHOUSE_PASSWORD}`. The pipeline appears configured, appears validated, and
cannot connect. **The two runs are indistinguishable, so no validate step built on
this config can tell a working credential from a placeholder.**

Add one **format-constrained** interpolated value to the same config and the whole
config stops loading instead:

```
endpoint: "${CLICKHOUSE_ENDPOINT}"  and  password: "${CLICKHOUSE_PASSWORD}"
  -> x invalid uri character   in `sinks.clickhouse_events_raw`
  EXIT=78, with and without the environment variables set
```

Observed on `timberio/vector:0.57.0-alpine`, digest
`sha256:19e3526faf4d4b1ed0c28a0d68d4cc3a1e13e437099986a5b7a768707907497c`, build
`0.57.0 (x86_64-unknown-linux-musl 8832452 2026-07-14 20:58:30)`, 2026-08-08. The
endpoint must parse as a URI, `${...}` does not, and the load aborts before any
credential is used. **The failure is loud, and it is loud because a format-
constrained value shares the config.** A password alone stays silent.

### The rule

**Prefer a `secret:` backend.** Where an environment variable is genuinely the only
available source — infrastructure that may be handed over as nothing but a
connection string, where a backend would have to be provisioned identically on every
deployment path — interpolation is a legitimate choice, provided all three hold:

1. **The opt-in is set on every command that reads the config** — the running
   `vector`, `vector validate`, and `vector test` each take it independently. One
   command left without it is a gate that cannot see the defect it gates.
2. **At least one format-constrained interpolated value shares the config, and a
   standing gate keeps it there.** An endpoint, URI, port, or duration interpolated
   alongside the credential is the tripwire that converts the silent failure into a
   loud one. A config that interpolates *only* credentials has no tripwire and does
   not meet this rule.

   The tripwire is a property of an unrelated field, so **a future edit deletes it
   without touching the credential and without any symptom** — hard-code the endpoint,
   and condition 3's check silently stops discriminating. This is therefore not a
   one-time check: the CI gate in condition 3 is what enforces it, and **removing the
   tripwire must fail that gate**. Whoever removes it either restores one or moves the
   config to a `secret:` backend.

3. **A standing CI gate proves the opt-in is load-bearing, using the discriminating
   pair.** One run is never sufficient. Require **both**, on every pipeline run:

   | Run | Required result |
   | --- | --- |
   | `vector validate --skip-healthchecks` with **no** opt-in | exit **78**, and the diagnostic must be the interpolation failure — for a URI-valued tripwire, `invalid uri character` |
   | the same command **with** the opt-in and real values | exit **0** |

   **Both halves, and the diagnostic check, are load-bearing.** Exit 78 is reachable
   for reasons that have nothing to do with interpolation: a stale `api.graphql` key
   produces `unknown field 'graphql'` and exit 78 on every run, with and without the
   opt-in, which is exactly what an unguarded gate reads as success. If the two runs
   produce the same result, every conclusion drawn from the pair is void. A validate
   step that exports an empty value first, or that never runs without the opt-in,
   reports the same result for a working credential and a literal placeholder.

Deployment-layer sourcing is where the security benefit is obtained under this
option: the variable comes from a secret object rather than a mounted configuration
object. That is a platform decision, not a Vector one — `/alaa-k8s-helm`
(`$alaa-k8s-helm`), and `/alaa-security-review` (`$alaa-security-review`) for whether
the resulting trust boundary is acceptable.

**Use a secret backend where nothing forces the other choice.** Declare it once and
reference it:

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

The opt-in that condition 1 requires is
`--dangerously-allow-env-var-interpolation` or
`VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true`. **Upstream's "dangerously"
is not decoration:** interpolation splices the value in verbatim, including
characters that change the config's structure, so an attacker-influenced variable
can alter the shape of the config and not only one field's value. That risk is
unchanged by conditions 1 to 3 — they make a *disabled* opt-in loud, and do nothing
about a *hostile* value. The old `--disable-env-var-interpolation` flag and
`VECTOR_DISABLE_ENV_VAR_INTERPOLATION` were removed in 0.57.0, so a runbook carrying
either will fail.

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
