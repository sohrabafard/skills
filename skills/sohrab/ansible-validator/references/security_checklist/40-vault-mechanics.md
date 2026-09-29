# Security checklist: Vault Mechanics

## S3. Vault mechanics

This is the authoritative statement of Ansible Vault for both skills.

**Encrypt one value into a variable.**

```bash
ansible-vault encrypt_string --stdin-name 'vault_app_db_password'
```

Paste the block into `group_vars/<group>/vault.yml`. Reference it from
`group_vars/<group>/vars.yml` as
`app_db_password: "{{ vault_app_db_password }}"`, so that a grep for
`app_db_password` finds a definition and not a wall of ciphertext.

**Encrypt a whole file.**

```bash
ansible-vault create  group_vars/production/vault.yml
ansible-vault encrypt group_vars/production/vault.yml
ansible-vault edit    group_vars/production/vault.yml
ansible-vault view    group_vars/production/vault.yml
```

**Vault IDs: one per environment, never one per project.**

```bash
ansible-vault encrypt_string --vault-id prod@prompt --stdin-name 'vault_x'
ansible-playbook site.yml --vault-id prod@~/.vault/prod.pass
```

A single password shared across environments means rotating it after a
production incident also rotates staging, so nobody rotates it.

**Rotate.**

```bash
ansible-vault rekey --vault-id prod@~/.vault/prod-old.pass \
                    --new-vault-id prod@~/.vault/prod-new.pass \
                    group_vars/production/vault.yml
```

Rekeying changes the file's encryption, not the secret inside it. When the
secret itself leaked, change the secret at its source first and then re-encrypt.

**Verify that a file that should be encrypted actually is.**

```bash
head -1 group_vars/production/vault.yml   # $ANSIBLE_VAULT;1.1;AES256
```

**Predicate.** Every file matching `*vault*.yml` under `group_vars/` and
`host_vars/` begins with `$ANSIBLE_VAULT`.

```bash
find group_vars host_vars -name '*vault*.yml' -print0 \
  | xargs -0 -I{} sh -c 'head -1 "{}" | grep -q "^\$ANSIBLE_VAULT" || echo "NOT ENCRYPTED: {}"'
```

**Where the vault password comes from in CI.** The password reaches the runner
as a masked variable; that half is `/alaa-gitlab-ci-cd`'s. This pair owns `--vault-id` on the command line and the
rule that a decrypt failure is fatal: a play that cannot decrypt its vault
stops, and does not continue with the variable undefined.
