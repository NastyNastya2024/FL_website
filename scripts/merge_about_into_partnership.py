#!/usr/bin/env python3
"""Merge about.html content into partnership.html; redirect about + update links."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://digi-track.ru"


def extract_section(html: str, section_id: str) -> str:
    pattern = re.compile(
        rf'(<section id="{re.escape(section_id)}"[^>]*>.*?</section>)',
        re.DOTALL,
    )
    match = pattern.search(html)
    if not match:
        raise RuntimeError(f"Section #{section_id} not found")
    return match.group(1)


def renumber_partnership_faq(section: str) -> str:
    section = section.replace('id="faq"', 'id="faq-partnership"', 1)
    section = section.replace('id="faqAcc"', 'id="faqPartnershipAcc"', 1)
    section = re.sub(r'data-bs-parent="#faqAcc"', 'data-bs-parent="#faqPartnershipAcc"', section)
    section = re.sub(r'\bid="f(\d+)"', r'id="pf\1"', section)
    section = re.sub(r'\bid="fa(\d+)"', r'id="pfa\1"', section)
    section = re.sub(
        r'data-bs-target="#fa(\d+)"',
        lambda m: f'data-bs-target="#pfa{m.group(1)}"',
        section,
    )
    section = re.sub(
        r'aria-controls="fa(\d+)"',
        lambda m: f'aria-controls="pfa{m.group(1)}"',
        section,
    )
    section = re.sub(
        r'aria-labelledby="f(\d+)"',
        lambda m: f'aria-labelledby="pf{m.group(1)}"',
        section,
    )
    section = section.replace("about.html#contacts", "partnership.html#contacts")
    section = section.replace("about.html#process", "partnership.html#process")
    section = section.replace("about.html#faq", "partnership.html#faq")
    section = re.sub(
        r"<h2 class=\"h3 fw-700 mb-4\">Часто задаваемые вопросы</h2>",
        '<h2 class="h3 fw-700 mb-2">Вопросы о партнёрстве</h2>\n'
        '<p class="snippet-answer mb-4">Требования к данным, монетизация, безопасность и сроки пилота.</p>',
        section,
        count=1,
    )
    return section


def patch_company_blocks(text: str) -> str:
    text = text.replace("about.html#contacts", "partnership.html#contacts")
    text = text.replace("about.html#process", "partnership.html#process")
    text = text.replace("about.html#faq", "partnership.html#faq")
    text = text.replace('href="partnership.html"', 'href="#partners-types"', 1)
    text = re.sub(
        r'<h1 class="h2 fw-700 mb-2">О компании DigiTrack</h1>',
        '<h2 class="h2 fw-700 mb-2">О компании DigiTrack</h2>',
        text,
        count=1,
    )
    text = text.replace(
        '<a href="index.html">На главную →</a>',
        '<a href="#partners-types">Партнёрство →</a>',
    )
    return text


def company_nav() -> str:
    return """      <nav class="company-page-nav mb-4 py-3" aria-label="Разделы страницы">
        <ul class="list-inline small mb-0">
          <li class="list-inline-item me-3"><a href="#partners-types">Партнёрство</a></li>
          <li class="list-inline-item me-3"><a href="#about">О компании</a></li>
          <li class="list-inline-item me-3"><a href="#process">Как мы работаем</a></li>
          <li class="list-inline-item me-3"><a href="#faq-partnership">FAQ партнёров</a></li>
          <li class="list-inline-item me-3"><a href="#faq">Вопросы и ответы</a></li>
          <li class="list-inline-item"><a href="#contacts">Контакты</a></li>
        </ul>
      </nav>
