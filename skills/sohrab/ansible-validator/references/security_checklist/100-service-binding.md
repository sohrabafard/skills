# Security checklist: Service Binding

## S9. A service binds to an address, not to everything

**Predicate.** No default in a shipped role sets a bind address of `0.0.0.0`.

**Evaluate.**

```bash
grep -rn "0\.0\.0\.0" <target>
```

Read the result: a bind address of `0.0.0.0` in `defaults/main.yml` is a role
whose out-of-the-box behaviour is to listen on every interface, including the
one facing the internet. Default to `127.0.0.1` and make the wider bind an
explicit override.
