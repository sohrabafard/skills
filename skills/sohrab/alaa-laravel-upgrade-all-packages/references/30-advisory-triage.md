# Advisory Triage

An agent produces the record; a named human decides. Threat classes, hardening and the fail-closed doctrine are `/alaa-security-review` (`$alaa-security-review`). This file owns only the mapping from an audit finding to an action inside a sweep.

`composer audit --locked --format=json` returns advisories per package with an identifier, a CVE where one exists, a severity, the affected range and a link; `npm audit --json` reports its own scale. Record the identifier (`CVE-...` or `GHSA-...`), never the title, because titles are not stable across databases.

## Severity to action

| Severity | Action | Acceptance |
|---|---|---|
| critical | Stop the sweep; fix on the hotfix path, alone | none exists |
| high | Stop the sweep; fix on the hotfix path, alone | none exists |
| medium | Fix here when a non-major fix exists; otherwise the fix becomes a major change per `20-breaking-change-detection.md` | record required |
| low | Fix here when a non-major fix exists; otherwise recorded | record required |
| absent, unscored or disputed | Treat as high until a human assigns one | none until assigned |

Unscored treated as high is the fail-closed choice, on the discriminator `/alaa-security-review` (`$alaa-security-review`) owns: when this control cannot answer, does proceeding without it let something through that must not get through? For an unknown-severity advisory in a dependency of a security-sensitive multi-tenant service it does, so it is a gate.

## The hotfix path is not this sweep

1. Restore point (`10-rollback-and-blast-radius.md`) on a branch named for the advisory, not the sweep.
2. Move only the vulnerable package: `composer update <vendor/package> --with-dependencies`. Not `--with-all-dependencies` -- the change under review has to be one subtree.
3. Run the `SKILL.md` gates against that change alone, at the proof level `20-breaking-change-detection.md` sets for it.
4. Ship it, then resume the sweep from a fresh restore point.

The revert-unit argument in `20-breaking-change-detection.md` applies with the added cost that the fix waits behind the batch's gate.

If the only fix for that package is a major bump, the hotfix *is* that major bump per `20-breaking-change-detection.md`, never deferred into an acceptance record, because critical and high have no acceptance path.

## Reachability, determined rather than assumed

- `composer depends <vendor/package>` names what pulls it in.
- The `require-dev` and container-build-stage test in `10-rollback-and-blast-radius.md` decides request-path reach. A package that reaches only CI is a build-integrity finding, recorded rather than dismissed.
- The advisory names a symbol, class or endpoint; `grep -rn '<symbol>' app/ config/ routes/` decides whether this service calls it. "We do not think we use it" is not a reachability finding.

Unreachable lowers urgency and never removes the record: the next refactor can make it reachable, and nothing re-runs this analysis on its own.

## The acceptance record

Medium and low only. Every field is required; a record missing any field is not an acceptance and the finding still blocks.

- Advisory identifier, package name, installed version.
- Severity as reported, and which database reported it.
- The reachability finding and the command that produced it.
- Why no upstream fix exists: the upstream issue or merge-request URL. "No fix available" with no link is not a reason.
- The compensating control, and where it is implemented.
- **The named human approver.** A person, not a role, not a team, never the agent.
- **An expiry date.** After it the finding blocks again and the record must be renewed by the same authority. A record with no expiry is a permanent silent exemption, which is the failure this section exists to prevent.

The record lives in the state file `SKILL.md` names, so the next scheduled run reads it and re-checks every expiry before touching a dependency.

## npm differences

`npm audit fix --force` is forbidden: it applies major bumps silently, defeating the classification in `20-breaking-change-detection.md` and producing an unreviewable diff. Run `npm audit fix` without `--force`; whatever remains becomes an explicit major change or an acceptance record on the Composer side's terms.

## When the advisory database is unreachable

Apply the false branch `/alaa-controlled-ops` (`$alaa-controlled-ops`) `references/40-validation-and-release-gates.md` already defines for `composer audit --locked`: retry once, then report `supply-chain audit not run: advisory endpoint unreachable` as a named gap and ask the user whether to proceed. That file wins on conflict. Never report the supply-chain gate clean when it did not run.
