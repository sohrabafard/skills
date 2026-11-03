# Project facts — fill from the current repository

- Repository / commit / working-tree state:
- Service owner and bounded context:
- Runtime and framework versions from lockfiles:
- Entry points and test commands from actual project scripts:
- Public API and event contracts:
- Tenant boundary and identity/authorization source:
- Data authority; PostgreSQL/Redis/ClickHouse responsibilities:
- RabbitMQ/Kafka/outbox/job delivery semantics:
- Deployment: Compose / OpenShift / namespace / rootless / offline constraints:
- Actual NFRs, workload and test dataset:
- Required review and release checks:
- Forbidden or separately authorized operations:
- Existing task tracker and ADR locations:
- Existing skill and MCP routing policy:

Historical Alaa leads to verify: Vue 3/Quasar/Vite; PHP/Laravel with Octane;
Go services; PostgreSQL/Redis/ClickHouse; RabbitMQ/Kafka;
trusted gateway identity injection; tenant_id; OpenFGA; outbox;
rootless/single-namespace deployment in some environments.
These are not proof of this repository's current architecture or versions.

Use existing alaa-workflow / alaa-code-intelligence-routing / language and testing
skills when present and applicable. Read their actual contents; names alone do not
define behavior. Do not replace them with this package's generic defaults.
