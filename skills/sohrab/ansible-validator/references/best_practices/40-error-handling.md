# Ansible ruleset: Error Handling

## 5. Error handling

**5.1 A group of tasks that must be undone on failure goes in a
`block`/`rescue`/`always`.** `rescue` restores the previous state; `always`
removes the lock, the temporary file and the maintenance flag.

**5.2 `ignore_errors: true` is not a failure strategy.** Replace it with
`failed_when` naming the condition that is genuinely acceptable, so that the
other failures still fail.
*Reported by:* `ansible-lint` rule `ignore-errors`.

**5.3 A play that must not half-apply across a fleet sets `any_errors_fatal:
true`,** or `max_fail_percentage` with a number.
*Reported by:* nothing. What the number should be is not this skill's decision:
`/alaa-reliability-sla` owns why a timeout, retry,
backoff or degradation mechanism exists and what shape it takes. This skill
reports that a play has no `any_errors_fatal` and stops there.

**5.4 A health check that is allowed to take time states `until`, `retries` and
`delay`.** A health check with no `until` either passes on the first poll or
fails the play, which is a race, not a check.
*Reported by:* nothing. The values are `/alaa-reliability-sla`'s.

**5.5 A task whose failure must stop the run states so.** A play that continues
past a failed decrypt, a failed certificate fetch or a failed schema migration
has decided to proceed without something it needed. Whether proceeding is
allowed is `/alaa-security-review`'s when the missing
thing is a security control, and `/alaa-reliability-sla`'s when it is an availability dependency. The
discriminating question: *when this dependency cannot answer, does proceeding
without it let something through that must not get through?*

For custom modules and action plugins, report failures explicitly: set `failed: true`
in a returned result, call the module's `fail_json`, or raise an appropriate error.
A nonzero `rc` without `failed` relies on deprecated inference; test the returned
failure state as well as the return code. The core 2.21 porting guide documents this
transition; runtime deprecation warnings begin in 2.22, not removal in 2.21.
Source and observation date: `references/source-map.md`.



Source dates for the core behavior: [source map](../source-map.md).
