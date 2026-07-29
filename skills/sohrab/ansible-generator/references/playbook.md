# The generation procedure

Read this when actually generating anything. `SKILL.md` is the router; this file
carries the procedure by artifact type, the validation handoff and the delivery
format. Nothing here restates the body.

The validator this file hands to throughout is `ansible-validator`
(`/ansible-validator`, `$ansible-validator`); `<ansible-validator>` below stands
for that skill's directory.

---

## 1. Playbooks

**Triggered by:** "create a playbook to…", "build a playbook for…", "automate
…".

**Procedure.**

1. Establish four things before writing a line: the end state, the host group,
   which tasks need privilege escalation, and which OS families must work. A
   playbook written without the last one silently does nothing on an unlisted
   family.
2. Start from `assets/templates/playbook/basic_playbook.yml`.
   `references/scaffold.md` states the placeholder convention.
3. Write tasks in the shape of `references/best-practices.md` section A1, using
   `references/module-patterns.md` to pick the module.
4. Put the health check in `post_tasks` with `until`, `retries` and `delay`.
5. Run the delivery gate in section 6 below.

**Shape.**

```yaml
---
# Playbook: deploy_web.yml
# Description: Install nginx and render its configuration
# Requirements:
#   - ansible-core 2.19 or newer on the control node
#   - Target hosts: Ubuntu 22.04+, Debian 12+, EL 9+
# Variables:
#   - app_port: port the application listens on (optional, default 8080)
#   - app_version: version to deploy (required)
# Usage:
#   ansible-playbook -i inventory/production deploy_web.yml \
#     -e "app_version=1.4.2" --check --diff --limit web1.example.com

- name: Deploy and configure the web server
  hosts: webservers
  gather_facts: true

  vars:
    app_port: 8080

  pre_tasks:
    - name: Refresh the package cache on the Debian family
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600
      become: true
      when: ansible_os_family == "Debian"
      tags:
        - always

  tasks:
    - name: Ensure nginx is installed
      ansible.builtin.package:
        name: nginx
        state: present
      become: true
      tags:
        - install

    - name: Render the nginx configuration
      ansible.builtin.template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        owner: root
        group: root
        mode: "0644"
        backup: true
        validate: "/usr/sbin/nginx -t -c %s"
      become: true
      notify: Reload nginx
      tags:
        - configure

  post_tasks:
    - name: Verify nginx answers on the health endpoint
      ansible.builtin.uri:
        url: "http://127.0.0.1:{{ app_port }}/health"
        status_code: 200
      register: health_check
      until: health_check.status == 200
      retries: 5
      delay: 10
      tags:
        - verify

  handlers:
    - name: Reload nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
      become: true
```

`validate:` runs the service's own configuration checker against the candidate
file before it replaces the live one, so a bad render cannot take the service
down. `%s` is the candidate's path. Include it whenever the service ships a
checker.

`become` is on the tasks that need it, not on the play. A play-level `become`
escalates every read-only command too, and an audit cannot then tell which tasks
genuinely needed root.

## 2. Roles

**Triggered by:** "create a role for…", "make this reusable".

**Procedure.**

1. Copy `assets/templates/role/`, substitute, and delete what the role does not
   use. `references/scaffold.md` has the end-to-end commands.
2. Fill `meta/argument_specs.yml` first. Deciding the interface before the
   implementation is what stops a role reading six undeclared variables.
3. Prefix every role variable with the role name.
4. Put OS-specific package and service names in `vars/<family>.yml` and load
   them with `include_vars`, rather than branching in the task list.
5. Put every service restart behind a handler.
6. Write `README.md` from the template as you go.
7. Run the delivery gate in section 6.

## 3. Task files

**Triggered by:** "create tasks to…", "extract this into a task file".

A task file is a bare list of tasks, with no `hosts` and no `tasks:` key. It is
included with `ansible.builtin.include_tasks` (evaluated at run time, so it can
be conditional and looped) or `ansible.builtin.import_tasks` (evaluated at parse
time, so tags and `when` propagate differently). Choose `include_tasks` when the
inclusion itself depends on a variable.

```yaml
---
# Tasks: back up the application database

- name: Ensure the backup directory exists
  ansible.builtin.file:
    path: "{{ db_backup_dir }}"
    state: directory
    owner: postgres
    group: postgres
    mode: "0750"

- name: Dump the database
  community.postgresql.postgresql_db:
    name: "{{ db_name }}"
    state: dump
    target: "{{ db_backup_dir }}/{{ db_name }}_{{ ansible_date_time.date }}.sql"
    login_host: "{{ db_host }}"
    login_user: "{{ db_user }}"
    login_password: "{{ vault_db_password }}"
  no_log: true

- name: Compress the dump
  community.general.archive:
    path: "{{ db_backup_dir }}/{{ db_name }}_{{ ansible_date_time.date }}.sql"
    dest: "{{ db_backup_dir }}/{{ db_name }}_{{ ansible_date_time.date }}.sql.gz"
    format: gz
    mode: "0600"
    remove: true

- name: Find backups past the retention window
  ansible.builtin.find:
    paths: "{{ db_backup_dir }}"
    patterns: "*.sql.gz"
    age: "{{ db_backup_retention_days }}d"
  register: expired_backups

- name: Remove the expired backups
  ansible.builtin.file:
    path: "{{ item.path }}"
    state: absent
  loop: "{{ expired_backups.files }}"
  loop_control:
    label: "{{ item.path }}"
```

