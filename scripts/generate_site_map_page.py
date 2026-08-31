#!/usr/bin/env python3
"""Generate human-readable site-map.html from sitemap structure."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://digi-track.ru"

MAIN_PAGES = [
    ("index.html", "Главная"),
    ("federated-learning.html", "Федеративное обучение"),
    ("data-platform.html", "Дата-платформа"),
    ("learning-types.html", "VFL и HFL — типы федеративного обучения"),
    ("partnership.html", "Партнёрство"),
    ("about.html", "О компании — контакты, FAQ, этапы работы"),
    ("blog.html", "Блог"),
]

SERVICE_PAGES = [
    ("vacancies.html", "Вакансии"),
    ("documents.html", "Документация на ПО"),
    ("expert-review.html", "Экспертная оценка"),
]


def list_items(items: list[tuple[str, str]]) -> str:
    rows = "\n".join(f'            <li><a href="{href}">{label}</a></li>' for href, label in items)
    return f"          <ul class=\"site-map-list\">\n{rows}\n          </ul>"


def article_items(manifest: list[dict], hub: str) -> str:
    items = [
        (f"blog/articles/{e['slug']}.html", e["title"])
        for e in manifest
        if e["hub"] == hub
    ]
    return list_items(items)


def build_html(manifest: list[dict]) -> str:
    from apply_standard_footer import footer_html

    fl = article_items(manifest, "fl")
    bdp = article_items(manifest, "bdp")
    main = list_items(MAIN_PAGES)
    service = list_items(SERVICE_PAGES)

    item_list = []
    for href, label in MAIN_PAGES + SERVICE_PAGES:
        item_list.append({"@type": "ListItem", "name": label, "url": f"{BASE}/{href}"})
    for e in manifest:
        item_list.append({
            "@type": "ListItem",
            "name": e["title"],
            "url": f"{BASE}/blog/articles/{e['slug']}.html",
        })

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{BASE}/site-map.html#webpage",
                "url": f"{BASE}/site-map.html",
                "name": "Карта сайта DigiTrack",
                "description": "Полная структура сайта digi-track.ru: продукты, услуги, блог и служебные разделы.",
                "inLanguage": "ru-RU",
                "isPartOf": {"@id": f"{BASE}/#website"},
            },
            {
                "@type": "ItemList",
                "@id": f"{BASE}/site-map.html#sitemap-list",
                "name": "Разделы сайта DigiTrack",
                "numberOfItems": len(item_list),
                "itemListElement": item_list,
            },
        ],
    }

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Карта сайта — DigiTrack</title>
  <meta name="description" content="Полная карта сайта digi-track.ru: федеративное обучение, платформа данных, блог, FAQ и контакты."/>
  <link rel="canonical" href="{BASE}/site-map.html"/>
  <meta name="robots" content="index, follow"/>
  <meta name="author" content="DigiTrack"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./styles.css"/>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, indent=2)}</script>
</head>
<body class="bg-deep">
  <nav class="navbar navbar-expand-lg navbar-dark sticky-top nav-glass" aria-label="Primary">
    <div class="container">
      <a class="navbar-brand fw-semibold" href="index.html">DigiTrack</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMain" aria-controls="navMain" aria-expanded="false" aria-label="Переключить меню">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navMain">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="index.html">Главная</a></li>
          <li class="nav-item"><a class="nav-link" href="federated-learning.html#tech">Федеративное обучение</a></li>
          <li class="nav-item"><a class="nav-link" href="data-platform.html">Дата-платформа</a></li>
          <li class="nav-item"><a class="nav-link" href="partnership.html">Партнёрство</a></li>
          <li class="nav-item"><a class="nav-link" href="vacancies.html">Вакансии</a></li>
          <li class="nav-item"><a class="nav-link" href="blog.html">Блог</a></li>
        </ul>
        <div class="d-flex gap-2">
          <button type="button" class="btn btn-primary-gy" data-bs-toggle="modal" data-bs-target="#contactModal">Узнать больше</button>
        </div>
      </div>
    </div>
  </nav>
  <main class="py-6 site-map-page" style="padding-top: 7rem !important;">
    <div class="container">
      <h1 class="h2 fw-700 mb-2">Карта сайта</h1>
      <p class="snippet-answer mb-2">Полная структура сайта DigiTrack (ООО «ДТ»): продукты, услуги, материалы блога и служебные страницы.</p>
      <p class="small mb-4"><a href="sitemap.xml">XML-карта для поисковых систем (sitemap.xml) →</a></p>

      <div class="row g-4">
        <div class="col-12 col-lg-6">
          <section class="glass pad-2x site-map-section" id="products">
            <h2 class="h5 fw-700 mb-3">Продукты и услуги</h2>
{main}
          </section>
          <section class="glass pad-2x site-map-section" id="service">
            <h2 class="h5 fw-700 mb-3">Служебные разделы</h2>
{service}
          </section>
        </div>
        <div class="col-12 col-lg-6">
          <section class="glass pad-2x site-map-section" id="blog-fl">
            <h2 class="h5 fw-700 mb-3">Блог — федеративное обучение</h2>
{fl}
          </section>
          <section class="glass pad-2x site-map-section" id="blog-bdp">
            <h2 class="h5 fw-700 mb-3">Блог — платформа данных</h2>
{bdp}
          </section>
        </div>
      </div>

      <p class="small mt-4 mb-0"><a href="index.html">На главную →</a> · <a href="about.html#contacts">Контакты →</a> · <a href="about.html#faq">Вопросы и ответы →</a></p>
    </div>
  </main>
{footer_html("", compact=False)}
  <div class="modal fade" id="contactModal" tabindex="-1" aria-labelledby="contactModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title" id="contactModalLabel">Будем рады вашим вопросам</h6>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body text-center">
          <p class="mb-0">Пишите на <a href="mailto:info@digi-track.ru">info@digi-track.ru</a></p>
        </div>
      </div>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def update_sitemap_xml() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    loc = f"{BASE}/site-map.html"
    if loc in text:
        return
    block = f"""  <url>
    <loc>{loc}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
"""
    text = text.replace("</urlset>", block + "</urlset>")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    manifest = json.loads((ROOT / "blog" / "articles-manifest.json").read_text(encoding="utf-8"))
    (ROOT / "site-map.html").write_text(build_html(manifest), encoding="utf-8")
    update_sitemap_xml()
    print("Created site-map.html and updated sitemap.xml")


if __name__ == "__main__":
    main()
