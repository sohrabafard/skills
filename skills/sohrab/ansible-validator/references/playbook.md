# The validation procedure

Read this when running a full validation. `SKILL.md` is the router and carries
the script table; this file carries the procedure, the tool-by-tool detail and
the worked scenarios. Nothing here restates the body.

---

## The stage table

Run the stages in this order. Each row names what the stage asserts, what its
exit code means, and where to go when it fails. Earlier stages produce clearer
messages than later ones about the same defect, which is why the order matters:
a YAML parse error reported by yamllint names a line, and the same file reported
by ansible-lint names a crash.

| # | Stage | Command | Asserts | Exit meaning | On failure read |
|---|---|---|---|---|---|
| 0 | Toolchain | `bash scripts/setup_tools.sh` | every required tool is installed and at or above its floor | 1 a tool is missing or too old | `references/source-map.md` |
| 1 | YAML | `bash scripts/validate_playbook.sh <file>` stage 1 | the file is well-formed YAML | 1 findings, 2 yamllint could not run | `references/failure-classes.md` class A |
| 2 | Ansible syntax | same script, stage 2 | Ansible can load the play, its includes and its role references | 1 findings | class B |
| 3 | Lint | same script, stage 3 | the artifact satisfies the production profile | 1 findings, 2 the config is rejected | `references/best_practices.md` |
| 4 | FQCN | `bash scripts/check_fqcn.sh <target>` | every task action is fully qualified | 1 findings | `references/module_alternatives.md` |
| 5 | Module currency | `python3 scripts/check_module_currency.py <target>` | no `ansible.builtin.*` name works only through a redirect | 1 findings | `references/module_alternatives.md` |
| 6 | Security | `bash scripts/validate_playbook_security.sh <target>`, `bash scripts/scan_secrets.sh <target>`, `python3 scripts/check_task_safety.py <target>` | no credential literal, no world-writable mode, no unquoted Jinja in a shell, no disabled certificate validation | 1 findings, 2 a scanner could not run | `references/security_checklist.md` |
| 7 | Check mode | `ansible-playbook -i <inv> <playbook> --check --diff --limit <hosts>` | the play's intended changes are the changes you expect | non-zero a task would fail | class G |
| 8 | Molecule | `bash scripts/test_role.sh <role> <scenario> --i-confirm-disposable-host` | the role applies, is idempotent and verifies | 1 a stage failed, 2 the scenario could not start | `references/molecule.md` |

Stage 8 runs only under the condition `references/molecule.md` states. Stage 7
runs only when an inventory is available and the caller has named a `--limit`.

**Exit codes, identically in all scripts:** `0` clean, `1` findings, `2` could
not run, `64` usage error. A CI gate treats `2` as a hard stop. Before
2026-07-29 every script returned `1` for "no argument", "target not found",
"tool unavailable" and "findings present" alike, so a gate built on any of them
treated a missing tool as a pass.

## Reporting a finding

Every reported finding cites the reference line that supplies its remediation,
in the form `references/<file>` plus the rule or class identifier. A finding
with no citation is not reported, because a finding an operator cannot act on is
noise. That is the observable form of the old instruction that reference files
"must be consulted"; nothing could check the old form.

A report has four parts and no more:

1. **What ran**, with the exit code of each script.
2. **What failed**, one line per finding: file, line, rule identifier, and the
   reference citation.
3. **What was blocked**, one line per stage that exited 2, with the reason. A
   blocked stage is never folded into "passed".
4. **The verdict**, which is `PASS`, `FAIL` or `BLOCKED`, and never a mixture.

Machine-readable output for a gate or an aggregator:

```bash
bash scripts/validate_playbook.sh playbook.yml --format json
python3 scripts/check_fqcn.py playbook.yml --format json
python3 scripts/check_task_safety.py playbook.yml --format json
ansible-lint -c assets/.ansible-lint --sarif-file ansible-lint.sarif <target>
```

Where the artifact goes and how long it is retained is `/alaa-gitlab-ci-cd`'s
(`$alaa-gitlab-ci-cd`). Whether a signal is required at all is
`/alaa-observability-soc`'s (`$alaa-observability-soc`).

## The stopping condition

Fix, re-run, repeat — with a bound. **If two consecutive fix-and-re-run cycles
do not reduce the failure count, stop and report the remaining findings.** An
unbounded loop on a finding you cannot move is worse than a report that names it.

## Stage detail

### YAML

```bash
yamllint -c assets/.yamllint -f parsable <file>
```

`-f parsable` gives `path:line:col: [level] message (rule)`, which is greppable
and stable across releases. The configuration is resolved in this order: the
`--yamllint-config` flag, then `ANSIBLE_VALIDATOR_YAMLLINT_CONFIG`, then the
nearest `.yamllint` found by walking up from the target, then this skill's
`assets/.yamllint`. A project with its own configuration is entitled to it;
before 2026-07-29 the scripts hardcoded the skill's copy with no override.

### Ansible syntax

```bash
ansible-playbook <playbook> --syntax-check
ansible-playbook -i <inventory> <playbook> --syntax-check
```

