# Sources

Use this file when GNU Make, POSIX make, validation tooling, portability, or recipe security behavior must be current.

## Freshness triggers

Re-check primary sources when the user asks for latest/current behavior, GNU Make version features, POSIX portability, recipe shell semantics, validator behavior, security-sensitive recipes, CI behavior, or portability across Linux, macOS, BSD, and minimal containers.

## First-check official and primary sources

- GNU Make manual: https://www.gnu.org/software/make/manual/
- GNU Make news: https://git.savannah.gnu.org/cgit/make.git/tree/NEWS
- GNU Make Savannah project: https://savannah.gnu.org/projects/make/
- POSIX make utility: https://pubs.opengroup.org/onlinepubs/9799919799/utilities/make.html
- POSIX shell and utilities: https://pubs.opengroup.org/onlinepubs/9799919799/

## Validation and formatting sources

- checkmake: https://github.com/mrtazz/checkmake
- mbake: https://github.com/StackExchange/mbake
- unmake: https://github.com/mcandre/unmake
- shellcheck: https://www.shellcheck.net/
- shfmt: https://github.com/mvdan/sh/tree/master/cmd/shfmt

## Related primary sources

- GNU Bash manual: https://www.gnu.org/software/bash/manual/
- Docker build docs for image-oriented targets: https://docs.docker.com/build/
- GitLab CI YAML docs for CI-wrapped Make targets: https://docs.gitlab.com/ci/yaml/

## Conflict resolution

1. Repository Makefile behavior and explicit user constraints.
2. GNU Make manual or POSIX make spec, depending on the target dialect.
3. Primary validator/tool docs.
4. This skill's local references and scripts.

## Community troubleshooting sources

Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting after manuals, validator output, and local reproduction are checked. Do not use them as normative portability, security, or style guidance.
