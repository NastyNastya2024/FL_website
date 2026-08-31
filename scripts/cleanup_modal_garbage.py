#!/usr/bin/env python3
"""Remove orphaned privacy/consent HTML outside modals and dedupe modal blocks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODAL_CLOSE = r"        </div>\n      </div>\n    </div>\n  </div>\n\n"
VALID_NEXT = r"  <!-- Модальное окно|  <div class=\"modal fade\"|  <script "

ORPHAN_GARBAGE_RE = re.compile(
    rf"({MODAL_CLOSE})"
    r"((?:[ \t]*\n)?(?:[ \t]*(?:"
    r"<p>|<p class=\"legal-section-title\">|<li>|<h6>|<ul>|"
    r"<div class=\"modal-footer\">|<div class=\"modal-body\">"
    r").*)+?)"
    rf"(?={VALID_NEXT})",
    re.DOTALL,
)

MODALS_BLOCK_RE = re.compile(
    r"  <!-- Модальное окно политики конфиденциальности -->.*?"
    r"        </div>\n      </div>\n    </div>\n  </div>\n\n"
    r"  <!-- Модальное окно согласия на обработку данных -->.*?"
    r"        </div>\n      </div>\n    </div>\n  </div>\n\n",
    re.DOTALL,
)


def remove_orphan_garbage(html: str) -> str:
    prev = None
    while prev != html:
        prev = html

        def repl(match: re.Match[str]) -> str:
            if '<div class="modal fade"' in match.group(2):
                return match.group(0)
            return match.group(1)

        html = ORPHAN_GARBAGE_RE.sub(repl, html)
    return html


def dedupe_pattern(html: str, pattern: re.Pattern[str]) -> str:
    matches = list(pattern.finditer(html))
    if len(matches) <= 1:
        return html
    for match in reversed(matches[1:]):
        html = html[: match.start()] + html[match.end() :]
    return html


def dedupe_modal_by_id(html: str, modal_id: str) -> str:
    pattern = re.compile(
        rf"(?:  <!-- [^\n]+ -->\n)?"
        rf'  <div class="modal fade" id="{re.escape(modal_id)}".*?'
        r"        </div>\n      </div>\n    </div>\n  </div>\n\n",
        re.DOTALL,
    )
    return dedupe_pattern(html, pattern)


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        html = path.read_text(encoding="utf-8")
        original = html

        html = remove_orphan_garbage(html)
        html = dedupe_pattern(html, MODALS_BLOCK_RE)
        html = dedupe_modal_by_id(html, "consentModal")

        if html != original:
            path.write_text(html, encoding="utf-8")
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
