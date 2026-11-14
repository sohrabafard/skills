# Transactions, authorization, and lifecycle

This file owns transaction, concurrency, hook, privacy, soft-delete, raw-SQL, and RLS semantics. Routed references own constraints, indexes, and rollout; SKILL.md owns authority.

## Transaction ownership

Assign one owner for begin, commit and rollback. Pass `tx.Client()` or the transaction's entity clients through the work; outer-client operations remain outside the transaction. Use the request context, and avoid remote calls and waits while holding a transaction.

Use `client.Tx(ctx)` or `client.BeginTx(ctx,&sql.TxOptions{...})`, with sql = database/sql. BeginTx belongs to Client; WithTx is application-defined. Handle begin, body, rollback and commit errors. Roll back body failures; retain the primary error when rollback also fails. Clean up before preserving intended panic behavior. Return success, including HTTP responses, only after commit succeeds.

Transactional clients reject nested transactions. Savepoints need verified same-transaction SQL and an owner for rollback-to and release. Use actual signatures, including ExecContext's ctx argument.

Transaction-created entities retain their driver. After successful commit, Unwrap once only when later entity methods need the base client. Never unwrap ordinary or already-unwrapped entities. Discard rolled-back entities; copy DTO values when no further entity methods are needed.

## Concurrency

Define the invariant. Read Committed does not make a read, check and write sequence atomic. Prefer a sufficient atomic conditional update; check rows and validate input ranges. Optimistic concurrency combines a version predicate with atomic increment. UpdateOne NotFound may mean absent, denied, deleted, or stale; preserve public errors without leaking existence.

Use ForUpdate or ForShare within the transaction of the writes that follow, with `sql/lock` enabled. Lock rows consistently; handle NOWAIT and timeouts. Use SKIP LOCKED only when incomplete queue-claim results are acceptable. Check server restrictions for DISTINCT, joins, or grouping.

Use `context.WithTimeout` and cancel; database/sql has no WithTimeout. Align request deadlines with server statement and lock timeouts. Choose the advisory-lock scope, transaction or session, explicitly; canceled cleanup can leave a session lock on a pooled connection. Returning the connection does not prove release.

Retry the serialization (40001) and deadlock (40P01) SQLSTATEs only when the whole transaction can repeat safely. Bound attempts and time, and retain the final errors. Never retry only the last aborted statement. Do not blindly retry validation, permission, cancellation, uniqueness, or indeterminate commit failures. Reconcile unknown commit outcomes through idempotency before repeating visible work.

## Hooks and read interception

Hooks cover writes; interceptors and traversers cover reads. Update differs from UpdateOne, and Delete differs from DeleteOne. Mutation Fields contains changes, not stored state; OldX is operation-dependent and bulk mutation has no single old entity. Follow selected-generator runtime blank-import registration instead of patching generated code.

Completion of next.Mutate does not imply commit. Use tx.OnCommit for commit-bound work; invoke the next committer before declaring success. Durable external effects need a transactional outbox and idempotent delivery. Fire-and-forget proves neither commit nor delivery. A rejecting hook may return before next.Mutate.

Interceptors wrap final execution; traversers cover intermediate graph steps. Use traversers for path-wide filters. Default-limit interceptors must retain smaller explicit limits; inspect query context, not unrelated string keys. For upsert hook and policy coverage, read [queries](30-ent-queries.md). Cascades and raw SQL do not replay ordinary per-entity hooks; define policy and audit coverage.

## Privacy and tenants

Resolve the trusted viewer and tenant context, generated privacy APIs, and required flags through [feature integration](80-advanced-ent.md). Do not import `entgo.io/ent/schema/privacy`. Use the generated QueryRuleFunc, MutationRuleFunc, FilterFunc or typed filters as appropriate; ContextQueryMutationRule takes a context-only rule.

Specify default denial: empty policies, or policies whose rules all Skip, do not automatically deny. Allow stops later rules. Put mandatory authentication and tenant checks before bypassing Allow decisions. Privileged bypasses need separate authorization.

Authenticate tenants; use typed context keys. Tenant and owner IDs from a payload confer no authority. Assign tenants server-side, reject reassignment, scope writes to persisted ownership, and authorize links.

Cover Get, Only and First, Count and Exist, projections, traversal and eager loads, bulk writes, upserts, and associations. A read interceptor secures neither writes nor raw SQL. Tenant fields plus AlwaysAllow do not isolate tenants; policy and cross-tenant database constraints serve different roles.

## Soft deletion

Define default visibility, include-deleted, restore, retention, hard-delete authority, and active-row uniqueness. Keep include-deleted distinct from privacy bypass and from hard-delete authority. Do not use DecisionContext(...,Allow) to include deleted rows. Remove Allow at its source: DecisionContext(ctx,Skip) returns its parent and cannot clear inherited Allow.

Authorize the original delete, then change its operation to update, set the timestamp, and redispatch through its mutation client. Merely setting deleted_at while retaining Delete physically deletes. Preserve predicates, scope, and transaction; keep update policies active. Prevent recursion by recognizing the new operation and explicit bypass context.

Preserve the count and NotFound contracts; v0.14.6 delete builders expect a count, not an UpdateOne entity. Filter reads, Count and Exist, and intermediate traversal. Authorize updates, restores, associations, and hard deletes separately. Use narrow typed options for authorized bypasses. Report restore uniqueness conflicts; never silently delete or rename conflicting data.

## Raw SQL, RLS and audit

Raw ExecContext or QueryContext under sql/execquery bypasses Ent validators, hooks and privacy. Preserve binding, tenant predicates, and transaction context manually or through verified database policies. Never evade a denied Ent policy with raw SQL.

For RLS, test the actual application role, owner and BYPASSRLS behavior, FORCE requirements, and USING and WITH CHECK for reads and writes. Enabled RLS without policy defaults to denial, but owners and privileged roles can bypass it. Transaction-local tenant settings require the same connection and transaction; base-client queries need not share them. Prevent pool leakage.

Audit necessary actor, tenant, action, resource, correlation, and outcome. Exclude secrets, large payloads, and complete SQL arguments. Distinguish failed changes from committed changes; keep required atomic audit records inside the transaction. Sensitive alone cannot redact all logs.

## Acceptance and sources

Test the affected cases: missing identity, allowed and denied tenant, cross-tenant association, single and bulk write, and traversal and projection. Test changed rollback, commit failure, optimistic conflict, and contention. Soft-delete checks include physical retention, default hiding, tenant-preserving include-deleted, restore conflicts, and authorized hard deletion. [Runtime verification](70-runtime-testing.md) governs unavailable PostgreSQL execution; claim no untested policy completeness or race fix.

Consult [transactions](https://entgo.io/docs/transactions/), [hooks](https://entgo.io/docs/hooks/), [interceptors](https://entgo.io/docs/interceptors/), and [privacy](https://entgo.io/docs/privacy/) for unfamiliar APIs. Soft-delete return and decision behavior was checked against v0.14.6 [delete builders](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/builder/delete.tmpl) and [privacy source](https://github.com/ent/ent/blob/v0.14.6/privacy/privacy.go) on 2026-11-05; inspect selected-release code when these contracts differ. Consult target-version PostgreSQL [isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [locks](https://www.postgresql.org/docs/current/explicit-locking.html), and [RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) before relying on unfamiliar restrictions.
