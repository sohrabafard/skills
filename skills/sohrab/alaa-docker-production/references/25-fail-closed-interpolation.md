# The fail-closed interpolation invariant, and the fleet safety-control register

Open this file before any change to a Compose or Swarm stack file, and before any change to a
generator that emits one.

This skill owns this invariant for Compose authorship. `/alaa-frontend-devops`
(`$alaa-frontend-devops`) states it as a configuration gate on the frontend runtime container at
its `references/15-build-time-vs-runtime-config.md:26-36` and routes authorship here; this file
states it as the authorship rule for every Compose file in the fleet and does not restate the
frontend gate.

The checker is `scripts/check-compose-interpolation.mjs`. Its rule ids are the section names below.

---

## 1. Three forms, one decision

| Form | Meaning | When it is correct |
|---|---|---|
| `${VAR:?message}` | Compose refuses to render and prints `message` when `VAR` is unset **or empty**. | The value must come from outside this file. |
| `${VAR:-default}` | `default` is used when `VAR` is unset or empty. | The default is correct in production. Writing this form asserts that. |
| `${VAR}` or `$VAR` | Empty string when unset. | Never, in a production-shaped file. |
| `${VAR?message}`, `${VAR-default}` | Colon-less: an empty value counts as *set*. | Never. `VAR=` in the shell defeats them. |
| `${VAR:+alt}`, `${VAR+alt}` | Alternate value when set. | Not used in this fleet; allowlist it in a `--register` file if a real case appears. |

The decision is one question, and it is not about whether a value happens to be present in your
shell: **if this variable were unset on a manager node with a clean environment, would the
deployment come up with a control turned off?** If yes, `:?` with no default. If no, `:-default`
and the default is a real production value.

