# Defaults association

Open this procedure when the task matches its trigger. The topic map routes to this file.

For current version-sensitive claims, follow the dated [source ledger](../SOURCES.md).

## The `defaults` association rule

**A `defaults` section applies only to the proxies that follow it, up to the next `defaults`
section, or to the proxies that name it with `from`. It is never file-wide.**

Four consequences, all of which cost a production incident when the rule is not known:

1. A `frontend`, `backend` or `listen` with no `from` inherits the **nearest preceding**
   `defaults`. A `defaults` further up the file has already been superseded.
2. A `defaults` section does not implicitly inherit from another `defaults` section. Each one
   conveys only what it directly specifies. Explicit inheritance is written `defaults b from a`.
3. A `defaults` section can be named, and a proxy selects it with `frontend fe from base`,
   `backend be from base` or `listen l from base`. Naming works on 3.2, 3.3 and 3.4.
4. From 3.3, a duplicate `defaults` **name** is a startup error. Naming is therefore cheap: the
   collision that naming could introduce is caught by the parser.

**The rule for this skill: any config file that declares a `defaults` section names every one of
them and gives every `frontend`, `backend` and `listen` an explicit `from`.** A file that
declares no `defaults` at all is exempt, because there is nothing to associate. Positional
association is not forbidden by HAProxy and it is forbidden here, because it cannot be reviewed:
the reader has to hold the whole file in their head to know which block governs a proxy.
`scripts/check_defaults_scope.py` reports a violation.

### Why this is the rule and not a preference

Composing two configs is the normal way to build one. Take a file whose `defaults` sets
`mode http`, `timeout client 30s`, `option forwardfor` and `retries 3`, append a second file
whose `defaults` sets `mode tcp` and `timeout client 1m`, and the result **parses, starts and
serves traffic**, while every proxy after the second `defaults` silently runs in TCP mode, with
different timeouts, and with no `option forwardfor`. Nothing warns.

Observed with a real binary:

```
$ haproxy -c -f concatenated.cfg
[ALERT] config : http frontend 'fe_a' (concatenated.cfg:8) tries to use incompatible
        tcp backend 'be_a' (concatenated.cfg:22) as its default backend (see 'mode').
```

That is the loud case, and it only happens when the mode mismatch crosses a `default_backend`
edge. The quiet case is the dangerous one: a `defaults`-level `http-request del-header`, a
`timeout http-request`, an `option forwardfor` or a `retries` value that an agent adds to the
`defaults` it can see at the top of the file, believing it now applies to the proxy it is
protecting, when a second `defaults` further down has already taken over. The header keeps
arriving, the timeout keeps being the wrong one, and the config is valid.

Worked example, both halves in one file, with each proxy stating its own defaults:

```
defaults http_edge
  mode http
  timeout connect 5s
  timeout client 30s
  timeout server 30s
  option forwardfor

defaults tcp_l4
  mode tcp
  timeout connect 5s
  timeout client 1m
  timeout server 1m

frontend fe_web from http_edge     # forwardfor applies here
  bind :8080
  default_backend be_web

frontend fe_db from tcp_l4         # and not here, visibly
  bind :3306
  default_backend be_db
```
