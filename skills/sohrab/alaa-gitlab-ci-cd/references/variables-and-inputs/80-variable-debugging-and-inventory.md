# Variable debugging and inventory

Open this guide when diagnosing an unexpected variable value or recording custom values. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Debugging an unexpected value

Check in this order, and stop at the first answer:

1. Was the variable created at the scope you expected — instance, group, project,
   pipeline, job?
2. Is a higher-precedence source overriding it?
3. Is the job running on a ref that can read protected variables?
4. Is the value masked or hidden in a way that prevents safe expansion?
5. Is it unavailable when rules are evaluated, or using unsupported shell-style
   defaults in a `variables:` value?
6. Is the job actually running in a downstream or child pipeline with different
   inheritance?

## Variable inventory template

Publish this table in the answer whenever the design introduces a custom value.

| Name | Type | Source | Sensitive | Default | Consumed by |
| --- | --- | --- | --- | --- | --- |
| `IMAGE_TAG` | variable | pipeline or `default:` | no | `$CI_COMMIT_SHA` | build job |
| `KUBECONFIG` | file variable | project | yes | none — job fails if unset | deploy job |
| `VAULT_ID_TOKEN` | id_token | per job | yes | n/a | secrets fetch |

A value with no default and a stated "job fails if unset" is a deliberate
fail-closed choice. Say so in the table rather than inventing a default. Where the
name is also read by another service, it is a shared name and
`/alaa-services-contract` owns it.