Two things this example does that the previous version did not: it uses the
collection module instead of shelling out to `pg_dump` with `PGPASSWORD` in the
environment, and it uses `community.general.archive` rather than
`ansible.builtin.archive`, which is no longer a builtin. Both collections are <!-- check-module-currency:ignore -->
declared in `requirements.yml`.

How long backups are retained, and what happens when the dump fails, are
`/alaa-reliability-sla`'s (`$alaa-reliability-sla`). Schema shape and migration
ordering are `/alaa-data-layer`'s (`$alaa-data-layer`).

## 4. Inventories

**Triggered by:** "create an inventory for…", "set up the hosts file".

Start from `assets/templates/inventory/`. INI form for a flat inventory, YAML
when the group hierarchy is deep enough that `[group:children]` stops being
readable.

- One inventory directory per environment. Sharing one inventory between
  production and staging and switching on a variable means a mistyped `--limit`
  reaches production.
- Group by function (`webservers`, `databases`), then compose environments with
  `[env:children]`.
- Variables go in `group_vars/` and `host_vars/`, where they can carry comments,
  not in `[group:vars]` blocks.
- A host variable that is the same on every host belongs in `group_vars`.

For a cloud fleet use a dynamic inventory plugin — `amazon.aws.aws_ec2`,
`azure.azcollection.azure_rm`, `google.cloud.gcp_compute` — rather than a static
file that drifts. Declare the collection and keep the plugin configuration in
`inventory/<env>/<name>.aws_ec2.yml`.

## 5. Projects

Start from `assets/templates/project/`. `references/scaffold.md` has the
commands and states which of those files this skill owns and which it copies.

## 6. The delivery gate

Every artifact this skill produces passes this gate before it is presented.

```bash
# 1. This skill's own check: parses, canonical booleans, no stray placeholder.
python3 scripts/check_templates.py <the files you generated>

# 2. The sibling's checks. Exit 0 is the only pass.
bash    <ansible-validator>/scripts/validate_playbook.sh <playbook>   # or validate_role.sh <role>
bash    <ansible-validator>/scripts/scan_secrets.sh      <target>
python3 <ansible-validator>/scripts/check_task_safety.py <target>
python3 <ansible-validator>/scripts/check_module_currency.py <target>
```

**The accept condition:** exit `0` from every command, with zero ansible-lint
failures. Exit `1` is findings to fix. Exit `2` means a check could not run,
which is not a pass and must be reported as blocked.

**The stopping condition:** if two consecutive fix-and-re-run cycles do not
reduce the failure count, stop and report the remaining findings rather than
continuing. An unbounded loop on a finding you cannot move is worse than a
report that names it.

**What is exempt from the gate:** an inline snippet of fewer than ten lines
shown in conversation, and a fragment quoted inside documentation. Every file
that is written to disk goes through the gate. There is no user-consent exemption:
"the user asked me to skip validation" is not a property of the artifact, and an
unvalidated file is unvalidated whoever asked for it.

## 7. Delivery format

State these four things once, when handing over. Do not repeat the block
elsewhere in the same response.

```
Generated <type>: <name>

Checks:  check_templates 0 | validate_* 0 | scan_secrets 0 | check_task_safety 0
Summary: <what it does, and the one implementation decision worth knowing>
Usage:   <the exact command, with --check --diff --limit on the first run>
Needs:   <collections with floors, target platform requirements>
```

When a check exited 2, say so in place of its number and say why. A gate that
could not run is not a gate that passed.

## 8. When the artifact reaches another skill's ground

- **A play that applies a Kubernetes manifest** uses `kubernetes.core.k8s` with
  a `definition` sourced from a file. This skill writes the task; it does not
  write the manifest body. `/alaa-k8s-helm` (`$alaa-k8s-helm`) owns the
  manifest and the chart.

  ```yaml
  - name: Apply the application manifest
    kubernetes.core.k8s:
      kubeconfig: "{{ k8s_kubeconfig }}"
      namespace: "{{ k8s_namespace }}"
      state: present
      definition: "{{ lookup('file', 'files/deployment.yml') | from_yaml }}"
  ```

- **A play that configures a container host** installs the engine, places
  `/etc/docker/daemon.json` and manages the unit. It templates a Compose file
  authored under `/alaa-docker-production`'s (`$alaa-docker-production`) rules;
  it does not invent one, and it does not generate Compose YAML inline.
- **A play that templates an HAProxy configuration** owns the `template:` task,
  its `validate:` argument and the reload handler. `/alaa-haproxy`
  (`$alaa-haproxy`) chooses the directives.
- **A play invoked from a CI job**: the boundary is the `ansible-playbook`
  command line. The arguments are `/alaa-gitlab-ci-cd`'s
  (`$alaa-gitlab-ci-cd`); everything the command reads is this skill's.

## 9. Troubleshooting the generation loop

`ansible-validator references/failure-classes.md` is the diagnosis index:
symptom, the one command that tells you which cause it is, the smallest retry,
and when to escalate. The three classes this skill produces most often:

| What the validator reported | Class | Usual cause here |
|---|---|---|
| the file does not parse | A | a bracketed placeholder, or a key indented under a bare `---` |
| `couldn't resolve module/action` | B | a collection used but not declared in `requirements.yml`, or a name that left core |
| `'x' is undefined` | C | a variable used but not declared in `meta/argument_specs.yml` |

For a module name specifically, look nothing up on the web: run
`python3 <ansible-validator>/scripts/check_module_currency.py`, which reads
ansible-core's own routing table offline. For anything else version-sensitive,
`ansible-validator references/source-map.md` carries the primary sources, the
pinned values and the command that re-derives each one.
