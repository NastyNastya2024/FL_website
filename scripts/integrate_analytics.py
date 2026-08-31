#!/usr/bin/env python3
"""Ensure Google Analytics + Metrika loader on all HTML pages."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GA_ID = "G-FL8MNDG3M8"
SKIP = {"contacts.html", "voprosy.html", "kak-my-rabotaem.html"}


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parent.parts)
    return "../" * depth if depth else "./"


def ensure_head_tags(html: str) -> str:
    if 'name="google-analytics-id"' not in html:
        meta = f'  <meta name="google-analytics-id" content="{GA_ID}"/>\n'
        if 'name="yandex-metrika-counter"' in html:
            html = re.sub(
                r'(<meta name="yandex-metrika-counter"[^>]*>\n?)',
                r"\1" + meta,
                html,
                count=1,
            )
        elif "<head>" in html:
            html = html.replace("<head>", "<head>\n" + meta, 1)
        else:
            html = meta + html

    if 'href="//www.googletagmanager.com"' not in html:
        prefetch = '  <link rel="dns-prefetch" href="//www.googletagmanager.com"/>\n'
        if 'href="//mc.yandex.ru"' in html:
            html = html.replace(
                '  <link rel="dns-prefetch" href="//mc.yandex.ru"/>\n',
                '  <link rel="dns-prefetch" href="//mc.yandex.ru"/>\n' + prefetch,
                1,
            )
        elif "<head>" in html:
            html = html.replace("<head>", "<head>\n" + prefetch, 1)
    return html


def ensure_metrika_script(html: str, path: Path) -> str:
    src = f'{prefix_for(path)}metrika.js'
    tag = f'<script src="{src}" defer data-ga="{GA_ID}"></script>'
    if "metrika.js" in html:
        html = re.sub(
            r'<script[^>]*src="[^"]*metrika\.js"[^>]*></script>',
            tag,
            html,
            count=1,
        )
        return html
    if "</body>" in html:
        return html.replace("</body>", f"  {tag}\n</body>", 1)
    return html + f"\n  {tag}\n</body>\n</html>\n"


def restore_tail_from_git(html: str, path: Path) -> str:
    if "</html>" in html:
        return html
    try:
        git_html = subprocess.check_output(
            ["git", "show", f"HEAD:{path.relative_to(ROOT).as_posix()}"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return html

    footers = list(re.finditer(r"</footer>", html, re.I))
    if not footers:
        return html
    pos = footers[-1].end()
    tail = git_html[pos:]
    if not tail.strip():
        return html
    return html[:pos] + tail


def process(path: Path) -> bool:
    if path.name in SKIP:
        return False
    original = path.read_text(encoding="utf-8")
    html = restore_tail_from_git(original, path)
    html = ensure_head_tags(html)
    html = ensure_metrika_script(html, path)
    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = [str(p.relative_to(ROOT)) for p in sorted(ROOT.rglob("*.html")) if process(p)]
    print(f"Updated {len(updated)} files")
    for name in updated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
