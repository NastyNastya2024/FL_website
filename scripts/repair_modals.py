#!/usr/bin/env python3
"""Remove duplicate privacy/consent modals and fix broken FL page tail."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODALS_BLOCK_RE = re.compile(
    r"  <!-- Модальное окно политики конфиденциальности -->.*?"
    r"  </div>\n\n"
    r"  <!-- Модальное окно согласия на обработку данных -->.*?"
    r"  </div>\n\n",
    re.DOTALL,
)

CORRUPT_FOOTER_RE = re.compile(
    r"  </footer>(?=[^\s<])[^\n]*\n"
    r"(?:(?!  <!-- Модальное окно стоимости продукта -->).*\n)*?",
    re.MULTILINE,
)

FL_BROKEN_TAIL_RE = re.compile(
    r"  </main>\n\n  <!-- Модальное окно обратной связи -->\n  </footer>\n\n"
    r"  <!-- Модальное окно политики конфиденциальности -->.*?"
    r"(?=  <div class=\"modal fade\" id=\"contactModal\")",
    re.DOTALL,
)


def extract_modals_from(path: Path) -> str:
    ref = path.read_text(encoding="utf-8")
    m = MODALS_BLOCK_RE.search(ref)
    if not m:
        raise RuntimeError(f"No modals block in {path}")
    return m.group(0)


def dedupe_modals(html: str) -> str:
    matches = list(MODALS_BLOCK_RE.finditer(html))
    if len(matches) <= 1:
        return html
    for m in reversed(matches[1:]):
        html = html[: m.start()] + html[m.end() :]
    return html


def fix_corrupt_footer(html: str, modals: str) -> str:
    if not CORRUPT_FOOTER_RE.search(html):
        return html
    return CORRUPT_FOOTER_RE.sub("  </footer>\n\n" + modals, html, count=1)


def fix_fl(html: str) -> str:
    return FL_BROKEN_TAIL_RE.sub("  </main>\n\n", html, count=1)


def main() -> None:
    modals = extract_modals_from(ROOT / "partnership.html")

    for path in sorted(ROOT.rglob("*.html")):
        html = path.read_text(encoding="utf-8")
        original = html
        html = fix_corrupt_footer(html, modals)
        html = dedupe_modals(html)
        if path.name == "federated-learning.html":
            html = fix_fl(html)
        if html != original:
            path.write_text(html, encoding="utf-8")
            print(f"fixed: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
