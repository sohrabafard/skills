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
| Cross-repository ownership, contracts, and handoffs | Service catalog, contract registry, hosting surface, or approved memory surface | Evidence from another checkout is unavailable; query a named repository and reproduce proof there. |
| Git review | Diff first | Expand only from changed artifacts and named risks. |

No parser, language server, graph, or runtime tool receives authority from availability. Apply the repository's existing read, write, secret, data, environment, and production boundaries before invoking it.
