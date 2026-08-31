#!/usr/bin/env python3
"""Apply standard 3-column footer: brand | products | company."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parent.parts)
    return "../" * depth if depth else ""


def footer_html(prefix: str, *, compact: bool = False) -> str:
    p = prefix
    col2 = f"""        <div class="col-6 col-lg-4">
          <ul class="list-unstyled small m-0">
            <li><a class="link-fade" href="{p}federated-learning.html#tech">Федеративное обучение</a></li>
            <li><a class="link-fade" href="{p}data-platform.html">Дата-платформа</a></li>
            <li><a class="link-fade" href="{p}partnership.html">Партнёрство</a></li>
            <li><a class="link-fade" href="{p}blog.html">Блог</a></li>
            <li><a class="link-fade" href="{p}vacancies.html">Вакансии</a></li>
            <li><a class="link-fade" href="{p}expert-review.html">Экспертам</a></li>
            <li><a class="link-fade" href="{p}documents.html">Документы</a></li>
          </ul>
          <ul class="list-unstyled small m-0 mt-4 text-mute-500">
            <li><a href="#pricingModal" class="link-fade" data-bs-toggle="modal" data-bs-target="#pricingModal">Стоимость услуг</a></li>
            <li><a href="{p}img/pdf1.pdf" class="link-fade" target="_blank">Политика обработки данных</a></li>
          </ul>
        </div>"""

    col3 = f"""        <div class="col-6 col-lg-4">
          <ul class="list-unstyled small m-0">
            <li><a class="link-fade" href="{p}about.html">О компании</a></li>
            <li><a class="link-fade" href="{p}site-map.html">Карта сайта</a></li>
          </ul>
          <ul class="list-unstyled small m-0 mt-4 text-mute-500">
            <li><a href="#" class="link-fade" data-bs-toggle="modal" data-bs-target="#consentModal">Согласие на обработку данных</a></li>
            <li><a href="#" class="link-fade" data-bs-toggle="modal" data-bs-target="#legalModal">Правовая информация</a></li>
          </ul>
        </div>"""

    brand = f"""        <div class="col-12 col-lg-4">
          <div class="h5 text-white mb-2"><a class="link-fade text-white text-decoration-none" href="{p}index.html">DigiTrack</a></div>
          <p class="small text-mute-400 m-0">
            Конфиденциальные вычисления: федеративное обучение и платформа данных для бизнеса.
          </p>
          <div class="small text-mute-500 mt-4">
            © <span id="year"></span> ООО «ДТ»
          </div>
        </div>
"""

    if compact:
        col2 = col2.replace("margin-left: 23px;", "margin-left: 0;")

    return f"""  <footer class="py-5 bg-deeper text-mute-300 border-top border-ink-700">
    <div class="container">
      <div class="row g-4">
{brand}{col2}
{col3}
      </div>
    </div>
  </footer>"""


FOOTER_BLOCK = re.compile(
    r"<footer class=\"(?:py-5 bg-deeper|py-5 mt-auto|py-4 bg-deeper).*?</footer>",
    re.S,
)

# footer without closing tag up to modal/script
FOOTER_BROKEN = re.compile(
    r"<footer class=\"(?:py-5 bg-deeper|py-5 mt-auto|py-4 bg-deeper).*?(?=\n  (?:</footer>|<!-- |<div class=\"modal|<script))",
    re.S,
)


def process(path: Path) -> bool:
    if path.name in ("contacts.html", "voprosy.html", "kak-my-rabotaem.html"):
        # Soft-redirect stubs — do not inject footer
        return False
    html = path.read_text(encoding="utf-8")
    prefix = prefix_for(path)
    compact = path.parent.name == "articles"
    new_footer = footer_html(prefix, compact=compact)

    if FOOTER_BLOCK.search(html):
        new_html = FOOTER_BLOCK.sub(new_footer, html, count=1)
    elif "<footer class=\"py-5 bg-deeper" in html or "<footer class=\"py-5 mt-auto" in html or "<footer class=\"py-4 bg-deeper" in html:
        new_html = FOOTER_BROKEN.sub(new_footer, html, count=1)
    else:
        return False

    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = [str(p.relative_to(ROOT)) for p in sorted(ROOT.rglob("*.html")) if process(p)]
    print(json.dumps({"updated": updated, "count": len(updated)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
