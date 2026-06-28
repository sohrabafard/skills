# ABR and track management

## Adaptive bitrate strategy

Use ABR by default. Let the player choose the best quality unless the product
explicitly asks for manual quality control.

For low-latency live or MoQ-style workloads, treat custom ABR strategies as an
advanced path. The 5.1 line gives ABR more information about low-latency streams
and dropped frames, so do not implement a bespoke ABR manager unless
measurements clearly justify it.

## 5.1 preference model

Use structured preference arrays in new or touched code:

- `preferredAudio`
- `preferredText`
- `preferredVideo`

Do not add new uses of old individual preference fields such as
`preferredAudioLanguage`, `preferredTextLanguage`, or `preferredVideoCodecs`.
They still work in 5.1 with deprecation warnings, but the official upgrade guide
says they will be removed in the next major version.

## Manual override

If the user manually selects a quality level:

- disable or constrain auto behavior in a controlled way
- expose a clear path back to Auto

## Track management

Support these track flows in the UI:

- audio track selection
- subtitle on or off
- subtitle language selection
- manual quality selection
- audio, text, and video preference fallback order
- return to auto

## Telemetry

Whenever quality or track selection changes, send a structured analytics event.

## Anti-patterns

- disabling ABR globally just to make manual selection easier
- permanently forking Shaka ABR logic without a measured need
- treating subtitle visibility, subtitle language, and audio track choice as the
  same state machine
