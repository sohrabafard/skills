# Component Library and Design-System Governance

Use this file when building or evolving shared/reusable UI components, or when deciding how a design system lives and changes over time. This is what makes the system a system instead of a folder of pages.

## When to promote a pattern to a shared component

- Rule of three: the third real occurrence of a pattern earns a shared component; the first two stay local. Premature abstraction is as costly as copy-paste divergence.
- Promote when the pattern carries design decisions (states, spacing, variants) that must stay synchronized; keep purely structural one-offs local.
- Before promoting, design the full state coverage (`60-components-states-and-ux.md`) and pass the gates (`90-quality-gates-and-review.md`) — a shared component multiplies its defects.

## Component API design (Vue)

- Variants are small closed sets mapped to tokens: `variant: 'primary' | 'secondary' | 'ghost' | 'destructive'`, `size: 'sm' | 'md' | 'lg'` drawn from the token scales. Consumers pick meaning; the component resolves visuals.
- Never accept raw visual values as props (`color="#2563EB"`, `rounded="12px"`) — that reopens the raw-hex hole tokens closed. Escape hatch is `class`/`style` passthrough, used consciously.
- Avoid boolean explosion (`primary`, `outlined`, `dense`, `flat` all together): mutually exclusive looks are one enum prop, not four booleans.
- Slots for composition (content, icon, actions); props for configuration. Follow the Vue style guide via `$alaa-vue-typescript-clean-code` for naming, typing, and emits.
- Multi-word names with one consistent app namespace per repo (e.g. `AppButton`, `UiCard`) — follow the repo's existing convention; never introduce a second one.

## Quasar posture: wrap, don't fork

- Build the app-family identity as one thin wrapper layer over Quasar components (tokens via `app.scss` + wrapper components for recurring configurations). Never fork Quasar component internals or restyle per usage.
- If a wrapper only forwards props with no design decision, delete it — wrappers exist to encode decisions.
- Component visuals come from the token layer; a shared component with hardcoded values is drift with a nice name.

## Documentation and discoverability

- Each shared component documents: purpose, variants and when to use each, state coverage, accessibility notes (focus, labels, keyboard), and one ✅/❌ usage pair. Keep it next to the code (docblock or co-located md; Storybook/Histoire only if the repo already uses it).
- MASTER.md lists the shared components with one-line purposes so agents and humans find them before rebuilding them.

## Change management and drift control

- Tokens change in one place and propagate; a visual refresh that edits components one by one is drift, not a refresh.
- Never fork a shared component per page ("CheckoutButton" that is `AppButton` with one hardcoded color). Page-level needs become a variant, a page override in `design-system/pages/`, or a conscious local component — decided, not drifted.
- Deprecate loudly: when a variant/component is replaced, mark it deprecated in its doc and MASTER.md, migrate usages, then delete. Two live generations of the same pattern is a defect.
- Contract changes to widely-used shared components (renamed props, removed variants) are breaking changes: search all usages first, migrate in the same change, note it in MASTER.md.

## Anti-patterns

- Snowflake components: five nearly-identical cards because nobody checked the library first.
- Prop APIs that mirror CSS instead of meaning (`bgColor`, `borderRadius` props).
- A "design system" that is only a Figma/board artifact with no token or component counterpart in the repo.
- Wrapping every Quasar component preemptively; abstraction without a decision to encode.
- Silent divergence: editing a shared component's look for one page's need.

## Pairing guidance

- State coverage and UX rules for the components themselves: `60-components-states-and-ux.md`
- Token layer these components consume: `20-design-tokens-and-theming.md`
- Code quality, typing, composables: `$alaa-vue-typescript-clean-code`; exact Quasar APIs: `$alaa-quasar-app-vite-v3`
