# SEO / AEO / GEO — рекомендации по улучшению digi-track.ru

> На основе аудита 28.08.2026 и документа `content-restructure.md`

---

## Критичные (P0) — внедрить в первую очередь

### 1. Заголовки и outline

| # | Проблема | Рекомендация | Страница |
|---|----------|--------------|----------|
| 1 | H1 «DigiTrack» без ключевых слов | `DigiTrack — федеративное обучение и платформа данных для enterprise` | index.html |
| 2 | Нет H1 на блоге | Добавить H1: «Блог DigiTrack — федеративное обучение и платформа данных» | blog.html |
| 3 | H2/H3 — утверждения, не вопросы | Переименовать по шаблонам из `content-restructure.md` (Что? Как? Почему? Сколько?) | index, FL, BDP, partnership |
| 4 | FAQ внутри accordion = H2 | Оставить вопросы в accordion, но добавить видимый блок «Краткий ответ» над каждым (≤40 слов) для GEO | все страницы с FAQ |
| 5 | H6 в футере/модалках | Перевести юридические подзаголовки на `<p>` или `<strong>`, не использовать H6 | все страницы |

### 2. Мета-теги

Обновить Title и Description по таблице из `content-restructure.md`. Общие правила:

- **Title:** 50–60 символов, primary keyword + бренд
- **Description:** 140–160 символов, CTA (email/заявка), LSI (VFL, on-premise, 152-ФЗ)
- Добавить `canonical` на всех коммерческих страницах
- Унифицировать `og:url` — сейчас относительные пути (`/federated-learning.html`)

**Пример для index.html:**
```html
<title>DigiTrack — федеративное обучение и платформа данных on-premise | ООО «ДТ»</title>
<meta name="description" content="Разработчик ПО для федеративного обучения и Big Data Platform без vendor lock-in. VFL, HFL, Hadoop/Spark on Astra Linux. Заявка: info@digi-track.ru"/>
<link rel="canonical" href="https://digi-track.ru/index.html"/>
```

### 3. Schema.org

- Подключить `seo/schema-updated.jsonld` на `index.html`:
  ```html
  <script type="application/ld+json" src="/seo/schema-updated.jsonld"></script>
  ```
- Удалить дублирующий inline Organization из `federated-learning.html` (конфликт с глобальным графом)
- На страницах FL / BDP / partnership — page-specific FAQPage (подмножество из глобального или локальный)
- Добавить `blog.html?q=` поддержку в JS для валидного SearchAction

### 4. Технические SEO-проблемы

| Проблема | Решение |
|----------|---------|
| `about.html` — пустая страница, нет meta | Удалить из sitemap или наполнить контентом «О компании» |
| `documents.html`, `expert-review.html` — нет description | Добавить noindex или meta description |
| Дубли FAQ (FL + partnership) | Объединить уникальные ответы; на FL — ссылка «Подробнее о партнёрстве» |
| Карточки новостей на FL ведут на blog.html, не на статьи | Заменить ссылки на конкретные `blog/articles/*.html` |

---

## Важные (P1) — контент и перелинковка

### 5. Структурированный контент в HTML

Внедрить из `content-restructure.md`:

1. **3+ сравнительные таблицы** (уже описаны):
   - FL: Sandbox vs Embeddings vs FL
   - BDP: слои технологического стека
   - BDP: тарифы лицензирования
   - FL: VFL vs HFL
   - FL: пакеты услуг

2. **Нумерованные списки** для этапов (FL: 4 этапа, partnership: M1–M6, BDP: data flow)

3. **Чек-листы** (collapsible `<details>` или accordion):
   - Готовность к FL
   - 15 критериев BDP (сокращённый)
   - Готовность к партнёрству

4. **GEO-блоки «Краткий ответ»** — `<p class="snippet-answer">` сразу под каждым H2-вопросом (≤40 слов)

### 6. Перелинковка

| Откуда | Куда | Анкор |
|--------|------|-------|
| index #products | federated-learning, data-platform | «Узнать больше →» |
| federated-learning #types | learning-types.html, vfl-or-hfl | «VFL или HFL — подробнее» |
| data-platform #licensing | tco-big-data, choose-bdp-15 | «Рассчитать TCO» |
| каждая статья блога | product page + pillar | CTA в конце |
| partnership | federated-learning, documents | «Технология FL», «Документация ПО» |

