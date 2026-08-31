#!/usr/bin/env python3
"""Move blog breadcrumbs directly under navbar; remove «← Все статьи» back link."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BREADCRUMB_BLOCK_RE = re.compile(
    r"\n\s*<nav class=\"breadcrumb-nav breadcrumb-nav--in-header\"[^>]*>\s*"
    r"(<ol class=\"breadcrumb[^\"]*\"[^>]*>.*?</ol>)\s*"
    r"</nav>\s*",
    re.DOTALL,
)

BACK_LINK_RE = re.compile(
    r"\n<a href=\"[^\"]*blog\.html\" class=\"btn-news-link article-back-link[^\"]*\"[^>]*>"
    r"← Все статьи</a>\s*",
    re.IGNORECASE,
)

NAV_END_RE = re.compile(r"</nav>\s*\n", re.IGNORECASE)


def wrap_under_nav(ol_html: str, container_prefix: str = "") -> str:
    prefix = "../../" if container_prefix == "article" else ""
    return (
        f"\n  <div class=\"breadcrumb-bar\">\n"
        f"    <div class=\"container\">\n"
        f"      <nav class=\"breadcrumb-nav breadcrumb-nav--under-nav\" aria-label=\"Хлебные крошки\">\n"
        f"        {ol_html.strip()}\n"
        f"      </nav>\n"
        f"    </div>\n"
        f"  </div>\n"
    )


def process_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if "breadcrumb-nav--under-nav" in html:
        return False

    m = BREADCRUMB_BLOCK_RE.search(html)
    if not m:
        return False

    ol_html = m.group(1)
    is_article = "blog/articles/" in path.as_posix()
    bar = wrap_under_nav(ol_html, "article" if is_article else "hub")

    html = html[: m.start()] + html[m.end() :]
    html = BACK_LINK_RE.sub("\n", html)

    nav_match = NAV_END_RE.search(html)
    if not nav_match:
        return False

    insert_at = nav_match.end()
    html = html[:insert_at] + bar + html[insert_at:]

    path.write_text(html, encoding="utf-8")
    return True


def main() -> None:
    targets = [ROOT / "blog.html", *sorted((ROOT / "blog" / "articles").glob("*.html"))]
    updated = [str(p.relative_to(ROOT)) for p in targets if p.exists() and process_file(p)]
    print(f"Updated {len(updated)} files:")
    for name in updated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
