#!/usr/bin/env python3
"""Reorder blog article above-the-fold blocks for EPOS / behavioral SEO."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "blog" / "articles"

EPOS_LEADS: dict[str, str] = {
    "fl-guide.html": (
        '<p class="lead direct-answer snippet-answer text-mute-300 mb-4">'
        "Федеративное обучение (FL) — обучение ML-моделей на данных нескольких организаций "
        "без передачи сырых ПДн: записи остаются on-premise, между участниками передаются "
        "только зашифрованные обновления модели (градиенты, веса, статистики сплитов)."
        "</p>"
    ),
    "bdp-guide.html": (
        '<p class="lead direct-answer snippet-answer text-mute-300 mb-4">'
        "Big Data Platform — on-premise инфраструктура для хранения и обработки больших данных "
        "(Hadoop, Spark, Kafka, Delta Lake): единый контур для аналитики, BI и корпоративного AI "
        "без выгрузки данных в облако."
        "</p>"
    ),
}

BLOCK_PATTERNS = {
    "author": r'<aside class="article-author"[^>]*>.*?</aside>',
    "product": r'<p class="article-product-inline[^>]*>.*?</p>',
    "keywords": r'<p class="article-keywords[^>]*>.*?</p>',
    "lead": r'<p class="lead[^>]*>.*?</p>',
}


def extract_block(html: str, key: str) -> tuple[str, str]:
    pat = BLOCK_PATTERNS[key]
    m = re.search(pat, html, flags=re.S)
    if not m:
        return html, ""
    return html[: m.start()] + html[m.end() :], m.group(0)


def normalize_lead(lead: str) -> str:
    if "direct-answer" not in lead:
        lead = lead.replace('class="lead', 'class="lead direct-answer snippet-answer', 1)
    if "mb-4" not in lead and "mb-3" in lead:
        lead = lead.replace("mb-3", "mb-4", 1)
    return lead


def fix_article(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html

    m = re.search(
        r"(<h1 class=\"h3 fw-700 mb-3\"[^>]*>.*?</h1>\s*)(.*?)(\s*<div class=\"article-text\")",
        html,
        flags=re.S,
    )
    if not m:
        return False

    prefix, middle, article_open = m.group(1), m.group(2), m.group(3)
    blocks: dict[str, str] = {}
    for key in ("author", "product", "keywords", "lead"):
        middle, block = extract_block(middle, key)
        if block:
            blocks[key] = block

    lead = blocks.get("lead") or EPOS_LEADS.get(path.name, "")
    if not lead:
        return False
    lead = normalize_lead(lead)

    meta_parts = [blocks[k] for k in ("author", "product", "keywords") if k in blocks]
    meta_html = "\n        ".join(meta_parts)
    if meta_parts:
        meta_footer = (
            '\n      <div class="article-meta-footer mt-4 pt-3 border-top">\n        '
            + meta_html
            + "\n      </div>"
        )
    else:
        meta_footer = ""

    new_intro = prefix + lead + article_open
    html = html[: m.start()] + new_intro + html[m.end() :]

    if meta_footer:
        for marker in (
            '<section class="article-sources',
            '<div class="article-footer-link">',
            '<section class="related">',
        ):
            if marker in html:
                html = html.replace(marker, meta_footer + "\n      " + marker, 1)
                break
        else:
            html = re.sub(
                r"(<div class=\"article-text\" itemprop=\"articleBody\">)(.*?)(</div>\s*<div class=\"article-footer-link\">)",
                lambda mm: mm.group(1) + mm.group(2) + meta_footer + "\n      " + mm.group(3),
                html,
                count=1,
                flags=re.S,
            )

    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = []
    for path in sorted(ARTICLES.glob("*.html")):
        if fix_article(path):
            updated.append(path.name)
    print(f"Updated {len(updated)} articles: {', '.join(updated)}")


if __name__ == "__main__":
    main()
