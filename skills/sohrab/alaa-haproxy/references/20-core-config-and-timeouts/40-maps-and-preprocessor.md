# Maps and preprocessor

Open this procedure when the task matches its trigger. The topic map routes to this file.

For current version-sensitive claims, follow the dated [source ledger](../SOURCES.md).

## Maps instead of ACL chains

Maps centralize routing data; lookup cost depends on the match method and data.
Do not promise constant time or choose a universal entry-count threshold. Use a map
when it simplifies ownership, then measure representative keys and worst-case
patterns. The branch manual documents matcher-dependent indexing:
https://docs.haproxy.org/3.4/configuration.html#7.3.1-map. Queue-timeout fallback:
https://docs.haproxy.org/3.4/configuration.html#4.2-timeout%20queue.

A map is loaded at startup and is not re-read when the file changes. A live change is `add map`,
`del map` or `set map` on the Runtime API and is lost on restart unless the file is updated too.
Complexity budgets in general are decided by `/alaa-algorithms-data-structures`.

## Environment variables and the preprocessor

HAProxy expands `${NAME}` in the config file, and `${NAME-default}` supplies a default. Both work
only when the whole argument is enclosed in double quotes; unquoted, `bind :${PORT-8443}` is
parsed as a port offset and fails. `"${NAME[*]}"` splits the value on spaces into separate
arguments, which is what a list-valued setting such as `compression type` needs.

**An unset variable with no default expands to nothing and produces a parse error at
`haproxy -c -f` time.** That is the fail-closed shape and it is why a value that must be supplied
gets no default.

For a value whose absence must produce a message rather than a parse error, use the preprocessor:

```
.if !defined(HAPROXY_ASSET_PREFIX)
.alert "HAPROXY_ASSET_PREFIX is not set. It is decided by alaa-frontend-devops."
.endif
```

`.if` also takes `defined(NAME)`, `feature(NAME)` for a build option and `version_atleast(X.Y)`
for a branch test, with `.elif`, `.else` and `.endif`. `version_atleast` is how one file serves a
mixed estate.

Which variable name expresses a given runtime value, when the config is generated rather than
written, is decided by `/service-runtime-kit-governance`. The
`HAPROXY_*` names in this skill's examples are this skill's own convention for standalone configs.
