# Runtime and network blockers

Observed 2026-09-26.

## Correctness reviewer dispatch

Two attempts to create the canonical `alaa-reviewer` returned exactly
`collab spawn failed: agent thread limit reached`. Between attempts the writer
finished, but the second attempt still failed. No role substitution or third
correctness-review dispatch was attempted after the retry budget.
Recovery: explicitly authorize a fresh dispatch after slots are available, using
the frozen candidate and current evidence. Instruction review is a distinct gate
and does not replace correctness review.

After instruction review completed, a first dispatch of `alaa-verifier`
succeeded. Its separate source-gate evidence is authoritative for that role;
earlier lead checks remain supplemental and are labelled as lead-operated.

## Read-only freshness check

Both commands ran on the frozen candidate, at BelowNormal priority, from the
repository root; exact command/time/process exits are in `verification/`.

1. Default `check_versions.py`: process exit 2, Helm EOL page request timed out.
2. One materially different retry, `check_versions.py --timeout 30`: process
   exit 2, the same page returned a connection timeout (WinError 10060).

Classification: ENVIRONMENT-BLOCKED, not drift and not PASS. The browser research
surface had supplied official EOL evidence, but that is not a successful execution
of this checker. No proxy, trust-store, dependency or runtime configuration change
was made. Recovery: restore approved Python HTTPS reachability to
https://helm.sh/blog/helm-v3-end-of-life/ and authorize a new read-only check.

## Bash startup probe

`bash --version` failed before executing with `CreateFileMapping ... Win32 error 5`.
The shell function resolves to the installed Git Bash executable; no installation
was attempted. The runtime-ops owner classifies this as MSYS sandbox IPC startup
failure, not source failure. No retry or source repair was attempted for this
optional runtime probe. Bash example execution and chart-structure shell checks
remain unrun. Recovery: an exact, scoped outside-sandbox retry under the runtime
owner's policy when that proof is required; no protection/configuration changes.
