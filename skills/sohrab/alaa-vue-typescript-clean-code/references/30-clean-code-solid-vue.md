# Clean code and SOLID for Vue, Quasar, and TypeScript

Design principles as enforceable frontend rules. The numeric budgets that back them are in `SKILL.md`; the
patterns you reach for once a rule bites are `41-pattern-selection.md`.

## Separation of concerns

Each layer has one job, and the test is what a change to it is caused by:

- **Component** — renders UI and coordinates user interaction. Changes when the screen changes.
- **Composable** — reusable UI or stateful behaviour: resize, dirty state, selection, table filters.
- **Pinia store** — shared application and domain state, and the actions that mutate it.
- **Service or API client** — HTTP, SDK, browser API, persistence, DTO mapping.
- **Validator** — pure validation returning user-safe error objects.
- **Formatter** — presentation-only value formatting.

Rejected: one component that fetches, maps DTOs, notifies, mutates the route, validates, and renders a
table; a service that imports a Vue component or a Quasar UI primitive; a store that knows about the DOM or
a component instance.

One rule about the validator and formatter layers is not stated here because it has one home: what a
validator or formatter may do with characters, and where input normalization runs, is
`72-frontend-security-binding.md`.

## Composition over inheritance

Use composables, slots and scoped slots, renderless components, small service facades, discriminated unions
with strategy maps, and Quasar's own extension points. Do not write a mixin in new code, and do not build a
base component that forces unrelated features into one hierarchy — in Vue the extension points are
compositional, and an inheritance chain removes them without replacing them.

## Single responsibility

A file has one primary reason to change. Split a component once it owns three or more unrelated concerns
among fetching, state ownership, validation, formatting, and complex rendering.

Do not split so far that a prop or a button becomes a component with no reuse, no separate test, and no
readability gain. The test for a good split is that each part has a name in the domain and could be
described to a colleague without saying "and then".

## Encapsulation

Components are black boxes with typed props, emits, and slots. Stores and services are modules with small
public APIs. SDK and browser-API quirks live behind a facade or adapter.

Rejected: reaching into a child's internals; exporting a mutable module global that is not an intentional
app-level singleton; sharing a raw API response shape across the UI.

## Keep it clean

Group related code in a predictable order inside a file: state, derived state, actions, lifecycle, helpers.

Clean up what you register: listeners, timers, subscriptions, observers, object URLs, pending requests,
worker messages. Explicit cleanup is not left to garbage collection where an explicit path exists, because
the failure mode is a leak that only appears after a user navigates back and forth twenty times.

Delete dead code, unused imports, and commented-out implementations; git remembers them. Deleting a
`console.log` is a telemetry decision, not a cleanup — `74-observability-binding.md` states what replaces
it. What earns a comment, and what an annotation must contain, is
`/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`); do not invent a local comment policy.

## DRY, with a condition instead of a feeling

**Extract on the third occurrence, or on the second when the two copies encode the same domain rule and
would have to change together. Two copies that change for different reasons stay separate.** That is the
whole rule; there is no threshold of discomfort involved, because a feeling is not a condition and two
agents feel differently.

Extract duplicated domain rules, mapping, validation, API calls, Quasar option builders, and repeated table
column configuration. Do not abstract from visual similarity, and do not create `utils`, `common`, or
`helper` modules holding unrelated functions — a module named for its single responsibility can be found;
a bucket cannot.

## Keep it simple

Prefer obvious data flow and explicit state transitions. Use a plain function before a pattern; use pattern
machinery only against complexity that exists now. Do not add a factory, a bus, a container, or a global
store for state that lives in one component.

## Code for the next reader

Names expose intent: `isEnrollmentOpen`, `submitEnrollment`, `mapCourseDtoToCourse`. Do not use an
abbreviation the domain does not use, a negated boolean (`isNotDisabled`), or a magic string where a typed
state reads better. Do not depend on
undocumented ordering, timing, or Quasar internals; if you must, the dependency is stated in the code and
covered by a test that fails when it changes.

## Code smells — the diagnosis vocabulary

