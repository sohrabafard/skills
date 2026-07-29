/**
 * The Tier 0 substitute. It implements the same interface as the real facade, so a
 * caller at tier 0 does not branch. references/31, class 5.
 */

/** The one storage interface every store in this pack implements. */
export interface KeyValueStore<T> {
  get(key: string): Promise<T | undefined>;
  set(key: string, value: T): Promise<void>;
  delete(key: string): Promise<void>;
  clear(): Promise<void>;
  /** Every user-scoped store must be purgeable by account. references/62. */
  deleteByAccount(accountKey: string): Promise<number>;
}

/** Use only as a Tier 0 fallback. It does not survive a reload, and it says so. */
export class MemoryStore<T extends { accountKey?: string }> implements KeyValueStore<T> {
  readonly durable = false;
  private readonly data = new Map<string, T>();

  async get(key: string): Promise<T | undefined> {
    return this.data.get(key);
  }

  async set(key: string, value: T): Promise<void> {
    this.data.set(key, value);
  }

  async delete(key: string): Promise<void> {
    this.data.delete(key);
  }

  async clear(): Promise<void> {
    this.data.clear();
  }

  async deleteByAccount(accountKey: string): Promise<number> {
    let removed = 0;
    for (const [key, value] of this.data) {
      if (value.accountKey === accountKey) {
        this.data.delete(key);
        removed += 1;
      }
    }
    return removed;
  }
}
