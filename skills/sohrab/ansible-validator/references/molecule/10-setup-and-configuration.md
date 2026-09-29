# Molecule setup and configuration

Read this guide only when a `molecule/` directory exists or when someone asks for one to be created. The scenario setup is verified against molecule 26.6.0 on 2026-07-29; [source-map.md](../source-map.md) owns the pinned values and re-derivation commands.

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

## Which image a scenario uses

The base image a scenario tests against is a testing decision and belongs here.
How a **project's own** image is built and expressed — the Dockerfile, the
layers, the Compose file, the fail-closed `${VAR:?}` interpolation invariant —
is `/alaa-docker-production`'s. A scenario that
needs the project's image references it; it does not author it.
