#!/usr/bin/env python3
"""Restore privacy/consent modals after corrupted </footer> markup."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "federated-learning.html"

MODALS_RE = re.compile(
    r"(  <!-- Модальное окно политики конфиденциальности -->.*?"
    r"  </div>\n\n"
    r"  <!-- Модальное окно согласия на обработку данных -->.*?"
    r"  </div>\n\n)",
    re.DOTALL,
)

CORRUPT_FOOTER_RE = re.compile(
    r"  </footer>(?=[^\s<])[^\n]*\n"
    r"(?:(?!  <!-- Модальное окно стоимости продукта -->).*\n)*?",
    re.MULTILINE,
)


def extract_modals() -> str:
    ref = REFERENCE.read_text(encoding="utf-8")
    m = MODALS_RE.search(ref)
    if not m:
        raise RuntimeError("Could not extract modals from federated-learning.html")
    return m.group(1)


def fix_file(path: Path, modals: str) -> bool:
    html = path.read_text(encoding="utf-8")
    if not CORRUPT_FOOTER_RE.search(html):
        return False
    fixed = CORRUPT_FOOTER_RE.sub("  </footer>\n\n" + modals, html, count=1)
    if fixed == html:
        return False
    path.write_text(fixed, encoding="utf-8")
    return True


def main() -> None:
    modals = extract_modals()
    updated: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if fix_file(path, modals):
            updated.append(str(path.relative_to(ROOT)))
    print(f"Fixed {len(updated)} files:")
    for name in updated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
