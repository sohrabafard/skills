Version-sensitive claims in this topic depend on [Vue and TypeScript sources and freshness](../05-sources-and-freshness.md).

## Strict flags, one at a time

`"strict": true` turns the group on. Know what each member catches, because the repair differs and because
a repo turning one off needs a reason you can evaluate.

| Flag | What it catches | The symptom when it is off |
|---|---|---|
| `strictNullChecks` | `null`/`undefined` used where a value is required | `Cannot read properties of undefined` in production, on the path that is rarely taken |
| `strictFunctionTypes` | a callback accepting a narrower parameter than the contract promises | a handler compiled against `MouseEvent` receiving a `KeyboardEvent` |
| `strictBindCallApply` | wrong argument types through `bind`, `call`, `apply` | silent `NaN` and `undefined` in argument-forwarding helpers |
| `strictPropertyInitialization` | a class field never assigned in the constructor | an `undefined` field on an object the type says is complete |
| `noImplicitAny` | a parameter or variable the compiler cannot infer | `any` spreading from one un-annotated callback across a module |
| `noImplicitThis` | `this` of unknown type | Options API and plain-function callbacks silently untyped |
| `useUnknownInCatchVariables` | `catch (e)` treated as `any` | `e.message` on a thrown string, at the moment the error path finally runs |
| `alwaysStrict` | non-strict-mode emit | accidental globals from a missing declaration |

Worth adding beyond the group, when the repo can absorb the diff: `noUncheckedIndexedAccess`, which makes
`arr[0]` be `T | undefined` and catches the empty-list case that every table page eventually hits;
`exactOptionalPropertyTypes`, which distinguishes an absent property from one explicitly set to `undefined`
and matters wherever a patch payload is built; and `noFallthroughCasesInSwitch`.

Turning a strict flag off repo-wide is a project decision, not a task decision. If a task cannot compile
under the repo's current flags, report the file and the error rather than relaxing the flag.
## Type-only imports and `verbatimModuleSyntax`

Import a type with `import type`, and a value with a plain `import`:

```ts
import type { Course, CourseId } from '@/domain/course'
import { courseApi } from '@/services/course-api'
```

With `verbatimModuleSyntax` on, the emitted JavaScript keeps exactly the import statements you wrote and
elides only those marked `import type`. A type imported without the marker survives into the bundle as a
real module reference, which turns a types-only file into a runtime dependency, and which can pull a boot
file, a store, or a Quasar plugin into a chunk that never needed it. The symptom is a circular-import
warning or a store initialising before Pinia is installed.

Rules that follow: type-only files export types only; a module that exports both a type and a value is
imported twice, once with `import type`; and `export type { ... }` is used for re-exports of types.
