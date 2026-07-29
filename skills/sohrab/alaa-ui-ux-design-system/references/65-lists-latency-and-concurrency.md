# Lists, Latency and Concurrency

Read this file when rendering a list whose length is not bounded in code, when an edit could be made from two places at once, or when designing for a connection that is slow rather than absent.

## When a list stops being a list

A collection has three design regimes, and the boundary between them is a number, not a feeling.

| Rows rendered | Regime | Design |
|---|---|---|
| up to ~50 | plain list | render everything; no pagination affordance, no virtualization |
| ~50 to ~200 | paged or lazily extended | the user chooses to see more; the choice is visible and reversible |
| more than ~200, or unbounded | **virtualized** | only the visible window is in the DOM |

**Unbounded means the row count is a function of tenant size, history length, or time.** A list of a user's bookmarks is unbounded. A list of the seven days of the week is not. If you cannot state the maximum from code, treat it as unbounded.

**Design consequences of virtualization, which are ours even though the mechanism is not:**

- **Every row must be the same height, or its height must be measurable before it renders.** Variable-height rows in a virtualized list produce scroll jumps. Design the row to a fixed height, or accept that the design constrains the technique.
- **The scrollbar must tell the truth.** A virtualized list whose total height is unknown produces a scrollbar that lies about position; design a count or a progress indicator that does not.
- **Find-in-page stops working.** Content not in the DOM cannot be found by the browser. Any virtualized list of text the user might search needs its own search affordance, designed, not assumed.
- **Anchoring and deep links.** "Jump to my comment" must work; a virtualized list needs a designed way to scroll to an item by identity, not by pixel offset.
- **Sticky headers, selection state and keyboard navigation** must survive recycling. A checkbox whose checked state is stored on the DOM node is a defect here in a way it is not in a plain list.
- **Print and export** ignore virtualization. If the list must be printable or exportable, that is a separate rendering path, designed separately.

**Wrap the official capability.** Quasar ships `QVirtualScroll` and `QInfiniteScroll`; the fleet preference is to wrap what the framework already provides rather than to add a library or hand-roll a windowing implementation. `client` already does this at `src/content-show/ContentShowCommentsSection.vue:69`. Their props, slots and configuration are owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`); what this file requires is the outcome above.

**Infinite scroll is a decision with a cost, not a default.** It removes the footer, breaks the back button's scroll restoration, and makes "how much is there" unanswerable. Use it for a feed the user browses; use paging for a list the user works through. Never use it where the user needs to reach the end.

## Slow networks

Slow is not offline, and it is the more common case. The offline state is in `15-designed-failure-states.md`; this section is about the connection that works and takes a long time.

- **Design against the slowest connection in the product's actual audience, not the development machine.** State that assumption in `MASTER.md` so it can be argued with.
- **Progressive disclosure of data, not of the page.** Render the shell and the parts that resolved; do not hold the whole page for the slowest request. A page that appears in one piece after four seconds is worse than one that appears in three pieces over four seconds.
- **Reserve the space before the data arrives**, so nothing moves when it lands. A skeleton whose dimensions differ from the content it replaces is a layout shift with extra steps.
- **Order requests by what the user is looking at.** Above-the-fold data first; a sidebar widget never blocks the article.
- **Every request the user waits on can be cancelled or backgrounded past 10 s** (`15-designed-failure-states.md`).
- **Design the retry.** An automatic retry that is invisible produces a page that seems stuck; an automatic retry that is announced produces a page that seems to be working. Retry policy itself — how many, how spaced, when to stop — is owned by `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Optimistic updates

Showing a change before the server confirms it is a **design decision with a stated failure design**, not a performance trick.

**Use an optimistic update when all four hold:**

1. The action almost always succeeds.
2. The result is fully predictable from the client's state — a toggle, a like, a reorder, a local rename.
3. Reverting is cheap and comprehensible to the user.
4. The user can tolerate seeing the revert.

**Never use one when any of these hold:** the action costs money, is irreversible, is a permission-sensitive write, or produces a value the server computes (an identifier, a total, a rank, a timestamp the user will rely on).

**If you use one, you must design all three of these:**

- The **pending appearance** — subtle, not a spinner over the whole row. The user should be able to keep working.
- The **revert** — the row returns to its previous state *and says why*, in place. A silent revert is the worst outcome in this file: the user believes their change is saved and it is not.
- The **conflict** — the server answered with something different rather than with an error. See the next section.

## Concurrent mutation

Two tabs, a phone and a laptop, or two people with the same permissions. The design question is what the second writer sees.

- **Never let the last write win silently.** That is not a policy; it is the absence of one, and it destroys work invisibly.
- **Detect, then choose one posture per surface and record it:**
  - **Refuse and show:** the write is rejected, the current server state is shown beside the user's version, and the user chooses. Correct for anything with stakes.
  - **Merge by field:** non-overlapping field edits both apply; overlapping ones surface. Correct for long forms.
  - **Take the newest and announce it:** correct only for a value with no editorial content — a toggle, a status flag.
- **A surface open long enough to go stale tells the user it changed underneath them** before they submit, not after. A form open for twenty minutes on data that changed ten minutes ago should say so while there is still time to act.
- **Cross-tab consistency is a design requirement.** A user who logs out, changes theme, or changes permissions in one tab must not find a second tab still acting on the old state. Which state is synchronized and how is `/alaa-frontend-developer` (`$alaa-frontend-developer`) ground; that it must be visibly consistent is ours.
- **Never resolve a conflict by discarding the user's input without showing it to them.** Whatever the posture, the text they typed is recoverable from the screen.

## Anti-patterns

- A list with no stated maximum rendered without virtualization.
- Variable-height rows inside a virtualized list.
- Infinite scroll on a list the user must finish.
- A spinner covering an entire page while one sidebar request resolves.
- An optimistic update with no designed revert.
- An optimistic update on a payment, a deletion, or a permission change.
- Last-write-wins with no detection and no message.
- A stale form that discovers its staleness only at submit.

## Pairing

- Loading, stale and error appearances: `15-designed-failure-states.md`
- Frame and interaction budgets: `45-render-and-asset-budgets.md`
- Interaction states of the rows themselves: `60-components-states-and-ux.md`
- Announcing changes to assistive technology: `85-accessibility-patterns.md`
- Timeout, retry and degradation policy: `/alaa-reliability-sla` (`$alaa-reliability-sla`)
