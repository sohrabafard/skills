# Topic Map

This is the only router in this skill. `SKILL.md` points here and carries no second table.

Each row states an observable condition. Match the condition, open that one file, and stop. Rows are grouped by register: **(a)** upstream tusd, **(b)** the browser client, **(c)** the Ala `tusd` service. When a row in (a) and a row in (c) both match, read both and say which half of the answer came from which; (c) wins inside the Ala repository.

## References

| You are about to… | Read | Register |
|---|---|---|
| assert a version, a flag name, a default value or an upstream behaviour, or you are unsure how old a fact in this skill is | `references/10-source-map.md` | all |
| touch the Ala `tusd` repository, or answer a question about how the Ala upload plane actually behaves | `references/15-ala-service.md` | (c) |
| choose between the tusd binary, the embedded library, one deployment or two, or you are about to propose custom code around tusd | `references/20-decision-matrix.md` | (a) + (c) |
| configure the tusd binary or construct `tusdhandler.NewHandler`, wire a storage backend, or reason about what upstream guarantees | `references/25-upstream-library.md` | (a) |
| lay out an upload plane end to end, place a relay or staging hop, or decide how it scales and locks | `references/30-topologies.md` | (a) + (c) |
| set a size cap, decide part sizes, size temp disk, define retention for unfinished uploads, build an object key, or explain why a finished object is not in the bucket yet | `references/35-storage-lifecycle.md` | (a) + (c) |
| decide who may create, resume, inspect, or terminate an upload; consume an `upload_to_*` permission bit; or design the durable ownership record | `references/40-authorization.md` | (c) |
| write, review or debug a hook, a callback or a lifecycle notification, or you need to state what happens when one fails | `references/45-hooks.md` | (a) + (c) |
| triage a live upload incident, or you need the symptom-to-cause table for a stall, a duplicate, a lost record or a wrong-tenant resume | `references/50-failure-modes.md` | all |
| add tests, or you must prove a change did not regress resume, authorization, size, retention or shutdown | `references/55-tests.md` | all |
| write or review browser upload code, choose `tus-js-client` options, or define the states the UI shows | `references/60-browser-client.md` | (b) |
| configure or debug the proxy, load balancer or gateway in front of an upload plane, including timeouts, buffering and URL rewriting | `references/70-front-door.md` | (a) + (c) |
| design logs, metrics, traces, alerts or SLOs for an upload plane, or you are correlating an upload across hops | `references/80-observability.md` | all |
| hit a protocol or runtime limit and need to know whether it is fixed, configurable, or a defect | `references/90-constraints.md` | (a) |

## Assets

Assets are starting points that carry this skill's protocol decisions. Adapt hostnames, credentials, TLS, timeouts and version pins; do not copy them unchanged into production.

| You are about to… | Use | Notes |
|---|---|---|
| write the browser upload composable, or fix resume matching, offline handling or retry timing | `assets/client/useTusUpload.ts` | reference implementation; imports only `vue`, `tus-js-client` and `./uploadStates` |
| name an upload state anywhere in client code, a store, a UI label or a telemetry field | `assets/client/uploadStates.ts` | the one canonical state list; every other file imports it |
| hold more than one upload on a screen, or keep progress alive across navigation | `assets/client/useUploadQueueStore.ts` | this skill owns only the tus-protocol fields; store shape belongs to the frontend skill |
| build the first upload UI, or show what the composable exposes | `assets/client/TusUploadPanel.vue` | example only; this skill owns nothing about component structure |
| send upload telemetry to Sentry or analytics without leaking a URL, a key or a filename | `assets/client/uploadTelemetry.ts` | redaction takes the base path as an argument; it hardcodes no route |
| register upload code in a Quasar app with SSR enabled | `assets/client/quasar.boot.uploads.ts` | client-only boot; boot convention belongs to the frontend skill |
| scrub upload material out of Sentry events before they leave the browser | `assets/client/quasar.boot.sentry.ts` | pass the same base path used by the app |
| exclude upload routes from a service worker, or wire the boot files into `quasar.config.ts` | `assets/client/quasar.config.snippet.ts` | PWA denylist is built from the app's base path |
| run the tusd binary against S3 or MinIO | `assets/docker-compose/tusd-s3.compose.yaml` | register (a); `-max-size` is mandatory and the image must be pinned by `TUSD_IMAGE` |
| run the tusd binary against local disk for staging and relay | `assets/docker-compose/tusd-staging.compose.yaml` | register (a); same two obligations |
| fill in the environment for either Compose file | `assets/env/tusd-s3.env.example`, `assets/env/tusd-staging.env.example` | `TUSD_IMAGE` is deliberately empty; take the pin from `references/10-source-map.md` |
| put HAProxy in front of tusd | `assets/haproxy/tusd-reverse-proxy.cfg` | read the `timeout client` note in `references/70-front-door.md` before shipping it |
| alert on an upload plane | `assets/prometheus/tusd-alert-rules.yml` | every threshold is a variable; set it from a measured baseline before enabling |
| persist the ownership record for an upload | `assets/schemas/upload-record.schema.json` | the machine form of the single record in `references/40-authorization.md` |
| finish a change to this skill | `scripts/validate_pack.py` | run `python3 scripts/validate_pack.py --root .` from the skill directory |
