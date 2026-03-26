# Audit and Verification

Use this file as the final check for package-boundary work.

## Audit order

1. Search for package source imports from the root app.
2. Inspect the package manifest and build output shape.
3. Inspect peer dependency and bundler externalization rules.
4. Build the final app and inspect the final browser asset output.

## Minimum checks

- no root-app imports into package private source
- package public entrypoint still resolves
- no missing chunk errors for routes that use the package
- package assets exist in the final browser asset folder

## Reporting

Close out with:

- the boundary issue that was fixed
- the package or root-app contract that changed
- the final validation result
