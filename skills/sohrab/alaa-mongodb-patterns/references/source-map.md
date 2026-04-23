# Source Map

Use this map when MongoDB collection design, index behavior, TTL, transactions, or current server behavior may be version-sensitive.

## Source order

1. Repository truth:
   - installed MongoDB driver/ODM packages, collection access code, migrations/index bootstrap scripts, tests, runtime config, and production docs.
2. Official MongoDB sources:
   - MongoDB manual: https://www.mongodb.com/docs/manual/
   - Indexes: https://www.mongodb.com/docs/manual/indexes/
   - Compound indexes: https://www.mongodb.com/docs/manual/core/indexes/index-types/index-compound/
   - TTL indexes: https://www.mongodb.com/docs/manual/core/index-ttl/
   - Schema validation: https://www.mongodb.com/docs/manual/core/schema-validation/
   - Transactions: https://www.mongodb.com/docs/manual/core/transactions/
   - Retryable writes: https://www.mongodb.com/docs/manual/core/retryable-writes/
3. Driver and Laravel integration sources:
   - PHP MongoDB library: https://www.mongodb.com/docs/php-library/current/
   - PHP extension docs: https://www.php.net/manual/en/book.mongodb.php
   - Laravel MongoDB docs: https://laravel.com/docs/13.x/mongodb
4. Community posts and StackOverflow answers:
   - Troubleshooting only. Verify index restrictions, TTL behavior, and query-plan claims against MongoDB docs and `explain()`.

## Freshness triggers

Verify official docs or live server behavior when the task mentions:

- `latest`, `current`, `upgrade`, `security`, `CVE`, MongoDB server major version, Atlas behavior, TTL, time series, compound indexes, transactions, retryable writes, sharding, or query planner changes.

## Small example

Use a single-field TTL index for expiration:

```javascript
db.sessions.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 })
```

Anti-pattern:

```javascript
db.sessions.createIndex(
  { project_id: 1, expires_at: 1 },
  { expireAfterSeconds: 0 }
)
```

MongoDB TTL indexes are single-field indexes. Keep tenant/query acceleration in a separate compound index.
