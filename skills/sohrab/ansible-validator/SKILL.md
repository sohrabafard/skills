---
name: ansible-validator
description: Validate, lint, security-audit and dry-run existing Ansible playbooks, roles, collections and inventories with ansible-lint, yamllint, check mode, Checkov and Molecule, reporting a verdict with per-finding remediation citations. Use when every file you need already exists and your job is to produce a verdict about it. Do not use when a file that does not yet exist has to exist when you are done (use /ansible-generator, $ansible-generator), for Terraform, Helm, Dockerfile or CI-config validation unless Ansible is the main artifact, or for plain YAML edits with no Ansible semantics.
---

# Ansible Validator

## Overview

Validate existing Ansible content and report a verdict. This `SKILL.md` is the
router; the procedure is `references/playbook.md`, the enforcement is
`scripts/`. Load reference files by skill-relative path, never absolute.

## Source freshness

Read `references/source-map.md` before any version-sensitive claim: it carries
every pinned value and the command that re-derives it. Community posts explain
an observed failure; they do not establish that a module parameter exists.

## When NOT to use

The deciding test between this skill and its sibling: **does a file that does
not yet exist have to exist when you are done? If yes, `/ansible-generator`
(`$ansible-generator`). If every file you need already exists and your job is to
produce a verdict about it, `/ansible-validator` (`$ansible-validator`).**

Also not for Terraform, Helm, Dockerfile or CI-config validation unless Ansible
is the main artifact, nor for YAML with no Ansible semantics.

## What to run

Every script takes `--help` and `--self-test`. Exit codes are identical
throughout: `0` clean, `1` findings, `2` could not run, `64` usage. **`2` is a
hard stop for a gate, never a pass.** `references/playbook.md` holds the stage
table, the report format and the stopping condition.

| Command | Asserts |
|---|---|
| `setup_tools.sh` | the toolchain meets `scripts/requirements.txt` |
| `validate_playbook.sh <file>`, `validate_role.sh <dir>` | YAML, Ansible syntax, ansible-lint, role structure |
| `validate_playbook_security.sh`, `validate_role_security.sh` | Checkov `--framework ansible,secrets` is clean |
| `scan_secrets.sh <target>` | no credential literal, no alarm on a vaulted value |
| `check_fqcn.sh`, `check_module_currency.py` | actions are fully qualified, and to a live module |
| `check_task_safety.py <target>` | no world-writable mode, no unquoted Jinja in a shell |
| `check_assets.sh` | the lint configs still enable the rules they claim |
| `test_role.sh <dir> <scenario> --i-confirm-disposable-host` | a Molecule scenario applies, is idempotent, verifies |
| `extract_ansible_info_wrapper.sh`, `self_test.sh` | every file parses; every checker above passes |

## Workflow

1. `setup_tools.sh`. A floor not met is a blocked audit.
2. `validate_playbook.sh` or `validate_role.sh` on the target.
3. `check_fqcn.sh` and `check_module_currency.py`.
4. All three security commands, on every audit.
5. `--check --diff --limit <hosts>` when an inventory exists; a Molecule
   scenario only under the condition in `references/molecule.md`.
6. Report `PASS`, `FAIL` or `BLOCKED`, never a mixture, citing the reference
   line behind each finding.

## Boundaries

- **Authoring** is `/ansible-generator`'s (`$ansible-generator`): it owns the
  bytes, this skill owns the verdict. Jinja, lookups and module call patterns
  live there; the ruleset, name mapping, lint configs, Molecule, security
  predicates, source map and test corpus live here.
- **CI.** `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns the job that runs
  these scripts — image, `rules:`, caching, artifacts, the masked vault
  password. This skill publishes the predicate and decides no gate placement.
- **Containers.** `/alaa-docker-production` (`$alaa-docker-production`) owns the
  image and the Compose file, including the fail-closed `${VAR:?}` invariant;
  this skill owns the host state a play manages around it.
- **Kubernetes.** `/alaa-k8s-helm` (`$alaa-k8s-helm`) owns the manifest; this
  skill validates the play that applies it.
- **Fail-closed** is `/alaa-security-review`'s (`$alaa-security-review`); a
  scanner that could not run is a blocked audit, not a clean one.
- **Retry, timeout, `serial`, `forks`, degradation** are
  `/alaa-reliability-sla`'s (`$alaa-reliability-sla`). This skill reports a
  missing `changed_when`, `until` or `any_errors_fatal`; it picks no number.
- **Model and effort settings** are `/alaa-prompting-guide`'s
  (`$alaa-prompting-guide`), at `references/50-effort-and-thinking.md`.

## Reference map

| File | Read it when |
|---|---|
| `references/playbook.md` | running a full validation |
| `references/failure-classes.md` | a check failed or a run errored |
| `references/best_practices.md` | a finding needs a remediation citation |
| `references/module_alternatives.md` | an FQCN or deprecation finding |
| `references/security_checklist.md` | any security finding or Vault question |
| `references/molecule.md` | a `molecule/` directory exists |
| `references/source-map.md` | before any version-sensitive claim |
