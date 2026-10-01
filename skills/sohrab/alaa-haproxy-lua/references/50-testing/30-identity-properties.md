# Collision and ordering property tests

A smoke test that generates one identifier passes on a generator with a few hundred distinct seeds per second, because one identifier is indistinguishable from a correct one. Two properties catch what a smoke test cannot.

**Collision, across process boundaries.** Run the generator in *N* freshly started processes, not *N* times in one process, because the defect lives in per-state seeding:

```
for i in $(seq 1 40); do lua5.4 gen.lua; done | sort | uniq -d
```

Any output line is a duplicate. Run the same loop against the module under `lua-load-per-thread` with `nbthread` set to the production value, since each thread seeds separately inside the same second.

**Ordering, under uneven CPU load.** Generate a value in a CPU-heavy caller and then in a CPU-light caller inside one wall-clock second, and assert the derived timestamps are non-decreasing in the order the calls actually happened. This is the assertion that fails on a CPU-time-derived timestamp and passes on `core.now()`.

**Keep a property case set non-vacuous.** A property that accepts nothing holds for the wrong reason. Draw candidates from a pool that is mostly valid, and assert the acceptance count as its own check — the shipped example accepts 309 of 5000 candidates and asserts that at least 100 were accepted.

**Seed test randomness with a fixed constant and print it.** A test that seeds from the clock cannot be re-run on the input that failed.

For scope and related decisions, return to the [parent reference](../50-testing.md).