"""


def build_partnership_schema(faq: dict, howto: dict) -> str:
    faq = json.loads(json.dumps(faq))
    howto = json.loads(json.dumps(howto))
    faq["url"] = f"{BASE}/partnership.html#faq"
    faq["@id"] = f"{BASE}/partnership.html#faqpage"
    howto["url"] = f"{BASE}/partnership.html#process"
    howto["@id"] = f"{BASE}/partnership.html#howto-order"

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE}/partnership.html#organization",
                "name": "DigiTrack",
                "legalName": "Общество с ограниченной ответственностью «ДИДЖИТРЕК»",
                "alternateName": ["ООО «ДТ»", "Диджи Трек"],
                "url": f"{BASE}/",
                "description": "Разработка ПО для федеративного обучения и корпоративных платформ данных on-premise.",
                "foundingDate": "2023",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{BASE}/img/DataIcon.png",
                    "width": 512,
                    "height": 512,
                },
                "email": "info@digi-track.ru",
                "telephone": "+7-985-770-45-12",
                "taxID": "9705200012",
                "sameAs": [
                    "https://t.me/digitrack",
                    "https://vk.com/digitrack",
                    "https://www.youtube.com/@digitrack",
                    "https://www.linkedin.com/company/digitrack",
                ],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "telephone": "+7-985-770-45-12",
                    "email": "info@digi-track.ru",
                    "contactType": "sales",
                    "areaServed": "RU",
                    "availableLanguage": ["Russian", "English"],
                },
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Шлюзовая набережная, д. 8, стр. 1",
                    "addressLocality": "Москва",
                    "postalCode": "115114",
                    "addressCountry": "RU",
                },
            },
            {
                "@type": "WebPage",
                "@id": f"{BASE}/partnership.html#webpage",
                "url": f"{BASE}/partnership.html",
                "name": "Партнёрство и о компании DigiTrack",
                "description": "Партнёрство в FL, о компании, FAQ, этапы работы и контакты DigiTrack.",
                "inLanguage": "ru-RU",
                "about": {"@id": f"{BASE}/partnership.html#organization"},
                "hasPart": [
                    {"@id": f"{BASE}/partnership.html#faqpage"},
                    {"@id": f"{BASE}/partnership.html#howto-order"},
                ],
            },
            faq,
            howto,
        ],
    }
    return json.dumps(graph, ensure_ascii=False, indent=2)


def contact_modal_and_scripts() -> str:
    return """
  <div class="modal fade" id="contactModal" tabindex="-1" aria-labelledby="contactModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title" id="contactModalLabel">Будем рады вашим вопросам</h6>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body text-center">
          <p class="mb-0">Пишите на <a href="mailto:info@digi-track.ru">info@digi-track.ru</a></p>
        </div>
      </div>
    </div>
  </div>
  <script>
  document.getElementById('year').textContent = new Date().getFullYear();
  var contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = document.getElementById('contactName').value.trim();
      var email = document.getElementById('contactEmail').value.trim();
      var message = document.getElementById('contactMessage').value.trim();
      var subject = encodeURIComponent('Заявка с сайта DigiTrack');
      var body = encodeURIComponent('Имя: ' + name + '\\nEmail: ' + email + '\\n\\n' + message);
      window.location.href = 'mailto:info@digi-track.ru?subject=' + subject + '&body=' + body;
    });
  }
  </script>
"""


def redirect_stub(title: str, target: str, label: str, *, preserve_hash: bool = False) -> str:
    js = (
        'location.replace("partnership.html" + location.hash);'
        if preserve_hash
        else f'location.replace("partnership.html{target}");'
    )
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} — DigiTrack</title>
  <link rel="canonical" href="{BASE}/partnership.html{target}"/>
  <meta http-equiv="refresh" content="0;url=partnership.html{target}"/>
  <meta name="robots" content="noindex, follow"/>
  <script>{js}</script>
</head>
<body>
  <p>Раздел перенесён: <a href="partnership.html{target}">{label}</a>.</p>
</body>
</html>
"""


