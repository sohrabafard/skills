# Drift Management

Drift is a recorded mismatch between two sources of truth: a document against code, memory against the
repository, one service against another, a shared architecture document against actual behaviour.

## What the rule produces

`SKILL.md` states the rule itself, and states it there rather than here so that an agent who never opens this
file still cannot silently resolve a disagreement. This file owns what the rule produces, and the mechanism is
the point: a disagreement becomes a first-class, queryable, non-deletable object with an owner and a
lifecycle, and no agent may close it.

## The registry lives in the repository, under version control

The drift record is a file in a git repository. It is not a memory-store record. Three reasons, and the
third is the one that decides it:

1. **A recall store resolves disagreements by recency, which is exactly the forbidden behaviour.** A store
   that supersedes on the most recently mentioned statement will silently prefer the newer of two
   conflicting claims. Drift is precisely the case where the newest statement is not known to be the true
   one. Feeding both sides into such a store hands it a decision this skill forbids it to make.
2. **The lifecycle field must be filterable, and in a recall store it usually is not.** Where only tags are
   filterable at recall and arbitrary metadata is not, a `drift_status` carried in metadata is invisible to
   the query that drives the whole workflow. See the store adapter for the tag encoding that works around
   this when a pointer is retained.
3. **"Do not delete" has to be a fact, not a request.** In git, history is enforced by the tool: a deleted
   record is still in the log, and removing it takes a deliberate rewrite that leaves a trace. In a store
   whose value is synthesising one smoothed belief from conflicting evidence, an audit trail survives only
   as long as policy is followed. Moving the registry into git converts a policy into a property.

**Where the file goes.** Default to `docs/drift/` in the repository that owns the disputed contract, because
the fix lands in that repository and the record must travel with the code that has to change. Override only
when that repository already keeps drift records under another directory name; then use the existing one. A
mismatch spanning two services gets one record in each affected repository, both carrying the same drift
identifier, so neither repository can be fixed while believing the matter is closed.

Optionally retain one pointer per open drift in the memory store so that recall surfaces it. That pointer
carries the drift identifier and nothing else that could be mistaken for a verdict. The store adapter in use
owns the tag encoding, because only that file knows what is filterable.

## The record

- One record per mismatch, with a stable identifier used by every reference to it.
- Lifecycle: `drift_status: open` to `analyzed` to `decided` to `fixing` to `resolved`.
- Severity is not set here. `/alaa-observability-soc` (`$alaa-observability-soc`) owns whether an
  observability record is required and at what level, and `/alaa-services-contract`
  (`$alaa-services-contract`) owns the field, event, and metric names a drift record cites. Ask SOC for the
  level rather than assigning one, and state the answer's origin in the record.
- Each affected note in the store gets exactly one `[drift]` observation pointing at the record identifier,
  and its `status` becomes `needs_review`.
- Both sides of the disagreement are quoted with their source paths. A record that states only the
  conclusion cannot be re-checked once the code moves.

## These disagreements are the expensive ones

Not a severity assignment — a list of where a silent resolution costs the most, so they are checked first:

- Log contracts reaching the SOC collector: field names, format, destination.
- Notification contracts: command and event payloads, routing keys, queues, delivery workers.
- Authorisation and entitlement rules, including relationship tuples.
- Upload lifecycle events between the upload service and its target services.

## Work it by symptom

**A document contradicts the code.** The code is the behaviour; the document is a claim about it. Verify the
code path actually runs, record the mismatch, and continue on the code's behaviour. Do not edit the document
during recording — that is the fix step, and it needs the decision first.

**Memory contradicts the repository.** The repository wins on fact, always. This is not a drift record by
itself; it is a stale note. Update the note, refresh `last_verified`, and record drift only if the
repository itself is internally inconsistent. Recording every stale note as drift buries the real ones.

**Two services contradict each other.** Neither is authoritative. Establish what each actually does from its
own repository, not from a shared document, and record one drift with a record in both repositories. This is
the case where a derivation settles the question faster than either document: `alaa-signoz-clickhouse-docs`
`references/50-service-topology.md` derives which service actually calls which from trace data, so check the
observed call graph before treating a documented one as a side of the argument.

**A shared architecture document contradicts observed behaviour.** Treat the document as one side and the
derivation as the other, and name the derivation tool in the record so the next agent can re-run it.

## Derive rather than record

A drift record is for a disagreement a tool cannot settle. When a tool can settle it, run the tool:

- Which service calls which: derived from traces, as above.
- Whether an API change breaks a consumer: oasdiff, against the two OpenAPI documents.
- Whether a symbol is still referenced: Serena or ast-grep, against the current tree.

Recording a derivable fact as drift is the failure mode this section exists to prevent, because the record
then goes stale on its own schedule while the derivation stays correct.

## Separation of powers

Three steps, and no step may do another's work. The prompt numbers below are the owner's external prompt
pack, which is not in this repository; the separation holds whatever invokes it.

1. **Record.** Verify both sides, create or update the record, mark the affected notes, register it. No code
   changes.
2. **Analyse and decide.** Re-verify, state the impact, recommend a winning side, and wait for human
   approval. Record the decision and generate the per-repository fix list. Still no code changes.
3. **Fix, per repository.** Apply the decision to code *and* documents, run that repository's validation,
   clear the `[drift]` markers, refresh `last_verified`. When every affected repository is fixed, set
   `drift_status: resolved` and archive.

## Do not

- Do not change code during the record or analyse steps.
- Do not resolve a record while any affected repository remains unfixed.
- Do not delete a drift record; archive it. The audit trail is the point.
- Do not treat a schema-versus-usage report from the store's own tooling as contract drift. That is metadata
  maintenance, and the store adapter covers it.
- Do not assign a severity level in the record without naming where the level came from.
