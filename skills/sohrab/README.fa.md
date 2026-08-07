# راهنمای فارسی skill های Alaa

این فایل فهرست راهنمای skill های شخصی است تا بدانید هر کدام برای چه کاری است و کِی باید سراغش بروید. زبان مرجع هر skill انگلیسی است؛ این سند فقط نقشه راه است.

**نحوه فراخوانی:** در Claude Code با `/نام-skill` و در Codex با `$نام-skill`. هر skill که هر دو runtime را پوشش می‌دهد، هر دو شکل را داخل خودش اعلام کرده است.

---

## قواعد طراحی این pack

- یک agent در Codex فقط skill ای را می‌تواند بار کند که `agents/openai.yaml` داشته باشد، و هر ۶۹ پوشه skill از ۶۹ پوشه اینجا این فایل را دارند؛ این وضعیت با `python scripts\check_skill_index.py` بررسی شده است.
- هیچ skill ای نام مدل نمی‌گوید؛ هر سوال مدل و effort و توان runtime به `alaa-prompting-guide` می‌رود.
- سطح‌های بالغ یک مالک routing-first دارند، نه چند skill ریز و تقریبا تکراری.
- skill های همراه جایی صریح می‌مانند که مرز مالکیت هنوز اهمیت دارد.
- فایل `AGENTS.md` همین پوشه مالک نحوه نوشتن و ساختاردهی یک skill است و این سند آن را تکرار نمی‌کند.

### نشانه‌گذاری مسیر در یک ارجاع

مسیری که داخل یک skill نوشته می‌شود یا به فایلی اشاره دارد که با همان skill می‌آید، یا به فایلی در مخزنی که agent روی آن کار می‌کند، و مسیر بی‌نشانه نمی‌گوید کدام. دو نشانه می‌گویند، و `python scripts\check_fleet_references.py` آن‌ها را می‌خواند:

- شکل `$SKILL_DIR/<path>` برای فایلی است که داخل همان skill بسته‌بندی شده. آن checker مسیر را resolve می‌کند و فایل غایب یک finding است.
- شکل `<repo>/<path>` برای مسیری در مخزن هدف است. آن checker هرگز این مسیر را resolve نمی‌کند، چون این مخزن نمی‌داند آنجا چه هست.

هنگام نوشتن یا ویرایش هر ارجاع، مسیر را نشانه بگذارید. مسیر بی‌نشانه‌ای که به جایی resolve نمی‌شود فقط اطلاعی گزارش می‌شود و هرگز اجرا را نمی‌شکند، پس تبدیل ناوگان می‌تواند skill به skill جلو برود و هیچ حالت میانی gate را خراب نمی‌کند. همین حالا `alaa-postman-collections` هر دو نشانه را به کار می‌برد.

## قواعد تقدم اصلی

وقتی دو skill یک قاعده را می‌گویند، فایل `AGENTS.md` مالک و سمت اشاره‌کننده را نام می‌برد. آن مرزها مال همان فایل است و قواعد زیر تکرارشان نمی‌کنند.

### ۱. سیاست Arvan-first برای پلتفرم

اگر کار زیرساخت یا Kubernetes یا Helm یا استقرار روی ArvanCloud CaaS است، منبع حقیقت سطح-pack همان `caas-arvan-kuber` است. اگر توصیه عمومی زیرساخت با محدودیت‌های آروان تناقض داشت، Arvan-first برنده است، مگر کاربر صریحا override را تایید کند.

### ۲. سیاست اعتماد gateway

اگر سرویسی پشت gateway علاء زندگی می‌کند، منبع حقیقت مرز اعتماد همان `alaa-trust-gateway-auth` است: هویت مشتق از JWT، قواعد هدر معتمد، انتشار مرز tenant و project، تصمیم اعتماد به سرویس پایین‌دست، و راهنمای route و قرارداد خطای سرویس auth.

### ۳. سیاست خانواده frontend

