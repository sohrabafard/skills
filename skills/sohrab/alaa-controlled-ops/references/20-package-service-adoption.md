# Package And Service Adoption

## Adoption source

Normal service adoption should use a tagged `alaa/controlled-ops` package release from the Ala Satis Composer repository.

Use a sibling checkout only while developing the package itself. Do not commit a service dependency model that requires `../alaa-controlled-ops` unless the user explicitly asks for that temporary state.

## Package release checklist

Before asking a service to consume a new package tag:

- run package metadata validation
- run the package verifier
- run package PHPUnit tests when dependencies are installed
- run Composer audit when the advisory endpoint is reachable
- tag the verified package commit with the intended semantic version
- after the approved branch/tag push, refresh Satis from `D:\satis-local` with `docker compose --profile build run --rm satis-build`

## Package release and publish workflow

Use this sequence when the user asks to release, publish, push, or make a new `alaa/controlled-ops` package version available to services:

1. Confirm repository truth from the current checkout:
   - `git status --short --branch`
   - `git log --oneline --decorate -5`
   - `git tag --sort=-creatordate`
   - `git remote -v`
   - when network access is available, `git ls-remote --tags origin <tag>`
2. Choose the next semantic version from the actual latest tag and the change type. Do not recreate a tag that already exists locally or remotely; if `HEAD` is already tagged and the remote has that tag, the Git publish step is already done.
3. Run the package release gates before tagging:
   - `composer validate --strict`
   - `php scripts/controlled_ops_verify.php`
   - `vendor/bin/phpunit` or the platform-specific PHPUnit wrapper after dependencies are installed
   - `composer audit --locked` when the advisory endpoint is reachable
   - `git diff --check`
4. Commit only intentional package changes. Preserve unrelated user edits.
5. Create an annotated semver tag only after the commit and validation gates are clean:
   - `git tag -a vX.Y.Z -m "vX.Y.Z"`
6. Approval gate: before any publishing action, stop and ask the user for explicit approval unless the current request already says approval is not required or publishing is authorized. Publishing actions include:
   - `git push origin <branch>`
   - `git push origin vX.Y.Z`
   - running the Satis build command in `D:\satis-local`
   - updating a consuming service to the newly published tag as part of the release rollout
7. Publish after approval:
   - push the verified branch
   - push the verified tag
   - switch to `D:\satis-local`
   - run `docker compose --profile build run --rm satis-build`
   - treat `satis-build` as a one-shot builder: it should exit with code `0` after writing `satis-output`; it is not expected to stay `Up`
8. Verify package availability before service adoption:
   - confirm the tag exists on the primary remote
   - when the local Satis web stack is running, check `http://satis.alaa.local/packages.json`
   - confirm Composer can resolve the tag from Satis, preferably with `composer show alaa/controlled-ops --available -vvv` before update and the consuming service lock after update

Read-only remote checks such as `git ls-remote` may run before the approval gate. Writes, tag pushes, `docker compose --profile build run --rm satis-build` in `D:\satis-local`, and consuming-service release rollouts require the approval gate above.

## Service adoption checklist

In the consuming service:

- require the approved package constraint
- run `composer update alaa/controlled-ops --with-dependencies`
- confirm `composer show alaa/controlled-ops --locked` reports the intended tag and a Satis dist URL
- reject lock files that record a path repository unless the task explicitly asked for local package development
- bind only the package contracts the service actually adopts
- keep public API shape and docs under the service repo

## Public surface rule

Do not introduce new service route families, Postman folders, queue jobs, or lifecycle actions just because the package has a helper. Add them only when the service implementation, tests, docs, and public artifact sync are part of the task.