The forms are the documented Compose set
(https://docs.docker.com/reference/compose-file/interpolation/, checked 2026-07-29).

## 2. What Compose interpolation actually reads

Interpolation reads, in precedence order: the shell environment of the process running
`docker compose`; the file named by `--env-file`; and, when `--env-file` is not given, the `.env`
file in the project directory
(https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/, checked
2026-07-29).

**It never reads a service's `env_file:` key.** That key is a list of files whose contents are
injected into the container's environment at run time, after the file has already been rendered.
This is the source of the most confusing failure in this area: a Compose file with
`env_file: [.env]` and `DB_PASSWORD: ${DB_PASSWORD:-}` renders `DB_PASSWORD` empty in the *Compose
model* even though `.env` contains the password, and then the container also receives the real
`DB_PASSWORD` from `env_file`, so the explicit `environment:` entry overwrites it with empty. The
generated files in this fleet carry both keys on the same service
(`service-runtime-kit` `render-runtime.sh:1307-1310` and the rendered
`docker-compose.yml`), which is why this is written down rather than left to be rediscovered.

Two consequences that change what you do:

- A wrapper that invokes Compose must pass `--env-file`, or run with the project directory as the
  working directory so the `.env` is found. `service-runtime-kit/scripts/up-local.sh:85-87` aborts
  before touching Docker when the file is missing, and only the exact string `true` in
  `ALLOW_NO_ENV_FILE` bypasses it. That guard is correct and any wrapper written under this skill
  reproduces it.
- `docker compose config` renders interpolation, so it is the command that shows what will actually
  deploy. `docker compose config --no-interpolate` shows the file as written. Compare the two when
  a value is not what you expected.

## 3. The two grep traps

Anyone hand-searching for violations hits both of these within a minute.

**Trap 1: `$$` escapes.** `$$` is a literal `$` to Compose. `$${HOME}` reaches the container as
`${HOME}` and is expanded by the container's shell, not by Compose. `$$(date)` likewise. Both are
legitimate and frequent — an nginx template, a shell `-c` command, a literal price string. Counting
matters: an **odd** number of `$` characters before `{` means escaped, an **even** number means
interpolated, so `$$${VAR}` *is* interpolated (two dollars become one literal, the third opens a
substitution).

**Trap 2: comments.** Compose parses YAML, and YAML drops comments before Compose interpolates
anything. A `$VAR` written in a comment is never substituted and is never a finding. Both a
whole-line comment and a trailing `# ...` outside quotes count.

`service-runtime-kit/scripts/validate-runtime.sh:82,88-96` handles both, and the checker in this
skill ports that logic and extends it to trailing comments. The fixture
`scripts/fixtures/compose/escapes.compose.yml` is six lines that a naive grep reports as six
violations and that are all correct.

## 4. The register: variables for which `:-` is a defect regardless of syntax

This is the artifact this skill exists to hold. The syntactic half of the invariant — "every
substitution carries `:?` or `:-`" — is already enforced by
`service-runtime-kit/scripts/validate-runtime.sh:73-118`, and it passes a Swarm stack file
containing `DB_PASSWORD: ${DB_PASSWORD:-}` and
`DB_PROVISION_ADMIN_PASSWORD: ${DB_PROVISION_ADMIN_PASSWORD:-postgres}`. The semantic half needs a
judgment about *which* variable is a safety control, and that judgment lives here.

Membership in this register **overrides any tracked default the generator carries**. If
`service-runtime-kit-governance` records `RABBITMQ_PASSWORD_DEFAULT=app` as the tracked default,
that is a statement about the generator's contract; the interpolation form written into the Compose
file is still `${RABBITMQ_PASSWORD:?...}`, because the form is this skill's call.

### 4.1 How to read an entry, and how to add one

Every entry states **why a wrong default for that variable is a production defect**, because a
register nobody can extend goes stale on the first new variable. To decide whether a variable you
are looking at belongs here, answer the entry-shaped question: *name the production state that
results from the default being used, and say why no metric or probe in this fleet would report it.*
If you can answer both halves, it is a register member; write the entry.

Two classes, because "a default would silently disable a safety control" has two shapes.

- **Class A — no default is ever correct.** The value cannot be invented by the file that uses it.
  Any `:-` form is a violation, including `:-` with an empty default.
- **Class B — the default is the disabling value.** The variable may legitimately carry a default,
  and the defect is the specific default that turns the control off. A class-B variable with a real
  restrictive default is not a finding.

The machine-readable form of the register, used by the checker, is
`scripts/lib/safety-controls.mjs`. When the two disagree, this file is the specification and that
file is the defect. The `id` values match.

### 4.2 Class A — no default permitted

| id | Matches | Why a default is a production defect |
|---|---|---|
| `sc-password` | `*_PASSWORD`, `*_PASSWD`, `*_PASS` | The file becomes a credential source. A service that forgot to set the variable authenticates with whatever the file says instead of failing to start. The empty default is the worst case, not the mildest: PostgreSQL under `trust` or `md5` and RabbitMQ both accept an empty password from a client that offers one, so the stack comes up, every probe is green, and no credential is in play. |
| `sc-secret` | `*_SECRET`, `SECRET_*` | A signing, encryption or authentication secret. The moment the file is committed, the default is published; every environment that forgets to override it then shares one attacker-known secret, and the compromise is invisible because every request using it is valid. |
| `sc-token` | `*_TOKEN` | A bearer credential presented to another system. The default is either an invalid token that fails at the first outbound call in production — long after deploy, so the rollout looks successful — or a real token committed to the repository. |
| `sc-key` | `APP_KEY`, `*_PRIVATE_KEY`, `*_PUBLIC_KEY`, `*_API_KEY`, `*_ACCESS_KEY`, `*_SECRET_KEY`, `*_SIGNING_KEY`, `*_ENCRYPTION_KEY`, `*_KEYFILE`, `*_KEY_PATH` | Key material. `APP_KEY` is the canonical case: with a defaulted `APP_KEY` every environment can decrypt every other environment's cookies and encrypted columns, and correcting it later is a data-loss event rather than a configuration change, because everything encrypted under the wrong key becomes unreadable. |
| `sc-credentials` | `*_CREDENTIALS`, `*_DSN`, `*_CONNECTION_STRING` | A compound value with a credential inside it. Defaulting it hides the credential from every review and every grep that looks for `PASSWORD` or `SECRET`. |
| `sc-admin-password` | `DB_PROVISION_ADMIN_PASSWORD`, `POSTGRES_PASSWORD`, `MYSQL_ROOT_PASSWORD`, `RABBITMQ_DEFAULT_PASS`, `REDIS_PASSWORD` | A superuser credential for shared infrastructure. Named explicitly because the vendor images accept a well-known default: the container starts, the port answers, and the superuser account has the password every scanner on the internet tries first. In this fleet the same variable is also written as `POSTGRES_PASSWORD` on the shared Postgres container (`render-runtime.sh:325` and the rendered `docker-compose.yml:399`), so one default sets the superuser password for every service on the host. |

### 4.3 Class B — the default must not be the disabling value

| id | Matches | Disabling defaults | Why it is a safety control |
|---|---|---|---|
| `sc-tls-verification` | `*VERIFY_PEER*`, `*TLS_VERIFY*`, `*SSL_VERIFY*`, `*CERT_VERIFY*` | `false`, `0`, `off`, `no`, `none`, empty | Turning verification off converts every TLS connection into an unauthenticated encrypted channel. The connection still succeeds, the latency is unchanged, and no probe or dashboard in this fleet reports it. |
| `sc-insecure-flag` | `*INSECURE*`, `*SKIP_VERIFY*`, `*DISABLE_AUTH*`, `*DISABLE_TLS*`, `*NO_VERIFY*` | `true`, `1`, `on`, `yes` | A negatively worded control: the disabling value is the true one. The habit that "a `false` default is the safe one" is inverted here, which is exactly why reviewers miss it. |
| `sc-auth-toggle` | `*AUTH_ENABLED`, `*AUTH_REQUIRED`, `REQUIRE_AUTH*`, `*SIGNATURE_REQUIRED`, `*AUTHORIZATION_ENABLED` | `false`, `0`, `off`, `no`, empty | The switch that decides whether requests are authenticated at all. A service with authentication off answers every caller, emits no error, and is indistinguishable from a healthy service in every metric collected. |
| `sc-size-cap` | `*MAX_UPLOAD*`, `*UPLOAD_MAX*`, `*MAX_BODY*`, `*BODY_LIMIT*`, `*MAX_REQUEST_SIZE*`, `*MAX_FILE_SIZE*`, `*CLIENT_MAX_BODY*` | `0`, empty, `-1`, `unlimited`, `none` | Nginx, HAProxy, PHP and most brokers read `0` or empty as "no limit". The number that looks safest is the one that removes the control, and the failure mode is a single request exhausting a node's memory. |
| `sc-rate-limit` | `*RATE_LIMIT*`, `*THROTTLE*`, `*MAX_ATTEMPTS*`, `*MAX_CONCURRENC*`, `*MAX_CONNECTIONS*`, `*PIDS_LIMIT*` | `0`, empty, `-1`, `unlimited`, `none`, `false` | A rate, concurrency or process cap that stops one caller or one bug consuming the node. Zero and empty mean unlimited in every implementation this fleet uses. Why a given limit exists and what shape it takes is `/alaa-reliability-sla` (`$alaa-reliability-sla`)'s decision; that it must not silently be absent is this skill's. |
| `sc-allowlist` | `ALLOWED_ORIGINS`, `ALLOWED_HOSTS`, `CORS_ALLOWED*`, `TRUSTED_PROXIES`, `TRUSTED_HOSTS`, `ALLOWED_IPS` | `*`, `**`, `0.0.0.0/0`, empty, `all`, `any` | The wildcard accepts everything. `TRUSTED_PROXIES` is the sharpest case: a wildcard makes every client-supplied `X-Forwarded-For` authoritative, so an IP allowlist anywhere else in the system becomes an attacker-controlled value. |
| `sc-debug` | `APP_DEBUG`, `DEBUG`, `DEBUGBAR_ENABLED`, `TELESCOPE_ENABLED` | `true`, `1`, `on`, `yes` | Laravel with `APP_DEBUG=true` renders the stack trace, the environment and the database connection parameters into the body of an HTTP 500. The result is an information-disclosure endpoint that only appears when something is already going wrong, which is when it is least likely to be noticed. |

Threat classification for anything not on this list — whether a newly named variable is a security
control at all, and what class of threat it belongs to — is `/alaa-security-review`
(`$alaa-security-review`)'s decision. The discriminating question this programme uses: *when this
dependency cannot answer, does proceeding without it let something through that must not get
through?* If yes, it is fail-closed and belongs here. If the answer is instead about availability —
proceeding degraded rather than not at all — that is `/alaa-reliability-sla`
(`$alaa-reliability-sla`)'s ground and the variable is not a register member.

### 4.4 Adding an entry

Three ways, in order of preference.

1. **Edit the register.** Add a row to §4.2 or §4.3 above with the "why" written out, and the
   matching object to `scripts/lib/safety-controls.mjs` with the same `id`. This is the right answer
   for anything that recurs across services.
2. **A project register file**, for a variable that is one service's own:
   ```json
   { "entries": [
     { "id": "sc-comment-webhook-hmac", "class": "A",
       "pattern": "^COMMENT_WEBHOOK_HMAC$",
       "why": "Signs outbound webhook bodies. A default means every receiver accepts a body this service never sent." }
   ] }
   ```
   ```
   node scripts/check-compose-interpolation.mjs --register runtime/safety-controls.json docker-compose.yml
   ```
3. **In the Compose file itself**, when the variable exists in one file only:
   ```yaml
   # safety-control: COMMENT_WEBHOOK_HMAC — signs outbound webhook bodies; a default means every receiver accepts a forged body
   COMMENT_WEBHOOK_HMAC: ${COMMENT_WEBHOOK_HMAC:?set the webhook signing secret in the service .env}
   ```
   An in-file declaration is class A, because a variable worth declaring by hand is one whose value
   must come from outside the file.

### 4.5 Waiving an entry

A waiver is a written argument, not a silencer. It sits on the line immediately above the finding
and states a reason:

```yaml
# safety-control-waiver: LOCAL_ONLY_TOKEN reason=fixture value; this file is never deployed
LOCAL_ONLY_TOKEN: ${LOCAL_ONLY_TOKEN:-fixture}
```

A waiver with no `reason=` is itself a finding (`waiver-without-reason`). Waivers are legitimate in
exactly two places: a fixture file that is never deployed, and a development-only Compose file
where the value is a known-bad placeholder and the file carries no production path. A waiver in
`docker-compose.yml` or `docker-compose.swarm.yml` is a defect being renamed.

## 5. Correcting a violation

Do not simply change `:-` to `:?`. The variable now has to reach the process that runs Compose, and
the three places it can come from are the shell, `--env-file`, and the project `.env`. The
correction is therefore three edits, and skipping any one of them turns a silent misconfiguration
into a failed deploy — which is better, but not the goal:

1. Change the Compose form: `${DB_PASSWORD:?DB_PASSWORD must come from the service .env}`. The
   message is read by a human at 3am; make it name the file to edit, not the variable they can
   already see.
2. Make the value required where it is produced. In this fleet that is
   `service-runtime-kit`'s `validate_service_env` (`render-runtime.sh:91-145`), which today requires
   `DB_USERNAME` and does not require `DB_PASSWORD`. Adding a `require_env_value` there is
   `/service-runtime-kit-governance` (`$service-runtime-kit-governance`)'s change; naming it as
   required is this skill's finding.
3. Make the value present where it is consumed. For Swarm that means the credential is a Docker
   secret rather than an environment variable at all; see this skill's
   `references/35-secret-delivery.md`, which is the better answer for every class-A entry.

The end state for a class-A variable in a Swarm stack file is that it does not appear under
`environment:` in any form. `:?` is the correct interim state and the correct permanent state only
where a file mount is genuinely unavailable.

## 6. Current state of the fleet, 2026-07-29

Rendered from `service-runtime-kit` v2.3.0 using its own
`contracts/service.runtime.env.example`, then checked:

```
$ node scripts/check-compose-interpolation.mjs docker-compose.swarm.yml
docker-compose.swarm.yml:28: safety-control-default: DB_PASSWORD matches register entry sc-password; no default is permitted, write ${DB_PASSWORD:?…}.
docker-compose.swarm.yml:36: safety-control-default: RABBITMQ_PASSWORD matches register entry sc-password; no default is permitted, write ${RABBITMQ_PASSWORD:?…}.
...
docker-compose.swarm.yml:294: safety-control-default: DB_PROVISION_ADMIN_PASSWORD matches register entry sc-password; no default is permitted, write ${DB_PROVISION_ADMIN_PASSWORD:?…}.
11 finding(s)
```

`service-runtime-kit/scripts/validate-runtime.sh` returns `Runtime validation passed`, exit 0, on
the same file. That is not a bug in that checker: it enforces the syntactic half correctly and has
no register. The gap it leaves is the reason this file exists.

`APP_KEY` is the one credential the kit already writes fail-closed, at
`render-runtime.sh:1218,1312,1379,1655,1712`, and its message —
`APP_KEY is missing from the service .env; pass it with --env-file` — is the model for the messages
in §5.1: it names the file and the flag, not the variable.
