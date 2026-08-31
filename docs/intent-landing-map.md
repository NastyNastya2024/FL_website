| URL | Роль |
|-----|------|
| `index.html` | Маркетинговый лендинг: герой → цифры → 2 продукта → CTA → тизеры process/FAQ → новости |
| `about.html` | Канон: **О компании → Процесс → FAQ → Контакты** |
| `contacts.html`, `voprosy.html`, `kak-my-rabotaem.html` | **Soft-redirect** → `about.html#contacts` / `#faq` / `#process`. `noindex` + `canonical` на about. Нет в sitemap |

---

## Дубли URL (одинаковый / почти одинаковый контент)

Несколько URL с одним и тем же смыслом — серьёзнее, чем кажется: поисковик не знает, какую страницу показывать, и может показать «неправильную» или **разделить PageRank** между обеими. Итог: обе ранжируются хуже, чем могла бы одна.

| Тип дубля | Правило | Статус на сайте |
|-----------|---------|-----------------|
| **Точные дубли** (копии страниц) | Один канон; остальные — 301 или soft-redirect + `canonical` + `noindex` | ✅ stubs → `about` |
| **Каннибализация** (один интент, два URL) | Развести Title/H1/роль; иерархия parent → child | ✅ см. §2 |
| **Технические** (`?utm_`, `/` vs `index.html`) | `Clean-param`, единый canonical, серверный 301 `/` ↔ `index.html` | ⚠️ canonical = `index.html`; 301 на хостинге |
| **Служебные** (login, docs, expert) | `noindex` + `Disallow` в robots | ✅ |
| **Не плодить** третий URL на тот же primary | Новые страницы только с новой задачей пользователя | правило §4 |

**Проверка:** в sitemap только канонические URL; у каждого индексируемого документа свой уникальный `<link rel="canonical">`; пересечения primary — таблица §2.1.

---

## Критерии ЭПОС и above-the-fold (Яндекс) — на каждой странице

**Первый экран без прокрутки** — критически важен для поведенческих факторов (длительность, отказ, глубина).

| Критерий | Правило | Статус на сайте |
|----------|---------|-----------------|
| **H1 = запрос** | H1 формулирует задачу пользователя так, как он ищет (коммерческий или образовательный вариант). Title ≠ H1 допустимо (intent split). | ✅ продукты + pillar-статьи |
| **Первый абзац = ответ** | Сразу после H1 — прямой ответ без «воды», без блока «Экспертный материал» и без «Продукт: …» | ✅ 15 статей: `lead direct-answer` после H1 |
| **Нет помех в первые 5 с** | Нет автопопапов, баннеров cookie, форм подписки поверх контента; модалки только по клику | ✅ Bootstrap modal по `data-bs-toggle` |
| **Нет autoplay со звуком** | Hero-video только `muted playsinline` | ✅ index, FL, BDP, learning-types |
| **Скорость ≤ 3 с** | FCP / LCP ≤ 3 с на мобильном 4G | ⏳ целевой KPI |

**Структура статьи (above-the-fold):**

```
H1 (запрос)
→ p.lead.direct-answer (ответ)
→ article-text (развёрнутый контент)
→ .article-meta-footer (ключевые слова, продукт — ниже сгиба)
→ CTA / related
```

**Скрипт:** `scripts/fix_epos_above_fold.py` — переставляет lead/meta в статьях блога.

**Зазор закрыт (2026-08):** блок «Экспертный материал DigiTrack» и «Продукт: …» убраны из первого экрана статей.

---

## Типографика и читаемость (WCAG / поведенческие)

| Параметр | Правило | Реализация в `styles.css` |
|----------|---------|---------------------------|
| **Размер шрифта** | Минимум **16px** для основного текста на мобильном | `html { font-size: 16px }`, body и `.bg-section p` = `1rem` |
| **Контрастность** | Не менее **4.5:1** для текста ([WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)) | Основной `#020827` на белом; вторичный `#4B5563`; ссылки `#0B5345` (не mint `#9FE29E` на светлом) |
| **Ширина строки** | **60–80 символов** оптимально | `max-width: 70ch` на `.article-text`, lead, snippet-answer |
| **Межстрочный интервал** | **1.5–1.7** | `line-height: 1.6–1.65` для body и статей |

