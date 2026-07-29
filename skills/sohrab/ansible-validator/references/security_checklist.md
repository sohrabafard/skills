# Security predicates, and the command that evaluates each one

This file is the pair's single statement of the Ansible security predicates and
of Ansible Vault mechanics. `ansible-generator` (`/ansible-generator`,
`$ansible-generator`) keeps only the authoring-time shape rules — where `no_log`
goes, what `mode` to write — and cites this file by line for everything else.

A checklist item with no command that evaluates it is a preference. Every
predicate below names its command.

**Whose decision a finding is.** This skill reports. It does not decide whether
a finding blocks a change. `/alaa-security-review` (`$alaa-security-review`)
owns fail-closed doctrine for security decisions and `/alaa-reliability-sla`
(`$alaa-reliability-sla`) owns fail-open and degradation for availability. The
discriminating question, which you may quote: *when this dependency cannot
answer, does proceeding without it let something through that must not get
through?* A secret-scan finding answers yes, so it is fail-closed by default.

**A scan that could not run is a blocked audit, not a clean one.** Every script
here exits 2 when it could not run, and 2 is never a pass.

---

## The three commands that make up an audit

All three run on every security audit, in any order.

```bash
bash scripts/validate_playbook_security.sh <target>   # Checkov, ansible + secrets
bash scripts/scan_secrets.sh <target>                 # Ansible-specific credential shapes
python3 scripts/check_task_safety.py <target>         # world-writable modes, shell injection
```

**Why three and not one.** Each covers what the others cannot, measured
2026-07-29 against `test/fixtures/secrets/planted-secrets.yml`:

| Tool | Catches | Misses |
|---|---|---|
| Checkov `--framework ansible` | TLS, HTTPS and GPG policy: 12 `CKV_ANSIBLE_*` and `CKV2_ANSIBLE_*` checks | every credential. It reported **zero** of the six planted secrets. |
| Checkov `--framework secrets` | generic credential shapes: AWS keys, private-key blocks, basic-auth URLs, high-entropy literals. Reported five failed checks covering all six planted secrets. | Ansible conventions: it did not report the plaintext `db_password: "hunter2-plaintext"`, which is neither high-entropy nor a generic shape. |
| `scan_secrets.sh` | credential-shaped variable names assigned a literal, connection strings with an inline password, and the absence of vault indirection | anything that is not shaped like an assignment. |
| `check_task_safety.py` | a `mode` that grants write to `other`; a Jinja expression in a `command`, `shell` or `raw` value without `\| quote` | everything else. |

So the mandated Checkov invocation is `--framework ansible,secrets`, never
`--framework ansible` alone. `references/source-map.md` carries the measured
table and the command that re-derives it; `scripts/lib/checkov_scan.sh`
implements it.

---

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

## S2. `no_log` covers every task that can print a secret

**Predicate.** `no_log: true` is set on any task whose module arguments or
registered result can contain a value sourced from a vault file, from
`lookup('env', ...)`, or from a variable whose name matches
`(pass|secret|token|key|credential)`.

**Evaluate.**

```bash
ansible-lint -c assets/.ansible-lint <target>   # rule no-log-password
bash scripts/scan_secrets.sh <target>
```

**What `no_log` does not cover.** `--diff` prints the content of a templated
file. A template that renders a secret into a configuration file leaks it into
the diff of a check-mode run even when the task carries `no_log: true`, because
the diff is produced by the file module and not by the argument logger. When a
template renders a secret, either set `diff: false` on that task or accept that
`--check --diff` output is itself sensitive and handle it accordingly.

## S3. Vault mechanics

This is the authoritative statement of Ansible Vault for both skills.

**Encrypt one value into a variable.**

