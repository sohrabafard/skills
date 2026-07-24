# بسته نهایی Alaa Codex Orchestrator

نسخه: **2.1.0**

این بسته یک Skill کامل برای تبدیل Codex اصلی به orchestrator و نصب خودکار subagentهای تخصصی است.

## ویژگی‌های اصلی

- نصب و به‌روزرسانی خودکار ۲۱ subagent داخل `~/.codex/agents`
- backup گرفتن از نسخه قبلی agentهای هم‌نام
- عدم تغییر agentها و تنظیمات دیگر کاربر
- تفکیک implementation، verification، diagnosis، review و documentation
- specialist gate برای architecture، security، migration، browser QA، performance، observability و release
- اجرای تست‌های سنگین با اولویت `BelowNormal` در Windows
- پشتیبانی از محدودیت CPU، timeout و artifact directory
- حفظ اجباری آرگومان `--browser chromium`
- review مستقل و حداکثر دو چرخه اصلاح
- اتصال skill های اکوسیستم Alaa به نقش‌های security و migration و observability و release و performance و browser QA
- مسیردهی کارهای چندفازی durable به $alaa-workflow

## نصب Skill

بعد از Extract کردن ZIP، نصب یک‌مرحله‌ای در PowerShell:

```powershell
& ".\alaa-codex-orchestrator\scripts\Install-AlaaCodexOrchestrator.ps1"
```

این دستور Skill را در مسیر زیر نصب می‌کند:

```text
%USERPROFILE%\.codex\skills\alaa-codex-orchestrator
```

سپس Codex را اجرا و Skill را صدا بزن:

```text
$alaa-codex-orchestrator
```

در اولین activation، فایل‌های TOML به‌صورت خودکار در این مسیر نصب می‌شوند:

```text
%USERPROFILE%\.codex\agents
```

به دلیل محافظت sandbox از مسیرهای خارج workspace، ممکن است Codex برای اجرای installer یک approval محدود درخواست کند. این installer فقط فایل‌های agent همین بسته را مدیریت می‌کند.

## نقش‌ها

### هسته

- `alaa-explorer`
- `alaa-researcher`
- `alaa-test-strategist`
- `alaa-implementer`
- `alaa-implementer-sol`
- `alaa-verifier`
- `alaa-failure-analyst`
- `alaa-reviewer`
- `alaa-documenter`

### Specialist

- `alaa-architecture-critic`
- `alaa-security-reviewer`
- `alaa-migration-guardian`
- `alaa-browser-qa`
- `alaa-performance-profiler`
- `alaa-observability-reviewer`
- `alaa-release-guardian`

جزئیات trigger و مدل هر نقش در `references/agent-catalog.md` و `references/routing-matrix.md` قرار دارد.

## تست نصب

```powershell
& "$env:USERPROFILE\.codex\skills\alaa-codex-orchestrator\scripts\Get-AlaaCodexAgentStatus.ps1"
```

## اجرای تست با اولویت پایین

نمونه Go:

```powershell
$runner = "$env:USERPROFILE\.codex\skills\alaa-codex-orchestrator\scripts\Invoke-AlaaLowPriority.ps1"

& $runner `
  -Priority BelowNormal `
  -CpuCount 2 `
  -Environment @{ GOMAXPROCS = "2" } `
  -FilePath "go" `
  -ArgumentList @("test", "-p", "1", "-parallel", "2", "-count=1", "./...")
```

فقط پایین آوردن priority کافی نیست؛ concurrency داخلی test runner نیز باید جداگانه محدود شود.