برای خانواده استاندارد Vue 3 و Quasar و Vite، از `alaa-frontend-developer` شروع کنید. سپس `alaa-vue-typescript-clean-code` را به‌عنوان خط پایه کیفیت اعمال کنید، هر جا کدنویسی یا بازبینی یا refactor به SFC و composable و store مربوط به Pinia و TypeScript سمت frontend دست بزند. بعد به کوچک‌ترین skill همراهی بروید که مالک تصمیم بعدی است:

- برای build و استقرار و Docker و CI و artifact و public-path و CDN و proxy: `alaa-frontend-devops`
- برای کار فقط-مستندسازی روی JSDoc یا کامنت درون‌کد: `alaa-frontend-doc-annotations`
- برای package کاری و `packages/*` و peer dependency و انتشار asset: `alaa-mono-package`
- برای Quasar CLI و `quasar.config` و جزئیات mode و ارتقای Quasar: `alaa-quasar-app-vite-v3`
- برای کتابخانه کامپوننت و توکن طراحی و حاکمیت بصری: `alaa-ui-ux-design-system`

### ۴. خط پایه کدنویسی PHP و Laravel

برای کار PHP و Laravel، خط پایه پیش‌فرض `alaa-php-clean-code` است. آن را همراه کوچک‌ترین skill های مرتبط به کار ببرید: `alaa-laravel-architecture`، `alaa-data-layer`، `alaa-async-messaging`، `alaa-laravel-job-rabbitmq`، `alaa-octane-performance`، `alaa-security-review`، `alaa-observability-soc`، `alaa-cicd-laravel-postgres`، `alaa-repo-docs`، `alaa-mongodb-patterns`، `alaa-trust-gateway-auth`، `alaa-workflow`.

## پیش از فرض اینکه سرویسی از قبل منطبق است

فایل `alaa-services-contract references/95-fleet-conformance.md` برای تاریخ نوشته‌شده در ابتدایش ثبت می‌کند که کدام یک از هفت مولفه علاء کدام قواعد قرارداد را برآورده می‌کنند و هر کدام که نمی‌کند چه باید تغییر دهد. پیش از برنامه‌ریزی یک migration، ترتیب‌دهی یک تغییر در سطح ناوگان، یا نوشتن هر جمله‌ای که فرض می‌گیرد سرویسی نام‌برده از قبل منطبق است، آن فایل را بخوانید. خودش هیچ قاعده‌ای نمی‌گوید: فایل reference شماره‌دار کنار هر سطر برنده است، و هر جا آن snapshot با مخزن پیش چشم شما اختلاف داشت، مخزن درست است.

## وابستگی pack-local در برابر سطح-سیستم

هر چیزی که در نقشه skill ها پایین‌تر آمده با pack به نام `sohrab` می‌آید و سطح نصب عمومی و قابل حمل است. سه مورد زیر کمک‌کننده سطح-سیستم‌اند: قابل ارجاع، ولی pack-local نیستند و هیچ چیزی در این pack جایشان را نمی‌گیرد.

- شکل `/openai-docs` و `$openai-docs` برای راهنمای رسمی OpenAI و Codex، ارجاع‌دهی، به‌روزرسانی prompt، و رفتار CLI یا اپ
- شکل `/playwright` و `$playwright` برای خودکارسازی صریح مرورگر، navigation، یا QA مبتنی بر مرورگر
- شکل `/playwright-interactive` و `$playwright-interactive` برای حلقه‌های دیباگ مرورگر که کار تعاملی لازم دارند

## نقشه فعلی skill ها

