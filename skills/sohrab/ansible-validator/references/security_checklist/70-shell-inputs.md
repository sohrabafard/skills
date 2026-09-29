# Security checklist: Shell Inputs

## S6. No unvalidated value reaches a shell

**Predicate.** No `command`, `shell` or `raw` value interpolates a Jinja
expression that does not end in `| quote`.

**Evaluate.**

```bash
python3 scripts/check_task_safety.py <target>     # rule command[unquoted-jinja]
```

Nothing else in this toolchain reports it: measured 2026-07-29, a task reading
`shell: "grep {{ search_term }} /var/log/app.log"` passes ansible-lint's
production profile and Checkov's ansible framework alike.

```yaml
# Reported
- name: Search the log
  ansible.builtin.shell: "grep {{ search_term }} /var/log/app.log"

# Correct: the value cannot break out of the argument
- name: Search the log
  ansible.builtin.shell: "grep {{ search_term | quote }} /var/log/app.log"
  changed_when: false

# Better: no shell at all
- name: Search the log
  ansible.builtin.lineinfile:
    path: /var/log/app.log
    regexp: "{{ search_term | regex_escape }}"
    state: absent
  check_mode: true
```

A value that reaches a command from inventory, from an extra var or from a
registered result is attacker-controlled until proved otherwise. The `args:
warn: false` idiom that used to appear near this advice no longer exists:
ansible-core fails with `Unsupported parameters for (ansible.legacy.command)
module: warn`.
