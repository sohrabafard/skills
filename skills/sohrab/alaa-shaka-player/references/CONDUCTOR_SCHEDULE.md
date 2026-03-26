# Playback conductor and TV-like scheduling

## What this solves

Some products need more than a simple playlist. They need playback that follows
a wall-clock schedule, similar to a TV channel.

## Recommended schedule model

```ts
type ScheduleItem = {
  id: string
  startAtIso: string
  endAtIso?: string
  media: MediaItem
  startOffsetSec?: number
}
```

## Switching logic

At each tick:

1. evaluate which schedule item is active for the current wall-clock time
2. if the active item changed, compute the source offset
3. load the correct manifest and start at the computed position

## Offset formula

A practical offset is:

- `startOffsetSec + (now - startAtIso)`

## UX upgrades

If you need smoother switching, consider:

- preloading the next item
- using a two-player strategy in advanced cases
- fallback content if the new item fails to load
