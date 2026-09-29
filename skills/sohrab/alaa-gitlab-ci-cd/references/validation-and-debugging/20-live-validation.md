# Live GitLab validation

Open this guide when the task involves merged configuration or project-context CI Lint. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Live GitLab validation

```bash
glab ci lint
glab ci lint .gitlab-ci.yml --dry-run --include-jobs
glab ci lint path/to/pipeline.yml --dry-run --include-jobs --ref main
```

Use the CI Lint API when you need merged-configuration inspection from a script,
or pipeline simulation when includes, local project files or project context
matter. This is the only local-ish check that resolves `include:`.
