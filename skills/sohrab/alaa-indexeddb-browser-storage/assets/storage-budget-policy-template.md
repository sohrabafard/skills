# Storage budget policy

Feature:
Owner:
Date:

## Budget summary

| Data class | Soft cap | Hard cap | Cleanup rule | User visible? |
|---|---:|---:|---|---|
| critical unsynced | | | never silent-delete | yes |
| drafts | | | user-confirmed | yes |
| outbox | | | retry/dead-letter policy | sometimes |
| cache | | | TTL/LRU | no |
| prefetch | | | first to delete | no |

## Persistence policy

Request persistent storage when:

- [ ] user enables offline/local durable mode
- [ ] user has created valuable local data
- [ ] storage estimate is available
- [ ] private/incognito mode is not likely

If denied:

## QuotaExceededError handling

1.
2.
3.

## Cleanup order

1.
2.
3.

## User controls

- Clear cache:
- Clear offline data:
- Clear drafts:
- Storage usage display:

## Telemetry

- quota estimate buckets:
- cleanup events:
- error events:
