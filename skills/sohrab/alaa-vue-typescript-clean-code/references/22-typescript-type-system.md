# TypeScript type system, in Vue

The type system as a design tool: each section names the situation, shows the Vue-shaped form, and says
what the compiler catches once you have written it that way. Compiler flags, module syntax, augmentation,
and the antipattern catalogue are `24-typescript-project-and-antipatterns.md`.

The through-line: **a type earns its place by making a wrong program fail to compile.** A type that only
restates what the value already is costs maintenance and buys nothing.

## Discriminated unions and exhaustiveness

Use when a value has more than one shape and the shapes carry different data. The discriminant is a literal
field shared by every member.

```ts
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: AppError }
```

The payoff is at the use site: inside `if (state.status === 'success')` the compiler knows `state.data`
exists, and outside it the compiler refuses to read `data`. The shape that makes this work is one literal
discriminant on every member — a union of `{ data?: T; error?: AppError }` with optional fields narrows
nothing and pushes every consumer into non-null assertions.

Close every branch over a union with `assertNever`, so adding a member becomes a compile error rather than
a silent fall-through:

```ts
function assertNever(value: never): never {
  throw new Error(`Unhandled variant: ${JSON.stringify(value)}`)
}

function label(state: AsyncState<Course>): string {
  switch (state.status) {
    case 'idle': return ''
    case 'loading': return 'Loading'
    case 'success': return state.data.title
    case 'error': return state.error.message
    default: return assertNever(state)
  }
}
```

`assertNever` is defined once per repository and imported. Its runtime `throw` is the second line of
defence for data that arrived from outside the type system; the compile error is the first.

In a template, branch on the discriminant, not on derived booleans: `v-if="state.status === 'error'"` is
checked, `v-if="hasError"` is not.

## Narrowing and type predicates

Prefer narrowing the compiler already understands: `typeof`, `instanceof`, `in`, a literal comparison, a
truthiness check on a nullable. Reach for a user-defined predicate only at a boundary where none of those
express the check.

```ts
export function isAppError(value: unknown): value is AppError {
  return typeof value === 'object' && value !== null && 'code' in value && typeof (value as { code: unknown }).code === 'string'
}
```

A predicate is a promise the compiler cannot verify — it trusts your `boolean`. So a predicate body checks
every field the type claims, and a predicate that checks one field of a five-field type is a cast wearing a
costume. Prefer an assertion function when the caller should not continue at all on failure:

```ts
export function assertIsCourse(value: unknown): asserts value is Course { /* throws otherwise */ }
```

Symptom that narrowing is missing: a chain of `?.` and `!` on the same expression. Narrow once into a local
`const` and the rest of the block reads plainly.

## `unknown` versus `any`, and the adapter rule

`unknown` accepts anything and permits nothing until you narrow. `any` accepts anything and permits
everything, including the typo three files away, and it spreads silently through every value derived from
it.

The rule: **untyped data enters as `unknown` and leaves the adapter as a declared domain type.**

```ts
// src/adapters/legacy-upload.adapter.ts — the only file permitted an `any`.
// legacy-upload-sdk@2.4.1 ships no types.
import type { UploadResult } from '@/domain/upload'

export function toUploadResult(raw: unknown): UploadResult {
  if (!isRawUploadResult(raw)) throw new UploadContractError(raw)
  return { id: raw.upload_id, sizeBytes: raw.size, uploadedAt: raw.uploaded_at }
}
```

One adapter per foreign boundary, holding the narrowing, the field renaming, and the error translation.
Components and stores import the domain type and never see the foreign one. `SKILL.md` states the
invariant; this is its shape.

## Generics and constraints in composables

A generic is right when the composable's behaviour is identical for every `T` and only the data type
varies. If the body has to branch on what `T` is, it is not generic — it is two functions.

```ts
export function useSelection<T, K extends PropertyKey>(
  items: MaybeRefOrGetter<readonly T[]>,
  keyOf: (item: T) => K,
) {
  const selectedKeys = ref(new Set<K>()) as Ref<Set<K>>
  const selected = computed(() => toValue(items).filter(item => selectedKeys.value.has(keyOf(item))))
  function toggle(item: T) { /* ... */ }
  return { selectedKeys, selected, toggle }
}
```

