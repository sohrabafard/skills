# Magfa HTTP v2 endpoints, send fields and send response

Read this file when you build a request path, a `send` body, or a parser for the `send` response. The rules that govern these shapes stay in `SKILL.md`.

Source: `https://messaging.magfa.com/ui/?public/wiki/api/http_v2`, read 2026-10-20 from the rendered page. `SKILL.md` "Provenance" owns the re-verification rule.

## Endpoints

| Method | HTTP | Path | Purpose |
|---|---|---|---|
| `send` | POST | `/send` | send to at most 100 recipients |
| `mid` | GET | `/mid/{uid}` | provider message id for a client `uid` |
| `statuses` | GET | `/statuses/{mid1,mid2,...}` | final status, at most 100 ids |
| `messages` | GET | `/messages` or `/messages/{count}` | inbound messages, at most 100 |
| `balance` | GET | `/balance` | remaining credit |

## Send fields

| Field | Type | Vendor | Alaa | Notes |
|---|---|---|---|---|
| `senders` | string[] | required | required | sender lines |
| `recipients` | string[] | required | required | at most 100 |
| `messages` | string[] | required | required | full UTF-8 text |
| `uids` | long[] | optional | **required** | one client id per message; see `SKILL.md` "Idempotency" |
| `encodings` | int[] | optional | omit or `0` | `0` auto (default), `2` Farsi, `5` 8-bit, `6` binary |
| `udhs` | string[] | optional | omit | Alaa sends no UDH |

## Send response example

```json
{
  "status": 0,
  "messages": [
    { "status": 13, "userId": "1223", "recipient": "98912xxxxxxx" },
    { "status": 0, "id": 111111111, "userId": 1224, "parts": 3, "tariff": 160.00, "alphabet": "UCS2", "recipient": "98913xxxxxxx" }
  ]
}
```

The first item is rejected with code `13`. The second item is accepted. The vendor example shows `userId` as a string in the first item and as a number in the second.
