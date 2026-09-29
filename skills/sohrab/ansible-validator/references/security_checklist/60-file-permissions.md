# Security checklist: File Permissions

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
