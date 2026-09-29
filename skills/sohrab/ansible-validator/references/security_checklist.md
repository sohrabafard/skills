# Security predicates, and the command that evaluates each one

This file is the pair's single statement of the Ansible security predicates and
of Ansible Vault mechanics. `ansible-generator` (`/ansible-generator`) keeps only the authoring-time shape rules — where `no_log`
goes, what `mode` to write — and cites this file by line for everything else.

A checklist item with no command that evaluates it is a preference. Every
predicate below names its command.

**Whose decision a finding is.** This skill reports. It does not decide whether
a finding blocks a change. `/alaa-security-review`
owns fail-closed doctrine for security decisions and `/alaa-reliability-sla` owns fail-open and degradation for availability. The
discriminating question, which you may quote: *when this dependency cannot
answer, does proceeding without it let something through that must not get
through?* A secret-scan finding answers yes, so it is fail-closed by default.

**A scan that could not run is a blocked audit, not a clean one.** Every script
here exits 2 when it could not run, and 2 is never a pass.

---

## The three commands that make up an audit

When preparing or interpreting a security audit, read [audit commands](security_checklist/10-audit-commands.md) for the exact three-command contract.

## S1. No credential is a literal in a tracked file

When reviewing tracked credential storage, read [credential storage](security_checklist/20-credential-storage.md) for approved storage and scanning rules.

## S2. `no_log` covers every task that can print a secret

When a task can print secret material, read [secret redaction](security_checklist/30-secret-redaction.md) for `no_log` coverage.

## S3. Vault mechanics

When encrypting or reading vaulted values, read [Vault mechanics](security_checklist/40-vault-mechanics.md) for the supported Vault lifecycle.

## S4. Privilege escalation is scoped

When granting privilege escalation, read [privilege escalation](security_checklist/50-privilege-escalation.md) for scope boundaries.

## S5. Every written path has an explicit mode, and none is world-writable

When writing a file or directory, read [file permissions](security_checklist/60-file-permissions.md) for explicit safe modes.

## S6. No unvalidated value reaches a shell

When passing external values to a shell, read [shell inputs](security_checklist/70-shell-inputs.md) for validation and transport rules.

## S7. Transport is encrypted and verified

When connecting to a managed host, read [transport verification](security_checklist/80-transport-verification.md) for encrypted, verified transport.

## S8. Host keys are checked

When SSH host identity is involved, read [host-key verification](security_checklist/90-host-key-verification.md) for host-key validation.

## S9. A service binds to an address, not to everything

When binding a service, read [service binding](security_checklist/100-service-binding.md) for listener scope.

## S10. SELinux and AppArmor stay enforcing

When MAC policy affects an artifact, read [mandatory access control](security_checklist/110-mandatory-access-control.md) for enforcing SELinux and AppArmor.

## S11. A security-relevant change is visible after the fact

When reviewing an auditable security change, read [audit trail](security_checklist/120-audit-trail.md) for visible after-the-fact evidence.

## S12. The tools that are not this skill's

When choosing a tool outside this skill, read [tool boundaries](security_checklist/130-tool-boundaries.md) for ownership and routing.
