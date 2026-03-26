# Timeline markers

## Supported marker types

This skill is designed to support:

- personal notes
- comments
- bookmarks
- share links tied to a timestamp

## Separation of concerns

Keep marker storage and marker UI separate.

The marker service should own:

- marker retrieval
- add or delete operations
- share URL construction

The UI layer should own:

- marker ticks on the timeline
- click interactions
- popovers or dialogs

## Share link pattern

A practical share URL pattern is:

- `/watch/<id>?t=123.4`

At initialization time:

- parse `t`
- apply it as the startup position through the player wrapper
