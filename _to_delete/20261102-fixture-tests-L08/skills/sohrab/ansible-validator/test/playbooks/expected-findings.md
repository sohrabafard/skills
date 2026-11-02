# What each checker must report on `bad-playbook.yml`

This file is the contract for the negative fixture. When a checker stops
reporting a row below, the checker regressed, not the fixture.

Measured 2026-07-29 with ansible-core 2.19.11, ansible-lint 26.6.0,
yamllint 1.38.0 and checkov 3.3.8.

| Defect in the fixture | Reported by | Identifier |
|---|---|---|
| The play has no name | `validate_playbook.sh` stage 3 | `name[play]` |
| A task has no name | `validate_playbook.sh` stage 3 | `name[missing]` |
| A task name starts lowercase | `validate_playbook.sh` stage 3 | `name[casing]` |
| `become: yes` instead of `true` | `validate_playbook.sh` stages 1 and 3 | `yaml[truthy]` |
| Short module names throughout | `validate_playbook.sh` stage 3, `check_fqcn.sh` | `fqcn[action-core]` |
| `shell: mkdir -p` where a module exists | `validate_playbook.sh` stage 3 | `command-instead-of-module`, `command-instead-of-shell` |
| `command`/`shell` with no `changed_when` | `validate_playbook.sh` stage 3 | `no-changed-when` |
| `get_url` with no `mode` | `validate_playbook.sh` stage 3 | `risky-file-permissions` |
| `mode: '0777'` on a directory | `check_task_safety.py` | `mode[world-writable]` |
| `mode: '0666'` on a key file | `check_task_safety.py` | `mode[world-writable]` |
| `{{ search_term }}` inside `shell:` | `check_task_safety.py` | `command[unquoted-jinja]` |
| `db_password: "hunter2-plaintext"` | `scan_secrets.sh` | hardcoded password |
| `validate_certs: no` on `get_url` | `validate_playbook_security.sh` | `CKV_ANSIBLE_2` |
| `http://` URL on `get_url` | `validate_playbook_security.sh` | `CKV2_ANSIBLE_2` |
| High-entropy literal | `validate_playbook_security.sh` | `CKV_SECRET_6` |

## Four things the fixture contains that nothing reports

Recorded so that nobody mistakes silence for a clean file. Each is a real gap.

| Defect | Why nothing reports it |
|---|---|
| The handler is named `Restart nginx` and the task notifies `restart nginx service` | No static check compares the two strings. `--syntax-check` passes and ansible-lint passes; only a real run errors with `The requested handler ... was not found`. `references/failure-classes.md` class F is the diagnosis procedure. |
| `with_items` instead of `loop` | `with_*` is discouraged, not deprecated, and ansible-core 2.19.11 emits no warning. The claim that it does was fabricated in the retired `common_errors.md`. |
| No OS conditional on the `apt` tasks | Nothing models "this play would do nothing on RedHat". It is a review finding. |
| `search_term` is never defined | An undefined variable surfaces at run time, not at lint time. `meta/argument_specs.yml` is how a role refuses at the start instead; a playbook has no equivalent. |
