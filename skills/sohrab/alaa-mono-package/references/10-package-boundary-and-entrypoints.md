# Package Boundary and Entrypoints

Use this file when the task touches internal packages or their import paths.

## Hard rules

- Before changing or auditing a package, read the package-local `AGENTS.md` if it exists, even when the current shell stays at the repo root.
- If the user declares a clean-island package lane, write only inside the named package or package family. Treat sibling packages, the root app, legacy files, and root config as read-only until the user explicitly widens scope.
- Root apps should consume package entrypoints, not package source files directly.
- Packages should expose stable dist outputs.
- Imports that reach into `packages/<name>/src/*` are boundary violations unless the repo explicitly allows them.
- Internal dependency specifiers follow the repo's package manager: in a **pnpm** workspace use `workspace:*` (never a yarn `link:` or a `file:`/relative path); rewrite any `link:` carried over from a yarn repo to `workspace:*` before the package lands.

## Why this matters

- direct source imports bypass package contracts
- asset handling can diverge between package builds and app builds
- externalization and dedupe rules become harder to enforce

## Good pattern

- import from the package name or the documented dist entrypoint
- keep package public surface small and explicit

## Bad pattern

- reaching into private package internals from the root app
- relying on unbuilt package source files as if they were stable public API
