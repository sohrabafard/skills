# Designed Failure States

Read this file when designing what a surface shows when it does not have what it needs. Failure behaviour is a design deliverable with the same status as the happy path: a component shipped with only its success state is incomplete, not "done pending edge cases".

## The eight states every data-bearing surface designs

Each row states what the user must be able to tell from the screen without asking anyone.

| State | Entered when | The user must be able to tell |
|---|---|---|
| Loading | the request is in flight | that the system is working, and roughly on what |
| Empty | the request succeeded and returned zero rows | that there is nothing here yet, and the one action that would put something here |
| Partial | some fields or some rows resolved and others did not | which parts are real and which are missing |
| Stale | the displayed data is a cached copy older than its freshness budget | how old it is, and how to get a fresh copy |
| Error | the request failed and retrying might succeed | what failed, what to do next, and a reference they can quote |
| Not permitted | the capability is absent for this session | that this is about their access, not about the data or a bug |
| Offline | the browser reports no connectivity | that the failure is local, and what still works |
| Degraded | a dependency is up but not answering usefully | which part of the page is affected and which part is trustworthy |

**The distinguishability rule.** Empty, error, not-permitted and offline must be visually and textually distinguishable from each other on the same surface. Rendering all four as an empty region, a spinner that never resolves, or the same generic "no data" is the defect this table exists to prevent: the user's next action differs in all four cases, and a single presentation makes every one of them wrong.

*When the system enters each state* — timeout values, retry budgets, circuit-breaker posture, what "degraded" formally means — belongs to `/alaa-reliability-sla` (`$alaa-reliability-sla`). This file owns only what the surface shows once it is there.

## Permission-denied: the affordance decision

When a capability is absent for the current session, a control has exactly three possible treatments. Pick one deliberately, per control, and record the choice.

| Treatment | Use when | Never use when |
|---|---|---|
| **Hide** | the capability belongs to a role the user will never hold, and its visibility would only confuse (an admin-only section for an end user) | the user could plausibly gain the capability, or its absence would make the page look broken or incomplete |
| **Disable with a stated reason** | the user could gain the capability, or its absence needs explaining ("Available to course editors") | the reason cannot be stated without disclosing something the user should not learn |
| **Show and let the server answer** | the capability is expensive or ambiguous to determine client-side, or the check is genuinely per-item | the action is destructive or irreversible, where a predictable refusal beats an attempt |

Three standing rules:

1. **A disabled control always states why.** A control that is grey with no reason is indistinguishable from a bug and generates support load. Put the reason in a tooltip and in the accessible name, not in colour alone.
2. **Hiding a control is a presentation choice and never a security control.** The full statement of that rule, and what it means for flow design, is in `25-untrusted-content-and-ui-authority.md`; it is not restated here.
3. **An empty capability set is a legitimate ready state, not a broken session.** A user with no permissions sees a designed, explained surface — never a loading state that never resolves, and never an error.

The meaning of each permission bit is owned by `/alaa-services-contract` (`$alaa-services-contract`). The decoder that turns a token into a capability set is owned by `/alaa-permission-generator` (`$alaa-permission-generator`); on `client` it is consumed through `src/stores/authPermissions.ts`, which correctly documents every value as an unverified UI hint. Whether an action is actually allowed is owned by `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). This file cites all three and restates none.

## Stale data

A surface that can show cached data designs its staleness.

- Every cached surface has a **freshness budget** stated in its documentation: the age past which the copy is labelled stale. Pick it from how fast the underlying data actually changes, and write the number down.
- Inside the budget, show the data with no ornament. Past it, show the data with a visible age and a refresh affordance. Never silently show data older than its budget as though it were live.
- **Never blank a screen to refresh it.** Stale-while-revalidate is the default: keep the old content visible, mark it as refreshing, and swap when the new data lands. Replacing content with a skeleton the user has already read is a regression.
- A refresh that fails leaves the stale copy on screen with the failure stated. It never leaves an empty screen where readable data used to be.
- Values where staleness is dangerous — a balance, a quota, a permission, a live count — are labelled with their as-of time, always, not only when stale.

## Degraded dependency

- Degradation is **scoped to the surface that depends on it**. One failing panel shows its own failure; the rest of the page stays usable. A page-level error for a sidebar widget's failure is a design defect.
- A degraded surface says which capability is unavailable in the user's terms ("Comments are unavailable right now"), not which service is down.
- If a degraded dependency makes an action unsafe rather than merely unavailable, the action is disabled with its reason, not left clickable to fail later.
- The page never claims success it cannot verify. A write whose confirmation did not arrive shows "not confirmed", not a success toast.

## Offline

- Detect with the browser's own connectivity signal and confirm with a failed request; a reported-online browser behind a captive portal is the common case.
- State it once, at the page level, and mark the surfaces that cannot work. Do not put an offline banner on every card.
- Say what still works: cached reading, a draft that is saved locally, navigation that does not need the network.
- On reconnect, restore automatically and say so. Never require a manual reload to recover from a transient disconnection.

## Loading, with thresholds

Numbers, not adjectives.

- **Under 100 ms:** show nothing. A flash of a loading state is worse than no loading state.
- **100 ms to 300 ms:** the control that started the work shows in-place feedback (a pressed state, an inline spinner on the button). The page does not change.
- **Past 300 ms:** a skeleton in the content area, laid out to the same dimensions as the content it replaces so nothing shifts when it resolves.
- **Past 3 s:** state what is happening and, when the work is measurable, its progress ("Uploading video, 40%").
- **Past 10 s:** offer a way out — cancel, continue in the background, or notify me when it is done.
- A button that started async work disables itself and shows progress until the work settles, so a second submit is impossible by construction rather than by warning.

## Anti-patterns

- A spinner as the only failure design: it is indistinguishable from a hang.
- "No data" for an empty list, a failed request, and a forbidden resource alike.
- A greyed control with no reason.
- Blanking readable content to show a skeleton on refresh.
- A success toast fired on request dispatch rather than on confirmed response.
- An offline banner that appears on every card on the page.
- Designing the happy path and filing the rest as "error handling for later".

## Pairing

- The copy inside these states: `35-ux-writing-and-microcopy.md`
- The reference the user quotes from an error state: `28-ui-diagnosability.md`
- The authority rule behind hiding controls: `25-untrusted-content-and-ui-authority.md`
- Interaction states (hover, focus, disabled) as opposed to data states: `60-components-states-and-ux.md`
- Long lists, slow networks and concurrent edits: `65-lists-latency-and-concurrency.md`
- How these states are proven before delivery: `95-design-proofs.md`
