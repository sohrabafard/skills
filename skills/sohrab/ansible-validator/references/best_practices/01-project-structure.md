# Ansible ruleset: 1. Structure

## 1. Structure

**1.1 A project has one inventory directory per environment.** Production and
staging inventories are separate trees under `inventory/`, each with its own
`hosts`, `group_vars/` and `host_vars/`. Sharing one inventory between
environments and switching on a variable means a mistyped `--limit` reaches
production.
*Reported by:* nothing. This is a review finding.

**1.2 A role has `tasks/main.yml`.** `defaults/`, `handlers/`, `meta/`,
`templates/` and `vars/` are present when the role uses them, and each present
directory has a `main.yml`.
*Reported by:* `scripts/validate_role.sh` stage 1.

**1.3 A role declares `meta/argument_specs.yml`.** Every variable the role reads
from outside itself appears there with a type, and with `required: true` or a
default. This is validation at the boundary: without it, a missing variable
surfaces as a Jinja error in the middle of a run rather than as a refusal at the
start.
*Reported by:* `ansible-lint` rule `role-argument-spec`.

**1.4 `meta/main.yml` states `min_ansible_version` and the platform list it was
tested on.** A platform not in the list is a platform nobody tested.
*Reported by:* `ansible-lint` rules `meta-incorrect`, `meta-runtime`.
