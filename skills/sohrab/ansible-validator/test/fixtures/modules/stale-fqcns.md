# Fixture: names that check_module_currency.py must classify correctly

Do not fix this file. Three of the names below left ansible-core and now work
only through a compatibility redirect; three are live builtins. The self-test
asserts both directions.

Must be reported:

- `ansible.builtin.yum` - the module file is gone; the name runs dnf through an
  action redirect, so "only use for RHEL 7" is now impossible advice.
- `ansible.builtin.archive` - redirects to `community.general.archive`.
- `ansible.builtin.authorized_key` - redirects to `ansible.posix.authorized_key`.

Must not be reported:

- `ansible.builtin.dnf`
- `ansible.builtin.template`
- `ansible.builtin.systemd_service`
