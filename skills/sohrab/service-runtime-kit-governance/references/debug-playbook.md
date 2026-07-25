# Debug Playbook

Use when a runtime path is failing and the cause is not yet located. Work the stages in order; each removes a class of cause the later stages would otherwise chase.

## 1. Fix the ownership class first

Run the classification in `SKILL.md` "Ownership Model" before diagnosing. A wrong class produces a fix in the wrong layer that rerender then discards.

## 2. Confirm the expected kit source

- inspect `runtime/runtime-kit.env` for the pin and fetch settings
- inspect `scripts/runtime/ensure-runtime-kit.sh` for the resolution order compiled into the copied wrapper
- determine which source the wrapper actually resolved: `change-routing.md` owns the supported sources and the `SERVICE_RUNTIME_KIT_PREFER_SHARED_PARENT` rule, `runtime-contract-map.md` owns the staleness check

## 3. Regenerate before trusting any generated output

Do not treat a generated file as current until `bash scripts/runtime/render-runtime.sh` and then `bash scripts/runtime/validate-runtime.sh` have both exited `0`. A non-zero exit from either means the generated tree does not reflect the current `.env` and runtime contract: fix the input the failure names, then rerun both before continuing. Any conclusion drawn from a generated file before both exit `0` is unsound.

## 4. Read the layer that matches the symptom

- **App cannot reach Redis in containers.** Compare generated `REDIS_RUNTIME_*` values against the service `.env`; the host-side/container-side split is deliberate.
- **Worker cannot authenticate to RabbitMQ.** Confirm which naming variant the service config expects, then verify the generated env block exports both.
- **RabbitMQ vhost `/` wrong only from Windows Git Bash.** Read `windows-git-bash-compose.md` before touching `config/queue.php` or queue driver code.
- **Worker crashes because the queue does not exist.** Confirm `QUEUE_CONNECTION`, the declared queue names, and that generated RabbitMQ bootstrap ran before the worker began polling.
- **Render still reproduces a bug already fixed in the shared kit.** Suspect stale copied wrappers or a stale repo-local `.service-runtime-kit` cache; `runtime-contract-map.md` has the check.
- **Service logs not visible in Docker.** `runtime-contract-map.md` owns the logging-visibility rule; apply it there rather than forcing a shared override.
- **Octane logs or traces stay buffered in SigNoz.** Confirm the generated **app** env block carries the Octane request-recycling variable, and the generated **common** env block carries the OTEL scheduled-flush, flush-on-operation, and OTLP/BSP/BLRP export-timeout variables. A variable missing from the block that carries it is a shared `service-runtime-kit` fix, never a hand edit to generated Compose. This skill owns only which block carries which variable; `alaa-observability-soc` (`$alaa-observability-soc`) owns the telemetry contract and every value in it.
- **A corrected `.env` still appears ignored.** Rerender, then check whether the generated file reads `.env` directly or a default from `runtime/service.runtime.env`.

## 5. Re-run the original failing path

A successful rerender is not evidence the reported failure is gone. Re-run the exact bootstrap or runtime command that failed, and report that command's result rather than the render result.
