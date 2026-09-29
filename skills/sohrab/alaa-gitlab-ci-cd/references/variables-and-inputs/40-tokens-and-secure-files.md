# Tokens and secure files

Open this guide when using job identity tokens, secret fetches or secure files. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## `id_tokens:`, `secrets:` and secure files

```yaml
deploy:
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  secrets:
    DB_PASSWORD:
      vault: production/db/password@ops
      token: $VAULT_ID_TOKEN
      file: false
  script:
    - ./scripts/deploy.sh
```

- `id_tokens:` mints a short-lived JWT per job, with the audience the provider
  expects. Each token gets its own variable name.
- `secrets:` fetches the value with that token and exposes it. `file: true`
  writes it to a temp file and sets the variable to the path; `file: false` sets
  the value directly.
- `CI_JOB_JWT` and `CI_JOB_JWT_V2` are removed and return `401 Unauthorized`.

**Secure files** are the platform feature for a credential that is a file by
nature — a keystore, a signing key, a provisioning profile. Download them in the
job with `glab securefile`, which also verifies the checksum. The older
`download-secure-files` tool was deprecated in GitLab 18.6.
