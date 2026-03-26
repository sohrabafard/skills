# Playlist support

## Two common playlist modes

### 1. Sequential playlist
A simple list of sources played one after another.

Recommended behavior:
- when content ends, load the next item
- preserve analytics and state boundaries clearly

### 2. Conductor-driven playback
A wall-clock controlled flow where the active source is determined by the
schedule rather than by content end events.

## Recommendation

Start with sequential playlist support first. Add the playback conductor only if
the product truly needs TV-like behavior.