هر پوشه این دایرکتوری دقیقا یک بار در جدول‌های زیر می‌آید، و هر نامی که در آن جدول‌ها هست یک پوشه است. دستور `python scripts\check_skill_index.py` هر دو جهت را برای این فایل و برای `README.md` بررسی می‌کند و وقتی یکی از دو جهت نقض شود شکست می‌خورد. عضویت این فایل با `README.md` دقیقا یکی است؛ مرز دسته‌ها یکی نیست، چون اینجا نه دسته داریم و آنجا هشت دسته.

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
| `alaa-prompting-guide` | **تنها مرجع مدل و effort.** نوشتن prompt، skill، تعریف agent، و فایل‌های `AGENTS.md`/`CLAUDE.md`؛ صاحب قرارداد فشرده‌سازیِ رفتار-حفظ و نصب‌کننده تخصصیِ `alaa-rule-writer` | هر سوالی درباره انتخاب مدل، سطح تلاش، نوشتن skill، یا کوتاه‌کردن متنی که رفتار agent دیگری را کنترل می‌کند |
| `alaa-low-noise` | صرفه‌جویی در context و نظم خروجی، در هر دو runtime | کارهای طولانی که خروجی پرگو تولید می‌کنند |
| `alaa-workflow` | برنامه‌ریزی کارهای چندفازی با فایل plan و state که از compaction و تحویل جان سالم ببرد | کاری که در یک نشست تمام نمی‌شود |
| `alaa-system-design` | روش طراحی یک سرویس یا زیرسیستم **پیش از** پیاده‌سازی: مرزبندی، قرارداد قبل از کد، مالکیت داده، و انتخاب بین چند طرح | قبل از نوشتن کدی که مرز، قرارداد، یا مالکیت داده را جابه‌جا می‌کند |
| `alaa-testing-strategy` | طراحی تست: لایه‌ها، test double ها، شش سطح قدرت اثبات، کنترل flake، و پوشش | تصمیم‌گیری درباره اینکه چه چیزی و در کدام لایه تست شود |
| `alaa-algorithms-data-structures` | بودجه پیچیدگی، پیدا کردن کران واقعی ورودی، انتخاب ساختار داده از روی الگوی دسترسی، و خانواده N+1 | مسیری که ورودی‌اش با تعداد کاربر، تاریخچه یا fan-out رشد می‌کند |
| `alaa-code-intelligence-routing` | هدایت قطعی شواهد میان CodeGraph، Serena، Laravel Boost، مالک‌های native/domain و proof مخزن؛ جلوگیری از retrieval تکراری و الزام اعتبارسنجی در همان worktree | وقتی باید برای discovery، ویرایش معنایی، مستندسازی، artifact، review یا proof یک مالک انتخاب کنید |
| `alaa-keyset-pagination` | طراحی pagination مبتنی بر cursor: ترتیب قطعی با tie-breaker، ایندکس متناظر، امضا و اعتبارسنجی cursor، و استثنای offset برای جدول‌های ادمین | هر route لیستی که کلاینت صفحه‌به‌صفحه می‌خواند |
| `alaa-input-normalization` | تبدیل ارقام فارسی و عربی و هر رقم غیر-ASCII به ASCII در هر دو مرز ورودی، یعنی مرورگر در لحظه submit و middleware هر سرویس backend، با یک قرارداد و چهار پیاده‌سازی و یک harness انطباق | نوشتن یا بازبینی مسیر submit فرم، validator، middleware تازه، یا فیلد OTP و موبایل و کد ملی؛ و وقتی مقداری که با ارقام فارسی تایپ شده در validation یا unique index یا idempotency شکست می‌خورد |

## ۲. هدایت چند-agent

| Skill | برای چه کاری |
|---|---|
| `alaa-cc-orchestrator` | هدایت چند-agent در Claude Code با ۲۱ نقش، دروازه‌های تایید و بازبینی مستقل |
| `alaa-codex-orchestrator` | همان چیز برای Codex |
| `alaa-codex-runtime-ops` | بازیابی از خطاهای runtime در Codex و ویندوز |
| `alaa-memory-os` | مدل عملیاتی حافظه، مستقل از انبار: اینکه چه چیزی ارزش ثبت دارد، در چه شکل یادداشتی، و با چه بودجه بازخوانی و مسیر fail-open. ثبت drift وقتی دو منبع حقیقت اختلاف دارند. Basic Memory و Hindsight هر کدام یک reference آداپتور دارند و هیچ‌کدام موضوع این skill نیستند |
| `alaa-extract-agent-lessons` | دروازه میانی و پایانی برای استخراج رابط‌های تصمیم‌گیری، معیارهای قضاوت، و کارت‌های دانش ماندگارِ مبتنی بر شواهد؛ نگهداری نامزدهای فعال در `alaa-workflow` و انتشار فقط دانش ماندگارِ مجاز از مسیر `alaa-memory-os` |

## ۳. PHP و Laravel

