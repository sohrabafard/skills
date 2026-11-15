# Final gates and batch repair

`/alaa-testing-strategy` `references/100-test-execution.md` owns how checks are collected, repaired and retested: *Prepare the check list* and *Collect, repair, retest*. This file adds only what an upgrade changes.

## One run

Run the gates after every dependency move and every planned code change is in place. Do not run the suite before the upgrade or between packages; the stepwise fallback in `20-apply-and-recover.md` is the one exception.

A gate is one of the checks below. A repository script that proves runtime, release or delivery behaviour is not a gate of this skill; run it only when the owner asks.

Run each gate once and keep its full output:

- The repository's test command.
- The static analysis and the formatter that the repository declares in `require-dev`. When it declares none, report `gate not available: none declared`.
- `composer validate --strict`.
- `composer audit --locked --format=json`, and `npm audit --json` when a `package.json` exists.
- The frontend build, when the frontend ships. It ships when its build output is tracked or served, a Blade or Inertia entrypoint references it, or a container build stage runs it. Otherwise `npm audit` closes the npm side.
- The boot proof below.

## One failure list

Collect every failure from every gate into one list before the first fix. Group the list by cause, not by test. Name each cause from the plan table or from the package's changelog:

- a guide item, cited by its row;
- an API that the new version removed or changed;
- a default that changed;
- a deprecation that became an error;
- a defect that the upgrade did not cause.

## Repair

1. Fix each cause once, in the code that the failing tests share.
2. Rerun only the checks that failed.
3. Run every gate once more.

Repeat while the list gets shorter. When one cause survives two repairs, stop work on it and report it with its evidence.

**A test is never weakened.** Do not delete a test, skip it, mark it incomplete or loosen its assertion to make it pass. Change an expected value only when an official guide or changelog entry documents that behaviour change. Cite the entry in the commit body and in the run record. In every other case, change the code.

- A failure is repaired whatever its age, because this skill takes no baseline. When its cause lies outside the upgrade and the repair needs a product decision, list it and ask.
- Add a test only where a repair changes the service's own behaviour and `/alaa-testing-strategy` says a test is owed.

## Boot proof

- **Every run.** After `php artisan optimize:clear`, `php artisan about` exits zero.
- **When the framework or the application server moved a major** and the repository has a ready local runtime command: start it, send one request to a route that needs the database, and confirm the expected status.

Run nothing more. Report the level reached. A runtime that will not start is reported with its error, not relabelled.

## Advisories

Every package is now at its latest stable release, so a remaining finding has no fix in range. Record the advisory identifier (`CVE-...` or `GHSA-...`), the package and the installed version.

| Severity | Action |
|---|---|
| critical, high, or none assigned | Stop condition in `SKILL.md`: report it and ask. No acceptance exists |
| medium, low | List it in the report. A named human decides acceptance |

- No agent accepts a finding, at any severity. An acceptance record names the human, the compensating control and an expiry date; a record without all three does not accept anything.
- `npm audit fix --force` is forbidden: it applies major moves outside the plan.
- When the advisory endpoint is unreachable, retry once, then report `supply-chain audit not run: advisory endpoint unreachable`. Never report the gate clean when it did not run.
