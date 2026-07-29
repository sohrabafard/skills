# Observability — the Vue binding

**`/alaa-observability-soc` (`$alaa-observability-soc`) owns the signal model, the instrumentation gates,
the requirement level for each signal, and the review gates.** **`/alaa-services-contract`
(`$alaa-services-contract`) owns every name** — event names, field names, header names, metric names. This
file states only what a Vue component, composable, or adapter may emit, and where, and it invents no name.

Read it before deleting a `console.log`, adding an error handler, attaching a header in an interceptor, or
handing an error to Notify or Dialog.

## Deleting a `console.log` is a telemetry decision

`30-clean-code-solid-vue.md` says delete dead code and stale logs. That rule does not mean "remove the
telemetry and ship". A `console.log` is usually somebody's only visibility into a path, and removing it
without a replacement makes the next failure on that path silent.

The binding: **when a change removes a `console.*` call that was covering a real failure path, the same
change installs the replacement signal, or reports that no signal channel exists.** A debug log left over
from local development, on a path that already reports its failures, is deleted with no replacement — and
saying which of the two it was is part of the finding.

`console.log` is not the telemetry channel. It is invisible in production, it is not sampled, it is not
correlated, and anything logged through it can be read by any script on the page.

## What each layer may emit

| Layer | May emit | Never emits |
|---|---|---|
| Presentational component | nothing; it emits Vue events to its host | any telemetry call |
| Container component or page | a user-intent event, through the app's reporting facade | a raw transport error |
| Composable | the failure it classified, once, at the point it stops retrying or gives up | a log per render or per watcher tick |
| Transport adapter / HTTP client | request-scoped signals: outcome, duration, correlation identifier | the request body, the token, the response payload |
| Global error handler | anything unhandled that reached it | a duplicate of what a layer below already reported |

**One failure produces one report.** A composable that reports, a page that reports the same thing, and a
global handler that reports it again produce three events for one incident, which makes the volume useless
and the rate alarms wrong.

## The error boundary

An application has a top-level `app.config.errorHandler` and, where a subtree can fail independently, an
`onErrorCaptured` boundary around that subtree. A boundary does three things and no more: it renders a
degraded UI the user can act on, it reports once through the app's reporting facade, and it does not
swallow the error silently.

An `onErrorCaptured` that returns `false` without reporting is a swallowed error, and the symptom is a blank
region of a page with nothing anywhere to explain it.

Vue's error handler does not catch a rejected promise from an `await` inside an event handler. Those are
`70-async-and-failure-binding.md`'s classified failures, and they are reported there.

## Correlation identifiers

A correlation identifier is attached in **one place**: the HTTP facade or its interceptor chain
(`43-behavioral-patterns.md`, Chain of Responsibility). It is not attached per call site, because a per-call
site attachment is missing from exactly the call site nobody remembered.

The binding: the same identifier that goes out on the request is the one included in whatever the frontend
reports about that request's failure, so a browser-side report and a server-side trace can be joined. The
header name, the identifier format, and whether the client generates it or echoes one are
`/alaa-services-contract` (`$alaa-services-contract`) and
`/alaa-observability-soc` (`$alaa-observability-soc`). Do not choose them here.

## What must never be in a frontend signal

A token, a session cookie value, a password field, a full request or response body, a permission bitmap, a
national id, a phone number, or an email address. Report an identifier and a code; the payload is already
on the server side of the same request.

Redaction happens before the report is constructed, not inside the reporting facade as an afterthought — a
redactor applied at the end has to know every shape it might receive, and it does not.

## Sentry, profiling, sampling, and alerting

Whether Sentry is enabled, its sampling rates, profiling, and every alert and burn-rate rule are
`/alaa-observability-soc` (`$alaa-observability-soc`). This skill's only requirement is structural: the
application reports through **one facade module**, so that turning reporting on, off, or down is a change to
one file rather than a search across the codebase.
