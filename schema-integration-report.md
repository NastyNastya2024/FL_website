# Отчёт об интеграции Schema.org — DigiTrack

**Дата:** 28 августа 2026  
**Сайт:** https://digi-track.ru  
**Скрипт:** `scripts/integrate_schema_markup.py`

---

## 1. Проверка файлов схем

Единственный каталог JSON-LD для статического сайта — **`/schemas/`**:

| Файл | Назначение |
|------|------------|
| `/schemas/faq-schema.jsonld` | FAQPage → `voprosy.html` |
| `/schemas/howto-schema.jsonld` | HowTo → `kak-my-rabotaem.html` |
| `/schemas/article-schema.jsonld` | Эталон BlogPosting для статей |
| `/schemas/all-schemas.jsonld` | Объединённый `@graph` |

Дубликат `/public/schemas/` **удалён** (сборщик не используется).

---

## 2. Новые страницы со встроенной разметкой

| Страница | Schema.org | Способ вставки |
|----------|------------|----------------|
| `voprosy.html` | `FAQPage` (12 вопросов) | Inline `<script type="application/ld+json">` в `<head>` |
| `kak-my-rabotaem.html` | `HowTo` (7 шагов) | Inline JSON-LD в `<head>` |

**Примечание:** вместо англоязычных `faq.html` / `process.html` использованы русскоязычные URL:
- `voprosy.html` — вопросы и ответы
- `kak-my-rabotaem.html` — как мы работаем

На страницах размещён видимый контент (аккордеон FAQ и блоки этапов), соответствующий JSON-LD.

---

## 3. Статьи блога — Article / BlogPosting

Обновлены **15 статей** в `blog/articles/`:

- `@type`: `BlogPosting`
- Поля: `headline`, `alternativeHeadline`, `description`, `image`, `author`, `publisher`, `datePublished`, `dateModified`, `articleSection`, `keywords`, `about`, `wordCount`, `mainEntityOfPage`, `speakable`
- Дополнительно: `BreadcrumbList` в `@graph`

Данные берутся из `blog/articles-manifest.json`; количество слов считается автоматически по тексту статьи.

---

## 4. Навигация и внутренние ссылки

### Главное меню (26 HTML-файлов)

Добавлены пункты:
- **Вопросы и ответы** → `voprosy.html`
- **Как мы работаем** → `kak-my-rabotaem.html`

### Футер

На страницах с футером добавлены ссылки на `voprosy.html` и `kak-my-rabotaem.html`.

### Дополнительные перелинковки

| Страница | Изменение |
|----------|-----------|
| `index.html` | Блок ссылок на FAQ, процесс и блог в секции «О компании» |
| `contacts.html` | Ссылки на FAQ и «Как мы работаем» |
| `voprosy.html` | Ссылки на процесс, контакты, FL |
| `kak-my-rabotaem.html` | Ссылки на FAQ, партнёрство, документацию |

---

## 5. Индексация

| Проверка | Результат |
|----------|-----------|
| `robots.txt` | `Allow: /` — страницы **не закрыты** |
| `meta robots` на новых страницах | `index, follow` |
| `sitemap.xml` | Добавлены `voprosy.html` и `kak-my-rabotaem.html` (priority 0.9) |
| Статьи блога | Уже были в sitemap |

---

## 6. Локальная проверка (HTTP + JSON)

Сервер: `python3 -m http.server 8765`

| URL | JSON-LD | Тип схемы |
|-----|---------|-----------|
| `/voprosy.html` | ✅ | `FAQPage` |
| `/kak-my-rabotaem.html` | ✅ | `HowTo` |
| `/blog/articles/choose-bdp-15.html` | ✅ | `BlogPosting` + `speakable` |

Парсинг JSON-LD через Python (`json.loads`) — **без ошибок** на всех проверенных страницах.

---

## 7. Google Rich Results Test

Автоматическая проверка через Google Rich Results Test **не выполнялась** (требуется публичный URL после деплоя).

**После публикации на digi-track.ru проверьте вручную:**

1. https://search.google.com/test/rich-results  
2. URL для проверки:
   - `https://digi-track.ru/voprosy.html` → FAQPage
   - `https://digi-track.ru/kak-my-rabotaem.html` → HowTo
   - `https://digi-track.ru/blog/articles/choose-bdp-15.html` → Article

**В DevTools (F12):** Elements → `<head>` → найти `<script type="application/ld+json">`.

---

## 8. Что не изменялось

- Существующий контент страниц **не удалялся**
- Глобальная схема `/seo/schema-updated.jsonld` на коммерческих страницах **сохранена**
- Inline-схемы в статьях **расширены**, а не заменены пустым шаблоном

---

## 9. Повторный запуск

При обновлении manifest или schema-файлов:

```bash
python3 scripts/integrate_schema_markup.py
```

Скрипт пересоздаёт `voprosy.html`, `kak-my-rabotaem.html`, обновляет статьи блога и записывает JSON-LD в `/schemas/`.

---

## 10. Рекомендации после деплоя

1. Отправить обновлённый `sitemap.xml` в Яндекс.Вебмастер и Google Search Console
2. Запросить переобход `voprosy.html` и `kak-my-rabotaem.html`
3. Проверить Rich Results для FAQ и HowTo
4. При необходимости заменить `datePublished` / `dateModified` в статьях на реальные даты публикации
