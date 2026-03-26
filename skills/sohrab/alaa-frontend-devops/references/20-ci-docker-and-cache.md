# CI, Docker, and Cache Discipline

Use this file when the task changes CI pipelines, dependency install layers, Docker builds, or reproducibility rules.

## CI rules

- Keep the pipeline deterministic.
- Cache by lockfile and toolchain version, not by wishful broad reuse.
- Prefer explicit runtime versions for Node and package managers.
- Treat asset-producing steps as contract-sensitive; verify outputs, not just exit codes.

## Docker rules

- Keep dependency install layers driven mainly by manifest files and lockfiles.
- Avoid invalidating dependency layers on source-only changes.
- Separate build-time tooling from the runtime image whenever the repo architecture supports it.
- Keep images minimal and predictable.

## Cache-safety checklist

- If lockfiles change, cache keys must change.
- If Node or package-manager versions change, cache keys must change.
- If a workspace package manifest affects install resolution, it belongs in the dependency layer inputs.
- Do not treat stale caches as harmless when debugging missing assets or broken build output.

## Good defaults

- Yarn-first when the repo is already Yarn-based
- explicit Node version
- explicit install command
- explicit build command
- explicit artifact verification step

## Anti-patterns

- floating toolchain versions in CI
- upload jobs that assume a folder exists without checking
- Docker layers that copy the full repo before dependency install
- "fixes" that delete caches without addressing the real cache-key problem
