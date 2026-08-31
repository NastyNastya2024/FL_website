#!/usr/bin/env python3
"""Revert header nav to pre-SEO menu; move new pages to footer column 3."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_EXTRA = re.compile(
    r"\n?\s*<li class=\"nav-item\"><a class=\"nav-link(?: active)?\" "
    r"href=\"(?:\.\./)*(?:voprosy|kak-my-rabotaem|about|contacts)\.html\">"
    r"(?:Вопросы и ответы|Как мы работаем|О нас|Контакты)</a></li>",
    re.I,
)

FOOTER_COL3_OLD = re.compile(
    r"<div class=\"col-6 col-lg-3\">\s*"
    r"<ul class=\"list-unstyled small m-0\">.*?"
    r"<li><a class=\"link-fade\" href=\"(?:\.\./)*site-map\.html\">Карта сайта</a></li>\s*"
    r"</ul>\s*</div>",
    re.S,
)

FOOTER_ABOUT_CONTACTS_IN_COL2 = re.compile(
    r"\n?\s*<li><a class=\"link-fade\" href=\"(?:\.\./)*about\.html\">О компании</a></li>"
    r"\n?\s*<li><a class=\"link-fade\" href=\"(?:\.\./)*contacts\.html\">Контакты</a></li>",
    re.I,
)

FOOTER_VOPROSY_KAK_IN_COL3 = re.compile(
    r"\n?\s*<li><a class=\"link-fade\" href=\"(?:\.\./)*voprosy\.html\">Вопросы и ответы</a></li>"
    r"\n?\s*<li><a class=\"link-fade\" href=\"(?:\.\./)*kak-my-rabotaem\.html\">Как мы работаем</a></li>",
    re.I,
)


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parent.parts)
    return "../" * depth if depth else ""


def footer_col3(prefix: str) -> str:
    p = prefix
    return f"""        <div class="col-6 col-lg-4">
          <div class="small text-mute-500 mb-2 fw-600">Компания</div>
          <ul class="list-unstyled small m-0">
            <li><a class="link-fade" href="{p}about.html">О компании</a></li>
            <li><a class="link-fade" href="{p}about.html#contacts">Контакты</a></li>
            <li><a class="link-fade" href="{p}about.html#faq">Вопросы и ответы</a></li>
            <li><a class="link-fade" href="{p}about.html#process">Как мы работаем</a></li>
            <li><a class="link-fade" href="{p}site-map.html">Карта сайта</a></li>
          </ul>
          <ul class="list-unstyled small m-0 mt-4 text-mute-500">
            <li><a href="#" class="link-fade" data-bs-toggle="modal" data-bs-target="#consentModal">Согласие на обработку данных</a></li>
            <li><a href="#" class="link-fade" data-bs-toggle="modal" data-bs-target="#legalModal">Правовая информация</a></li>
          </ul>
        </div>"""


def fix_footer(html: str, prefix: str) -> str:
    # brand column width
    html = html.replace('class="col-12 col-lg-6"', 'class="col-12 col-lg-4"', 1)
    html = html.replace('class="col-6 col-lg-3"', 'class="col-6 col-lg-4"', 2)

    html = FOOTER_ABOUT_CONTACTS_IN_COL2.sub("", html)
    html = FOOTER_VOPROSY_KAK_IN_COL3.sub("", html)

    # remove duplicate contacts in col3 if alone
    html = re.sub(
        r"\n?\s*<li><a class=\"link-fade\" href=\"(?:\.\./)*contacts\.html\">Контакты</a></li>",
        "",
        html,
        count=1,
    )

    m = FOOTER_COL3_OLD.search(html)
    if m:
        html = html[: m.start()] + footer_col3(prefix) + html[m.end() :]
    elif 'href="' + prefix + 'about.html">О компании</a></li>' not in html and "<footer" in html:
        # simple footers (voprosy, about) — append col if two-column only
        html = re.sub(
            r"(</footer>)",
            "",
            html,
            count=1,
        )
    return html


def fix_simple_footer(html: str, prefix: str) -> str:
    """Minimal footers on voprosy/kak/about/contacts generated pages."""
    if "footer-col-company" in html:
        return html
    old = """          <p class="small mb-2"><a class="link-fade" href="voprosy.html">Вопросы и ответы</a> · <a class="link-fade" href="kak-my-rabotaem.html">Как мы работаем</a> · <a class="link-fade" href="blog.html">Блог</a></p>"""
    if old in html:
        block = f"""      <div class="row g-4 footer-col-company">
        <div class="col-12 col-lg-4">
          <div class="small text-mute-500 mb-2 fw-600">Компания</div>
          <ul class="list-unstyled small m-0">
            <li><a class="link-fade" href="{prefix}about.html">О компании</a></li>
            <li><a class="link-fade" href="{prefix}about.html#contacts">Контакты</a></li>
            <li><a class="link-fade" href="{prefix}about.html#faq">Вопросы и ответы</a></li>
            <li><a class="link-fade" href="{prefix}about.html#process">Как мы работаем</a></li>
            <li><a class="link-fade" href="{prefix}site-map.html">Карта сайта</a></li>
            <li><a class="link-fade" href="{prefix}blog.html">Блог</a></li>
          </ul>
        </div>
      </div>"""
        html = html.replace(
            '      <div class="row g-4">\n        <div class="col-12 col-lg-6">',
            '      <div class="row g-4">\n        <div class="col-12 col-lg-4">',
            1,
        )
        html = html.replace(old, block)
    return html


def process_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html
    prefix = prefix_for(path)

    html = NAV_EXTRA.sub("", html)

    if "<footer" in html and "col-lg-3" in html or "footer-col-company" in html:
        html = fix_footer(html, prefix)
    html = fix_simple_footer(html, prefix)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = []
    for path in sorted(ROOT.rglob("*.html")):
        if process_file(path):
            updated.append(str(path.relative_to(ROOT)))
    print(json.dumps({"updated": updated, "count": len(updated)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