Name the smell before choosing the repair. A ranked finding with a smell name is precise and impersonal,
and it tells the reader which repair family applies.

**Bloaters**

- Long function, mammoth component → the size budgets in `SKILL.md`; extract along the standard seams.
- Primitive obsession: statuses, ids, and money as bare strings and numbers → discriminated unions, branded
  types, typed value helpers (`22-typescript-type-system.md`).
- Long parameter list, or a boolean flag steering behaviour → one typed options object, or one function per
  flag value.
- Data clumps: the same field group recurring (page/size/sort; from/to) → one interface. Test: delete one
  field; if the rest lose meaning, they belong together.

**Object-orientation abusers**

- The same `switch` on one kind repeated across files → a strategy map, or a per-operation handler map
  closed by `assertNever`.
- Temporary state: refs that are meaningful only during one flow → extract the flow into its own composable
  that owns that state.
- Refused bequest: a "base" component or composable whose consumers stub half of it → split the contract,
  or compose instead of inheriting.

**Change preventers**

- Divergent change: one file edited for many unrelated reasons → split by change axis.
- Shotgun surgery: one conceptual change — a status rename, an event name — touching many files → gather it
  into one owner: an `as const` registry, one mapper, one store. This is the dual of divergent change, and
  over-correcting either one creates the other.

**Dispensables**

- A comment explaining *what* unclear code does → extract and name the extraction after the comment.
- Dead code, unused props and emits, a speculative abstraction with one implementation → delete.
- Data class: an interface whose derived logic is recomputed in every consumer → move the derivation into
  the mapper or composable that owns the type.

**Couplers**

- Feature envy: a component computing mostly from another module's state → move the computation to that
  store or composable.
- Inappropriate intimacy: reaching into child internals, `$parent`, importing another feature's private
  modules → typed contracts only.
- Message chains: `store.a.b.c.d` in a template → an intention-named getter at the owner.
- Middle man: a wrapper that only forwards → remove it. An adapter or decorator at a boundary is not a
  middle man; it is doing translation or adding behaviour on purpose.

**When not to fix.** Three cases, and each is recorded as a follow-up finding rather than repaired: the
smell is a deliberate pattern (a strategy map concentrates switches; an adapter concentrates foreign
shapes); the cure couples more than the smell does; or the repair falls outside the task's declared scope,
in which case it is reported with file and symbol, never done quietly.

## Boundary naming alignment

One canonical domain term per concept, identical across the concept's whole artifact family:

`CourseDto` → `mapCourseDtoToCourse` → `Course` → `useCourseFilters` → `useCourseStore` → `CourseTable.vue`
→ `course-table.spec.ts`.

Pick one term — `Course`, not sometimes `Lesson` and sometimes `ClassItem` — and keep singular and plural
accurate. Rename the whole family in one change; a half-renamed family is worse than the old name, because
now both names are wrong somewhere. Do not use role suffixes (`Service`, `Facade`, `Adapter`)
interchangeably for the same role inside one repo.

## SOLID, in Vue form

**Single responsibility** — components, composables, stores, and services each have one reason to change.
Split UI from state from API from validation from mapping from formatting.

**Open/closed** — extend through slot content, typed strategy maps, composables, store actions, adapter
implementations, and Quasar props. A central `switch` that must be edited for every new variant is the
thing this principle exists to remove.

**Liskov substitution** — two components or services implementing the same contract must be
interchangeable. A hidden precondition like "works only after the parent calls `init`" belongs in the
contract or does not exist.

**Interface segregation** — keep APIs role-specific. `UserPickerProps` does not carry user-management table
settings; a composable does not return twenty values when callers need two; a facade exposes domain
operations, not every SDK method.

**Dependency inversion** — high-level UI depends on typed abstractions: injection keys, service interfaces,
store actions, API facades, testable adapters. The recognition signals are in the diagnostic table in
`41-pattern-selection.md`, and the rule that decides the interface's shape is here:

**The port belongs to the consumer.** Define the interface as what the UI needs — three methods, in domain
words — not as a mirror of what the SDK offers. A port shaped like the SDK inverts nothing: it changes
whenever the SDK changes, which is the coupling you were removing.
