# Protected and file variables

Open this guide when checking masking, protection or file-variable paths. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Masked, protected and file variables

**Masked variables.** Masking replaces the literal value in the log. It does not
survive transformation: shell tracing prints expanded arguments, `base64` output
is not the masked string, and a value split across lines is not matched. Do not
rely on a masked value to expand another variable safely.

**Protected variables.** Available only to jobs on protected refs. Whenever a
design uses one, state whether the jobs that need it actually run on protected
refs, and test `$CI_COMMIT_REF_PROTECTED == "true"` rather than assuming the
default branch is protected.

**File variables.** GitLab writes the value to a temp file and sets the variable
to that path. Consume it as a path. Do not `cat` it into a log to check it.
