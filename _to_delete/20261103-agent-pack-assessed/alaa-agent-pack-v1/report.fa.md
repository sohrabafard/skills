# انتخاب مدل و پک ایجنت‌های تخصصی آلاء

**نسخه ۱ · بررسی منابع: ۲ نوامبر ۲۰۲۶ · ۳۰ نقش · ۳۶ طرح ارزیابی**

## نتیجه تصمیم

برای پروژه بزرگ آلاء، **Sol 6.1 را مدل اصلی توسعه** قرار بده؛ **Astra را برای تصمیم و بازبینی دشوار** به کار بگیر؛ **Terra را برای کار بصری، مستندات مبتنی بر شواهد و فیکس محدود** وارد کن؛ **Luna را برای کار محدود و پرتکرار** نگه دار. این، سیاست پیشنهادی شروع است و با نتایج واقعی پروژه باید تنظیم شود.

Terra برای کدنویسی قابل‌استفاده است. آنچه فعلاً نمی‌توان از شواهد این پژوهش نتیجه گرفت، برتری قطعی آن بر Sol یا Luna در Python، PHP یا JavaScript است. هیچ اجرای مقایسه‌ای روی مخزن آلاء انجام نشده است. تفاوت **زبان**، **نوع مسئله**، **کیفیت کانتکست** و **ابزارهای اعتبارسنجی** را جدا نگه داریم.

## رسیدگی به ادعای Model selection