| Skill | برای چه کاری |
|---|---|
| `alaa-php-clean-code` | کد تمیز PHP 8.5 و Laravel 13 برای سرویس‌های امن زیر Octane: نام‌گذاری، SOLID، تشخیص الگو و بوی کد، persistence اول-repository، caching با الگوی decorator، بودجه اندازه، و شعاع انفجار refactor |
| `alaa-laravel-architecture` | نقشه لایه‌ای Laravel برای سرویس‌های علاء (Controller تا Service تا Repository تا DB): کجا cache seam و error envelope و رویداد دامنه تولید می‌شود، و یک gate برای نقض لایه و نشت public-id |
| `alaa-octane-performance` | ایمنی runtime و کارایی مسیر داغ زیر Octane با worker های طولانی‌عمر: چه چیزی هرگز نباید بین دو request باقی بماند، مکانیزم reset، چرخه عمر worker، و تست رگرسیون نشتی |
| `alaa-laravel-job-rabbitmq` | job های صف‌شده Laravel روی RabbitMQ از طریق `vladimir-yuldashev/laravel-queue-rabbitmq`: تصمیم `queue:work` در برابر `rabbitmq:consume`، سیاست ack و nack، سقف تحویل و خطر crash-loop، و هشت کلاس خطای نام‌گذاری‌شده |
| `alaa-laravel-public-api-contract-pack` | ساخت و ممیزی بسته قرارداد API عمومی یک سرویس Laravel از روی حقیقت اجرایی مخزن: فهرست route، نسخه‌بندی، معنای retry هر route، مستندات OpenAPI و Postman و SDK، و gate ای که تا تاریخ deprecation حل‌نشده باشد بسته نمی‌شود |
| `alaa-laravel-upgrade-all-packages` | جاروب ارتقای وابستگی Composer و npm برای سرویس Laravel: اول restore point و baseline تست، سپس وضعیت outdated و audit، اولویت‌بندی advisory بر اساس severity، و یک تغییر قابل بازگشت |
| `alaa-cicd-laravel-postgres` | دروازه‌های انتشار برای سرویس‌های Laravel روی Postgres: کدام چک gate است و کدام advisory، gate برگشت‌پذیری up-down-up مایگریشن، ایزولاسیون پایگاه‌داده تست per-worker، و تطابق نسخه production با Postgres |
| `alaa-permission-generator` | ثبت و تولید و اعمال و اعتبارسنجی دسترسی‌های coarse علاء از طریق `alaa-permission-catalog`: کلید و bitmap id دسترسی، مصرف‌کننده Laravel و Go و TypeScript، seed احراز هویت، و رمزگشایی bitmap معتمد `X-Access` |

## ۴. Go

| Skill | برای چه کاری |
|---|---|
| `alaa-golang` | نقطه ورود Go و مسیریابی به ۴۶ skill بالادستی `golang-*`. مالک تصمیم framework هم همین است: kit یعنی `alaa-go-chi` روی chi و پیش‌فرض هر سرویس Go تازه. همچنین انتشار deadline، کران‌های server، محدودیت decode درخواست، و مرز repository و cache |
| `alaa-golang-clean-code-principles` | کد تمیز Go در عصر kit، و مرز اعتماد |
| `alaa-golang-fiber` | سرویس Go روی Fiber |
| `alaa-go-chi-development` | قرارداد حاکمیت kit مشترک `alaa-go-chi` و سرویس‌های ساخته‌شده روی آن، در دو نقش: کار داخل مخزن kit و کار داخل سرویس مصرف‌کننده. فاز اجرا را از تصمیم ratified شده خود مخزن kit می‌خواند و اگر فاز ناشناخته بود متوقف می‌شود |

> ۴۶ skill با پیشوند `golang-*` از upstream می‌آیند و زیر `vendor/` هستند. **هرگز ویرایش نشوند** — چهار skill بالا به آن‌ها ارجاع می‌دهند.

## ۵. داده و ذخیره‌سازی

