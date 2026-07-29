# Official-first source map, and the freshness procedure

This is the pair's single source map. `ansible-generator` (`/ansible-generator`,
`$ansible-generator`) does not keep a second copy; it routes here. Read this
file before making any version-sensitive claim about Ansible, a collection,
ansible-lint, Molecule or Checkov.

Official and primary documentation outranks examples, blogs, issue threads and
Stack Overflow. Community material explains an observed failure; it does not
establish that a module parameter exists.

## Primary sources

| Subject | URL |
|---|---|
| Ansible documentation home | https://docs.ansible.com/projects/ansible/latest/ |
| Playbooks guide | https://docs.ansible.com/projects/ansible/latest/playbook_guide/ |
| Inventory guide | https://docs.ansible.com/projects/ansible/latest/inventory_guide/ |
| Collections guide | https://docs.ansible.com/projects/ansible/latest/collections_guide/ |
| Collection and module index | https://docs.ansible.com/ansible/latest/collections/ |
| Playbook keywords reference | https://docs.ansible.com/projects/ansible/latest/reference_appendices/playbooks_keywords.html |
| Ansible Vault guide | https://docs.ansible.com/projects/ansible/latest/vault_guide/ |
| Porting guides | https://docs.ansible.com/projects/ansible/latest/porting_guides/ |
| Releases and maintenance | https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html |
| `ansible-playbook` CLI | https://docs.ansible.com/projects/ansible/latest/cli/ansible-playbook.html |
| `ansible-test` | https://docs.ansible.com/projects/ansible/latest/dev_guide/testing_running_locally.html |
| ansible-lint rules | https://docs.ansible.com/projects/lint/rules/ |
| ansible-lint profiles | https://docs.ansible.com/projects/lint/profiles/ |
| Molecule documentation | https://docs.ansible.com/projects/molecule/ |
| Molecule installation | https://docs.ansible.com/projects/molecule/installation/ |
| Molecule pre-ansible-native configuration | https://docs.ansible.com/projects/molecule/pre-ansible-native/ |
| Checkov Ansible policy index | https://www.checkov.io/5.Policy%20Index/ansible.html |
| Checkov secrets policy index | https://www.checkov.io/5.Policy%20Index/secrets.html |

The two `ansible.readthedocs.io` hostnames that both skills carried until
2026-07-29 (`ansible.readthedocs.io/projects/lint/rules/` and `.../molecule/`)
still resolve, with a 302 to `docs.ansible.com`. The canonical host is the one
in the table above.

## Pinned values, and the command that re-derives each one

Verified 2026-07-29. A version written into a file goes stale silently, so each
row carries the command that re-derives it. `scripts/setup_tools.sh` compares
the installed toolchain against the floors in `scripts/requirements.txt` and
exits 1 when a floor is not met, so the check is executable rather than a note.

| Value | As of 2026-07-29 | Re-derive with |
|---|---|---|
| `ansible-core` latest | 2.21.2, released 2026-07-13 | `python3 -m pip index versions ansible-core` |
| `ansible-core` supported control-node Python | 3.12 or newer; 2.20 and later declare `requires_python >=3.12` | `curl -s https://pypi.org/pypi/ansible-core/json \| python3 -c "import json,sys;d=json.load(sys.stdin);print(d['info']['version'],d['info']['requires_python'])"` |
| `ansible-core` supported target Python | 3.9 or newer | the 2.20 porting guide, under Porting guides above |
| `ansible-core` maintained branches | 2.21 full support; 2.20 security-only; 2.19 security-only to November 2026 | Releases and maintenance page |
| `ansible` community package latest | 14.2.0, released 2026-07-14, depends on `ansible-core~=2.21.2` | `python3 -m pip index versions ansible` |
| `ansible-lint` latest | 26.6.0, released 2026-06-30, `requires_python >=3.10` | `python3 -m pip index versions ansible-lint` |
| `ansible-lint` rule count | 52 | `ansible-lint -L` |
| `ansible-lint` profiles | min, basic, moderate, safety, shared, production. There is no `security` profile; the nearest is `safety`. | `ansible-lint --help \| grep -- --profile` |
| `yamllint` latest | 1.38.0, released 2026-01-13 | `python3 -m pip index versions yamllint` |
| `molecule` latest | 26.6.0, released 2026-06-30 | `python3 -m pip index versions molecule` |
| `molecule-plugins` latest | 26.7.15, released 2026-07-15. This is the current driver package. | `python3 -m pip index versions molecule-plugins` |
| `molecule-docker` | 2.1.0, last released 2022-09-29. Retired route; the installation guide tells upgraders to uninstall it. | `python3 -m pip index versions molecule-docker` |
| `molecule` actions | check, cleanup, converge, create, dependency, destroy, drivers, idempotence, init, list, login, matrix, prepare, reset, side-effect, syntax, test, verify. There is no `lint` action. | `molecule --help` |
| `molecule` drivers on a stock install | `default` only; `docker` appears once `molecule-plugins[docker]` is installed | `molecule drivers` |
| `checkov` latest | 3.3.8, released 2026-07-09 | `python3 -m pip index versions checkov` |
| Checkov Ansible policies | 12 `CKV_ANSIBLE_*` and `CKV2_ANSIBLE_*` checks, all about TLS, HTTPS and GPG | Checkov Ansible policy index above |

