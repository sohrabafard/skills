# راهنمای فارسی skill های Alaa

این فایل فهرست راهنمای skill های شخصی است تا بدانید هر کدام برای چه کاری است و کِی باید سراغش بروید. زبان مرجع هر skill انگلیسی است؛ این سند فقط نقشه راه است.

**نحوه فراخوانی:** در Claude Code با `/نام-skill` و در Codex با `$نام-skill`. هر skill که هر دو runtime را پوشش می‌دهد، هر دو شکل را داخل خودش اعلام کرده است.

---

## ۱. دکترین و استانداردهای مشترک

این‌ها پایه‌اند و بقیه به آن‌ها ارجاع می‌دهند. اگر قاعده‌ای در دو جا تعریف شده باشد، مالک اصلی همین دسته است.

| Skill | برای چه کاری | کِی سراغش بروید |
|---|---|---|
| `alaa-project-constitution` | ساخت و نگهداری `CONSTITUTION.md` هر پروژه و بستن آن به `AGENTS.md` و `CLAUDE.md`. **مالک نوار کیفیت ده‌گانه** و **لایه archetype** که خودش تشخیص می‌دهد یک پروژه چه الزاماتی دارد | شروع یک سرویس جدید، یا وقتی سند RFP یا دانش تازه‌ای دارید که باید وارد قانون اساسی شود |
| `alaa-services-contract` | قرارداد سخت بین microservice ها: پاکت خطا، نام رویدادها، هدرها، شناسه‌ها، مسیرها، مقادیر timeout و pool مخصوص Alaa، و قاعده deprecation | هر تغییری که سطح مشترک بین دو سرویس را جابه‌جا می‌کند |
| `alaa-reliability-sla` | دکترین پایداری، مستقل از زبان: deadline، retry با backoff، circuit breaker، backpressure، load shedding، idempotency، error budget، تخریب تدریجی | طراحی رفتار سیستم در خطا و زیر بار — عددهای Alaa در `alaa-services-contract` است |
| `alaa-security-review` | بازبینی امنیتی: مرزهای اعتماد، authn و authz، جداسازی tenant، ورودی نامعتمد، SSRF، آپلود، رمزنگاری، و دکترین fail-closed | هر تغییری که مرز اعتماد یا دسترسی را جابه‌جا می‌کند |
| `alaa-observability-soc` | سطح الزام و gate های telemetry: انتخاب سیگنال، بودجه cardinality، مرز histogram، sampling، burn-rate، شواهد SOC | افزودن یا تغییر سیگنال، هشدار، یا مسیر telemetry |
| `alaa-controlled-ops` | مرز مالکیت بین package `alaa/controlled-ops` و سرویس مصرف‌کننده، و انتشار آن روی Satis | کار روی همان package یا سرویسی که آن را adopt کرده |
| `service-runtime-kit-governance` | اینکه یک تغییر runtime در کدام لایه می‌نشیند و چرا، و دیباگ اختلاف بین خروجی تولیدشده و ورودی‌هایش | تغییر `runtime/*`، فایل‌های تولیدشده Compose، یا pin کردن نسخه kit |
| `alaa-prompting-guide` | **تنها مرجع مدل و effort.** نوشتن prompt، skill، تعریف agent، و فایل‌های `AGENTS.md`/`CLAUDE.md` | هر سوالی درباره انتخاب مدل، سطح تلاش، یا نوشتن skill |
| `alaa-low-noise` | صرفه‌جویی در context و نظم خروجی، در هر دو runtime | کارهای طولانی که خروجی پرگو تولید می‌کنند |
| `alaa-workflow` | برنامه‌ریزی کارهای چندفازی با فایل plan و state که از compaction و تحویل جان سالم ببرد | کاری که در یک نشست تمام نمی‌شود |
| `alaa-system-design` | روش طراحی یک سرویس یا زیرسیستم **پیش از** پیاده‌سازی: مرزبندی، قرارداد قبل از کد، مالکیت داده، و انتخاب بین چند طرح | قبل از نوشتن کدی که مرز، قرارداد، یا مالکیت داده را جابه‌جا می‌کند |
| `alaa-testing-strategy` | طراحی تست: لایه‌ها، test double ها، شش سطح قدرت اثبات، کنترل flake، و پوشش | تصمیم‌گیری درباره اینکه چه چیزی و در کدام لایه تست شود |
| `alaa-algorithms-data-structures` | بودجه پیچیدگی، پیدا کردن کران واقعی ورودی، انتخاب ساختار داده از روی الگوی دسترسی، و خانواده N+1 | مسیری که ورودی‌اش با تعداد کاربر، تاریخچه یا fan-out رشد می‌کند |
| `alaa-keyset-pagination` | طراحی pagination مبتنی بر cursor: ترتیب قطعی با tie-breaker، ایندکس متناظر، امضا و اعتبارسنجی cursor، و استثنای offset برای جدول‌های ادمین | هر route لیستی که کلاینت صفحه‌به‌صفحه می‌خواند |

