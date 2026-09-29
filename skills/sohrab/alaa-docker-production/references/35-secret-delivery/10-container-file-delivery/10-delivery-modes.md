# Secret delivery modes

Open this procedure when deciding whether runtime credentials must use file mounts. The source route is in [the Docker topic map](../../00-topic-map.md).

## 1. Why `environment:` is not secret delivery

An environment variable set on a container is readable by:

- anyone who can run `docker inspect` on the container, which is anyone in the `docker` group and
  therefore anyone with effective root on the host;
- any process in the same container, through `/proc/<pid>/environ`;
- any child process, because the environment is inherited — including a crash handler, a profiler,
  or a `phpinfo()` page;
- most error reporters by default, which serialise the environment into the report.

None of that requires a compromise. It is the normal behaviour of the mechanism. So:

**A runtime secret is delivered as a file mount, read by the process at start, with mode `0400` and
owned by the runtime user. An `environment:` entry is permitted only for a value that is not a
secret.** Where a file mount is genuinely unavailable, the value takes `${VAR:?message}` with no
default and the merge request names the constraint that prevented the file mount.

This replaces the older fleet sentence "secrets via env/secret manager", which endorsed the delivery
path that leaks.

## 2. The two modes, and which applies

`service-runtime-kit` switches on `RUNTIME_SECRET_FILES_ENABLED` (`render-runtime.sh:1173`), whose
tracked default is `false` (`contracts/service.runtime.env.example:112`).

| Mode | Compose | Swarm | Applies when |
|---|---|---|---|
| Secret files **on** | `secrets:` backed by `file: ./docker/.local-secrets/*` | `secrets:` with `external: true` | Always, in any environment that is not a developer's laptop. This is the correct default for production and Swarm. |
| Secret files **off** | every credential is an `environment:` entry | same | A local development stack where every credential is a known-bad placeholder and the host is the developer's own. |

With secret files on, the app receives `APP_KEY_FILE: /run/secrets/app_key` plus the Passport key
paths (`render-runtime.sh:1174-1176`) and no `APP_KEY` variable at all.

The decision rule with an observable condition: **if the value would still be a credential after the
stack is destroyed, secret files are on.** A placeholder that only opens a throwaway local database
is not; anything that reaches a shared host, a shared broker or a shared database is.
