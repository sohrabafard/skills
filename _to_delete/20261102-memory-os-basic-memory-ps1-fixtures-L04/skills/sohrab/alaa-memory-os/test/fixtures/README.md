# Checker Fixtures

Two vaults, committed so that every assertion the shipped checkers make has been observed to fail on an input
that violates it. A checker that has only ever been seen to pass is decoration.

`red-vault/` violates all of it at once:

| Assertion | Violated by |
|---|---|
| Wiki links resolve | `A.md` links to `[[Missing Note]]`, which does not exist. |
| Every note has an incoming link | Nothing links to `Orphan Note.md`. |
| Every note has a Relations section | `B.md` has none. |
| Recorded source paths resolve | `A.md` records `does/not/exist.md`. |
| Source-derived notes carry the required fields | `B.md` is `type: architecture` with neither `canonical_source_paths` nor `last_verified`. |
| Freshness | `A.md` and `Orphan Note.md` carry `last_verified: 2020-01-01`. |

`green-vault/` satisfies all of them, and its two notes link to each other so neither is an orphan.

The green fixture's `last_verified` is a fixed past date on purpose. The staleness self-test asserts twice
against it: once with a very large threshold, where it must be clean, and once with a zero-day threshold, where
it must report findings. The second case proves the freshness assertion actually fires and cannot rot, because
the committed date only recedes further into the past. A fixture carrying a hardcoded "fresh" date would stop
testing anything the day it aged past the default threshold.

Run everything with `test/run-tests.ps1`.
