## Migration journal

```ts
type MigrationJournalEntry = {
  id: string;              // `${fromVersion}->${toVersion}:${step}`
  fromVersion: number;
  toVersion: number;
  step: string;
  status: 'started' | 'chunk-complete' | 'complete' | 'failed';
  processedCount: number;
  lastKey?: IDBValidKey;   // resume point for a chunked copy
  nonIdempotent?: true;
  approver?: string;       // required when nonIdempotent is true
  error?: string;
  updatedAt: string;
};
```

The journal is what makes an interrupted migration recoverable instead of ambiguous. Teaching shadow copy
without a journal is teaching half a pattern.


## What an upgrade owes other contexts

An upgrade blocks every other connection to the same database, including one held by the service worker.
`41-multitab-versionchange-and-locks.md` holds that sequence; do not design an upgrade without reading it.
