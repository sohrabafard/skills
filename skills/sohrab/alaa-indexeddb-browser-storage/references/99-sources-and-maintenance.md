# Sources and maintenance

Last researched: 2026-06-29.

## Authoritative sources consulted

### IndexedDB API and semantics

- MDN IndexedDB API: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API
- MDN Using IndexedDB: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
- W3C Indexed Database API 3.0: https://www.w3.org/TR/IndexedDB/

### Browser storage quota, persistence, and eviction

- MDN Storage quotas and eviction criteria: https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria
- web.dev Storage for the web: https://web.dev/articles/storage-for-the-web
- WebKit Updates to Storage Policy: https://webkit.org/blog/14403/updates-to-storage-policy/

### Browser support and newer/experimental APIs

- Can I Use IndexedDB API: https://caniuse.com/mdn-api_indexeddb
- MDN Window.indexedDB: https://developer.mozilla.org/en-US/docs/Web/API/Window/indexedDB
- MDN IDBTransaction.durability: https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability
- Chrome Developers: IndexedDB default durability mode change: https://developer.chrome.com/blog/indexeddb-durability-mode-now-defaults-to-relaxed
- Chrome Developers: More efficient IndexedDB storage in Chrome: https://developer.chrome.com/docs/chromium/indexeddb-storage-improvements
- MDN IDBObjectStore.getAllKeys: https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore/getAllKeys
- MDN IDBObjectStore.getAllRecords: https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore/getAllRecords

### Skill/prompt authoring sources

- OpenAI Prompt engineering guide: https://developers.openai.com/api/docs/guides/prompt-engineering
- OpenAI GPT-5 prompting guide: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
- Anthropic Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Anthropic Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Claims embedded in this skill

- IndexedDB is a low-level async API for significant structured client-side data, including files/blobs; it uses indexes and follows same-origin policy.
- Browser storage quotas and eviction differ between browsers and apply at origin/storage-bucket level.
- Best-effort storage is default; persistent storage can be requested with the Storage API where supported.
- Private browsing modes may apply different quotas and usually delete stored data at session end.
- Firefox, Chromium, and WebKit have different quota rules.
- Safari/WebKit has proactive eviction behavior under tracking-prevention conditions and different browser-app vs embedded-app quotas in modern versions.
- `navigator.storage.estimate()` is an estimate, not an exact guarantee.
- `QuotaExceededError` must be handled.
- `getAllRecords()` is experimental/limited and must not be required for production.
- Chrome changed IndexedDB default readwrite durability to relaxed from Chrome 121.
- Skills should be concise, well-structured, and route heavy context to references.

## Maintenance schedule

Refresh this pack when:

- every 6 months for browser compatibility/quota facts
- Safari/iOS/WebKit releases change storage policy
- Chrome/Edge/Firefox change durability/quota/storage-bucket behavior
- IndexedDB 3.0 or related APIs reach new Baseline status
- Alaa frontend architecture changes storage ownership or service boundaries
- a production incident reveals a browser-specific IndexedDB failure

## Maintenance workflow

1. Search official sources first.
2. Update source list with date.
3. Update compatibility and quota references.
4. Update examples if API recommendations change.
5. Run `python scripts/validate_skill_pack.py`.
6. Run a grep for prohibited storage of secrets in examples.
7. Test the skill on realistic prompts:
   - design an outbox
   - fix a migration bug
   - audit quota handling
   - review token storage proposal
   - plan Safari/iOS offline support

## Known uncertainty

Browser vendors intentionally pad/alter quota estimates to reduce fingerprinting. Exact storage capacity cannot be guaranteed by documentation alone. Agents should design probes, fallback tiers, and cleanup paths instead of promising exact byte availability.
