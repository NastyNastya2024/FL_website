#!/usr/bin/env python3
"""Fix broken footers and apply standard 3-column layout with Company column."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FOOTER_COL3 = """        <div class="col-6 col-lg-4">
          <div class="small text-mute-500 mb-2 fw-600">Компания</div>
          <ul class="list-unstyled small m-0">
            <li><a class="link-fade" href="{p}about.html">О компании</a></li>
            <li><a class="link-fade" href="{p}site-map.html">Карта сайта</a></li>
          </ul>
          <ul class="list-unstyled small m-0 mt-4 text-mute-500">
            <li><a href="#" class="link-fade" data-bs-toggle="modal" data-bs-target="#consentModal">Согласие на обработку данных</a></li>
            <li><a href="#" class="link-fade" data-bs-toggle="modal" data-bs-target="#legalModal">Правовая информация</a></li>
          </ul>
        </div>"""


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parent.parts)
    return "../" * depth if depth else ""


def fix_missing_close(html: str) -> str:
    if "<footer" in html and "</footer>" not in html:
        for marker in (
            "\n  <!-- CONTACT MODAL -->",
            "\n  <!-- Contact Modal -->",
            '\n  <div class="modal fade" id="contactModal"',
            "\n  <script src=",
            "\n  <script>",
        ):
            if marker in html:
                return html.replace(marker, "\n  </footer>" + marker, 1)
    return html


def fix_footer_columns(html: str, prefix: str) -> str:
    html = html.replace('class="col-12 col-lg-6"', 'class="col-12 col-lg-4"')

    # Remove about/contacts from col2
    html = re.sub(
        r"\n?\s*<li><a class=\"link-fade\" href=\"(?:\.\./)*about\.html\">О компании</a></li>",
        "",
        html,
    )
    html = re.sub(
        r"\n?\s*<li><a class=\"link-fade\" href=\"(?:\.\./)*contacts\.html\">Контакты</a></li>",
        "",
        html,
    )

    col3 = FOOTER_COL3.format(p=prefix)

    # Replace last footer column before closing row
    if "Компания</div>" in html:
        return html

    pattern = re.compile(
        r"(<footer[^>]*>.*?<div class=\"row g-4\">.*?)"
        r"(<div class=\"col-6 col-lg-4\">(?!.*Компания).*?</div>\s*)"
        r"(</div>\s*</div>\s*</footer>)",
        re.S,
    )
    m = pattern.search(html)
    if m:
        return html[: m.start(2)] + col3 + "\n      " + m.group(3)

    # Two-column footers (about, contacts pages): inject third col
    pattern2 = re.compile(
        r"(<footer[^>]*>.*?<div class=\"row g-4\">.*?<div class=\"col-6 col-lg-4\">.*?</div>\s*)"
        r"(</div>\s*</div>\s*</footer>)",
        re.S,
    )
    m2 = pattern2.search(html)
    if m2 and "Компания" not in m2.group(0):
        return html[: m2.start(2)] + col3 + "\n      " + m2.group(2)

    return html


def process(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html
    prefix = prefix_for(path)
    html = fix_missing_close(html)
    if "<footer" in html:
        html = fix_footer_columns(html, prefix)
    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = [str(p.relative_to(ROOT)) for p in sorted(ROOT.rglob("*.html")) if process(p)]
    print(json.dumps({"updated": updated, "count": len(updated)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
