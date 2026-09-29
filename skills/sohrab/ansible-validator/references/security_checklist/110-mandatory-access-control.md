# Security checklist: Mandatory Access Control

## S10. SELinux and AppArmor stay enforcing

**Predicate.** No task sets SELinux `state: permissive` or `state: disabled`, and
no task unloads an AppArmor profile.

**Evaluate.**

```bash
grep -rn "state: *\(permissive\|disabled\)" <target>
grep -rn "apparmor_parser -R" <target>
```

When a role needs a context rather than a disabled policy, set the context:

```yaml
- name: Label the web content directory
  community.general.sefcontext:
    target: '/srv/web(/.*)?'
    setype: httpd_sys_content_t
    state: present
  notify: Restore SELinux contexts
```
