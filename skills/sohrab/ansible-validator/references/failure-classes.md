# Failure classes: symptom, diagnosis, smallest retry, escalation

Read this when a check fails or a run errors. It replaces the former
`references/common_errors.md`, which was a flat list of symptoms with prose
"solutions" and no diagnosis step; three of its claims were factually wrong and
are corrected here in transit.

Every entry has the same four parts:

- **Symptom** — the text you actually see.
- **Diagnose** — the one command that tells you which cause it is.
- **Smallest retry** — the narrowest change that tests your hypothesis.
- **Escalate when** — the condition under which this stops being your fix.

---

## A. YAML does not parse

**Symptom**

```
syntax error: expected <block end>, but found '<block mapping start>'
mapping values are not allowed here
could not find expected ':'
```

**Diagnose**

```bash
python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>
yamllint -c assets/.yamllint -f parsable <file>
```

The Python line gives the parser's own message and the exact mark. yamllint adds
the style findings.

**Smallest retry** — the three causes, in the order they occur:

1. **Inconsistent indentation.** A key indented under a bare `---` when its
   siblings are at column 0. Fix: put every top-level key at column 0.
2. **An unquoted colon inside a value.** `db_host: localhost:5432` parses as a
   nested mapping. Fix: `db_host: "localhost:5432"`.
3. **A bracketed placeholder.** `[ role_name ]_port: [ default_port ]` is not a
   placeholder; YAML reads `[ role_name ]` as a one-element flow sequence, so
   the line is a mapping key that begins with a sequence. Fix: use a bare token
   such as `ROLE_NAME_port: CHANGE_ME_port`. This is the defect class that made
   six of the eight template files in `ansible-generator`'s
   (`/ansible-generator`, `$ansible-generator`) scaffold unparsable
   until 2026-07-29.

**Escalate when** the file parses in isolation but fails inside a role. That is
class B, not class A.

## B. Ansible cannot load the play or the role

**Symptom**

```
ERROR! couldn't resolve module/action 'community.general.docker_container'
ERROR! the role 'webserver' was not found
ERROR! Unable to retrieve file contents. Could not find or access 'install.yml'
```

**Diagnose**

```bash
ansible-playbook --syntax-check <playbook>
ansible-galaxy collection list
ansible-doc -t module <fqcn>
```

**Smallest retry**

- *Module not resolved:* the collection is not installed. Install it and pin it
  in `requirements.yml`:
  `ansible-galaxy collection install -r requirements.yml`. Do not replace the
  module with a `command` shell-out; rule 3.4 in `references/best_practices.md`
  states why.
- *Module resolved but "not found" from `ansible-doc`:* the name left core and
  works only through a redirect. Run
  `python3 scripts/check_module_currency.py <path>` and take the name it gives
  you. `references/module_alternatives.md` carries the mapping.
- *Role not found:* `ANSIBLE_ROLES_PATH` or `roles_path` in `ansible.cfg` does
  not include the directory. Confirm with `ansible-config dump | grep -i roles`.
- *Include not found:* an `include_tasks` path is relative to the file that
  includes it, not to the playbook. Confirm with `ls` from that directory.

**Escalate when** the collection is installed, `ansible-doc` finds the module,
and the play still fails to resolve it. That means two collection versions are
installed at different precedence; `ansible-galaxy collection list` shows both.

## C. A variable is undefined at run time

**Symptom**

```
The task includes an option with an undefined variable. The error was: 'app_port' is undefined
An unhandled exception occurred while templating
```

**Diagnose**

```bash
ansible-inventory -i <inventory> --host <hostname> --yaml
ansible-playbook <playbook> --syntax-check -e @vars.yml
```

The first prints every variable that host will actually receive, which settles
precedence arguments faster than reading the table.

**Smallest retry**

- The variable is genuinely optional: read it through `default()`.
- The variable is mandatory: declare it in `meta/argument_specs.yml` with
  `required: true`, so the run refuses at the start rather than failing in the
  middle. Or read it through `| mandatory`. The filter is `mandatory`; there is
  no `required` filter, and `{{ x | required('...') }}` fails with
  `No filter named 'required'`. Both skills in this pair taught the
  non-existent one until 2026-07-29.
- The variable is defined but not where you think: check precedence, rule 6.2 in
  `references/best_practices.md`. The most common surprise is that `set_fact`
  outranks role, block and task vars.

**Escalate when** `ansible-inventory --host` shows the variable and the task
still cannot see it. That is a scoping problem: a `vars:` on a `block` or an
`include_role` param, not an inventory problem.

