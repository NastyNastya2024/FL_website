# Crawl Budget Audit — DigiTrack (digi-track.ru)

**Дата:** 28 августа 2026  
**Объект:** статический сайт `/Users/a1/Documents/GitHub/FL_website`  
**Скрипт аудита:** `python3 scripts/crawl_budget_audit.py`

---

## Executive summary

| Метрика | Значение | Статус |
|---------|----------|--------|
| HTML-страниц всего | 30 | — |
| Индексируемых (`index, follow`) | 27 | ✅ |
| Закрытых (`noindex`) | 3 | ✅ |
| URL в `sitemap.xml` | **27** (после оптимизации) | ✅ |
| Конфликт sitemap ↔ noindex | **0** (было 2) | ✅ исправлено |
| Цепочки редиректов | 0 | ✅ |
| Пагинация | нет | ✅ |
| Query-параметры в ссылках | 0 (внутренних) | ✅ |
| Якорные дубли (#section) | есть, некритично | ⚠️ мониторинг |

**Вывод:** сайт компактный (27 приоритетных URL + 15 статей), crawl budget используется эффективно после удаления noindex-страниц из sitemap и настройки `robots.txt`.

---

## 1. Инвентаризация HTML-страниц

### 1.1 Индексируемые (27) — в sitemap

| Группа | Страницы | Priority |
|--------|----------|----------|
| Продукты | `index.html`, `federated-learning.html`, `data-platform.html` | 1.0 |
| FAQ / процесс | `voprosy.html`, `kak-my-rabotaem.html` | 0.9 |
| Конверсия | `partnership.html`, `blog.html`, `learning-types.html`, `contacts.html` | 0.8 |
| О компании | `about.html` | 0.7 |
| Служебные SEO | `site-map.html` | 0.5 |
| HR | `vacancies.html` | 0.3 |
| Блог | 15 × `blog/articles/*.html` | 0.6 |

### 1.2 Закрытые от индексации (3) — **не в sitemap**, Disallow в robots.txt

| Страница | Причина | robots meta |
|----------|---------|-------------|
| `login.html` | Авторизация, служебная | `noindex, nofollow` |
| `documents.html` | Техдокументация ПО (PDF-ссылки) | `noindex, nofollow` |
| `expert-review.html` | Временная страница для экспертов | `noindex, nofollow` |

### 1.3 Бывшие проблемы (исправлены)

| Проблема | Было | Стало |
|----------|------|-------|
| `documents.html` в sitemap при `noindex` | ✅ в sitemap | ❌ удалено |
| `expert-review.html` в sitemap при `noindex` | ✅ в sitemap | ❌ удалено |
| `about.html` — редирект на главную | meta refresh | полноценная страница, в sitemap |
| Дублирующий `<meta robots>` на expert-review | 2 тега | 1 тег |

---

## 2. Проверка ссылок (4xx / битые)

### 2.1 Внутренние HTML-ссылки

**Битых ссылок на HTML-страницы: 0.**

Все 30 HTML-файлов связаны перелинковкой; «сирота» только `login.html` (ожидаемо — закрытая страница).

### 2.2 Топ страниц по входящим ссылкам (link equity)

| Страница | Входящих ссылок |
|----------|-----------------|
| `index.html` | 116 |
| `contacts.html` | 100 |
| `blog.html` | 97 |
| `federated-learning.html` | 96 |
| `data-platform.html` | 86 |
| `partnership.html` | 73 |
| `about.html` | 57 |

### 2.3 Некритичные замечания по ассетам

| Ресурс | Статус | Рекомендация |
|--------|--------|--------------|
| `/favicon.ico`, `/favicon-*.png`, `/apple-touch-icon.png` | не в репозитории | добавить в деплой или заменить на `img/DataIcon.png` |
| `learning-types.html` → `img/hero.mp4` | файл отсутствует | заменить или удалить ссылку |
| `dns-prefetch` на `//fonts.googleapis.com` | ложное срабатывание аудита | не является HTML-страницей |

---

## 3. Редиректы

| Тип | Найдено |
|-----|---------|
| HTTP 301/302 (серверные) | не проверялись локально — статический `python -m http.server` |
| Meta refresh | **0** |
| JavaScript `location.replace` | **0** |

**Рекомендация для продакшена:** настроить на nginx/apache:
- `https://digi-track.ru/` → `index.html` (один канонический URL, без цепочек)
- без `www` ↔ без `www` (301 одним hop)

---

## 4. Дубли URL

### 4.1 Query-параметры

| Проверка | Результат |
|----------|-----------|
| Внутренние ссылки с `?page=`, `?filter=`, `?sort=` | **нет** |
| Пагинация блога | **нет** (все 15 статей на одной `blog.html`) |
| SearchAction в Schema (`blog.html?q=`) | только в JSON-LD, не в HTML-ссылках |

### 4.2 Якорные URL (#anchors)

Используются для навигации внутри длинных страниц, например:
- `federated-learning.html#tech`, `#faq`, `#algo`
- `index.html#contactModal` (модальное окно)

**Оценка:** не создают отдельных URL в sitemap; боты обычно канонизируют на URL без hash. Риск дублей — **низкий**.

### 4.3 Canonical

| Проверка | Результат |
|----------|-----------|
| Все индексируемые страницы | `<link rel="canonical">` с абсолютным URL `https://digi-track.ru/...` |
| Дублирующие canonical | **0** |
| `index.html` vs `/` | canonical = `index.html` — согласовать с серверным редиректом |

---

## 5. Пагинация

**Отсутствует.** Блог — flat list из 15 статей на `blog.html` + прямые URL статей в sitemap.  
Crawl budget на пагинацию не расходуется.

---

## 6. robots.txt — применённые настройки

Файл: `/robots.txt`

```
User-agent: *
Allow: /

Disallow: /login.html
Disallow: /documents.html
Disallow: /expert-review.html
Disallow: /scripts/
Disallow: /docs/
Disallow: /seo/
Disallow: /schemas/
Disallow: /*?page=
Disallow: /*?p=
Disallow: /*?filter=
Disallow: /*?sort=
...

Clean-param: page&p&filter&sort&q&utm_* /   # Yandex

Sitemap: https://digi-track.ru/sitemap.xml
```

### Зачем каждый Disallow

| Правило | Цель |
|---------|------|
| `/login.html` | не тратить crawl на форму входа |
| `/documents.html` | техdocs + PDF, уже `noindex` |
| `/expert-review.html` | закрытая экспертная зона |
| `/scripts/`, `/docs/`, `/seo/`, `/schemas/` | не контент, служебные файлы |
| `?page=`, `?filter=`, … | защита от будущих faceted URL |
| `Clean-param` | Яндекс не индексирует UTM и фильтры |

---

## 7. sitemap.xml — оптимизация

**До:** 29 URL (включая `documents.html`, `expert-review.html`)  
**После:** **27 URL** (только индексируемые)

Исключены автоматически в `scripts/optimize_structure_schema.py` через `NOINDEX_PAGES`.

Перегенерация:
```bash
python3 -c "import sys; sys.path.insert(0,'scripts'); from optimize_structure_schema import regenerate_sitemap; regenerate_sitemap()"
```

---

## 8. Crawl budget — оценка приоритетов

```
Высокий приоритет (бот должен обходить часто):
  index, federated-learning, data-platform, voprosy, kak-my-rabotaem

Средний:
  partnership, blog, learning-types, contacts, about, 15 статей

Низкий:
  vacancies, site-map.html

Не обходить:
  login, documents, expert-review, /docs/*.pdf, /scripts/
```

**Глубина сайта:** максимум 3 клика от главной до любой статьи (Главная → Блог → Статья).  
**HTML sitemap:** `site-map.html` — дополнительный путь для ботов.

---

## 9. Выполненные изменения

| Файл | Изменение |
|------|-----------|
| `robots.txt` | Disallow служебных страниц, query-параметров, Clean-param, Sitemap |
| `sitemap.xml` | Удалены `documents.html`, `expert-review.html` (27 URL) |
| `scripts/optimize_structure_schema.py` | `NOINDEX_PAGES` — автоисключение из sitemap |
| `expert-review.html` | Убран дублирующий meta robots |
| `scripts/crawl_budget_audit.py` | Скрипт повторного аудита |

---

## 10. Рекомендации (следующий этап)

1. **Продакшен-сервер:** один 301-hop для `/` ↔ `/index.html`, HTTPS, без лишних редиректов.
2. **Favicon:** добавить файлы в корень деплоя — убрать 404 на `/favicon.ico`.
3. **Google Search Console / Яндекс.Вебмастер:** отправить `sitemap.xml`, проверить «Покрытие» и «Исключённые».
4. **Log analysis:** мониторить crawl stats — доля 404, время ответа, частота обхода `/blog/articles/`.
5. **При росте блога (>50 статей):** рассмотреть `sitemap-index.xml` или paginated blog с rel=next/prev.
6. **documents.html:** оставить `noindex` + Disallow; PDF в `/docs/` уже закрыты через `Disallow: /docs/`.

---

## 11. Команды для повторной проверки

```bash
# Аудит ссылок и sitemap
python3 scripts/crawl_budget_audit.py

# Перегенерация sitemap (без noindex-страниц)
python3 -c "import sys; sys.path.insert(0,'scripts'); from optimize_structure_schema import regenerate_sitemap; print(len(regenerate_sitemap()))"

# Локальная проверка robots.txt
curl -s http://127.0.0.1:8765/robots.txt
```

---

*Отчёт сгенерирован в рамках оптимизации crawl budget для DigiTrack.*
