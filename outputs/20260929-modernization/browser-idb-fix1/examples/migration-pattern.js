import { openIndexedDb } from './idb-core.js';
export const DEFAULT_SCHEMA_CONFIG = {
    dbName: 'alaa-client-storage',
    dbVersion: 4
};
export const USER_SCOPED_STORES = [
    'learning_state',
    'wa_outbox',
    'drafts',
    'upload_resume_state'
];
export async function openAlaaClientStorage(options = {}) {
    const config = options.config ?? DEFAULT_SCHEMA_CONFIG;
    if (!Number.isSafeInteger(config.dbVersion) || config.dbVersion < 4) {
        throw new RangeError('This schema requires an integer database version >= 4');
    }
    return openIndexedDb({
        name: config.dbName,
        version: config.dbVersion,
        upgrade (db, tx, oldVersion, newVersion) {
            if (oldVersion < 1) {
                db.createObjectStore('meta', {
                    keyPath: 'key'
                });
                db.createObjectStore('migration_journal', {
                    keyPath: 'id'
                });
                db.createObjectStore('capabilities', {
                    keyPath: 'key'
                });
                db.createObjectStore('storage_items', {
                    keyPath: 'id'
                }).createIndex('byDataClassLastAccessedAt', [
                    'dataClass',
                    'lastAccessedAt'
                ]);
            }
            if (oldVersion < 2) {
                const learning = db.createObjectStore('learning_state', {
                    keyPath: 'id'
                });
                learning.createIndex('byAccountUpdatedAt', [
                    'accountKey',
                    'updatedAt'
                ]);
                learning.createIndex('byContent', [
                    'accountKey',
                    'contentId'
                ]);
                const outbox = db.createObjectStore('wa_outbox', {
                    keyPath: 'id'
                });
                outbox.createIndex('byStatusNextAttemptAt', [
                    'status',
                    'nextAttemptAt'
                ]);
                outbox.createIndex('byAccountCreatedAt', [
                    'accountKey',
                    'createdAt'
                ]);
            }
            if (oldVersion < 3) {
                const drafts = db.createObjectStore('drafts', {
                    keyPath: 'id'
                });
                drafts.createIndex('byAccountTargetUpdatedAt', [
                    'accountKey',
                    'targetType',
                    'targetId',
                    'updatedAt'
                ]);
                const upload = db.createObjectStore('upload_resume_state', {
                    keyPath: 'id'
                });
                upload.createIndex('byAccountUpdatedAt', [
                    'accountKey',
                    'updatedAt'
                ]);
            }
            if (oldVersion < 4) {
                tx.objectStore('storage_items').createIndex('byAccount', [
                    'accountKey'
                ]);
            }
            tx.objectStore('meta').put({
                key: 'schemaVersion',
                value: newVersion ?? config.dbVersion,
                updatedAt: new Date().toISOString()
            });
        },
        onBlocked () {
            options.onBlocked?.();
        },
        onVersionChange () {
            options.onVersionChange?.();
        }
    });
}