What the constraints buy: `K extends PropertyKey` refuses an object key at the call site, and `keyOf`
means the composable never guesses that the id field is called `id`. What to avoid: a type parameter used
exactly once in the signature — it is a slower way to write `unknown`; and a default type parameter
(`<T = any>`) that silently disables the check for every caller who omits it.

Constrain to what you actually read: `<T extends { id: string }>` when you read `item.id`, not
`<T extends BaseEntity>` when `BaseEntity` has fourteen fields you ignore. The narrower constraint accepts
more real call sites.

## `satisfies`

Use when a value must conform to a type **and** keep its own narrower inferred type. The classic case is a
registry that must be exhaustive but whose keys you still want to read as literals:

```ts
const statusColor = {
  draft: 'grey',
  published: 'positive',
  archived: 'warning',
} satisfies Record<CourseStatus, QuasarColor>
```

`: Record<CourseStatus, QuasarColor>` would check exhaustiveness but widen every value to `QuasarColor`, so
`statusColor.draft` would no longer be the literal `'grey'`. `as` would keep the literals but check
nothing. `satisfies` gives both, and a new `CourseStatus` member breaks this line at compile time.

Use it for Quasar column definitions, route meta objects, form schemas, and any typed option table.

## Template-literal and mapped types

Reach for these where the relationship between two types is mechanical — otherwise write the type out.

```ts
type CourseEvent = `course:${'created' | 'updated' | 'archived'}`

type Handlers<T extends { kind: string }> = {
  [K in T['kind']]: (node: Extract<T, { kind: K }>) => void
}
```

`Handlers<Node>` gives one handler map that is exhaustive over `Node['kind']` and correctly typed per
member — the same guarantee as `assertNever`, obtained at the type level, which is why the per-operation
handler map in `43-behavioral-patterns.md` is written this way.

Where they earn their place: deriving `update:${keyof Props & string}` emit names, deriving a handler map
from a node union, and modifiers such as `Readonly<T>` and `Partial<T>` over your own types. Where they do
not: parsing strings at the type level for display purposes, and any type whose error message a colleague
cannot read.

## Branded and opaque types for identifiers

Two ids that are both `string` are interchangeable to the compiler, so passing a `courseId` where a
`userId` belongs compiles and fails at runtime with a 404. Brand them:

```ts
declare const brand: unique symbol
type Brand<T, B extends string> = T & { readonly [brand]: B }

export type CourseId = Brand<string, 'CourseId'>
export type UserId = Brand<string, 'UserId'>

export function toCourseId(raw: string): CourseId { /* validate, then return raw as CourseId */ }
```

The only cast is inside the one constructor function that validates. Brand the ids that appear in more
than one function signature and that could be swapped without a type error — route params, entity ids,
tenant ids. Do not brand a value used once and locally.

Identifier *encoding* — the alphabet, the checksum, the canonical form — is not this skill's:
`/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) owns it, and
`72-frontend-security-binding.md` states when its conformance script must run.

## `readonly` and immutability

`readonly T[]` and `Readonly<T>` on a function parameter say the function will not write to it, and the
compiler enforces it. Use them on props (`items?: readonly Course[]`), on anything returned from a store
getter that callers should not mutate, and on module-level constant tables.

`readonly` is shallow and it is compile-time only. `Object.freeze` is the runtime counterpart, worth using
on a preset registry that ships to many call sites. Neither protects a reactive proxy from being written
through a different reference, so ownership of mutation still lives with the store or composable that owns
the state.

## Utility types worth knowing

`Pick` and `Omit` to build a narrow port from a wide type — `Pick<Router, 'replace'>` as a test seam is the
canonical Vue use. `Partial` for patch payloads and for draft state. `Required` and `NonNullable` after a
validation step. `Record<K, V>` for registries, usually with `satisfies`. `Extract` and `Exclude` to select
union members. `Parameters` and `ReturnType` to stay in step with a function you do not own. `Awaited` for
the resolved type of a promise-returning API.

The rule that keeps these honest: **a derived type follows the source, so derive when the two must change
together, and write it out when they must not.** `Omit<CourseDto, 'id'>` as a create payload is right only
if the create payload genuinely is the DTO minus the id; the day it diverges, the derived type lies and the
compiler agrees with it.
