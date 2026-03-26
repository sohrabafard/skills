# Watch-time analytics and interaction monitoring

## What counts as watch-time

Count watch-time only when content is genuinely being watched.

A practical baseline is:

- the video is playing
- the content is not buffering
- the user is not seeking
- the tab is not hidden, if your policy excludes hidden time
- an ad is not currently playing

## Heartbeat design

Send a heartbeat every 10 to 15 seconds with at least:

- content ID
- playback position
- watched delta
- playback rate
- mute and volume state
- quality or QoE snapshot
- ad state
- timestamp

## Interaction events

Track at minimum:

- play
- pause
- seek start and end
- rate change
- subtitle toggle or track change
- quality selection
- fullscreen transitions
- hard errors

## QoE snapshot ideas

If available from player stats, record:

- estimated bandwidth
- video resolution
- dropped frames
- buffering count or duration
- startup time

## Hidden tab policy

Decide early whether hidden-tab playback counts as watch-time. This should be a
product-level decision, not an accidental implementation detail.
