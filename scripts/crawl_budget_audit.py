#!/usr/bin/env python3
"""Crawl budget audit for DigiTrack static site."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://digi-track.ru"
ASSET_EXT = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".css", ".js",
    ".xml", ".jsonld", ".mp4", ".webmanifest", ".svg", ".woff", ".woff2",
}

LINK_RE = re.compile(r'''(?:href|src|action)\s*=\s*["']([^"']+)["']''', re.I)


def resolve_link(from_path: Path, href: str) -> tuple[str | None, str]:
    href = href.strip()
    if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None, "skip"
    if href.startswith(("http://", "https://")):
        return href, "external"
    base = href.split("#")[0].split("?")[0]
    if not base:
        return None, "anchor"
    if base.startswith("/"):
        target = base.lstrip("/")
    else:
        target = (from_path.parent / base).resolve()
        try:
            target = target.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return None, "broken-outside"
    return target, "internal"


def main() -> dict:
    html_files = sorted(ROOT.rglob("*.html"))
    sitemap_text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_urls = re.findall(r"<loc>(.*?)</loc>", sitemap_text)
    sitemap_paths = {u.replace(f"{BASE}/", "") for u in sitemap_urls}

    broken: list[dict] = []
    query_links: list[dict] = []
    redirect_pages: list[str] = []
    noindex_pages: list[str] = []
    canonicals: dict[str, str] = {}
    internal_links: Counter = Counter()

    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")

        if 'http-equiv="refresh"' in text or "location.replace(" in text:
            redirect_pages.append(rel)
        if re.search(r'noindex', text, re.I):
            noindex_pages.append(rel)
        if m := re.search(r'<link rel="canonical" href="([^"]+)"', text):
            canonicals[rel] = m.group(1)

        for m in LINK_RE.finditer(text):
            href = m.group(1)
            if "?" in href:
                query_links.append({"from": rel, "href": href})
            target, kind = resolve_link(path, href)
            if kind == "internal" and target:
                internal_links[target] += 1
                ext = Path(target).suffix.lower()
                p = ROOT / target
                if not p.exists():
                    if ext and ext not in ASSET_EXT:
                        broken.append({"from": rel, "href": href, "target": target, "type": "html"})
                    elif ext in ASSET_EXT or "/" not in target:
                        if not p.exists():
                            broken.append({"from": rel, "href": href, "target": target, "type": "asset"})

    all_html = {p.relative_to(ROOT).as_posix() for p in html_files}
    indexable = [p for p in all_html if p not in noindex_pages]

    report = {
        "total_html": len(html_files),
        "indexable": len(indexable),
        "noindex": noindex_pages,
        "redirects": redirect_pages,
        "sitemap_count": len(sitemap_paths),
        "in_sitemap_not_indexable": sorted(sitemap_paths & set(noindex_pages)),
        "indexable_not_in_sitemap": sorted(set(indexable) - sitemap_paths),
        "sitemap_404": sorted(sitemap_paths - all_html),
        "broken_links": broken,
        "query_param_links": len(query_links),
        "pagination": "none",
        "duplicate_canonical_targets": {k: v for k, v in Counter(canonicals.values()).items() if v > 1},
        "orphan_candidates": sorted(all_html - {t for t, c in internal_links.items() if c > 0 and t.endswith(".html")}),
        "top_linked": internal_links.most_common(15),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    main()
