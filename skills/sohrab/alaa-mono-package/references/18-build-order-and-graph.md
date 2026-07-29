# Build Order and the Dependency Graph

Open this file to decide the order in which packages build, when a build read an upstream `dist/` that was not there, or when two parallel builds produce different output for the same commit.

## Name the structure

The workspace is a **directed acyclic graph**: nodes are packages, edges are internal dependencies. Build order is a **topological order** of that graph. Saying so is not pedantry — it tells you what the failure modes are, because a graph algorithm has exactly three: a missing node, a wrong order, and a cycle.

The complexity of any traversal you write over this graph, and the structure to hold it in, belong to `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`). This file states what the graph is and what must hold of it.

## The order

Framework-free core and model packages, then domain packages and adapters, then aggregate packages, then UI packages, then the playground and the root application. Derive it from the graph rather than maintaining that list by hand: a hand-maintained order is correct until someone adds an edge.

- Under pnpm, `pnpm -r build` runs the whole graph in topological order and `pnpm --filter "<pkg>..." build` builds a package after everything it depends on. Prefer these to a hand-written order script. Which manager's commands apply is `references/15-package-manager-modes.md`.
- The live `client` repository runs `nx run-many -t build` as `packages:build`, and makes it a `pre` hook of both `dev` and `build`, so the graph is built before the application in every entry point (`read: 2026-07-28`).

## Upstream `dist/` must exist before a consumer builds

A package's `build` script must not read an upstream package's `dist/` without that upstream having been built. Source aliases, test aliases, and `tsconfig` path mappings hide this: they let the package's own tests pass against upstream *source* while the built artifact resolves upstream *`dist/`*, which may be absent, stale, or from a different commit.

Rule: a package-local `build` or `check` script either builds its required upstream packages first, or exits non-zero naming the specific upstream package whose `dist/` is missing. Exiting zero with a stale artifact is the failure this rule exists to prevent, and "fail with a clear message" is not a rule — the message must name the package.

After building a consumer package, import its built entrypoint from `dist/` and then check its CSS and assets. A package that passes its source tests and fails as a dist-only consumer is the normal case, not an unusual one.

## Cycles

A cycle between two internal packages is a defect, not a configuration to work around. Its symptoms are: a build order that differs between two runs; one package building against the other's previous output; and a `dist/` whose contents depend on which package happened to build first.

Rule: the internal dependency graph is acyclic. Detect a cycle by depth-first traversal marking each node unvisited, in-progress, or done — an edge to an in-progress node is a cycle. Report the full cycle path, not just the edge that closed it. Break it by extracting the shared surface into a third package that both depend on; do not break it by importing a source path, which trades a detectable cycle for an undetectable boundary violation.

Under pnpm, `pnpm -r` will refuse to order a cyclic graph, so a cycle usually surfaces as a build that cannot start rather than one that produces wrong output. Do not read that refusal as a tooling problem.

## Parallel builds on a shared output

This skill contemplates parallel package lanes, so it must state what happens when two of them build at once.

**Symptom:** a `dist/` containing files from two different commits; a build that succeeds on one run and fails on the next with no source change; a consumer resolving an entrypoint that no single build ever emitted.

**Cause:** two processes writing the same package's `dist/` concurrently, or one process reading a `dist/` while another is mid-write. A build is not atomic: it deletes, then writes, and a reader arriving between the two sees an empty or partial tree.

**Rules:**

1. One package's `dist/` has exactly one writer at a time. Two agents in parallel lanes must not both hold a package whose `dist/` the other's build reads. Establish that before either starts, per the lane guard in `SKILL.md`.
2. A build that must be safe against a concurrent reader writes to a temporary directory **outside the package** and renames it into place, so a reader sees either the old tree or the new one and never a partial one.
3. Where a build tool provides its own concurrency control, use it and name it. Nx and pnpm each serialise a given target for a given project; that serialisation is the interlock, and relying on it is correct as long as both lanes go through the same tool. Two agents running two different tools against one workspace have no interlock at all.
4. The equivalent interlock for publishing a built artifact belongs to `/alaa-frontend-devops` (`$alaa-frontend-devops`), `references/20-ci-gates-and-predicates.md`. It is a different lock on a different resource; do not assume one covers the other.
