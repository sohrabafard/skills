# HLS notes

## HLS as the primary target

This skill assumes HLS is the main playback format. DASH can be added as a
secondary path if the product needs it.

## Practical integration concerns

### 1. CORS and signed URLs
If manifests, segments, or licenses require signed requests or custom headers,
register networking filters in the Shaka core wrapper.

### 2. Range requests
Make sure your origin or CDN correctly supports range requests and streaming
headers.

### 3. Codec signaling
Your HLS master playlist should expose codec information cleanly whenever
possible.

If codec information is missing, Chrome-family browsers can fail with chunk
demuxer append errors because the player must guess codecs.

### 4. Safari and iOS
Safari and iOS can behave differently from Chromium-based browsers, especially
around HLS playback behavior, ABR control, and autoplay policy. Test those
platforms explicitly.

The Shaka FAQ still states that iOS support relies on Apple's native HLS path,
so do not promise DASH-on-iOS parity or full MSE-level control there.

### 5. Live startup and drift
For short live playlists, default buffering assumptions may be too optimistic.
If live playback buffers between chunks, review `manifest.hls.liveSegmentsDelay`
and other low-latency settings before building a custom workaround.

### 6. Chapters and timed metadata
Shaka 5.1 adds or documents useful chapter and metadata surfaces, including
chapter images, external `chaptersUri`, and public timeline or EMSG region
functions. Use these for chapter menus, seek previews, MediaSession metadata,
and cuepoint overlays before inventing a custom parser.

### 7. Version-aware fixes
Current releases include fixes and performance improvements around live playlist
refresh, LL-HLS stalls, discontinuity sequence timeline sync, duplicate segment
detection, `audio/x-mpegurl`, and long DVR startup. Re-check release notes
before copying older live-HLS workarounds into a new project.

### 8. Error funnel
Do not let network and media errors vanish into the console. Forward them into
a structured error reporting path.

## Anti-patterns

- relying on `video.currentTime` as the only startup-position mechanism during
  initial attach or manifest startup
- mixing auth-header logic into unrelated UI code
- assuming Safari and Chromium HLS behavior are interchangeable
- cargo-culting old stream-switch or live-manifest workarounds without checking
  whether the current release already fixed the issue
