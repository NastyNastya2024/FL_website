#!/usr/bin/env python3
"""Import Pillar/Cluster articles from content_DT with AI-search optimizations."""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ai_search_optimize import (
    build_author_box,
    build_keywords_line,
    build_schema_graph,
    optimize_article_html,
    strip_tags,
)

CONTENT_DT = Path(__file__).resolve().parents[2] / "content_DT"
SITE_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = SITE_ROOT / "blog" / "articles"

EXCLUDED_SLUGS = {"mlops-dataops"}

SITE_SLUGS = {
    "ai-ready-platform", "bdp-guide", "choose-bdp-15", "confidential-computing-152",
    "fate-flower-nvflare", "federated-xgboost-experiments", "fl-antifraud", "fl-guide",
    "fl-sandbox-or-embeddings", "ha-big-data-platform", "homomorphic-encryption",
    "opensource-enterprise", "scale-to-federated", "tco-big-data", "vfl-or-hfl",
}

HUB_LABEL = {"fl": "Федеративное обучение", "bdp": "Дата-платформа"}
HUB_LINK = {"fl": "../../federated-learning.html", "bdp": "../../data-platform.html"}
PILLAR = {"fl": "fl-guide", "bdp": "bdp-guide"}

CARD_IMAGES = {
    "fl-guide": "../../img/news1.jpeg",
    "fl-sandbox-or-embeddings": "../../img/news2.jpeg",
    "confidential-computing-152": "../../img/news3.jpeg",
    "vfl-or-hfl": "../../img/news1.jpeg",
    "federated-xgboost-experiments": "../../img/news2.jpeg",
    "homomorphic-encryption": "../../img/news3.jpeg",
    "fl-antifraud": "../../img/news1.jpeg",
    "fate-flower-nvflare": "../../img/news2.jpeg",
    "bdp-guide": "../../img/DataIcon.png",
    "tco-big-data": "../../img/img1.png",
    "choose-bdp-15": "../../img/img2.png",
    "ai-ready-platform": "../../img/DataIcon.png",
    "opensource-enterprise": "../../img/img1.png",
    "scale-to-federated": "../../img/img2.png",
    "ha-big-data-platform": "../../img/img1.png",
}

CONTACT_MODAL = '''
  <div class="modal fade" id="contactModal" tabindex="-1" aria-labelledby="contactModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title" id="contactModalLabel">Будем рады вашим вопросам<br>и предложениям</h6>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body text-center">
          <p class="mb-0">Отправляйте все предложения на <a href="mailto:info@digi-track.ru">info@digi-track.ru</a></p>
        </div>
      </div>
    </div>
  </div>
'''

NAV = '''  <nav class="navbar navbar-expand-lg navbar-dark sticky-top nav-glass" aria-label="Primary">
    <div class="container">
      <a class="navbar-brand fw-semibold" href="../../index.html">DigiTrack</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMain" aria-controls="navMain" aria-expanded="false" aria-label="Переключить меню">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navMain">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="../../index.html">Главная</a></li>
          <li class="nav-item"><a class="nav-link" href="../../federated-learning.html">Федеративное обучение</a></li>
          <li class="nav-item"><a class="nav-link" href="../../data-platform.html">Дата-платформа</a></li>
          <li class="nav-item"><a class="nav-link" href="../../partnership.html">Партнёрство</a></li>
          <li class="nav-item"><a class="nav-link" href="../../vacancies.html">Вакансии</a></li>
          <li class="nav-item"><a class="nav-link active" href="../../blog.html">Блог</a></li>
        </ul>
        <div class="d-flex gap-2">
          <button type="button" class="btn btn-primary-gy" data-bs-toggle="modal" data-bs-target="#contactModal">Узнать больше</button>
        </div>
      </div>
    </div>
  </nav>'''