def merge_partnership() -> None:
    about = (ROOT / "about.html").read_text(encoding="utf-8")
    partnership = (ROOT / "partnership.html").read_text(encoding="utf-8")

    about_section = patch_company_blocks(extract_section(about, "about"))
    process_section = patch_company_blocks(extract_section(about, "process"))
    company_faq = patch_company_blocks(extract_section(about, "faq"))
    contacts_section = patch_company_blocks(extract_section(about, "contacts"))

    partnership_faq = renumber_partnership_faq(extract_section(partnership, "faq"))

    # Remove minimal contacts + partnership faq from partnership (re-added later)
    partnership = re.sub(
        r'\n    <section id="contacts" class="py-6 bg-section">.*?</section>\n',
        "\n",
        partnership,
        count=1,
        flags=re.DOTALL,
    )
    partnership = re.sub(
        r'\n    <!-- FAQ -->\n    <section id="faq" class="py-6 bg-section">.*?</section>\n',
        "\n",
        partnership,
        count=1,
        flags=re.DOTALL,
    )

    company_block = f"""
    <div class="container company-hub about-page py-6">
{company_nav()}
{about_section}

      <hr class="border-ink-700 my-5"/>

{process_section}

      <hr class="border-ink-700 my-5"/>

{partnership_faq.replace('class="py-6 bg-section"', 'class="mb-5"', 1)}

      <hr class="border-ink-700 my-5"/>

{company_faq}

      <hr class="border-ink-700 my-5"/>

{contacts_section}
    </div>
"""

    partnership = partnership.replace(
        '                <a href="index.html" class="btn btn-link text-white px-4 py-2">О компании →</a>',
        '                <a href="#about" class="btn btn-link text-white px-4 py-2">О компании →</a>',
    )

    partnership = partnership.replace("\n  </main>", f"\n{company_block}\n  </main>", 1)
    partnership = partnership.replace(
        'body class="bg-deep partnership-page"',
        'body class="bg-deep partnership-page company-hub"',
    )
    partnership = partnership.replace(
        'about.html#contacts',
        "partnership.html#contacts",
    )
    partnership = partnership.replace(
        'href="about.html">О компании</a>',
        'href="partnership.html#about">О компании</a>',
    )

    faq = json.loads((ROOT / "schemas" / "faq-schema.jsonld").read_text(encoding="utf-8"))
    howto = json.loads((ROOT / "schemas" / "howto-schema.jsonld").read_text(encoding="utf-8"))
    schema = build_partnership_schema(faq, howto)

    partnership = re.sub(
        r'<title>.*?</title>',
        "<title>Партнёрство и о компании DigiTrack — FL, FAQ, контакты</title>",
        partnership,
        count=1,
    )
    partnership = re.sub(
        r'<meta name="description" content="[^"]*"/>',
        '<meta name="description" content="Партнёрство в федеративном обучении, о компании DigiTrack, FAQ, этапы работы и контакты в Москве. Пилот ~6 месяцев — info@digi-track.ru"/>',
        partnership,
        count=1,
    )

    if 'partnership.html#organization' not in partnership:
        breadcrumb = partnership.find('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList"')
        if breadcrumb != -1:
            end = partnership.find("</script>", breadcrumb) + len("</script>")
            partnership = partnership[:breadcrumb] + f'<script type="application/ld+json">{schema}</script>\n  ' + partnership[breadcrumb:end] + partnership[end:]

    if 'id="contactModal"' not in partnership:
        partnership = partnership.replace(
            "  <!-- Bootstrap bundle + App -->",
            contact_modal_and_scripts() + "\n  <!-- Bootstrap bundle + App -->",
        )

    (ROOT / "partnership.html").write_text(partnership, encoding="utf-8")


def patch_about_redirect() -> None:
    (ROOT / "about.html").write_text(
        redirect_stub("О компании", "", "Партнёрство и о компании", preserve_hash=True),
        encoding="utf-8",
    )


def patch_stubs() -> None:
    stubs = {
        "contacts.html": ("#contacts", "Контакты"),
        "voprosy.html": ("#faq", "Вопросы и ответы"),
        "kak-my-rabotaem.html": ("#process", "Как мы работаем"),
    }
    for name, (anchor, label) in stubs.items():
        (ROOT / name).write_text(
            redirect_stub(label, anchor, label),
            encoding="utf-8",
        )


def patch_links() -> None:
    skip = {"partnership.html", "about.html"}
    for path in ROOT.rglob("*.html"):
        if path.name in skip or "blog/articles" in str(path) and False:
            pass
        text = path.read_text(encoding="utf-8")
        original = text

        if path.name == "about.html":
            continue

        prefix = "../" * (len(path.relative_to(ROOT).parts) - 1)
        target = f"{prefix}partnership.html"

        text = re.sub(r"(?<![./\w])about\.html", lambda m: target, text)
        text = text.replace(f"{prefix}partnership.html#", f"{prefix}partnership.html#")

        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"links: {path.relative_to(ROOT)}")


def patch_blog_links() -> None:
    for path in (ROOT / "blog" / "articles").glob("*.html"):
        text = path.read_text(encoding="utf-8")
        original = text
        text = text.replace("../../about.html", "../../partnership.html")
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"links: {path.relative_to(ROOT)}")


def patch_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\s*<url>\s*<loc>https://digi-track\.ru/about\.html</loc>.*?</url>",
        "",
        text,
        count=1,
        flags=re.S,
    )
    path.write_text(text, encoding="utf-8")


def patch_schema_files() -> None:
    for name, anchor in (("faq-schema.jsonld", "#faq"), ("howto-schema.jsonld", "#process")):
        data = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
        data["url"] = f"{BASE}/partnership.html{anchor}"
        slug = "faqpage" if "faq" in name else "howto-order"
        data["@id"] = f"{BASE}/partnership.html#{slug}"
        (ROOT / "schemas" / name).write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def main() -> None:
    merge_partnership()
    patch_about_redirect()
    patch_stubs()
    patch_links()
    patch_blog_links()
    patch_sitemap()
    patch_schema_files()
    print("Merged about → partnership.html")


if __name__ == "__main__":
    main()
