#!/usr/bin/env python3
"""Add about/contacts nav, footer links, CTA blocks, and article cross-links."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_MARKER = 'href="{prefix}blog.html">Блог</a></li>'
NAV_INSERT = """          <li class="nav-item"><a class="nav-link{active_about}" href="{prefix}about.html">О нас</a></li>
          <li class="nav-item"><a class="nav-link{active_contacts}" href="{prefix}contacts.html">Контакты</a></li>
          <li class="nav-item"><a class="nav-link{active_blog}" href="{prefix}blog.html">Блог</a></li>"""

CTA_ROOT = """
  <section class="contact-cta-bar py-4 border-top border-ink-700" aria-label="Связаться с нами">
    <div class="container text-center text-lg-start">
      <p class="mb-0 snippet-answer"><strong>Остались вопросы?</strong> <a href="contacts.html">Свяжитесь с нами</a> — ответим в течение 1 рабочего дня.</p>
    </div>
  </section>
"""

CTA_ARTICLE = """
  <section class="contact-cta-bar py-4 border-top border-ink-700" aria-label="Связаться с нами">
    <div class="container text-center text-lg-start">
      <p class="mb-0 snippet-answer"><strong>Остались вопросы?</strong> <a href="../../contacts.html">Свяжитесь с нами</a> — ответим в течение 1 рабочего дня.</p>
    </div>
  </section>
"""

ARTICLE_LINKS_OLD = '<a href="../../contacts.html">Контакты →</a>'
ARTICLE_LINKS_NEW = (
    '<a href="../../about.html">О компании →</a> · '
    '<a href="../../contacts.html">Контакты →</a>'
)

INDEX_ABOUT_BLOCK = """        <div class="glass pad-2x mt-4 about-teaser">
          <h2 class="h5 fw-600 mb-2">Кто мы</h2>
          <p class="snippet-answer mb-2 about-mission">DigiTrack (ООО «ДТ») — команда разработчиков ПО для федеративного обучения и Big Data Platform on-premise. С 2023 года помогаем банкам и enterprise обучать модели без передачи персональных данных.</p>
          <p class="mb-0"><a href="about.html">Подробнее о компании →</a> · <a href="contacts.html">Контакты →</a></p>
        </div>"""


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parent.parts)
    return "../" * depth if depth else ""


def active_page(path: Path) -> str:
    return path.name.replace(".html", "")


def update_nav(html: str, path: Path) -> str:
    return html


def update_footer(html: str, prefix: str) -> str:
    return html


def insert_cta(html: str, path: Path) -> str:
    if "contact-cta-bar" in html or path.name in ("contacts.html", "login.html", "about.html"):
        return html
    cta = CTA_ARTICLE if path.parent.name == "articles" else CTA_ROOT
    prefix = prefix_for(path)
    if path.parent.name == "articles":
        cta = cta.replace("../../contacts.html", f"{prefix}contacts.html")
    for anchor in ("  <footer", "  <!-- FOOTER -->"):
        if anchor in html and "contact-cta-bar" not in html:
            return html.replace(anchor, cta + "\n\n" + anchor, 1)
    return html


def update_index(html: str) -> str:
    if "about-teaser" in html:
        return html
    needle = '<p class="snippet-answer">ООО «ДТ» — разработчик ПО для конфиденциальных вычислений:'
    if needle in html:
        return html.replace(needle, INDEX_ABOUT_BLOCK + "\n        " + needle, 1)
    return html


def update_article_links(html: str) -> str:
    if 'about.html">О компании' in html:
        return html
    return html.replace(ARTICLE_LINKS_OLD, ARTICLE_LINKS_NEW)


def main() -> None:
    updated = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.name == "about.html" and path.read_text(encoding="utf-8").startswith("<!doctype"):
            pass
        html = path.read_text(encoding="utf-8")
        original = html
        prefix = prefix_for(path)
        html = update_nav(html, path)
        html = update_footer(html, prefix)
        html = insert_cta(html, path)
        if path.name == "index.html":
            html = update_index(html)
        if path.parent.name == "articles":
            html = update_article_links(html)
        if html != original:
            path.write_text(html, encoding="utf-8")
            updated.append(str(path.relative_to(ROOT)))
    print(json.dumps({"updated": updated, "count": len(updated)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
