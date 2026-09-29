# Corpus usage

When running or selecting checks from the existing corpus, use this guide. It owns the directory map, fixture pairs, exact checker commands and CI contract.

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

## The playbook pair

`playbooks/good-playbook.yml` exits 0 on every checker.

`playbooks/bad-playbook.yml` exits 1, and `playbooks/expected-findings.md`
records which checker reports each defect. That file is the contract: when a
checker stops reporting one of them, the corresponding assertion fails.

Do not fix either playbook. `bad-playbook.yml` is deliberately wrong.

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

The job that runs `bash scripts/self_test.sh` is `/alaa-gitlab-ci-cd`'s: the image, the caching of the tool environment, the
`rules:` that decide when it runs, and how long the report is kept. This skill
owns what the script asserts and what its exit codes mean. Gate on exit 0; treat
exit 2 as a hard stop, because a self-test that could not run has proved
nothing.

Run synthetic authority, redaction and Molecule-failure regressions with
`python scripts/test_security_regressions.py --bash <explicit-bash-path>`.
They substitute mock tools and need no installed Ansible or Molecule.
