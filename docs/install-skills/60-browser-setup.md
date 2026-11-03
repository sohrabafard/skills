# Set up browser tools

## Install browser tools

```bash
mkdir -p ~/.playwright-mcp-profile
npm install playwright
npx playwright install chromium
npm install -g -D @axe-core/playwright
npx @playwright/mcp@latest --port 8931 --browser chromium --user-data-dir ~/.playwright-mcp-profile
```

Codex config: substitute your own home directory for `USER_HOME` below. Codex reads this file as
TOML and does not expand an environment variable inside it, so the path has to be absolute.

```toml
[mcp_servers.playwright_visual]
command = "npx"
args = [
  "-y",
  "@playwright/mcp@latest",
  "--browser",
  "chromium",
  "--user-data-dir",
  "USER_HOME/.playwright-mcp-profile"
]
startup_timeout_sec = 60
tool_timeout_sec = 300
enabled = true
```
