# Package And Service Adoption

## The doctrine this file implements

The Ala fleet has one rule for shared components: change the shared component, release it, then bump the pinned reference downstream. `alaa-services-contract/references/15-deployment-and-runtime-contract.md` states it for `service-ci-kit` and `/alaa-services-contract` ($alaa-services-contract) owns it. This file applies that doctrine to a Composer package instead of a CI kit; it does not restate or amend it.

**One deliberate exception.** There, CI performs the release; here a developer performs it by hand, because the Ala Satis instance distributing this package is a local Docker stack with no CI runner attached, so no pipeline can rebuild its index. The approval gate in `SKILL.md` substitutes for CI's review. The exception ends the moment a pipeline can push the tag and rebuild the index: move this sequence into CI then and delete the manual steps, rather than keeping both.

## Configuration

Defaults, not fixed paths. Read each from the environment when set; when a step needs one that is unset, report the missing value and stop rather than guessing a path.

- `SATIS_LOCAL_DIR` — local Ala Satis checkout. Resolve it in this order: a path named in the current request, then `$SATIS_LOCAL_DIR`, then a directory named `satis-local` beside the package checkout. Confirm a candidate by the presence of both `docker-compose.yml` and `satis.json` at its root, because those two files are what the build step reads. When none of the three resolves to such a directory, report every path you tried and stop, because a Satis build run from the wrong tree publishes a different package index than the one adopters resolve against. Its `README.md` is authoritative for that stack.
- `SATIS_PACKAGES_URL` — Satis index an adopter resolves against. Default `http://satis.alaa.local/packages.json`.

## Adoption source

Normal service adoption uses a tagged `alaa/controlled-ops` release from the Ala Satis Composer repository. Reject a lock file recording a path repository unless the current task explicitly asked for local package development: a sibling checkout is a developer-only override, and a committed dependency model requiring `../alaa-controlled-ops` is a defect to report and revert.

## Release and publish sequence

Use this when the user asks to release, publish, push, or make a new version available to services.

1. Confirm repository truth from the current checkout: `git status --short --branch`, `git log --oneline --decorate -5`, `git tag --sort=-creatordate`, `git remote -v`, and, when network access is available, `git ls-remote --tags origin <tag>`.
2. Choose the next semantic version from the actual latest tag and the change type. Do not recreate a tag that already exists locally or remotely; if `HEAD` is already tagged and the remote has that tag, the Git publish step is already done.
3. Run every package gate in `references/40-validation-and-release-gates.md`. Do not tag while a gate is failing or unrun.
4. Tag only after the working tree is committed and every gate is clean: `git tag -a vX.Y.Z -m "vX.Y.Z"`.
5. Stop at the approval gate in `SKILL.md`. It covers exactly four actions: `git push origin <branch>`; `git push origin vX.Y.Z`; the Satis build in `$SATIS_LOCAL_DIR`; updating a consuming service to the new tag.
6. After approval, push the verified branch, then the verified tag.
7. After an approved release branch/tag push, refresh the local Ala Satis repository by running `docker compose --profile build run --rm satis-build` from the resolved `$SATIS_LOCAL_DIR`. The Git push alone does not rebuild the index, so the package is not available to adopters until that build runs; stopping at the push and reporting the package as published is the defect this step exists to prevent.
8. `satis-build` is a one-shot builder: it must exit `0` and write `satis-output`, and is not expected to stay `Up`. On any other exit code, stop, report the code with the last twenty lines of output, and tell the user the package is not published. Never continue to adoption on a failed build.
9. Verify availability before adoption: confirm the tag on the primary remote; when the Satis web stack is running, fetch `$SATIS_PACKAGES_URL` and confirm the tag is listed; confirm `composer show alaa/controlled-ops --available -vvv` resolves it before update, and the adopter's lock after.

Read-only remote checks such as `git ls-remote` may run before the approval gate. Writes, tag pushes, `docker compose --profile build run --rm satis-build` in the resolved `$SATIS_LOCAL_DIR`, and consuming-service release rollouts require the approval gate above.

## Adopter adoption checklist

In the consuming service:

- require the approved package constraint
- run `composer update alaa/controlled-ops --with-dependencies`
- confirm `composer show alaa/controlled-ops --locked` reports the intended tag and a Satis dist URL; on a different tag or a non-Satis dist source, stop, report which of the two it was, and make no code changes against the wrong version
- bind only the package contracts the service actually adopts
- keep public API shape and docs under the service repo

## Public surface rule

Do not introduce new service route families, Postman folders, queue jobs, or lifecycle actions just because the package has a helper. Add them only when the service implementation, tests, docs, and public artifact sync are part of the task.