**Проверка контраста (светлый фон #FFFFFF):**

| Элемент | Цвет | ≈ ratio |
|---------|------|--------|
| Основной текст | `#020827` | > 15:1 ✅ |
| Вторичный / meta | `#4B5563` | ~7:1 ✅ |
| Ссылки в статьях | `#0B5345` | ~7:1 ✅ |
| Акцент «Краткий ответ» | `#047857` | ~5.5:1 ✅ |

Mint `#9FE29E` на белом — **не для текста** (декор / CTA-кнопки / тёмный footer).

---

## Мобильный UX (Apple HIG / Material)

| Критерий | Правило | Реализация в `styles.css` |
|----------|---------|---------------------------|
| **Touch targets** | Кнопки и ссылки ≥ **44×44 px** | `.btn`, `.nav-link`, `.navbar-toggler`, `.btn-close`, `.btn-news-link`, footer links |
| **Горизонтальная прокрутка** | Страница не скроллится по X | `html, body { overflow-x: clip }`; `.news-section { overflow-x: clip }`; таблицы — scroll внутри `.timeline-container-full`, `.seo-table-wrap` |
| **Текст** | Не обрезается, не наезжает | `overflow-wrap: break-word`; hero-кнопки `white-space: normal` на mobile |
| **Формы** | Удобно с телефона | `input/textarea`: `min-height: 44px`, `font-size: 16px` (без zoom iOS); форма на `about#contact-form` — full-width submit |

**Проверка:** DevTools → iPhone SE / 375px — нет горизонтального scrollbar; tap-зоны кнопок ≥ 44px; поля формы не вызывают auto-zoom.

---

## 1. Таблица: страница → запрос → точный ответ

| Страница | Title (`<title>`, симв.) | Точный запрос пользователя | Прямой ответ, который даём | Тип | Статус |
|----------|--------------------------|----------------------------|----------------------------|-----|--------|
| `index.html` | Федеративное обучение и Big Data on-premise — DigiTrack 2026 (60) | digitrack / диджитрек / кто такой DigiTrack | DigiTrack (ООО «ДТ») — российский разработчик ПО для федеративного обучения и on-premise платформ данных; два продукта: Confidential Computing и Big Data Platform | N+I бренд | index |
| `federated-learning.html` | DigiTrack FL: федеративное обучение для банков — пилот 2 нед (60) | федеративное обучение для банков / платформа федеративного обучения купить | **H1:** DigiTrack FL — платформа федеративного обучения для банков. Ответ: коммерческая платформа FL (VFL, HFL, Federated XGBoost) on-premise; данные не уходят за периметр; пилот 1–2 недели | C продукт FL | index |
| `data-platform.html` | Big Data on-premise от 600 000 ₽ — Dev/Test бесплатно (53) | big data platform on-premise / платформа данных для банков купить | **H1:** DigiTrack BDP — платформа данных on-premise для банков. Ответ: enterprise on-premise (Hadoop, Spark, Kafka, Delta Lake) на Astra Linux, 1 ПБ+, zero downtime | C продукт BDP | index |
| `partnership.html` | Партнёрство в федеративном обучении: пилот за 6 месяцев (55) | партнёрство федеративное обучение / стать дата-партнёром FL | Можно стать дата-партнёром DigiTrack: совместные модели без обмена сырыми данными; этапы пилота и условия на странице | C партнёрство | index |
| `learning-types.html` | VFL и HFL: в чём разница — таблица из 5 критериев [2026] (56) | **vfl hfl разница** / vfl что это | **Канон.** H1: VFL и HFL: в чём разница. Определения + таблица; → дочка: кейс финсектора | I справочник | index |
| `blog/articles/vfl-or-hfl.html` | VFL или HFL для банков: антифрод, скоринг, PSI [Кейс] (53) | vfl или hfl для банка / финсектор | **Дочка.** Прикладной кейс финтеха; не равный справочнику; в конце CTA на продукт FL | I кейс | index |
| `blog.html` | Блог DigiTrack: 15 статей о FL, Big Data и 152-ФЗ [2026] (56) | блог федеративное обучение / статьи big data platform | Хаб статей по FL, VFL/HFL, BDP, 152-ФЗ и on-premise AI | N хаб | index |
| `about.html` | DigiTrack: 12 FAQ, 7 этапов внедрения и контакты в Москве (57) | digitrack о компании / контакты digitrack | ООО «ДТ» — разработчик CC и BDP; на одной странице: о компании → процесс заказа → FAQ → контакты/реквизиты | T+N | index |
| `about.html#contacts` | *(как `about.html`)* | digitrack контакты / реквизиты ООО ДТ | Email, телефон, юр. адрес и реквизиты для заявки и договора | T | якорь |
| `data-platform.html#licensing` | *(как `data-platform.html`)* | тарифы big data platform / лицензия bdp | **MOFU.** Standard / Enterprise / Custom — цены «от», что входит. Ссылка на методику TCO | C тарифы BDP | якорь |
| `about.html#faq` (стоимость) | *(как `about.html`)* | сколько стоит digitrack | **BOFU.** Один короткий ответ: зависит от конфигурации → заявка → КП. Без цифр и тарифов | T конверсия | якорь |
| `about.html#process` | *(как `about.html`)* | как заказать digitrack / этапы внедрения | Канон: 7 шагов от заявки до сопровождения | I процесс | якорь |
| `index.html#proof` / тизеры | *(как `index.html`)* | digitrack кейсы / цифры | Доказательства: объёмы, сроки пилота, отрасли — кратко, с ссылкой на полный процесс/FAQ | I proof | якорь |
| `vacancies.html` | Вакансии DigiTrack: разработка FL и Big Data on-premise (55) | вакансии digitrack / работа федеративное обучение | Открытые вакансии в команде FL / Big Data | HR | index |
| `site-map.html` | Карта сайта DigiTrack: продукты, блог, FAQ и контакты (53) | карта сайта digitrack | Полная структура URL: продукты, блог, компания, служебные | N служебная | index |
| `documents.html` | Документация DigiTrack FL: скачать после авторизации (52) | документация digitrack скачать | Доступ к документации ПО (после авторизации) | N/T | noindex* |
| `expert-review.html` | Экспертная проверка DigiTrack: стенд и материалы для оценки (59) | экспертная проверка ПО digitrack | Материалы для экспертной оценки: скачивание, стенд, развёртывание | N | noindex* |
| `login.html` | Вход в документацию DigiTrack FL — Confidential Computing (57) | вход документы digitrack | Служебный вход по паролю к документам | N | noindex |
| `contacts.html` | *(удалена)* | *(удалена)* | Бывший stub → используйте `about#contacts` | — | gone |
| `voprosy.html` | *(удалена)* | *(удалена)* | Бывший stub → `about#faq` | — | gone |
| `kak-my-rabotaem.html` | *(удалена)* | *(удалена)* | Бывший stub → `about#process` | — | gone |
| `blog/articles/fl-guide.html` | Что такое FL: 7 принципов, риски и применение [Обзор] (53) | федеративное обучение это / что такое федеративное обучение | **H1:** Что такое федеративное обучение: принципы, применение, риски. Title + `[Обзор]`. Ответ: обучение моделей без передачи сырых ПДн — принципы, применение, риски | I pillar FL | index |
| `blog/articles/confidential-computing-152.html` | 152-ФЗ и федеративное обучение: AI без утечки ПДн [2026] (56) | федеративное обучение 152-фз / ai и персональные данные законно | При 152-ФЗ/GDPR регулятор смотрит, где обрабатываются ПДн и можно ли доказать, что исходные данные не покидали контур; ответ — Confidential Computing + FL on-premise | I комплаенс | index |
| `blog/articles/fate-flower-nvflare.html` | FATE vs Flower vs NVFlare: 10 критериев выбора FL [2026] (56) | fate vs flower vs nvflare / фреймворк федеративного обучения выбрать | Фреймворк выбирают по сценарию, модели угроз и российскому стеку; сравнение FATE, Flower, NVFlare и DigiTrack + 10 критериев для тендера | I сравнение | index |
| `blog/articles/federated-xgboost-experiments.html` | Federated XGBoost vs эмбеддинги: что безопаснее [2026] (54) | federated xgboost vs эмбеддинги | Эмбеддинги можно инвертировать; Federated XGBoost считает сплиты без отдачи исходных записей — выше качество скоринга на партнёрских данных при меньшем риске утечки | I техника | index |
| `blog/articles/fl-antifraud.html` | Антифрод банков на FL: общая модель без обмена данными (54) | федеративное обучение антифрод / совместный антифрод банков | Банки могут учить общую антифрод-модель без обмена транзакциями; изолированный антифрод видит только свой кусок; FL закрывает «слепые зоны» между участниками | I use-case | index |
| `blog/articles/fl-sandbox-or-embeddings.html` | Sandbox, эмбеддинги или FL: 3 пути без выгрузки ПДн (51) | sandbox или федеративное обучение или эмбеддинги | Три пути обмена сигналом без полной выгрузки: sandbox, эмбеддинги, FL — разные юр. конструкты и модели угроз; выбор = компромисс права и качества модели | I архитектура | index |
| `blog/articles/homomorphic-encryption.html` | Гомоморфное шифрование в ML: когда работает, когда нет (54) | гомоморфное шифрование машинное обучение / he в ml | HE считает на шифротексте без раскрытия данных; для ИБ идеален, для ML — дорого и точечно, не «вся модель под FHE» | I PPML | index |
| `blog/articles/bdp-guide.html` | Big Data Platform: 6 компонентов стека и риски [Обзор] (54) | big data platform что это / платформа данных для ai | **H1:** Что такое Big Data Platform: принципы, архитектура, риски. Title + `[Обзор]`. Ответ: инфраструктура данных для аналитики и AI — принципы, архитектура, риски выбора | I pillar BDP | index |
| `blog/articles/ai-ready-platform.html` | AI-ready платформа: 7 компонентов для корпоративного AI (55) | ai-ready data platform / инфраструктура для корпоративного ai | AI-ready — не «GPU на озере», а связка: объём данных, Delta Lake, мультиверсионный Spark/Python, Kafka, оркестрация, Jupyter и zero downtime | I AI-ready | index |
| `blog/articles/choose-bdp-15.html` | Как выбрать Big Data Platform: 15 критериев для CIO (51) | как выбрать big data platform / критерии выбора bdp | 15 критериев enterprise: Open Source, Astra Linux, HA, Zero Downtime, мультиверсионность, Delta Lake, CDC, безопасность, прозрачный TCO | I+C выбор | index |
| `blog/articles/ha-big-data-platform.html` | Отказоустойчивая Big Data без простоя: HA и rolling restart (59) | отказоустойчивая big data / zero downtime hadoop | HA NameNode/YARN/Hive/Patroni + rolling restart с drain и health-check; прод без окна простоя | I надёжность | index |
| `blog/articles/opensource-enterprise.html` | Open Source Big Data: суверенитет стека для enterprise (54) | open source enterprise / цифровой суверенитет big data | Open Source в enterprise — вопрос суверенитета (стек, ОС, реестр ПО), а не только экономии на лицензии | I суверенитет | index |
| `blog/articles/scale-to-federated.html` | Масштабирование Big Data: от 1 кластера до федерации [2026] (59) | масштабирование big data кластера / федерация кластеров | От одного кластера к федерации: scale-out Data Nodes, Delta Lake, HA, Ansible, rolling restart — рост без простоя; дальше — мост к FL | I масштаб | index |
| `blog/articles/tco-big-data.html` | TCO Big Data: формула и 5 статей расходов за 3–5 лет [Обзор] (60) | tco big data / как считать стоимость платформы | **TOFU.** Методика: формула TCO, переменные CapEx/OpEx, чек-лист. Без цен. CTA → расчёт TCO | I методика | index |

\*documents / expert-review — в robots могут быть ограничены.

---

## 2. Пересечения primary-интентов

Группы, где **несколько URL претендуют на одну задачу пользователя**.

### 2.1. Конфликт / каннибализация (нужно развести)

| Интент / задача | Страницы-конкуренты | Проблема | Как развести |
|-----------------|---------------------|----------|--------------|
| **Что такое FL** | `federated-learning.html` ↔ `fl-guide.html` | Product и pillar оба отвечают на «федеративное обучение» | **Сделано:** product Title/H1 = «DigiTrack FL — платформа федеративного обучения для банков»; pillar = «Что такое федеративное обучение: принципы, применение, риски» + Title `[Обзор]`; бренд только в CTA статьи |
| **VFL vs HFL** | `learning-types.html` ↔ `vfl-or-hfl.html` | Два URL на «vfl hfl разница» | **Сделано:** learning-types = канон (Title/H1 «в чём разница», `rel=canonical`, WebPage keywords); → дочка «кейс финсектора»; статья не ссылается как на равную, CTA → продукт |
| **Что такое / обзор BDP** | `data-platform.html` ↔ `bdp-guide.html` | Product vs pillar | **Сделано:** product Title/H1 = «DigiTrack BDP — платформа данных on-premise для банков»; guide = «Что такое Big Data Platform: принципы, архитектура, риски» + Title `[Обзор]` |
| **Выбор BDP / критерии** | `data-platform.html` ↔ `choose-bdp-15.html` | Оба commercial-informational | Статья = 15 критериев; продукт = оффер DigiTrack под этими критериями |
| **TCO / стоимость** | `tco-big-data.html` ↔ `data-platform#licensing` ↔ `about#faq` | Три ответа про цену | **Сделано:** TOFU = методика (статья); MOFU = тарифы «от» (#licensing); BOFU = короткий ответ + КП (FAQ) |
| **Как заказать / этапы** | `index` тизеры ↔ `about#process` ↔ stub | Дубль процесса | Index = тизер; about = канон 7 шагов; stub = soft-redirect → about |
| **FAQ** | `about#faq` ↔ stub `voprosy` | Дубль FAQ | about = полный канон; stub = soft-redirect → about |
| **О компании** | `index` ↔ `about` | Два «о нас» | Index = бренд + 2 продукта; about = канон компании + контакты/FAQ/процесс |
| **Документы / вход** | `login.html` ↔ `documents.html` | Одинаковый H1 «Документы» | **Сделано:** login H1 = «Вход в документацию»; оба `noindex` |
| **Sandbox vs FL vs эмбеддинги** | `fl-sandbox-or-embeddings` ↔ `federated-xgboost-experiments` | Оба про «эмбеддинги vs FL» | sandbox = юр/архитектурный выбор 3 путей; xgboost = техника бустинга vs векторов |
| **Масштаб / федерация** | `scale-to-federated` ↔ `federated-learning` ↔ `data-platform` | Статья тянет оба продукта | Primary = BDP scale-out; FL только secondary CTA |

### 2.2. Допустимая иерархия (не конфликт)

| Интент | Хаб (primary) | Поддержка (secondary OK) |
|--------|---------------|---------------------------|
| Купить FL | `federated-learning.html` | статьи FL → CTA на продукт |
| Купить BDP | `data-platform.html` | статьи BDP → CTA |
| VFL/HFL разница | `learning-types.html` | `vfl-or-hfl` = кейс финсектора (дочка) |
| Партнёрство | `partnership.html` | fl-antifraud, fl-guide |
| Контакты / КП | `about#contacts` | CTA со всех money-pages |
| Навигация по блогу | `blog.html` | related в статьях |
| HR | `vacancies.html` | блок join на about |

### 2.3. Свободные / без пересечения (уникальный primary)

| Страница | Уникальный интент |
|----------|-------------------|
| `fate-flower-nvflare` | сравнение фреймворков FL |
| `confidential-computing-152` | 152-ФЗ / GDPR + FL |
| `homomorphic-encryption` | HE в ML |
| `fl-antifraud` | антифрод use-case |
| `ha-big-data-platform` | HA / rolling restart |
| `opensource-enterprise` | open source / суверенитет |
| `ai-ready-platform` | AI-ready инфраструктура |
| `vacancies` | вакансии |
| `site-map` | карта сайта |
| `documents` / `expert-review` / `login` | служебные |

---

## 3. Сводка: где пересечения опасны

```
ВЫСОКИЙ риск каннибализации
  FL «что это»     : federated-learning  ×  fl-guide
  VFL/HFL          : learning-types (канон) → vfl-or-hfl (дочка)
  BDP «обзор»      : data-platform       ×  bdp-guide
  Процесс/FAQ      : index               ×  about  (× stubs)

СРЕДНИЙ риск
  TCO / стоимость   : tco (методика) → data-platform#licensing (тарифы) → about#faq (КП)
  Эмбеддинги vs FL : fl-sandbox × federated-xgboost

НИЗКИЙ / OK
  Статьи → продукт по CTA (иерархия, не дубль primary)
```

---

## 4. Что сделать с пересечениями

1. **Зафиксировать канон primary** для каждой задачи (колонка «как развести» в §2.1).  
2. **Title/H1** продукта ≠ title pillar (убрать одинаковые формулировки без уточнения роли).  
3. **Перелинковка**: со статьи «что это» — на продукт «внедрить»; с learning-types — на vfl-or-hfl как «подробнее для финсектора».  
4. **Stubs** не индексировать — в перелинковке только about/index якоря.  
5. **Не плодить** третий URL на тот же primary без смены задачи пользователя.  
6. **ЭПОС в статьях:** первый абзац после H1 = колонка «Прямой ответ» из §1 (убрать бренд-дисклеймер из первого экрана).

---

## 5. Сниппет и CTR (Title / Description / Schema)

**Title — самый важный элемент сниппета.** Рекомендуемая длина: **50–60 символов** для Google, **до 70 символов** для Яндекса.

**Формулы эффективного title:**

| Формула | Пример |
|---------|--------|
| **[Ключевой запрос] + [выгода]** | `Big Data on-premise от 600 000 ₽ — Dev/Test бесплатно` |
| **[Число] + [тема]** | `VFL и HFL: в чём разница — таблица из 5 критериев [2026]` |
| **[Вопрос]: инструкция** | `Как выбрать Big Data Platform: 15 критериев для CIO` |

**До/после title:** ❌ `DigiTrack FL 2026 — топ-платформа…` (67, без выгоды) → ✅ `DigiTrack FL: федеративное обучение для банков — пилот 2 нед` (60).

**Description — поддерживает title.** Рекомендуемая длина: **140–155 символов**. Не фактор ранжирования, но влияет на CTR. Раскрывает выгоды title: цифры, сроки, условия, CTA — без «воды» и клише.

**До/после description:** ❌ «FL для банков. Большой выбор. Низкие цены.» → ✅ «VFL, HFL on-premise по 152-ФЗ: данные не покидают периметр, пилот за 1–2 недели. Оставьте заявку на КП — info@digi-track.ru» (143).

| Элемент | Правило | Пример |
|---------|---------|--------|
| **Title** | **50–60** (Google), **≤70** (Яндекс); формулы выше; продукт = бренд + выгода; pillar = `[Обзор]` / `[Кейс]` | `DigiTrack FL: … — пилот 2 нед` (60) |
| **Description** | **140–155** симв.; поддерживает title; конкретные выгоды + CTA; синхрон `og:description`, `twitter:description` | «3 тарифа от 600k ₽, Dev/Test бесплатно…» (148) |
| **FAQPage** | 4–6 вопросов под основным сниппетом на money-страницах: `index`, FL, BDP, `learning-types`, `about` | Вопросы = реальные accordion / FAQ на странице |
| **BreadcrumbList** | Отдельный JSON-LD + видимые крошки; цепочка для статей через hub (`learning-types`, `blog.html`) | `Главная → Блог → [Обзор] FL` |

**Скрипт:** `scripts/apply_snippet_seo.py` — словари `TITLES` и `DESCRIPTIONS` для всех 27 URL; FAQ и BreadcrumbList правятся в HTML/schema вручную или через `integrate_schema_markup.py`.

**Не ломать:** intent split (§2), канон VFL/HFL, TCO-воронку (статья → `#licensing` → `about#faq`).
