# Browser Debug and SSR-Safe Implementation

The engineering side of looking at a running page, and the constraints SSR imposes on a design before it
is built. Visual design, tokens, state coverage and design review are `/alaa-ui-ux-design-system`
(`$alaa-ui-ux-design-system`) `references/00-topic-map.md`.

## SSR-aware implementation constraints

- A design that requires DOM measurement before hydration cannot be implemented deterministically. Say so
  before building it.
- Initial layout comes from CSS, not from JavaScript running on first render.
- Where client-only measurement is genuinely unavoidable, define three things in the diff: the stable SSR
  placeholder, the moment hydration enhances it, and how the transition avoids a visible shift
  (`41-lighthouse-and-web-vitals.md` — CLS).

When a proposed design cannot satisfy these, the decision belongs to the design owner:
`/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/90-quality-gates-and-review.md`
decides whether the design changes. SSR is not broken to honour a design.

## The gate before opening a browser

Browser automation opens only when the user asks for browser, visual or responsive validation; a repo rule
requires reproduction; or **one static pass is complete and you can name the single observation source
cannot produce** — the exact console warning text, a computed style value, or an HTTP status. State that
observation, then open. Profile choice is `70-companion-skill-routing.md`.

Before opening, write four lines: the expected behaviour, the observed failure, the target route or URL,
and the success criterion. Without them the session produces screenshots instead of a diagnosis.

## Evidence checklist

Capture the smallest proof:

- one relevant console or hydration warning, quoted exactly;
- one failing request with the status and the deciding response detail, when the network is implicated;
- one DOM, ARIA or visual capture showing the wrong state.

Then write one root-cause hypothesis, define the smallest patch that could prove or disprove it, apply it,
and re-run the same reproduction. A second screenshot is not a second piece of evidence.

## Symptom to first move

| What you see | Look here first |
|---|---|
| a hydration warning on first load only | `20-vue-js-ssr-patterns.md` — non-determinism, or a client-only branch |
| a formatted value differing between server HTML and hydrated DOM | `55-i18n-locale-and-rtl.md` |
| a 404 on a hashed asset after a deploy | `30-pwa-sw-and-offline.md`, then `/alaa-frontend-devops` (`$alaa-frontend-devops`) `references/45-deploy-failure-playbook.md` |
| an unexplained CORS or preflight failure on a request that used to work | a newly added header — `47-frontend-observability.md` |
| a control that renders for a user who should not have it | `25-frontend-security.md`; the server is still the decider |
| a request that never resolves | `46-resilience-and-degradation.md` — no deadline attached |
| jank under a burst of updates | `40-performance-and-realtime.md` — backpressure |

Record what the session produced per `50-qa-and-verification.md`.