Создать **sitemap.xml** с приоритетами:
- 1.0: index, federated-learning, data-platform
- 0.8: partnership, blog, learning-types
- 0.6: blog/articles/*
- 0.3: vacancies, documents, expert-review

### 7. LSI-ключи в заголовках

| Страница | Primary | LSI для H2/H3 |
|----------|---------|---------------|
| index | федеративное обучение, платформа данных | confidential computing, on-premise, 152-ФЗ |
| FL | федеративное обучение для бизнеса | VFL, HFL, Federated XGBoost, гомоморфное шифрование |
| BDP | big data platform | Hadoop, Spark, vendor lock-in, TCO, Astra Linux |
| partnership | партнёрство федеративное обучение | монетизация данных, дата-партнёр, revenue share |
| blog | блог федеративное обучение | AI-ready, DataOps, антифрод, импортозамещение |

---

## Средний приоритет (P2) — AEO / GEO

### 8. Голосовой поиск (AEO)

- Все новые H2/H3 — только в форме вопроса
- Первый абзац после H2 — прямой ответ (не «В данной статье мы рассмотрим…»)
- FAQ минимум 7 вопросов на каждой коммерческой странице (BDP сейчас без FAQ — добавить)
- Speakable schema: разметить hero-lead и FAQ-блоки (`speakable` уже в schema-updated.jsonld)

### 9. AI-сниппеты (GEO)

| Intent | Формат на странице | Schema |
|--------|-------------------|--------|
| Что такое X? | `<p class="geo-definition">` ≤40 слов | FAQPage Question |
| Как сделать Y? | `<ol>` 5 шагов | HowTo |
| Где получить Z? | таблица контактов | ContactPoint + geo |
| Когда начать? | `<p class="geo-timing">` | FAQPage |
| Сколько стоит? | таблица тарифов + «индивидуальный расчёт» | Offer / OfferCatalog |

### 10. Блог

- Добавить hub-фильтры «FL» / «BDP» на blog.html (уже есть data-hub в manifest)
- Pillar-статьи (`fl-guide`, `bdp-guide`) — блок «Связанные материалы» (cluster links)
- Обновить карточки на index/FL/BDP — прямые ссылки на статьи, не на blog.html
- Реализовать чтение `?q=` в blog.html для SearchAction

---

## Низкий приоритет (P3) — расширение

### 11. Новые страницы

| Страница | Зачем |
|----------|-------|
| `/contacts.html` | Отдельный landing для «контакты digitrack» + LocalBusiness schema |
| `/portfolio.html` или `/cases.html` | Кейсы: антифрод, скоринг, BDP 1 ПБ — сейчас только в блоге |
| `/about.html` | «О компании» — команда, миссия, реквизиты (контент из index #team) |

### 12. Международное SEO

- `hreflang` не нужен (RU-only), но добавить `inLanguage: ru-RU` в schema (сделано)
- Проверить актуальность sameAs (LinkedIn, Twitter)

### 13. Performance / Core Web Vitals

- Hero-video: `preload="metadata"` уже есть — рассмотреть poster + lazy load на mobile
- Изображения блога: width/height attributes для CLS
- Минификация CSS для above-the-fold

---

## Чек-лист перед деплоем SEO-изменений

- [ ] Title/Description обновлены на 5 коммерческих страницах
- [ ] H1 содержит primary keyword на каждой странице
- [ ] H2/H3 переформулированы в вопросы (минимум 80% outline)
- [ ] FAQ ≥7 вопросов на index, FL, BDP, partnership
- [ ] ≥3 сравнительные таблицы в HTML
- [ ] schema-updated.jsonld подключён, валиден (Google Rich Results Test)
- [ ] sitemap.xml создан и отправлен в Яндекс.Вебмастер / GSC
- [ ] canonical на всех страницах
- [ ] Перелинковка: каждая коммерческая → 3+ статьи блога
- [ ] blog.html: H1 + SearchAction ?q= работает
- [ ] Дубли schema Organization удалены

---

## Инструменты проверки

1. **Google Rich Results Test** — schema-updated.jsonld, FAQPage, HowTo
2. **Яндекс.Вебмастер** — переобход страниц после изменений meta
3. **Screaming Frog** (или аналог) — проверка H1-H6, дублей title, broken links
4. **PageSpeed Insights** — Core Web Vitals после добавления таблиц/FAQ
5. **Ручной тест AEO** — голосовой запрос «Что такое федеративное обучение DigiTrack» → проверить featured snippet

---

## Ожидаемый эффект

| Метрика | Горизонт | Ожидание |
|---------|----------|----------|
| Индексация FAQ | 2–4 нед. | Rich snippets по 152-ФЗ, VFL, TCO |
| Органика по «федеративное обучение» | 2–3 мес. | Top-20 → Top-10 (конкуренция высокая) |
| AI-сниппеты (Perplexity, YandexGPT) | 1–2 мес. | Цитирование GEO-блоков ≤40 слов |
| CTR из SERP | 2–4 нед. | +15–25% за счёт улучшенных title/description |
| Внутренний link equity | 1 мес. | Рост индексации cluster-статей блога |

---

*Следующий шаг: поэтапное внедрение P0 в HTML-файлы по приоритету страниц (index → federated-learning → data-platform → partnership → blog).*
