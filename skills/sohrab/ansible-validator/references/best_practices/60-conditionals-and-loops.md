# Ansible ruleset: Conditionals And Loops

## 7. Conditionals and loops

**7.1 `loop`, not `with_*`.** `with_items` and its siblings are discouraged in
favour of `loop`; they are **not** deprecated, and ansible-core 2.19.11 emits no
deprecation warning for them. Both skills quoted a `[DEPRECATION WARNING]` text
that ansible-core does not produce.

**7.2 A `when` holding several conditions is a YAML list,** one condition per
line, so that a failing condition is identifiable from the output.

**7.3 A `when` does not wrap its expression in `{{ }}`.**
*Reported by:* `ansible-lint` rule `no-jinja-when`.

**7.4 An OS-conditional task branches on `ansible_os_family` or
`ansible_distribution`,** and the play states what happens on a family it does
not name. A play that silently skips every task on an unlisted OS reports
success having done nothing.



Version-sensitive claims and source dates: [source map](../source-map.md).
