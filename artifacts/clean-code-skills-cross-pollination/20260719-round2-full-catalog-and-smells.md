# Round 2 — full refactoring.guru catalog + selection training + code smells (2026-07-19)

Basis: complete study of refactoring.guru — all 22 GoF pattern pages (via 4 parallel research agents;
distilled notes saved as `20260719-refactoring-guru-notes-{creational,structural,behavioral,smells-refactoring}.md`)
plus /refactoring/smells (23 smells, 5 families), /refactoring/when, /refactoring/what-is-refactoring.
Round 1 was committed by the maintainer as 6d715eb4.

## The centerpiece: pattern-selection training (the user-named gap)

Every skill now teaches *recognition before choice*:

- **Vue** `40-patterns-vue-quasar.md` opens with "Pattern selection diagnostic": a 16-row symptom → pattern →
  confirming-question table + look-alike disambiguation (Adapter/Decorator/Proxy/Facade; CoR/Pipeline/Decorator;
  Command/Strategy; Template Method/Strategy). SKILL.md orders agents to run it before choosing.
- **PHP** `design-patterns.md` opens with "Pattern recognition diagnostic": a 20-row table + the same
  look-alike block + Repository-vs-query-dump discriminator. SKILL.md pattern-decision-order points to it.
- **Go** `60-design-patterns-kit-era.md` opens with "Recognize by symptom first" (17 rows, kit-era) +
  look-alikes, each row confirming against a P-principle.

## Full catalog coverage (22/22 GoF patterns)

- **PHP** now covers all 22 + platform patterns (748 lines): added this round — Abstract Factory (provider
  suites bound at boot), Prototype (`__clone` deep-copy, PHP 8.5 clone-with, Eloquent `replicate()`),
  Bridge (notifications as native bridge; report × exporter), Flyweight (enums as interned flyweights;
  all-three-conditions + optimization-only rule), Mediator (orchestrating service vs event dispatcher;
  vs Facade), Memento (audit pre-images, `getOriginal()`, Octane no-in-memory-undo), Visitor (handler-map
  pragmatic form first; accept() only for deep recursive accumulation). Sharpened: Singleton criticisms,
  Observer dynamic-subscriber signal, Strategy first-class-callable + vs-State, Facade god-object warning.
- **Vue** now covers all 22 in frontend form (444 lines): added — Abstract Factory (suites via injection),
  Prototype (structuredClone + toRaw, frozen preset registries), Bridge (two-axis splits), Mediator
  (orchestrator composable = GoF mediator; god-composable guard), Memento (owner-built snapshots, bounded
  history, pairs with Command + failure classification), Flyweight (virtualization first; measured need),
  Visitor (functional form: per-operation handler maps over discriminated unions + assertNever).
  Sharpened: Observer (Vue reactivity IS observer), Singleton criticisms, Strategy function-first + vs-State.
- **Go** kit-era map now covers all 22 + Pipeline + DIP (252 lines): added stances — Abstract Factory
  (suite struct at boot), Prototype (value semantics + aliasing warning), Bridge (renderer × channel),
  Flyweight (immutable lookup tables only), Mediator (use case is the mediator; in-process hubs = Observer
  ban), Memento (durable pre-images in the same tx), Visitor (exhaustive kind-switch / handler maps, no
  accept()); symptom rows added for each. Depth still routes to golang-* skills per the boundary contract.

## Code smells layer (new diagnosis vocabulary)

- **PHP**: new reference `code-smells-and-refactoring-triggers.md` (65 lines) — all 5 families in Laravel
  terms (each smell → treatment), Rule of Three, when-to-refactor triggers, when NOT to refactor
  (deliberate patterns exempt; mode limits), clean-code qualities. Wired into SKILL.md reference list.
- **Vue**: "Code smells — the diagnosis vocabulary" section in `30-clean-code-solid-vue.md` (5 families in
  frontend form) + Rule of Three added to DRY.
- **Go**: compact "Code smells → where the repair lives" routing block in the 60 file (respects
  golang-code-style ownership; Rule of Three vs kit-intake rule).

## Files changed this round

- PHP: SKILL.md, references/design-patterns.md, references/solid-in-practice.md,
  references/code-smells-and-refactoring-triggers.md (new).
- Vue: SKILL.md, references/30-clean-code-solid-vue.md, references/40-patterns-vue-quasar.md.
- Go: SKILL.md, references/60-design-patterns-kit-era.md.
- Artifacts: 4 distilled-notes files + this report.

## Validation

Header-order greps on all three catalogs: PHP Contents matches physical order (35 sections); Vue 20
pattern sections + diagnostic; Go map/table/sections consistent. Markdown-only change set; no executable
validation applicable.
