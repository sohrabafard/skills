# Package-Manager Modes

Open this file to write or change a dependency specifier for an internal workspace package, or to run a filtered workspace command.

**Detect first; never assume a manager.** Read the lockfile that exists in the repository before giving any dependency-linking, command, or build-order advice. The manager decides the syntax, and a specifier written for the wrong manager installs a second copy of the package instead of linking the workspace one.

## The modes

- **pnpm** (`pnpm-lock.yaml` plus `pnpm-workspace.yaml`): internal dependencies use the **`workspace:*`** protocol — `"@alaa/<x>": "workspace:*"`, or `workspace:^` for a package that is also published. **Never write `link:` or a `file:`/relative path.** Members come from the `packages:` glob in `pnpm-workspace.yaml`. pnpm's isolated, non-flat `node_modules` means a package can import only what it declares, so declare every used dependency explicitly; an import that works because another package hoisted the dependency will break the moment that other package drops it.
- **Yarn Berry, v2 and later** (`.yarnrc.yml`): internal dependencies use `workspace:^` or `workspace:*`; commands are `yarn workspace <pkg> <script>` and `yarn workspaces foreach`.
- **Yarn classic, v1** and **npm**: internal dependencies are `link:` or `file:` specifiers, or `*` resolved through the root `workspaces` field; commands are `yarn workspace <pkg> <script>` and `npm -w <pkg> run <script>`.

*(The live `client` repository is pnpm: `pnpm-lock.yaml`, `pnpm-workspace.yaml` with `packages: ["packages/*"]`, `packageManager: "pnpm@11.10.0"`, and internal dependencies written `workspace:*`. `read: 2026-07-28`.)*

## Filter syntax, pnpm

The ellipsis direction is the part that gets written backwards. Verified against https://pnpm.io/filtering, `read: 2026-07-28`:

| Command | Selects |
|---|---|
| `pnpm --filter <pkg> <script>` | that package alone |
| `pnpm --filter "<pkg>..." build` | that package **and its dependencies**, direct and indirect — ellipsis *after* the name means downstream of the arrow, the things it needs |
| `pnpm --filter "...<pkg>" build` | that package **and its dependents**, direct and indirect — ellipsis *before* the name means the things that need it |
| `pnpm -r <script>` | every workspace member, in topological order |

Use `"<pkg>..."` before building a package, to guarantee its upstream `dist/` exists. Use `"...<pkg>"` after changing a package, to rebuild everything that consumes it. Reversing the two produces a build that succeeds and a consumer that is stale.

## Migration rule

When a package is ported from a repository using a different manager, rewrite its internal specifiers to the **target** manager before it lands. Porting into a pnpm workspace means every `link:../x` and `link:packages/x` becomes `workspace:*`. Carrying a `link:` into a pnpm workspace is a boundary defect, not a stylistic choice: it bypasses the workspace graph, so the ported package resolves a copied tree instead of the sibling that the rest of the repository builds.

The manager decides the *specifier*. It does not decide whether a shared runtime stays a peer; that is `references/20-peer-deps-dedupe-and-build-output.md`, and both rules apply at once.

`scripts/verify-package-entrypoints.mjs` asserts that every internal specifier matches the detected manager, so a carried-over `link:` fails a gate rather than waiting to be noticed.

## The frozen install

Every automated install uses the detected manager's frozen form: `pnpm install --frozen-lockfile`, `npm ci`, or `yarn install --immutable`. A run that modifies the lockfile fails. Where that gate sits in a pipeline, and every other pipeline concern, belongs to `/alaa-frontend-devops` (`$alaa-frontend-devops`), `references/20-ci-gates-and-predicates.md`.
