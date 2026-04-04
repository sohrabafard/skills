# Alaa Trust Gateway Auth Topic Map

Use this file to choose the smallest relevant reference first.
When needed, jump to the matching section in `./full-guide.md`.

## Covered sections

- `## Purpose and use`
- `## Companion skill routing`
- `## Source priority and execution order`
- `## Compact claim and header contract`
- `## Trusted ingress and auth-service boundary`
- `## Downstream normalization and authorization`
- `## Error contract, review checklist, and anti-patterns`

## Fast file routing

- Routing order, rename rules, public versus service-local routes:
  - `10-source-priority-and-routing.md`
- Gateway verification, trusted header rules, tenant and user context:
  - `20-core-trust-model-and-headers.md`
- Auth-service v3 endpoint contract and current client flow:
  - `30-auth-service-v3-and-route-shapes.md`
- Downstream normalization, authorization, and permission bitmap rules:
  - `40-downstream-service-rules.md`
- Error contract, implementation checklist, review checklist, and anti-patterns:
  - `50-error-contract-checklists-and-anti-patterns.md`
- Permission bitmap packing, base64url semantics, and bit ordering:
  - `permission-bitmap.php`
- Historical migration intent for compact claims and null sentinels:
  - `../request-for-change.md`
- Cross-cutting or high-risk work spanning multiple domains:
  - `full-guide.md`

## Use this file when the task is about

- JWT compact claims or claim-to-header mapping
- trusted gateway header injection and spoofing defense
- public versus service-local route shape behind the gateway
- downstream request-scoped identity normalization
- permission bitmap decoding, bit ordering, or service-local permission maps
- auth-service route families and current v3 client flow
- deny-code semantics, review checklists, or anti-patterns

## Working rule

- Read only the sections you need from `./full-guide.md`.
- Prefer the smaller reference file when one file clearly matches the task.
- Keep this topic map aligned with the actual headings in the full guide.
