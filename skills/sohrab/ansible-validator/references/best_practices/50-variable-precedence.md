# Ansible ruleset: Variable Precedence

## 6. Variables

**6.1 `defaults/main.yml` holds what a caller may override.
`vars/main.yml` holds what a caller must not.** The difference is precedence,
not convention: `vars/` outranks almost everything a caller can set.

**6.2 Variable precedence, lowest to highest.** This is the pair's single
precedence table. `ansible-generator` routes here rather than restating it,
because it shipped a nine-item list that placed `set_fact` *below* task, block
and role vars, which is the reverse of the truth and is the single question most
likely to produce a wrong-value bug.

1. role defaults (`defaults/main.yml`)
2. inventory file or script group vars
3. inventory `group_vars/all`
4. playbook `group_vars/all`
5. inventory `group_vars/*`
6. playbook `group_vars/*`
7. inventory file or script host vars
8. inventory `host_vars/*`
9. playbook `host_vars/*`
10. host facts and cached `set_fact`
11. play vars
12. play `vars_prompt`
13. play `vars_files`
14. role vars (`vars/main.yml`)
15. block vars
16. task vars
17. `include_vars`
18. `set_fact` and registered vars
19. role and `include_role` params
20. include params
21. extra vars (`-e`), which always win

Source: the Ansible variable-precedence section of the playbooks guide, linked
from `references/source-map.md`.
*Reported by:* nothing. Precedence bugs are read, not linted.

**6.3 An optional variable is read through `default()`.** `{{ app_port |
default(8080) }}`.

**6.4 A mandatory variable is read through `mandatory`, or declared `required:
true` in `meta/argument_specs.yml`.** The filter is `mandatory`. There is no
`required` filter; `{{ x | required('...') }}` fails at runtime with
`No filter named 'required'`. Both skills taught the non-existent one until
2026-07-29.

**6.5 Fact caching values are the same everywhere they appear.** The pair's
single value for `fact_caching_timeout` is **86400** seconds, stated in [the performance rules](./80-performance.md#9-performance); `ansible-generator`'s `ansible.cfg` template carries a comment naming
this file as the owner instead of a second number. It shipped 3600 against this
file's 86400 until 2026-07-29.



Version-sensitive claims and source dates: [source map](../source-map.md).