## D. A connection fails

**Symptom**

```
UNREACHABLE! => {"msg": "Failed to connect to the host via ssh"}
Permission denied (publickey)
Authentication or permission failure
```

**Diagnose**

```bash
ansible -i <inventory> <host> -m ansible.builtin.ping -vvv
ssh -v <user>@<host>
```

`-vvv` prints the exact SSH command Ansible built, which is what you compare
against your working manual `ssh`.

**Smallest retry**

- Wrong user: set `ansible_user` in the inventory, not on the command line, so
  it is recorded.
- Wrong key: set `ansible_ssh_private_key_file`. Do not hardcode
  `~/.ssh/id_rsa` in a shared `group_vars/all.yml`; that is one developer's path
  written into everyone's inventory.
- Host key: `host_key_checking = True` is the correct setting. A host whose key
  you have not accepted is a host you have not verified; add the key with
  `ssh-keyscan` into a known-hosts file the play references, rather than turning
  the check off globally.
- **Never** set `ansible_ssh_pass` to a literal. If password authentication is
  the only option, put the value in a vault file and reference the vaulted
  variable, and set `no_log: true` on the tasks that use it.

**Escalate when** `ansible -m ping` succeeds and the playbook is still
unreachable. That means the play is targeting a different host pattern than you
think; `--list-hosts` settles it.

## E. Privilege escalation fails

**Symptom**

```
FAILED! => {"msg": "Missing sudo password"}
FAILED! => {"msg": "Could not create file: Permission denied"}
```

**Diagnose**

```bash
ansible -i <inventory> <host> -m ansible.builtin.command -a 'id' --become -vvv
```

**Smallest retry**

- Missing `become`: add `become: true` to the task that needs it, not to the
  play. Escalating the whole play means every read-only command also runs as
  root, and an audit cannot tell which tasks genuinely needed it.
- Missing sudo password: `--ask-become-pass`, or a vaulted `ansible_become_pass`.
- Passwordless sudo on the target: scope it to the commands the automation
  actually runs. A `NOPASSWD: ALL` line grants the automation user full root
  over anything on the box, which is a larger grant than the automation needs:

```
# /etc/sudoers.d/ansible
ansible ALL=(root) NOPASSWD: /usr/bin/systemctl, /usr/bin/apt-get, /usr/bin/dnf
```

**Escalate when** the grant the play needs cannot be enumerated. That is a
design question about what the automation is allowed to do, and
`/alaa-security-review` (`$alaa-security-review`) owns it.

## F. A handler does not run

**Symptom** — the notifying task reports `changed`, the service is not
restarted, and nothing errors.

**Diagnose**

```bash
ansible-playbook <playbook> --list-tasks
grep -rn 'notify:' <role>/tasks/
grep -rn '^- name:' <role>/handlers/
```

**Smallest retry**

- The `notify` string and the handler `name` must match exactly, including case.
  Nothing static reports a mismatch: `--syntax-check` passes and ansible-lint
  passes, and only a real run errors with
  `The requested handler ... was not found`. Compare the two greps above.
- The handler ran but at the wrong time: handlers run at the end of the play.
  When a later task in the same play depends on the restart, force it with
  `- ansible.builtin.meta: flush_handlers`.
- The notifying task reported `ok` rather than `changed`, so nothing was
  notified. That is usually correct behaviour and the bug is elsewhere.

**Escalate when** the names match and the handler still does not fire. Check
that the handler is in `handlers/`, not in `tasks/`.

## G. Check mode reports a failure that a real run would not

**Symptom**

```
FAILED! => {"msg": "This module does not support check mode"}
```

or a task failing because a directory an earlier task would have created does
not exist.

**Diagnose**

```bash
ansible-playbook <playbook> --check --diff --limit <one-host> -vv
```

**Smallest retry**

- A read-only command: `check_mode: false` together with `changed_when: false`,
  so it runs in a dry run and reports no change.
- A task that must not run in a dry run: `when: not ansible_check_mode`.
- A dependent task: check mode cannot see a change that did not happen. This is
  a limitation, not a defect. Report it as such rather than adding
  `ignore_errors`.

**Escalate when** check mode reports changes on a host you have just converged.
That means a task is not idempotent; go to class H.

## H. A role is not idempotent

**Symptom** — a second apply reports `changed` on tasks that changed nothing.

**Diagnose**

```bash
bash scripts/test_role.sh <role> default --i-confirm-disposable-host
```

