# The Ansible ruleset

This file is the pair's single statement of the rules an Ansible artifact is
measured against. `ansible-generator` (`/ansible-generator`,
`$ansible-generator`) generates against these rules and does not restate them;
its `references/best-practices.md` holds only the rules that apply at authoring
time and have no checker, and routes here for everything else.

The ownership rule that produced that split: **a rule lives with the skill that
ships the checker which reports its violation.** Only this skill ships
checkers, so the ruleset lives here. Every rule below names the checker that
reports it, or says plainly that nothing reports it yet.

Read this file when a finding needs a remediation citation, and cite the rule
number in the report.

---

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

## 2. Naming

**2.1 Every task has a `name`.** The name is what an operator reads in the
output of a failing run at 03:00.
*Reported by:* `ansible-lint` rule `name[missing]`, which `assets/.ansible-lint`
enables. `scripts/check_assets.sh` asserts that it fires.

**2.2 A task name starts with a capital letter and a verb in the imperative:**
"Install nginx", "Ensure the configuration directory exists", "Reload the web
server". A name that describes a noun ("Nginx configuration") does not say what
the task did when it appears beside `changed`.
*Reported by:* `ansible-lint` rule `name[casing]` for the capital;
nothing reports the verb.

**2.3 Variables are `snake_case`,** and a role's variables carry the role name
as a prefix: `nginx_worker_processes`, not `workers`. An unprefixed variable in
a role collides with the same name in another role at play scope, and the
collision is silent.
*Reported by:* `ansible-lint` rule `var-naming`, with the pattern in
`assets/.ansible-lint`.

**2.4 Files and directories are lowercase with underscores.**
*Reported by:* nothing. This is a review finding.

## 3. Module selection

**3.1 Every action is a fully qualified collection name.** `ansible.builtin.apt`,
not `apt`. A short name resolves through core's routing table, which changes
between releases, so the same play can run on one machine and fail on another.
*Reported by:* `ansible-lint` rule `fqcn[action-core]` and
`scripts/check_fqcn.sh`, which agree that this is an error rather than advice.

**3.2 The FQCN names the collection that provides the module today, not the one
that used to.** Three names the pair taught until 2026-07-29 —
`ansible.builtin.yum`, `ansible.builtin.archive`, `ansible.builtin.authorized_key` <!-- check-module-currency:ignore -->
— left core and now work only through a compatibility redirect, so they run
where the collection happens to be installed and fail where it is not.
*Reported by:* `python3 scripts/check_module_currency.py`.
*Mapping:* `references/module_alternatives.md`.

**3.3 A collection an artifact uses is declared in `requirements.yml` with a
version floor.** A floor so low that every release satisfies it asserts nothing;
state the version whose behaviour you relied on.
*Reported by:* `scripts/extract_ansible_info_wrapper.sh` lists
`unpinned_collections`.

**3.4 Use the module for the operation. Do not shell out to the tool the module
wraps.** `community.postgresql.postgresql_db`, not
`ansible.builtin.command: psql -c "CREATE DATABASE ..."`. Shelling out to dodge
a collection dependency destroys idempotency, check-mode support and error
semantics in one move; a missing collection is an environment defect to fix in
the environment, not a design choice.
*Reported by:* `ansible-lint` rule `command-instead-of-module`.

**3.5 `ansible.builtin.command` before `ansible.builtin.shell`.** Use `shell`
only when the command needs a pipe, a redirect, a glob or a shell variable, and
say which in a comment.
*Reported by:* `ansible-lint` rule `command-instead-of-shell`.

## 4. Idempotency

**4.1 A task states the end state, not the operation.** `state: present`, not
`command: apt-get install`.
*Reported by:* `ansible-lint` rule `command-instead-of-module`.

**4.2 A `command` or `shell` task states `changed_when`,** or `creates`, or
`removes`. Without one it reports `changed` on every run, which makes a real
change invisible in the output and makes the idempotence test meaningless.
*Reported by:* `ansible-lint` rule `no-changed-when`.

**4.3 A read-only command sets `changed_when: false`** and states its own
`failed_when` when a non-zero return code is expected.

**4.4 A second apply changes nothing.** This is the definition, and it is
testable: `molecule idempotence` compares every host.
*Reported by:* `scripts/test_role.sh`, idempotence stage. See
`references/molecule.md` for when running a scenario is correct.

## 5. Error handling

