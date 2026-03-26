# Annotation Boundaries

Use this file before editing anything.

## Hard rule

This skill is for documentation-only diffs.

Allowed changes:

- JSDoc blocks
- file-level explanatory headers
- narrow inline comments that explain non-obvious reasoning

Not allowed:

- logic changes
- template structure changes
- CSS or style changes
- behavior changes hidden behind "comment cleanup"

## Good targets

- boot files
- store actions or mutations
- fetch wrappers
- SSR data-loading code
- lifecycle-heavy components
- code that bridges auth or hydration concerns

## Bad targets

- obvious one-line assignments
- large blocks of repetitive comments
- comments that only restate the code
- comments inside templates unless the repo explicitly wants them

## Safety checks

- Re-open the target file before editing if time has passed.
- If the file is actively changing for unrelated reasons, avoid mixing documentation edits into it.
- Keep comment wording simple and stable across future refactors.
