# The `_FILE` convention

Open this procedure when implementing or auditing the container entrypoint file contract. The source route is in [the Docker topic map](../../00-topic-map.md).

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
