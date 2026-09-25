# بسته نهایی Alaa Codex Orchestrator

نسخه: **4.0.0**

این بسته یک Skill کامل برای تبدیل Codex اصلی به orchestrator و مسیردهی subagentهای تخصصی با نصب مجاز و صریح است.

## ویژگی‌های اصلی

- ارائهٔ ۲۲ نقش و یک profile مستقل برای deep review؛ نصب و به‌روزرسانی فقط با مجوز صریح در `~/.codex/agents`
- جایگزینی کامل نسخه قبلی agentهای هم‌نام، بدون نگه‌داشتن backup یا هیچ کپی از نسخه قدیمی
- عدم تغییر agentها و تنظیمات دیگر کاربر
- تفکیک implementation، verification، diagnosis، review و documentation
- specialist gate برای architecture، security، migration، browser QA، performance، observability و release
- اجرای تست‌های سنگین با اولویت `BelowNormal` در Windows
- پشتیبانی از محدودیت CPU، timeout و artifact directory
- حفظ اجباری آرگومان `--browser chromium`
- review مستقل و حداکثر دو چرخه اصلاح
- اتصال skill های اکوسیستم Alaa به نقش‌های security و migration و observability و release و performance و browser QA
- مسیردهی کارهای چندفازی durable به /alaa-workflow

## نصب Skill

پس از دریافت مجوز صریح نصب، بستهٔ کامل را کنار `alaa-prompting-guide` قرار بده. سپس این دستور PowerShell را اجرا کن:

```powershell
& ".\alaa-codex-orchestrator\scripts\Install-AlaaCodexOrchestrator.ps1"
```

این دستور Skill را در مسیر زیر نصب می‌کند:

```text
%USERPROFILE%\.codex\skills\alaa-codex-orchestrator
```

سپس Codex را اجرا و Skill را صدا بزن:

```text
/alaa-codex-orchestrator
```

با activation فقط وضعیت نقش‌ها بررسی می‌شود. نصب خودکار انجام نمی‌شود. installer مجاز، فایل‌های TOML را پس از بررسی pinها، wrapperها، manifest و materialization مجوزهای MCP در این مسیر می‌نویسد:

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
- `alaa-reviewer-deep`
- `alaa-instruction-reviewer`
- `alaa-documenter`

### Specialist

- `alaa-architecture-critic`
- `alaa-security-reviewer`
- `alaa-migration-guardian`
- `alaa-browser-qa`
- `alaa-performance-profiler`
- `alaa-observability-reviewer`
- `alaa-release-guardian`

جزئیات نقش‌ها و triggerها در `references/agent-catalog.md` و `references/routing-matrix.md` قرار دارد. مالک مدل و effort، مهارت `/alaa-prompting-guide` است. راهنمای انگلیسی نصب و ارتقا در `references/installation.md` قرار دارد.

## قرارداد گزارش نسخهٔ جدید

در نقش‌های دارای verdict، گزارش با verdict شروع می‌شود. تنظیم‌های configured/requested جدا از هویت observed گزارش می‌شوند. مقدار غیرقابل‌مشاهده `unknown` است. profile استاندارد و deep برای یک scope هم‌زمان اجرا نمی‌شوند. نبود مدل یا نقش، fallback پنهانی یا مجوز نصب ایجاد نمی‌کند.

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
