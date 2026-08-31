# Отчёт: аудит и оптимизация структуры DigiTrack для Schema.org

**Дата:** 28 августа 2026  
**Домен:** https://digi-track.ru  
**Скрипт аудита:** `python3 scripts/optimize_structure_schema.py`

---

## Итог

| Задача | Статус |
|--------|--------|
| 1. Единая папка `/schemas/` | ✅ |
| 2. TechArticle во всех 15 статьях | ✅ 15/15 |
| 3. BreadcrumbList на всех страницах (кроме главной) | ✅ 13/14 корневых + 15 статей |
| 4. HTML-карта `/site-map.html` | ✅ |
| 5. Перелинковка (voprosy, kak-my-rabotaem, blog) | ✅ |
| 6. Organization + WebSite + ItemList на главной | ✅ inline `@graph` |
| 7. Обновлён `sitemap.xml` (28 URL) | ✅ |
| 8. Валидность JSON-LD, абсолютные URL | ✅ 0 ошибок |

**Исключение:** `about.html` — редирект на главную (`noindex`), только JSON-LD BreadcrumbList без визуальных крошек.

---

## 1. Устранение дублирования схем

**Было:** схемы в `/schemas/` и `/public/schemas/`  
**Стало:** только `/schemas/`

```
schemas/
├── all-schemas.jsonld      # сводный @graph (шаблон)
├── article-schema.jsonld   # эталон TechArticle
├── faq-schema.jsonld       # FAQPage
├── home-schema.jsonld      # Organization + WebSite + WebPage + ItemList
└── howto-schema.jsonld     # HowTo
```

Папка `/public/schemas/` удалена. Коммерческие страницы (FL, BDP, партнёрство и др.) по-прежнему подключают расширенную продуктовую разметку из `/seo/schema-updated.jsonld` — это отдельный слой, не дублирующий `/schemas/`.

---

## 2. TechArticle во всех статьях блога

Для каждого файла `blog/articles/*.html` в `<head>` добавлен inline JSON-LD `@graph`:

1. **TechArticle** — полный набор полей:
   - `headline`, `alternativeHeadline`, `description`, `image`
   - `author`, `publisher`, `datePublished`, `dateModified`
   - `articleSection`, `keywords`, `about`, `wordCount`
   - `proficiencyLevel`, `audience` (специфика TechArticle)
   - `isPartOf` (Blog), `mainEntityOfPage`, `speakable`
2. **BreadcrumbList** — Главная → Блог → [Хаб FL/BDP] → [Заголовок статьи]

| # | Файл | Хаб |
|---|------|-----|
| 1 | `fl-guide.html` | FL |
| 2 | `confidential-computing-152.html` | FL |
| 3 | `fate-flower-nvflare.html` | FL |
| 4 | `federated-xgboost-experiments.html` | FL |
| 5 | `fl-antifraud.html` | FL |
| 6 | `fl-sandbox-or-embeddings.html` | FL |
| 7 | `homomorphic-encryption.html` | FL |
| 8 | `vfl-or-hfl.html` | FL |
| 9 | `scale-to-federated.html` | FL |
| 10 | `bdp-guide.html` | BDP |
| 11 | `ai-ready-platform.html` | BDP |
| 12 | `choose-bdp-15.html` | BDP |
| 13 | `ha-big-data-platform.html` | BDP |
| 14 | `opensource-enterprise.html` | BDP |
| 15 | `tco-big-data.html` | BDP |

Проверка: `python3 scripts/integrate_schema_markup.py --verify-articles` → **15/15 OK**

---

## 3. BreadcrumbList на всех страницах

**Главная (`index.html`)** — без хлебных крошек (корень иерархии).

**Корневые страницы** — визуальный `<nav class="breadcrumb-nav">` + отдельный JSON-LD `BreadcrumbList`:

| Страница | Цепочка |
|----------|---------|
| `federated-learning.html` | Главная → Федеративное обучение |
| `data-platform.html` | Главная → Дата-платформа |
| `partnership.html` | Главная → Партнёрство |
| `learning-types.html` | Главная → Федеративное обучение → VFL и HFL |
| `voprosy.html` | Главная → Вопросы и ответы |
| `kak-my-rabotaem.html` | Главная → Как мы работаем |
| `blog.html` | Главная → Блог |
| `contacts.html` | Главная → Контакты |
| `vacancies.html` | Главная → Вакансии |
| `documents.html` | Главная → Документация на ПО |
| `expert-review.html` | Главная → Экспертная оценка |
| `site-map.html` | Главная → Карта сайта |
| `login.html` | Главная → Вход |

**Статьи** — 4 уровня (см. п. 2), крошки в `@graph` и в HTML.

Скрипт: `scripts/add_breadcrumbs.py`

---

## 4. Страница `/site-map.html`

Создана иерархическая HTML-карта сайта:

