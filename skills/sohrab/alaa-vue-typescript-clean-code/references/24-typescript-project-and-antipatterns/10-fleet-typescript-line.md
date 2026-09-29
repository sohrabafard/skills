Version-sensitive claims in this topic depend on [Vue and TypeScript sources and freshness](../05-sources-and-freshness.md).

## The fleet TypeScript line

**Keep TypeScript 6 for this fleet's Quasar + Vue + `vue-tsc` toolchain.** TypeScript 7 is stable,
but its 7.0 release lacks a stable programmatic API. Microsoft's
[release guidance](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)
explicitly keeps Vue/Volar workflows on TypeScript 6 (read 2026-09-29). This is a tooling
compatibility constraint, not a claim that TypeScript 7 is a preview.

Consequences that bind every task:

- Typechecking is `vue-tsc --noEmit`, exactly as `../60-validation-gates.md` prescribes. Do not substitute a
  different typechecker, and do not add a second one alongside it.
- Do not replace the installed compiler or editor service merely because a newer stable release exists.
- For an explicit TypeScript 7 migration, first verify version-matched Vue language-tools, Quasar and
  plugin compatibility. If unavailable, report the blocker and retain TypeScript 6. Once supported,
  require the consumer's SFC typecheck, editor diagnostics and production build before adoption;
  an upstream release alone proves none of them.

Keep `tsconfig` strictness explicit rather than inheriting whatever a major version turned on by default,
so an upgrade changes the build in one reviewable diff instead of silently.
