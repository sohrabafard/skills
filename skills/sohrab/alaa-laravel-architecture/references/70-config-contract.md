# The config contract for this skill's surfaces

Behaviour that must vary by environment or scale is a named key with a stated default, a stated range, and a place it is validated. "Config-driven" without a key name is not configurability: two agents implement two different keys, and neither default is written down anywhere an operator can find during an incident.

Keys live in `config/architecture.php` in every Ala service, under the `architecture.*` namespace, so that an operator moving between services looks in one place. Uniformity here beats a locally nicer name.

| Key | What it decides | Safe default | Valid range | Validated where |
|---|---|---|---|---|
| `cache.default` | which store the repository decorator wraps | the store the repository already configures — this key is not introduced by this skill, only consumed by the binding in `references/20-composition-and-boot.md` | a key present in `config('cache.stores')` | the config test below asserts the named store exists; never read in a provider `register()` |
| `architecture.cache.<domain>.enabled` | whether the decorator is bound at all for that domain | `false` | boolean | the provider binds the decorator only when true; the config test asserts the value is a boolean and that a true value has a corresponding bound interface |
| `architecture.outbox.enabled` | whether domain events are written to the durable outbox | `true` for any service that emits an event another component consumes; `false` only for a service that emits none | boolean | the config test; when true, the outbox appears in the readiness dependency set |
| `architecture.pagination.max_page_size` | the ceiling a list route accepts | the fleet value in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` — this skill states no number | `1` to that fleet value inclusive; a larger configured value is a config error, not a local decision | the FormRequest that validates the page size reads the key rather than a literal; the config test asserts the value does not exceed the fleet value |
| `architecture.dependencies.<name>.required` | whether an unreachable dependency fails the request or degrades it, and whether readiness reports it | `true` for a dependency on an authorization or entitlement path; `false` for a dependency that only enriches a response | boolean | the config test; the value must agree with the route classification in `references/40-degraded-mode.md` |

The default for the last key is not a judgment call: it follows the gate-versus-contributor discriminator owned by `/alaa-security-review` (`$alaa-security-review`) — when the dependency cannot answer, does proceeding without it let through something that must not get through?

## Where "validated at the boundary" actually happens

One test, named for its job, asserts every row of the table above:

- every key exists;
- every value has the declared type;
- every value is inside the declared range, including the page-size ceiling against the fleet value;
- `architecture.cache.<domain>.enabled` is not true for a domain with no bound repository interface.

Two rules make the test meaningful rather than decorative:

- **No key in this table is read during a provider's `register()`.** A provider that reads one has taken a config value another provider may still change, and `references/20-composition-and-boot.md` states why that placement fails at boot.
- **`env()` is read only inside `config/*.php`.** Application code reads `config()` or receives typed config through its constructor. The wording of that rule is `/alaa-php-clean-code`'s (`$alaa-php-clean-code`).

## Values this skill does not own

Every timeout, retry count, backoff, pool bound, acquire wait, shed threshold, TTL, and claim lifetime. Doctrine is `/alaa-reliability-sla`'s (`$alaa-reliability-sla`) and `/alaa-data-layer`'s (`$alaa-data-layer`) for cache TTL; every number is in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. A key holding one of those values belongs in the config file of the skill that owns it, referenced from there, not copied into this table.

## What must never become configurable

- The layer map and its call graph. A flag that lets a Controller reach a Repository is a flag that will be set.
- Whether a response exposes an internal identifier.
- The envelope's shape, its keys, or its code casing.
- Whether an event is emitted before or after commit.

These are invariants, and a switch on an invariant is how the invariant ends.

## Adding a key

A change that introduces a key adds its row to this table in the same change, with all four columns filled. A key with an unstated default is a key whose behaviour in production nobody can predict from the repository.
