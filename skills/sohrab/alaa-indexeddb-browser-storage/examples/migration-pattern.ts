/**
 * Versioned schema with explicit oldVersion branches and a migration journal.
 * references/40-schema-and-migrations.md
 *
 * Every name below is a value owned by /alaa-services-contract ($alaa-services-contract).
 * They are constants here so a real application injects its registered values.
 */
import { openIndexedDb } from './idb-core';

export interface StorageSchemaConfig {
  readonly dbName: string;
  readonly dbVersion: number;
}

/** Defaults only. A real application reads these from its registered configuration. */
export const DEFAULT_SCHEMA_CONFIG: StorageSchemaConfig = {
  dbName: 'alaa-client-storage',
  dbVersion: 3,
};

/** Every user-scoped store, for the logout purge. references/62. */
export const USER_SCOPED_STORES = [
  'learning_state',
  'wa_outbox',
  'drafts',
  'upload_resume_state',
] as const;

export interface OpenStorageOptions {
  readonly config?: StorageSchemaConfig;
  readonly onBlocked?: () => void;
  readonly onVersionChange?: () => void;
}

export async function openAlaaClientStorage(options: OpenStorageOptions = {}): Promise<IDBDatabase> {
  const config = options.config ?? DEFAULT_SCHEMA_CONFIG;

  return openIndexedDb({
    name: config.dbName,
    version: config.dbVersion,
    upgrade(db, tx, oldVersion, newVersion) {
      if (oldVersion < 1) {
        db.createObjectStore('meta', { keyPath: 'key' });
        db.createObjectStore('migration_journal', { keyPath: 'id' });
        db.createObjectStore('capabilities', { keyPath: 'key' });
        db.createObjectStore('storage_items', { keyPath: 'id' })
          // dataClass values come from assets/data-classification-policy.yaml.
          .createIndex('byDataClassLastAccessedAt', ['dataClass', 'lastAccessedAt']);
      }

      if (oldVersion < 2) {
        const learning = db.createObjectStore('learning_state', { keyPath: 'id' });
        learning.createIndex('byAccountUpdatedAt', ['accountKey', 'updatedAt']);
        learning.createIndex('byContent', ['accountKey', 'contentId']);

        const outbox = db.createObjectStore('wa_outbox', { keyPath: 'id' });
        // Both segments are declared fields on BrowserOutboxItem. An index over a
        // field the record lacks is silently empty and the queue never drains.
        outbox.createIndex('byStatusNextAttemptAt', ['status', 'nextAttemptAt']);
        outbox.createIndex('byAccountCreatedAt', ['accountKey', 'createdAt']);
      }

      if (oldVersion < 3) {
        const drafts = db.createObjectStore('drafts', { keyPath: 'id' });
        // accountKey first: the logout purge is O(matching + log n), not O(n).
        drafts.createIndex('byAccountTargetUpdatedAt', [
          'accountKey',
          'targetType',
          'targetId',
          'updatedAt',
        ]);

        const upload = db.createObjectStore('upload_resume_state', { keyPath: 'id' });
        upload.createIndex('byAccountUpdatedAt', ['accountKey', 'updatedAt']);
      }

      // Written once, outside every branch. Inside the newest branch it goes stale
      // the first time an author adds a branch and forgets.
      tx.objectStore('meta').put({
        key: 'schemaVersion',
        value: newVersion ?? config.dbVersion,
        updatedAt: new Date().toISOString(),
      });
    },
    onBlocked() {
      // Another tab or the service worker holds the old version. Surface the reload
      // UX; never delete the database to resolve this. references/41.
      options.onBlocked?.();
    },
    onVersionChange() {
      // openIndexedDb already closed this connection.
      options.onVersionChange?.();
    },
  });
}

export interface MigrationJournalEntry {
  id: string; // `${fromVersion}->${toVersion}:${step}`
  fromVersion: number;
  toVersion: number;
  step: string;
  status: 'started' | 'chunk-complete' | 'complete' | 'failed';
  processedCount: number;
  lastKey?: IDBValidKey;
  nonIdempotent?: true;
  approver?: string; // required when nonIdempotent is true
  error?: string;
  updatedAt: string;
}
