# Security checklist: Secret Redaction

## S2. `no_log` covers every task that can print a secret

**Predicate.** `no_log: true` is set on any task whose module arguments or
registered result can contain a value sourced from a vault file, from
`lookup('env', ...)`, or from a variable whose name matches
`(pass|secret|token|key|credential)`.

**Evaluate.**

```bash
ansible-lint -c assets/.ansible-lint <target>   # rule no-log-password
bash scripts/scan_secrets.sh <target>
```

**What `no_log` does not cover.** `--diff` prints the content of a templated
file. A template that renders a secret into a configuration file leaks it into
the diff of a check-mode run even when the task carries `no_log: true`, because
the diff is produced by the file module and not by the argument logger. When a
template renders a secret, either set `diff: false` on that task or accept that
`--check --diff` output is itself sensitive and handle it accordingly.
