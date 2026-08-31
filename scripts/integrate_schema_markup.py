#!/usr/bin/env python3
"""Integrate FAQ, HowTo and Article JSON-LD into DigiTrack HTML pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
BASE = "https://digi-track.ru"

HUB_SECTION = {
    "fl": "Федеративное обучение",
    "bdp": "Дата-платформа",
}

HUB_PAGE = {
    "fl": "federated-learning.html",
    "bdp": "data-platform.html",
}

NAV_INSERT = ""


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def patch_faq_schema_url(schema: dict) -> dict:
    schema = json.loads(json.dumps(schema))
    schema["url"] = f"{BASE}/about.html#faq"
    schema["@id"] = f"{BASE}/about.html#faqpage"
    return schema


def patch_howto_schema_url(schema: dict) -> dict:
    schema = json.loads(json.dumps(schema))
    schema["url"] = f"{BASE}/about.html#process"
    schema["@id"] = f"{BASE}/about.html#howto-order"
    return schema


def build_faq_accordion(questions: list[dict]) -> str:
    items = []
    for i, q in enumerate(questions, start=1):
        qid = f"f{i}"
        aid = f"fa{i}"
        answer = q["acceptedAnswer"]["text"]
        items.append(
            f"""          <div class="accordion-item faq-item">
            <h2 class="accordion-header" id="{qid}">
              <button class="accordion-button collapsed faq-question" type="button" data-bs-toggle="collapse" data-bs-target="#{aid}" aria-expanded="false" aria-controls="{aid}">
                {q["name"]}
              </button>
            </h2>
            <div id="{aid}" class="accordion-collapse collapse" aria-labelledby="{qid}" data-bs-parent="#faqAcc">
              <div class="accordion-body snippet-answer faq-answer">{answer}</div>
            </div>
          </div>"""
        )
    return "\n".join(items)


def build_howto_steps(steps: list[dict]) -> str:
    blocks = []
    for step in steps:
        blocks.append(
            f"""          <article class="glass pad-2x mb-3 howto-step" id="howto-step-{step['position']}">
            <h3 class="h5 howto-step-name"><span class="badge bg-success me-2">{step["position"]}</span>{step["name"]}</h3>
            <p class="howto-step-text mb-2">{step["text"]}</p>
            <p class="small mb-0"><a href="{step.get("url", "#")}">Подробнее →</a></p>
          </article>"""
        )
    return "\n".join(blocks)


def page_shell(title: str, description: str, canonical: str, body: str, schema_json: str, active: str) -> str:
    from apply_standard_footer import footer_html

    footer_block = footer_html("", compact=False)
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <meta name="description" content="{description}"/>
  <link rel="canonical" href="{canonical}"/>
  <meta name="robots" content="index, follow"/>
  <meta name="author" content="DigiTrack"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./styles.css"/>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <script type="application/ld+json">{schema_json}</script>
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
  <main class="py-6" style="padding-top: 7rem !important;">
{body}
  </main>
{footer_block}
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


def create_voprosy_page(faq_schema: dict) -> None:
    faq_schema = patch_faq_schema_url(faq_schema)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    (SCHEMA_DIR / "faq-schema.jsonld").write_text(dump_json(faq_schema) + "\n", encoding="utf-8")
    accordion = build_faq_accordion(faq_schema["mainEntity"])
    body = f"""    <div class="container">
      <h1 class="h2 fw-700 mb-2">Вопросы и ответы о DigiTrack</h1>
      <p class="snippet-answer geo-definition">Ответы об услугах, стоимости, сроках внедрения, гарантии и поддержке федеративного обучения и платформы данных.</p>
      <p class="small mb-4"><a href="kak-my-rabotaem.html">Как мы работаем →</a> · <a href="federated-learning.html">Федеративное обучение →</a> · <a href="data-platform.html">Дата-платформа →</a> · <a href="partnership.html">Партнёрство →</a> · <a href="blog.html">Блог →</a> · <a href="contacts.html">Контакты →</a></p>
      <section id="faq" class="mt-4">
        <div class="accordion" id="faqAcc">
{accordion}
        </div>
        <p class="small mt-4 mb-0">Не нашли ответ? Смотрите <a href="kak-my-rabotaem.html">этапы работы</a>, <a href="partnership.html">партнёрство</a> или <a href="contacts.html">напишите нам</a>.</p>
      </section>
    </div>"""
    html = page_shell(
        title="Вопросы и ответы — DigiTrack",
        description="FAQ: услуги, цены, сроки пилота FL, гарантия и поддержка Big Data Platform. info@digi-track.ru",
        canonical=f"{BASE}/voprosy.html",
        body=body,
        schema_json=dump_json(faq_schema),
        active="voprosy",
    )
    (ROOT / "voprosy.html").write_text(html, encoding="utf-8")


def create_process_page(howto_schema: dict) -> None:
    howto_schema = patch_howto_schema_url(howto_schema)
    (SCHEMA_DIR / "howto-schema.jsonld").write_text(dump_json(howto_schema) + "\n", encoding="utf-8")
    steps_html = build_howto_steps(howto_schema["step"])
    body = f"""    <div class="container" id="howto-order">
      <h1 class="h2 fw-700 mb-2">Как мы работаем</h1>
      <p class="snippet-answer">Пошаговый процесс заказа федеративного обучения, Big Data Platform или партнёрства с DigiTrack — от заявки до поддержки после запуска.</p>
      <p class="geo-timing mb-4">Ориентировочный срок полного цикла — 6 месяцев. Стоимость — от 1 000 000 ₽ без НДС.</p>
      <p class="small mb-4"><a href="voprosy.html">Вопросы и ответы →</a> · <a href="federated-learning.html">Федеративное обучение →</a> · <a href="data-platform.html">Дата-платформа →</a> · <a href="partnership.html">Партнёрство →</a> · <a href="documents.html">Документация →</a></p>
      <h2 class="h4 mb-3">Этапы работы</h2>
{steps_html}
      <p class="mt-4"><button type="button" class="btn btn-primary-gy" data-bs-toggle="modal" data-bs-target="#contactModal">Оставить заявку</button></p>
      <p class="small mt-3 mb-0">Подробнее о сроках и стоимости — в <a href="voprosy.html">разделе вопросов и ответов</a>. Материалы по продуктам — в <a href="blog.html">блоге</a>.</p>
    </div>"""
    html = page_shell(
        title="Как мы работаем — DigiTrack",
        description="7 шагов заказа услуг DigiTrack: заявка, брифинг, коммерческое предложение, договор, внедрение, приёмка, поддержка.",
        canonical=f"{BASE}/kak-my-rabotaem.html",
        body=body,
        schema_json=dump_json(howto_schema),
        active="process",
    )
    (ROOT / "kak-my-rabotaem.html").write_text(html, encoding="utf-8")


def word_count(html: str) -> int:
    m = re.search(r"<article[^>]*class=\"article-main\"[^>]*>(.*?)</article>", html, re.S)
    body = re.sub(r"<[^>]+>", " ", m.group(1) if m else html)
    return len(re.findall(r"[\w\u0400-\u04FF]+", body))


def article_schema_for(entry: dict, html_path: Path, html: str) -> dict:
    slug = entry["slug"]
    url = f"{BASE}/blog/articles/{slug}.html"
    title = entry["title"]
    excerpt = entry["excerpt"][:160]
    hub = entry["hub"]
    img_path = ROOT / "img" / "blog" / f"{slug}.jpg"
    image_url = f"{BASE}/img/blog/{slug}.jpg" if img_path.exists() else f"{BASE}/img/DataIcon.png"
    if ":" in title:
        alt = title.split(":", 1)[1].strip()[:120]
    else:
        alt = title[:120]
    kw_raw = entry.get("search", "")
    keywords = list(dict.fromkeys([HUB_SECTION[hub], *kw_raw.split()]))[:12]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "@id": f"{url}#article",
                "url": url,
                "inLanguage": "ru-RU",
                "headline": title,
                "alternativeHeadline": alt,
                "description": excerpt,
                "image": {
                    "@type": "ImageObject",
                    "url": image_url,
                    "width": 1200,
                    "height": 630,
                },
                "author": {
                    "@type": "Organization",
                    "@id": f"{BASE}/#author-team",
                    "name": "Команда DigiTrack",
                    "url": f"{BASE}/",
                    "parentOrganization": {"@id": f"{BASE}/#organization"},
                },
                "publisher": {
                    "@type": "Organization",
                    "@id": f"{BASE}/#organization",
                    "name": "DigiTrack",
                    "legalName": "Общество с ограниченной ответственностью «ДИДЖИТРЕК»",
                    "url": f"{BASE}/",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{BASE}/img/DataIcon.png",
                    },
                },
                "datePublished": "2025-06-15",
                "dateModified": "2026-08-01",
                "articleSection": HUB_SECTION[hub],
                "keywords": keywords,
                "about": [
                    {"@type": "Thing", "name": HUB_SECTION[hub]},
                    {"@type": "Thing", "name": title.split(":")[0].strip()},
                ],
                "wordCount": word_count(html),
                "proficiencyLevel": "Expert",
                "audience": {
                    "@type": "Audience",
                    "audienceType": "CTO, архитектор данных, ML-инженер, специалист по ИБ",
                },
                "isPartOf": {
                    "@type": "Blog",
                    "@id": f"{BASE}/blog.html#blog",
                    "name": "Блог DigiTrack",
                    "url": f"{BASE}/blog.html",
                },
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": url,
                    "url": url,
                    "name": f"{title} — DigiTrack",
                },
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [
                        "article.article-main h1",
                        "article.article-main .lead",
                        "article.article-main .direct-answer",
                        "article.article-main .snippet-answer",
                    ],
                },
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/index.html"},
                    {"@type": "ListItem", "position": 2, "name": "Блог", "item": f"{BASE}/blog.html"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": url},
                ],
            },
        ],
    }


ARTICLE_LD_COMMENT = "  <!-- Schema.org: TechArticle -->"
ARTICLE_LD_PATTERN = re.compile(
    r"(?:\s*<!-- Schema\.org: (?:BlogPosting \(Article\)|TechArticle) -->\n)*"
    r"\s*<script type=\"application/ld\+json\">.*?</script>",
    re.S,
)


def article_ld_block(schema: dict) -> str:
    return f"{ARTICLE_LD_COMMENT}\n  <script type=\"application/ld+json\">{dump_json(schema)}</script>"


def update_blog_articles(manifest: list[dict]) -> list[str]:
    updated = []
    by_slug = {e["slug"]: e for e in manifest}
    for path in sorted((ROOT / "blog" / "articles").glob("*.html")):
        slug = path.stem
        if slug not in by_slug:
            continue
        html = path.read_text(encoding="utf-8")
        schema = article_schema_for(by_slug[slug], path, html)
        new_ld = article_ld_block(schema)
        if ARTICLE_LD_PATTERN.search(html):
            html = ARTICLE_LD_PATTERN.sub(new_ld, html, count=1)
        else:
            html = html.replace("</head>", f"{new_ld}\n</head>", 1)
        html = ensure_article_related_links(html)
        path.write_text(html, encoding="utf-8")
        updated.append(path.name)
    return updated


ARTICLE_RELATED_LINKS = '''        <p class="small mt-3 mb-0 seo-related-links"><a href="../../about.html#faq">Вопросы и ответы →</a> · <a href="../../about.html#process">Как мы работаем →</a> · <a href="../../about.html">О компании →</a> · <a href="../../about.html#contacts">Контакты →</a></p>
'''


def ensure_article_related_links(html: str) -> str:
    if "seo-related-links" in html:
        return html
    return html.replace("      </article>", ARTICLE_RELATED_LINKS + "      </article>", 1)


def verify_blog_article_schemas(manifest: list[dict]) -> dict:
    required = [
        "headline", "alternativeHeadline", "description", "image", "author",
        "publisher", "datePublished", "dateModified", "articleSection",
        "keywords", "about", "wordCount", "mainEntityOfPage", "speakable",
        "proficiencyLevel", "audience",
    ]
    by_slug = {e["slug"]: e for e in manifest}
    report = {"ok": [], "fail": []}
    for path in sorted((ROOT / "blog" / "articles").glob("*.html")):
        slug = path.stem
        html = path.read_text(encoding="utf-8")
        head_block = re.search(r"<head>(.*?)</head>", html, re.S)
        in_head = bool(head_block and "application/ld+json" in head_block.group(1))
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        if not m:
            report["fail"].append({"file": path.name, "error": "нет JSON-LD"})
            continue
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError as exc:
            report["fail"].append({"file": path.name, "error": str(exc)})
            continue
        graph = data.get("@graph", [data])
        article = next((n for n in graph if n.get("@type") in ("TechArticle", "BlogPosting", "Article")), None)
        if not article:
            report["fail"].append({"file": path.name, "error": "нет TechArticle/Article"})
            continue
        missing = [f for f in required if f not in article]
        if missing or not in_head:
            report["fail"].append({"file": path.name, "missing": missing, "in_head": in_head})
        else:
            report["ok"].append(path.name)
    report["summary"] = f"{len(report['ok'])}/{len(by_slug)} статей с полной TechArticle Schema в <head>"
    return report


def update_nav(html: str, prefix: str = "") -> str:
    return html


def update_footer_links(html: str, prefix: str = "") -> str:
    return html


def update_all_nav_and_footers() -> int:
    import subprocess
    import sys

    subprocess.run([sys.executable, str(ROOT / "scripts" / "apply_standard_footer.py")], check=True)
    return 0


def add_index_links(html: str) -> str:
    needle = '<p class="snippet-answer">ООО «ДТ» — разработчик ПО для конфиденциальных вычислений'
    insert = '<p class="small mb-4"><a href="about.html#faq">Вопросы и ответы →</a> · <a href="about.html#process">Как мы работаем →</a> · <a href="blog.html">Блог →</a></p>'
    if insert in html:
        return html
    if needle in html:
        html = html.replace(needle, insert + "\n        " + needle, 1)
    return html


def update_contacts(html: str) -> str:
    needle = '<p class="mt-4"><a href="index.html" class="btn btn-primary-gy">На главную</a></p>'
    extra = """<p class="mt-3"><a href="about.html#faq">Вопросы и ответы →</a> · <a href="about.html#process">Как мы работаем →</a></p>
      """
    if "about.html#faq" in html:
        return html
    return html.replace(needle, extra + needle, 1)


def update_sitemap() -> None:
    """Ensure stub redirect pages are never in sitemap."""
    sitemap_path = ROOT / "sitemap.xml"
    text = sitemap_path.read_text(encoding="utf-8")
    for page in ("contacts.html", "voprosy.html", "kak-my-rabotaem.html"):
        text = re.sub(
            rf"\s*<url>\s*<loc>{re.escape(BASE)}/{re.escape(page)}</loc>.*?</url>",
            "",
            text,
            flags=re.S,
        )
    sitemap_path.write_text(text, encoding="utf-8")


def verify_pages() -> dict:
    results = {}
    checks = [
        ("voprosy.html", "FAQPage"),
        ("kak-my-rabotaem.html", "HowTo"),
    ]
    for page, schema_type in checks:
        html = (ROOT / page).read_text(encoding="utf-8")
        has_ld = 'type="application/ld+json"' in html and schema_type in html
        has_robots = "index, follow" in html
        results[page] = {"json_ld": has_ld, "indexable": has_robots}
    article_path = ROOT / "blog" / "articles" / "choose-bdp-15.html"
    ah = article_path.read_text(encoding="utf-8")
    results["blog/articles/choose-bdp-15.html"] = {
        "json_ld": "TechArticle" in ah and "speakable" in ah,
        "indexable": "index, follow" in ah,
    }
    return results


def main() -> None:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    faq = load_json(SCHEMA_DIR / "faq-schema.jsonld")
    howto = load_json(SCHEMA_DIR / "howto-schema.jsonld")
    manifest = json.loads((ROOT / "blog" / "articles-manifest.json").read_text(encoding="utf-8"))

    # Company content lives on about.html — do not recreate stub pages
    articles = update_blog_articles(manifest)
    nav_count = update_all_nav_and_footers()

    update_sitemap()
    for stub in ("contacts.html", "voprosy.html", "kak-my-rabotaem.html"):
        p = ROOT / stub
        if p.exists():
            p.unlink()
    verification = {"stubs_removed": True}
    article_audit = verify_blog_article_schemas(manifest)

    report = {
        "schemas_dir": str(SCHEMA_DIR),
        "pages_created": [],
        "stubs_policy": "deleted; use about.html#contacts|#faq|#process",
        "articles_updated": articles,
        "nav_files_updated": nav_count,
        "verification": verification,
        "article_schema_audit": article_audit,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--verify-articles":
        manifest = json.loads((ROOT / "blog" / "articles-manifest.json").read_text(encoding="utf-8"))
        print(json.dumps(verify_blog_article_schemas(manifest), ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--articles-only":
        manifest = json.loads((ROOT / "blog" / "articles-manifest.json").read_text(encoding="utf-8"))
        updated = update_blog_articles(manifest)
        audit = verify_blog_article_schemas(manifest)
        print(json.dumps({"articles_updated": updated, "audit": audit}, ensure_ascii=False, indent=2))
    else:
        main()
