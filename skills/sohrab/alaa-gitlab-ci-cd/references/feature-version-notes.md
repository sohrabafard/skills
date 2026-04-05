# Feature and version notes

Use this file only when the task depends on a specific GitLab or Runner version.

## High-value version checks

- `spec:inputs` is mature enough for modern reusable CI design, but very old GitLab versions may not support it. If the user gives no version, assume a modern GitLab 18.x baseline and mention that assumption.
- Job inputs are newer than classic pipeline inputs and can require a recent Runner. Verify before recommending them in production.
- `run` is not the safe default for production pipeline design. If a user asks about it, verify current status and prefer normal `script` jobs unless there is a clear reason.
- `identity`, `id_tokens`, and external `secrets` integrations are powerful but sometimes version- or platform-scoped. Check current docs before relying on them.
- Runner registration tokens are on the way out. Prefer runner authentication tokens and current runner-creation workflows.
- Some component-expression contexts and matrix features are still evolving. Verify before using them in reusable enterprise templates.

## How to write the answer when versions are unclear

Use this pattern:

1. State the assumed GitLab and Runner baseline.
2. Call out any feature that needs confirmation.
3. Give a fallback design that works on a broader baseline when possible.

Example:

- "This design assumes GitLab 18.x and Runner 18.x. If your fleet is older, keep the component structure but replace job inputs with classic variables."
