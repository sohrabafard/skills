For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## Mapping a code to a user-facing message

Map on **code**, never on `message` — the compiled build's message is only `'Shaka Error <code>'`.
Keep the mapping in one table with an explicit default, so a code you have never seen still produces
a sensible message rather than an empty string. Message copy is `/alaa-ui-ux-design-system`, `references/35-ux-writing-and-microcopy.md`; failure-state design is
`references/15-designed-failure-states.md` there.

**Best practice.** Check `instanceof Error` *before* treating something as a `shaka.util.Error` —
Shaka designed the runtime prototype chain specifically to make that check meaningful.
**Common mistake.** Only listening to `player.addEventListener('error', …)`. Load-time failures reject
the `load()` promise and never reach that listener, so the most common failure in production —
a 404 or an unsupported manifest — is the one path with no handler.