## ۲. هدایت چند-agent

| Skill | برای چه کاری |
|---|---|
| `alaa-cc-orchestrator` | هدایت چند-agent در Claude Code با ۲۱ نقش، دروازه‌های تایید و بازبینی مستقل |
| `alaa-codex-orchestrator` | همان چیز برای Codex |
| `alaa-codex-runtime-ops` | بازیابی از خطاهای runtime در Codex و ویندوز |
| `alaa-basic-memory-os` | حافظه بین‌نشستی روی Basic Memory و Obsidian |

## ۳. PHP و Laravel

| Skill | برای چه کاری |
|---|---|
| `alaa-php-clean-code` | کد تمیز، SOLID، الگوهای طراحی و بوی کد در PHP |
| `alaa-laravel-architecture` | معماری لایه‌ای، سرویس‌ها و ساختار پروژه Laravel |
| `alaa-octane-performance` | کارایی و ایزولاسیون state زیر Octane |
| `alaa-laravel-job-rabbitmq` | job و queue روی RabbitMQ در Laravel |
| `alaa-laravel-public-api-contract-pack` | قرارداد API عمومی و آمادگی SDK |
| `alaa-laravel-upgrade-all-packages` | ارتقای امن همه package ها |
| `alaa-cicd-laravel-postgres` | خط CI/CD قطعی برای سرویس Laravel با Postgres |
| `alaa-permission-generator` | تولید کاتالوگ دسترسی‌ها |

## ۴. Go

| Skill | برای چه کاری |
|---|---|
| `alaa-golang` | نقطه ورود Go و مسیریابی به ۴۶ skill بالادستی `golang-*` |
| `alaa-golang-clean-code-principles` | کد تمیز Go در عصر kit، و مرز اعتماد |
| `alaa-golang-fiber` | سرویس Go روی Fiber |
| `alaa-go-chi-development` | سرویس Go روی chi و قالب‌های kit |

> ۴۶ skill با پیشوند `golang-*` از upstream می‌آیند و زیر `vendor/` هستند. **هرگز ویرایش نشوند** — چهار skill بالا به آن‌ها ارجاع می‌دهند.

## ۵. داده و ذخیره‌سازی

| Skill | برای چه کاری |
|---|---|
| `alaa-data-layer` | الگوی repository، Redis، و مرزهای لایه داده |
| `alaa-mongodb-patterns` | طراحی سند و الگوهای MongoDB |
| `alaa-partitioned-table-fk-audit` | جدول partition شده و بازبینی کلید خارجی |
| `alaa-crockford-base32-codecs` | کدگذاری شناسه با Crockford Base32 |
| `clickhouse-performance-schema-ops` | کارایی و schema در ClickHouse |

## ۶. Frontend

| Skill | برای چه کاری |
|---|---|
| `alaa-frontend-developer` | نقطه ورود frontend: SSR، PWA، کارایی و دیباگ مرورگر |
| `alaa-vue-typescript-clean-code` | کد تمیز Vue و TypeScript |
| `alaa-quasar-app-vite-v3` | پروژه Quasar روی Vite |
| `alaa-ui-ux-design-system` | سیستم طراحی و حاکمیت کتابخانه کامپوننت |
| `alaa-frontend-devops` | CI و Docker مخصوص frontend |
| `alaa-frontend-doc-annotations` | مستندسازی درون‌کد frontend |
| `alaa-mono-package` | ساخت و انتشار package در mono-repo |
| `alaa-indexeddb-browser-storage` | ذخیره‌سازی سمت مرورگر |
| `alaa-shaka-player` | پخش ویدیو با Shaka |

