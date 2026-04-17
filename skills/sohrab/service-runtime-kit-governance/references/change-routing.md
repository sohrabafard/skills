# Change Routing

Use this reference when the main question is where a runtime-related change should land.

## Fast Routing Table

| Request type | Correct layer | Edit here first | Do not start here |
|---|---|---|---|
| Change one service's normal app env such as `APP_NAME`, `APP_ENV`, `APP_DEBUG`, `LOG_CHANNEL`, DB credentials, RabbitMQ credentials, Redis host, or direct app ports | Service repo app env | `.env` | generated compose or generated shell files |
| Change one service's runtime naming, image fallback, runtime toggles, PgBouncer mode, worker defaults, alias defaults, or kit-consumed fallbacks | Service repo runtime contract | `runtime/service.runtime.env` | generated compose or generated shell files |
| Change runtime-kit pin, kit source, auto-fetch behavior, or sibling-kit preference | Service repo bootstrap contract | `runtime/runtime-kit.env` and copied `scripts/runtime/*.sh` when needed | generated wrappers |
| Change secret bundle shape or secret source env names | Service repo secret contract | `runtime/secret-files.env` | generated secret helper scripts |
| Add service-only env lines for app, worker, or scheduler | Service repo runtime extras | `runtime/env.*.extra` | generated compose |
| Add service-specific provisioning or migration logic | Service repo hooks | `runtime/hooks/**` | generated `scripts/docker/*.sh` |
| Change generated compose structure, generated shell behavior, generated Octane or PgBouncer files, render or validate logic, repo-support seeding, `.gitattributes` management, `.githooks`, or copied helper scripts for all services | Shared runtime kit | sibling `service-runtime-kit` repo | generated outputs in the service repo |
| Change GitLab CI, Helm, Kubernetes, or OpenShift deployment behavior | Deployment layer | `service-ci-kit` or deploy files | `service-runtime-kit` or generated runtime files |

## Practical Examples

### Edit the service repo contract or `.env`

Use service-owned files when the request is already supported by configuration.

Examples:

- `Expose the app on another host port for this service.`
- `Disable app host publishing by setting APP_PORT=null.`
- `Run this service without PgBouncer by setting pgbouncer_mode=off.`
- `Use LOG_CHANNEL=stderr in this service so Docker logs are visible.`
- `Rename the queue consumed by this service worker.`
- `Add one more worker-only env line.`
- `Run extra SQL or shell logic before or after DB provisioning.`

### Edit the sibling `service-runtime-kit` repo

Use the kit repo when the request changes the generator itself or the copied bootstrap support shared by many repos.

Examples:

- `Add another generated helper script for every service.`
- `Change how generated RabbitMQ bootstrap works.`
- `Teach the renderer a new runtime contract variable.`
- `Change how render validates required .env values.`
- `Seed runtime starter files into every adopted service.`
- `Manage BOM and LF behavior through copied .gitattributes and git hooks.`

### Route away to deployment tooling

Do not push deployment concerns into local runtime generation.

Examples:

- `Mount a Kubernetes secret into the app pod.`
- `Change Helm values or templates.`
- `Adjust GitLab pipeline deploy jobs.`
- `Change OpenShift deployment strategy or RBAC.`

## Mandatory Regenerate Workflow

After any service-owned runtime change:

```bash
bash scripts/runtime/render-runtime.sh
bash scripts/runtime/validate-runtime.sh
```

After any shared runtime-kit change:

1. update the sibling `service-runtime-kit` repo
2. refresh copied wrappers or bump the kit ref in the service when needed
3. regenerate and validate in the service repo

## Bootstrap Troubleshooting

If the service wrappers cannot locate the kit, use one of the supported sources instead of patching generated files by hand.

Supported sources, in practice:

1. `SERVICE_RUNTIME_KIT_DIR`
2. `./.service-runtime-kit`
3. `../service-runtime-kit`
4. archive download based on `runtime/runtime-kit.env`

Current shared behavior detail:

- when `SERVICE_RUNTIME_KIT_PREFER_SHARED_PARENT=true`, a valid sibling `../service-runtime-kit` should win over a stale repo-local `.service-runtime-kit` cache

## Ownership Reminder

If another tool or agent points you at a generated runtime file first, stop and re-route the task through the ownership model above.
