# ABR and track management

## Adaptive bitrate strategy

Use ABR by default. Let the player choose the best quality unless the product
explicitly asks for manual quality control.

For low-latency live or MoQ-style workloads, treat custom ABR strategies as an
advanced path. There is active upstream work on `BufferBasedAbrManager`, so do
not implement a bespoke ABR manager unless measurements clearly justify it.

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
- return to auto

## Telemetry

Whenever quality or track selection changes, send a structured analytics event.

## Anti-patterns

- disabling ABR globally just to make manual selection easier
- permanently forking Shaka ABR logic without a measured need
- treating subtitle visibility, subtitle language, and audio track choice as the
  same state machine