**5.1 A group of tasks that must be undone on failure goes in a
`block`/`rescue`/`always`.** `rescue` restores the previous state; `always`
removes the lock, the temporary file and the maintenance flag.

**5.2 `ignore_errors: true` is not a failure strategy.** Replace it with
`failed_when` naming the condition that is genuinely acceptable, so that the
other failures still fail.
*Reported by:* `ansible-lint` rule `ignore-errors`.

**5.3 A play that must not half-apply across a fleet sets `any_errors_fatal:
true`,** or `max_fail_percentage` with a number.
*Reported by:* nothing. What the number should be is not this skill's decision:
`/alaa-reliability-sla` (`$alaa-reliability-sla`) owns why a timeout, retry,
backoff or degradation mechanism exists and what shape it takes. This skill
reports that a play has no `any_errors_fatal` and stops there.

**5.4 A health check that is allowed to take time states `until`, `retries` and
`delay`.** A health check with no `until` either passes on the first poll or
fails the play, which is a race, not a check.
*Reported by:* nothing. The values are `/alaa-reliability-sla`'s
(`$alaa-reliability-sla`).

**5.5 A task whose failure must stop the run states so.** A play that continues
past a failed decrypt, a failed certificate fetch or a failed schema migration
has decided to proceed without something it needed. Whether proceeding is
allowed is `/alaa-security-review`'s (`$alaa-security-review`) when the missing
thing is a security control, and `/alaa-reliability-sla`'s
(`$alaa-reliability-sla`) when it is an availability dependency. The
discriminating question: *when this dependency cannot answer, does proceeding
without it let something through that must not get through?*

## 6. Variables

**6.1 `defaults/main.yml` holds what a caller may override.
`vars/main.yml` holds what a caller must not.** The difference is precedence,
not convention: `vars/` outranks almost everything a caller can set.

**6.2 Variable precedence, lowest to highest.** This is the pair's single
precedence table. `ansible-generator` routes here rather than restating it,
because it shipped a nine-item list that placed `set_fact` *below* task, block
and role vars, which is the reverse of the truth and is the single question most
likely to produce a wrong-value bug.

1. role defaults (`defaults/main.yml`)
2. inventory file or script group vars
3. inventory `group_vars/all`
4. playbook `group_vars/all`
5. inventory `group_vars/*`
6. playbook `group_vars/*`
7. inventory file or script host vars
8. inventory `host_vars/*`
9. playbook `host_vars/*`
10. host facts and cached `set_fact`
11. play vars
12. play `vars_prompt`
13. play `vars_files`
14. role vars (`vars/main.yml`)
15. block vars
16. task vars
17. `include_vars`
18. `set_fact` and registered vars
19. role and `include_role` params
20. include params
21. extra vars (`-e`), which always win

Source: the Ansible variable-precedence section of the playbooks guide, linked
from `references/source-map.md`.
*Reported by:* nothing. Precedence bugs are read, not linted.

**6.3 An optional variable is read through `default()`.** `{{ app_port |
default(8080) }}`.

**6.4 A mandatory variable is read through `mandatory`, or declared `required:
true` in `meta/argument_specs.yml`.** The filter is `mandatory`. There is no
`required` filter; `{{ x | required('...') }}` fails at runtime with
`No filter named 'required'`. Both skills taught the non-existent one until
2026-07-29.

**6.5 Fact caching values are the same everywhere they appear.** The pair's
single value for `fact_caching_timeout` is **86400** seconds, stated in section
9 below; `ansible-generator`'s `ansible.cfg` template carries a comment naming
this file as the owner instead of a second number. It shipped 3600 against this
file's 86400 until 2026-07-29.

## 7. Conditionals and loops

**7.1 `loop`, not `with_*`.** `with_items` and its siblings are discouraged in
favour of `loop`; they are **not** deprecated, and ansible-core 2.19.11 emits no
deprecation warning for them. Both skills quoted a `[DEPRECATION WARNING]` text
that ansible-core does not produce.

**7.2 A `when` holding several conditions is a YAML list,** one condition per
line, so that a failing condition is identifiable from the output.

**7.3 A `when` does not wrap its expression in `{{ }}`.**
*Reported by:* `ansible-lint` rule `no-jinja-when`.

**7.4 An OS-conditional task branches on `ansible_os_family` or
`ansible_distribution`,** and the play states what happens on a family it does
not name. A play that silently skips every task on an unlisted OS reports
success having done nothing.

## 8. Security rules that apply at authoring time

