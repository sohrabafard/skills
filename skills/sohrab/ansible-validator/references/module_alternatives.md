# Module names: what each one maps to today

This is the pair's single name-to-FQCN mapping. `ansible-generator`
(`/ansible-generator`, `$ansible-generator`) routes here when it needs a current
FQCN rather than maintaining a second table inside
`references/module-patterns.md`; that skill owns *how to call* a module, this
one owns *what its name is now*.

Read this on an `fqcn[action-core]` finding, on a `deprecated-module` finding, or
when `scripts/check_module_currency.py` reports a name.

<!-- check-module-currency:ignore-file -->
This file is exempt from `check_module_currency.py`: naming the stale FQCNs is
its whole purpose, and they are the left column of the table below.

Verified 2026-07-29 against ansible-core 2.19.11's own routing table,
`ansible/config/ansible_builtin_runtime.yml`, plus the presence of each module
file. Re-derive the whole table offline with:

```bash
python3 scripts/check_module_currency.py <path>          # report stale names
python3 scripts/check_fqcn.py <path>                     # report short names
```

## Two different problems, told apart

The pre-repair version of this file had one column headed "Deprecated Module"
that mixed two unrelated things, and the skill's own scripts inherited the
confusion. They are separate:

**Problem 1: a short name.** `apt`, `copy`, `file`, `service` are not deprecated
modules. They are unqualified references to live modules. Ansible resolves them
through core's routing table, which changes between releases, so the same play
can run on one machine and fail on another. The fix is a rename.
*Reported by:* `ansible-lint` rule `fqcn[action-core]`, `scripts/check_fqcn.sh`.

**Problem 2: a module that left ansible-core.** The name still works, because
core keeps a compatibility redirect, but the implementation now lives in a
collection. The task runs where that collection happens to be installed and
fails where it is not, and nothing in a normal lint run says so. The fix is a
rename *and* a `requirements.yml` entry.
*Reported by:* `scripts/check_module_currency.py`.

Problem 2 is the invisible one. Three of the 34 `ansible.builtin.*` names taught
by `ansible-generator/references/module-patterns.md` were in that state on
2026-07-29 — an 8.8% defect rate over an exhaustive sample of that stratum — and
nothing in either skill reported it.

## Problem 2: names that left ansible-core

| Name still written | What it resolves to now | What to write | Collection to declare |
|---|---|---|---|
| `ansible.builtin.yum` | `ansible.builtin.dnf`, through an **action** redirect | `ansible.builtin.dnf` | none |
| `ansible.builtin.archive` | `community.general.archive` | `community.general.archive` | `community.general` |
| `ansible.builtin.authorized_key` | `ansible.posix.authorized_key` | `ansible.posix.authorized_key` | `ansible.posix` |
| `ansible.builtin.synchronize` | `ansible.posix.synchronize` | `ansible.posix.synchronize` | `ansible.posix` |
| `ansible.builtin.acl` | `ansible.posix.acl` | `ansible.posix.acl` | `ansible.posix` |
| `ansible.builtin.at` | `ansible.posix.at` | `ansible.posix.at` | `ansible.posix` |
| `ansible.builtin.firewalld` | `ansible.posix.firewalld` | `ansible.posix.firewalld` | `ansible.posix` |
| `ansible.builtin.mount` | `ansible.posix.mount` | `ansible.posix.mount` | `ansible.posix` |
| `ansible.builtin.seboolean` | `ansible.posix.seboolean` | `ansible.posix.seboolean` | `ansible.posix` |
| `ansible.builtin.selinux` | `ansible.posix.selinux` | `ansible.posix.selinux` | `ansible.posix` |
| `ansible.builtin.sysctl` | `ansible.posix.sysctl` | `ansible.posix.sysctl` | `ansible.posix` |
| `sysvinit` | `community.general.sysvinit` | `community.general.sysvinit` | `community.general` |

**On `yum` specifically.** The `yum.py` module file is gone from ansible-core.
`ansible.builtin.yum:` still executes, because the routing table carries
`yum: redirect: ansible.builtin.dnf` under `action:`. So a task written for
RHEL 7 now runs **dnf**, and RHEL 7 has no dnf. Advice of the form "use
`ansible.builtin.yum` for RHEL 7" is not merely stale; it names a module that
cannot do what the sentence says. Write `ansible.builtin.dnf` and state the
RHEL 8-or-newer scope.

**On `sysvinit` specifically.** `ansible.builtin.service` is a wrapper that
picks a service manager; it is not a replacement for the `sysvinit` module,
which exposes sysvinit-specific parameters. When a task needs those parameters,
use `community.general.sysvinit`.

**On `systemd`.** `ansible.builtin.systemd` exists and is not deprecated, but
the canonical name is `ansible.builtin.systemd_service` and `systemd` is its
alias. Write the canonical name.

## Problem 1: short names to FQCN

### Package management

| Short | FQCN | Note |
|---|---|---|
| `apt` | `ansible.builtin.apt` | |
| `dnf` | `ansible.builtin.dnf` | the RHEL-family package module |
| `yum` | `ansible.builtin.dnf` | see the section above |
| `package` | `ansible.builtin.package` | picks the manager; use when the play is OS-agnostic |
| `pip` | `ansible.builtin.pip` | |
| `apk` | `community.general.apk` | `community.general` |
| `homebrew` | `community.general.homebrew` | `community.general` |
| `zypper` | `community.general.zypper` | `community.general` |
| `easy_install` | `ansible.builtin.pip` | `easy_install` is gone from Python |

