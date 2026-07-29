# Components, Interaction States and UX Patterns

Read this file when designing a component's interaction, a form, a navigation surface, or a chart. **Data and failure states — empty, stale, error, permission-denied, offline, degraded — are in `15-designed-failure-states.md` and are not repeated here.** This file covers what a component does under the user's hand.

## Interaction state coverage

Every interactive component ships with all applicable interaction states designed:

`default` · `hover` · `focus-visible` · `active/pressed` · `disabled` · `read-only` · `selected` · `busy`

Rules:

- **Hover and press change colour, opacity or elevation — never layout bounds.** A hover that changes size, padding or border width shifts the layout under the cursor.
- **Focus-visible ring 2 to 4px from the `ring` token**, with a visible offset so it is not swallowed by the control's own border. Never removed without a stronger replacement.
- **Disabled** reduces emphasis and carries the semantic disabled state, with no pointer affordance. It always states its reason (`15-designed-failure-states.md`).
- **Read-only is visually and semantically distinct from disabled.** Read-only content is selectable and copyable; disabled content is not. Rendering them identically is a defect because the user's next action differs.
- **Press feedback within 100 ms.** A control that starts async work disables itself and shows progress for the duration.
- **Touch targets at least 44x44 CSS px with at least 8px between them.** Extend the hit area when the visual mark is smaller rather than enlarging the mark. This is deliberately stricter than the WCAG 2.2 Level AA minimum; see `90-quality-gates-and-review.md`.
- `cursor: pointer` on every clickable element. No interaction exists only on hover — there is no hover on touch.

## Forms

- **A visible label per field. A placeholder is never the label** — it disappears exactly when the user needs it, and it fails for every user who returns to a partly-filled form.
- Helper text below complex fields, before the error, not instead of it.
- **Validate on blur, not on keystroke.** Validating as the user types marks a correct entry as wrong halfway through. After a failed submit, focus moves to the first invalid field.
- Errors sit below their field, state cause and fix, and are announced (`85-accessibility-patterns.md`). Multiple errors also get a summary with anchors to each field.
- **Semantic input types and autocomplete attributes** so the right keyboard appears and autofill works. On a Persian product this includes the LTR islands from `05-rtl-and-persian.md` section 4.
- **A field with a canonical form declares its maximum length**, so a paste that carries separators or formatting is visibly truncated instead of silently submitted.
- Destructive actions use the destructive role, are spatially separated from primary actions, and prefer undo over a confirmation wall for bulk operations. Irreversible actions confirm, and the confirming button names the action.
- Multi-step flows show progress and allow going back. Long forms auto-save. Dismissing a sheet or modal with unsaved input confirms first.

## Navigation

- Placement is consistent across every page; the current location is marked by more than colour.
- **Back is predictable and preserves scroll position, filters and input state.** Never silently reset the stack.
- Bottom navigation on mobile: at most five items, icon plus label, top-level destinations only. Sidebar from 1024px. A drawer holds secondary navigation, never primary actions.
- Do not mix a tab bar, a sidebar and bottom navigation at one hierarchy level.
- Modals are for focused tasks, never for primary navigation. Every modal and sheet has an obvious dismiss and an escape route.
- Breadcrumbs from three levels deep. Overflow menus instead of cramming actions.
- Key screens are deep-linkable. Destructive items — sign out, delete account — are spatially separated from ordinary navigation.
- Direction-bearing navigation affordances follow `05-rtl-and-persian.md` sections 2 and 3.

## Charts and data visualization

- **The chart type answers the question:** trend to a line; comparison to a bar; part-to-whole to a stacked bar, with a pie only for five or fewer categories with clearly distinct proportions; distribution to a histogram; relationship to a scatter.
- **Colour is never the only encoding.** Add a label, a pattern or a shape. Data series against background at least 3:1; data labels at the body threshold.
- Direct-label small datasets. Legends sit next to the chart, not below the fold. Tooltips show exact values. Gridlines stay low-contrast so the data leads.
- Tabular numerals wherever numbers align. Locale-aware number and date formatting per `05-rtl-and-persian.md` sections 7 and 8; axis order under RTL per section 5.
- **Ship a table alternative or a text summary.** A chart that cannot be read by a screen reader has no accessible content at all, and a summary sentence is usually enough.
- Entrance animation respects reduced motion and never delays readability.
- **A chart designs its empty, loading and error states like any other component** (`15-designed-failure-states.md`). A bare axis frame is not a state.

## Anti-patterns

- Components delivered with only the default state.
- Placeholder-as-label forms.
- Errors listed only at the top of the page.
- Disabled and read-only rendered identically.
- Validation firing on every keystroke.
- A pie chart with eight slices; red and green as the only status encoding.
- Hover-only interactions and focus outlines removed for aesthetics.
- A layout-shifting hover effect.

## Pairing

- Data and failure states: `15-designed-failure-states.md`
- Long lists, latency and concurrent edits: `65-lists-latency-and-concurrency.md`
- Promoting a pattern to a shared component: `55-component-library-and-governance.md`
- Copy inside these components: `35-ux-writing-and-microcopy.md`
- Focus, ARIA and live regions behind these rules: `85-accessibility-patterns.md`
- Motion for state transitions: `70-motion-contract.md`
- Icons inside components: `80-icons-assets-and-imagery.md`
