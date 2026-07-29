---
name: ansible-generator
description: Generate production-ready Ansible playbooks, roles, task files, inventories and project scaffolding with FQCN-correct modules, idempotent tasks, declared role interfaces and explicit file modes, then hand the result to the validator. Use when a file that does not yet exist has to exist when you are done. Do not use when every file you need already exists and your job is to produce a verdict about it (use /ansible-validator, $ansible-validator), for Terraform, Helm, Dockerfile or CI authoring unless Ansible is the main artifact, or for one-off shell automation that should stay a script.
---

# Ansible Generator

## Overview

Generate Ansible content that parses, is idempotent, and passes the validator on
the first run. This `SKILL.md` is the router; the procedure is
`references/playbook.md`. Load reference files by skill-relative path.

## Source freshness

Version-sensitive claims are `ansible-validator references/source-map.md`
(`/ansible-validator`, `$ansible-validator`), which carries every pinned value
and the command that re-derives it. For a module name look nothing up: run
`python3 <ansible-validator>/scripts/check_module_currency.py <path>`, which
reads ansible-core's routing table offline.

## When NOT to use

The deciding test between this skill and its sibling: **does a file that does
not yet exist have to exist when you are done? If yes, `/ansible-generator`
(`$ansible-generator`). If every file you need already exists and your job is to
produce a verdict about it, `/ansible-validator` (`$ansible-validator`).**

Also not for Terraform, Helm, Dockerfile or CI authoring unless Ansible is the
main artifact, nor for one-off shell automation that should stay a script.

## Workflow

1. Establish the artifact type, the host group, the OS families that must work,
   and which tasks need privilege escalation.
2. Read `references/best-practices.md` for the task shape and
   `references/module-patterns.md` to pick the module.
3. Start from `assets/templates/`; `references/scaffold.md` states the
   placeholder convention and the substitution commands.
4. Write idempotent tasks: fully qualified actions, an end state, an explicit
   quoted `mode`, role-prefixed variables, a handler per restart, tags.
5. Run the delivery gate: `python3 scripts/check_templates.py <files>`, then the
   validator's `validate_playbook.sh` or `validate_role.sh`, `scan_secrets.sh`
   and `check_task_safety.py`. **Exit 0 from every one is the only pass; exit 2
   means a check could not run and is reported as blocked.** If two consecutive
   fix-and-re-run cycles do not reduce the failure count, stop and report.
6. Deliver in the format at `references/playbook.md` section 7: checks, summary,
   usage command, prerequisites.

## Boundaries

This skill owns the bytes. `references/playbook.md` section 8 states each seam
in full; the one-line form:

- **Verdicts, and everything a checker can test,** are `/ansible-validator`'s
  (`$ansible-validator`): the ruleset, variable precedence, the module-name
  mapping, both lint configs, Molecule, the security predicates, Vault
  mechanics, check mode, the source map and the test corpus.
- **CI:** `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns the job. The boundary
  is the `ansible-playbook` command line — the arguments are that skill's,
  everything the command reads is this one's.
- **Containers:** `/alaa-docker-production` (`$alaa-docker-production`) owns the
  Dockerfile and the Compose file, including the fail-closed `${VAR:?}`
  invariant; this skill owns the host state a play manages around them.
- **Kubernetes:** `/alaa-k8s-helm` (`$alaa-k8s-helm`) owns the manifest; this
  skill writes the `kubernetes.core.k8s` task that applies it.
- **Proxy:** `/alaa-haproxy` (`$alaa-haproxy`) chooses the directives; this
  skill owns the `template:` task, its `validate:` argument and the handler.
- **Fail-closed** is `/alaa-security-review`'s (`$alaa-security-review`): a play
  that cannot decrypt a vault stops.
- **Retry, timeout, `serial`, `forks`, degradation** are
  `/alaa-reliability-sla`'s (`$alaa-reliability-sla`). Write the mechanism; let
  that skill pick the number.
- **Model and effort settings** are `/alaa-prompting-guide`'s
  (`$alaa-prompting-guide`), at `references/50-effort-and-thinking.md`. No
  emitted artifact carries a model key.

## Reference map

| File | Read it when |
|---|---|
| `references/playbook.md` | generating anything: procedure by artifact type, the gate, the delivery format |
| `references/best-practices.md` | before the first task; the authoring rules and what this skill does not decide |
| `references/module-patterns.md` | choosing a module; copy-ready usage by operation |
| `references/jinja-and-lookups.md` | writing a Jinja template, a filter chain or a lookup |
| `references/scaffold.md` | creating a role, playbook, inventory or project from `assets/templates/` |
