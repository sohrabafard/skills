# Security checklist: Audit Trail

## S11. A security-relevant change is visible after the fact

**Predicate.** A play that creates an account, grants a privilege or writes a
credential emits a record an operator can find later.

Whether a signal is required, what gates on it and why is
`/alaa-observability-soc`'s. The shared field names
and the metric catalogue are `/alaa-services-contract`'s. This skill owns only the assertion that the play
emits something, and the SARIF and JSON emission of its own findings:

```bash
bash scripts/validate_playbook.sh playbook.yml --format json
ansible-lint -c assets/.ansible-lint --sarif-file ansible-lint.sarif <target>
```
