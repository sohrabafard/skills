# Consistency and naming rules

## Contents
- Why consistency matters
- What each mode does to naming
- Canonical naming rules
- Method and variable naming
- Boundary alignment rules
- Canonical Alaa conventions for normalization mode
- Refactor approach for naming changes
- Anti-patterns

## Why consistency matters
One-author consistency comes mostly from naming discipline, repeated layer roles, and predictable boundaries.

Whose convention wins is not decided here: `SKILL.md` owns the uniformity rule, and `refactor-modes.md` owns the blast radius each mode allows. This file owns the naming rules themselves — what a good name looks like, which names to replace, and what the Alaa targets are when normalization is the mode.

## What each mode does to naming
- In `scoped-soft`, `scoped-hard-contract-preserving`, and `whole-project-preserve-local`: start from the repository's existing dialect, choose one local term per concept, and clean inconsistency without importing a foreign naming family.
- In `whole-project-normalize-alaa`: converge on the canonical layer names from `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) where they fit, remove vague or duplicated naming families, and make repeated feature slices structurally alike across the repo. Persistence-name normalization in this mode is owned by `refactor-modes.md`.

## Canonical naming rules
- Use one domain term per concept. Pick `Student`, `SchoolPost`, `Tenant`, or `Profile`, then keep that term across related classes and tests.
- Prefer intention-revealing nouns for classes and verbs for methods.
- Use role suffixes only when they communicate a real role.
- Keep file names, class names, and namespaces aligned.
- Keep singular vs plural accurate.
- Rename vague names when the current mode allows it.

### Good class names
- `ProfileService`
- `SchoolPostRepository`
- `UpdateProfileRequest`
- `ProfileResource`
- `ProfileData`
- `SchoolPostFilterData`
- `VerifyStepUpCodeStrategy`
- `TenantId`
- `PublishInvoiceJob`

### Weak class names to replace
- `ProfileHelper`
- `CommonUtil`
- `DataManager`
- `BaseRepository`
- `Processor`
- `ThingService`
- `GeneralHandler`

## Method and variable naming
- Methods should read like actions or questions:
  - actions: `createProfile`, `publishInvoice`, `syncRoster`
  - booleans: `isExpired`, `hasStepUpProof`, `canModerate`
- Prefer concrete variable names over generic placeholders:
  - `tenantId`, `profileData`, `stepUpPurpose`, `schoolPosts`
  - avoid `data`, `item`, `obj`, `payloadData`, `tempValue` when a real name exists
- Name collections in plural and single items in singular.
- Keep abbreviations limited to established technical terms already used by the repo.

## Boundary alignment rules
Keep related artifacts centered on the same domain term.

Examples:
- `UpdateProfileRequest` -> `ProfileData` -> `ProfileService` -> `ProfileRepository` -> `ProfileResource`
- `ListSchoolPostsRequest` -> `SchoolPostFilterData` -> `SchoolPostService` -> `SchoolPostRepository` -> `SchoolPostResource`

If the repository uses a different stable family, keep that family in preserve-local modes. In normalization mode, converge toward one family.

## Canonical Alaa conventions for normalization mode
When the user explicitly requests `whole-project-normalize-alaa`, the default naming targets are:
- controller: `<Domain>Controller`
- service: `<Domain>Service`
- repository: `<Domain>Repository`
- DTO: `<Domain>Data`, `<Domain>FilterData`
- resource: `<Domain>Resource`
- policy: `<Domain>Policy`
- request validation: `<Action><Domain>Request` or a repository-consistent RESTful request name
- strategy: `<Concern>Strategy`
- factory: `<Concern>Factory`
- value object: the domain concept itself, such as `TenantId`, `EmailAddress`, `DateRange`, or `Money`
- job: `<Verb><Domain>Job`
- listener: `<EventOrIntent><Effect>Listener` when that style fits the repo

Do not force these names onto code that a companion skill explicitly structures differently.

## Refactor approach for naming changes
- Rename one concept family at a time.
- Keep public contracts stable unless the task explicitly allows broader changes.
- Update imports, docblocks, tests, docs, and Postman examples together when a rename affects them.
- Prefer mechanical, reviewable renames over mixed conceptual rewrites.
- When a generic class actually hides multiple responsibilities, split by responsibility before or during the rename.

## Anti-patterns
- Renaming only half of a concept family
- Introducing synonyms for the same business concept
- Using `Service`, `Manager`, and `Helper` interchangeably for the same role
- Adding suffixes to sound architectural without improving clarity
- Normalizing names across the repo without first choosing the correct task mode
