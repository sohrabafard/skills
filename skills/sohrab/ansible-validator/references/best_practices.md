# The Ansible ruleset

These references are the pair's single statement of the rules an Ansible artifact is
measured against. `ansible-generator` (`/ansible-generator`) generates against these rules and does not restate them;
its `references/best-practices.md` holds only the rules that apply at authoring
time and have no checker, and routes here for everything else.

The ownership rule that produced that split: **a rule lives with the skill that
ships the checker which reports its violation.** Only this skill ships
checkers, so the ruleset lives here. Every rule below names the checker that
reports it, or says plainly that nothing reports it yet.

Read this file when a finding needs a remediation citation, and cite the rule
number in the report.

---

## 1. Structure

When laying out a role or collection directory, read [project structure](best_practices/10-structure-and-naming.md) for canonical directories and ownership.

## 2. Naming

When naming tasks or variables, read [task and variable naming](best_practices/10-structure-and-naming.md) for the naming conventions.

## 3. Module selection

When choosing a module for a state change, read [module selection](best_practices/20-module-selection.md) for the rules that distinguish modules from command execution.

## 4. Idempotency

When designing or reviewing repeated task execution, read [idempotency](best_practices/30-idempotency.md) for state and check-mode contracts.

## 5. Error handling

When handling task failures or recovery, read [error handling](best_practices/40-error-handling.md) for block, rescue, always and failure semantics.

## 6. Variables

When a role value may come from more than one scope, read [variable precedence](best_practices/50-variable-precedence.md) for the ordered precedence table and variable rules.

## 7. Conditionals and loops

When adding a condition, loop or retry, read [conditionals and loops](best_practices/60-conditionals-and-loops.md) for their authoring rules.

## 8. Security rules that apply at authoring time

When a task handles paths, commands or privilege at authoring time, read [authoring security](best_practices/70-authoring-security.md) for the rules owned by this skill.

## 9. Performance

When tuning Ansible task cost, read [performance](best_practices/80-performance.md) for execution and fact-cache settings.

## 10. Check mode

When a task must be safe in check mode, read [check mode](best_practices/90-check-mode-and-documentation.md) for its validation rules.

## 11. Documentation

When documenting an Ansible artifact, read [documentation](best_practices/90-check-mode-and-documentation.md) for required documentation behavior.
