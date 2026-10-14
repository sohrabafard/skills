[CmdletBinding()]
param(
  [string]$VaultPath = ""
)

# Nonwriting compatibility hook. VaultPath remains accepted but is intentionally
# unused. No payload, transcript, environment, git or vault content is read.
# Exit 0 and legacy JSON fields are retained. Current Claude Code discards
# PreCompact systemMessage/continue; this output guarantees no context injection.
# See references/checkers-and-hooks.md for the official hook protocol.
@{
  systemMessage = 'Before active-task compaction, use /alaa-workflow for its checkpoint and handoff.'
  continue = $true
} | ConvertTo-Json -Compress
exit 0
