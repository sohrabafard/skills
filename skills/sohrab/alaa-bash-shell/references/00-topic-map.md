# Topic Map

Use this file first. Then load only the smallest reference file that answers the current task.

## Pick the smallest file

- **New CLI or refactor**
  - Read `script-contract.md`
  - Then read `generation-workflow.md`
  - Check the closest template in `../assets/templates/`

- **Choosing Bash vs POSIX `sh`**
  - Read `portability-and-platforms.md`

- **Alpine, BusyBox `ash`, Debian `dash`, GNU vs BSD, or macOS**
  - Read `portability-and-platforms.md`

- **Validation, linting, smoke tests, or debugging**
  - Read `validation-and-debugging.md`
  - Use `../scripts/validate-shell.sh` if local execution is possible

- **Performance or command selection**
  - Read `tool-selection-and-performance.md`

- **Tests, CI, or pre-commit**
  - Read `testing-and-ci.md`

- **Reusable code patterns**
  - Read `patterns-and-examples.md`

- **Version-sensitive flags or current official guidance**
  - Read `official-reference-map.md`
  - Re-check the linked docs when the exact version or flag behavior matters

## Minimum references by task

### Generate one Bash script
- `script-contract.md`
- `generation-workflow.md`

### Generate one portable `/bin/sh` script
- `script-contract.md`
- `generation-workflow.md`
- `portability-and-platforms.md`

### Debug an existing script
- `validation-and-debugging.md`
- `portability-and-platforms.md` if portability is involved

### Refactor a group of scripts
- `script-contract.md`
- `generation-workflow.md`
- `patterns-and-examples.md`
- `testing-and-ci.md`

### Review a shell-heavy repository
- `validation-and-debugging.md`
- `tool-selection-and-performance.md`
- `portability-and-platforms.md`

## Working rule

Keep `SKILL.md` lean. Put detailed guidance here or in the other reference files, and read only what the task truly needs.
