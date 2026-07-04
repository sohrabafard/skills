# CLI And MCP

## Correct CLI commands

```powershell
bm status --project alaa-memory --wait --timeout 60
bm reindex -p alaa-memory
bm doctor
bm schema validate <type> --project alaa-memory
bm format --project alaa-memory
bm orphans --project alaa-memory
bm schema diff <type> --project alaa-memory
```

Do not use unsupported:

```powershell
basic-memory sync
```

## Search and context

```powershell
bm tool search-notes "rabbitmq notification contract" --hybrid --project alaa-memory
bm tool search-notes --type drift --meta drift_status=open --project alaa-memory
bm tool search-notes --status needs_review --project alaa-memory
bm tool build-context memory://alaa-rabbitmq-messaging-contracts --project alaa-memory
bm tool read-note memory://alaa-rabbitmq-messaging-contracts --include-frontmatter --project alaa-memory
bm tool recent-activity --timeframe 7d --project alaa-memory
```

## HTTP MCP for Codex app/desktop

```powershell
bm mcp --project alaa-memory --transport streamable-http --host 127.0.0.1 --port 8000
```

Server URL:

```text
http://localhost:8000/mcp
```

## Codex CLI

```powershell
codex mcp add basic-memory bash -c "uvx basic-memory mcp --project alaa-memory"
```