### Files

| Short | FQCN |
|---|---|
| `copy` | `ansible.builtin.copy` |
| `file` | `ansible.builtin.file` |
| `template` | `ansible.builtin.template` |
| `lineinfile` | `ansible.builtin.lineinfile` |
| `blockinfile` | `ansible.builtin.blockinfile` |
| `replace` | `ansible.builtin.replace` |
| `fetch` | `ansible.builtin.fetch` |
| `stat` | `ansible.builtin.stat` |
| `find` | `ansible.builtin.find` |
| `unarchive` | `ansible.builtin.unarchive` |
| `archive` | `community.general.archive` |
| `synchronize` | `ansible.posix.synchronize` |
| `acl` | `ansible.posix.acl` |

### Services

| Short | FQCN | Note |
|---|---|---|
| `service` | `ansible.builtin.service` | picks the manager |
| `systemd` | `ansible.builtin.systemd_service` | `systemd` is the alias |
| `sysvinit` | `community.general.sysvinit` | not a `service` synonym |

### Users, groups and keys

| Short | FQCN |
|---|---|
| `user` | `ansible.builtin.user` |
| `group` | `ansible.builtin.group` |
| `authorized_key` | `ansible.posix.authorized_key` |
| `known_hosts` | `ansible.builtin.known_hosts` |

### Network and firewall

| Short | FQCN |
|---|---|
| `get_url` | `ansible.builtin.get_url` |
| `uri` | `ansible.builtin.uri` |
| `iptables` | `ansible.builtin.iptables` |
| `firewalld` | `ansible.posix.firewalld` |
| `ufw` | `community.general.ufw` |

### Commands

| Short | FQCN | Note |
|---|---|---|
| `command` | `ansible.builtin.command` | first choice of the three |
| `shell` | `ansible.builtin.shell` | only for a pipe, redirect, glob or shell variable |
| `raw` | `ansible.builtin.raw` | only before Python exists on the target |
| `script` | `ansible.builtin.script` | |

### Cloud and containers

| Short | FQCN | Collection |
|---|---|---|
| `ec2` | `amazon.aws.ec2_instance` | `amazon.aws` |
| `ec2_ami` | `amazon.aws.ec2_ami` | `amazon.aws` |
| `ec2_vpc` | `amazon.aws.ec2_vpc_net` | `amazon.aws` |
| `azure_rm_*` | `azure.azcollection.*` | `azure.azcollection` |
| `gcp_*` | `google.cloud.*` | `google.cloud` |
| `docker_container` | `community.docker.docker_container` | `community.docker` |
| `docker_image` | `community.docker.docker_image` | `community.docker` |
| `k8s` | `kubernetes.core.k8s` | `kubernetes.core` |

A play that applies a Kubernetes manifest uses `kubernetes.core.k8s`; the
manifest itself is `/alaa-k8s-helm`'s (`$alaa-k8s-helm`). A play that manages a
container host uses `community.docker.*`; the Dockerfile and the Compose file
are `/alaa-docker-production`'s (`$alaa-docker-production`).

### Databases

| Short | FQCN | Collection |
|---|---|---|
| `mysql_db` | `community.mysql.mysql_db` | `community.mysql` |
| `mysql_user` | `community.mysql.mysql_user` | `community.mysql` |
| `postgresql_db` | `community.postgresql.postgresql_db` | `community.postgresql` |
| `postgresql_user` | `community.postgresql.postgresql_user` | `community.postgresql` |
| `mongodb_*` | `community.mongodb.*` | `community.mongodb` |

Schema shape, index choice and migration ordering are not this skill's:
`/alaa-data-layer` (`$alaa-data-layer`) owns them. This skill owns whether the
task that applies them is idempotent and check-mode-safe.

## Declaring the collections

Every collection named above is declared in `requirements.yml` with a floor that
states the version whose behaviour you relied on:

```yaml
---
collections:
  - name: ansible.posix
    version: ">=2.0.0"
  - name: community.general
    version: ">=11.0.0"
  - name: community.docker
    version: ">=4.0.0"
  - name: community.postgresql
    version: ">=4.0.0"
```

```bash
ansible-galaxy collection install -r requirements.yml
```

Re-derive the current major of any collection with
`ansible-galaxy collection list <namespace.name>` after installing it, or from
the collection index in `references/source-map.md`. A floor set to a major that
is several releases behind, such as `community.general >=8.0.0`, asserts nothing
and should be raised to the version you tested.

## Version boundaries worth knowing

| Boundary | What changed |
|---|---|
| 2.10 | Collections split out of core. FQCN becomes meaningful. |
| 2.12 | Many modules removed from core; redirects remain. |
| 2.17 onward | Progressive removal of the redirects themselves. |
| 2.19 | Current security-only branch; end of life November 2026. |
| 2.20 | Control node requires Python 3.12 or newer. Targets require 3.9 or newer. |
| 2.21 | Current fully supported branch (2.21.2 on 2026-07-29). |

`references/source-map.md` carries the command that re-derives each of these.
