# Fork divergence: `sohrabafard` @ `9c8125f1` versus upstream `9b8df5d4`

Read this when a service still carries a `repositories` VCS override for
`vladimir-yuldashev/laravel-queue-rabbitmq`, or when someone proposes adding one.

This file replaces the fork tree. The fork's `README.md` was byte-identical to the upstream copy
(`md5 c50f327c483a6969f0e8a2e28bc7b49d`); its `RabbitMQQueue.php` differed by exactly the one inserted
block below. Those two files plus the fork's `composer.json`, `.github/workflows/tests.yml` and
`CHANGELOG-14x.md` were retired to `_to_delete/2026-07-26-batch2/alaa-laravel-job-rabbitmq/`. The pin at
`references/forks/FORK_COMMIT.txt` stays; the pin is the durable artifact.
`references/forks/sohrabafard/9c8125f.../src/Consumer.php` was **kept** — it is this skill's only offline
snapshot of the consume loop.

**1. The four added methods — the entire code divergence.** Inserted into `src/Queue/RabbitMQQueue.php`
after `push()`; nothing else changed:

```php
public function pendingSize($queue = null): int { return $this->size($queue); }
public function delayedSize($queue = null): int { return 0; }
public function reservedSize($queue = null): int { return 0; }
public function creationTimeOfOldestPendingJob($queue = null): ?int { return null; }
```

(One-line bodies here; the shipped file spaced them across four docblocked methods.)

**2. `Consumer::stop()` signature.** Fork and installed upstream `v15.0.0` are identical:
`public function stop($status = 0, $options = null, $reason = null)`. Upstream `9b8df5d4` predates the
third parameter, and Laravel 13's `Worker::stop()` passes a stop reason, so the two-parameter form is a
signature mismatch under Laravel 13.

**3. Constraint string.** Fork `composer.json`: `"illuminate/queue": "^10.0|^11.0|^12.0|^13.0"`. Installed
upstream `v15.0.0` carries the identical string — the fork's constraint work landed upstream. Both still
declare `"branch-alias": {"dev-master": "13.0-dev"}`, a stale alias inside the package and not a statement
about the release you get.

**4. CI matrix delta.** The fork's `tests.yml` added `'8.5'` to `php` and `'^13.0'` to `laravel`, excluding
`php 8.1 x laravel ^11.0|^12.0|^13.0` and `php 8.2 x laravel ^13.0`. Composer does not install `.github/`,
so this path never exists in a consuming repository.

**Verbatim from the retired `CHANGELOG-14x.md`, `[unreleased]`:** Add Laravel 13 compatibility to the queue
constraints. Add PHP 8.5 and Laravel 13 to the CI test matrix. Implement Laravel 13 queue monitor metric
methods on `RabbitMQQueue`. Update `Consumer::stop()` to accept the Laravel 13 optional stop reason
parameter.

## What this skill's guidance depends on

Only item 1: every `queue:monitor` claim in this skill rests on those four bodies, and they are present in
installed upstream `v15.0.0` — verification and date in `references/driver-facts.md`. Items 2, 3 and 4 are
settled history explaining why the fork existed and why it no longer needs to. Nothing in this skill
depends on the fork tree.

**Do not reintroduce the fork.** Where the override still exists, delete the `repositories` entry, run
`composer update vladimir-yuldashev/laravel-queue-rabbitmq --with-all-dependencies`, and confirm
`composer.lock` names `vyuldashev/laravel-queue-rabbitmq.git` as the source before changing any queue
behaviour.
