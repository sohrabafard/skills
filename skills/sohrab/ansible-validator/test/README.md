# The test corpus

This directory is the pair's fixture corpus. `ansible-generator`
(`/ansible-generator`, `$ansible-generator`) keeps one scaffold fixture of its
own and routes here for everything else.

Every fixture is referenced by a `--self-test` in `scripts/`. Run the whole set
with:

```bash
bash scripts/self_test.sh
```

From a fresh checkout with `scripts/requirements.txt` installed, that exits 0
and reports 63 assertions. Exit 2 means the toolchain is missing, not that the
skill is broken.

## Layout

```
test/
├── README.md
├── playbooks/
│   ├── good-playbook.yml          must exit 0 on every checker
│   ├── bad-playbook.yml           must exit 1, with the findings listed below
│   └── expected-findings.md       what each checker must report on bad-playbook
├── fixtures/
│   ├── secrets/                   scan_secrets.sh and the Checkov frameworks
│   ├── yaml/                      the inverted-YAML-stage regression
│   ├── roles/                     validate_role.sh, clean and broken
│   ├── tasks/                     check_task_safety.py
│   ├── lint/                      check_assets.sh
│   ├── fqcn/                      check_fqcn.py
│   ├── modules/                   check_module_currency.py
│   └── extract/                   extract_ansible_info.py
└── roles/
    └── geerlingguy.mysql/         vendored third-party integration fixture
```

## Why each fixture exists

A fixture whose only job is to be present proves nothing. Each of these exists
because a shipped defect got past every check until it did.

| Fixture | The defect it pins down |
|---|---|
| `fixtures/yaml/broken-with-doc-start.yml`, `fixtures/roles/broken_yaml_role/` | `validate_role.sh` read `grep`'s exit status instead of `yamllint`'s. Since `grep` exits 0 whenever it printed anything, and every conventional Ansible file starts with `---` which the old `.yamllint` flagged, the YAML stage of role validation could never report a failure. It printed five `syntax error` lines and then `YAML syntax check passed`. |
| `fixtures/yaml/clean-no-doc-start.yml` | the other half of the same contradiction: a clean file with no `---` was counted as a failure. |
| `fixtures/secrets/planted-secrets.yml` | `scan_secrets.sh` wrote extended regular expressions and called basic `grep`, so `AKIA[A-Z0-9]{16}` matched a literal `{16}` and the highest-signal credential shape in the list was undetectable. Six credentials, one per shape; the self-test asserts all six by name. |
| `fixtures/secrets/vaulted-clean.yml` | the symmetric defect: a correctly vaulted playbook was reported as two secrets and exited 1. A scanner that red-lights the correct pattern gets switched off. |
| `fixtures/lint/unnamed-task.yml`, `lowercase-task-name.yml` | `assets/.ansible-lint` set `task_name_prefix: "{path}:"`; `{path}` is not a valid substitution key, ansible-lint swallowed the `KeyError`, and `NameRule` died silently. The config disabled the two rules its own `enable_list` asked for. |
| `fixtures/lint/truthy-yes.yml`, `document-start.yml` | the two shipped lint configs contradicted each other about `become: yes` and about the leading `---`. |
| `fixtures/tasks/unsafe-tasks.yml` | nothing in the toolchain reported `mode: '0777'` on a directory or `{{ user_input }}` inside `shell:`. Both pass a production-profile lint run and Checkov's ansible framework. |
| `fixtures/fqcn/fqcn-correct.yml` | `check_fqcn.sh` reported the `group:` parameter of a template task and the `gather_facts:` play keyword as modules. |
| `fixtures/modules/stale-fqcns.md` | three of the 34 `ansible.builtin.*` names the generator taught had left core and worked only through a redirect: an 8.8% defect rate that nothing reported. |
| `fixtures/extract/block-nesting.yml` | `extract_ansible_info.py` listed `block`, `rescue` and `always` in its skip set and `continue`d before the recursion below it, so no module inside a `block:` was ever seen. |
| `fixtures/roles/clean_role/` | the positive control. A role with no findings must exit 0, or the negative fixtures prove nothing. |

## The playbook pair

`playbooks/good-playbook.yml` exits 0 on every checker.

`playbooks/bad-playbook.yml` exits 1, and `playbooks/expected-findings.md`
records which checker reports each defect. That file is the contract: when a
checker stops reporting one of them, the corresponding assertion fails.

