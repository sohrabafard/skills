# The acceptance gate, and what done means for a layer change

```sh
sh scripts/architecture-gate.sh --app-dir app          # 0 clean, 1 findings, 2 usage or config error
sh scripts/architecture-gate.sh --self-test            # fixture suite; run after editing the script
sh scripts/architecture-gate.sh --help
```

It needs `sh`, `find`, `grep -nE`, `awk`, `sort`, and `mktemp`. No PHP, no Composer, no repository configuration — it runs on a fresh checkout before `composer install`.

## What each finding means

The gate detects the mechanical form of five boundary defects. It does not hold the rules; each rule lives in one file, and the gate only finds the places that break it.

| Check | The defect it finds | The rule it enforces |
|---|---|---|
| `L1-controller-persistence` | a Controller composing a query, naming a repository interface, or calling `DB::` | `SKILL.md`, forbidden edges |
| `L2-public-id-leak` | an internal key or a raw model reaching a response body | `references/10-layer-map.md`, Identifiers |
| `L3-repository-bypass` | a write or query composed in a Service, Job, Listener, Command, Policy, Action, or Pipeline | `references/10-layer-map.md`; the repository policy's wording is `/alaa-php-clean-code`'s (`$alaa-php-clean-code`) |
| `L4-provider-io` | a service provider reading cache, Redis, the database, the network, or the filesystem | `references/20-composition-and-boot.md` |
| `L5-provider-resolve-in-register` | a service provider resolving a service in `register()`, outside a binding closure | `references/20-composition-and-boot.md` |

## What the gate cannot see

A green gate is a floor, not a proof. It reads text, so it cannot see:

- **an event emitted before commit** — ordering is a runtime property; only a test that rolls back and asserts no event was published proves it;
- **a stale cache** — it finds the bypassing write that causes staleness, not the staleness;
- **an envelope that conforms in shape but carries the wrong code** — names are `/alaa-services-contract`'s (`$alaa-services-contract`) and its own `jq` observable checks them against saved examples;
- **a raw array crossing a boundary** — a typed signature is checkable, but only by a static analyser at the repository's configured level, which `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) owns;
- **indirection** — a Controller calling a helper that queries, or a provider whose I/O sits inside a class it constructs.

Treating exit 0 as "the architecture is correct" is the one way this gate makes things worse.

## Waivers

A finding is fixed, or waived in `.architecture-gate-allow` as three fields:

```
app/Services/SettingsService.php@@@L3-repository-bypass@@@Pre-repository slice, tracked in docs/design/0007-settings.md
```

A waiver with an empty reason exits 2, because an exception an agent can grant itself without naming anything is not an exception. The reason names an artifact — a design record, an issue, an `AGENTS.md` note — that someone other than the waiving agent can open. Every applied waiver is printed on every run, so a waiver stays visible instead of becoming permanent quietly.

## Wiring it

Run it as its own pipeline stage, before the test stage, so a boundary defect fails in seconds rather than after the suite. Stage definition, caching, and release gating belong to `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`).

## Done, for a change that touches a layer boundary

All four hold. Report the gate's exit code you observed, not the one you expect.

**1. The gate exits 0**, or every finding carries a waiver with an artifact.

**2. The boundary is proven from outside itself.** What makes a test a test rather than a replay of the happy path, which layer a behaviour belongs at, and whether a double is honest are `/alaa-testing-strategy`'s (`$alaa-testing-strategy`) — read it for the test's design. The architectural obligations it does not know about are these three, and each names a specific broken implementation it must fail against:

- a route added or changed carries a test asserting the response's envelope keys and asserting that no internal identifier appears anywhere in the body — it must fail against an implementation that serializes the model;
- a repository interface added or changed carries a test written **against the interface**, not the concrete class, so the store implementation and a cache decorator are both substitutable — a test naming the concrete class passes while the seam does not exist;
- an event whose ordering matters carries a test that rolls the transaction back and asserts nothing was published — it must fail against an implementation that emits before commit.

**3. The surfaces are observable.** Every surface in `references/60-telemetry-surfaces.md` that this change added or moved emits its signal.

**4. The documentation moved with the surface.** A change to a route, an envelope, a public identifier, an emitted event, a repository interface, or a key in `references/70-config-contract.md` updates the repository's API artifact and the layer note in its `AGENTS.md`, in the same change. This is unconditional: a contract surface whose documentation lags is a surface the next agent re-derives from the code and copies wrong. The docs workflow, Postman sync, and diagram alignment are `/alaa-docs-farsi`'s (`$alaa-docs-farsi`); docblock and artifact rules are `alaa-php-clean-code references/documentation-and-artifacts.md`.
