# Ansible ruleset: Performance

## 9. Performance

Each value below is a starting point with the reason it exists. What the number
should be for a given fleet and SLA is `/alaa-reliability-sla`'s.

**9.1 SSH pipelining on.** It removes one round trip per task, which dominates
run time on a high-latency link.

```ini
[ssh_connection]
pipelining = True
```

**9.2 Fact caching on, with one timeout value across the whole project.**

```ini
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = {{ project_fact_cache_dir }}
fact_caching_timeout = 86400
```

86400 is the pair's single value for `fact_caching_timeout`; rule 6.5 states
that. Do not put the cache in `/tmp`: it is world-writable on a shared host and
does not exist on a Windows control node.

**9.3 `gather_facts: false` unless the play reads an `ansible_*` fact.** When it
reads fewer than three, set `gather_subset` naming exactly those. Fact gathering
is one full module execution per host before any task runs.

**9.4 A long task runs async and is polled.**

```yaml
- name: Run the database migration
  ansible.builtin.command: /opt/app/migrate.sh
  async: 3600
  poll: 0
  register: migration
  changed_when: true

- name: Wait for the migration to finish
  ansible.builtin.async_status:
    jid: "{{ migration.ansible_job_id }}"
  register: migration_status
  until: migration_status.finished
  retries: 360
  delay: 10
```

**9.5 `forks` and `serial` are stated, not defaulted.** `forks = 5` is the stock
default; shipping it as if it were a tuning decision tells the reader nothing.
`serial` bounds how much of the fleet a bad change reaches at once, which is a
blast-radius decision. Both numbers are `/alaa-reliability-sla`'s.

**9.6 A loop or a fan-out that grows with the inventory has a stated bound.**
A play whose cost grows with tenants, hosts or history is a complexity question:
`/alaa-algorithms-data-structures` owns
complexity budgets and structure choice.



Version-sensitive claims and source dates: [source map](../source-map.md).
