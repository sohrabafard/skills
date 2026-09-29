# Account purge procedure

The logout and account-switch purge is a security operation. Two properties make it correct: the work
must be atomic or journalled, and it must be bounded by account-indexed cursors.

When implementing the transaction or journal, follow [Transaction and journal](./20-account-purge-procedure/10-transaction-and-journal.md) for preflight, request ordering, commit handling, and retry behavior.

When handling deferred cleanup, account deletion, or verification, follow [Recovery and verification](./20-account-purge-procedure/20-recovery-and-verification.md) for the pending marker, ordered purge sequence, draft protection, reporting, and logging limits.

## It must be atomic, or journalled

See [Transaction and journal](./20-account-purge-procedure/10-transaction-and-journal.md).

## It must be bounded

See [Recovery and verification](./20-account-purge-procedure/20-recovery-and-verification.md).

## The sequence

See [Recovery and verification](./20-account-purge-procedure/20-recovery-and-verification.md).

## Unsynced drafts

See [Recovery and verification](./20-account-purge-procedure/20-recovery-and-verification.md).

## Account deletion

See [Recovery and verification](./20-account-purge-procedure/20-recovery-and-verification.md).

## What is reported

See [Recovery and verification](./20-account-purge-procedure/20-recovery-and-verification.md).
