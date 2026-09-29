# Security checklist: Audit Commands

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
