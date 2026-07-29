/**
 * Recovery of rows orphaned in 'sending' by a context that ceased to exist.
 * references/71-browser-outbox.md
 *
 * This failure class is structurally absent from the server-side outbox, which
 * deletes the row on claim and rolls that delete back when the relay dies. The
 * browser mutates a status field in place and has no supervisor, so nothing
 * releases the claim except this function.
 */
import { txDone } from './idb-core';
import type { BrowserOutboxItem, OutboxPolicy } from './outbox-pattern';
import { DEFAULT_OUTBOX_POLICY } from './outbox-pattern';

export interface ReaperPolicy {
  /**
   * A row whose sendingSince is older than this is presumed orphaned.
   * Must exceed OutboxPolicy.sendTimeoutMs by a clear margin, or the reaper
   * races a send that is still in flight and produces a duplicate request.
   */
  readonly staleAfterMs: number;
}

export const DEFAULT_REAPER_POLICY: ReaperPolicy = { staleAfterMs: 120_000 };

export function validateReaperPolicy(
  reaper: ReaperPolicy,
  outbox: OutboxPolicy = DEFAULT_OUTBOX_POLICY,
): ReaperPolicy {
  if (!Number.isFinite(reaper.staleAfterMs) || reaper.staleAfterMs <= 0) {
    throw new RangeError('staleAfterMs must be positive');
  }
  if (reaper.staleAfterMs <= outbox.sendTimeoutMs * 2) {
    throw new RangeError(
      'staleAfterMs must exceed twice sendTimeoutMs, or the reaper races a live send',
    );
  }
  return reaper;
}

export interface ReapResult {
  /** Rows returned to 'queued'. */
  reaped: number;
  /** Rows still 'sending' and not yet stale. */
  inFlight: number;
}

/**
 * Run at the start of every flush BEFORE any claim, and on application boot.
 * Never on a timer alone: a closed device has no timer, and boot is when the
 * orphans are guaranteed to be visible.
 *
 * Safe because every request carried an idempotencyKey: if the original send did
 * reach the server, the duplicate is deduped there.
 *
 * Complexity: O(log d + s) where s is the number of rows in 'sending'.
 * It reads only the ['sending', ...] slice of the index, never the whole store.
 */
export async function reapOrphanedOutboxRows(options: {
  db: IDBDatabase;
  now?: () => Date;
  policy?: OutboxPolicy;
  reaper?: ReaperPolicy;
}): Promise<ReapResult> {
  const policy = options.policy ?? DEFAULT_OUTBOX_POLICY;
  const reaper = validateReaperPolicy(options.reaper ?? DEFAULT_REAPER_POLICY, policy);
  const now = options.now ?? (() => new Date());
  const nowMs = now().getTime();
  const nowIso = new Date(nowMs).toISOString();
  const result: ReapResult = { reaped: 0, inFlight: 0 };

  const tx = options.db.transaction(policy.storeName, 'readwrite');
  const index = tx.objectStore(policy.storeName).index(policy.indexName);
  // Only the 'sending' slice. The empty array sorts after every other key type.
  const range = IDBKeyRange.bound(['sending'], ['sending', []]);

  await new Promise<void>((resolve, reject) => {
    const request = index.openCursor(range);
    request.onerror = () => reject(request.error ?? new Error('Reaper cursor failed'));
    request.onsuccess = () => {
      const cursor = request.result;
      if (!cursor) {
        resolve();
        return;
      }

      const item = cursor.value as BrowserOutboxItem;
      // A row in 'sending' with no sendingSince is already broken: treat it as stale.
      const startedMs = item.sendingSince ? Date.parse(item.sendingSince) : 0;
      const stale = !Number.isFinite(startedMs) || nowMs - startedMs >= reaper.staleAfterMs;

      if (stale) {
        const attempts = item.attempts + 1;
        cursor.update({
          ...item,
          status: 'queued',
          sendingSince: undefined,
          attempts,
          nextAttemptAt: new Date(nowMs + policy.nextDelayMs(attempts)).toISOString(),
          lastError: 'reaped',
          updatedAt: nowIso,
        } satisfies BrowserOutboxItem);
        result.reaped += 1;
      } else {
        result.inFlight += 1;
      }

      cursor.continue();
    };
  });

  await txDone(tx);

  // 'queued' sorts after 'sending', so a reaped row moves ahead of this cursor and
  // is not revisited. The claim cursor in outbox-pattern.ts relies on the mirror
  // image of the same property. Both break if either token is renamed.
  return result;
}

/**
 * Never resolve a stuck row by deleting it: a deleted row is a user mutation that
 * no longer exists, and nothing will detect its absence.
 */
export const NEVER_DELETE_TO_UNSTICK = true;
