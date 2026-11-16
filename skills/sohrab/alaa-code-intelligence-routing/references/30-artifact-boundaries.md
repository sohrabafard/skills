# Artifact boundaries

`references/10-routing-contract.md` owns source, semantics, Laravel runtime and proof.

| Artifact or evidence | Primary owner | Boundary |
|---|---|---|
| JSON, YAML, TOML, CI, manifests, environment templates | Native scoped read plus a parser or repository checker | Parsed syntax is not the effective runtime value |
| OpenAPI, AsyncAPI, Postman, protobuf, schemas | The owning contract skill or generator | Markdown can summarize the exact contract but never replaces it |
| Migrations and source schema | The framework or schema owner | Name whether the question concerns migration intent or live schema |
| Generated source or docs | The generator and source template; otherwise repository-declared hand-maintained source, never an invented owner | Never patch generated output as the source of truth |
| Logs, traces, metrics, browser state | The authorized runtime owner, or another authorized surface that proves the same fact | Static tools can map evidence to source but prove no runtime behavior |
| Images, diagrams, PDFs, archives, binary assets | A native visual or artifact tool | CodeGraph and Serena do not own binary content |
| External framework or package behavior | Official version-aware documentation | Boost owns installed Laravel package documentation |
| Cross-repository ownership, contracts and handoffs | A catalog, contract registry, hosting surface or approved memory surface | Local static evidence proves nothing about another repository |
