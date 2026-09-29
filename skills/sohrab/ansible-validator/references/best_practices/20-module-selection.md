# Ansible ruleset: Module Selection

## 3. Module selection

**3.1 Every action is a fully qualified collection name.** `ansible.builtin.apt`,
not `apt`. A short name resolves through core's routing table, which changes
between releases, so the same play can run on one machine and fail on another.
*Reported by:* `ansible-lint` rule `fqcn[action-core]` and
`scripts/check_fqcn.sh`, which agree that this is an error rather than advice.

**3.2 The FQCN names the collection that provides the module today, not the one
that used to.** Three names the pair taught until 2026-07-29 —
`ansible.builtin.yum`, `ansible.builtin.archive`, `ansible.builtin.authorized_key` <!-- check-module-currency:ignore -->
— left core and now work only through a compatibility redirect, so they run
where the collection happens to be installed and fail where it is not.
*Reported by:* `python3 scripts/check_module_currency.py`.
*Mapping:* `references/module_alternatives.md`.

**3.3 A collection an artifact uses is declared in `requirements.yml` with a
version floor.** A floor so low that every release satisfies it asserts nothing;
state the version whose behaviour you relied on.
*Reported by:* `scripts/extract_ansible_info_wrapper.sh` lists
`unpinned_collections`.

**3.4 Use the module for the operation. Do not shell out to the tool the module
wraps.** `community.postgresql.postgresql_db`, not
`ansible.builtin.command: psql -c "CREATE DATABASE ..."`. Shelling out to dodge
a collection dependency destroys idempotency, check-mode support and error
semantics in one move; a missing collection is an environment defect to fix in
the environment, not a design choice.
*Reported by:* `ansible-lint` rule `command-instead-of-module`.

**3.5 `ansible.builtin.command` before `ansible.builtin.shell`.** Use `shell`
only when the command needs a pipe, a redirect, a glob or a shell variable, and
say which in a comment.
*Reported by:* `ansible-lint` rule `command-instead-of-shell`.



Version-sensitive claims and source dates: [source map](../source-map.md).
