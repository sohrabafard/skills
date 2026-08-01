# Artifact boundaries

| Artifact or evidence | Primary owner | Boundary |
|---|---|---|
| JSON, YAML, TOML, CI, manifests, environment templates | Native scoped search/read and parser or repository checker | A parsed graph is not the effective runtime value. |
| OpenAPI, AsyncAPI, Postman, protobuf, schemas | Owning contract skill or generator | Markdown may summarize but never replaces the exact contract. |
| Migrations and database schema | Framework/schema owner and source files | Name whether the question concerns migration intent or live schema. |
| Generated source or docs | Generator and source template | Do not patch output as the source of truth. |
| Logs, traces, metrics, browser state | Authorized runtime owner | Static tools may map evidence to source but cannot prove runtime behavior. |
| Images, diagrams, PDFs, binary assets | Native visual or artifact tool | CodeGraph and Serena do not own binary content. |
| External framework or package behavior | Official version-aware docs | Laravel Boost owns installed Laravel package documentation. |
| Cross-repository ownership and contracts | Service catalog, contract registry, GitHub, or existing Hindsight surface | Query local repositories only after the authority names them. |
| Git review | Diff first | Expand only from changed artifacts and named risks. |
