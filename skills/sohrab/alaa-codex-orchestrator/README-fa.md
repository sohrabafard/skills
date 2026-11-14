# بسته نهایی Alaa Codex Orchestrator

نسخه: **4.0.0**

این بسته یک Skill کامل برای تبدیل Codex اصلی به orchestrator و مسیردهی subagentهای تخصصی با نصب مجاز و صریح است.

## ویژگی‌های اصلی

- ارائهٔ ۲۲ نقش و یک profile مستقل برای deep review؛ نصب و به‌روزرسانی فقط با مجوز صریح در `~/.codex/agents`
- جایگزینی کامل نسخه قبلی agentهای هم‌نام، بدون نگه‌داشتن backup یا هیچ کپی از نسخه قدیمی
- عدم تغییر agentها و تنظیمات دیگر کاربر
- تفکیک implementation، verification، diagnosis، review و documentation
- specialist gate برای architecture، security، migration، browser QA، performance، observability و release
- اجرای تست‌های سنگین با اولویت `BelowNormal` (معادل `nice`) در WSL
- پشتیبانی از محدودیت CPU، timeout و artifact directory
- حفظ اجباری آرگومان `--browser chromium`
- review مستقل و حداکثر دو چرخه اصلاح
- اتصال skill های اکوسیستم Alaa به نقش‌های security و migration و observability و release و performance و browser QA
- مسیردهی کارهای چندفازی durable به /alaa-workflow

## نصب Skill

پس از دریافت مجوز صریح نصب، بستهٔ کامل را کنار `alaa-prompting-guide` قرار بده. سپس این دستور Bash را اجرا کن:

```bash
./alaa-codex-orchestrator/scripts/install-skill.sh
```

این دستور Skill را در مسیر زیر نصب می‌کند:

```text
~/.codex/skills/alaa-codex-orchestrator
```

سپس Codex را اجرا و Skill را صدا بزن:

```text
/alaa-codex-orchestrator
```

Activation inspects roles only. An explicitly authorized installer validates model-neutral roles, wrappers, manifests and resolved MCP grants before writing the TOML files to the following path:

```text
~/.codex/agents
```

به دلیل محافظت sandbox از مسیرهای خارج workspace، ممکن است Codex برای اجرای installer یک approval محدود درخواست کند. این installer فقط فایل‌های agent همین بسته را مدیریت می‌کند.

## نقش‌ها

### هسته

- `alaa-explorer`
- `alaa-researcher`
- `alaa-test-strategist`
- `alaa-implementer`
- `alaa-implementer-astra`
- `alaa-implementer-laravel`
- `alaa-implementer-frontend`
- `alaa-implementer-go`
- `alaa-implementer-infra`
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

Role triggers and actual task model AND effort allocation are owned by `references/routing-matrix.md`. `/alaa-prompting-guide` supplies capabilities and runtime mechanics. All roles are model-neutral; installation and source-versus-session activation are documented in `references/installation.md`.

## قرارداد گزارش نسخهٔ جدید

در نقش‌های دارای verdict، گزارش با verdict شروع می‌شود. تنظیم‌های configured/requested جدا از هویت observed گزارش می‌شوند. مقدار غیرقابل‌مشاهده `unknown` است. profile استاندارد و deep برای یک scope هم‌زمان اجرا نمی‌شوند. نبود مدل یا نقش، fallback پنهانی یا مجوز نصب ایجاد نمی‌کند.

## تست نصب

```bash
python3 ~/.codex/skills/alaa-codex-orchestrator/scripts/check_agent_grants.py --resolved-agents-dir ~/.codex/agents
```

این دستور هر فایل `*.toml` در آن مسیر را می‌خواند و سه چیز را بررسی می‌کند:

- مجموعهٔ نام agentها باید با کاتالوگ برابر باشد. نبود یک نقش یا وجود یک agent مدیریت‌نشده، دستور را `FAILED` می‌کند.
- هر نقش لازم است اعلان `sandbox_mode` موردنیاز خود را داشته باشد.
- هر override در `mcp_servers` باید با inventory زندهٔ MCP و grant کاتالوگ همان نقش یکی باشد.

کد خروج `0` یعنی سالم، `1` یعنی یافته، و `2` یعنی دستور اجرا نشد.

این دستور فایل نصب‌شده را با منبع مقایسه نمی‌کند. وضعیت Current یا Different هر agent را گزارش نمی‌دهد. پس drift در محتوای خارج از فیلدهای بالا دیده نمی‌شود. برای دیدن آن، خروجی `check_agent_grants.py --materialize agents <پوشهٔ-خالی-جدید>` را با فایل‌های نصب‌شده مقایسه کن. این دستور در دسترس‌بودن مدل یا هویت runtime را هم ثابت نمی‌کند.

## اجرای تست با اولویت پایین

نمونه Go:

```bash
bash ~/.codex/skills/alaa-codex-orchestrator/scripts/run-low-priority.sh \
  --priority BelowNormal --cpu-count 2 -- \
  env GOMAXPROCS=2 go test -p 1 -parallel 2 -count=1 ./...
```

فقط پایین آوردن priority کافی نیست؛ concurrency داخلی test runner نیز باید جداگانه محدود شود.
