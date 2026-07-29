# UI Diagnosability

Read this file when designing an error surface, or when deciding what the interface should record about a failure. The question this file answers: **when a user reports "it did not work", can anyone find out what happened?**

Today's default answer on most surfaces is no. A toast that auto-dismisses in three to five seconds is the only channel a failure gets, and once it fades there is no artefact: the user cannot say what it said, and support cannot join it to anything on the server.

## The rule

**Every error a user can see and might report carries a correlation reference that is visible, copyable, and joinable to a server-side record.**

Three properties, each checkable:

- **Visible** — present in the error surface itself, not only in the console. A value that requires opening devtools does not exist for the person reporting the problem.
- **Copyable** — a copy affordance, or selectable text. Not an image, not a value inside a canvas, not truncated with an ellipsis. A reference the user has to transcribe by hand will be transcribed wrong.
- **Joinable** — the same value the request carried, so a support engineer can find the server-side record from it. Not a client-invented number with no counterpart.

`client` already emits the joinable value: `src/sdk/requestCorrelation.ts` attaches `X-Request-Id` to every SDK request and a W3C `traceparent` when a provider supplies one. The design gap is that no error surface shows it. **Surface what the transport already sends** rather than inventing a second identifier.

## Copy and presentation

The complement to the standing rule that error copy never shows a raw code alone: the cause and the fix are stated in the user's language, and the reference sits beside them as a secondary, quiet element.

- **Primary line:** what failed and what to do, in the user's terms.
- **Secondary element:** the reference, visually subordinate — smaller, muted, monospaced, with a copy affordance and a label the user can repeat to support.
- **Never make the reference the message.** A screen whose most prominent element is a hexadecimal string tells the user they have hit a bug rather than a situation.
- The reference is LTR content inside a Persian interface and takes an LTR island per `05-rtl-and-persian.md` section 4. `client`'s `src/auth/AuthErrorNotice.scss:45` already does this with `unicode-bidi: plaintext`.
- **A reference is shown only when there is one.** A validation error the user can fix themselves gets no reference; adding one implies a system fault that did not occur.

## Which surface gets which channel

| Failure | Channel | Persistence |
|---|---|---|
| Field validation the user can fix | inline, next to the field | until fixed |
| A user-initiated action that failed and can be retried | inline near the action, or a toast **plus** a persistent inline state | the inline state stays; the toast may fade |
| A surface that could not load | in place of the surface | until reload or retry |
| A background failure the user did not initiate | a non-blocking, dismissible notice | until dismissed |
| A failure that lost user work | a modal that cannot be dismissed by clicking away | until acknowledged |

**A toast is never the only record of a failure.** It may announce; something durable must remain. A failure whose only trace vanished in four seconds is not diagnosable, and the user who reports it has nothing to quote.

## What the UI emits

The interface is a source of evidence, not only a consumer of it.

- Emit on the boundaries that matter to a person: a failed user-initiated action, an unhandled render error, a route that could not resolve, a component that fell back to its error state, a permission-denied surface a user actually reached.
- Do not emit on every render, every keystroke, or every hover. Volume is not evidence, and a UI event stream nobody can afford to keep is worse than none.
- Every emitted event carries the same correlation reference the user sees, or it cannot be joined to the user's report.
- **Never put a secret, a token, a full request body, or a personal identifier into a UI event or an error surface.** The reference exists precisely so the payload does not have to.

**Names and values are not ours.** The name of any event, field or metric the UI emits is owned by `/alaa-services-contract` (`$alaa-services-contract`). Whether emitting it is required, recommended or optional, and what retention and cardinality apply, is owned by `/alaa-observability-soc` (`$alaa-observability-soc`). Invent neither: look them up, and if the name does not exist yet, request one rather than coining it in a component.

## The support round trip, as a design test

Walk it before calling an error surface done:

1. The user sees the failure and, without technical vocabulary, can say what went wrong.
2. The user can copy or read out a reference in one action.
3. Support can find the server-side record from that reference alone, with nothing else from the user.
4. The record says what the user's screen said.

An error surface that fails any step of this walk is not finished.

## Anti-patterns

- A toast as the only trace of a failed action.
- An error screen whose largest element is an error code.
- A reference in the console only, or in an unselectable element.
- A client-generated identifier with no server-side counterpart.
- The same generic message for a validation error, a permission denial, and a server fault.
- A stack trace, request body, or token rendered into the interface.
- Coining an event name in a component because the registry did not have one.

## Pairing

- The states these surfaces render: `15-designed-failure-states.md`
- The wording of the primary line: `35-ux-writing-and-microcopy.md`
- Announcing errors to assistive technology: `85-accessibility-patterns.md`
- Direction handling for the reference itself: `05-rtl-and-persian.md`
