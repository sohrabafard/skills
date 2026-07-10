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
- UPDATE: treat the existing constitution as the durable prior-decision record, preserve its
  semantic intent, and apply only supported normative deltas. Do not regenerate from scratch
  or ask the owner to repeat information already retained there.
- AUDIT: report drift without editing.

EVIDENCE WORKFLOW
1. Inspect instructions and Git status; preserve unrelated work.
2. In UPDATE mode, read the complete existing constitution before this template.
3. Read this template completely.
4. Build a prior-decision map from the existing constitution: preserved principles, open
   TODOs/proposals, exceptions, canonical sources, status/version, and missing provenance.
5. Inventory executable truth, canonical contracts/governance, architecture, tests, CI,
   generators, runbooks, consumers, security boundaries, and upstream contracts.
6. Infer the project's intent, owned outcomes, critical journeys, load-bearing qualities,
   and plausible failure modes from current user context, prior governance, and repo truth.
7. Investigate applicable cross-cutting risks and current authoritative domain guidance to
   discover material candidate obligations beyond the user's wording.
8. Build the evidence ledger, source-role map, module classification, candidate disposition,
   decision gaps, ratification evidence, and binding state as internal working data.
9. Ask only essential unresolved owner decisions. A deferred answer makes a new or already
   non-binding result DRAFT/NON_BINDING and prevents new bindings. During an update to an
   existing BINDING constitution, preserve that baseline and its adapters unchanged unless
   the owner explicitly approves replacing it with a draft.
10. Write binding rules only from repository evidence, still-valid prior governance, or
   explicit owner decisions; never invent facts, limits, contracts, dates, or approval.
11. Keep research-derived implementation ideas outside CONSTITUTION.md unless they become a
   durable owner decision or are delegated to a named canonical source.
12. Perform two writing passes, then a final constitutional compression pass.
13. Bind AGENTS.md/CLAUDE.md externally only after BINDING is authorized.
14. Validate the final document and bindings, then report authoring evidence in the final
    response—not inside CONSTITUTION.md.

INTENT AND RISK DISCOVERY
- Synthesize four claim classes separately: OBSERVED repository truth; INHERITED prior
  governance; INFERRED_CANDIDATE risks or practices; OWNER_DECIDED policy.
- Existing CONSTITUTION.md preserves only context that survived refinement. Never claim to
  recover a prior chat message or discarded rationale; ask only if missing provenance changes
  the policy outcome.
- Write an internal intent statement covering users/consumers, owned outcome, critical user
  and system journeys, runtime/data surfaces, trust boundaries, and load-bearing qualities.
- Test each evidenced surface against applicable horizons: correctness/concurrency;
  availability/overload; connectivity/offline/degraded use; data lifecycle/recovery;
  security/privacy/abuse; performance/scale/cost; accessibility/localization/compatibility;
  operations/change safety; and domain-specific continuity.
- Use relevant counterfactuals such as peak load, concurrent writes, duplicate delivery,
  dependency outage, restart, stale cache, network interruption, partial rollout, expired
  identity, storage pressure, and rollback. Do not invent applicability.
- Research only material gaps. Prefer current standards and official framework, database,
  browser/platform, protocol, vendor, or regulator sources; then maintained upstream repos
  and primary research. Use secondary articles only when primary evidence is insufficient.
- Record source, verification date, applicability, and limitation. External knowledge can
  reveal a risk or option; it does not prove current behavior or owner intent.
- Disposition every candidate as REQUIRED_BY_EVIDENCE, OWNER_DECISION_REQUIRED,
  DELEGATE_TO_CANONICAL_SOURCE, NON_CONSTITUTIONAL_FOLLOW_UP, NOT_APPLICABLE, or UNKNOWN.
- Ask interactively when a credible choice changes a durable product promise, offline or
  degraded behavior, security/privacy posture, data lifecycle, compatibility, cost/resource
  commitment, or operational risk. Recommend one option from evidence and explain trade-offs.
- Do not turn the result into a generic best-practice catalog. Keep only the smallest durable
  rules that govern real project decisions, risks, amendments, or exceptions.

INTERACTIVE OWNER DECISIONS
- Inspect evidence and complete intent/risk discovery before asking anything.
- Ask only a decision that materially changes project promises, authority, security/privacy,
  data lifecycle, compatibility, cost, validation, exceptions, status, or ratification and
  cannot be resolved from current evidence or still-valid prior governance.
- Ask at most three questions per batch. Normally stop after two batches; if essential gaps
  remain, record structured blocking TODOs and leave a DRAFT instead of extending the interview.
- Use 2-3 mutually exclusive options. Put one evidence-backed recommendation first, explain
  its project-specific reason and trade-off, and include `Decide later`.
- If evidence cannot support a recommendation, recommend `Decide later` honestly.
- Pause for the owner's answer; never select an option on the owner's behalf. A deferred or
  unanswered decision leaves a new/non-binding result DRAFT and unbound. For an existing
  BINDING baseline, preserve the canonical file, version, status, and adapters unchanged and
  report the proposed delta outside it unless the owner explicitly chose replacement.

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

CROSS-CUTTING COVERAGE GATE
For every evidenced critical journey and high-risk owned surface, investigate the applicable
intent/risk horizons above. Positive evidence may exclude a horizon; limited search may not.
Every material candidate needs provenance and one disposition before drafting. These working
classifications MUST NOT appear as a checklist, matrix, or research report in CONSTITUTION.md.

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
