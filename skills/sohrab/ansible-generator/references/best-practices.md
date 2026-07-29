# Authoring rules

Read this before writing the first task.

**This file is not the ruleset.** The ruleset an Ansible artifact is measured
against is `ansible-validator references/best_practices.md`
(`/ansible-validator`, `$ansible-validator`), because a rule is only real if
something reports its violation, and only that skill ships checkers. This file
holds the subset that applies while you are typing, where knowing the rule early
is cheaper than being told about it afterwards. Every entry cites the rule it
corresponds to on that side.

Nothing here is restated from there. Where you want the full statement, the
reason, or the command that reports a violation, follow the citation.

---

## What this skill decides, and what it does not

| Question | Owner |
|---|---|
| Which module, and how to call it | this skill, `references/module-patterns.md` |
| What a module name maps to today | `ansible-validator references/module_alternatives.md` |
| Jinja filters, lookups, template control | this skill, `references/jinja-and-lookups.md` |
| The rule a finding is measured against | `ansible-validator references/best_practices.md` |
| Variable precedence | `ansible-validator references/best_practices.md` rule 6.2 |
| Security predicates and Vault mechanics | `ansible-validator references/security_checklist.md` |
| `.ansible-lint` and `.yamllint` | `ansible-validator assets/` |
| Molecule | `ansible-validator references/molecule.md` |
| Check-mode procedure | `ansible-validator references/best_practices.md` section 10 |
| Version-sensitive claims and the freshness procedure | `ansible-validator references/source-map.md` |
| Retry, timeout, `serial`, `forks`, degradation | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Whether a missing dependency stops the run | `/alaa-security-review` (`$alaa-security-review`) when the missing thing is a security control; `/alaa-reliability-sla` (`$alaa-reliability-sla`) when it is an availability dependency |
| Complexity budget for a loop or fan-out that grows | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |

## A1. Shape of a task

Write every task in this shape and most of the ruleset is satisfied before you
run anything:

```yaml
- name: Ensure the configuration directory exists
  ansible.builtin.file:
    path: "{{ myrole_config_dir }}"
    state: directory
    owner: "{{ myrole_user }}"
    group: "{{ myrole_group }}"
    mode: "0755"
  tags:
    - configure
```

Five properties, and the rule each one satisfies:

| Property | Rule |
|---|---|
| a `name` starting with a capital and a verb | validator rules 2.1, 2.2 |
| a fully qualified action | validator rule 3.1 |
| an end state, not an operation | validator rule 4.1 |
| an explicit, quoted `mode` on anything written | validator rules 8.1, 8.2 |
| a role-prefixed variable | validator rule 2.3 |

Quote every mode. An unquoted `0644` is the integer 420 in YAML, and the module
then applies a mode nobody wrote.

## A2. Booleans are `true` and `false`

`yes`, `no`, `on` and `off` are rejected by ansible-lint's `yaml[truthy]` under
the production profile. `python3 scripts/check_templates.py <path>` reports them
in anything this skill emits, which is why this is now a rule here rather than a
checklist line nothing enforced.

## A3. Choosing the module

Ask, in this order:

1. **Is there a module for this operation?** Use it.
   `references/module-patterns.md` is organised by operation for exactly this
   question.
2. **Is the module in a collection?** Declare the collection in
   `requirements.yml` with a version floor, and use it. A missing collection is
   an environment defect to fix in the environment.
3. **Is there genuinely no module?** Then `ansible.builtin.command`, with
   `changed_when`, `creates` or `removes`. `ansible.builtin.shell` only when the
   command needs a pipe, a redirect, a glob or a shell variable, and say which in
   a comment.

**Do not substitute `ansible.builtin.command` for a collection module to avoid a
dependency.** Shelling out to `psql` instead of using
`community.postgresql.postgresql_db` destroys idempotency, check-mode support
and error semantics in one move, and it is what this skill instructed until
2026-07-29. Validator rules 3.4 and 3.5.

**Write the name the module has today.** Three names this skill taught had left
ansible-core and worked only through a compatibility redirect, so the example
ran where the collection happened to be installed and failed where it was not.
Verify offline with
`python3 <ansible-validator>/scripts/check_module_currency.py <path>`.

## A4. Defaults versus vars

`defaults/main.yml` holds what a caller may override. `vars/main.yml` holds what
a caller must not. The difference is precedence, not convention:
`vars/main.yml` outranks almost everything a caller can set. Validator rule 6.1;
the 21-step precedence table is validator rule 6.2, and this file carries no
second copy of it. The nine-item table that used to live here placed `set_fact`
*below* task, block and role vars, which is the reverse of the truth.

Write a default that is safe when nobody thinks about it:

- Bind to `127.0.0.1`, not `0.0.0.0`. A wider bind is the caller's explicit
  decision, not the role's default.
- Do not default a version to `latest`. It makes the run non-reproducible and
  trips `package-latest`.
- Default every mode to a value that denies write to `other`.

## A5. Declare the interface

