# Build Contract and Artifacts

Use this file when the task touches build output shape, artifact locations, public asset paths, or SSR runtime delivery.

## Core contract

- The final browser assets must land in the client asset output for the deployed build.
- If the repo uses SSR, the runtime entry path must stay stable unless maintainers explicitly change the contract.
- Do not silently change the public base path, asset prefix, or chunk location.
- Treat missing chunks, bad asset URLs, and asset paths that escape the final client asset root as deployment-critical failures.

## Practical audit order

1. Inspect the build config that decides output paths and public path.
2. Inspect the pipeline or release job that uploads or ships build artifacts.
3. Inspect Docker or runtime packaging if the built files are copied into an image.
4. Verify the exact output tree after a build instead of assuming the config is enough.

## Frontend-specific non-negotiables

- Keep SSR builds deterministic.
- Do not break the final asset output by moving package assets out of the bundling graph.
- Do not move runtime-only files into browser-visible outputs unless required.
- Do not change root package-manager scripts unless maintainers explicitly ask for that change.

## Typical failure modes

- `publicPath` or base-path drift between local and deployed environments
- CI uploading the wrong folder
- Docker copying partial outputs and omitting browser assets
- package assets emitted outside the final client asset folder
- reverse proxy rewriting paths in a way that breaks hashed chunks

## Minimum verification

- Run a build that matches the deployment mode closely enough to verify the final file tree.
- Confirm the expected SSR runtime entry exists when SSR is enabled.
- Confirm the expected browser asset folder contains the built chunks and assets that the app needs.
- If the task mentions a missing chunk, verify the final output tree before assuming it is a runtime-only problem.
