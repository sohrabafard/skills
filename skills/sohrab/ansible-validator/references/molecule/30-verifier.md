# Molecule verifier

Read this guide only when a `molecule/` directory exists or when someone asks for one to be created. The scenario setup is verified against molecule 26.6.0 on 2026-07-29; [source-map.md](../source-map.md) owns the pinned values and re-derivation commands.

## Writing the verifier

The default verifier is `ansible`: a playbook of assertions.

```yaml
---
# molecule/default/verify.yml
- name: Verify
  hosts: all
  gather_facts: false
  tasks:
    - name: Confirm the service is enabled and running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
      check_mode: true
      register: service_state
      failed_when: service_state.changed

    - name: Confirm the configuration file has the intended mode
      ansible.builtin.stat:
        path: /etc/nginx/nginx.conf
      register: conf

    - name: Assert the mode denies write to other
      ansible.builtin.assert:
        that:
          - conf.stat.exists
          - conf.stat.mode == '0644'
        fail_msg: "nginx.conf is {{ conf.stat.mode | default('absent') }}, expected 0644"
```

The `check_mode: true` plus `failed_when: result.changed` shape is how you
assert a state without changing it. What a verify playbook should cover — the
layering, the doubles, the flake control — is `/alaa-testing-strategy`'s; this skill owns the mechanics of running it.
