# Security checklist: Privilege Escalation

## S4. Privilege escalation is scoped

**Predicate.** `become` appears on the tasks that need it, not on the play, and
`become_user` names the account that needs it rather than defaulting to root.

**Evaluate.**

```bash
grep -rn 'become' <target> | grep -v 'become_user\|become_method'
ansible-lint -c assets/.ansible-lint <target>   # rule partial-become
```

Read the result: a `become: true` at play level with read-only tasks under it is
the finding. A blanket `[privilege_escalation] become = True` in `ansible.cfg`
is the same finding at project scope, and it makes every ad-hoc `ansible -m`
command run as root too.

**On the target,** scope the sudoers grant to the commands the automation
actually runs rather than granting `NOPASSWD: ALL`:

```
# /etc/sudoers.d/ansible
ansible ALL=(root) NOPASSWD: /usr/bin/systemctl, /usr/bin/apt-get, /usr/bin/dnf
```
