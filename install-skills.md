#git clone https://github.com/openai/skills.git

$srcRoot = "D:\Sohrab\Project\skills\skills\.curated"
$dstRoot = "$HOME\.codex\skills"

New-Item -ItemType Directory -Force -Path $dstRoot | Out-Null

Get-ChildItem $srcRoot -Directory | ForEach-Object {
    $linkPath = Join-Path $dstRoot $_.Name
    if (-not (Test-Path $linkPath)) {
        New-Item -ItemType SymbolicLink -Path $linkPath -Target $_.FullName | Out-Null
        Write-Host "Linked: $($_.Name)"
    } else {
        Write-Host "Exists: $($_.Name)"
    }
}


## install browser:
New-Item -ItemType Directory -Force -Path "C:\Users\CIT\.playwright-mcp-profile" | Out-Null
npm install playwright
npx playwright install chromium
npm install -g -D @axe-core/playwright
npx @playwright/mcp@latest --port 8931 --browser chromium --user-data-dir "C:\Users\CIT\.playwright-mcp-profile"

codex config:
```
[mcp_servers.playwright_visual]
command = "npx"
args = [
  "-y",
  "@playwright/mcp@latest",
  "--browser",
  "chromium",
  "--user-data-dir",
  "C:\\Users\\CIT\\.playwright-mcp-profile"
]
startup_timeout_sec = 60
tool_timeout_sec = 300
enabled = true
```