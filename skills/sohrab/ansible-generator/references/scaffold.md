# The scaffold

Read this when creating a new role, playbook, inventory or project. It describes
`assets/templates/`, the placeholder convention, and the check that proves the
result.

Every file under `assets/templates/` parses as YAML before substitution, and
`python3 scripts/check_templates.py --scaffold assets/templates` proves it. That
was not true until 2026-07-29: six of the eight YAML files failed
`yaml.safe_load`, so an agent following "copy the role structure from
`assets/templates/role/`" started from files that could not load.

---

## The placeholder convention

Two token shapes, both bare YAML scalars, so a template parses before anyone
touches it:

| Token | Meaning | Example |
|---|---|---|
| `ROLE_NAME` | the role's name, used as the variable prefix | `ROLE_NAME_port` becomes `nginx_port` |
| `CHANGE_ME_<what>` | a value you must supply | `CHANGE_ME_package` becomes `nginx` |

Substitute with a plain textual replacement of `ROLE_NAME` first, then each
`CHANGE_ME_*` token. Longest token first, so that `CHANGE_ME_service_user` is
not partly eaten by `CHANGE_ME_service`.

**Do not reintroduce the bracketed form.** `[ role_name ]_port: [ default_port ]`
is not a placeholder: YAML reads `[ role_name ]` as a one-element flow sequence,
so the line is a mapping key that begins with a sequence and the file does not
load. `check_templates.py` reports it as `placeholder[bracketed]`, and
`test/fixtures/broken-bracket-placeholder.yml` is the regression fixture.

## What each template is

### `assets/templates/role/`

A complete role. Copy the directory, substitute, then delete what the role does
not use rather than leaving an empty `templates/`.

| File | What it is |
|---|---|
| `tasks/main.yml` | the task list, opening with the OS-family `include_vars` |
| `handlers/main.yml` | restart and reload handlers |
| `defaults/main.yml` | what a caller may override, with a comment per variable |
| `vars/main.yml` | what a caller must not override, and derived values |
| `vars/Debian.yml`, `vars/RedHat.yml` | package and service names per OS family |
| `meta/main.yml` | `min_ansible_version`, the tested platform list, tags |
| `meta/argument_specs.yml` | the role's declared interface, with types |
| `templates/config.j2` | a configuration template using the role's variables |
| `README.md` | the variable table, one worked example, the platform list |

### `assets/templates/playbook/basic_playbook.yml`

A single play with `pre_tasks`, `tasks`, `post_tasks` and `handlers`, a header
comment in the documented shape, and a health check that shows the
`until`/`retries`/`delay` mechanism.

### `assets/templates/inventory/`

`hosts` in INI form, `group_vars/all.yml`, two group files and one host file.
These are worked examples rather than substitution templates: copy them and edit
the values.

### `assets/templates/project/`

| File | What it is |
|---|---|
| `ansible.cfg` | validated clean by `ansible-config validate -t all`; `host_key_checking = True`, no blanket `become`, fact cache outside `/tmp` |
| `requirements.yml` | the two collections a normal project needs, with floors, and commented examples for the rest |
| `.ansible-lint` | **a copy**, owned by `ansible-validator` (`/ansible-validator`, `$ansible-validator`) at its `assets/.ansible-lint` |

**On `.ansible-lint`.** This skill does not own a lint configuration. The file
in `assets/templates/project/` is a copy with a header comment naming the owner,
because two divergent forks of one config mean the lint result depends on which
copy an agent happened to pick. To change it, change it in `ansible-validator`,
where `scripts/check_assets.sh` proves that every rule in its `enable_list`
still fires on a fixture built to violate it, then copy the result back.

The 267-line file this scaffold shipped until 2026-07-29 was rejected outright
by ansible-lint with exit 3 — `'severity' was unexpected`, from a per-rule
severity block that is not a supported option — so every scaffolded project was
unlintable until a human deleted 113 lines of it.

**This skill does not scaffold a `molecule/` directory.** A scenario it cannot
run is a scenario nobody has proved. `ansible-validator references/molecule.md`
owns Molecule, including the template and the condition under which running a
scenario is correct.

## Creating a role, end to end

```bash
ROLE=nginx
mkdir -p roles/$ROLE
cp -r <ansible-generator>/assets/templates/role/. roles/$ROLE/

# Substitute. Do ROLE_NAME first, then each CHANGE_ME_* token.
grep -rl 'ROLE_NAME\|CHANGE_ME_' roles/$ROLE | while read -r f; do
  sed -i "s/ROLE_NAME/${ROLE}/g" "$f"
done
grep -rn 'CHANGE_ME_' roles/$ROLE      # every remaining token needs a value

# Prove the result before anyone runs it.
python3 <ansible-generator>/scripts/check_templates.py roles/$ROLE
bash    <ansible-validator>/scripts/validate_role.sh   roles/$ROLE
```

`check_templates.py` reports any surviving `CHANGE_ME_*` or `ROLE_NAME` token as
`placeholder[unsubstituted]`, which is the observable form of the old
instruction "replace all `[PLACEHOLDERS]` with actual values".

`test/fixtures/scaffold_role/` is that procedure carried out once and committed:
the shipped scaffold with `ROLE_NAME` set to `demo_nginx` and every token
supplied. `scripts/check_templates.py --self-test` asserts it is clean in output
mode, and `validate_role.sh` passes it with no findings. When you change a
template, regenerate that fixture in the same change.

## Creating a project

```bash
mkdir -p inventory/production/{group_vars,host_vars} roles playbooks
cp <ansible-generator>/assets/templates/project/ansible.cfg      .
cp <ansible-generator>/assets/templates/project/requirements.yml .
cp <ansible-generator>/assets/templates/project/.ansible-lint    .
cp -r <ansible-generator>/assets/templates/inventory/. inventory/production/

ansible-galaxy collection install -r requirements.yml
ansible-config validate -t all
```

Add `.ansible-cache/` to `.gitignore`: `ansible.cfg` points the fact cache and
the log there, and neither belongs in version control.

One inventory directory per environment. Sharing one inventory between
production and staging and switching on a variable means a mistyped `--limit`
reaches production.

## After editing a template

```bash
python3 scripts/check_templates.py --scaffold assets/templates
python3 <ansible-validator>/scripts/check_module_currency.py assets/templates
```

The first proves every template still parses, still uses canonical booleans and
still carries its substitution tokens. The second proves no example names a
module that ansible-core no longer provides directly. Then regenerate
`test/fixtures/scaffold_role/` and re-run
`bash <ansible-validator>/scripts/validate_role.sh test/fixtures/scaffold_role`.
