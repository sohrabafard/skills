# CI secrets and supply chain

Read when a credential, registry token, OIDC role, vulnerability scan or SBOM enters a job. Every rule about what a secret is, how it is stored, compared, rotated and logged belongs to `/alaa-security-review` (`$alaa-security-review`), in its `references/50-credentials-and-cryptography.md` and `references/60-deep-review-and-hardening.md`. Three exposures exist only in CI, and this file owns those.

**Short-lived over long-lived.** A job obtains registry, cloud and cluster credentials as a short-lived token issued to the pipeline's own identity — OIDC where the provider supports it. A long-lived token stored as a CI variable is permitted only for a target that cannot issue one, and then it is scoped to the single project that uses it, marked protected, and rotated on a schedule recorded in the repository. "Cannot issue one" means the provider's documentation says so, cited in the change; it is not a judgment the agent makes about convenience.

**Fork and merge-request exposure.** A job that can run on a fork or on an untrusted merge request receives no protected variable and no deploy credential. The replacement is a two-pipeline split: the untrusted pipeline builds, lints, tests and migrates against its own throwaway database with no credential at all, and a second pipeline gated on a protected branch holds the credentials and performs the release. The mechanism that enforces the split — protected branches and variables, rule conditions, runner selection — belongs to `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`).

**Log and artifact redaction.** `set -x` is forbidden in any job step that holds a secret, because tracing prints the expanded value into a log that outlives the job. A step may log a secret-bearing variable's **name** and whether it was present, never its value or anything derived from it. A credential is never placed inside a URL a command may echo on failure: it is passed by environment variable or by a file the runner creates and the artifact paths exclude. Masking at the runner is a backstop, not the control — it fails on a value that is split, encoded, or printed a character at a time.

**Scans and SBOM.** The dependency-advisory gate, its committed severity policy, the rule that a missing policy fails the job, and the SBOM's class and retention are all in `10-gate-register.md`. Neither is restated here.

Any step that would create, rotate or read production credentials, or change production infrastructure, stops and follows `/alaa-controlled-ops` (`$alaa-controlled-ops`) instead of proceeding.
