#!/usr/bin/env python3
"""Audit and optimize DigiTrack site structure for Schema.org integration."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://digi-track.ru"

PRIORITY = {
    "index.html": 1.0,
    "federated-learning.html": 1.0,
    "data-platform.html": 1.0,
    "voprosy.html": 0.9,
    "kak-my-rabotaem.html": 0.9,
    "partnership.html": 0.8,
    "blog.html": 0.8,
    "learning-types.html": 0.8,
    "contacts.html": 0.8,
    "about.html": 0.7,
    "site-map.html": 0.5,
    "vacancies.html": 0.3,
}

NOINDEX_PAGES = {"login.html", "documents.html", "expert-review.html"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_json_ld_in_html(html: str) -> list[str]:
    errors = []
    for i, block in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)):
        try:
            data = json.loads(block)
            if isinstance(data, dict):
                _check_urls(data, errors)
        except json.JSONDecodeError as e:
            errors.append(f"JSON parse error block {i}: {e}")
    return errors


def _check_urls(obj, errors: list, path: str = "") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("url", "item", "contentUrl", "@id") and isinstance(v, str) and v.startswith("/"):
                errors.append(f"Relative URL at {path}.{k}: {v}")
            _check_urls(v, errors, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for j, item in enumerate(obj):
            _check_urls(item, errors, f"{path}[{j}]")


def regenerate_sitemap() -> list[str]:
    manifest = load_json(ROOT / "blog" / "articles-manifest.json")
    urls: list[tuple[str, float]] = []

    for name, prio in PRIORITY.items():
        if name in NOINDEX_PAGES:
            continue
        if (ROOT / name).exists():
            urls.append((f"{BASE}/{name}", prio))

    for entry in manifest:
        slug = entry["slug"]
        urls.append((f"{BASE}/blog/articles/{slug}.html", 0.6))

    # dedupe preserve order
    seen = set()
    unique = []
    for loc, prio in urls:
        if loc not in seen:
            seen.add(loc)
            unique.append((loc, prio))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio in unique:
        freq = "weekly" if prio >= 0.8 else "monthly" if prio >= 0.5 else "yearly"
        lines.extend([
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio:.1f}</priority>",
            "  </url>",
        ])
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return [u for u, _ in unique]


def update_index_schema() -> bool:
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")
    home = load_json(ROOT / "schemas" / "home-schema.jsonld")
    inline = f'  <script type="application/ld+json">{json.dumps(home, ensure_ascii=False, indent=2)}</script>'
    html, n = re.subn(
        r'\s*<script type="application/ld\+json" src="/seo/schema-updated\.jsonld"></script>',
        f"\n{inline}",
        html,
        count=1,
    )
    if n:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def audit() -> dict:
    report: dict = {
        "schemas_dir": str(ROOT / "schemas"),
        "public_schemas_exists": (ROOT / "public" / "schemas").exists(),
        "pages": {},
        "articles": {},
        "issues": [],
        "stats": {},
    }

    # HTML pages except index
    for path in sorted(ROOT.glob("*.html")):
        if path.name == "index.html":
            continue
        html = path.read_text(encoding="utf-8")
        report["pages"][path.name] = {
            "breadcrumb_visual": "breadcrumb-nav" in html,
            "breadcrumb_jsonld": "BreadcrumbList" in html,
            "json_ld_errors": validate_json_ld_in_html(html),
        }

    for path in sorted((ROOT / "blog" / "articles").glob("*.html")):
        html = path.read_text(encoding="utf-8")
        report["articles"][path.name] = {
            "tech_article": "TechArticle" in html,
            "blog_posting_only": "BlogPosting" in html and "TechArticle" not in html,
            "breadcrumb_visual": "breadcrumb-nav" in html,
            "breadcrumb_jsonld": "BreadcrumbList" in html,
            "link_voprosy": "voprosy.html" in html,
            "json_ld_errors": validate_json_ld_in_html(html),
        }

    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    report["index"] = {
        "organization": "Organization" in idx and "#organization" in idx,
        "website": "WebSite" in idx and "#website" in idx,
        "item_list": "ItemList" in idx and "site-sections" in idx,
        "link_voprosy": "voprosy.html" in idx,
        "link_kak": "kak-my-rabotaem.html" in idx,
    }

    voprosy = (ROOT / "voprosy.html").read_text(encoding="utf-8") if (ROOT / "voprosy.html").exists() else ""
    report["voprosy"] = {"link_blog": "blog.html" in voprosy}
    report["site_map_exists"] = (ROOT / "site-map.html").exists()

    pages_ok = sum(1 for p in report["pages"].values() if p["breadcrumb_visual"] and p["breadcrumb_jsonld"])
    articles_ok = sum(1 for a in report["articles"].values() if a["tech_article"] and a["breadcrumb_visual"])
    report["stats"] = {
        "pages_with_breadcrumbs": f"{pages_ok}/{len(report['pages'])}",
        "articles_techarticle": f"{sum(1 for a in report['articles'].values() if a['tech_article'])}/{len(report['articles'])}",
        "sitemap_urls": len(regenerate_sitemap()),
    }
    return report


def main() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import integrate_schema_markup as ism  # noqa: WPS433
    import add_breadcrumbs as bc  # noqa: WPS433

    import generate_site_map_page as gsm  # noqa: WPS433

    manifest = load_json(ROOT / "blog" / "articles-manifest.json")
    ism.update_blog_articles(manifest)
    update_index_schema()
    gsm.main()
    bc.main()
    if (ROOT / "public" / "schemas").exists():
        import shutil
        shutil.rmtree(ROOT / "public" / "schemas", ignore_errors=True)
        if (ROOT / "public").exists() and not any((ROOT / "public").iterdir()):
            (ROOT / "public").rmdir()

    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