| ادعا | نتیجه بررسی | مبنا |
|---|---|---|
| OpenAI اصلاً Terra را برای کدنویسی پیشنهاد نکرده | **برای نسخه فعلی صفحه نادرست است** | صفحه Model selection صریحاً عبارت «scoped code fixes» را برای Terra دارد. [O1](https://developers.openai.com/api/docs/guides/model-selection) |
| Terra مدل پیشنهادی اصلی برای تمام پروژه‌های بزرگ است | **از منابع بررسی‌شده نتیجه نمی‌شود** | راهنمای کدنویسی، Sol را در زمینه Codex و Astra را برای شروع بسیاری از کاربردهای API کدنویسی مطرح می‌کند. [O6](https://developers.openai.com/api/docs/guides/code-generation) |
| نبودن مدل در یک خروجی پیشنهادگر، یعنی ناتوانی آن در کدنویسی | **استنتاج معتبر نیست** | توصیه وابسته به نوع کار، کیفیت، هزینه و effort است؛ خروجی یک حالت، رتبه‌بندی جامع توانایی نیست. این توضیح، تحلیل ماست. |
| Terra در PHP/Python/JS حتماً بهتر یا بدتر از Luna است | **اثبات نشده در این پژوهش** | مقایسه رسمی تفکیک‌شده و هم‌شرایط برای این زبان‌ها در منابع بررسی‌شده پیدا نشد. |

مبنای داوری، متن فعلی صفحه بازشده است. تمام ترکیب‌های ویجت تعاملی پیشنهادگر آزموده نشده‌اند. ممکن است گوینده نسخه قدیمی یا حالت خاصی را دیده باشد؛ علت دقیق اختلاف معلوم نیست. عدم کشف بنچمارک نیز به معنی اثبات نبودن آن در همه منابع جهان نیست.

## چهار مدل، چهار کاربرد اولیه

| مدل دقیق | جایگاه معرفی‌شده | کاربرد پیشنهادی در تیم آلاء | قیمت پایه API: ورودی / خروجی، دلار به‌ازای یک میلیون توکن |
|---|---|---|---|
| `gpt-6-astra` | دشوارترین کارها، استدلال و کدنویسی پیچیده [O4](https://developers.openai.com/api/docs/models/gpt-6-astra) | معمار، داور مسئله سخت و reviewer تغییر پرریسک | ۱۰ / ۵۰ |
| `gpt-6.1-sol` | کار پیچیده و کدنویسی با هزینه پایین‌تر از Astra [O3](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | توسعه‌دهنده اصلی و هماهنگ‌کننده روزمره | ۲ / ۱۰ |
| `gpt-6.1-terra` | استدلال بصری، کار با محیط نرم‌افزار و نگارش [O2](https://developers.openai.com/api/docs/models/gpt-6.1-terra) | UI محدود، مستندات و فیکس محلی قابل‌آزمایش | ۱ / ۵ |
| `gpt-6-luna` | کار محدود، پرتعداد و کم‌هزینه [O5](https://developers.openai.com/api/docs/models/gpt-6-luna) | scout، استخراج، دسته‌بندی و تغییر مکانیکی | ۰٫۱ / ۰٫۵ |

قیمت‌ها Standard API و متن هستند، نه سهمیه اشتراک ChatGPT/Codex. cache، ابزار، سرعت بالاتر، پردازش منطقه‌ای و درخواست‌های بلند می‌توانند محاسبه را تغییر دهند. برای نمونه فرضی ۱۰۰هزار توکن ورودیِ بدون cache و ۱۰هزار توکن خروجی: Luna حدود ۰٫۰۱۵ دلار، Terra حدود ۰٫۱۵، Sol حدود ۰٫۳۰ و Astra حدود ۱٫۵۰ دلار است. این مثال **توکن برابر** دارد؛ کیفیت، تعداد retry، زمان و هزینه واقعی کار را اندازه نمی‌گیرد.

**قیمت توکن پایین‌تر لزوماً هزینه کار تمام‌شده را پایین نمی‌آورد.** هزینه مورد استفاده در تصمیم، مجموع تلاش‌های موفق و ناموفق، ابزار، review و اصلاح است. زمان انسانی را جداگانه ثبت کن. نسبت ۲ برابری قیمت توکن Sol به Terra، ادعای نسبت سرعت یا کیفیت آن‌ها نیست.

## Terra برای Python، PHP و JS دقیقاً کجا؟

| خانواده کار | Terra را کجا امتحان کنیم؟ | انتخاب اولیه برای کار اصلی | نمونه‌ای که باید مدل قوی‌تر وارد شود |
|---|---|---|---|
| Python | parser محدود، تبدیل داده مشخص، اصلاح تابع با تست روشن، ویرایش مستندات | Sol medium | cancellation پیچیده، الگوریتم دشوار، عددی/حافظه‌ای حساس → Astra یا Sol high |
| PHP / Laravel | validation یا DTO محدود، فیکس محلی با قرارداد روشن | Sol medium/high | state باقی‌مانده در Octane، race تراکنش و جداسازی tenant → Astra برای بررسی دشوار |
| JavaScript / TypeScript | خطای type یا رفتار کوچک، component مستقل | Sol medium | state گسترده، ترتیب پاسخ async، SSR و قرارداد مشترک → Sol high/Astra |
| HTML / CSS / UI | اصلاح بصری با screenshot، viewport و حالت معلوم | Terra medium برای تغییر محدود؛ Sol برای فیچر کامل | مشکل در state، accessibility پیچیده یا hydration → Sol |

جدول بالا **پیشنهاد آزمایش ماست، نه رتبه‌بندی رسمی زبان‌ها**. Luna نیز می‌تواند در بعضی اصلاحات روشن رقیب اقتصادی Terra باشد؛ تا آزمایش هم‌شرایط، ترتیب قطعی Terra>Luna را فرض نکن.

## جدول نقش‌ها و مدل‌ها

در این جدول «مدل شروع» یعنی انتخاب پیش‌فرض متعادل برای آن نقش؛ «ارتقا» یعنی وقتی ریسک یا ابهام افزایش یافت. هیچ سطر، ادعای بنچمارک اختصاصی آن زبان/ابزار ندارد. اطمینان به صحت نقل معرفی مدل‌ها بالاتر از اطمینان به برتری در یک task خاص آلاء است.

| نقش / حوزه | مدل شروع | ارتقا برای کار دشوار | مسئولیت و معیار انتخاب |
|---|---|---|---|
| **رهبر تیم و هماهنگ‌کننده**<br><code>lead</code> | Sol · high | Astra · high | تقسیم کار، وابستگی‌ها، مالکیت فایل و یکپارچه‌سازی؛ Astra وقتی تصمیم مبهم و چندسرویسی است. |
| **معمار سامانه**<br><code>architect</code> | Astra · high | Astra · xhigh با ارزیابی | تصمیم مرز سرویس، consistency، NFR و ADR؛ Sol برای مسئله‌ای با قیود و الگوی تثبیت‌شده کافی‌تر است. |
| **تحلیل نیازمندی و دامنه**<br><code>requirements</code> | Sol · high | Astra · high | تبدیل خواسته به معیار پذیرش و غیرهدف؛ حل تعارض قواعد کسب‌وکار. |
| **کاوش کد و تهیه کانتکست**<br><code>scout</code> | Luna · medium | Sol · medium/high | کشف مسیرها و نمادها با ارجاع دقیق؛ بدون اختیار تغییر کد. |
| **طراحی API و قراردادها**<br><code>api</code> | Sol · high | Astra · high | OpenAPI، خطاها، idempotency و سازگاری مصرف‌کنندگان؛ طراحی پروتکل پیچیده به Astra. |
| **پیاده‌سازی Vue و TypeScript**<br><code>frontend</code> | Sol · medium | Sol high → Astra high | Vue/TS/JS، state و API integration؛ SSR، hydration و raceها ریسک را بالا می‌برند. |
| **اصلاح بصری محدود و CSS**<br><code>ui-fixer</code> | Terra · medium | Sol · medium/high | فیکس CSS/HTML و UI محدود با مرجع روشن؛ رفتار، کیبورد و responsive هم باید تست شوند. |
| **PHP، Laravel و Octane**<br><code>php</code> | Sol · medium | Sol high → Astra high | PHP/Laravel/Octane؛ چرخه worker، transaction و tenant isolation معیارهای مهم‌اند. |
| **Python و ابزارهای داده/اتوماسیون**<br><code>python</code> | Sol · medium | Astra · high | سرویس/ابزار Python؛ Terra و Luna گزینه آزمایش برای فیکس محلی و تبدیل داده روشن هستند. |
| **Golang و سرویس‌های همزمان**<br><code>go</code> | Sol · medium | Sol high → Astra high | Golang، cancellation، worker pool و backpressure؛ concurrency دشوار به Astra. |
| **Rust و تغییرات سطح پایین**<br><code>rust</code> | Sol · high | Astra · high | کد واقعی Rust؛ برای unsafe، ownership پیچیده و الگوریتم همزمان بازبینی قوی‌تر. |
| **PostgreSQL و SQL**<br><code>postgres</code> | Sol · high | Astra · high | schema، SQL و plan؛ isolation و migration حساس به بازبینی Astra نیاز دارند. |
| **Redis و Cache**<br><code>redis</code> | Sol · high | Astra · high | کلید، TTL، invalidation، stampede؛ قفل و failover حساس را مستقل بررسی کنید. |
| **RabbitMQ، Kafka و Outbox**<br><code>messaging</code> | Sol · high | Astra · high | RabbitMQ/Kafka، retry، outbox و replay؛ مرز ack و تکمیل کسب‌وکار روشن باشد. |
| **ClickHouse و تحلیل رخدادها**<br><code>clickhouse</code> | Sol · high | Astra · high | grain، ingestion و query؛ درستی dedup/late event قبل از بهینه‌سازی. |
| **امنیت و Auth/AuthZ**<br><code>security</code> | Astra · high | xhigh فقط با نیاز مشخص | Auth/AuthZ، tenant و gateway، OTP/TOTP؛ یافته باید مسیر و شواهد قابل‌بازآفرینی داشته باشد. |
| **طراحی راهبرد تست**<br><code>test-designer</code> | Sol · high | Astra · high | طراحی تست از قرارداد، مستقل از پیاده‌سازی؛ properties امنیتی/همزمانی به Astra. |
| **پیاده‌سازی تست و Regression**<br><code>test-engineer</code> | Sol · medium | Sol · high | پیاده‌سازی تست واقعی؛ fixture مکانیکی به Luna پس از تثبیت معیار پذیرش. |
| **بازبینی مستقل کد**<br><code>reviewer</code> | Sol · high | Astra · high | review روزمره؛ برای diff پرریسک از Astra با شواهد مستقل استفاده کنید. |
| **Bug hunting و ریشه‌یابی**<br><code>debugger</code> | Sol · high | Astra · high | reproducer و فرضیه‌های قابل رد؛ رخداد نادر و چندسرویسی به Astra. |
| **الگوریتم و ساختمان داده**<br><code>algorithms</code> | Astra · high | xhigh فقط با نیاز مشخص | انتخاب الگوریتم و اثبات کوتاه؛ پیاده‌سازی الگوریتم تثبیت‌شده می‌تواند با Sol باشد. |
| **کارایی و Load testing**<br><code>performance</code> | Sol · high | Astra · high | پروفایل و اندازه‌گیری p95/p99؛ مسئله چندلایه یا شواهد متعارض به Astra. |
| **Sentry، SigNoz، OTel و Vector**<br><code>observability</code> | Sol · high | Astra · high | Sentry/SigNoz/OTel/Vector، correlation و cardinality؛ incident پیچیده با Astra. |
| **Bash، CI/CD و زیرساخت**<br><code>infra</code> | Sol · high | Astra · high | Bash، Compose/OpenShift و CI؛ با قواعد واقعی دسترسی و rootless. |
| **تحقیق فنی**<br><code>research</code> | Sol · high | Astra · high | تحقیق با منابع اولیه و نسخه دقیق؛ جمع‌بندی تعارض عمیق با Astra. |
| **پرامپت و قواعد ایجنت**<br><code>prompting</code> | Sol · high | Astra · high | طراحی قواعد ایجنت و ارزیابی رفتار؛ Terra برای ویرایش نگارشی معنای تثبیت‌شده. |
| **مستندسازی و نگارش**<br><code>docs</code> | Terra · medium | Sol · high | مستندسازی از کد/شواهد آماده؛ کشف رفتار پیچیده و ADR به Sol/Astra. |
| **یکپارچه‌سازی و تحویل**<br><code>integrator</code> | Sol · high | Astra · high | کنترل سازگاری، diff نهایی، تست یکپارچه و بسته تحویل. |
| **مهاجرت و Refactor بزرگ**<br><code>migration</code> | Sol · high | Astra · high | اجرای مرحله‌ای refactor/migration؛ طراحی مهاجرت پرریسک با Astra. |
| **دسترس‌پذیری و RTL**<br><code>accessibility</code> | Terra · medium | Sol · high | بازبینی RTL و UI با شواهد DOM/تعامل؛ اسکرین‌شات به‌تنهایی کافی نیست. |


## اندازه تیم و شیوه هماهنگی

۳۰ نقش به معنای ۳۰ پردازه همزمان نیست. هر نقش یک تخصص قابل‌فراخوانی است. برای یک فیچر معمولی از این گروه آغاز کن: **lead، scout، مهندس مربوط، test-engineer و reviewer**؛ نقش داده/امنیت را با توجه به diff وارد کن. یک ایجنت می‌تواند نقش‌ها را به‌ترتیب انجام دهد؛ بازبینی حساس بهتر است در context مستقل و از شواهد اولیه شروع شود.

| مرحله | خروجی لازم | مالک |
|---|---|---|
| فهم درخواست | معیار پذیرش، غیرهدف و ابهام مؤثر | requirements + lead |
| شناخت کد | مسیر واقعی، نسخه‌ها و قرارداد موجود | scout |
| طراحی ضروری | API/ADR و invariant | api یا architect |
| اجرا | patch محدود و شواهد رفتار | مهندس حوزه |
| اعتبارسنجی | regression، integration و بررسی مستقل | test-engineer + reviewer |
| تحویل | diff نهایی، نتیجه واقعی تست و پیامد rollout | integrator + lead |

برای ماشین توسعه با منابع محدود، سقف اولیه **سه زیرایجنت علاوه بر lead** و **یک job سنگین build/test** پیشنهاد می‌شود؛ این عدد حاصل benchmark سخت‌افزار تو نیست. بر اساس CPU/RAM، فشار Docker و زمان اجرای ابزارها اصلاحش کن. reasoning مدل عمدتاً در سرویس مدل اجرا می‌شود، اما build، browser، تست و ابزارهای محلی منابع دستگاه را مصرف می‌کنند.

در یک worktree، یک فایل فقط یک نویسنده فعال داشته باشد. migration، lockfile، قرارداد مشترک، client تولیدشده و Git index یک مالک یکپارچه‌سازی داشته باشند. بررسی read-only می‌تواند موازی باشد، اما review نهایی باید روی snapshot ثابت باشد. تغییر فایل پس از review، بخش مربوط را دوباره نیازمند review می‌کند. ثبت مالکیت در این بسته قراردادی است؛ قفل سیستم‌عامل پیاده نشده است.

## انتخاب effort و مسیر ارجاع

| وضعیت | نقطه شروع پیشنهادی | قدم بعدی |
|---|---|---|
| فیکس محدود و معیار روشن | medium روی مدل مناسب | در صورت شکست، ابتدا شواهد/کانتکست را اصلاح کن |
| کدنویسی چندفایلی و integration | Sol medium؛ high برای ابهام بیشتر | reviewer مستقل و تست واقعی |
| معماری، امنیت و مسئله سخت | Astra high | xhigh/max فقط در صورت مسئله حل‌نشده و فایده قابل‌اندازه‌گیری |
| استخراج بسیار ساده | Luna low/medium | بررسی ساختار خروجی؛ در صورت پیچیدگی به Sol |

نام effort در API و تجربه کاربری یکسان‌بودن رفتار یا زمان را تضمین نمی‌کند. در بسته medium/high صریح انتخاب شده‌اند؛ نبود تنظیم صریح می‌تواند مقایسه را منحرف کند. اسناد رسمی نیز effort را وابسته به مدل می‌دانند. [O11](https://developers.openai.com/api/docs/guides/reasoning)

مدل قوی‌تر جای نیازمندی ناقص، reproducer گم‌شده یا telemetry ناکافی را نمی‌گیرد. ابتدا علت گیرکردن را مشخص کن. پس از یک تلاش اصلاحی هدفمند بدون شواهد جدید، به جای loop همان فرضیه را تکرار نکن؛ packet کوتاه تحویل بده و مسیر بررسی/مدل را تغییر بده.

## کنترل‌های اختصاصی استک آلاء

- **Octane و Vue SSR:** فرض «هر درخواست یک process/state تازه دارد» را بررسی کن؛ آزمون چند درخواست و چند tenant لازم می‌شود. مستندات هر دو فناوری درباره state مشترک هشدار می‌دهند. [T1](https://laravel.com/docs/12.x/octane) و [T2](https://vuejs.org/guide/scaling-up/ssr).
- **RabbitMQ/outbox:** publisher confirm، consumer ack و تکمیل عملیات کسب‌وکار را یکی نکن. تست duplicate و crash window را در مرز transaction قرار بده. [T3](https://www.rabbitmq.com/docs/confirms).
- **PostgreSQL:** plan و cardinality واقعی بخواه؛ `EXPLAIN ANALYZE` خود statement را اجرا می‌کند، پس بستر و اثر آن باید مشخص باشد. [T5](https://www.postgresql.org/docs/18/sql-explain.html).
- **Redis:** TTL، مالکیت lock، invalidation، outage و failover را صریح بنویس؛ وجود lock به‌تنهایی اثبات invariant کسب‌وکار نیست. [T6](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/).
- **ClickHouse:** صحت metric را با grain، late event و duplicate تطبیق بده؛ merge پس‌زمینه را با نتیجه فوری query یکی ندان. [T8](https://clickhouse.com/resources/engineering/clickhouse-optimize-table-final).
- **Observability:** نام درست ابزار **SigNoz** است. نقش observability در بسته Sentry، SigNoz، OTel و pipeline را پوشش می‌دهد. برای transformهای Vector معمولاً با **VRL** کار می‌کنیم؛ تغییر کد داخلی Rust تخصص جداست. [T4](https://vector.dev/docs/reference/configuration/transforms/remap/).

این کنترل‌ها جای بررسی نسخه واقعی dependency را نمی‌گیرند. سابقه معماری آلاء در template به‌عنوان سرنخ آمده؛ قواعد موجود پروژه و lockfile بر حدس تاریخی مقدم‌اند. قواعد عمومی بسته نیز جایگزین خودکار alaa-workflow یا alaa-code-intelligence-routing نشده‌اند.

## قرارداد ورودی و خروجی ایجنت

هر task باید هدف، معیار پذیرش، غیرهدف، فایل‌های مجاز، dependency، نسخه مبنا، بودجه و گیرنده خروجی داشته باشد. هر handoff باید تغییرات، شواهد، تست اجراشده، تست اجرا‌نشده، محدودیت و قدم بعد را گزارش کند. جمله «تمام شد» بدون شواهد، نتیجه قابل‌پذیرش نیست.

پرامپت نقش‌ها به انگلیسی نوشته شده تا با شناسه‌ها و کد هماهنگ باشد؛ ارتباط با تو فارسی خواسته شده است. این انتخاب نگارشی، ادعای برتری همیشگی انگلیسی بر فارسی نیست. تنها common policy، نقش لازم و task جاری را بار کن. ۳۰ پرامپت را یکجا به همه ایجنت‌ها نده؛ ابزارها و حافظه را هم با نیاز task وارد کن.

## چطور انتخاب‌ها را روی پروژه خودت اثبات کنیم؟

`evals/cases.json` شامل **۳۶ طرح مسئله** از Python/PHP/JS تا SQL، cache، امنیت، review، observability و prompting است. fixtureهای مخزن و oracle باید فراهم شوند؛ این فایل، نتایج اجرا نیست.

پایلوت پیشنهادی ۱۲ task × چهار مدل × سه اجرای مستقل است. ورودی، ابزار، نسخه پروژه، effort و بودجه را ثابت نگه دار؛ ترتیب اجرا را تصادفی کن؛ کیفیت را بدون دیدن نام مدل داوری کن. آزمون holdout را از prompt tuning جدا نگه دار. timeoutها و شکست‌ها را حذف نکن.

قبولی در معیار پذیرش و نبود شکست مهم امنیت/تمامیت، شرط اولیه باشد. سپس first-attempt success، هزینه تمام تلاش‌ها، wall time، زمان review انسانی و خروجی قابل‌نگهداری را بسنج. نتایج review، coding و research را در یک میانگین مبهم مخلوط نکن. ابزار محلی `summarize_eval.py` خلاصه نتایج اندازه‌گیری‌شده را می‌سازد و داده نمونه ساختگی را به‌صورت پیش‌فرض رد می‌کند.

تکرار یک task با seed/run متفاوت، معادل داشتن task مستقل جدید نیست. گزارش نمونه کم باید عدم‌قطعیت را نشان دهد. هدف، انتخاب سبک‌ترین مدلِ عبورکننده از معیار کیفیت هر خانواده کار است. [O10](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

## فایل‌ها و وضعیت اعتبارسنجی

| مسیر | محتوا |
|---|---|
| `START-HERE.fa.md` | راه‌اندازی و نکات سازگاری |
| `roles/` | ۳۰ پرامپت نقش با mission، ورودی، کنترل، خروجی و escalation |
| `codex/agents/` | ۳۰ تعریف مستقل TOML برای Codex محلی |
| `codex/config-snippet.toml` | مدل root و سقف همزمانی پیشنهادی |
| `policy/` | قواعد مشترک، context پروژه و هماهنگی worktree |
| `templates/` | task contract، handoff، ADR و مالکیت فایل |
| `workflows/` | فیچر، incident، migration، review و آزمون Terra |
| `evals/` | ۳۶ طرح آزمون، روش اجرا و نمونه صریحاً ساختگی |
| `scripts/` | اعتبارسنجی ساختار، ساخت پرامپت و خلاصه‌سازی eval |
| `tests/` | آزمون ابزار خلاصه‌سازی نتایج |
| `research/` | منابع رسمی و محدوده شواهد |

تعریف‌های Codex بر قالب فعلی مستندات تهیه شده‌اند: agentهای مستقل در `.codex/agents/`، مدل و effort صریح. دسترسی حساب و نسخه نصب‌شده باید سازگار باشند. دستور read-only در prompt محدودیت امنیتی ایجاد نمی‌کند؛ مجوزها از جلسه والد می‌آیند. [O8](https://learn.chatgpt.com/docs/agent-configuration/subagents)

بسته روی سیستم تو نصب نشده است. بررسی ساختار فایل‌ها و اجرای ابزارهای محلی با تست‌های مصنوعی، جای آزمون بارگذاری در Codex تو یا benchmark روی مخزن واقعی را نمی‌گیرد. هیچ اسکریپت همراه بسته به API مدل وصل نمی‌شود و ارزیابی پولی را خودکار آغاز نمی‌کند.

## منابع

| کد | منبع رسمی | کاربرد |
|---|---|---|
| O1 | [OpenAI Model selection](https://developers.openai.com/api/docs/guides/model-selection) | Terra is explicitly mentioned for scoped code fixes; general model/effort guidance. |
| O2 | [GPT-6.1 Terra](https://developers.openai.com/api/docs/models/gpt-6.1-terra) | Visual/computer-use/writing positioning, model ID, reasoning settings and price. |
| O3 | [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Complex coding positioning, model ID, reasoning settings and price. |
| O4 | [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) | Most demanding reasoning/coding positioning, settings and price. |
| O5 | [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) | Focused high-volume tasks, settings and price. |
| O6 | [Code generation](https://developers.openai.com/api/docs/guides/code-generation) | Codex general-purpose model guidance and API coding recommendation. |
| O7 | [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model) | Family positioning and model/effort distinction. |
| O8 | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Standalone custom-agent TOML schema, delegation, permissions inheritance. |
| O9 | [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Current config key names and agent concurrency controls. |
| O10 | [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Task-specific empirical evaluation; this package uses no hosted Evals dependency. |
| O11 | [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning) | Reasoning effort is model-dependent; increased effort requires evaluation. |
| T1 | [Laravel 12 Octane](https://laravel.com/docs/12.x/octane) | Long-lived workers, dependency injection and request state. |
| T2 | [Vue SSR](https://vuejs.org/guide/scaling-up/ssr) | Cross-request state pollution and SSR concerns. |
| T3 | [RabbitMQ confirms](https://www.rabbitmq.com/docs/confirms) | Publisher confirms and consumer acknowledgements are separate. |
| T4 | [Vector remap](https://vector.dev/docs/reference/configuration/transforms/remap/) | Vector transformation uses VRL. |
| T5 | [PostgreSQL 18 EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html) | EXPLAIN ANALYZE executes statements. |
| T6 | [Redis distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/) | Lock and failover assumptions require explicit treatment. |
| T7 | [Go race detector](https://go.dev/doc/articles/race_detector) | Race detection is a useful runtime check, limited to executed paths. |
| T8 | [ClickHouse merge behavior](https://clickhouse.com/resources/engineering/clickhouse-optimize-table-final) | Background deduplication and query-time correctness differ. |
