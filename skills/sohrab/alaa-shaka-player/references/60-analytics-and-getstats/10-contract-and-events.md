For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## The seam — read this before naming anything

**This skill states which *quantities* playback can produce. It defines no name.** Every event name,
field name and metric name is requested from `/alaa-services-contract`, `references/24-metric-registry.md` and
`references/20-operational-and-observability-contract.md`. Requirement levels and gates are
`/alaa-observability-soc`. A payload shape invented in a player file is a
defect regardless of how reasonable it looks.

**Two pipeline facts bound any claim you make about a count.** The WA tables `wa_raw.events_raw` and
`wa_raw.watch_segments_raw` already exist with a settled schema, monthly partitions and `project_id`
first in `ORDER BY`.

- Sinks retry **20×** against a plain `MergeTree` with block deduplication **off**, so `count()` is an
  **upper** bound. A player event carrying no idempotency key makes over-count *structural*, not
  incidental.
- Vector's disk buffer sits on an `emptyDir` with one replica, so buffered events are **lost on pod
  replacement after clients were told `202`**, making `count()` also a **lower** bound.

So no dashboard built on these tables may state a playback count as exact. Emit an idempotency key
with every playback event (the key's **name** comes from the contract), and write the two bounds into
any figure derived from them.


## Events available for analytics

`buffering` (`buffering: boolean`) · `stalldetected` · `gapjumped` · `adaptation`
(`oldTrack`, `newTrack`; **automatic**) · `variantchanged` (**app-initiated**) · `textchanged` ·
`trackschanged` · `audiotrackschanged` · `audiotrackchanged` · `abrstatuschanged` (`newStatus`) ·
`error` (`detail`) · `statechanged` (`newstate`) · `onstatechange` (`state`) · `ratechange` ·
`loading` / `loaded` / `unloading` (`isSwitchingContent`) · `manifestparsed` / `streaming` /
`manifestupdated` · `downloadcompleted` (`requestType`, `request`, `context`, `response`) ·
`downloadfailed` (`requestType`, `request`, `context`, `error`, `httpResponseCode`, `aborted`) ·
`downloadheadersreceived` · `segmentappended` (`start`, `end`, `contentType`, `isMuxed`,
`isDependency`, **`mediaTimestamp`** new in 5.2.0, `null` if unparseable) · `mediaqualitychanged`
(only when `streaming.observeQualityChanges === true`) · `mediasourcerecovered` ·
`expirationupdated` / `keystatuschanged` / `drmsessionupdate` · `firstquartile` / `midpoint` /
`thirdquartile` / `complete` / `started` · and the specialised set `prft`, `emsg`, `metadata`,
`metadataadded`, `timelineregionadded`/`enter`/`exit`, `sessiondata`, `programinformation`,
`boundarycrossed`, `spatialvideoinfo`, `nospatialvideoinfo`, `canupdatestarttime`,
`configurationchanged`, `bufferappending`, `licenserenewal`.

`downloadfailed` is the best hook for CDN error telemetry — but record `requestType` and
`httpResponseCode`, **never `request.uris`**, which is a presigned credential
(`42-media-url-trust-and-presigned.md`).
