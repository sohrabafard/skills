# TypeScript project setup and antipatterns

Compiler configuration, module syntax, type augmentation for Vue and Quasar, and the bad practices with the
observable symptom of each. The type system itself is `22-typescript-type-system.md`.

## The fleet TypeScript line

**TypeScript 6 is the line this fleet builds on, with Quasar + Vue + `@quasar/app-vite` v3. TypeScript 7 and
its native compiler are not adopted, because Quasar has not declared support for TypeScript 7.** That is the
reason, and it is written down so a future agent knows exactly what would change the rule: a support
statement from Quasar, not a release announcement from TypeScript.

Consequences that bind every task:

- Typechecking is `vue-tsc --noEmit`, exactly as `60-validation-gates.md` prescribes. Do not substitute a
  different typechecker, and do not add a second one alongside it.
- Write no guidance, no config, and no migration note for the native compiler anywhere in a repository this
  skill governs. Proposing it is a finding, not a suggestion.
- If a task's premise depends on TypeScript 7 behaviour, stop and report the conflict rather than
  implementing against an unsupported toolchain.

Keep `tsconfig` strictness explicit rather than inheriting whatever a major version turned on by default,
so an upgrade changes the build in one reviewable diff instead of silently.

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

## Declaration merging and module augmentation

Augmentation is how a Vue or Quasar type gains a field your repo needs, in one place, with the compiler
enforcing it everywhere.

Route meta — this is what makes `meta.requiresAuth` a checked field rather than a hopeful one:

```ts
// src/types/router.d.ts
import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    permissions?: readonly PermissionKey[]
  }
}
```

Vite environment variables, so `import.meta.env.VITE_API_BASE_URL` is typed and a missing one is a compile
error:

```ts
// src/types/env.d.ts
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
}
interface ImportMeta { readonly env: ImportMetaEnv }
```

Global component properties added by a boot file, so `this.$myThing` and template usage type-check:

```ts
declare module 'vue' {
  interface ComponentCustomProperties {
    $formatCurrency: (value: number) => string
  }
}
```

Rules: augmentations live in `src/types/*.d.ts` and are included by `tsconfig`, never scattered beside
feature code; an augmentation file that contains a top-level `import`/`export` becomes a module, so
`declare module` inside it is the augmentation form and `declare global` is needed for true globals; and an
augmentation only ever adds — narrowing or redefining an upstream member breaks at the next upgrade in a
way that is very hard to trace.

Which environment variables may exist at all, and which are forbidden, is
`72-frontend-security-binding.md`. Global component properties added by boot files are
`50-quasar-vite-pinia-contract.md`.

## Bad practices, by observable symptom

Each row is something you can see in a diff. Seeing it is the finding; the repair is stated.

**The non-null assertion used as a silencer.** Symptom: `!` appearing after an expression that the compiler
just complained about, often more than once in a line — `props.user!.profile!.name`. What it means is "the
compiler is wrong", and it is usually the compiler being right about a loading state. Repair: narrow once
into a local, or model the absence in the type (`AsyncState<User>`), or return early. A `!` is acceptable
only where a runtime invariant is established one or two lines above and visible in the same function, such
as immediately after an `assertIsCourse` call.

**The cast chain through `unknown`.** Symptom: `value as unknown as Course`. The `as unknown` step exists
purely to defeat the compiler's refusal to cast between unrelated types, so this construct means "I have no
evidence". Repair: a type predicate that checks the fields, inside the adapter that owns the boundary
(`22-typescript-type-system.md`).

**An `enum` where a `const` object belongs.** Symptom: `enum Status { ... }` in application code. A
numeric enum admits any number at the call site; enums emit runtime code and interact badly with
`isolatedModules` and type-only imports; and their members are not assignable from the plain literals that
arrive over the wire. Repair:

```ts
export const COURSE_STATUS = { draft: 'draft', published: 'published' } as const
export type CourseStatus = (typeof COURSE_STATUS)[keyof typeof COURSE_STATUS]
```

**An interface that mirrors an implementation.** Symptom: a port whose method list matches a vendor SDK's
method list, name for name, or that has exactly one implementation and one consumer and changes whenever
the implementation changes. It buys no substitutability and costs a file. Repair: define the port as the
three things the UI actually needs, in domain words — the port belongs to the consumer
(`30-clean-code-solid-vue.md`) — or delete it and call the module directly.

**`@ts-ignore`.** Symptom: any occurrence. Repair: `@ts-expect-error` instead, because it fails the build
when the underlying cause is fixed, so the suppression cannot outlive its reason. Every suppression carries
a line-scoped comment naming the lint rule or error and the upstream issue or library version that forces
it; a suppression with no named cause is removed rather than annotated.

**`Function`, `object`, and `{}` as parameter types.** Symptom: any of the three in a signature. They
accept almost everything and describe almost nothing — `{}` accepts every non-nullish value. Repair: a
call signature (`(id: CourseId) => void`), `Record<string, unknown>`, or `unknown` plus narrowing.

**A `try/catch` that returns a default.** Symptom: `catch { return [] }`. It converts a failure into an
empty screen with no error path, and the user sees "no results" for an outage. Repair: classify the
failure and surface it — `70-async-and-failure-binding.md`.