The security predicates, the Vault mechanics and the command that evaluates
each one are in `references/security_checklist.md`. The rules below are the
subset that is also a code-shape rule.

**8.1 Every `file`, `copy` and `template` task states an explicit `mode`.**
Without one the result depends on the remote umask.
*Reported by:* `ansible-lint` rule `risky-file-permissions`.

**8.2 No mode grants write to `other`.** Secrets are `'0600'` and their
directories `'0700'`; configuration is `'0644'` and its directories `'0755'`.
*Reported by:* `python3 scripts/check_task_safety.py`, rule
`mode[world-writable]`. ansible-lint's `yaml[octal-values]` fires on the
unquoted form only, so `mode: '0777'` passes a production-profile run.

**8.3 A Jinja expression interpolated into a `command`, `shell` or `raw` value
ends in `| quote`,** or the task uses a module that takes the value as a
parameter instead.
*Reported by:* `python3 scripts/check_task_safety.py`, rule
`command[unquoted-jinja]`. Nothing else in the toolchain reports it.

**8.4 `no_log: true` on any task whose module arguments or registered result can
contain a value sourced from a vault file, from `lookup('env', ...)`, or from a
variable whose name matches `(pass|secret|token|key|credential)`.**
*Reported by:* `ansible-lint` rule `no-log-password` for the password case;
`scripts/scan_secrets.sh` for the rest.

**8.5 `validate_certs` is absent or `true`.** A task that sets it `false`
carries a comment naming the internal certificate authority it is working
around and a linked issue for installing that authority.
*Reported by:* Checkov `CKV_ANSIBLE_1` and `CKV_ANSIBLE_2`.

## 9. Performance

Each value below is a starting point with the reason it exists. What the number
should be for a given fleet and SLA is `/alaa-reliability-sla`'s
(`$alaa-reliability-sla`).

**9.1 SSH pipelining on.** It removes one round trip per task, which dominates
run time on a high-latency link.

```ini
[ssh_connection]
pipelining = True
```

**9.2 Fact caching on, with one timeout value across the whole project.**

```ini
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = {{ project_fact_cache_dir }}
fact_caching_timeout = 86400
```

86400 is the pair's single value for `fact_caching_timeout`; rule 6.5 states
that. Do not put the cache in `/tmp`: it is world-writable on a shared host and
does not exist on a Windows control node.

**9.3 `gather_facts: false` unless the play reads an `ansible_*` fact.** When it
reads fewer than three, set `gather_subset` naming exactly those. Fact gathering
is one full module execution per host before any task runs.

**9.4 A long task runs async and is polled.**

```yaml
- name: Run the database migration
  ansible.builtin.command: /opt/app/migrate.sh
  async: 3600
  poll: 0
  register: migration
  changed_when: true

- name: Wait for the migration to finish
  ansible.builtin.async_status:
    jid: "{{ migration.ansible_job_id }}"
  register: migration_status
  until: migration_status.finished
  retries: 360
  delay: 10
```

**9.5 `forks` and `serial` are stated, not defaulted.** `forks = 5` is the stock
default; shipping it as if it were a tuning decision tells the reader nothing.
`serial` bounds how much of the fleet a bad change reaches at once, which is a
blast-radius decision. Both numbers are `/alaa-reliability-sla`'s
(`$alaa-reliability-sla`).

**9.6 A loop or a fan-out that grows with the inventory has a stated bound.**
A play whose cost grows with tenants, hosts or history is a complexity question:
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) owns
complexity budgets and structure choice.

## 10. Check mode

**10.1 Every task supports check mode, or says why it does not.** A read-only
command sets `check_mode: false` together with `changed_when: false`, so that it
runs in a dry run and reports no change. A task that must not run in a dry run
guards on `when: not ansible_check_mode`.

**10.2 A check-mode run against production states its `--limit`.**
`ansible-playbook --check --diff` still opens a connection to every host in
scope and still runs every fact gather and every read-only command. Bound it.

**10.3 A check-mode pass is not a guarantee.** A task whose result depends on a
change an earlier task would have made reports a state that will not exist. Read
the diff rather than the summary.

## 11. Documentation

**11.1 A playbook opens with a header comment** stating what it does, which
hosts it targets, the required and optional variables with their defaults, and
the exact command to run it.

**11.2 A role has a `README.md`** with the variable table, one worked example
and the platform list.

**11.3 Every variable in `defaults/main.yml` has a comment** saying what it
controls and what the units are.
