# Cache policy prerequisites

## When no policy has been given

**Emit no directive and ask for the policy.** Do not choose a default.

Every plausible default is wrong for at least one response class: `max-age=3600` is wrong for a
content-hashed asset (too short, and it forfeits the whole point of hashing), wrong for an HTML
document (too long, and a deploy does not take effect for an hour), and wrong for an authenticated
API response (it is a cache-poisoning surface). There is no value that is safe in the absence of
information about how the build names its files.

The mechanical form of "refuse rather than default" is the preprocessor:

```
.if !defined(HAPROXY_HASHED_ASSET_CACHE_CONTROL)
.alert "HAPROXY_HASHED_ASSET_CACHE_CONTROL is not set. alaa-frontend-devops decides it."
.endif
```

`.alert` makes `haproxy -c -f` fail with that message, so the missing policy is caught by the
gate register rather than discovered in production. A variable with no default achieves the same
outcome less legibly: it expands to nothing and produces a parse error naming the line.
