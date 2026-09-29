# Molecule

Read this only when a `molecule/` directory exists, or when someone asks for one
to be created. This is the pair's single statement about Molecule;
`ansible-generator` (`/ansible-generator`) routes here and
does not scaffold a `molecule/` directory, because a scenario it cannot run is a
scenario nobody has proved.

Verified 2026-07-29 against molecule 26.6.0.

---

## When running a scenario is correct

When deciding whether a scenario may run, read [Molecule execution lifecycle](./molecule/20-execution-lifecycle.md).

## Installing the driver

When installing or selecting the driver package, read [Molecule setup and configuration](./molecule/10-setup-and-configuration.md).

## The configuration model this skill ships

When creating or reviewing `molecule.yml`, read [Molecule setup and configuration](./molecule/10-setup-and-configuration.md).

## The actions, and what each asserts

When choosing Molecule stages or interpreting their results, read [Molecule execution lifecycle](./molecule/20-execution-lifecycle.md).

## Running one

When running or operating a scenario, read [Molecule execution lifecycle](./molecule/20-execution-lifecycle.md).

## Writing the verifier

When writing or reviewing a scenario verifier, read [Molecule verifier](./molecule/30-verifier.md).

## When a scenario cannot run

When a scenario stage cannot start or complete, read [Molecule execution lifecycle](./molecule/20-execution-lifecycle.md).

## Which image a scenario uses

When selecting the image tested by a scenario, read [Molecule setup and configuration](./molecule/10-setup-and-configuration.md).
