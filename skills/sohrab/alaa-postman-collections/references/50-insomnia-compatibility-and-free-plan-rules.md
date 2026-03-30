# Insomnia Compatibility And Free Plan Rules

## Portability baseline

Treat the primary artifact as:

- Postman Collection Format v2.1 JSON
- companion Postman environment JSON files with safe placeholders

That is the most reliable baseline for both Postman-first work and downstream Insomnia import.

## Official Insomnia import support

Current official Insomnia docs state that Insomnia can import:

- Postman collections
- Swagger or OpenAPI specs
- cURL commands
- Insomnia files
- HAR files
- WSDL files

Current official guidance also states:

- Postman collections and environments can be imported from separate JSON files or from a Postman export directory or ZIP
- Postman collection v2.0 and v2.1 scripts should work in Insomnia after import
- if a collection uses variables from a Postman global environment, the imported collection should use an Insomnia Base Environment
- mock servers from Postman are not imported

## Practical compatibility rules

- Prefer constructs that survive import with minimal interpretation.
- Favor folder-level auth when strong Insomnia clarity matters.
- Keep scripts simple and modern.
- Do not make the core workflow depend on Postman features that Insomnia will drop or reinterpret.
- If you cannot run an Insomnia import check locally, state that exact gap in the task output.

## Postman free-plan rules that matter here

Current official Postman pricing states that the Free plan includes:

- API client and core tools
- collections and environments
- collection generation and sync
- Native Git
- Postman CLI
- unlimited Collection Runner and Performance Testing runs

Paid plans add features such as custom-branded documentation, custom domains, broader collaboration, and enterprise governance. Therefore:

- do not require paid Postman documentation branding
- do not require custom domains
- do not require team-only governance or private workspace features
- keep the workflow local and file-based by default

## Insomnia free-plan rules that matter here

Current official Insomnia pricing states that the free Essentials tier includes:

- unlimited Cloud and Local projects
- unlimited collection runs
- unlimited environments
- Inso CLI access
- plugin access

Therefore:

- do not assume a paid Insomnia plan is needed to import or run the artifact
- keep validation steps compatible with free local usage
- treat enterprise-only storage controls, RBAC, SSO, and vault integrations as out of scope

## Cloud-only and paid-only features to keep optional

- Postman monitors
- Postman cloud publishing workflows
- custom-branded documentation
- custom domains
- enterprise governance or vault integrations
- Insomnia enterprise storage controls or SSO
