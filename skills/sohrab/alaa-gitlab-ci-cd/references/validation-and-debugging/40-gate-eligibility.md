# Gate eligibility

Open this guide when deciding which checker findings may block a pipeline. For version-sensitive claims, follow the [source map](../00-source-map.md).

## Gate-eligible versus advisory, and who chooses

`--fail-on-warnings` turns this skill's checker into something that can fail a
pipeline. This skill does not decide that it should.

- **Error severity** marks a finding that is wrong under every configuration:
  invalid `when`, a stage that does not exist, `cache:key:files` over its limit,
  a `${VAR:-default}` GitLab cannot expand, a `pull_policy` outside its own
  allowlist. These are gate-eligible on any project.
- **Warning severity** marks a finding whose correct handling depends on the
  project: an unpinned image, a bare `retry:`, an interruptible mutating job, a
  saturated resource group, an advisory check, an absent code gate. Whether each
  of these blocks is the calling skill's decision — `/alaa-frontend-devops` for a frontend repository,
  `/alaa-cicd-laravel-postgres` for a PHP or
  Laravel service.
- **Note severity** is never a gate. It marks something a reader should know.

When an answer proposes running either checker in a pipeline, state which
severity blocks and name the skill that decided it. A checker that can fail a
pipeline while nobody has written down what it is asserting is the same illusion
as an advisory job named like a gate.
