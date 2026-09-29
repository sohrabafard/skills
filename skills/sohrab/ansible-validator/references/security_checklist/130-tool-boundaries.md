# Security checklist: Tool Boundaries

## S12. The tools that are not this skill's

`ansible-lint --profile safety` is the security-leaning profile. There is **no**
`security` profile; `--profile security` is rejected by argparse, and both
skills documented it until 2026-07-29. The profiles are min, basic, moderate,
safety, shared, production.

`ansible-galaxy collection scan` does not exist and never has. The subcommands
are download, init, build, publish, install, list and verify. Use
`ansible-galaxy collection verify` to check an installed collection against its
signed manifest.

For repository-wide secret prevention rather than one-off scanning,
`git secrets --scan` and a pre-commit hook belong to the repository, not to this
skill. `/alaa-security-review` owns which controls a
repository must carry.

Secret-scan reports retain category, path and line only; never copy matched
source values into logs or artifacts. `scripts/scan_secrets.sh` redacts matches.
