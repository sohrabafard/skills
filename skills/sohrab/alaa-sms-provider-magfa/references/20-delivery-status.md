# Magfa HTTP v2 delivery status codes

Read this file when you map a `dlrs[].status` value from `GET /statuses/{mid1,mid2,...}` to a normalized delivery state, or decide whether to keep polling. `SKILL.md` "Delivery status (pull only)" owns the polling rules.

Source: `https://messaging.magfa.com/ui/?public/wiki/api/http_v2`, read 2026-10-20 from the rendered page. `SKILL.md` "Provenance" owns the re-verification rule.

| Magfa `status` | Meaning | Normalized | Polling |
|---|---|---|---|
| `1` | delivered to handset | `delivered` | stop |
| `2` | not delivered to handset | `failed` | stop |
| `16` | not delivered to operator | `failed` | stop |
| `8` | delivered to operator | `sent` | continue; may become `1` or `2` |
| `0` | no status yet | `pending` | continue |
| `-1` | unknown id, or more than 24 hours since send | `expired` | stop |