FOOTER = '''  <footer class="py-5 mt-auto">
    <div class="container">
      <div class="row g-4">
        <div class="col-6 col-lg-3">
          <ul class="list-unstyled small m-0">
            <li><a class="link-fade" href="../../federated-learning.html">Федеративное обучение</a></li>
            <li><a class="link-fade" href="../../data-platform.html">Дата-платформа</a></li>
            <li><a class="link-fade" href="../../partnership.html">Партнёрство</a></li>
            <li><a class="link-fade" href="../../blog.html">Блог</a></li>
          </ul>
        </div>
        <div class="col-6 col-lg-3">
          <ul class="list-unstyled small m-0">
            <li><a class="link-fade" href="../../vacancies.html">Вакансии</a></li>
            <li><a class="link-fade" href="../../index.html">О компании</a></li>
          </ul>
        </div>
      </div>
      <div class="small text-mute-500 mt-4">© <span id="year"></span> ООО "ДТ"</div>
    </div>
  </footer>'''


def load_meta() -> dict:
    meta = {}
    for fname in ["content_fl.py", "content_bdp.py"]:
        src = (CONTENT_DT / fname).read_text(encoding="utf-8")
        for m in re.finditer(
            r'"slug": "([^"]+)",\s*"hub": "([^"]+)",\s*"product": "[^"]+",\s*"role": "[^"]+",\s*"cjm": "[^"]+",\s*"kind": "([^"]+)",\s*"cluster": "([^"]+)",\s*"platforms": "[^"]*",\s*"title": "([^"]+)"',
            src,
            re.S,
        ):
            slug, hub, kind, cluster, title = m.groups()
            if kind in ("Pillar", "Cluster"):
                meta[slug] = {"hub": hub, "kind": kind, "cluster": cluster, "title": title}
    return meta


def extract_main(html: str) -> str:
    m = re.search(r'<main class="article">(.*?)</main>', html, re.S)
    if not m:
        return ""
    body = m.group(1)
    body = re.sub(r'<p class="crumbs">.*?</p>\s*', "", body, flags=re.S)
    body = re.sub(r'<p class="meta">.*?</p>\s*', "", body, flags=re.S)
    body = re.sub(r'<details class="semantics">.*?</details>\s*', "", body, flags=re.S)
    return body.strip()


def sanitize_terminology(html: str) -> str:
    """Replace non-standard phrasing with correct FL terminology."""
    html = re.sub(
        r"вертикальн(?:ая|ой|ую)\s+федераци(?:я|и|ю|ей)",
        "VFL",
        html,
        flags=re.I,
    )
    return html


def fix_links(html: str) -> str:
    def repl(m):
        href, text = m.group(1), m.group(2)
        slug = Path(href).name.replace(".html", "")
        return f'<a href="{slug}.html">{text}</a>' if slug in SITE_SLUGS else text

    return re.sub(r'<a href="([^"]+\.html)">([^<]+)</a>', repl, html)


def filter_related(html: str) -> str:
    def repl_section(m):
        section = m.group(0)

        def link_repl(lm):
            slug = Path(lm.group(1)).name.replace(".html", "")
            return f'<li><a href="{slug}.html">{lm.group(2)}</a></li>' if slug in SITE_SLUGS else ""

        section = re.sub(r'<li><a href="([^"]+\.html)">([^<]+)</a></li>', link_repl, section)
        section = re.sub(r"<ul>\s*</ul>", "", section)
        return "" if "<li>" not in section else section

    return re.sub(r'<section class="related">.*?</section>', repl_section, html, flags=re.S)


