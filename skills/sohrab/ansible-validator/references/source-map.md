# Official-first source map

Use this map before validating version-sensitive Ansible content. Official and primary docs outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Ansible documentation home: https://docs.ansible.com/projects/ansible/latest/
- ansible-playbook command reference: https://docs.ansible.com/projects/ansible/latest/cli/ansible-playbook.html
- ansible-test documentation: https://docs.ansible.com/projects/ansible-core/devel/dev_guide/testing.html
- Collections guide: https://docs.ansible.com/projects/ansible/latest/collections_guide/
- Collection index and module docs: https://docs.ansible.com/ansible/latest/collections/
- Playbook keywords reference: https://docs.ansible.com/projects/ansible/latest/reference_appendices/playbooks_keywords.html
- Porting guides: https://docs.ansible.com/projects/ansible/latest/porting_guides/
- ansible-lint rules: https://ansible.readthedocs.io/projects/lint/rules/
- Molecule documentation: https://ansible.readthedocs.io/projects/molecule/
- Checkov IaC docs: https://www.checkov.io/1.Welcome/What%20is%20Checkov.html

## Freshness triggers

Fetch current official docs when validation depends on `latest` behavior, a specific Ansible or collection version, ansible-lint rule changes, molecule driver behavior, Checkov policy IDs, deprecations, CVEs, execution environments, or a module/action that is not covered by local references.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, forum posts, and community blogs only to explain observed failures or collect hypotheses. Confirm any normative module syntax, lint rule, security rule, or compatibility claim against the primary sources above.
