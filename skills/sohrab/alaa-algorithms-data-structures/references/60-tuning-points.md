# Tuning Points

Load when a numeric constant is about to be written into code or into configuration.

`SKILL.md` owns the decision rules: when a value is configurable, when it stays a named constant, and the three
things every configurable value ships. This file says which values in this estate are which, what the validation
looks like, and how to handle a value another skill already owns.

## Which values this skill decides

Only the values that follow from a complexity decision. Everything else belongs to the skill that owns it, and
restating one here creates a second copy that drifts.

| Value | Owned here | Owned elsewhere |
|---|---|---|
| Chunk size for a streamed or batched operation | Yes | — |
| Maximum batch size for a bulk call | Yes | — |
| Prefetch key-set chunk size | Yes | — |
| Maximum depth for a recursive traversal | Yes | — |
| Maximum entries and eviction policy for an in-process map that outlives a request | Yes | — |
| Maximum page size and its default | The rule that one must exist | The value: `/alaa-services-contract` (`$alaa-services-contract`) |
| Connection pool maxima | No | `/alaa-services-contract` (`$alaa-services-contract`) |
| Timeouts, retry counts, backoff, breaker thresholds | No | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Cardinality ceilings, histogram boundaries, sampling rates | No | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Cache TTLs and invalidation | No | `/alaa-data-layer` (`$alaa-data-layer`) |
| KDF cost parameters | No | `/alaa-security-review` (`$alaa-security-review`) |

When a value is owned elsewhere, the code reads it from wherever that skill puts it and the budget cites the owning
skill. A budget that repeats the number is a copy, and the copy is the one that is wrong after the owner changes it.

## The three things a configurable value ships

**A default that is safe at the worst case, not optimal at the typical one.** The default is what runs in every
deployment nobody tuned, which is most of them, and on the worst input the system permits. A default chosen for the
typical tenant is a default that fails on the largest one, silently, in whichever service was deployed last.

**A validated range, checked at startup, that fails the boot on a bad value.** Naming the setting, the value
received, and the accepted range in the failure message. Three reasons the check is at startup and not at first use:
a misconfigured service that refuses to start is caught by the deployment, a misconfigured service that starts and
fails later is caught by a user; the first request is usually not the one that exercises the value; and a value
validated at use has to be validated at every use.

Validate all four properties, because three of them pass a naive type check:

1. **Type and parse** — a numeric setting supplied as an empty string is not zero, it is unset.
2. **Range** — a minimum and a maximum, both stated. A chunk size of zero is an infinite loop; a chunk size of ten
   million is the materialisation the chunking existed to prevent.
3. **Relationship to other settings** — a chunk size larger than a batch maximum, a maximum below its own default,
   a concurrency higher than the pool permits. These pass individually and are wrong together.
4. **Units** — one unit per setting, stated in the setting's name where the unit is ambiguous. A value that is
   seconds in one service and milliseconds in another is a thousand-fold error waiting for a copy-paste.

**One sentence stating what changes when it moves, and in which direction.** "Larger chunks mean fewer round trips
and more memory per chunk." Without it, the value is untunable in the only situation that matters — an incident,
at speed, by someone who did not write it — and it will be moved by guess or not at all.

## When making it configurable is the defect

Three cases, each of which produces a knob that is never touched and always wrong:

- **The value is derivable.** A worker's prefetch that should follow its concurrency, a chunk size that should follow
  a page size. Derive it in code and expose only the input. Two settings that must agree will disagree.
- **The value is a correctness constraint.** A batch maximum that also bounds a transaction's size, a depth limit
  that prevents a stack overflow, a maximum that a downstream contract enforces anyway. Making it configurable
  invites a deployment to configure a broken system, and the boundary that enforces correctness belongs in code.
- **Nobody can state what a different value would do.** This is the diagnostic case: an inability to write the third
  shipped item means the decision has not been made, and configuration is being used to avoid making it. Decide the
  value, write it as a named constant with its reasoning, and make it configurable later if a deployment ever
  actually needs a different one.

**A service with forty settings and no defaults is not configurable, it is undecided.** Every setting is a decision
deferred to whoever deploys, and they have less information than the author had.

## Anti-patterns

- a knob with no default, so the service depends on a value someone must know to supply;
- a default chosen from the developer's machine or the smallest tenant;
- a range validated at first use rather than at startup;
- two settings that must agree, both configurable, with no cross-check;
- a magic number inside a loop, with no name, no reasoning, and no test that would notice it changing;
- a setting whose name states no unit, carrying a unit that differs between services;
- restating a value another skill owns so the local copy drifts from the source;
- a value made configurable to avoid deciding it.
