# Transactions, authorization, and lifecycle

Own transaction, concurrency, hook, privacy, soft-delete, raw-SQL, and RLS semantics. Routed references own constraints, indexes, and rollout; SKILL.md owns authority.

## Transaction ownership

Assign one begin/commit/rollback owner. Pass `tx.Client()`/transaction entity clients through the work; outer-client operations remain outside it. Use request context; avoid remote calls/waits while holding transactions.

Use `client.Tx(ctx)` or `client.BeginTx(ctx,&sql.TxOptions{...})`, with sql = database/sql. BeginTx belongs to Client; WithTx is application-defined. Handle begin/body/rollback/commit errors. Roll back body failures; retain the primary error when rollback also fails. Clean up before preserving intended panic behavior. Return success, including HTTP responses, only after commit succeeds.

Transactional clients reject nested transactions. Savepoints need verified same-transaction SQL and rollback-to/release ownership. Use actual signatures, including ExecContext's ctx argument.

Transaction-created entities retain their driver. After successful commit, Unwrap once only when later entity methods need the base client. Never unwrap ordinary/already-unwrapped entities. Discard rolled-back entities; copy DTO values when no further entity methods are needed.

## Concurrency

Define the invariant. Read Committed does not make read/check/write atomic. Prefer a sufficient atomic conditional update; check rows and validate input ranges. Optimistic concurrency combines a version predicate with atomic increment. UpdateOne NotFound may mean absent, denied, deleted, or stale; preserve public errors without leaking existence.

Use ForUpdate/ForShare within the subsequent writes' transaction, with `sql/lock` enabled. Lock rows consistently; handle NOWAIT/timeouts. Use SKIP LOCKED only when incomplete queue-claim results are acceptable. Check server restrictions for DISTINCT, joins, or grouping.

Use `context.WithTimeout` and cancel; database/sql has no WithTimeout. Align request deadlines and server statement/lock timeouts. Choose advisory transaction/session scope explicitly; canceled cleanup can leave a session lock on a pooled connection. Returning the connection does not prove release.

Retry serialization (40001)/deadlock (40P01) SQLSTATEs only when the whole transaction can repeat safely. Bound attempts/time and retain final errors. Never retry only the last aborted statement. Do not blindly retry validation, permission, cancellation, uniqueness, or indeterminate commit failures. Reconcile unknown commit outcomes through idempotency before repeating visible work.

## Hooks and read interception

Hooks cover writes; interceptors/traversers cover reads. Update/UpdateOne and Delete/DeleteOne differ. Mutation Fields contains changes, not stored state; OldX is operation-dependent and bulk mutation has no single old entity. Follow selected-generator runtime blank-import registration instead of patching generated code.

Completion of next.Mutate does not imply commit. Use tx.OnCommit for commit-bound work; invoke the next committer before declaring success. Durable external effects need a transactional outbox and idempotent delivery. Fire-and-forget proves neither commit nor delivery. A rejecting hook may return before next.Mutate.

Interceptors wrap final execution; traversers cover intermediate graph steps. Use traversers for path-wide filters. Default-limit interceptors must retain smaller explicit limits; inspect query context, not unrelated string keys. For upsert hook/policy coverage, read [queries](30-ent-queries.md). Cascades/raw SQL do not replay ordinary per-entity hooks; define policy/audit coverage.

## Privacy and tenants

Resolve trusted viewer/tenant context, generated privacy APIs, and required flags through [feature integration](80-advanced-ent.md). Do not import `entgo.io/ent/schema/privacy`. Use generated QueryRuleFunc/MutationRuleFunc/FilterFunc/typed filters as appropriate; ContextQueryMutationRule takes a context-only rule.

Specify default denial: empty policies/all Skip do not automatically deny. Allow stops later rules. Put mandatory authentication/tenant checks before bypassing Allow decisions. Privileged bypasses need separate authorization.

Authenticate tenants; use typed context keys. Payload tenant/owner IDs confer no authority. Assign tenants server-side, reject reassignment, scope writes to persisted ownership, and authorize links.

Cover Get/Only/First, Count/Exist, projections, traversal/eager loads, bulk writes, upserts, and associations. A read interceptor secures neither writes nor raw SQL. Tenant fields plus AlwaysAllow do not isolate tenants; policy and cross-tenant database constraints serve different roles.

## Soft deletion

Define default visibility, include-deleted, restore, retention, hard-delete authority, and active-row uniqueness. Keep include-deleted distinct from privacy bypass/hard-delete authority. Do not use DecisionContext(...,Allow) to include deleted rows. Remove Allow at its source: DecisionContext(ctx,Skip) returns its parent and cannot clear inherited Allow.

Authorize the original delete, then change its operation to update, set the timestamp, and redispatch through its mutation client. Merely setting deleted_at while retaining Delete physically deletes. Preserve predicates, scope, and transaction; keep update policies active. Prevent recursion by recognizing the new operation and explicit bypass context.

Preserve count/NotFound contracts; v0.14.6 delete builders expect a count, not an UpdateOne entity. Filter reads, Count/Exist, and intermediate traversal. Authorize updates, restores, associations, and hard deletes separately. Use narrow typed options for authorized bypasses. Report restore uniqueness conflicts; never silently delete/rename conflicting data.

## Raw SQL, RLS, audit

Raw ExecContext/QueryContext under sql/execquery bypasses Ent validators/hooks/privacy. Preserve binding, tenant predicates, and transaction context manually or through verified database policies. Never evade a denied Ent policy with raw SQL.

For RLS, test the actual application role, owner/BYPASSRLS behavior, FORCE requirements, and USING/WITH CHECK for reads/writes. Enabled RLS without policy defaults to denial, but owners/privileged roles can bypass. Transaction-local tenant settings require the same connection/transaction; base-client queries need not share them. Prevent pool leakage.

Audit necessary actor, tenant, action, resource, correlation, and outcome. Exclude secrets, large payloads, and complete SQL arguments. Distinguish failed/committed changes; keep required atomic audit records inside the transaction. Sensitive alone cannot redact all logs.

## Acceptance and sources

Test affected missing-identity, allowed/denied tenant, cross-tenant association, single/bulk write, and traversal/projection cases. Test changed rollback, commit failure, optimistic conflict, and contention. Soft-delete checks include physical retention, default hiding, tenant-preserving include-deleted, restore conflicts, and authorized hard deletion. [Runtime verification](70-runtime-testing.md) governs unavailable PostgreSQL execution; claim no untested policy completeness or race fix.

Consult [transactions](https://entgo.io/docs/transactions/), [hooks](https://entgo.io/docs/hooks/), [interceptors](https://entgo.io/docs/interceptors/), and [privacy](https://entgo.io/docs/privacy/) for unfamiliar APIs. Soft-delete return/decision behavior was checked against v0.14.6 [delete builders](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/builder/delete.tmpl) and [privacy source](https://github.com/ent/ent/blob/v0.14.6/privacy/privacy.go) on 2026-11-05; inspect selected-release code when these contracts differ. Consult target-version PostgreSQL [isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [locks](https://www.postgresql.org/docs/current/explicit-locking.html), and [RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) before relying on unfamiliar restrictions.
