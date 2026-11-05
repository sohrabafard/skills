# Ent transactions, authorization, and lifecycle

Contents: [Ownership](#transaction-ownership) · [Concurrency](#isolation-locks-and-retries) · [Lifecycle](#hooks-and-interceptors) · [Privacy](#privacy-and-tenants) · [Soft delete](#soft-delete) · [Raw SQL and RLS](#raw-sql-rls-and-audit) · [Acceptance](#acceptance)

Read for transaction, concurrency, hook, privacy, tenant, soft-delete, raw SQL or database-authorization changes. This reference owns Ent execution semantics. Routed references own schema constraints, indexes and migration rollout. Apply the main skill's authority/execution limits.

Reviewed 2026-11-05. Verify version-sensitive details against the executing project's pinned Ent/PostgreSQL.

## Transaction ownership

Assign one begin/commit/rollback owner. Pass `tx.Client()` or transaction entity clients through the unit of work. An outer-client operation remains outside the transaction. Use the request context; avoid remote calls and unnecessary waits while holding transactions.

Use `client.Tx(ctx)`, or `client.BeginTx(ctx,&sql.TxOptions{...})` for explicit isolation/read-only mode. Here sql means database/sql. The receiver is Client, not Tx. WithTx is an application helper, not a universal generated API.

Handle begin, body, rollback and commit failures. Roll back body failures; preserve the primary error if rollback also fails. Preserve intended panic semantics after cleanup. Return success only after commit succeeds, including HTTP responses.

Generated clients reject nested transactions on transactional clients. Savepoints require explicit, verified same-transaction SQL and rollback-to/release ownership. Raw statements can bypass Ent safeguards. Use actual signatures, including the ctx argument to ExecContext.

Transaction-created entities retain their transaction driver. After successful commit, call Unwrap once only when later entity operations need the base client. Do not unwrap ordinary/already-unwrapped entities. Discard rolled-back entities; copy values into DTOs when further entity methods are unnecessary.

[Transactions](https://entgo.io/docs/transactions/) · [Client template](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/client.tmpl) · [Tx template](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/tx.tmpl)

## Isolation, locks, and retries

Define the invariant first. Read Committed does not make application read/check/write atomic. Prefer an atomic conditional update when one statement suffices: predicate on version/balance, change atomically, and check affected rows. Validate input ranges independently.

For multi-step locking, enable `sql/lock` and use ForUpdate/ForShare through the transaction performing subsequent writes. Lock multiple rows in consistent order. Handle NOWAIT/timeouts explicitly. Use SKIP LOCKED only where incomplete queue-claim results are acceptable. Check PostgreSQL restrictions when locking queries use DISTINCT, joins or grouping.

For optimistic concurrency, combine a version predicate and atomic increment. Conditional UpdateOne NotFound can mean absent, unauthorized, deleted or stale. Preserve the public error contract without leaking unauthorized existence.

Use `context.WithTimeout` and cancel. There is no database/sql.WithTimeout. Request deadlines differ from server statement/lock timeouts; align both with the operation budget.

Retry SQLSTATE `40001` serialization failures or `40P01` deadlocks only when the complete transaction can safely repeat. Bound attempts and elapsed time; preserve final errors. Do not retry only the last statement of an aborted transaction. Do not blindly retry validation, permission, cancellation, uniqueness or indeterminate commit failures. A commit network failure can leave outcome unknown; use idempotency/reconciliation before repeating visible work.

Choose transaction/session advisory-lock scope explicitly. A canceled cleanup can leave a session lock attached to a pooled connection. Returning that connection to the pool does not prove release.

[Ent locking](https://entgo.io/docs/feature-flags/#row-level-locks) · [Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) · [Locks](https://www.postgresql.org/docs/current/explicit-locking.html) · [SQLSTATE](https://www.postgresql.org/docs/current/errcodes-appendix.html)

## Hooks and interceptors

Use hooks for writes and interceptors/traversers for reads. Cover required operation variants: Update/UpdateOne and Delete/DeleteOne differ. Mutation Fields contains changes, not the full stored row. Use OldX only for supported operations; bulk mutation has no single old entity.

Follow the pinned generator's runtime blank-import registration pattern for schema hooks/policies/interceptors. Do not patch generated code to fix registration.

After next.Mutate is after that mutation, not necessarily after transaction commit. Use tx.OnCommit for commit-bound work; call the next committer before claiming committed success. For durable external effects, write an outbox transactionally and deliver idempotently. Fire-and-forget goroutines prove neither commit nor delivery. A rejecting hook can return before next.Mutate.

Interceptors wrap final execution; traversers affect intermediate graph steps. Choose traversers when filters must cover the path. A default-limit interceptor must preserve smaller explicit limits; inspect query context, not unrelated string keys.

Upsert uses create hooks. DB cascades and raw SQL do not replay ordinary per-entity Ent hooks. Define policy/audit behavior for these paths.

[Hooks](https://entgo.io/docs/hooks/) · [Interceptors](https://entgo.io/docs/interceptors/) · [Commit hooks](https://entgo.io/docs/transactions/#hooks) · [Upsert](https://entgo.io/docs/crud/#upsert-one)

## Privacy and tenants

Resolve trusted viewer/tenant context and the generated privacy package. Use `privacy` generation for policies, `entql` for privacy filters, and `intercept` for generated interceptor helpers. Do not import entgo.io/ent/schema/privacy. Use generated QueryRuleFunc/MutationRuleFunc/FilterFunc/typed filters as appropriate; ContextQueryMutationRule accepts a context-only rule.

Specify default denial explicitly. Empty policies or only Skip decisions do not automatically deny. Allow stops later rules. Apply mandatory authentication/tenant checks before any allow that could bypass them. Require separately authorized privileged bypass paths.

Verify tenant identity at the authentication boundary and use typed context keys. Payload tenant/owner IDs are not authority. Assign tenant IDs server-side, reject reassignment, scope updates/deletes to persisted ownership, and check linked entities.

Cover Get/Only/First, Count/Exist, projections, traversal, eager loads, bulk operations, upserts and relation changes. A read interceptor does not secure writes/raw SQL. A tenant_id field with AlwaysAllow does not isolate tenants. Application policy and database cross-tenant constraints serve distinct roles.

[Privacy](https://entgo.io/docs/privacy/) · [Traversal semantics](https://entgo.io/docs/interceptors/#interceptors-vs-traversers)

## Soft delete

Define default visibility, include-deleted, restore, retention, hard-delete authority and active-row uniqueness. Keep include-deleted separate from general privacy bypass. Do not use privacy.DecisionContext(...,privacy.Allow) merely to include deleted rows.

Remove Allow at its source. `DecisionContext(ctx, privacy.Skip)` returns its parent; it cannot clear inherited Allow.

The official hook changes the operation to update, sets the timestamp, and redispatches through the mutation's own client. Setting deleted_at while retaining Delete still physically deletes. Preserve scope, predicates and transaction ownership. Prevent recursion by recognizing the new operation and explicit bypass context.

Authorize the original delete before changing its operation. Keep update policies active after redispatch.
Preserve affected-row and NotFound semantics; v0.14.6 delete builders expect a count, not an UpdateOne entity.

Filter reads, Count/Exist and intermediate traversal. Authorize updates, restores, relations and hard deletes separately. Use narrow typed context options only for authorized bypasses. Include-deleted must not grant hard-delete authority. A restore uniqueness conflict must be reported, not silently resolved by deleting/renaming data.

[Soft-delete pattern](https://entgo.io/docs/interceptors/#soft-delete) · [v0.14.6 privacy decisions](https://github.com/ent/ent/blob/v0.14.6/privacy/privacy.go) · [v0.14.6 delete contract](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/builder/delete.tmpl)

## Raw SQL, RLS, and audit

Raw ExecContext/QueryContext under `sql/execquery` bypass Ent hooks, validation and privacy. Preserve binding, tenant predicates and transaction context manually or through verified database policies. Never use raw SQL to evade a denied Ent policy.

RLS provides separate database enforcement. Verify the real application role, owner behavior, BYPASSRLS and FORCE ROW LEVEL SECURITY requirements. Test USING/WITH CHECK for reads/writes. Enabled RLS without a policy defaults to denial, but owners/privileged roles can bypass. Transaction-local tenant settings require guaranteed same-connection transactions. Prevent pool leakage; a base-client query need not share those settings. Role/permission changes require the main skill's authority.

Audit necessary actor, tenant, action, resource, correlation and outcome only. Exclude secrets, large payloads and complete SQL arguments. Distinguish failed from committed changes. Keep required durable audit records in the transaction when atomicity is required. Sensitive is not complete log redaction.

[Raw API](https://entgo.io/docs/feature-flags/#sql-raw-api) · [RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) · [Sensitive fields](https://entgo.io/docs/schema-fields/#sensitive-fields)

## Acceptance

Test affected scenarios: missing identity, allowed/denied tenants, cross-tenant edges, single/bulk writes and relevant traversal/projection paths. Test changed rollback, commit-failure, optimistic-conflict or concurrent behavior.

For soft delete, verify physical retention, default hiding, tenant-preserving include-deleted, restore conflicts and authorized hard deletion. Use PostgreSQL for PostgreSQL policy/concurrency evidence; SQLite is insufficient. If execution is unavailable, inspect SQL/hooks and report that limitation. Separate static reasoning, observed agent behavior and executed tests. Do not claim an untested policy complete or an unverified race fixed.

