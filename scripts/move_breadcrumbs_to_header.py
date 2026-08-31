#!/usr/bin/env python3
"""Move breadcrumb nav from standalone strip into page header (above H1)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BREADCRUMB_RE = re.compile(
    r"\n\s*<nav class=\"breadcrumb-nav\"[^>]*>\s*"
    r"(?:<div class=\"container\">\s*)?"
    r"(<ol class=\"breadcrumb[^\"]*\"[^>]*>.*?</ol>)\s*"
    r"(?:</div>\s*)?"
    r"</nav>\s*",
    re.DOTALL | re.IGNORECASE,
)

IN_HEADER_CLASS = "breadcrumb-nav breadcrumb-nav--in-header"


def wrap_breadcrumb(ol_html: str) -> str:
    return (
        f'        <nav class="{IN_HEADER_CLASS}" aria-label="Хлебные крошки">\n'
        f"          {ol_html.strip()}\n"
        f"        </nav>\n"
    )


def move_into_hero(html: str, breadcrumb_block: str) -> str:
    pattern = re.compile(
        r"(<section[^>]*\bhero-hero\b[^>]*>.*?<div class=\"container[^\"]*\"[^>]*>)\s*",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(html)
    if not m:
        return html
    insert_at = m.end()
    return html[:insert_at] + "\n" + breadcrumb_block + html[insert_at:]


def move_into_blog_hub(html: str, breadcrumb_block: str) -> str:
    pattern = re.compile(
        r"(<section[^>]*\bblog-hub-page\b[^>]*>\s*<div class=\"container\">)\s*",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(html)
    if not m:
        return html
    insert_at = m.end()
    return html[:insert_at] + "\n" + breadcrumb_block + html[insert_at:]


def move_into_blog_article(html: str, breadcrumb_block: str) -> str:
    pattern = re.compile(
        r"(<section[^>]*\bblog-article-page\b[^>]*>\s*<div class=\"container article-container\">)\s*",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(html)
    if not m:
        return html
    insert_at = m.end()
    return html[:insert_at] + "\n" + breadcrumb_block + html[insert_at:]


def move_into_main_container(html: str, breadcrumb_block: str) -> str:
    pattern = re.compile(
        r"(<main[^>]*>\s*<div class=\"container\">)\s*",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(html)
    if not m:
        return html
    insert_at = m.end()
    return html[:insert_at] + "\n" + breadcrumb_block + html[insert_at:]


def move_into_login_section(html: str, breadcrumb_block: str) -> str:
    pattern = re.compile(
        r"(<main>\s*<section[^>]*>\s*<div class=\"container\">)\s*",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(html)
    if not m:
        return html
    insert_at = m.end()
    return html[:insert_at] + "\n" + breadcrumb_block + html[insert_at:]


def strip_hero_content_offset(html: str) -> str:
    return re.sub(
        r'<div style="margin-top:\s*\d+px;">',
        "<div>",
        html,
        count=1,
    )


def process_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if "breadcrumb-nav--in-header" in html:
        return False

    m = BREADCRUMB_RE.search(html)
    if not m:
        return False

    ol_html = m.group(1)
    breadcrumb_block = wrap_breadcrumb(ol_html)
    html = html[: m.start()] + "\n\n  " + html[m.end() :]

    name = path.name
    rel = path.relative_to(ROOT).as_posix()

    if "blog/articles/" in rel:
        html = move_into_blog_article(html, breadcrumb_block)
    elif name == "blog.html":
        html = move_into_blog_hub(html, breadcrumb_block)
    elif name == "about.html":
        html = move_into_main_container(html, breadcrumb_block)
    elif name == "login.html":
        html = move_into_login_section(html, breadcrumb_block)
    elif "hero-hero" in html:
        html = move_into_hero(html, breadcrumb_block)
        if name in {"documents.html", "expert-review.html"}:
            html = strip_hero_content_offset(html)
    else:
        html = move_into_main_container(html, breadcrumb_block)

    if "breadcrumb-nav--in-header" not in html:
        return False

    path.write_text(html, encoding="utf-8")
    return True


def main() -> None:
    updated: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.name == "index.html":
            continue
        if "breadcrumb-nav" not in path.read_text(encoding="utf-8"):
            continue
        if process_file(path):
            updated.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(updated)} files:")
    for name in updated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