| Skill | برای چه کاری |
|---|---|
| `alaa-data-layer` | سیاست لایه داده با Postgres به‌عنوان حقیقت: کدام انبار مالک یک واقعیت است، طراحی schema و ایندکس tenant-scoped، migration بدون قفل کردن جدول زنده، تنظیم query و pool، و Redis به‌عنوان cache ای که درخواست بدون آن هم زنده می‌ماند |
| `alaa-mongodb-patterns` | مکانیزم MongoDB: شکل سند و collection، ایندکس ترکیبی tenant-scoped، TTL و نگهداشت، upsert و bulkWrite خودتوان، read و write concern، و اینکه یک خواننده در زمان انتخاب primary چه می‌گیرد |
| `alaa-partitioned-table-fk-audit` | بازبینی کلید خارجی که با کلید ناقص به جدول partition شده اشاره می‌کند، یعنی SQLSTATE 42830. یک detector تست‌شده می‌فرستد که والدهای partition شده را از کد کشف می‌کند، شکل کلید واقعی هر والد را می‌خواند، و هر ارجاع ناقص را علامت می‌زند |
| `alaa-crockford-base32-codecs` | کدگذاری شناسه با Crockford Base32 و UUIDv7، با چهار پیاده‌سازی بایت-یکسان برای PHP و JavaScript و bash و Lua مربوط به HAProxy، به‌همراه harness ای که اثبات می‌کند هنوز هم‌خوان‌اند. برای تولید راز یا کلید رمزنگاری مناسب نیست |
| `clickhouse-performance-schema-ops` | schema و ingest و query و عملیات ClickHouse: مخزن ingest-pipeline مالک DDL است و هر مصرف‌کننده kit از یک lane با `readonly=2` می‌خواند که DDL اجرا نمی‌کند. انتخاب بین materialized view و projection و TTL و mutation و drop partition، و رفتار سرویس وقتی ClickHouse در دسترس نیست |
| `alaa-minio-object-storage` | سیاست ذخیره‌سازی شیء روی MinIO و S3: طراحی bucket و کلید شیء، دامنه tenant داخل کلید، lifecycle شامل قاعده abort برای multipart نیمه‌کاره، نسخه‌بندی و رمزنگاری و replication، تامین و چرخش اعتبارنامه، URL امضاشده، و کلاس‌های خطای انباری که در دسترس نیست یا نیمه‌نوشته است |
| `alaa-arvan-object-storage` | لایه تفاوت‌های Object Storage ابر آروان روی همان سیاست S3 و MinIO: endpoint های منطقه‌ای و جداسازی آن‌ها، آدرس‌دهی virtual-hosted، مدل کلید سطح-حساب، ماتریس سازگاری S3، سقف ۴۰۰ مگابایتی هر part، دسترسی عمومی از پشت CDN، و انتقال یک bucket یا کلاینت بین دو انبار |

## ۶. Frontend