For a role, `scripts/validate_role.sh` copies the role into a scratch directory
under the system temporary directory, generates a one-play playbook that
includes it, and syntax-checks that. It copies rather than symlinks because
`ln -s` needs Developer Mode or elevation on Windows, and it works outside the
repository because the caller's mount may be read-only.

### ansible-lint

```bash
ansible-lint -c assets/.ansible-lint <target>
ansible-lint -L                                   # the 52 rules
ansible-lint --profile safety <target>            # the security-leaning profile
ansible-lint -x yaml[line-length] <target>        # exclude one rule for one run
ansible-lint --fix <target>                       # writes files; see below
```

Exit `0` clean, `1` or `2` violations, `3` the configuration file is rejected.
Exit 3 is a blocked run, not a finding, and the scripts report it as exit 2.

`--fix` writes the files before you see anything. Run it only on a clean working
tree, then read the diff before committing. There is no mode that shows the
change without making it.

**A rule that stops firing is a defect, not an improvement.** An invalid option
value can raise inside a rule; ansible-lint catches the exception, prints
`Ignored exception from <Rule>.matchtasks`, and continues with that rule dead.
`bash scripts/check_assets.sh` asserts that every rule named in the config's
`enable_list` still fires on the fixture built to violate it. Run it after any
edit to `assets/.ansible-lint`.

### Security

The three commands and the reason there are three are in
`references/security_checklist.md`. The one sentence that belongs here: the
mandated Checkov invocation is `--framework ansible,secrets`, because
`--framework ansible` models TLS, HTTPS and GPG policy and models no credential
shape at all.

### Check mode

```bash
ansible-playbook -i inventory playbook.yml --check --diff --limit web1.example.com
```

**State the `--limit`.** A check run still opens a connection to every host in
scope, still gathers facts, and still runs every task carrying
`check_mode: false`. On a large fleet that is a real load, and the
`--forks` value that makes it acceptable is `/alaa-reliability-sla`'s
(`$alaa-reliability-sla`), not this skill's.

Read the diff, not the summary. Check mode cannot see a change that depends on a
change an earlier task would have made, so a task reporting failure in a dry run
is not necessarily a task that would fail. `references/failure-classes.md` class
G separates the two.

### Custom modules and collections

`scripts/extract_ansible_info_wrapper.sh <target>` emits JSON naming the
modules, the collections, the collection versions and the unpinned collections.
Its classification reads the collection prefix of a fully qualified name; before
2026-07-29 it tested fully qualified names against a set of short names, so a
correct playbook reported four "custom" modules and a playbook of unqualified
builtins reported none at all.

When the output names a collection this skill does not cover, look it up as
`references/source-map.md` describes: an MCP documentation server when the
session has one, `WebSearch` against the primary sources otherwise. For a
module *name* specifically, look nothing up: run
`python3 scripts/check_module_currency.py`, which reads ansible-core's routing
table offline.

## Worked scenarios

### 1. "Check whether this playbook is valid"

```bash
bash scripts/validate_playbook.sh playbook.yml
bash scripts/check_fqcn.sh playbook.yml
bash scripts/scan_secrets.sh playbook.yml
python3 scripts/check_task_safety.py playbook.yml
```

Report the four exit codes and the findings with their citations. Do not run
check mode without an inventory and a `--limit`.

### 2. "Validate my role in ./roles/webserver"

```bash
bash scripts/validate_role.sh roles/webserver
bash scripts/validate_role_security.sh roles/webserver
bash scripts/scan_secrets.sh roles/webserver
python3 scripts/check_task_safety.py roles/webserver
python3 scripts/check_module_currency.py roles/webserver
```

If `roles/webserver/molecule/` exists, report that it exists and state whether
you are running it, under the condition in `references/molecule.md`.

### 3. "Run this playbook in check mode against production"

```bash
ansible-playbook -i inventory/production site.yml --check --diff --limit web1.example.com
```

Then widen the `--limit` only after reading the diff for the first host. Report
which tasks would change, which handlers would fire, and which tasks failed for
a check-mode reason rather than a real one. Whether applying it is safe is a
change-control question: `/alaa-controlled-ops` (`$alaa-controlled-ops`) owns
change control and proof strength.

### 4. "Audit this repository for security"

```bash
bash scripts/validate_role_security.sh .
bash scripts/scan_secrets.sh .
python3 scripts/check_task_safety.py .
find group_vars host_vars -name '*vault*.yml' -print0 \
  | xargs -0 -I{} sh -c 'head -1 "{}" | grep -q "^\$ANSIBLE_VAULT" || echo "NOT ENCRYPTED: {}"'
```

All findings cite `references/security_checklist.md`. Whether any of them blocks
the change is `/alaa-security-review`'s (`$alaa-security-review`).

### 5. "This role is not idempotent"

`references/failure-classes.md` class H. Diagnose with
`bash scripts/test_role.sh <role> default --i-confirm-disposable-host`, whose
idempotence stage compares every host.

## Running the checkers on themselves

```bash
bash scripts/self_test.sh
```

Every checker's `--self-test` runs against the fixtures under `test/` and
asserts the documented exit codes, including the missing-tool case. From a fresh
checkout with `scripts/requirements.txt` installed it exits 0. A `2` means the
toolchain is missing, not that the skill is broken.
