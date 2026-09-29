# Variable precedence

Open this guide when resolving which variable source wins. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Variable precedence

Treat a precedence collision as a design problem, not trivia. The highest-risk
mixes:

- Manual or trigger variables overriding project defaults.
- Group variables shadowing project variables.
- `workflow:rules:variables` flowing into downstream pipelines as defaults.
- Job-level variables hiding top-level ones.
- A dotenv report from an earlier job silently replacing an assumption.

When a design mixes several sources, write a short precedence note into the
answer naming which source wins for each contested name.