The idempotence stage uses `molecule idempotence`, which compares every host. A
`grep` for `changed=0` over combined output passes whenever any one host of four
reported no change, which is how the pre-repair `test_role.sh` declared
idempotence.

**Smallest retry**

- A `command` or `shell` task with no `changed_when`, `creates` or `removes`
  reports `changed` every time. Rule 4.2 in `references/best_practices.md`.
- A `template` whose output contains a timestamp differs on every render. Move
  the timestamp out of the templated file, or exclude it.
- A `lineinfile` whose regexp does not match the line it inserts appends a
  duplicate on every run.

**Escalate when** the role is idempotent in Molecule and not on the real fleet.
That is drift on the fleet, and it is a change-control question:
`/alaa-controlled-ops` (`$alaa-controlled-ops`) owns change control and proof
strength.

## I. A check could not run

**Symptom** — exit code 2 from any script in `scripts/`, or

```
[BLOCKED] ...
This is exit 2: the check could not run. It is not a pass.
```

**Diagnose**

```bash
bash scripts/setup_tools.sh
```

It compares every installed tool against the floor in
`scripts/requirements.txt` and names the ones that are missing or too old.

**Smallest retry**

```bash
python3 -m pip install --upgrade -r scripts/requirements.txt
```

**Escalate when** the tool is installed and the script still exits 2. Read the
message: an ansible-lint exit of 3 means the configuration file itself is
rejected, and `bash scripts/check_assets.sh` reports which assertion the shipped
configuration no longer satisfies.

**Never** treat exit 2 as a pass. A test that could not run is not a passing
test. Report `BLOCKED` with the reason. A blocked security scan is a failure,
per `/alaa-security-review` (`$alaa-security-review`); a blocked idempotence
test is a warning, per `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## J. ansible-lint reports a rule you disagree with

**Symptom** — a finding that is correct for the tool and wrong for this project.

**Diagnose**

```bash
ansible-lint -L | grep <rule-id>
ansible-lint --profile <name> <target>
```

**Smallest retry**

- The rule is right and the code is wrong: fix the code. That is the usual case.
- The rule is right and the fix is mechanical: `ansible-lint --fix` writes the
  files first, so run it only on a clean working tree and read the resulting
  diff before committing. There is no mode that shows the change without making
  it.
- The rule genuinely does not apply here: move it to `warn_list` in
  `assets/.ansible-lint` with a comment stating why, and add a fixture under
  `test/fixtures/lint/` so `scripts/check_assets.sh` still proves what the
  config does. Do not add it to `skip_list`: a skipped rule is invisible, and
  the next reader cannot tell a considered exception from an accident.

**Escalate when** a rule you enabled stops firing. That is the
`task_name_prefix: "{path}:"` failure class: an invalid option value raises
inside a rule, ansible-lint catches the exception, prints
`Ignored exception from <Rule>.matchtasks`, and continues with the rule dead.
`scripts/check_assets.sh` reports it.

## K. Corrections carried over from the retired `common_errors.md`

Three claims in the retired file were wrong. They are recorded here so that a
reader who remembers them knows what replaced them.

| Claim | Status |
|---|---|
| `{{ x \| required('message') }}` makes a variable mandatory | **False.** There is no `required` filter; the call fails with `No filter named 'required'`. Use `mandatory`, or `required: true` in `meta/argument_specs.yml`. |
| `with_items` emits `[DEPRECATION WARNING]: with_items is deprecated, use loop instead` | **False.** ansible-core 2.19.11 emits no such warning. `with_*` is discouraged in favour of `loop`; it is not deprecated and the quoted text does not exist. |
| `args: warn: false` suppresses the command-module warning | **False.** The parameter was removed. ansible-core now fails with `Unsupported parameters for (ansible.legacy.command) module: warn`. |

## L. Quick reference

```bash
# Full validation of one playbook
bash scripts/validate_playbook.sh playbook.yml

# Full validation of one role
bash scripts/validate_role.sh roles/webserver

# Security: all three, every time
bash scripts/validate_playbook_security.sh playbook.yml
bash scripts/scan_secrets.sh playbook.yml
python3 scripts/check_task_safety.py playbook.yml

# What Ansible will actually give this host
ansible-inventory -i inventory --host web1.example.com --yaml

# What the play will do, bounded
ansible-playbook -i inventory playbook.yml --check --diff --limit web1.example.com

# Which tasks, which hosts, before running anything
ansible-playbook playbook.yml --list-tasks
ansible-playbook -i inventory playbook.yml --list-hosts
```
