# Symptoms and cross-file debugging

Open this guide when matching a literal symptom or tracing an include graph. For version-sensitive claims, follow the [source map](../00-source-map.md).

## Symptom map

| Literal message | Class | First thing to check |
|---|---|---|
| `job is pending, no runners` | 3 | job `tags:` against runner tags |
| `no stages / stage does not exist` | 1 | `stages` list and the job's `stage` |
| `config should be an array of hashes` | 1 | a mapping written where a list belongs |
| `timed out waiting for pod to start` | 4 | cluster capacity, webhooks, `poll_timeout` |
| `Cannot connect to the Docker daemon` | 4 | DinD alias, port, privileged mode, TLS variables |
| `unauthorized: authentication required` | 4 or 5 | registry credentials, job-token scope, `image_pull_secrets` |
| `ErrImagePull` / `ImagePullBackOff`, no job log | 4 | `image_pull_secrets` on every container in the job pod |
| variable empty only in a merge request pipeline | 5 | protected variable against `$CI_COMMIT_REF_PROTECTED`, or fork pipeline |
| a green job that did nothing | 2 | a script-level `exit 0` where a `rules:` condition belonged |

## Debugging across multiple files

- Validate each file statically, then validate the merged result in project
  context; only the merged result knows what `include:` produced.
- Show the include graph in the answer.
- Debug parent and child pipelines as separate problems.
- Re-running a job uses the configuration that created its pipeline. To test a
  configuration change, start a new pipeline.