| Skill | برای چه کاری |
|---|---|
| `alaa-frontend-developer` | نقطه ورود و سیاست frontend خانواده Vue 3 و Quasar و Vite: قطعیت hydration و امنیت cleanup، وضعیت auth و session در SSR، سیاست PWA و service worker، کتابچه Lighthouse و Core Web Vitals، و نیمه سمت-کلاینت پایداری و امنیت و رصدپذیری و قرارداد ورودی — همین‌جا شروع کنید، بعد به کوچک‌ترین skill همراه بروید |
| `alaa-vue-typescript-clean-code` | قرارداد الزامی کد تمیز Vue 3 و Quasar و Vite و TypeScript: تایپ script-setup، شکل composable و Pinia، تعمیر SOLID و بوی کد، عمق TypeScript، و بودجه سخت اندازه — پیش از تغییر هر فایل `.vue` یا `.ts` اعمال کنید |
| `alaa-quasar-app-vite-v3` | صفحه کنترل نسخه-آگاه برای Quasar CLI روی `@quasar/app-vite` نسخه ۳ (به‌همراه نگهداری v2 و مهاجرت v2-به-v3): `quasar.config`، boot و routing، هر mode پلتفرم، service worker، و بودجه دسترس‌پذیری و کارایی |
| `alaa-ui-ux-design-system` | تصمیم‌های UI/UX برای اپ‌های Vue/Quasar: توکن طراحی، theming، حالت تاریک، تایپوگرافی، RTL و تایپوگرافی فارسی، motion، وضعیت کامپوننت، و الگوهای دسترس‌پذیری |
| `alaa-frontend-devops` | دروازه‌های CI و pipeline برای مخزن frontend: قرارداد artifact ساخت، public path و پایه asset، سیاست cache، provenance ساخت، و اینکه چه چیزی مجاز است داخل bundle کلاینت کامپایل شود |
| `alaa-frontend-doc-annotations` | یک گذر فقط-مستندسازی روی کد frontend — JSDoc و کامنت درون‌خط روی فایل‌های Vue و Quasar و Vite — در diff ای که خروجی build آن پیش و پس بایت‌به‌بایت یکسان است؛ هرگز برای تغییری که رفتار را عوض می‌کند به کار نمی‌رود |
| `alaa-mono-package` | مهندسی package workspace زیر `packages/*`: نقشه `exports` و نقطه‌ورود عمومی، peer dependency، انتشار CSS و asset پکیج، ترتیب build، و اینکه اپ ریشه چگونه یک پکیج داخلی را مصرف می‌کند |
| `alaa-indexeddb-browser-storage` | بستر ذخیره‌سازی خود مرورگر برای ناوگان علاء: معناشناسی IndexedDB، سهمیه origin، eviction، شاخه‌بندی ارتقای schema، همروندی چند-تب و service-worker، و اینکه کدام کلاس داده مجاز است روی دستگاه بنشیند |
| `alaa-shaka-player` | اطلس کامل قابلیت Shaka Player: چرخه عمر، DASH و HLS، بیت‌ریت تطبیقی، DRM، دانلود آفلاین، طبقه‌بندی خطا، و binding مربوط به Vue و Quasar |

## ۷. زیرساخت و تحویل

| Skill | برای چه کاری |
|---|---|
| `alaa-docker-production` | Dockerfile و Compose و stack آماده production، شامل build secret و attestation و healthcheck و سقف منابع. مالک نحوه بیان image و فایل runtime است و هیچ gate ای تصمیم نمی‌گیرد؛ سیاست gate مال `alaa-frontend-devops` است |
| `alaa-k8s-helm` | تولید و بازبینی و اعتبارسنجی و دیباگ chart های Helm و manifest های Kubernetes و بار کاری OpenShift، شامل Route و SCC و CRD و امنیت rollout و در معرض گذاشتن سرویس، حتی روی پلتفرم namespace-محور |
| `alaa-gitlab-ci-cd` | تولید و اعتبارسنجی و بازبینی و دیباگ pipeline های GitLab CI/CD، کامپوننت‌های قابل استفاده‌مجدد CI، پیکربندی runner، و جریان‌کار container-build؛ مالک نحوه بیان یک gate روی runner است و هرگز تصمیم نمی‌گیرد که یک چک باید pipeline را ببندد یا نه |
| `alaa-haproxy` | پیکربندی و تنظیم و عیب‌یابی و ارتقای HAProxy: تبدیل تصمیم routing و TLS و cache و rate limiting و درین به directive، انتخاب بین branch های پشتیبانی‌شده، و خواندن Runtime API. هر تغییر با `haproxy -c -f` اثبات می‌شود |
| `alaa-haproxy-lua` | قرارداد مهندسی Lua ای که داخل پروسه HAProxy اجرا می‌شود: مدل اجرا، سطح API، دیده‌شدن خطا در لبه، و تست بیرون از HAProxy. یک checker پیش-از-انتشار می‌فرستد. directive های پیکربندی مال `alaa-haproxy` است |
| `caas-arvan-kuber` | حقایق پلتفرم Arvan CaaS برای بار کاری Kubernetes و Helm که با Kubernetes خام فرق دارد: سطح API محدود-به-namespace، هویت RBAC alias-در-برابر-canonical، برابری admission requests-equal-limits، و annotation های exposure مستندنشده |
| `alaa-bash-shell` | چرخه کامل عمر Bash و POSIX shell: تولید و بازآرایی و اعتبارسنجی و دیباگ اسکریپت `.sh` و `.bash`، با قرارداد الزامی `-h`/`--help` و جریان‌کارهای ShellCheck و shfmt و checkbashisms و Bats |
| `alaa-makefile` | تولید و اعتبارسنجی و بازآرایی و به‌روزسازی و دیباگ فایل‌های GNU Make و `.mk`: هدف‌های phony، طراحی متغیر، make بازگشتی، ایمنی shell در recipe، و اعتبارسنجی mbake و checkmake و unmake |
| `ansible-generator` | تولید playbook و role و task file و inventory آماده production برای Ansible با ماژول‌های صحیح FQCN و task های idempotent، سپس سپردن نتیجه به `ansible-validator` |
| `ansible-validator` | اعتبارسنجی و lint و ممیزی امنیتی و dry-run playbook و role و inventory موجود Ansible با ansible-lint و yamllint و check mode و Checkov و Molecule، با گزارش یک حکم همراه ارجاع رفع هر finding |

