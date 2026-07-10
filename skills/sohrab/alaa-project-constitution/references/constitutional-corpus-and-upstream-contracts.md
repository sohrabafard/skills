# Constitutional Corpus and Upstream Contracts

Read this reference when a repository already has mature governance/contract documents or
consumes a shared kit, framework, scaffold, SDK, platform baseline, or policy pack.

## Select the constitution shape

### THIN_CHARTER

Choose `THIN_CHARTER` when detailed policy already has maintained canonical owners, such
as `CONTRACTS.md`, `GOVERNANCE.md`, ADRs, architecture charters, security policies,
generated API contracts, runbooks, or upstream framework contracts.

A thin charter owns:

- scope, authority, and conflict handling;
- durable principles and ownership boundaries;
- the canonical-source registry and incorporation rules;
- change-risk classification and constitutional gates;
- ratification effect, amendment, exception, and periodic-review rules.

It does not reproduce exact wire formats, routes, headers, queues, event/error catalogs,
environment keys, metric names, thresholds, command catalogs, or long runbook procedures.
Those remain with their canonical owners.

Binding delivery remains external to the constitution: AGENTS.md and CLAUDE.md point to the
file, while CONSTITUTION.md contains no adapter status, import syntax, or runtime instructions.

### FULL_CHARTER

Choose `FULL_CHARTER` only when the repository lacks an adequate constitutional corpus and
the project-specific rules genuinely need to live in `CONSTITUTION.md`. Even then, assign
one canonical owner per topic and avoid duplicating executable or generated contracts.

## Build the document-role map

Classify every material source:

| Classification | Meaning |
|---|---|
| `LOCAL_CANONICAL` | Repository-owned source of truth for one defined topic. |
| `INCORPORATED_BY_REFERENCE` | Local canonical source made constitutionally required without copying its body. |
| `UPSTREAM_CANONICAL` | Versioned contract owned by another repository/package/platform. |
| `GENERATED` | Reproducible artifact whose generator is canonical. |
| `ADVISORY` | Useful guidance that is not approved policy. |
| `HISTORICAL` | Preserved provenance that no longer governs current work. |

For each source record its topic, owner, precedence, freshness rule, and what the
constitution intentionally does not duplicate. Two sources must not both claim canonical
ownership of the same detail. Record overlap as drift and resolve it before ratification.

Record authority/approval status independently from classification. “Canonical” means the
source owns a topic; it does not mean a human ratified it. A source may be canonical and
active while its approver roster or formal ratification remains pending.

## Upstream kit/framework consumer rule

A consumer repository must not copy an upstream editable contract and ask an agent to
rewrite it for local use. That creates an unversioned fork.

Instead record:

- upstream owner and canonical contract location;
- exact dependency/version pin from the manifest or lockfile;
- inherited surfaces versus consumer-owned domain behavior;
- conformance/contract tests that enforce the inherited contract;
- upgrade, deprecation, compatibility, and change-request workflow;
- how agents access the upstream contract when the source repository is unavailable.

A local generated snapshot is permitted only when the upstream owns that delivery model.
It must be reproducible, read-only in the consumer, stamped with upstream identity/version/
source, and drift-checked against the dependency pin. Otherwise use a short reference
manifest or documentation link, not a copied contract body.

## Consumer constitution pattern

For a service built on a shared kit, the consumer `CONSTITUTION.md` should combine:

1. the consumer's domain charter and service-specific risks;
2. an `UPSTREAM_KIT_FRAMEWORK_CONTRACTS` module pointing to the pinned kit contract;
3. an explicit rule that local policy cannot weaken or fork inherited kit surfaces;
4. the kit's conformance/contracttest and upgrade/change-request process;
5. local canonical domain sources such as its architecture document, API contract, data
   ownership, runbooks, and operational decisions.

The consumer does not inherit the kit repository's maintainer governance, package-owner
rules, or internal implementation constitution unless the upstream explicitly marks those
rules as consumer-facing.

## Status-aware adapter language

Use equivalent concise wording, adapted to the selected path.

### BINDING

```text
Read CONSTITUTION.md before work. It is binding project policy within its ratified scope.
Surface conflicts and use its amendment or exception process.
```

### DRAFT or NEEDS_REVIEW

```text
Read CONSTITUTION.md before work as a non-binding governance proposal. Existing canonical
sources remain authoritative under their current status. Surface conflicts and do not
present the draft as approved policy.
```

### SUPERSEDED

Remove the active import/reference or point it to the successor. State that the old file
is inactive historical policy.