Every variable a role reads from outside itself goes in
`meta/argument_specs.yml` with a type and either `required: true` or a default.
That is validation at the boundary: a missing variable becomes a refusal before
the first task rather than a Jinja error part-way through a partly applied run.
Validator rule 1.3; `assets/templates/role/meta/argument_specs.yml` is the
worked template.

## A6. Where `no_log` goes while you are writing

Set `no_log: true` on a task at the moment you write a module argument or a
registered result that can hold a value sourced from a vault file, from
`lookup('env', ...)`, or from a variable whose name matches
`(pass|secret|token|key|credential)`. Adding it afterwards means the value has
already been in a log.

`--diff` prints the content of a templated file, and that output is produced by
the file module rather than by the argument logger, so `no_log` does not
suppress it. A template that renders a secret needs `diff: false` on that task.
Validator rule 8.4 and `ansible-validator references/security_checklist.md`
section S2.

The Vault commands themselves — `encrypt_string`, vault IDs, rekeying, where a
vaulted value lives, how a decrypt failure behaves — are that checklist's
section S3. This skill carries no second copy.

## A7. Multi-OS

```yaml
- name: Load the OS-family variables
  ansible.builtin.include_vars: "{{ ansible_os_family }}.yml"
  tags:
    - always
```

with `vars/Debian.yml` and `vars/RedHat.yml` beside it. That keeps package and
service names out of the task list and makes adding a family a new file rather
than a new branch.

State what happens on a family the role does not name. A role that silently
skips every task on an unlisted OS reports success having done nothing.
Validator rule 7.4.

## A8. Handlers

Notify a handler for anything that restarts or reloads a service; do not put the
restart in the task list. A handler runs once at the end of the play however
many tasks notified it, so ten configuration changes produce one restart.

The `notify` string and the handler's `name` must match exactly, including case.
Nothing static reports a mismatch: `--syntax-check` passes, ansible-lint passes,
and only a real run errors. `ansible-validator references/failure-classes.md`
class F is the diagnosis procedure.

When a later task in the same play depends on the restart, force it:

```yaml
- name: Apply pending handlers before the health check
  ansible.builtin.meta: flush_handlers
```

## A9. Tags

Give every task at least one tag from a small, stated set: `install`,
`configure`, `service`, plus `always` for the `include_vars` everything else
depends on. Tags are how an operator re-runs one part of a play during an
incident, and a play with no tags is all-or-nothing at exactly the wrong moment.

## A10. Failure behaviour, at authoring time

Write these in as you go, because retro-fitting them means re-reading the play:

- A group of tasks that must be undone on failure goes in a
  `block`/`rescue`/`always`. `always` removes the lock file, the temporary
  directory and the maintenance flag.
- A `command` or `shell` states `changed_when`, `creates` or `removes`.
- A read-only command states `changed_when: false`, and its own `failed_when`
  when a non-zero return code is expected.
- A health check states `until`, `retries` and `delay`. A health check with no
  `until` either passes on the first poll or fails the play, which is a race.
- A play that must not half-apply across a fleet states `any_errors_fatal: true`
  or a `max_fail_percentage`.

What the numbers should be is `/alaa-reliability-sla`'s
(`$alaa-reliability-sla`). Write the mechanism; let that skill choose the value.

## A11. Performance decisions you make while writing

- `gather_facts: false` unless the play reads an `ansible_*` fact. When it reads
  fewer than three, `gather_subset` naming exactly those.
- `update_cache` with `cache_valid_time` rather than an unconditional refresh.
- A task that takes minutes runs `async` with `poll: 0`, and is polled by
  `ansible.builtin.async_status`.
- A loop whose length grows with the inventory, the tenant count or history has
  a stated bound. `/alaa-algorithms-data-structures`
  (`$alaa-algorithms-data-structures`) owns complexity budgets.

Validator section 9 carries the project-level settings — pipelining, fact
caching and its single `fact_caching_timeout` value of 86400, `forks`, `serial`
— and this file does not restate them. The `ansible.cfg` this skill emits
carries a comment naming that file as the owner instead of a second number; it
shipped 3600 against the validator's 86400 until 2026-07-29.

## A12. Documentation, written with the code

A playbook opens with a header comment stating what it does, which hosts it
targets, the required and optional variables with their defaults, and the exact
command to run it. A role has a `README.md` with the variable table, one worked
example and the platform list. Every variable in `defaults/main.yml` has a
comment saying what it controls and in what units.

`assets/templates/role/README.md` and
`assets/templates/playbook/basic_playbook.yml` are the shapes.

## A13. Before you hand it over

```bash
python3 scripts/check_templates.py <the files you generated>
bash <ansible-validator>/scripts/validate_playbook.sh <playbook>   # or validate_role.sh
bash <ansible-validator>/scripts/scan_secrets.sh <target>
python3 <ansible-validator>/scripts/check_task_safety.py <target>
```

Exit 0 is the only pass. Exit 2 means a check could not run, which is not a
pass. `references/playbook.md` states the stopping condition for the
fix-and-re-run loop.
