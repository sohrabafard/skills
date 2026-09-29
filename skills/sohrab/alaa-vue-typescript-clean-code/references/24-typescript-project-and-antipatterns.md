# TypeScript project setup and antipatterns

Compiler configuration, module syntax, type augmentation for Vue and Quasar, and the bad practices with the
observable symptom of each. The type system itself is `22-typescript-type-system.md`.

Before any task using this skill, read [Fleet TypeScript compatibility](./24-typescript-project-and-antipatterns/10-fleet-typescript-line.md#the-fleet-typescript-line); its compiler compatibility constraints and consequences apply to every task.

## The fleet TypeScript line
When choosing or upgrading the fleet TypeScript compiler, read [Fleet TypeScript compatibility](./24-typescript-project-and-antipatterns/10-fleet-typescript-line.md) for fleet typescript compatibility.

## Strict flags, one at a time
When changing strict compiler options, read [Compiler and module settings](./24-typescript-project-and-antipatterns/20-compiler-and-module-settings.md) for compiler and module settings.

## Type-only imports and `verbatimModuleSyntax`
When reviewing type imports or emitted module dependencies, read [Compiler and module settings](./24-typescript-project-and-antipatterns/20-compiler-and-module-settings.md) for compiler and module settings.

## Declaration merging and module augmentation
When adding Vue, Quasar, router, or environment declarations, read [Module augmentation](./24-typescript-project-and-antipatterns/30-module-augmentation.md) for module augmentation.

## Bad practices, by observable symptom
When reviewing suspicious TypeScript constructs, read [TypeScript antipatterns](./24-typescript-project-and-antipatterns/40-antipatterns.md) for typescript antipatterns.
