# Security checklist: Host Key Verification

## S8. Host keys are checked

**Predicate.** `host_key_checking` is `True` in `ansible.cfg`.

**Evaluate.**

```bash
ansible-config dump | grep -i host_key_checking
```

`False` means the first connection to any host succeeds regardless of identity,
which removes the only protection against a machine-in-the-middle on the
management path. Where hosts are genuinely ephemeral, collect their keys into a
known-hosts file the play references rather than turning the check off:

```yaml
- name: Record the host key
  ansible.builtin.known_hosts:
    path: "{{ project_known_hosts }}"
    name: "{{ inventory_hostname }}"
    key: "{{ lookup('pipe', 'ssh-keyscan -t ed25519 ' ~ inventory_hostname) }}"
  delegate_to: localhost
```