- **Продукты и услуги** — главная, FL, BDP, VFL/HFL, партнёрство, FAQ, HowTo, блог, контакты
- **Служебные** — вакансии, документация, экспертная оценка
- **Блог FL** — 9 статей
- **Блог BDP** — 6 статей
- Ссылка на `sitemap.xml`
- Schema: `WebPage` + `ItemList` (27 пунктов) + `BreadcrumbList`

Регенерация: `python3 scripts/generate_site_map_page.py`

---

## 5. Перелинковка

| Место | Ссылки |
|-------|--------|
| `index.html` | `voprosy.html`, `kak-my-rabotaem.html`, `blog.html`, `site-map.html` |
| Все 15 статей | `../../voprosy.html`, `../../kak-my-rabotaem.html`, `../../contacts.html` |
| `voprosy.html` | `blog.html`, `kak-my-rabotaem.html`, продуктовые разделы |
| Навигация (все страницы) | пункты «Вопросы и ответы», «Как мы работаем» |

---

## 6. Organization + WebSite на главной

В `index.html` внешний `<script src="/seo/schema-updated.jsonld">` заменён на inline `@graph` из `schemas/home-schema.jsonld`:

- **Organization** (`#organization`) — реквизиты, logo, email, телефон, адрес
- **WebSite** (`#website`) — SearchAction на блог
- **WebPage** — описание главной
- **ItemList** (`#site-sections`) — 8 основных разделов с абсолютными URL

---

## 7. Обновление `sitemap.xml`

**28 URL** с приоритетами:

| Приоритет | Страницы |
|-----------|----------|
| 1.0 | `index.html`, `federated-learning.html`, `data-platform.html` |
| 0.9 | `voprosy.html`, `kak-my-rabotaem.html` |
| 0.8 | `partnership.html`, `blog.html`, `learning-types.html`, `contacts.html` |
| 0.6 | 15 статей блога |
| 0.5 | `site-map.html` |
| 0.3 | `vacancies.html`, `documents.html`, `expert-review.html` |

`about.html` и `login.html` в sitemap **не включены** (редирект / служебная страница).

---

## 8. Валидация

- Все inline JSON-LD парсятся без ошибок (`JSON.parse` / `json.loads`)
- **0 относительных URL** в полях `url`, `item`, `contentUrl`, `@id` внутри JSON-LD-блоков
- Базовый домен: `https://digi-track.ru`

Рекомендуется дополнительно прогнать в [Google Rich Results Test](https://search.google.com/test/rich-results):
- `index.html` — Organization, WebSite
- `voprosy.html` — FAQPage
- `kak-my-rabotaem.html` — HowTo
- любая статья — TechArticle, BreadcrumbList

---

## Изменённые и добавленные файлы

### Новые страницы
- `voprosy.html` — FAQPage (12 вопросов)
- `kak-my-rabotaem.html` — HowTo (7 шагов)
- `site-map.html` — HTML-карта сайта

### Схемы (`/schemas/`)
- `home-schema.jsonld` — главная
- `article-schema.jsonld` — обновлён до TechArticle
- `faq-schema.jsonld`, `howto-schema.jsonld`, `all-schemas.jsonld`

### Скрипты автоматизации
- `scripts/integrate_schema_markup.py` — TechArticle, FAQ/HowTo, перелинковка
- `scripts/add_breadcrumbs.py` — визуальные + JSON-LD крошки
- `scripts/generate_site_map_page.py` — HTML-карта + sitemap
- `scripts/optimize_structure_schema.py` — полный пайплайн и аудит

### Обновлённые HTML (выборочно)
- `index.html` — inline Organization/WebSite/ItemList, ссылки на FAQ и HowTo
- 15 × `blog/articles/*.html` — TechArticle + BreadcrumbList + ссылки
- 14 корневых страниц — BreadcrumbList (кроме `index.html`, частично `about.html`)
- `sitemap.xml` — 28 URL
- `styles.css` — `.breadcrumb-nav`, `.site-map-list`

### Удалено
- `/public/schemas/` (дубликат)

---

## Команды для повторного запуска

```bash
# Полный цикл оптимизации и аудита
python3 scripts/optimize_structure_schema.py

# Только статьи
python3 scripts/integrate_schema_markup.py --articles-only

# Проверка TechArticle
python3 scripts/integrate_schema_markup.py --verify-articles
```

---

## Структура сайта (после оптимизации)

```
/
├── index.html                    # Organization + WebSite + ItemList
├── federated-learning.html       # BreadcrumbList + product schema
├── data-platform.html
├── partnership.html
├── learning-types.html
├── voprosy.html                  # FAQPage
├── kak-my-rabotaem.html          # HowTo
├── blog.html
├── contacts.html
├── site-map.html                 # ItemList + BreadcrumbList
├── vacancies.html, documents.html, expert-review.html, login.html
├── about.html                    # redirect → index (noindex)
├── blog/
│   ├── articles-manifest.json
│   └── articles/*.html           # TechArticle × 15
├── schemas/                      # единый источник JSON-LD-шаблонов
├── seo/schema-updated.jsonld     # продуктовая разметка (коммерческие страницы)
└── sitemap.xml
```
