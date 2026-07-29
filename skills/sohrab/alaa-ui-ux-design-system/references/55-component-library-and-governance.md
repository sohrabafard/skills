# Component Library and Design-System Governance

Read this file when building or evolving a shared component, or when deciding how a design system lives and changes over time. This is what makes the system a system instead of a folder of pages.

## When to promote a pattern to a shared component

- **Rule of three:** the third real occurrence earns a shared component; the first two stay local. Premature abstraction costs as much as copy-paste divergence.
- Promote when the pattern carries design decisions — states, spacing, variants — that must stay synchronized. Keep purely structural one-offs local.
- Before promoting, design the full state coverage (`60-components-states-and-ux.md`, `15-designed-failure-states.md`) and pass the gates (`90-quality-gates-and-review.md`). A shared component multiplies its defects by its usage count.

## Component API design

- **Variants are small closed sets mapped to tokens:** `variant: 'primary' | 'secondary' | 'ghost' | 'destructive'`, `size: 'sm' | 'md' | 'lg'`, drawn from the token scales. Consumers pick meaning; the component resolves visuals.
- **Never accept raw visual values as props** (`color="#2563EB"`, `rounded="12px"`). That reopens the raw-value hole tokens closed, one component at a time.
- **The escape hatch has a boundary.** `class` and `style` passthrough may set **placement only**: margin, grid area, width, order, alignment. A passthrough that sets colour, background, radius, shadow, border, font size or font weight is a defect — add a variant instead. This is checkable by reading the call site, which "used consciously" was not.
- **Avoid boolean explosion.** Mutually exclusive looks are one enum prop, not four booleans that can all be true at once.
- **Slots for composition** (content, icon, actions); **props for configuration**. A prop that takes a chunk of content wants to be a slot.
- **A direction-bearing icon is never a physical name in the prop.** `icon="next"` resolves; `icon="arrow-left"` does not. See `05-rtl-and-persian.md` section 2.
- **Every prop that renders untrusted content is documented as such**, and the component states what it does with it (`25-untrusted-content-and-ui-authority.md`).
- Multi-word names with one app namespace per repo (`AppButton`, `UiCard`). Follow the repo's existing convention; never introduce a second one.
- Naming, typing, emits and composable shape are owned by `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`).

## Quasar posture: wrap, do not fork

- Build the app-family identity as one thin wrapper layer over the framework's components: tokens plus wrapper components that encode recurring configurations. Never fork a component's internals, and never restyle per usage.
- **If a wrapper only forwards props and encodes no design decision, delete it.** Wrappers exist to hold decisions, not to add a layer.
- Component visuals come from the token layer. A shared component with hardcoded values is drift with a nice name.
- Which framework component to wrap, and its exact API, is owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`).

## Documentation

Each shared component documents, next to its code: purpose; every variant and when to use each; state coverage including the failure states it handles; accessibility notes (focus behaviour, accessible name, keyboard); whether it renders untrusted content; and one correct and one incorrect usage example. `MASTER.md` lists the shared components with one-line purposes so an agent finds one before rebuilding it.

The repository's own annotation and docblock conventions are owned by `/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`); this file states only what must be recorded, not the format.

## Change management and drift control

- **Tokens change in one place and propagate.** A visual refresh that edits components one by one is drift, not a refresh.
- **Never fork a shared component per page.** A `CheckoutButton` that is `AppButton` with one hardcoded colour is the canonical example. A page-level need becomes a variant, a page override in `design-system/pages/`, or a deliberate local component — decided, never drifted.
- **Deprecate loudly:** mark the replaced variant deprecated in its doc and in `MASTER.md`, migrate every usage, then delete it. Two live generations of one pattern is a defect.
- **A contract change to a widely-used component is a breaking change:** search all usages first, migrate in the same change, record it in `MASTER.md`. What "breaking" obliges beyond that — versioning, notice, coordination across repos — is owned by `/alaa-project-constitution` (`$alaa-project-constitution`).
- **Dead and near-dead tokens are drift too.** A token with zero usages is an abstraction nobody wanted; a token with one usage is a component token in the wrong place. Review both when the system is edited.

## Anti-patterns

- Snowflake components: five nearly-identical cards because nobody searched the library.
- Prop APIs that mirror CSS instead of meaning (`bgColor`, `borderRadius`).
- A `class` passthrough carrying a colour.
- A "design system" that is only a design-tool artefact with no token or component counterpart in the repo.
- Wrapping every framework component preemptively.
- Silently editing a shared component's look for one page's need.
- A component documented as "self-explanatory".

## Pairing

- Interaction states and forms: `60-components-states-and-ux.md`
- Data and failure states: `15-designed-failure-states.md`
- The token layer these components consume: `20-design-tokens-and-theming.md`
- Untrusted-content props: `25-untrusted-content-and-ui-authority.md`
- Direction-bearing props: `05-rtl-and-persian.md`
- Code quality, typing, composables: `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`)
