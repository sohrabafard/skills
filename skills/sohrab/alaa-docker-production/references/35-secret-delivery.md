# Secret delivery into a container

Open this file when a credential, key or token must reach a running container.

Which variables count as secrets, and what interpolation form they take when they must appear in a
Compose file at all, is this skill's `references/25-fail-closed-interpolation.md`. Getting a secret
into a *build* is a different mechanism entirely and is this skill's
`references/15-build-secrets-and-attestations.md`. Whether a particular value is a security control
and what threat class it belongs to is `/alaa-security-review` (`$alaa-security-review`)'s decision.

---

## 1. Why `environment:` is not secret delivery

An environment variable set on a container is readable by:

- anyone who can run `docker inspect` on the container, which is anyone in the `docker` group and
  therefore anyone with effective root on the host;
- any process in the same container, through `/proc/<pid>/environ`;
- any child process, because the environment is inherited — including a crash handler, a profiler,
  or a `phpinfo()` page;
- most error reporters by default, which serialise the environment into the report.

None of that requires a compromise. It is the normal behaviour of the mechanism. So:

**A runtime secret is delivered as a file mount, read by the process at start, with mode `0400` and
owned by the runtime user. An `environment:` entry is permitted only for a value that is not a
secret.** Where a file mount is genuinely unavailable, the value takes `${VAR:?message}` with no
default and the merge request names the constraint that prevented the file mount.

This replaces the older fleet sentence "secrets via env/secret manager", which endorsed the delivery
path that leaks.

## 2. The two modes, and which applies

`service-runtime-kit` switches on `RUNTIME_SECRET_FILES_ENABLED` (`render-runtime.sh:1173`), whose
tracked default is `false` (`contracts/service.runtime.env.example:112`).

| Mode | Compose | Swarm | Applies when |
|---|---|---|---|
| Secret files **on** | `secrets:` backed by `file: ./docker/.local-secrets/*` | `secrets:` with `external: true` | Always, in any environment that is not a developer's laptop. This is the correct default for production and Swarm. |
| Secret files **off** | every credential is an `environment:` entry | same | A local development stack where every credential is a known-bad placeholder and the host is the developer's own. |

With secret files on, the app receives `APP_KEY_FILE: /run/secrets/app_key` plus the Passport key
paths (`render-runtime.sh:1174-1176`) and no `APP_KEY` variable at all.

The decision rule with an observable condition: **if the value would still be a credential after the
stack is destroyed, secret files are on.** A placeholder that only opens a throwaway local database
is not; anything that reaches a shared host, a shared broker or a shared database is.

## 3. The `_FILE` convention

The container-side contract, implemented generically at
`service-runtime-kit/templates/generated/docker/octane/entrypoint.sh:33-36`: for every environment
variable whose name ends in `_FILE`, read the file it names and export the base name with the file's
contents.

```sh
# Contract, restated so it can be reimplemented for a non-PHP service.
# For each VAR_FILE in the environment:
#   1. the file must exist and be readable, or the entrypoint exits non-zero naming the path;
#   2. the value is the file contents with a single trailing newline removed and nothing else
#      trimmed, because a passphrase may legitimately begin or end with a space;
#   3. VAR is exported and VAR_FILE is unset, so the path does not leak into child processes;
#   4. if VAR is already set, the file wins and a warning names both sources, because two sources
#      for one credential is a configuration defect that must be visible.
```

Requirements on the entrypoint that implements it:

- It runs **before** `exec "$@"`. This is not a style point: `service-runtime-kit` sets `command:`
  on every worker (`render-runtime.sh:1248,1250-1253`), and the generated entrypoint runs
  `exec "$@"` at `:59-61` with its `APP_KEY` presence check at `:63-66`, after it. Every worker
  therefore bypasses that check. Any precondition check placed after `exec` protects nothing.
- It fails closed. A `_FILE` variable naming a path that does not exist is an exit, not a warning:
  the alternative is a container that starts with an empty credential.
- It does not log the value. Logging the *path* is useful; logging the contents puts the credential
  in the log driver, which has none of the protections the file mount had.

## 4. Compose: file-backed secrets

```yaml
services:
  platform-app-php:
    environment:
      APP_KEY_FILE: /run/secrets/app_key
      DB_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - source: app_key
        target: app_key
        uid: "1000"
        gid: "1000"
        mode: 0400
      - source: db_password
        target: db_password
        uid: "1000"
        gid: "1000"
        mode: 0400

secrets:
  app_key:
    file: ./docker/.local-secrets/app_key
  db_password:
    file: ./docker/.local-secrets/db_password
```

- The mount point is `/run/secrets/<target>` and `/run/secrets` is a tmpfs, so the contents are
  never written to the node's disk.
- `mode: 0400`, `uid` and `gid` matching the runtime user. The default is `0444`, world-readable
  inside the container.
- The source files live under a directory that `.dockerignore` excludes — `docker/.local-secrets`
  is on the required list in this skill's `references/10-dockerfile-authorship.md` — and that
  `.gitignore` excludes. A secret file committed to the repository is a rotation event.
