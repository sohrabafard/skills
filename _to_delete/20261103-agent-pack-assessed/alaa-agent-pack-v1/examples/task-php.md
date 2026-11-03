Implement the specified idempotent command in the current Laravel/Octane service.
First read repository instructions, composer.lock and the existing transaction,
tenant and outbox conventions. Do not introduce a new queue or cache abstraction.
Before coding, identify the exact API contract and acceptance criteria; if they are
missing, propose the smallest concrete brief and resolve material ambiguity.
Allowed writes must be assigned by the lead. Verify concurrent duplicate requests,
cross-tenant separation and failure between persistence and asynchronous dispatch.
Use a meaningful regression and the existing project commands. Report what actually ran.
