# Ansible ruleset: Authoring Security

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