## ۸. پیام‌رسانی، یکپارچه‌سازی و اعتماد

| Skill | برای چه کاری |
|---|---|
| `alaa-async-messaging` | معماری صفحه پیام روی RabbitMQ، تنها broker ناوگان: درز بین commit پایگاه داده و پیام منتشرشده، outbox تراکنشی و سطح عملیاتی‌اش، publisher confirm، نقطه ack، prefetch و همروندی مصرف‌کننده، توپولوژی dead-letter، و رویه replay از DLQ |
| `alaa-trust-gateway-auth` | صدور و اعتبارسنجی token و هدرهای معتمد در gateway |
| `alaa-bale-provider` | یکپارچه‌سازی با پیام‌رسان بله |
| `alaa-sms-provider-mediana` | ارسال پیامک با مدیانا |
| `tusd-upload-platform` | آپلود resumable با tusd |
| `jitsi-platform-architect` | معماری پلتفرم Jitsi |

## ۹. رصدپذیری، مستندات و دانش

| Skill | برای چه کاری |
|---|---|
| `alaa-signoz-clickhouse-docs` | نوشتن و تعمیر SQL خام پنل‌های SigNoz روی جدول‌های `signoz_logs` و `signoz_traces` و `signoz_metrics` که مالکشان vendor است و برای ناوگان فقط-خواندنی‌اند: کلیدهای ترتیب، اصطلاح bucket-filter و resource-CTE، انتخاب rollup، تشخیص span گم‌شده، و مسیریابی مستندات SigNoz |
| `vector-rust-observability-pipelines` | خط لوله production ای Vector: توپولوژی و قرارداد تحویل هر مسیر، تبدیل VRL، buffer و ack سرتاسری، backpressure، و retry و batch مقصد. مهم‌ترین بخشش این است که خط لوله وقتی مقصدش در دسترس نیست چه می‌کند. هیچ schema ای تصمیم نمی‌گیرد |
| `alaa-postman-collections` | ساخت و همگام‌سازی و اعتبارسنجی collection و environment نسخه v2.1 در Postman، به‌شکلی که هر request نمونه ذخیره‌شده برای حالت موفق و برای هر خطایی که واقعا می‌تواند برگرداند داشته باشد، یک script پس-از-پاسخ که token و id را برای request های بعدی بگیرد، و تست‌هایی که روی پیاده‌سازی خراب شکست بخورند. خروجی قابل import در Insomnia می‌ماند |
| `alaa-repo-docs` | مستندسازی سطح-مخزن برای راه‌اندازی، معماری، خلاصه API، داده، خطا، رویداد، رصدپذیری، و navigation داخلی. زبان هر سند موجود را حفظ می‌کند، نسخه زبانی دیگر را فقط با درخواست صریح می‌سازد، و برای هر موضوع یک محل canonical نگه می‌دارد تا سندهای دیگر با لینک نسبی به آن ارجاع دهند |

## تجمیع‌شده یا حذف‌شده از این pack

نام‌های زیر در نسخه‌های قدیمی‌تر نقشه بودند و اینجا هیچ پوشه‌ای ندارند، بازبینی‌شده در ۲۰۲۶-۰۷-۳۰. هیچ‌کدام را پیش از آنکه پوشه‌اش روی دیسک باشد به نقشه برنگردانید.