```bash
ansible-vault encrypt_string 'the-secret-value' --name 'vault_app_db_password'
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
ansible-vault encrypt_string --vault-id prod@prompt 'value' --name 'vault_x'
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
as a masked variable; that half is `/alaa-gitlab-ci-cd`'s
(`$alaa-gitlab-ci-cd`). This pair owns `--vault-id` on the command line and the
rule that a decrypt failure is fatal: a play that cannot decrypt its vault
stops, and does not continue with the variable undefined.

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

## S5. Every written path has an explicit mode, and none is world-writable

**Predicate.** Every `file`, `copy` and `template` task states `mode`, and no
mode grants write to `other`.

**Evaluate.**

```bash
ansible-lint -c assets/.ansible-lint <target>     # rule risky-file-permissions
python3 scripts/check_task_safety.py <target>     # rule mode[world-writable]
```

ansible-lint reports the *absent* mode. It does not report a permissive one:
`yaml[octal-values]` fires on the unquoted form only, so `mode: '0777'` on a
directory and `mode: '0666'` on a secret both pass a production-profile run.
`check_task_safety.py` exists for that gap.

**The table.**

| What | Mode | Directory |
|---|---|---|
| Private key, vault file, credential | `'0600'` | `'0700'` |
| Configuration holding a secret | `'0640'` | `'0750'` |
| Configuration with no secret | `'0644'` | `'0755'` |
| Executable | `'0755'` | `'0755'` |
| Log file | `'0640'` | `'0750'` |

Quote every mode. An unquoted `0644` is the integer 420 in YAML, and the module
then applies a mode nobody wrote.

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

## S7. Transport is encrypted and verified

**Predicate.** No `get_url` or `uri` task uses an `http://` URL, and none sets
`validate_certs: false`.

**Evaluate.**

```bash
bash scripts/validate_playbook_security.sh <target>
# CKV_ANSIBLE_1  uri disabling certificate validation
# CKV_ANSIBLE_2  get_url disabling certificate validation
# CKV2_ANSIBLE_1 uri over HTTP
# CKV2_ANSIBLE_2 get_url over HTTP
```

A task that sets `validate_certs: false` carries a comment naming the internal
certificate authority it is working around and a linked issue for installing
that authority on the target. "Only disable for testing" is not a rule, because
nothing distinguishes testing from production in the file.

A `get_url` that fetches an artifact states a `checksum`. Transport encryption
proves who served the bytes, not which bytes they served.

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

## S9. A service binds to an address, not to everything

**Predicate.** No default in a shipped role sets a bind address of `0.0.0.0`.

**Evaluate.**

```bash
grep -rn "0\.0\.0\.0" <target>
```

Read the result: a bind address of `0.0.0.0` in `defaults/main.yml` is a role
whose out-of-the-box behaviour is to listen on every interface, including the
one facing the internet. Default to `127.0.0.1` and make the wider bind an
explicit override.

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

## S11. A security-relevant change is visible after the fact

**Predicate.** A play that creates an account, grants a privilege or writes a
credential emits a record an operator can find later.

Whether a signal is required, what gates on it and why is
`/alaa-observability-soc`'s (`$alaa-observability-soc`). The shared field names
and the metric catalogue are `/alaa-services-contract`'s
(`$alaa-services-contract`). This skill owns only the assertion that the play
emits something, and the SARIF and JSON emission of its own findings:

```bash
bash scripts/validate_playbook.sh playbook.yml --format json
ansible-lint -c assets/.ansible-lint --sarif-file ansible-lint.sarif <target>
```

## S12. The tools that are not this skill's

`ansible-lint --profile safety` is the security-leaning profile. There is **no**
`security` profile; `--profile security` is rejected by argparse, and both
skills documented it until 2026-07-29. The profiles are min, basic, moderate,
safety, shared, production.

`ansible-galaxy collection scan` does not exist and never has. The subcommands
are download, init, build, publish, install, list and verify. Use
`ansible-galaxy collection verify` to check an installed collection against its
signed manifest.

For repository-wide secret prevention rather than one-off scanning,
`git secrets --scan` and a pre-commit hook belong to the repository, not to this
skill. `/alaa-security-review` (`$alaa-security-review`) owns which controls a
repository must carry.
