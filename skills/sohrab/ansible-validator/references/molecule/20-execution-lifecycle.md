# Molecule execution lifecycle

Read this guide only when a `molecule/` directory exists or when someone asks for one to be created. The scenario setup is verified against molecule 26.6.0 on 2026-07-29; [source-map.md](../source-map.md) owns the pinned values and re-derivation commands.

**Do not run a scenario unless both conditions hold:** the user asked for a test or named the role, and the machine is a disposable test host whose containers may be created and destroyed. `scripts/test_role.sh` requires `--i-confirm-disposable-host` and refuses without it.

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
machine, which is the class of action `/alaa-controlled-ops` exists to gate.

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

A nonzero dependency or prepare result is a failure, never evidence that the
scenario omitted that stage. Let Molecule handle an absent optional playbook;
do not infer absence from an execution error. A failed destroy also fails the
gate and reports that instances may remain. Missing executables remain blocked.

`scripts/test_role.sh` runs each stage with its failure tallied rather than
propagated, so the summary and `molecule destroy` always execute. Under the
pre-repair `set -e` the first failing stage killed the script, which left the
containers running and printed no summary at all.

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
failure per `/alaa-security-review`; a blocked
idempotence test is a warning per `/alaa-reliability-sla`.
