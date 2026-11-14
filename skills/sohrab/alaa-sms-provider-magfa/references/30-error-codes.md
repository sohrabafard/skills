# Magfa HTTP v2 error codes

Read this file when you classify a non-zero top-level `status` or a non-zero item `status`, or write the error-mapping tests. `SKILL.md` "Error codes and classes" defines each class and owns the rule for an unlisted code.

Source: `https://messaging.magfa.com/ui/?public/wiki/api/http_v2`, read 2026-10-20 from the rendered page. `SKILL.md` "Provenance" owns the re-verification rule.

| Code | Meaning | Class |
|---|---|---|
| `1` | invalid recipient | recipient-terminal; repeated occurrences indicate a normaliser defect |
| `2` | invalid sender | caller-defect |
| `3` | invalid encoding for the text | caller-defect |
| `4` | invalid mclass | caller-defect |
| `6` | invalid UDH | caller-defect |
| `8` | promotional send outside 07:00–22:00 | window |
| `13` | empty content | caller-defect |
| `14` | insufficient credit | account |
| `15` | internal server error, resend | transient; OTP: same-code resend without lookup allowed |
| `16` | account inactive | account |
| `17` | account expired | account |
| `18` | invalid username or password | account |
| `19` | invalid username, password and domain combination | account |
| `20` | sender not owned by the account | caller-defect (line-to-account mapping) |
| `22` | service not enabled for the account | account |
| `23` | cannot process now, resend | transient; OTP: same-code resend without lookup allowed |
| `24` | invalid message id, or older than one day | caller-defect on `mid`/`statuses`; `expired` when older than one day |
| `25` | invalid method name | caller-defect |
| `27` | recipient on operator blacklist (promotional) | recipient-terminal |
| `28` | recipient prefix blocked at Magfa | recipient-terminal |
| `29` | source IP not allowed | account (egress IP) |
| `30` | more than 265 parts | caller-defect |
| `31` | invalid JSON | caller-defect |
| `33` | subscriber blocked this sender (opt-out, «لغو ۱۱») | recipient-terminal; record an opt-out suppression for this line |
| `34` | no verified information for this sender number | account |
| `35` | invalid character in text | caller-defect |
| `101`–`110` | array length mismatch, empty arrays, too many recipients | caller-defect |
