#!/usr/bin/env python3
"""Add visual breadcrumbs and BreadcrumbList JSON-LD to all pages except index."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://digi-track.ru"

HUB = {
    "fl": ("federated-learning.html", "Федеративное обучение"),
    "bdp": ("data-platform.html", "Дата-платформа"),
}

ROOT_TRAILS: dict[str, list[tuple[str | None, str]]] = {
    "federated-learning.html": [("index.html", "Главная"), (None, "Федеративное обучение")],
    "data-platform.html": [("index.html", "Главная"), (None, "Дата-платформа")],
    "partnership.html": [("index.html", "Главная"), (None, "Партнёрство")],
    "learning-types.html": [
        ("index.html", "Главная"),
        ("federated-learning.html", "Федеративное обучение"),
        (None, "VFL и HFL"),
    ],
    "voprosy.html": [("index.html", "Главная"), (None, "Вопросы и ответы")],
    "kak-my-rabotaem.html": [("index.html", "Главная"), (None, "Как мы работаем")],
    "blog.html": [("index.html", "Главная"), (None, "Блог")],
    "contacts.html": [("index.html", "Главная"), (None, "Контакты")],
    "vacancies.html": [("index.html", "Главная"), (None, "Вакансии")],
    "documents.html": [("index.html", "Главная"), (None, "Документация на ПО")],
    "expert-review.html": [("index.html", "Главная"), (None, "Экспертная оценка")],
    "site-map.html": [("index.html", "Главная"), (None, "Карта сайта")],
    "about.html": [("index.html", "Главная"), (None, "О компании")],
    "login.html": [("index.html", "Главная"), (None, "Вход")],
}


def trail_to_json_ld(trail: list[tuple[str | None, str]], prefix: str, page_url: str) -> dict:
    elements = []
    for i, (href, name) in enumerate(trail, start=1):
        item: dict = {"@type": "ListItem", "position": i, "name": name}
        if href:
            item["item"] = f"{BASE}/{prefix}{href}".replace(f"{BASE}//", f"{BASE}/")
        else:
            item["item"] = page_url
        elements.append(item)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "@id": f"{page_url}#breadcrumb",
        "itemListElement": elements,
    }


def trail_to_html(trail: list[tuple[str | None, str]], prefix: str, in_header: bool = True) -> str:
    items = []
    for i, (href, name) in enumerate(trail, start=1):
        if href:
            inner = f'<a itemprop="item" href="{prefix}{href}"><span itemprop="name">{name}</span></a>'
        else:
            inner = f'<span itemprop="name">{name}</span>'
        items.append(
            f'        <li class="breadcrumb-item{" active" if not href else ""}" '
            f'itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">\n'
            f"          {inner}\n"
            f'          <meta itemprop="position" content="{i}"/>\n'
            f"        </li>"
        )
    lis = "\n".join(items)
    nav_class = "breadcrumb-nav breadcrumb-nav--in-header" if in_header else "breadcrumb-nav"
    indent = "        " if in_header else "  "
    return f"""{indent}<nav class="{nav_class}" aria-label="Хлебные крошки">
{indent}  <ol class="breadcrumb mb-0" itemscope itemtype="https://schema.org/BreadcrumbList">
{lis}
{indent}  </ol>
{indent}</nav>"""


def page_url(path: Path, prefix: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return f"{BASE}/{rel}"


def insert_visual(html: str, nav_html: str) -> str:
    if "breadcrumb-nav" in html:
        return html
    m = re.search(r"</nav>\s*(<main\b[^>]*>)", html, flags=re.I)
    if m:
        main_tag = m.group(1)
        insert_at = m.start()
        return html[:insert_at] + f"</nav>\n\n{nav_html}\n\n  {main_tag}" + html[m.end() :]
    return html


def insert_json_ld(html: str, schema: dict) -> str:
    if '"@type": "BreadcrumbList"' in html or '"@type":"BreadcrumbList"' in html:
        return html
    block = f'  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>\n'
    return html.replace("</head>", block + "</head>", 1)


def article_trail(entry: dict) -> list[tuple[str | None, str]]:
    return [
        ("../../index.html", "Главная"),
        ("../../blog.html", "Блог"),
        (None, entry["title"]),
    ]


def process_file(path: Path, trail: list[tuple[str | None, str]], prefix: str) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html
    url = page_url(path, prefix)
    nav_html = trail_to_html(trail, prefix)
    html = insert_visual(html, nav_html)
    # Статьи уже содержат BreadcrumbList в @graph
    if path.parent.name == "articles":
        pass
    else:
        html = insert_json_ld(html, trail_to_json_ld(trail, prefix, url))
    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    manifest = json.loads((ROOT / "blog" / "articles-manifest.json").read_text(encoding="utf-8"))
    by_slug = {e["slug"]: e for e in manifest}
    updated = []

    for name, trail in ROOT_TRAILS.items():
        path = ROOT / name
        if path.exists() and process_file(path, trail, ""):
            updated.append(name)

    for path in sorted((ROOT / "blog" / "articles").glob("*.html")):
        entry = by_slug.get(path.stem)
        if not entry:
            continue
        if process_file(path, article_trail(entry), ""):
            updated.append(str(path.relative_to(ROOT)))

    print(json.dumps({"updated": updated, "count": len(updated)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
