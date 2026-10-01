# Maps and preprocessor

Open this procedure when the task matches its trigger. The topic map routes to this file.

For current version-sensitive claims, follow the dated [source ledger](../SOURCES.md).

## Native samples, conditions and headers

Choose a native fetch by evaluation phase and output type, then an explicit ACL
matcher/converter. Missing headers and failed conversions are not valid identities.
Test absence, duplicates, empty strings and malformed input. Capture request
choices in `txn` variables when response rules need them; request-only fetches
cannot match there.

Normalize only according to the URI/header contract: decoding twice, changing
case on case-sensitive paths, or discarding query parameters can change routing.
Use `hdr_cnt`/the appropriate fetch when duplicate security headers must be
rejected. `set-header` replaces copies; `add-header` appends deliberately.
`option forwardfor` alone does not establish a trustworthy forwarding chain.
For identity/tenant selection, obtain the trust and shared-name contract from
`/alaa-trust-gateway-auth` and `/alaa-services-contract` before writing conditions.
Examples 11 and 18 state the upstream trust prerequisite. `unique-id` requires
`unique-id-format`; an unset format does not generate a correlation identifier.

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

## DNS and server discovery

Example 06 uses `resolvers`, `server-template`, `init-addr none` and `check`.
Templates bound address slots rather than allowing unlimited membership.
`init-addr none` tolerates missing initial DNS but can start with no usable server.
Verify resolver reachability, answer size/family, SRV versus A/AAAA semantics, and
actual template range. `hold valid` controls valid-resolution reuse; other `hold`
states and resolve/retry timeouts govern failure/recovery. Diagnose the failed
state before raising hold times: longer holds can delay convergence. Inspect
`show resolvers` and `show servers state`, then test empty/truncated answers,
missing names, address churn and DNS recovery. Configuration manual section 5.3
owns exact state/timer interactions; delivery owns nameserver wiring.
