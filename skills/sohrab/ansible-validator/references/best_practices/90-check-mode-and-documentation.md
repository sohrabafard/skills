# Ansible ruleset: Check Mode And Documentation

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
