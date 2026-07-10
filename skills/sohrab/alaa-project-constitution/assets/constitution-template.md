<!--
TEMPLATE-ONLY: PROJECT CONSTITUTION GENERATION CONTRACT

PURPOSE
Create or update one evidence-backed repository constitution. The final document is law,
not authoring telemetry, a tutorial, an evidence report, or a description of agent runtimes.

CANONICAL PATHS
- Template: ./constitution-template.md
- Output: ./CONSTITUTION.md
- Keep exactly one correctly spelled active constitution.

OPERATING MODES
- CREATE: no prior constitution exists.
- UPDATE: preserve prior governance and apply only supported normative deltas.
- AUDIT: report drift without editing.

EVIDENCE WORKFLOW
1. Inspect instructions and Git status; preserve unrelated work.
2. In UPDATE mode, read the complete existing constitution before this template.
3. Read this template completely.
4. Inventory executable truth, canonical contracts/governance, architecture, tests, CI,
   generators, runbooks, consumers, security boundaries, and upstream contracts.
5. Build the evidence ledger, source-role map, module classification, decision gaps,
   ratification evidence, and binding state as internal working data.
6. Ask only essential unresolved owner decisions. A deferred answer forces
   DRAFT/NON_BINDING and prevents new runtime bindings.
7. Write from repository evidence; never invent facts, owners, limits, contracts, dates,
   commands, or approval.
8. Perform two writing passes, then a final constitutional compression pass.
9. Bind AGENTS.md/CLAUDE.md externally only after BINDING is authorized.
10. Validate the final document and bindings, then report authoring evidence in the final
    response—not inside CONSTITUTION.md.

FINAL DOCUMENT IS LAW, NOT AUTHORING TELEMETRY
The final CONSTITUTION.md MUST contain only durable rules that materially guide project
decisions. It MUST NOT contain:
- a Constitution Metadata table;
- a Sync Impact Report or hidden generation report;
- evidence ledgers, confidence tables, module classifications, or project inventories;
- validation transcripts, command matrices, or pass/fail reports;
- AGENTS.md/CLAUDE.md binding instructions, import syntax, adapter status, or context budgets;
- owner-decision state, finalization outcome, template path, generation mode, or prompt data;
- amendment history ceremony, finalization narrative, or tutorial-style before/during/after steps.

Keep binding mechanics in AGENTS.md/CLAUDE.md and keep generation/validation details in the
agent's final response. A constitution may reference canonical files by path, but it must not
describe how an agent loads those files.

FINAL CONSTITUTIONAL COMPRESSION PASS
After the evidence-backed rewrite:
1. Reopen and reread the entire CONSTITUTION.md as if it will be injected into every coding
   task forever.
2. Delete any sentence that does not change a project decision, prevent a concrete failure,
   name a durable authority boundary, or define amendment/exception control.
3. Merge repeated rules and remove explanatory history, examples, workflow narration, and
   facts already owned by canonical sources.
4. Prefer one strong sentence over a table when the table adds no decision value.
5. Verify the document reads as a constitution, not a policy-generation artifact.

AUTHORITY AND STATUS
- Higher-precedence instructions remain controlling.
- Canonical ownership, current authority, approval, and ratification are distinct facts.
- CREATE/UPDATE permission is not ratification unless the launcher or owner explicitly says so.
- BINDING requires complete essential decisions and ratification evidence in the working
  record; the final document records status only in the footer.
- DRAFT and NEEDS_REVIEW remain non-binding and MUST NOT be newly imported or activated.
- SUPERSEDED is inactive and points runtime bindings to its successor.

UNKNOWN AND PROPOSAL RULES
- Missing evidence is not proof of absence.
- Material unresolved facts use:
  TODO(<stable-id>): <decision>; reason: <gap>; owner: <role or UNKNOWN>; blocking: yes|no.
- Unapproved policy uses:
  PROPOSAL(<stable-id>): <candidate rule>; evidence/rationale: <why>;
  approval required from: <role or UNKNOWN>.
- A BINDING constitution contains no blocking TODO.

CONSTITUTION SHAPE
- Prefer THIN_CHARTER when mature canonical sources own technical and operational detail.
- Use FULL_CHARTER only when the repository lacks an adequate constitutional corpus.
- Conditional modules shape the principles; they do not become a module inventory in the
  final document.
- A thin charter should normally remain below 12 KiB and 160 physical lines. Smaller is
  better when authority and safeguards remain complete.

MODULE DETECTION CHECKLIST
Classify each as INCLUDE, EXCLUDE, or UNKNOWN from positive evidence. Retain only the
load-bearing rule that belongs in constitutional policy; delegate technical detail to a
canonical source.
- MONOREPO_PACKAGES_SDK_CLI
- UPSTREAM_KIT_FRAMEWORK_CONTRACTS
- API_CONTRACTS
- GO_CHI
- LARAVEL_PHP_OCTANE
- FRONTEND_WEB_SSR_PWA
- GATEWAY_PROXY_TRUST
- DATA_MIGRATIONS
- REDIS_CACHE_LOCKS
- ASYNC_JOBS_EVENTS
- REALTIME_STREAMING
- INTEGRATIONS_WEBHOOKS
- MEDIA_FILES
- SEARCH_INDEXING
- INFRA_CI_RUNTIME
- OBSERVABILITY_SOC
- DOCS_GENERATED_AGENT_GUIDANCE

MINIMUM FINAL STRUCTURE
- One H1: project constitution title.
- A short purpose/effect paragraph.
- Authority and Scope.
- Core Principles, consolidated around actual project risks.
- Canonical Sources, as a compact closed delegation list when needed.
- Change Governance.
- Amendments and Exceptions.
- Unresolved Decisions only when a DRAFT/NEEDS_REVIEW has blocking decisions.
- Exactly one footer line for version/status/dates.

No other section is mandatory merely because the authoring workflow used it.
END TEMPLATE-ONLY GENERATION CONTRACT
-->

# {{PROJECT_NAME}} Constitution

{{PURPOSE_AND_BINDING_EFFECT}}

## Authority and Scope

{{GOVERNED_SCOPE_AUTHORITY_PRECEDENCE_AND_CONFLICT_RULE}}

## Core Principles

### {{PRINCIPLE_NUMBER_AND_NAME}}

{{PROJECT_SPECIFIC_DURABLE_RULES}}

## Canonical Sources

- `{{SOURCE_PATH_OR_VERSIONED_REFERENCE}}` owns {{CANONICAL_TOPIC}}.

{{SOURCE_PRECEDENCE_AND_DRIFT_RULE}}

## Change Governance

{{RISK_COMPATIBILITY_CONSUMER_IMPACT_AND_COMPLETION_RULES}}

## Amendments and Exceptions

{{VERSIONING_AMENDMENT_EXCEPTION_AND_REVIEW_RULES}}

{{UNRESOLVED_DECISIONS_SECTION_OR_OMIT}}

**Version**: {{SEMVER}} | **Status**: {{STATUS}} | **Ratified**: {{DATE_OR_NOT_RATIFIED}} | **Last Amended**: {{DATE}} | **Last Evidence Review**: {{DATE}}
