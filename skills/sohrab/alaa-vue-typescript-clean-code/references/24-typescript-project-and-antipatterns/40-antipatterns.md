Version-sensitive claims in this topic depend on [Vue and TypeScript sources and freshness](../05-sources-and-freshness.md).

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
(`../22-typescript-type-system.md`).

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
(`../30-clean-code-solid-vue.md`) — or delete it and call the module directly.

**`@ts-ignore`.** Symptom: any occurrence. Repair: `@ts-expect-error` instead, because it fails the build
when the underlying cause is fixed, so the suppression cannot outlive its reason. Every suppression carries
a line-scoped comment naming the lint rule or error and the upstream issue or library version that forces
it; a suppression with no named cause is removed rather than annotated.

**`Function`, `object`, and `{}` as parameter types.** Symptom: any of the three in a signature. They
accept almost everything and describe almost nothing — `{}` accepts every non-nullish value. Repair: a
call signature (`(id: CourseId) => void`), `Record<string, unknown>`, or `unknown` plus narrowing.

**A `try/catch` that returns a default.** Symptom: `catch { return [] }`. It converts a failure into an
empty screen with no error path, and the user sees "no results" for an outage. Repair: classify the
failure and surface it — `../70-async-and-failure-binding.md`.
