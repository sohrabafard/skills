# Ansible ruleset: Idempotency

## 4. Idempotency

**4.1 A task states the end state, not the operation.** `state: present`, not
`command: apt-get install`.
*Reported by:* `ansible-lint` rule `command-instead-of-module`.

**4.2 A `command` or `shell` task states `changed_when`,** or `creates`, or
`removes`. Without one it reports `changed` on every run, which makes a real
change invisible in the output and makes the idempotence test meaningless.
*Reported by:* `ansible-lint` rule `no-changed-when`.

**4.3 A read-only command sets `changed_when: false`** and states its own
`failed_when` when a non-zero return code is expected.

**4.4 A second apply changes nothing.** This is the definition, and it is
testable: `molecule idempotence` compares every host.
*Reported by:* `scripts/test_role.sh`, idempotence stage. See
`references/molecule.md` for when running a scenario is correct.
