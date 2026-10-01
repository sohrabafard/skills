# Migration from 3.2 to 3.3

## 3.2 to 3.3: deprecations and breaking changes

Confirmed 2026-07-29 against `https://www.haproxy.com/blog/announcing-haproxy-3-3`.

Breaking - these fail startup or change behaviour after an upgrade:

- The minimum Linux kernel rises to **4.17**.
- The `program` section is **removed** (deprecated in 3.1).
- Duplicate names across `frontend`, `backend`, `listen`, `defaults` and `log-forward` are now
  errors, as are duplicate `server` names within a backend. This makes naming every `defaults`
  section cheap: a collision is caught at startup rather than resolved silently.
- `http-send-name-header` may no longer overwrite `connection`, `content-length`, `host` or
  `transfer-encoding`.
- Multiple match types after `-m` in an ACL are no longer allowed.
- Email alerts now require the Lua implementation to be enabled. Lua work in HAProxy is owned by
  `/alaa-haproxy-lua`.
- `no-quic` is renamed `tune.quic.listen`.
- **The default load-balancing algorithm becomes `random`** when `balance` is absent. Every
  backend in this skill's examples states `balance` explicitly for this reason.
- **`mode http` backends default to `option abortonclose`**, which changes what happens to an
  in-flight request when the client disconnects.

Deprecated - these warn now and will be removed:

- the `master-worker` global directive, replaced by the `-W` or `-Ws` command-line argument
- `tune.quic.frontend.*`, replaced by `tune.quic.fe.*`
- `dispatch` and `option transparent`