## ۷. زیرساخت و تحویل

| Skill | برای چه کاری |
|---|---|
| `alaa-docker-production` | Dockerfile و Compose آماده production |
| `alaa-k8s-helm` | manifest و chart برای Kubernetes |
| `alaa-gitlab-ci-cd` | خط لوله GitLab |
| `alaa-haproxy` | پیکربندی HAProxy |
| `alaa-makefile` | Makefile و هدف‌های تکرارشدنی |
| `caas-arvan-kuber` | Kubernetes روی ابر آروان |
| `ansible-generator` / `ansible-validator` | تولید و اعتبارسنجی playbook |
| `alaa-bash-shell` | نوشتن و اعتبارسنجی اسکریپت Bash و POSIX |

## ۸. پیام‌رسانی، یکپارچه‌سازی و اعتماد

| Skill | برای چه کاری |
|---|---|
| `alaa-async-messaging` | معماری async: Kafka برای رویداد، RabbitMQ برای job |
| `alaa-trust-gateway-auth` | صدور و اعتبارسنجی token و هدرهای معتمد در gateway |
| `alaa-bale-provider` | یکپارچه‌سازی با پیام‌رسان بله |
| `alaa-sms-provider-mediana` | ارسال پیامک با مدیانا |
| `tusd-upload-platform` | آپلود resumable با tusd |
| `jitsi-platform-architect` | معماری پلتفرم Jitsi |

## ۹. رصدپذیری، مستندات و دانش

| Skill | برای چه کاری |
|---|---|
| `alaa-signoz-clickhouse-docs` | جستجوی مستندات SigNoz و کوئری ClickHouse |
| `vector-rust-observability-pipelines` | خط لوله Vector |
| `alaa-postman-collections` | ساخت و اعتبارسنجی collection و environment در Postman، و دکترین collection تجمیعی چند-سرویسی |
| `alaa-docs-farsi` | نگارش مستندات فارسی |

---

## قواعدی که همیشه برقرارند

**مالکیت یکتا.** هر قاعده فقط یک مالک دارد. اگر دو skill یک چیز را گفتند، یکی از آن‌ها اشتباه است — گزارش دهید.

**نام و مقدار در برابر سطح الزام.** در حوزه telemetry، نام‌ها و مقادیر مال `alaa-services-contract` است و سطح الزام و gate ها مال `alaa-observability-soc`. اگر این دو اختلاف داشتند: روی «آیا الزامی است» دومی برنده است، روی «اسمش چیست» اولی.

**قرارداد در برابر مکانیزم.** نام‌های canonical زیرساخت مشترک و الزام reuse مال `alaa-services-contract` است؛ اینکه کدام متغیر generator آن را بیان می‌کند مال `service-runtime-kit-governance`.

**fail-closed در برابر fail-open.** کنترلی که تصمیم می‌گیرد آیا کسی مجاز است — وقتی نمی‌تواند تصمیم بگیرد **رد می‌کند** و مالکش `alaa-security-review` است. مؤلفه‌ای که فقط مشارکت می‌کند — وقتی از کار می‌افتد **راه را باز می‌گذارد** و مالکش `alaa-reliability-sla` است. این دو عمداً متناقض‌اند و سوال تعیین‌کننده این است: اگر بدون این مؤلفه ادامه دهیم، چیزی که نباید عبور کند عبور می‌کند؟

**مدل و effort.** هیچ skill دیگری نام مدل نمی‌گوید. همه به `alaa-prompting-guide` ارجاع می‌دهند.

**پوشه vendor.** هر چیزی زیر `vendor/` از upstream می‌آید و ویرایش نمی‌شود. skill خودی آن را می‌پوشاند و به آن ارجاع می‌دهد.
