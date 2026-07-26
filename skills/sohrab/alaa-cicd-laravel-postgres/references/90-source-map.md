# Source map

Read before relying on any version, image tag, package constraint or tool behaviour that may have moved.

**No version number appears anywhere in this skill.** The framework, PHP, Composer, Node, Postgres and test-runner versions a task applies to are whatever the repository under change declares, and a version copied from a skill file goes stale silently while still looking authoritative. Read them, in this order:

1. **The repository.** `composer.json` and `composer.lock` for the framework, PHP constraint and dev tooling; the `Dockerfile` and CI configuration for the image tags and runtime actually used; `phpunit.xml` or the Pest configuration for what the suite connects to; `.env.example` for the declared `DB_*` surface; the repository's `AGENTS.md` for its own rules and its deviation register. Where two of these disagree, that disagreement is the split-brain finding of `10-gate-register.md`, not a question to resolve by picking one.
2. **The running production instance**, for the Postgres major and minor the parity rule requires: `SELECT version()`. No document substitutes for it.
3. **Official documentation**, selecting the version the repository declares rather than the newest: `https://laravel.com/docs` (upgrade, testing, deployment), `https://www.php.net/manual/`, `https://www.php.net/supported-versions.php`, `https://getcomposer.org/doc/`, `https://www.postgresql.org/docs/`, `https://docs.phpunit.de/`, `https://pestphp.com/docs`, and `https://phpstan.org/` plus the Larastan repository.
4. **Runner and provider behaviour** — service containers, caching, artifacts, masked variables, retry syntax, CI lint — belongs to `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) `references/SOURCES.md`. This skill holds no provider documentation link and no provider YAML, so that one place stays correct.
5. **Community posts** for troubleshooting only, and never as the basis for a gate. Verify any command semantics they suggest against the official source above and against one observed run.

## Fetch when the task mentions

`latest`, `current`, `upgrade`, `security`, `CVE`, a new PHP, Laravel, Postgres, Composer, PHPUnit, Pest or PHPStan release, an image tag change, a runner change, a cache miss, a flaky test, a health-check change, or any change to what gates a release.

## Pinning, stated as a predicate

An image reference passes when its tag names both a major and a minor and resolves to one immutable digest. A tag naming only a major floats its minor, so a rebuild can change behaviour with no review; `latest` and an absent tag are the same defect with less warning. The production Postgres major and minor come from source 2 above, never from an example. `scripts/check-ci-determinism.sh` checks this class.
