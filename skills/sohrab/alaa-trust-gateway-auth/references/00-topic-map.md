# Alaa Trust Gateway Auth Topic Map

Use this file to choose the smallest relevant section in `./full-guide.md`.

## Covered sections

- `# Purpose`
- `# When to use`
- `# Companion skill routing (mandatory)`
- `# Source priority`
- `# Execution order for agents`
- `# Canonical rename plan`
- `# Core trust model`
- `# How auth enters the system`
- `## Protected routes`
- `## Public routes`
- `## Auth-service route drift that must not be copied forward`
- `## Gateway-facing routes vs service-local routes`
- `# What the gateway verifies`
- `## Current deployment-specific truth`
- `## What the gateway does not verify`
- `## Important doc drift`
- `# Header trust rules`
- `## Headers the gateway rejects from client input`
- `## Headers the gateway injects after successful verification`
- `## X-Profile profile propagation contract`
- `## Auth-service local trusted header contract`
- `## Other header behavior`
- `# Tenant and user context`
- `## Tenant context`
- `## User identity`
- `## Services without a tenant boundary`
- `## What not to do`
- `# Auth-service v3 endpoint and client contract`
- `## Canonical gateway-facing client flow`
- `## Auth request details from the auth repo and Postman collection`
- `## Current protected auth-service route families behind the gateway`
- `## Direct local backend testing contract for auth-service`
- `## Protected-flow request families that agents should know`
- `### Session management`
- `### TOTP management and step-up`
- `### Admin authorization overrides`
- `### Profile reads and writes`
- `## Response and observability facts from the auth repo`
- `# What downstream services must do`
- `## Network and trust boundary rules`
- `## Authentication vs authorization`
- `## Laravel Gate and policy flow`
- `## Tenant-safe request handling`
- `## Async ingest and accept-then-validate flows`
- `## Header usage rules`
- `## Permission bitmap and downstream role contract`
- `## Logging and observability`
- `# Auth and token error contract`
- `## Contract rules`
- `## Recommended response envelope`
- `## Recommended log fields for auth denies`
- `## Canonical auth and token codes`
- `## Mapping from current gateway error names`
- `## Async transport note for canonical codes`
- `## Guidance for future backend harmonization`
- `# Service implementation checklist`
- `# Review checklist for agents`
- `# Laravel and Octane guidance`
- `# Related skills and required read order`
- `# Anti-patterns`

## Working rule

- Read only the sections you need from `./full-guide.md`.
- Keep this topic map small and update it when major sections are added or renamed.
