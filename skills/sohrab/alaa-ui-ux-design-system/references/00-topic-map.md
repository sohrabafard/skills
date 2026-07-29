# Topic Map

The only router in this skill. Each row states a situation you can observe in the task or the repo, not a subject heading. Match the situation, read that one file, then read a second-order row only if it also matches.

## Primary rows

| You are about to... | Read |
|---|---|
| start a product, site or redesign that has no persisted design decisions, or you cannot find a `MASTER.md` or token file in the repo | `10-design-workflow.md` |
| write a color, spacing, radius, shadow or z-index value into a component, add a theme, or add a semantic role name | `20-design-tokens-and-theming.md` |
| pick a font, set a line height, build a type scale, or judge whether two colors may sit on each other | `30-typography-and-color.md` |
| start a product with no palette at all and want a validated starting point | `32-starter-palettes.md` |
| render Persian text, set `dir`, mirror an icon, place a Latin string inside a Persian form, or display a date or a digit | `05-rtl-and-persian.md` |
| write a button label, an error message, an empty-state line, a toast, or any string a user will read | `35-ux-writing-and-microcopy.md` |
| choose a visual style, or add a shadow, blur, border or radius that is not already in the token file | `40-styles-and-visual-language.md` |
| set a breakpoint, a container width, a section order, or place a call-to-action | `50-layout-landing-and-ia.md` |
| create a component that a second page will also use, add a prop to a shared component, or copy a component to change one value | `55-component-library-and-governance.md` |
| ship a component whose only designed state is the happy path, or design a form, a navigation surface, or a chart | `60-components-states-and-ux.md` |
| design what the user sees when data is missing, stale, forbidden, offline, or a dependency is degraded | `15-designed-failure-states.md` |
| render content a user or another tenant supplied, handle a paste, or show or hide a control based on a permission | `25-untrusted-content-and-ui-authority.md` |
| show an error the user may need to report, or decide what the UI emits when something fails | `28-ui-diagnosability.md` |
| render a list whose length is not bounded in code, allow an edit that two tabs could make at once, or design for a slow connection | `65-lists-latency-and-concurrency.md` |
| animate anything, add a transition, or set a duration or easing value | `70-motion-contract.md` |
| use a CSS feature you are not certain ships in every target browser | `72-modern-css-baseline-tiers.md` |
| add an icon, an image, a logo, a favicon, or an Open Graph image | `80-icons-assets-and-imagery.md` |
| add `@click` to a non-`<button>`, open an overlay, change route in an SPA, or write ARIA | `85-accessibility-patterns.md` |
| add a font file, a hero image, a video embed, or a third-party script; or add a theme, density tier or preference axis that multiplies what must be verified | `45-render-and-asset-budgets.md` |
| deliver shipped UI, or answer a "review this design" request | `90-quality-gates-and-review.md` |
| claim that a design change is correct, or be asked what proves it | `95-design-proofs.md` |

## Second-order rows

Read these in addition when the condition also holds.

| Condition | Also read |
|---|---|
| The product renders Persian or any right-to-left text — true of `client` on every route | `05-rtl-and-persian.md` |
| You are adding or editing a theme, a dark mode, or any color value | `20-design-tokens-and-theming.md`, then run `scripts/check-design-system.mjs` |
| The style you picked has a "Do not use for" entry that names this product type | `40-styles-and-visual-language.md` before committing |
| The component you are changing is imported by more than one page | `55-component-library-and-governance.md` |
| The surface can fail, be empty, or be forbidden to this user | `15-designed-failure-states.md` |
| The value being rendered came from a request body, an upload, a URL parameter, or another tenant | `25-untrusted-content-and-ui-authority.md` |
| The task ends in shipped UI | `90-quality-gates-and-review.md` |
| The change must be implemented in Vue, Quasar or Vite, or needs SSR safety | pair with `/alaa-frontend-developer` (`$alaa-frontend-developer`) |
| The rule you want names a Quasar prop, plugin, directive or config key | it is not ours: `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) |

## Deciding between two files that both look right

- The rule survives swapping Quasar for another library, so it is here; the rule needs a Quasar symbol to be correct, so it belongs to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`).
- The question is "what must be true" — that is `90-quality-gates-and-review.md`. The question is "how do I make it true" — that is the topic file. The question is "how do I show it is true" — that is `95-design-proofs.md`.
- The question is about a value the server also knows (a permission bit, a date wire format, a metric name) — that value is not ours; cite `/alaa-services-contract` (`$alaa-services-contract`).
- The question is about the *appearance* of a state — ours. About *when the system enters* that state — `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Good first searches

Literal strings that appear in exactly one place in this pack:

`design brief` · `semantic token` · `token lookup` · `missing role` · `light-dark` · `oklch` · `contrast-color` · `dark mode` · `spacing scale` · `density tier` · `font pairing` · `contrast ratio` · `on-accent` · `Vazirmatn` · `font byte budget` · `glassmorphism` · `do not use for` · `landing structure` · `state coverage` · `empty state` · `permission-denied` · `stale data` · `degraded dependency` · `fake affordance` · `untrusted` · `v-html` · `paste` · `correlation reference` · `X-Request-Id` · `rule of three` · `variant` · `escape hatch` · `microcopy` · `unicode-bidi` · `must-mirror` · `LTR island` · `ZWNJ` · `Jalali` · `digit system` · `virtualization` · `optimistic update` · `two tabs` · `frame budget` · `image weight ceiling` · `theme matrix` · `skip link` · `focus management` · `live region` · `WCAG 2.2` · `view transitions` · `prefers-reduced-motion` · `stagger` · `Baseline tier` · `icon family` · `favicon` · `og:image` · `blocking gates` · `visual regression`
