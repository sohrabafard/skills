# Vendored third-party fixtures

One directory belongs here: `geerlingguy.mysql/`, the third-party integration
fixture. `../README.md` states its provenance, its licence obligation and the
refresh rule. This file exists so that an empty directory is not mistaken for a
missing decision.

The fixture was **kept**, not retired. The reasoning is in `../README.md`: a
first-party fixture proves the checkers run, and a real, well-built,
multi-platform role with real Molecule configuration proves they run on
something nobody wrote for them. What the fixture lacked was not a purpose; it
was a pin, a refresh rule and a licence artifact. All three are now stated.

To install or refresh it:

```bash
ansible-galaxy role install geerlingguy.mysql,<tag> -p test/roles --force
printf '%s\n' '<tag>' > test/roles/geerlingguy.mysql/.fixture-version
bash scripts/validate_role.sh test/roles/geerlingguy.mysql
```

`<tag>` is a released upstream tag, never a branch name. Record it in
`.fixture-version` in the same change, because a vendored copy with no pin
cannot be diffed against upstream and cannot be refreshed reproducibly.

Carry the upstream `LICENSE` file with the tree. `geerlingguy.mysql` is MIT, and
redistributing it without its licence is a licensing defect rather than a
testing question.

`assets/.ansible-lint` excludes `test/roles/` from directory scans, because this
skill does not report findings about code it does not own. An explicit target
bypasses `exclude_paths`, so the command above still lints it deliberately.

Do not add a second vendored role without a specific defect it pins down, a
pin, a licence file and a row in the table in `../README.md`.
