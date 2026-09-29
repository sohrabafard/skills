# The record

## The record

```ts
export type BrowserOutboxStatus = 'queued' | 'sending' | 'sent' | 'conflict' | 'abandoned';

export interface BrowserOutboxItem<TBody = unknown> {
  id: string;                    // domain identifier; /alaa-crockford-base32-codecs
  accountKey: string;
  endpointKey: string;           // a registered key, never a raw URL
  body: TBody;
  idempotencyKey: string;        // generated at enqueue; shared contract with the server
  status: BrowserOutboxStatus;
  priority: 'critical' | 'normal' | 'low';
  attempts: number;
  nextAttemptAt: string;         // second segment of the scheduling index
  sendingSince?: string;         // set on claim, read by the reaper
  createdAt: string;
  updatedAt: string;
  lastError?: string;
  expiresAt?: string;
}
```

The scheduling index is `['status', 'nextAttemptAt']`, and both segments are declared fields on this type.
Confirm that before creating it — an index over an absent field is silently empty and the queue never
drains (`40-schema-and-migrations.md`).

**The cursor invariant.** Claiming changes `queued` to `sending`; `'sending'` sorts after
`'queued'`, not before it. Safety comes from the bounded exact-status range: the updated row leaves
the claim range, and a reaped row leaves the `sending` range. Keep that range when renaming states
or changing indexes. `examples/vitest-idb-pattern.test.ts` checks ordering, range exclusion and
exactly-once selection across repeated claims.
