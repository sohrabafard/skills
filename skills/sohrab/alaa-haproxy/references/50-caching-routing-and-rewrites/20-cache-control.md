# Cache-Control emission

## Emitting `Cache-Control`

```
http-response set-header Cache-Control "<value from the policy>" if <condition>
```

**The trap: `path` is a request sample.** Writing the condition directly against `path` in an
`http-response` rule makes HAProxy warn

```
acl 'is_hashed_asset' will never match because it only involves keywords
that are incompatible with 'frontend http-response header rule'
```

and the header is then never set. The config is valid, the process starts, and the caching policy
silently did not apply. Capture the decision during the request phase into a transaction variable
and test the variable in the response phase:

```
acl is_hashed_asset path_reg "^${HAPROXY_ASSET_PREFIX}/.+\.[0-9a-fA-F]{8,}\.[a-z0-9]+\$"
http-request  set-var(txn.hashed_asset) bool(true) if is_hashed_asset
http-response set-header Cache-Control "${HAPROXY_HASHED_ASSET_CACHE_CONTROL}" if { var(txn.hashed_asset) -m bool }
```

Inside double quotes a bare `$` starts an environment-variable reference, so a regex anchor is
written `\$`. A regex needing no expansion uses single quotes instead.

`set-header` replaces any value the origin sent; `add-header` appends a second one and leaves the
cache to choose. For a response header that is a policy statement, `set-header` is the form,
because two `Cache-Control` headers is undefined behaviour spread across every intermediary.

Distinguishing HTML from a hashed asset is the whole job: an HTML document must not inherit the
immutable policy that applies to hashed assets, or a deploy is invisible to every client that has
the old document until its own `max-age` expires.
