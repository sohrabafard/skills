# Multi-agent setup

This skill is designed to work well with Codex multi-agent workflows.

## Why split the work

The player feature set is broad enough that parallel agents can reduce total
implementation time and keep each agent focused:

- core playback
- ads
- analytics
- overlays
- conductor
- QA

That focus reduces context drift and makes the final merge easier.

## Enabling multi-agent mode

Enable the experimental feature in Codex and restart the session.

You can also enable it in your Codex config via the `multi_agent` feature flag.

## Recommended role layout

Use role descriptions that are narrow and concrete.

Recommended roles:

- `core`
- `ads`
- `analytics`
- `overlay`
- `conductor`
- `qa`

See `assets/config-examples/` for sample role files.

## Suggested operating pattern

1. Ask the parent agent to spawn one sub-agent per track
2. Let each agent work independently
3. Wait for all results
4. Consolidate architecture and code
5. Run a final QA pass

## Sandbox suggestion

Mark exploration-oriented roles as read-only if they do not need to write code.
Keep implementation roles writable.
