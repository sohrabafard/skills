[CmdletBinding()]
param(
  [string]$Project = "alaa-memory"
)

# SessionStart hook: injects a short governance reminder into the new session's
# context so every agent starts with the Basic Memory operating rules.
# Output on stdout is added to the session context by Claude Code.

$ErrorActionPreference = "SilentlyContinue"

$driftCount = ""
if (Get-Command bm -ErrorAction SilentlyContinue) {
  $driftJson = & bm tool search-notes --type drift --project $Project --page-size 5 2>$null
  if ($LASTEXITCODE -eq 0 -and $driftJson) {
    $driftCount = "Open drift notes may exist in Basic Memory (type=drift). If your task touches an affected contract, read them first."
  }
}

@"
Alaa Basic Memory governance (auto-injected):
- Basic Memory project: $Project. Repo code/docs are source of truth; memory is the map.
- For non-trivial / cross-service / contract-sensitive / continuation work: search Basic Memory BEFORE planning (project, service, contract names, decisions, lessons, handoffs), then verify against repo files.
- Never store secrets, raw logs, transcripts, full docs, or active alaa-workflow checklists in memory.
- Contract facts must be source-backed (Extraction Mode). Proposals need [proposal]/[draft_contract]/[decision_needed] labels (Design Mode, only when asked).
- If memory and repo truth disagree, record a drift note (type: drift, folder drift/) instead of silently picking one.
- Health commands: bm status --project $Project --wait --timeout 60 | bm reindex -p $Project | bm doctor | bm schema validate <type> --project $Project. Never use 'basic-memory sync'.
$driftCount
"@

exit 0
