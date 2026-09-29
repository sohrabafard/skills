# Security checklist: Credential Storage

## S1. No credential is a literal in a tracked file

**Predicate.** No file under version control assigns a literal value to a key
whose name reads as a credential, and no file contains a private-key block, an
AWS access key ID, or a connection string with an inline password.

**Evaluate.**

```bash
bash scripts/scan_secrets.sh <target>
bash scripts/validate_playbook_security.sh <target>
```

**Correct forms, in the order to try them.**

```yaml
# 1. A vaulted variable. The value lives in an encrypted file.
- name: Create the database user
  community.postgresql.postgresql_user:
    name: app
    password: "{{ vault_app_db_password }}"
  no_log: true

# 2. An environment variable the CI job injects.
- name: Authenticate against the registry
  community.docker.docker_login:
    registry_url: registry.example.com
    username: ci
    password: "{{ lookup('env', 'REGISTRY_TOKEN') }}"
  no_log: true

# 3. An external secret store.
- name: Read the signing key
  ansible.builtin.set_fact:
    signing_key: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=secret/data/app:signing_key') }}"
  no_log: true
```

**What the scanner deliberately does not report.** A value that is a Jinja
expression, a `vault_`-prefixed variable, an inline `!vault` block, or a
`lookup()` call. Those are the correct patterns. A scanner that red-lights the
correct pattern gets switched off, which is what happened before 2026-07-29:
`scan_secrets.sh` reported a fully vaulted playbook as two secrets and exited 1.
Pass `--no-allow-vaulted` when you are auditing whether the indirection actually
resolves.
