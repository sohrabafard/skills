# Compose file-backed secrets

Open this procedure when declaring file-backed secrets in Compose. The source route is in [the Docker topic map](../../00-topic-map.md).

For current or version-sensitive claims, follow the [source map](../../00-source-map.md).

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
      - source: db_password
        target: db_password

secrets:
  app_key:
    file: ./docker/.local-secrets/app_key
  db_password:
    file: ./docker/.local-secrets/db_password
```

- Compose file-backed secrets are bind mounts at `/run/secrets/<target>`; the source
  remains on the host filesystem. Do not claim Swarm tmpfs guarantees for this path.
- Compose ignores `uid`, `gid` and `mode` for a file source. Protect the host source
  with ownership and permissions appropriate to the runtime UID, and verify effective
  access inside the container. If the filesystem cannot enforce this, block secret
  delivery until a supported secure mount is available. See the [Compose secrets
  reference](https://docs.docker.com/reference/compose-file/services/#secrets), read 2026-09-29.
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