**What the Python floor means in practice.** On a Python 3.11 control node,
`pip install ansible-core` resolves 2.19.x and says nothing about why. That is a
branch on security-only support that reaches end of life in November 2026, so a
validation run there is measuring against a core the vendor is about to stop
patching. `scripts/setup_tools.sh` reports the control-node Python version and
warns when it is below 3.12 for exactly this reason.

## The Checkov invocation this skill mandates, and why

`checkov --framework ansible,secrets`. Never `--framework ansible` alone.

Measured 2026-07-29 with checkov 3.3.8 against
`test/fixtures/secrets/planted-secrets.yml`, which carries six planted
credentials, using `-o json --skip-download --quiet`:

| Invocation | passed | failed | Check IDs |
|---|---|---|---|
| `--framework ansible` | 0 | 0 | none |
| `--framework secrets` | 0 | 5 | `CKV_SECRET_2` (AWS access key), `CKV_SECRET_4` (basic auth credentials), `CKV_SECRET_6` twice (high-entropy string), `CKV_SECRET_13` (private key) |
| `--framework ansible,secrets` | 0 | 5 | the same five |

The Ansible framework models TLS, HTTPS and GPG policy and models no credential
shape at all, so running it alone is a security scan that cannot see a leaked
AWS key. Neither framework replaces `scripts/scan_secrets.sh`: on the same
fixture Checkov did not report the plaintext `db_password: "hunter2-plaintext"`
that `scan_secrets.sh` reports, because that value is neither high-entropy nor a
generic credential shape. `references/security_checklist.md` states the division
of labour once, and `scripts/lib/checkov_scan.sh` implements it.

Re-derive the table with:

```bash
for fw in ansible secrets ansible,secrets; do
  echo "== $fw"
  checkov -f test/fixtures/secrets/planted-secrets.yml \
    --framework "$fw" -o json --skip-download --quiet
done
```

`--skip-download` stops Checkov reaching `api0.prismacloud.io` for guideline
text. In a locked-down runner that call fails with a proxy traceback that buries
the report; the policies themselves are local and unaffected.

## Freshness triggers

Fetch current official documentation when the task mentions `latest`, `current`,
a specific Ansible or collection version, a module parameter you have not
confirmed, an execution environment, an ansible-lint rule's behaviour, vault
handling, or a collection this skill does not already name.

For a fully qualified module name specifically, fetch nothing: run
`python3 scripts/check_module_currency.py <path>`. It reads ansible-core's own
`config/ansible_builtin_runtime.yml` routing table offline and reports any
`ansible.builtin.*` name that now works only through a compatibility redirect.
That is the defect class this pair measured at 8.8% across the 34
`ansible.builtin` names the generator teaches, and a scheduled run of that
script is the only thing that stops it recurring.

## Troubleshooting-only sources

Stack Overflow, GitHub issues, forum posts and community blogs explain an
observed failure and generate hypotheses. Confirm any normative module syntax,
security guidance or compatibility claim against the primary sources above
before writing it into a file.

## Documentation lookup through an MCP server

When a `mcp__context7__resolve-library-id` tool is present in the session, use
it and then `mcp__context7__get-library-docs` for a collection's documentation,
because the result is structured. When it is not present, use `WebSearch`
against the primary sources above. Neither path is a prerequisite: every claim
this skill makes about ansible-core is derivable offline from the installed
package, and a validation run does not stop because an MCP server is absent.
