# Molecule

Read this only when a `molecule/` directory exists, or when someone asks for one
to be created. This is the pair's single statement about Molecule;
`ansible-generator` (`/ansible-generator`, `$ansible-generator`) routes here and
does not scaffold a `molecule/` directory, because a scenario it cannot run is a
scenario nobody has proved.

Verified 2026-07-29 against molecule 26.6.0.

---

## When running a scenario is correct

`molecule converge` applies the role for real, inside a container it creates,
with `privileged: true` and `/sys/fs/cgroup` mounted read-write, on whatever
machine the agent happens to be on.

**Run a scenario when both of these hold:**

1. The user asked for a test, or named the role whose scenario to run.
2. The machine is a disposable test host whose containers may be created and
   destroyed.

`scripts/test_role.sh` requires `--i-confirm-disposable-host` for exactly that
reason, and refuses without it.

**When Molecule is configured and you are not running it, say so and say why.**
"A `molecule/default` scenario exists; I did not run it because this machine is
not a confirmed disposable test host" is a complete and correct report. Silence
is not.

This replaces the rule the skill carried until 2026-07-29, which said that
molecule tests run automatically whenever a `molecule/` directory is detected,
"non-negotiable and without asking for user permission", stated in five separate
places. That rule authorises spawning privileged containers on an unknown
machine, which is the class of action `/alaa-controlled-ops`
(`$alaa-controlled-ops`) exists to gate.

## Installing the driver

```bash
python3 -m pip install "molecule>=25.0" "molecule-plugins[docker]"
```

`molecule drivers` on a stock install lists `default` only. A scenario
specifying `driver: name: docker` fails with `ERROR Failed to find driver
docker` until a driver package is installed.

**Do not install `molecule-docker`.** Its last release was 2022-09-29 and the
official installation guide tells upgraders to uninstall it to avoid conflicts
with `molecule-plugins`. The skill's own scripts installed it until 2026-07-29.

Re-derive the current driver package with
`python3 -m pip index versions molecule-plugins`;
`references/source-map.md` carries the pinned values and their commands.

## The configuration model this skill ships

`assets/molecule.yml.template` uses the `driver` / `platforms` / `provisioner` /
`verifier` keys. The official documentation calls this the **pre-ansible-native**
model: maintained for compatibility, with drivers described as displaced by
collections, and no published removal date.

It is the model that almost every existing role uses, so it is the model the
template ships. It is not broken; it is on the deprecated path. Migrate a
scenario to the ansible-native model when the role is being reworked anyway, not
as a separate change.

**Keys the template no longer carries, and why:**

| Key | Status |
|---|---|
| `lint: \| yamllint . / ansible-lint .` | There is no `lint` key in the configuration schema and no `lint` action in `molecule --help`. Molecule runs nothing from it. Lint separately with `bash scripts/validate_role.sh <role>`. |
| `callback_whitelist` | Renamed `callbacks_enabled` in ansible-core 2.11. `ansible-config validate -t all` reports the old name as unknown. |
| `ubuntu:20.04`, `debian:11` platforms | Out of standard support. A role tested only against out-of-support bases gives a false signal in both directions: a fix you rely on may be absent, and a failure you see may already be fixed upstream. |

## The actions, and what each asserts

`molecule --help` lists: check, cleanup, converge, create, dependency, destroy,
drivers, idempotence, init, list, login, matrix, prepare, reset, side-effect,
syntax, test, verify. **There is no `lint` action.**

| Action | Asserts |
|---|---|
| `dependency` | the role's and collections' requirements resolve |
| `syntax` | the converge playbook parses |
| `create` | the platform instances start |
| `prepare` | the prepare playbook succeeds, when the scenario declares one |
| `converge` | the role applies without error |
| `idempotence` | a second apply changes nothing, **on every host** |
| `side-effect` | the side-effect playbook succeeds |
| `verify` | the verify playbook's assertions hold |
| `destroy` | the instances are removed |

**On `idempotence` specifically.** Use the action. A home-grown check that runs
`converge` a second time and greps the combined output for `changed=0` passes
whenever any one host of four reported no change, which is what
`scripts/test_role.sh` did until 2026-07-29. The action compares every host.

## Running one

```bash
# The supported route: every stage tallied, summary and teardown always run
bash scripts/test_role.sh roles/webserver default --i-confirm-disposable-host

# Directly, from inside the role
cd roles/webserver
molecule test              # the full sequence
molecule converge          # apply and leave the instances up
molecule login             # a shell inside an instance
molecule verify            # re-run the verifier only
molecule destroy           # tear down
```

`scripts/test_role.sh` runs each stage with its failure tallied rather than
propagated, so the summary and `molecule destroy` always execute. Under the
pre-repair `set -e` the first failing stage killed the script, which left the
containers running and printed no summary at all.

## Writing the verifier

The default verifier is `ansible`: a playbook of assertions.

```yaml
---
# molecule/default/verify.yml
- name: Verify
  hosts: all
  gather_facts: false
  tasks:
    - name: Confirm the service is enabled and running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
      check_mode: true
      register: service_state
      failed_when: service_state.changed

    - name: Confirm the configuration file has the intended mode
      ansible.builtin.stat:
        path: /etc/nginx/nginx.conf
      register: conf

    - name: Assert the mode denies write to other
      ansible.builtin.assert:
        that:
          - conf.stat.exists
          - conf.stat.mode == '0644'
        fail_msg: "nginx.conf is {{ conf.stat.mode | default('absent') }}, expected 0644"
```

The `check_mode: true` plus `failed_when: result.changed` shape is how you
assert a state without changing it. What a verify playbook should cover — the
layering, the doubles, the flake control — is `/alaa-testing-strategy`'s
(`$alaa-testing-strategy`); this skill owns the mechanics of running it.

## When a scenario cannot run

A Molecule stage that could not start is exit 2 from `scripts/test_role.sh`, and
exit 2 is never a pass. The common causes, in the order to check them:

| Symptom | Cause | Fix |
|---|---|---|
| `Failed to find driver docker` | no driver package | `pip install "molecule-plugins[docker]"` |
| `Cannot connect to the Docker daemon` | the daemon is not running, or the user is not in the `docker` group | start it; add the user; re-login |
| the container starts and immediately exits | the image has no init and the platform declares `command: /lib/systemd/systemd` | use a systemd-capable base, or drop the systemd command and test without service management |
| `permission denied` on `/sys/fs/cgroup` | the host runs cgroup v2 and the platform does not set `cgroupns_mode: host` | set it; the shipped template does |

**Report a blocked test as blocked.** "A test that could not run is not a
passing test" is the rule, and it applies here exactly as it applies to a
security scan. The difference is what follows: a blocked security scan is a
failure per `/alaa-security-review` (`$alaa-security-review`); a blocked
idempotence test is a warning per `/alaa-reliability-sla`
(`$alaa-reliability-sla`).

## Which image a scenario uses

The base image a scenario tests against is a testing decision and belongs here.
How a **project's own** image is built and expressed — the Dockerfile, the
layers, the Compose file, the fail-closed `${VAR:?}` interpolation invariant —
is `/alaa-docker-production`'s (`$alaa-docker-production`). A scenario that
needs the project's image references it; it does not author it.
