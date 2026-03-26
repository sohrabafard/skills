# Package Boundary and Entrypoints

Use this file when the task touches internal packages or their import paths.

## Hard rules

- Root apps should consume package entrypoints, not package source files directly.
- Packages should expose stable dist outputs.
- Imports that reach into `packages/<name>/src/*` are boundary violations unless the repo explicitly allows them.

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
