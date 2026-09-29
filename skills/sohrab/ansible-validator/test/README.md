# The test corpus

This directory is the pair's fixture corpus. `ansible-generator`
(`/ansible-generator`) keeps one scaffold fixture of its
own and routes here for everything else.

Every fixture is referenced by a `--self-test` in `scripts/`. Run the whole set
with:

```bash
bash scripts/self_test.sh
```

From a fresh checkout with `scripts/requirements.txt` installed, that exits 0
and reports 63 assertions. Exit 2 means the toolchain is missing, not that the
skill is broken.

When running the existing corpus, read [corpus usage](corpus-usage.md). When adding or refreshing fixtures, read [fixture and vendored-role maintenance](fixture-maintenance.md).

## Layout

## The playbook pair

## Running one checker against the corpus

## Using the corpus in CI

## Why each fixture exists

## The vendored role: `roles/geerlingguy.mysql/`

## Adding a fixture
