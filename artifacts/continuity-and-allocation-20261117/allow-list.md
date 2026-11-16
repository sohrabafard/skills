# Project allow-list for bd, as read on 2026-11-17

Source: `.claude/settings.json` `permissions.allow` of this repository. Read-only record; no setting was changed.

- `Bash(bd where *))`
- `Bash(bd version *))`
- `Bash(bd prime *))`
- `Bash(bd ready *))`
- `Bash(bd list *))`
- `Bash(bd show *))`
- `Bash(bd blocked *))`
- `Bash(bd create *))`
- `Bash(bd update *))`
- `Bash(bd close *))`
- `Bash(bd ping *))`
- `Bash(bd lint *))`
- `Bash(bd stale *))`
- `Bash(bd --sandbox --actor * create *))`
- `Bash(bd --sandbox --actor * update *))`
- `Bash(bd --sandbox --actor * close *))`

Not covered, so a lane may be asked for permission: `bd comments add`, `bd reclaim`, `bd dep add`, `bd unclaim`, `bd heartbeat`, and `bd --sandbox --actor <actor> comments add`.
