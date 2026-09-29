# Rules and value availability

Open this guide when checking when variables exist for rule evaluation. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Rules and variable limitations

- In `rules:if`, write `$VAR`, not `${VAR}`.
- Quote literal strings inside an `if` expression.
- `rules:changes` and `rules:exists` support variables; `changes:compare_to`
  supports them from GitLab 17.2. Check availability when rules are evaluated.
  Source: https://docs.gitlab.com/ci/yaml/#ruleschangescompare_to.
- Keep path-based patterns literal wherever correctness matters more than
  brevity.
