# Pipeline authoring

Which pipeline exists, which jobs are in it, and how the file is composed. Which
job runs when is `job-graph-and-scheduling.md`; cache and artifact expression is
`cache-artifacts-and-pinning.md`.

## Table of contents

- Authoring defaults
- `workflow:rules` and job `rules:`
- `rules:changes` and path filters
- Environments and rollback
- Reuse: hidden jobs, `extends`, `!reference`, includes and components
- Child pipelines and multi-file layouts
- Authoring checklist

## Authoring defaults

When setting pipeline authoring defaults, use [Authoring defaults](./pipeline-authoring/20-authoring-defaults.md).

## `workflow:rules` and job `rules:`

When deciding whether a pipeline or job is created, use [Pipeline creation and path rules](./pipeline-authoring/10-pipeline-creation-and-paths.md).

## `rules:changes` and path filters

When selecting jobs by changed paths, use [Pipeline creation and path rules](./pipeline-authoring/10-pipeline-creation-and-paths.md).

## Environments and rollback

When recording deployments or rerunning an earlier deployment, use [Environments and rollback](./pipeline-authoring/30-environments-and-rollback.md).

## Reuse: hidden jobs, `extends`, `!reference`, includes and components

When composing reusable jobs or pipeline files, use [Reuse and composition](./pipeline-authoring/30-reuse-composition.md).

## Child pipelines and multi-file layouts

When coordinating child pipelines or multiple files, use [Child pipelines and checklist](./pipeline-authoring/40-child-pipelines-and-checklist.md).

## Authoring checklist

Before completing pipeline authoring, use the [authoring checklist](./pipeline-authoring/40-child-pipelines-and-checklist.md).