- خانواده `dockerfile-*` جایش را به `alaa-docker-production` داد، و `makefile-generator` و `makefile-validator` جایشان را به `alaa-makefile` دادند
- خانواده‌های `azure-pipelines-*` و `github-actions-*` و `jenkinsfile-*` حذف شدند، چون `alaa-gitlab-ci-cd` تنها سطح CI ای است که این pack می‌فرستد
- خانواده‌های `terraform-*` و `terragrunt-*` حذف شدند، چون هدف‌های زیرساخت از `caas-arvan-kuber` و `alaa-k8s-helm` عبور می‌کنند
- نام `alaa-basic-memory-os` به `alaa-memory-os` تغییر کرد، چون آن مدل مستقل از انبار است و Basic Memory فقط یکی از آداپتورهاست
- خانواده `promql-*` و `logql-generator` و `loki-config-generator` و `fluentbit-*` حذف شدند، چون `alaa-observability-soc` مالک تصمیم سیگنال و gate است و `alaa-signoz-clickhouse-docs` و `vector-rust-observability-pipelines` مالک سطح کوئری و خط لوله‌اند

## تعریف انجام‌شده

کار در این pack وقتی آماده حساب می‌شود که:

- کوچک‌ترین skill درست از `SKILL.md` به‌راحتی پیدا شود
- راهنمای تفصیلی در فایل‌های یک-پرش `references/` یا `docs/` نگه داشته شده باشد
- فایل `agents/openai.yaml` وجود داشته باشد و با نیت فعلی skill بخواند
- نام skill های اهداکننده قدیمی از سندهای routing فعال حذف شده باشد
- دستور `python scripts\check_skill_index.py` هیچ finding مربوط به نقشه و هیچ کمبود `agents/openai.yaml` گزارش نکند
- مثال و checklist و ضدالگو به انگلیسی ساده حفظ شده باشند
- کمک‌کننده‌های سطح-سیستم از skill های pack-local به‌روشنی جدا باشند

---

## قواعدی که همیشه برقرارند

**مالکیت یکتا.** هر قاعده فقط یک مالک دارد. اگر دو skill یک چیز را گفتند، یکی از آن‌ها اشتباه است — گزارش دهید.

**نام و مقدار در برابر سطح الزام.** در حوزه telemetry، نام‌ها و مقادیر مال `alaa-services-contract` است و سطح الزام و gate ها مال `alaa-observability-soc`. اگر این دو اختلاف داشتند: روی «آیا الزامی است» دومی برنده است، روی «اسمش چیست» اولی.

**قرارداد در برابر مکانیزم.** نام‌های canonical زیرساخت مشترک و الزام reuse مال `alaa-services-contract` است؛ اینکه کدام متغیر generator آن را بیان می‌کند مال `service-runtime-kit-governance`.

**fail-closed در برابر fail-open.** کنترلی که تصمیم می‌گیرد آیا کسی مجاز است — وقتی نمی‌تواند تصمیم بگیرد **رد می‌کند** و مالکش `alaa-security-review` است. مؤلفه‌ای که فقط مشارکت می‌کند — وقتی از کار می‌افتد **راه را باز می‌گذارد** و مالکش `alaa-reliability-sla` است. این دو عمداً متناقض‌اند و سوال تعیین‌کننده این است: اگر بدون این مؤلفه ادامه دهیم، چیزی که نباید عبور کند عبور می‌کند؟

**مدل و effort.** هیچ skill دیگری نام مدل نمی‌گوید. همه به `alaa-prompting-guide` ارجاع می‌دهند.

**پوشه vendor.** هر چیزی زیر `vendor/` از upstream می‌آید و ویرایش نمی‌شود. skill خودی آن را می‌پوشاند و به آن ارجاع می‌دهد.

## یادداشت عملی

وقتی یک best practice عمومی با مدل اعتماد gateway علاء، قواعد پلتفرم آروان، یا قرارداد artifact مربوط به frontend تناقض دارد، دلیل انحراف را مستند کنید، نه اینکه پنهانش کنید.