def meta_description(title: str, lead: str) -> str:
    lead_plain = strip_tags(lead)
    if lead_plain:
        return lead_plain[:160]
    return title[:160]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    meta = load_meta()
    cards = []

    for slug in sorted(meta, key=lambda s: (0 if meta[s]["hub"] == "fl" else 1, 0 if meta[s]["kind"] == "Pillar" else 1, s)):
        if slug in EXCLUDED_SLUGS:
            continue
        raw = (CONTENT_DT / "articles" / f"{slug}.html").read_text(encoding="utf-8")
        title_m = re.search(r"<title>(.*?)</title>", raw)
        page_title = title_m.group(1) if title_m else meta[slug]["title"]
        main = filter_related(fix_links(sanitize_terminology(extract_main(raw))))

        info = meta[slug]
        hub = info["hub"]
        hub_label = HUB_LABEL[hub]
        pillar_slug = PILLAR[hub]
        if slug != pillar_slug:
            back_hub = f'<a href="{pillar_slug}.html" class="btn-news-link">{meta[pillar_slug]["title"]}</a>'
        else:
            back_hub = f'<a href="{HUB_LINK[hub]}" class="btn-news-link">{hub_label}</a>'

        lead_m = re.search(r'<p class="lead">(.*?)</p>', main, re.S)
        lead_text = lead_m.group(1) if lead_m else ""
        lead_html = f'<p class="lead text-mute-300 mb-3">{lead_text}</p>' if lead_m else ""
        if lead_m:
            main = main.replace(lead_m.group(0), "", 1)
        h1_m = re.search(r"<h1>(.*?)</h1>", main, re.S)
        h1 = h1_m.group(1) if h1_m else page_title
        if h1_m:
            main = main.replace(h1_m.group(0), "", 1)

        optimized_main, faq_items, howto = optimize_article_html(main, slug, hub, info["cluster"])
        keywords_html = build_keywords_line(slug, hub, info["cluster"])
        author_html = build_author_box(hub)
        description = meta_description(page_title, lead_text).replace('"', "&quot;")
        schema_html = build_schema_graph(
            slug=slug,
            title=page_title,
            description=description,
            hub=hub,
            hub_label=hub_label,
            faq_items=faq_items,
            howto=howto,
        )

        page = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{page_title} — DigiTrack</title>
  <meta name="description" content="{description}"/>
  <meta name="author" content="DigiTrack"/>
  <meta name="robots" content="index, follow"/>
  <link rel="canonical" href="https://digi-track.ru/blog/articles/{slug}.html"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../styles.css"/>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  {schema_html}
</head>
<body class="bg-deep">
{NAV}
<main>
  <section class="py-6 blog-section blog-article-page">
    <div class="container article-container">
      <article class="article-main" itemscope itemtype="https://schema.org/Article">
        <meta itemprop="headline" content="{page_title}"/>
        <meta itemprop="inLanguage" content="ru-RU"/>
        <span itemprop="author" itemscope itemtype="https://schema.org/Organization"><meta itemprop="name" content="DigiTrack"/></span>
        <h1 class="h3 fw-700 mb-3" itemprop="name">{h1}</h1>
        {author_html}
        {lead_html}
        {keywords_html}
        <div class="article-text" itemprop="articleBody">{optimized_main}</div>
        <div class="article-footer-link">{back_hub}</div>
      </article>
    </div>
  </section>
</main>
{FOOTER}
{CONTACT_MODAL}
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>
<script src="../../metrika.js" defer></script>
<script src="../../script.js" defer></script>
</body>
</html>
"""
        (OUT_DIR / f"{slug}.html").write_text(page, encoding="utf-8")

        excerpt = strip_tags(lead_text) if lead_text else ""
        if not excerpt:
            pm = re.search(r'<p class="direct-answer">(.*?)</p>', optimized_main, re.S)
            if pm:
                excerpt = strip_tags(pm.group(1)).replace("Краткий ответ:", "").strip()[:180]
        cards.append(
            {
                "slug": slug,
                "hub": hub,
                "kind": info["kind"],
                "title": info["title"],
                "excerpt": excerpt[:220] + ("…" if len(excerpt) > 220 else ""),
                "search": f"{info['title']} {info['cluster']} {hub_label}".lower(),
                "image": CARD_IMAGES.get(slug, "../../img/news1.jpeg"),
            }
        )

    (SITE_ROOT / "blog" / "articles-manifest.json").write_text(
        json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Generated {len(cards)} AI-optimized articles in {OUT_DIR}")


if __name__ == "__main__":
    main()