- The generator materialises these files through
  `templates/generated/scripts/docker/ensure-local-secrets.sh`. That script's `chmod 600 "${dst}"
  || true` (`:51,118`) swallows the failure it exists to catch: on a filesystem where `chmod` is a
  no-op — a Windows bind mount, a mounted share — the file stays world-readable and the script
  reports success. The correct form is `chmod 600 "${dst}"` with no `|| true`, and the script exits
  non-zero when it fails. Replacing "validate permissions" with a specific mode and a specific
  failure behaviour is the point: "permissions" is not a checkable word.

## 5. Swarm: external secrets

```yaml
services:
  platform-app-php:
    secrets:
      - source: comment_app_key_v3
        target: app_key
        uid: "1000"
        gid: "1000"
        mode: 0400

secrets:
  comment_app_key_v3:
    external: true
```

- `external: true` means the secret already exists in the swarm and this file only references it.
  A `file:`-backed secret in a stack file reads the file from the manager node where the deploy runs,
  which makes the deploy depend on which machine ran it.
- `uid`, `gid` and `mode` are supported unconditionally by Swarm. They are absent from every secret
  the generator emits (`render-runtime.sh:1177` writes `source`/`target` only), so every secret in
  the fleet's Swarm stacks currently lands at `0444`. The container-side defence at
  `entrypoint.sh:51-57`, which `chmod 600`s the Passport keys, cannot help: a secret mount is
  read-only and `chmod` on it fails.
- Naming: `<service>_<purpose>_v<n>`. The version suffix is not decoration; see §6.

## 6. Rotation is a create-new-name operation

A Docker secret is immutable. `docker secret update` exists but changes only labels, not content.
Rotation is therefore:

```
# 1. create the new secret under a new name
printf '%s' "$NEW_VALUE" | docker secret create comment_app_key_v4 -

# 2. update the stack file: source: comment_app_key_v4, target unchanged
#    the target stays `app_key`, so no application code or env var changes

# 3. deploy, which is an ordinary rolling update
docker stack deploy -c docker-compose.swarm.yml --with-registry-auth comment

# 4. confirm no task references the old secret, then remove it
docker service inspect --format '{{range .Spec.TaskTemplate.ContainerSpec.Secrets}}{{.SecretName}} {{end}}' comment_platform-app-php
docker secret rm comment_app_key_v3
```

Two consequences worth stating because they are counter-intuitive:

- **Rotation is a deploy.** There is no way to change a secret's value under a running task. Plan it
  as a rollout, with the rollout control from this skill's `references/30-swarm-delivery.md`.
- **`APP_KEY` is not rotatable this way.** Changing a Laravel `APP_KEY` makes every value encrypted
  under the old key unreadable. Rotating it requires a re-encryption step in the application first,
  with both keys available. That is an application change, not a container change; the container
  side is only the last step.

Never rotate by editing the file a `file:`-backed secret points at while the stack is running: the
task keeps the content it was created with, so half the tasks hold the old value and half the new,
and which is which depends on when each task last restarted.

## 7. Key material with two parties

Where one service owns a private key and others consume the public key — Passport signing keys are
the fleet's case:

- The owning service mounts the private key at `0400`, owned by its runtime user.
- Every consumer mounts only the public key, at `0444`, and has no path to the private one.
- The public key is a `configs:` entry in Swarm, not a `secrets:` entry, because it is not secret
  and treating it as one makes rotation harder for no benefit.
- Generation happens before deploy, by a script, not by hand. A key pair generated by hand is a key
  pair nobody can regenerate identically.

## 8. What must never appear in `docker inspect`

Run this against any container before calling a secret change done:

```
docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' CONTAINER \
  | grep -Ei '(password|secret|token|key)=' \
  | grep -v '_FILE='
```

Empty output is the pass condition. A line ending `_FILE=/run/secrets/...` is correct — that is a
path, not a value. Any other match is a credential in the container config, readable by anyone with
Docker access, and is a finding regardless of how it got there.

For a Swarm service, the same question at the spec level:

```
docker service inspect --format '{{range .Spec.TaskTemplate.ContainerSpec.Env}}{{println .}}{{end}}' SERVICE
```

## 9. Checklist for a secret change

1. The value is delivered as a file, not an environment variable. (§1, §4, §5)
2. `uid`, `gid` and `mode: 0400` are set on every `secrets:` entry.
   `node scripts/check-stack-rollout.mjs` reports `secret-mode-missing` when they are not.
3. The container-side loader runs before `exec`, and exits non-zero when the file is missing. (§3)
4. The source file is excluded by `.dockerignore` and `.gitignore`. (§4)
5. The secret name carries a version suffix so rotation has somewhere to go. (§5, §6)
6. `docker inspect` shows no credential value. (§8)
7. If any credential still appears under `environment:`, it uses `${VAR:?message}` with no default
   and the merge request names the constraint that prevented a file mount. (this skill's
   `references/25-fail-closed-interpolation.md`)
