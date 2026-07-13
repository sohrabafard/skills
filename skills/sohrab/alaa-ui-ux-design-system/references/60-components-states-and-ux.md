# Components, States, and UX Patterns

Use this file when designing components, forms, navigation, feedback, and data visualization.

## State coverage (design deliverable, not afterthought)

Every interactive component ships with all applicable states designed:

- default, hover, focus-visible, active/pressed, disabled
- loading, error, empty, partial-data (when relevant)

Rules:

- Hover/press feedback changes color, opacity, or elevation — never layout bounds (no jitter).
- Focus-visible ring 2–4px from the `ring` token; never removed without a stronger replacement.
- Disabled: reduced emphasis (opacity ~0.4–0.5), semantic `disabled` attribute, no pointer affordance. Read-only is visually and semantically distinct from disabled.
- Press feedback within ~100ms; buttons disable and show progress during async work.
- Touch targets >= 44x44px with >= 8px gaps; extend the hit area when the visual is smaller. `cursor: pointer` on clickable web elements; never hover-only interactions.

## Forms and feedback

- Visible label per field — placeholder is never the label. Helper text below complex fields.
- Validate on blur, not on keystroke; after failed submit, focus the first invalid field.
- Errors sit below the related field, state cause + fix ("Password needs 8+ characters"), and announce via `aria-live`/`role="alert"`. Multiple errors get a summary with anchors.
- Semantic input types (`email`, `tel`, `number`) and autocomplete attributes so keyboards and autofill work.
- Destructive actions: danger token, spatially separated from primary actions, confirm before irreversible ones, prefer undo ("Deleted — Undo") over confirmation walls for bulk actions.
- Multi-step flows show progress and allow going back; long forms auto-save; confirm before dismissing unsaved sheets/modals.
- Loading: skeletons over spinners for content areas past ~300ms; reserve space so nothing jumps (CLS). Success gets brief visible confirmation.
- Toasts: auto-dismiss 3–5s, never steal focus, `aria-live="polite"`.

## Navigation patterns

- Placement is consistent across all pages; current location visibly marked (active token, not color alone).
- Back is predictable and preserves scroll/filter/input state; never silently reset the stack.
- Bottom nav (mobile) max 5 items, icon + label, top-level destinations only. Sidebar for >= 1024px; drawer holds secondary navigation, not primary actions.
- Don't mix tab bar + sidebar + bottom nav at the same hierarchy level.
- Modals are for focused tasks, never primary navigation; every modal/sheet has an obvious dismiss and an escape route.
- Breadcrumbs for hierarchies 3+ levels deep; overflow menus instead of cramming actions.
- Key screens deep-linkable; destructive items (logout, delete account) spatially separated from normal nav.

## Empty, error, and edge states

- Empty states teach: what this area is + one action to fill it — never a blank region or a lonely "No data".
- Error states offer recovery (retry, edit, support link), not dead ends; timeouts say so and offer retry.
- Design for the ugly cases before shipping: long titles, long words (Farsi compounds included), zero items, one item, thousands of items, slow network, offline.

## Charts and data-viz design

- Chart type answers the question: trend -> line; comparison -> bar; part-to-whole -> stacked bar (pie only <= 5 categories with distinct proportions); distribution -> histogram; relationship -> scatter.
- Color is never the only encoding — add labels, patterns, or shape; data series vs background >= 3:1, data labels >= 4.5:1.
- Direct-label small datasets; legends sit next to the chart; tooltips show exact values; gridlines low-contrast so data leads.
- Tabular numerals everywhere numbers align; locale-aware number/date formatting (Persian digits decision per `30-typography-and-color.md`).
- Provide a table alternative or text summary for screen readers; entrance animation respects reduced-motion and never delays readability.
- Empty/error/loading chart states designed like any component — a bare axis frame is not a state.

## Anti-patterns

- Components delivered with only the default state ("happy-path design").
- Placeholder-as-label forms; errors listed only at the top of the page.
- Pie charts with 8 slices; red/green as the only status encoding.
- Empty regions with no explanation or action; error toasts with no recovery.
- Layout-shifting hover effects and focus outlines removed "for aesthetics".

## Pairing guidance

- Promoting patterns to shared components and component APIs: `55-component-library-and-governance.md`
- Copy inside these components (labels, errors, empty states): `35-ux-writing-and-microcopy.md`
- Accessibility patterns behind these rules (focus, ARIA, live regions): `85-accessibility-patterns.md`
- Motion for state transitions: `70-motion-and-modern-css.md`
- Icon usage inside components: `80-icons-assets-and-imagery.md`
- Quasar component selection and APIs: `$alaa-quasar-app-vite-v3`; implementation and QA: `$alaa-frontend-developer`
