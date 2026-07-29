# SSR, hydration, store and concurrency notes

Read this when the annotated code branches on an SSR flag, runs in a lifecycle hook, reads or writes a
store, or starts work that can be cancelled or fired twice.

**This file does not state SSR law.** What is true about SSR, hydration and lifecycle belongs to
`/alaa-frontend-developer` (`$alaa-frontend-developer`); Quasar's SSR discriminator, boot-file order and
platform modes belong to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`); double-fire and abort
correctness belongs to `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`),
`references/76-load-and-concurrency-binding.md`. This file states only which annotation those facts get.

## `SSR NOTE:`

**Where a module reads `window`, `document`, `localStorage`, `sessionStorage`, `navigator` or `IndexedDB`
inside a path that can run during server render, annotate the guard with `SSR NOTE:` naming the API and the
reason the guard exists.** Annotate the guard, not the API call, because the guard is what a later refactor
deletes.

**Where a module holds state at module scope that is written during a request, annotate the declaration
with `SSR NOTE:` stating whether the value is request-scoped.** A module global written per request is
shared across every concurrent request on the server.

Do not restate the Quasar flag that discriminates server from client. Name it and cite
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`); the flag is one repository setting away from
changing and this skill would then hold a stale copy.

## `HYDRATION NOTE:`

**Where a render path reads `Date`, `Math.random`, `window`, a locale-dependent formatter, or a
timezone-dependent value, annotate that line with `HYDRATION NOTE:` naming the value that must be identical
on server and client.** Naming the value is the point: "must be identical on server and client" alone does
not tell the next agent what to compare.

**Where behavior is deliberately deferred to after mount — a measurement, a viewport read, an observer —
annotate it with `HYDRATION NOTE:` stating that it is post-mount and what would break if it moved earlier.**

## `STORE NOTE:`

Annotate a store action with `STORE NOTE:` when any of these is true, and state the specific fact, not the
category:

- the action's result is replaced by hydration, so a value written before hydration is lost
- the action must run after another action, and the ordering is not visible at the call site
- the action is called from a boot file or a router guard, so it runs before the component tree exists
- the state it writes is read by a module that does not import it

State how state is injected, hydrated or replaced in the concrete terms of this store. "Explains cross-file
assumptions" is not an annotation; "`STORE NOTE:` replaced wholesale by the SSR payload on first client
render; a value written in a boot file before hydration does not survive" is.

## Concurrency: annotate the assumption, never the fix

**Where an exported function starts work that can be cancelled, annotate it with the abort owner: which
caller owns the `AbortController` and what happens to a resolved-after-abort response.** Where a handler
can fire twice — a double click, a repeated route enter, a retried submit — annotate whether the second
call is idempotent, deduplicated, or a defect.

If the annotation would have to say "the second call is a defect", that is a repair, and this pass does not
repair. Report it naming `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) and leave
the code alone.

## The run-phase line

Every exported fetch wrapper carries `runs: server`, `runs: client` or `runs: both` in its JSDoc block. A
wrapper without that line is a finding. Auth assumptions carried by that wrapper are not written here —
they are `AUTH NOTE:` and they carry a verification date:
`references/40-security-and-trust-annotations.md`.

## Observability facts a comment states

A comment that explains what a log line means, what a metric counts, or which trace attribute correlates
two requests states a fact owned by `/alaa-observability-soc` (`$alaa-observability-soc`). Cite it; do not
define the metric here. A comment naming a metric or field name is also quoting a contract value, so the
cross-service citation rule in `references/40-security-and-trust-annotations.md` applies.