Do not fix either playbook. `bad-playbook.yml` is deliberately wrong.

## The vendored role: `roles/geerlingguy.mysql/`

**Status: kept, as a third-party integration fixture with stated provenance.**

**Provenance.**

| Field | Value |
|---|---|
| Upstream | https://github.com/geerlingguy/ansible-role-mysql |
| Galaxy name | `geerlingguy.mysql` |
| Licence | MIT. The upstream `LICENSE` file must travel with the vendored tree; vendoring the code without it is a redistribution defect rather than a testing question. |
| Why it is here | It is a large, well-built, multi-platform role with real Molecule configuration. Validating a first-party fixture proves the checkers run; validating a real role proves they run on something nobody wrote for them. |
| Pin | recorded in `roles/geerlingguy.mysql/.fixture-version`, one line: the upstream tag, or the literal `unestablished` |

**The pin is `unestablished` as of 2026-07-29.** The tree was vendored into this
repository before 2026-03-12 with no pin recorded, and the upstream tag it came
from cannot be recovered from the vendored files alone — they carry no version
string. Its `vars/Debian-13.yml` and `vars/RedHat-10.yml` place it on a recent
line, and nothing more precise than that is established. Do not write a tag into
`.fixture-version` by inference; the only thing that establishes the pin is the
refresh below, which replaces the tree with a known tag. Until that runs, treat
this fixture as evidence that the checkers run on third-party code, not as a
regression baseline against a known upstream state.

**Refresh rule.** Re-sync at most once per calendar quarter, and only in a
change that does nothing else:

```bash
rm -rf test/roles/geerlingguy.mysql
ansible-galaxy role install geerlingguy.mysql,<tag> -p test/roles --force
printf '%s\n' '<tag>' > test/roles/geerlingguy.mysql/.fixture-version
bash scripts/validate_role.sh test/roles/geerlingguy.mysql
```

A refresh that changes the validator's verdict on this role is a finding about
the validator or about the role, and it is investigated before the refresh is
merged. A refresh with no pin recorded is reverted.

**Scope.** `assets/.ansible-lint` excludes `test/roles/` from directory scans,
because this skill does not own third-party code and will not report findings
about it during a project scan. Explicit file and directory targets bypass
`exclude_paths`, so the command above still lints it deliberately.
`test/playbooks/` and `test/fixtures/` are **not** excluded: a fixture corpus
the lint config hides is a corpus that proves nothing.

**Do not add more vendored roles by `git clone`.** One pinned integration
fixture answers the question "do the checkers work on code nobody wrote for
them". A second answers nothing new and doubles the licence surface. If a
specific defect needs a second real role, add it with a pin, a licence file and
a line in the table above saying which defect it pins down.

## Adding a fixture

A new fixture is added together with the assertion that consumes it. The
assertion states the exit code, and where the exit code alone would not prove
the point — because several findings could carry the same code — it also asserts
the finding by name, as `scan_secrets.sh --self-test` does for its six shapes.

## Running one checker against the corpus

```bash
bash scripts/validate_playbook.sh test/playbooks/good-playbook.yml       # 0
bash scripts/validate_playbook.sh test/playbooks/bad-playbook.yml        # 1
bash scripts/validate_role.sh     test/fixtures/roles/clean_role         # 0
bash scripts/validate_role.sh     test/fixtures/roles/broken_yaml_role   # 1
bash scripts/scan_secrets.sh      test/fixtures/secrets/planted-secrets.yml  # 1
bash scripts/scan_secrets.sh      test/fixtures/secrets/vaulted-clean.yml    # 0
python3 scripts/check_task_safety.py    test/fixtures/tasks/unsafe-tasks.yml # 1
python3 scripts/check_fqcn.py           test/fixtures/fqcn/short-names.yml   # 1
python3 scripts/check_module_currency.py test/fixtures/modules/stale-fqcns.md # 1
bash scripts/check_assets.sh                                              # 0
```

## Using the corpus in CI

The job that runs `bash scripts/self_test.sh` is `/alaa-gitlab-ci-cd`'s
(`$alaa-gitlab-ci-cd`): the image, the caching of the tool environment, the
`rules:` that decide when it runs, and how long the report is kept. This skill
owns what the script asserts and what its exit codes mean. Gate on exit 0; treat
exit 2 as a hard stop, because a self-test that could not run has proved
nothing.
