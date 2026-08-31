#!/usr/bin/env python3
"""Restore pricing/legal modals and bootstrap/metrika scripts removed by cleanup."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "partnership.html"

MODALS_RE = re.compile(
    r"(  <!-- Модальное окно стоимости продукта -->.*?  </div>\n\n"
    r"  <!-- Модальное окно правовой информации -->.*?  </div>\n\n)",
    re.DOTALL,
)

SCRIPTS_RE = re.compile(
    r"  <!-- Bootstrap bundle \+ App -->\n"
    r"  <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js\" defer></script>\n"
    r"  <script src=\"\./metrika.js\" defer data-ga=\"G-FL8MNDG3M8\"></script>\n",
)


def asset_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else "./"


def build_modals_block(prefix: str, template: str) -> str:
    return template


def build_scripts_block(prefix: str, template: str) -> str:
    return template.replace('src="./metrika.js"', f'src="{prefix}metrika.js"')


def insert_before_scripts(html: str, block: str) -> str:
    markers = (
        '  <!-- Bootstrap bundle + App -->',
        '  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"',
        '  <script src="./',
        '  <script src="../',
        '  <script>\n',
        "</body>",
    )
    for marker in markers:
        idx = html.find(marker)
        if idx != -1:
            return html[:idx] + block + html[idx:]
    return html + block


def main() -> None:
    ref_html = REF.read_text(encoding="utf-8")
    modals_match = MODALS_RE.search(ref_html)
    scripts_match = SCRIPTS_RE.search(ref_html)
    if not modals_match or not scripts_match:
        raise RuntimeError("Could not extract modal/script blocks from partnership.html")

    modals_template = modals_match.group(1)
    scripts_template = scripts_match.group(0)

    for path in sorted(ROOT.rglob("*.html")):
        if path == REF:
            continue
        html = path.read_text(encoding="utf-8")
        if 'id="consentModal"' not in html:
            continue

        original = html
        prefix = asset_prefix(path)

        if 'id="legalModal"' not in html:
            html = insert_before_scripts(html, build_modals_block(prefix, modals_template))

        if "bootstrap.bundle.min.js" not in html or "metrika.js" not in html:
            scripts = build_scripts_block(prefix, scripts_template)
            if "bootstrap.bundle.min.js" not in html and "metrika.js" not in html:
                html = insert_before_scripts(html, scripts)
            elif "bootstrap.bundle.min.js" not in html:
                html = insert_before_scripts(
                    html,
                    '  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>\n',
                )
            elif "metrika.js" not in html:
                html = insert_before_scripts(
                    html,
                    f'  <script src="{prefix}metrika.js" defer data-ga="G-FL8MNDG3M8"></script>\n',
                )

        if html != original:
            path.write_text(html, encoding="utf-8")
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
