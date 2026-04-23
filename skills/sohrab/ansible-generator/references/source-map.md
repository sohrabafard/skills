# Official-first source map

Use this map before generating version-sensitive Ansible content. Official and primary docs outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Ansible documentation home: https://docs.ansible.com/projects/ansible/latest/
- Playbooks guide: https://docs.ansible.com/projects/ansible/latest/playbook_guide/
- Inventory guide: https://docs.ansible.com/projects/ansible/latest/inventory_guide/
- Collections guide: https://docs.ansible.com/projects/ansible/latest/collections_guide/
- Collection index and module docs: https://docs.ansible.com/ansible/latest/collections/
- Playbook keywords reference: https://docs.ansible.com/projects/ansible/latest/reference_appendices/playbooks_keywords.html
- Ansible Vault guide: https://docs.ansible.com/projects/ansible/latest/vault_guide/
- Porting guides: https://docs.ansible.com/projects/ansible/latest/porting_guides/
- ansible-lint rules: https://ansible.readthedocs.io/projects/lint/rules/
- Molecule documentation: https://ansible.readthedocs.io/projects/molecule/

## Freshness triggers

Fetch current official docs when the task mentions `latest`, `current`, a specific Ansible or collection version, a new/deprecated module parameter, execution environments, ansible-lint rule behavior, security/vault handling, or an unknown collection.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, forum posts, and community blogs only to explain observed failures or collect hypotheses. Confirm any normative module syntax, security guidance, or compatibility claim against the primary sources above.
