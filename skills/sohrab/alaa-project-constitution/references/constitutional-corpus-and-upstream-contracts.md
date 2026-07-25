# Constitutional Corpus, Charter Shape, and Upstream Contracts

Read this reference when the repository already has governance or contract documents, when it
consumes a shared kit, framework, scaffold, SDK, platform baseline, or policy pack, or when
choosing the charter shape.

## Select the charter shape

### THIN_CHARTER

Choose `THIN_CHARTER` when detailed policy already has maintained canonical owners — a contracts
document, a governance document, ADRs, an architecture charter, security policy, generated API
contracts, runbooks, or upstream framework contracts.

A thin charter owns scope, authority, and conflict handling; durable principles and ownership
boundaries; the canonical-source registry and incorporation rules; change-risk classification and
constitutional gates; and ratification, amendment, exception, and periodic-review rules.

It does not reproduce wire formats, routes, headers, queues, event or error catalogs, environment
keys, metric names, thresholds, command catalogs, or long runbook procedures. Those stay with their
canonical owners.

A thin charter still carries every matched archetype's obligations — as one sentence each naming the
observable condition and the canonical source that owns the detail. Thinness is achieved by
delegating detail, never by dropping an obligation.

### FULL_CHARTER

Choose `FULL_CHARTER` only when the repository lacks an adequate constitutional corpus and the
project-specific rules genuinely need to live in `CONSTITUTION.md`. Even then, assign one canonical
owner per topic and do not duplicate executable or generated contracts.

## THIN_CHARTER compression profile

A thin charter is an authority and index layer, not a compressed copy of the repository's documents.

- Keep only scope, precedence, durable principles, source ownership, risk gates, amendment,
  exception, and review rules.
- Fold load-bearing module rules into the core principles; do not emit a module inventory.
- Put an exact command in one location at most. Prefer a canonical `Makefile`, manifest, CI job, or
  runbook reference over repeating command catalogs in module sections and again in a matrix.
- Keep only constitution-defining evidence; do not restate general project inventories.
- Delete repeated source descriptions, protocol catalogs, thresholds, and procedures.
- The bundled validator rejects a `THIN_CHARTER` above 12 KiB or 160 physical lines. Where policy
  genuinely needs more detail, move detail to a canonical source or select `FULL_CHARTER` with
  evidence; never relabel an oversized duplicate as thin.

Reject authoring residue from the final constitution: metadata tables, sync impact reports, evidence
ledgers, module inventories, claim labels, validation matrices or transcripts, agent operating
tutorials, finalization narratives, and binding sections. That information belongs in working state
and the final response.

## Closed delegation

Every durable phrase that delegates behaviour to another source must close over the source registry.
Replace vague text such as "follow maintained guidance" with a repository path, a versioned upstream
source, or a structured TODO. The registry records each source's topic ownership, authority status,
incorporation mode, and freshness or validation rule. A delegation whose target cannot be opened
from the repository is not closed.

## Build the document-role map

Classify every material source:

| Classification | Meaning |
|---|---|
| `LOCAL_CANONICAL` | Repository-owned source of truth for one defined topic. |
| `INCORPORATED_BY_REFERENCE` | Local canonical source made constitutionally required without copying its body. |
| `UPSTREAM_CANONICAL` | Versioned contract owned by another repository, package, or platform. |
| `GENERATED` | Reproducible artifact whose generator is canonical. |
| `ADVISORY` | Useful guidance that is not approved policy. |
| `HISTORICAL` | Preserved provenance that no longer governs current work. |

For each source record its topic, owner, precedence, freshness rule, and what the constitution
intentionally does not duplicate. Two sources must not both claim canonical ownership of the same
detail; record overlap as drift and resolve it before ratification.

Record authority and approval status independently from classification. "Canonical" means the source
owns a topic; it does not mean a human ratified it. A source may be canonical and active while its
approver roster or formal ratification remains pending.

## Upstream kit and framework consumer rule

A consumer repository must not copy an upstream editable contract and have an agent rewrite it for
local use. That creates an unversioned fork.

Record instead:

- the upstream owner and the canonical contract location;
- the exact dependency or version pin from the manifest or lockfile;
- inherited surfaces versus consumer-owned domain behaviour;
- the conformance or contract tests that enforce the inherited contract;
- the upgrade, deprecation, compatibility, and change-request workflow;
- how agents reach the upstream contract when the source repository is unavailable.

A local generated snapshot is permitted only where the upstream owns that delivery model. It must be
reproducible, read-only in the consumer, stamped with upstream identity, version, and source, and
drift-checked against the dependency pin. Otherwise use a short reference manifest or documentation
link, never a copied contract body.

## Consumer constitution pattern

For a service built on a shared kit, the consumer's `CONSTITUTION.md` combines:

1. the consumer's domain charter, matched archetypes, and service-specific risks;
2. an `UPSTREAM_KIT_FRAMEWORK_CONTRACTS` module pointing to the pinned kit contract;
3. an explicit rule that local policy cannot weaken or fork inherited kit surfaces;
4. the kit's conformance tests and its upgrade and change-request process;
5. local canonical domain sources such as its architecture document, API contract, data ownership,
   runbooks, and operational decisions.

Where the kit already satisfies an archetype obligation, the consumer constitution names the
obligation and cites the kit contract as its canonical owner. Where the kit is silent on an
obligation a matched archetype makes mandatory, the consumer owns that rule locally and says so —
inheritance narrows what the consumer must write, never what the service owes.

The consumer does not inherit the kit repository's maintainer governance, package-owner rules, or
internal implementation constitution unless the upstream explicitly marks those rules as
consumer-facing.
