#!/usr/bin/env python3
"""Apply SEO/AEO/GEO recommendations to FL_website HTML files."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://digi-track.ru"

SEO_CSS = """
/* SEO / AEO / GEO blocks */
.snippet-answer,
.geo-definition {
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--ink-700, #1a363a);
  margin-bottom: 1rem;
  padding-left: 0.75rem;
  border-left: 3px solid var(--mint-400, #9fe29e);
}
.geo-timing {
  font-size: 0.95rem;
  color: var(--mute-400, #6b7c7e);
  margin-bottom: 1rem;
}
.seo-table {
  width: 100%;
  margin: 1rem 0 1.5rem;
  font-size: 0.9rem;
  border-collapse: collapse;
}
.seo-table th,
.seo-table td {
  padding: 0.6rem 0.75rem;
  border: 1px solid rgba(26, 54, 58, 0.12);
  vertical-align: top;
}
.seo-table th {
  background: rgba(159, 226, 158, 0.15);
  font-weight: 600;
}
.seo-table-wrap {
  overflow-x: auto;
  margin-bottom: 1.5rem;
}
.seo-checklist {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem;
}
.seo-checklist li {
  padding: 0.35rem 0 0.35rem 1.75rem;
  position: relative;
}
.seo-checklist li::before {
  content: "☐";
  position: absolute;
  left: 0;
  color: var(--mint-500, #7bc97a);
}
details.seo-details {
  margin-bottom: 1.5rem;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 0.75rem;
  border: 1px solid rgba(26, 54, 58, 0.08);
}
details.seo-details summary {
  font-weight: 600;
  cursor: pointer;
}
.legal-section-title {
  font-weight: 600;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}
.blog-hub-filters .btn.active {
  background: var(--mint-400, #9fe29e);
  border-color: var(--mint-400, #9fe29e);
  color: #1a363a;
}
.article-product-cta {
  margin-top: 2rem;
  padding: 1.25rem 1.5rem;
  border-radius: 0.75rem;
  background: rgba(159, 226, 158, 0.12);
  border: 1px solid rgba(26, 54, 58, 0.1);
}
"""

ARTICLE_CTA_FL = """
        <aside class="article-product-cta">
          <p class="mb-2"><strong>DigiTrack Confidential Computing</strong> — федеративное обучение on-premise без передачи ПДн.</p>
          <p class="mb-0 small"><a href="../../federated-learning.html">Продукт →</a> · <a href="../../partnership.html">Партнёрство →</a> · <a href="fl-guide.html">Обзор FL →</a></p>
        </aside>
"""

ARTICLE_CTA_BDP = """
        <aside class="article-product-cta">
          <p class="mb-2"><strong>DigiTrack Big Data Platform</strong> — Hadoop/Spark/Kafka on-premise без vendor lock-in.</p>
          <p class="mb-0 small"><a href="../../data-platform.html">Платформа →</a> · <a href="bdp-guide.html">Обзор BDP →</a> · <a href="tco-big-data.html">Расчёт TCO →</a></p>
        </aside>
"""


def fix_legal_h6(html: str) -> str:
    """Replace h6 in modal bodies (not modal-title) with p.legal-section-title."""

    def repl_modal_body(m: re.Match) -> str:
        body = m.group(0)
        body = re.sub(
            r"<h6([^>]*)>(.*?)</h6>",
            r'<p class="legal-section-title"\1>\2</p>',
            body,
            flags=re.DOTALL,
        )
        return body

    return re.sub(
        r'<div class="modal-body">.*?</div>\s*(?=<div class="modal-footer">|<div class="modal-body">|</div>\s*</div>\s*</div>)',
        repl_modal_body,
        html,
        flags=re.DOTALL,
    )


def upsert_meta(html: str, *, title: str, description: str, canonical_path: str, og_title: str | None = None) -> str:
    og_title = og_title or title
    canonical = f"{BASE}{canonical_path}"
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content="[^"]*"/>',
        f'<meta name="description" content="{description}"/>',
        html,
        count=1,
    )
    if 'rel="canonical"' not in html:
        html = html.replace("</title>", f'</title>\n  <link rel="canonical" href="{canonical}"/>', 1)
    else:
        html = re.sub(r'<link rel="canonical" href="[^"]*"/>', f'<link rel="canonical" href="{canonical}"/>', html)
    html = re.sub(r'<meta property="og:url" content="[^"]*"/>', f'<meta property="og:url" content="{canonical}"/>', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*"/>', f'<meta property="og:title" content="{og_title}"/>', html)
    html = re.sub(
        r'<meta property="og:description" content="[^"]*"/>',
        f'<meta property="og:description" content="{description}"/>',
        html,
        count=1,
    )
    html = re.sub(r'<meta property="twitter:url" content="[^"]*"/>', f'<meta property="twitter:url" content="{canonical}"/>', html)
    html = re.sub(r'<meta property="twitter:title" content="[^"]*"/>', f'<meta property="twitter:title" content="{og_title}"/>', html)
    html = re.sub(
        r'<meta property="twitter:description" content="[^"]*"/>',
        f'<meta property="twitter:description" content="{description}"/>',
        html,
        count=1,
    )
    return html


def add_schema_link(html: str, path: str = "/seo/schema-updated.jsonld") -> str:
    tag = f'  <script type="application/ld+json" src="{path}"></script>'
    if "schema-updated.jsonld" in html:
        return html
    return html.replace("</head>", f"{tag}\n</head>", 1)


def remove_fl_org_schema(html: str) -> str:
    return re.sub(
        r"\s*<!-- Structured Data -->.*?<script type=\"application/ld\+json\">.*?</script>\s*",
        "\n  ",
        html,
        count=1,
        flags=re.DOTALL,
    )


def add_page_faq_schema(html: str, faqs: list[tuple[str, str]], page_id: str) -> str:
    entities = []
    for q, a in faqs:
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    block = json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "@id": page_id, "mainEntity": entities},
        ensure_ascii=False,
        indent=2,
    )
    tag = f'  <script type="application/ld+json">\n{block}\n  </script>'
    if f'"@id": "{page_id}"' in html:
        return html
    return html.replace("</head>", f"{tag}\n</head>", 1)


def patch_index(html: str) -> str:
    html = upsert_meta(
        html,
        title="DigiTrack — федеративное обучение и платформа данных on-premise | ООО «ДТ»",
        description="Разработчик ПО для федеративного обучения и Big Data Platform без vendor lock-in. VFL, HFL, Hadoop/Spark on Astra Linux. Заявка: info@digi-track.ru",
        canonical_path="/index.html",
    )
    html = add_schema_link(html)

    html = html.replace(
        '<h1 class="display-5 fw-800 mb-3 text-white">DigiTrack</h1>',
        '<h1 class="display-5 fw-800 mb-3 text-white">DigiTrack — федеративное обучение и платформа данных для enterprise</h1>',
    )
    html = html.replace(
        '<p class="text-white mb-4 hero-lead">\n              Команда профессионалов в области разработки программного обеспечения\n            </p>',
        '<p class="text-white mb-4 hero-lead geo-definition">DigiTrack (ООО «ДТ») разрабатывает ПО для федеративного обучения и корпоративных платформ данных on-premise. Данные не покидают контур заказчика — решения для финтеха и enterprise в соответствии с 152-ФЗ.</p>',
    )

    html = html.replace(
        '<h2 class="h3 fw-700 mb-4">Три основных направления разработки</h2>',
        '<h2 class="h3 fw-700 mb-2">Что такое DigiTrack и чем занимается компания?</h2>\n        <p class="snippet-answer">ООО «ДТ» — разработчик ПО для конфиденциальных вычислений: федеративное обучение, платформы ML и Big Data Platform без vendor lock-in on-premise.</p>\n        <h2 class="h4 fw-600 mb-4">Какие три направления разработки?</h2>',
    )
    html = html.replace('<h3 class="h5 mb-2">Конфиденциальные вычисления</h3>', '<h3 class="h5 mb-2">Что такое конфиденциальные вычисления?</h3>')
    html = html.replace('<h3 class="h5 mb-2">Платформы машинного обучения</h3>', '<h3 class="h5 mb-2">Как мы строим платформы машинного обучения?</h3>')
    html = html.replace('<h3 class="h5 mb-2">Обучение сложных ML моделей</h3>', '<h3 class="h5 mb-2">Как обучаем сложные ML-модели с защитой данных?</h3>')

    html = html.replace(
        '<h2 class="h3 fw-800 m-0">Продукты</h2>',
        '<h2 class="h3 fw-800 m-0">Какие продукты предлагает DigiTrack?</h2>',
    )
    html = html.replace(
        '<h3 class="h5 mb-2">Федеративное обучение</h3>',
        '<h3 class="h5 mb-2">Что такое DigiTrack Confidential Computing?</h3>',
        1,
    )
    html = html.replace(
        '<h3 class="h5 mb-2">Платформа данных</h3>',
        '<h3 class="h5 mb-2">Что такое DigiTrack Big Data Platform?</h3>',
        1,
    )

    products_panel = """          <div class="seo-table-wrap mt-3 mb-4">
            <table class="seo-table">
              <thead><tr><th>Продукт</th><th>Для кого</th><th>Ключевая ценность</th></tr></thead>
              <tbody>
                <tr><td><a href="federated-learning.html">Confidential Computing</a></td><td>Банки, финтех</td><td>ML на данных партнёров без передачи ПДн</td></tr>
                <tr><td><a href="data-platform.html">Big Data Platform</a></td><td>CTO, CDO</td><td>Hadoop/Spark on-premise, без vendor lock-in</td></tr>
              </tbody>
            </table>
          </div>"""
    html = html.replace(
        '<div class="row g-3">\n            <div class="col-12 col-lg-6">\n              <a class="products-card" href="federated-learning.html">',
        products_panel + '\n          <div class="row g-3">\n            <div class="col-12 col-lg-6">\n              <a class="products-card" href="federated-learning.html">',
        1,
    )

    html = html.replace(
        '<h2 class="h4 mb-2" style="color: #ffffff !important; font-size: 1.5rem !important;">Готовы разрабатывать ПО вместе с нами?</h2>',
        '<h2 class="h4 mb-2" style="color: #ffffff !important; font-size: 1.5rem !important;">Как начать сотрудничество с DigiTrack?</h2>',
    )

    coop_steps = """              <ol class="text-mute-300 small mb-3">
                <li>Заявка на <a href="mailto:info@digi-track.ru">info@digi-track.ru</a></li>
                <li>Согласование сценария: пилот FL, BDP или партнёрство</li>
                <li>Оценка данных и архитектуры (1–2 недели для FL)</li>
                <li>Договор и развёртывание on-premise</li>
              </ol>"""
    html = html.replace(
        '<p class="text-mute-300 mb-3">Присоединяйтесь к команде разработчиков',
        coop_steps + '\n              <p class="text-mute-300 mb-3">Присоединяйтесь к команде разработчиков',
    )

    extra_faq = """
          <div class="accordion-item">
            <h2 class="accordion-header" id="f6">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#fa6" aria-expanded="false" aria-controls="fa6">
                Передаются ли данные клиентов третьим лицам?
              </button>
            </h2>
            <div id="fa6" class="accordion-collapse collapse" aria-labelledby="f6" data-bs-parent="#faqAcc">
              <div class="accordion-body">
                <p class="snippet-answer mb-2">Нет — данные остаются у владельца, передаются только зашифрованные обновления модели.</p>
                <p class="mb-0">Подробнее: <a href="federated-learning.html#faq">FAQ по федеративному обучению</a>.</p>
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="f7">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#fa7" aria-expanded="false" aria-controls="fa7">
                Где получить коммерческое предложение?
              </button>
            </h2>
            <div id="fa7" class="accordion-collapse collapse" aria-labelledby="f7" data-bs-parent="#faqAcc">
              <div class="accordion-body">
                <p class="snippet-answer mb-0">Email: <a href="mailto:info@digi-track.ru">info@digi-track.ru</a>, тел.: <a href="tel:+79857704512">+7 985 770-45-12</a>. <a href="contacts.html">Контакты →</a></p>
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="f8">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#fa8" aria-expanded="false" aria-controls="fa8">
                Когда лучше начать пилот федеративного обучения?
              </button>
            </h2>
            <div id="fa8" class="accordion-collapse collapse" aria-labelledby="f8" data-bs-parent="#faqAcc">
              <div class="accordion-body">
                <p class="geo-timing mb-0">При наличии дата-партнёра с комплементарными данными — старт за 1–2 недели после заявки. <a href="partnership.html">Партнёрство →</a></p>
              </div>
            </div>
          </div>"""
    html = html.replace("        </div>\n      </div>\n    </section>\n\n    <!-- ПОСЛЕДНИЕ СТАТЬИ", extra_faq + "\n        </div>\n      </div>\n    </section>\n\n    <!-- ПОСЛЕДНИЕ СТАТЬИ", 1)

    html = html.replace(
        '<h2 class="h3 mb-0">Последние статьи и новости</h2>',
        '<h2 class="h3 mb-0">Какие статьи помогут разобраться в технологиях?</h2>',
    )

    html = html.replace('href="index.html">О компании</a>', 'href="contacts.html">Контакты</a>', 1)
    return html


def patch_federated_learning(html: str) -> str:
    html = remove_fl_org_schema(html)
    html = upsert_meta(
        html,
        title="Федеративное обучение для бизнеса — VFL, HFL | DigiTrack",
        description="DigiTrack Confidential Computing: обучение ML без передачи ПДн. VFL, HFL, гомоморфное шифрование, on-premise. Пилот за 1–2 недели.",
        canonical_path="/federated-learning.html",
    )
    html = add_schema_link(html, "../seo/schema-updated.jsonld" if False else "/seo/schema-updated.jsonld")
    html = add_page_faq_schema(
        html,
        [
            ("Как подключиться к федеративному обучению?", "Оставьте заявку на info@digi-track.ru — пилот за 1–2 недели."),
            ("Передаются ли сырые данные?", "Нет, только зашифрованные обновления модели."),
        ],
        f"{BASE}/federated-learning.html#faq",
    )

    html = html.replace(
        '<h1 class="h1 mb-2 text-white">Федеративное обучение для бизнеса</h1>',
        '<h1 class="h1 mb-2 text-white">Федеративное обучение для бизнеса — DigiTrack Confidential Computing</h1>',
    )
    html = html.replace(
        '<p class="text-white mb-3 fs-6">',
        '<p class="text-white mb-3 fs-6 geo-definition">Федеративное обучение — ML на данных нескольких организаций без передачи ПДн. VFL, HFL и Federated XGBoost on-premise с гомоморфным шифрованием. ',
        1,
    )

    replacements = [
        ("<h2 class=\"h3 mb-4\">Препятствия для совместного ИИ‑обучения</h2>", "<h2 class=\"h3 mb-2\">Почему совместное обучение ИИ часто невозможно?</h2>\n        <p class=\"snippet-answer\">152-ФЗ, банковская тайна и изоляция данных не дают собрать общий Data Lake — каждый участник упирается в потолок качества модели.</p>"),
        ("<h3 class=\"h5 mb-2\">Данные под замком</h3>", "<h3 class=\"h5 mb-2\">Почему данные остаются «под замком»?</h3>"),
        ("<h3 class=\"h5 mb-2\">Ограниченность данных</h3>", "<h3 class=\"h5 mb-2\">Почему одному участнику не хватает данных?</h3>"),
        ("<h3 class=\"h5 mb-2\">Потерянная ценность</h3>", "<h3 class=\"h5 mb-2\">Какую ценность теряет бизнес без партнёрских данных?</h3>"),
        ("<h2 class=\"h3 mb-1\">Технология федеративного обучения <br> - универсальное решение проблем</h2>", "<h2 class=\"h3 mb-1\">Что такое федеративное обучение?</h2>"),
        ("<h2 class=\"h4 m-0\" style=\"color: #1A363A !important;\">Этапы вычисления</h2>", "<h2 class=\"h4 m-0\" style=\"color: #1A363A !important;\">Какие этапы внедрения федеративного обучения?</h2>"),
        ("<h2 class=\"h4 mb-1\">Варианты федеративного обучения:</h2>", "<h2 class=\"h4 mb-1\">Какой тип федеративного обучения выбрать — VFL или HFL?</h2>"),
        ("<h3 class=\"h6 mb-1\">Данные разных пользователей</h3>", "<h3 class=\"h6 mb-1\">Что такое HFL (горизонтальный FL)?</h3>"),
        ("<h3 class=\"h6 mb-1\">Данные одних пользователей</h3>", "<h3 class=\"h6 mb-1\">Что такое VFL (вертикальный FL)?</h3>"),
        ("<h2 class=\"h4 mb-2\">Получить программу<br>федеративного обучения</h2>", "<h2 class=\"h4 mb-2\">Как получить DigiTrack Confidential Computing?</h2>"),
        ("<h2 class=\"h3 mb-0\">Последние статьи и новости</h2>", "<h2 class=\"h3 mb-0\">Какие материалы читать по теме FL?</h2>"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)

    compare_table = """
        <div class="seo-table-wrap mb-4">
          <table class="seo-table">
            <thead><tr><th>Подход</th><th>Данные покидают контур?</th><th>152-ФЗ</th><th>Качество</th></tr></thead>
            <tbody>
              <tr><td>Data Lake</td><td>Да</td><td>Риск</td><td>Высокое</td></tr>
              <tr><td>Sandbox</td><td>Да</td><td>Риск</td><td>Среднее–высокое</td></tr>
              <tr><td>Эмбеддинги</td><td>Частично</td><td>Компромисс</td><td>Среднее</td></tr>
              <tr><td><strong>Федеративное обучение</strong></td><td><strong>Нет</strong></td><td><strong>Да</strong></td><td><strong>Высокое</strong></td></tr>
            </tbody>
          </table>
          <p class="small mb-0"><a href="blog/articles/fl-sandbox-or-embeddings.html">Sandbox vs эмбеддинги vs FL →</a></p>
        </div>"""
    html = html.replace(
        '<p class="text-mute-300 mb-4">Техника машинного обучения, при которой данные',
        compare_table + '\n        <p class="text-mute-300 mb-4">Техника машинного обучения, при которой данные',
    )

    vfl_link = '<p class="small text-mute-300 mb-4"><a href="learning-types.html">Типы FL →</a> · <a href="blog/articles/vfl-or-hfl.html">VFL или HFL — подробнее →</a></p>'
    html = html.replace(
        '<p class="text-mute-300 mb-4">Есть два возможных варианта проведения обучения</p>',
        '<p class="snippet-answer">HFL — одинаковые признаки, разные клиенты. VFL — общие клиенты, разные признаки; основной режим для скоринга и антифрода.</p>\n        ' + vfl_link,
    )

    pricing = """
    <section id="pricing" class="py-6 bg-section">
      <div class="container">
        <h2 class="h3 fw-700 mb-2">Сколько стоит федеративное обучение?</h2>
        <p class="snippet-answer">Стоимость индивидуальна — от 1 млн ₽ без НДС. КП: info@digi-track.ru.</p>
        <div class="seo-table-wrap">
          <table class="seo-table">
            <thead><tr><th>Пакет</th><th>Состав</th><th>Срок</th></tr></thead>
            <tbody>
              <tr><td>Пилот</td><td>FL + PSI, 2 участника</td><td>4–6 мес.</td></tr>
              <tr><td>Enterprise</td><td>Лицензия + L4</td><td>12+ мес.</td></tr>
              <tr><td>Партнёрство</td><td>Revenue share</td><td>ongoing</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>"""
    html = html.replace('<section id="faq"', pricing + '\n    <section id="faq"', 1)

    checklist = """
    <section id="fl-checklist" class="py-6">
      <div class="container">
        <h2 class="h4 fw-700 mb-2">Готовы ли вы к федеративному обучению?</h2>
        <details class="seo-details">
          <summary>Чек-лист</summary>
          <ul class="seo-checklist mt-3">
            <li>Определён тип FL (VFL/HFL)</li>
            <li>Есть партнёр с комплементарными признаками</li>
            <li>Выделена on-premise инфраструктура</li>
            <li>Согласованы условия 152-ФЗ</li>
            <li>Определены метрики успеха (AUC, Gini)</li>
          </ul>
        </details>
      </div>
    </section>"""
    html = html.replace('<section id="faq"', checklist + '\n    <section id="faq"', 1)

    extra_faq = """
          <div class="accordion-item">
            <h2 class="accordion-header" id="f6">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#fa6" aria-expanded="false" aria-controls="fa6">
                Где получить документацию на ПО?
              </button>
            </h2>
            <div id="fa6" class="accordion-collapse collapse" aria-labelledby="f6" data-bs-parent="#faqAcc">
              <div class="accordion-body"><p class="snippet-answer mb-0"><a href="documents.html">Документы DigiTrack Confidential Computing →</a></p></div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="f7">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#fa7" aria-expanded="false" aria-controls="fa7">
                Когда лучше начать пилот?
              </button>
            </h2>
            <div id="fa7" class="accordion-collapse collapse" aria-labelledby="f7" data-bs-parent="#faqAcc">
              <div class="accordion-body"><p class="geo-timing mb-0">При готовом дата-партнёре — kick-off через 2–4 недели. <a href="partnership.html">Партнёрство →</a></p></div>
            </div>
          </div>"""
    html = html.replace(
        '<div class="accordion-body">\n                Конфиденциальные вычисления позволяют',
        '<div class="accordion-body">\n                <p class="snippet-answer mb-2">Аналитика без нарушения приватности и 152-ФЗ.</p>\n                <p class="mb-0">Конфиденциальные вычисления позволяют',
    )
    html = html.replace("        </div>\n      </div>\n    </section>\n\n    <!-- НОВОСТИ -->", extra_faq + "\n        </div>\n      </div>\n    </section>\n\n    <!-- НОВОСТИ -->")

    html = html.replace('<a href="blog.html" class="btn-news-link">Узнать больше →</a>', '<a href="blog/articles/vfl-or-hfl.html" class="btn-news-link">Узнать больше →</a>', 1)
    html = html.replace('<h3 class="h6 mb-1">Вертикальное федеративное обучение</h3>', '<h3 class="h6 mb-1">VFL для финансового сектора</h3>', 1)
    html = html.replace('<a href="blog.html" class="btn-news-link">Узнать больше →</a>', '<a href="blog/articles/fl-guide.html" class="btn-news-link">Узнать больше →</a>', 1)
    html = html.replace('<h3 class="h6 mb-1">Горизонтальное федеративное обучение</h3>', '<h3 class="h6 mb-1">HFL: обучение на разных клиентах</h3>', 1)
    html = html.replace('<a href="blog.html" class="btn-news-link">Узнать больше →</a>', '<a href="blog/articles/confidential-computing-152.html" class="btn-news-link">Узнать больше →</a>', 1)
    return html


def patch_data_platform(html: str) -> str:
    html = upsert_meta(
        html,
        title="Big Data Platform on-premise — Hadoop, Spark | DigiTrack",
        description="Enterprise-платформа данных без vendor lock-in: 1 ПБ+ в prod, Astra Linux, zero downtime. Dev/Test бесплатно. TCO: info@digi-track.ru",
        canonical_path="/data-platform.html",
    )
    html = add_schema_link(html)
    html = add_page_faq_schema(
        html,
        [
            ("Сколько стоит DigiTrack Big Data Platform?", "Dev/Test/UAT бесплатно. Production — по Data Nodes. TCO: info@digi-track.ru."),
            ("Работает ли на Astra Linux?", "Да, сертифицированная сборка под Воронеж 1.8."),
        ],
        f"{BASE}/data-platform.html#faq",
    )

    html = html.replace(
        '<h1 class="display-5 fw-800 mb-3 text-white">Big Data Enterprise Platform</h1>',
        '<h1 class="display-5 fw-800 mb-3 text-white">Big Data Platform on-premise — DigiTrack Enterprise</h1>',
    )
    html = html.replace(
        '<p class="text-white mb-4 hero-lead-md">',
        '<p class="text-white mb-4 hero-lead-md geo-definition">Корпоративная платформа данных на Astra Linux: Hadoop, Spark, Kafka, Delta Lake. 1 ПБ+ в prod, zero downtime, без vendor lock-in. ',
        1,
    )

    reps = [
        ("<h2 class=\"h3 fw-700 mb-3\">Почему DigiTrack Big Data Platform?</h2>", "<h2 class=\"h3 fw-700 mb-2\">Почему выбирают DigiTrack Big Data Platform?</h2>\n        <p class=\"snippet-answer\">100% open source, Astra Linux, SRE zero downtime и прозрачное лицензирование — платформа на 1 ПБ+ без «чёрных ящиков».</p>"),
        ("<h3 class=\"h6 mb-2\">Нет vendor lock-in</h3>", "<h3 class=\"h6 mb-2\">Почему нет vendor lock-in?</h3>"),
        ("<h3 class=\"h6 mb-2\">Российская платформа</h3>", "<h3 class=\"h6 mb-2\">Почему платформа российская?</h3>"),
        ("<h2 class=\"h3 fw-700 mb-4\">Battle-tested в промышленной эксплуатации</h2>", "<h2 class=\"h3 fw-700 mb-2\">Какие показатели у платформы в prod?</h2>\n        <p class=\"snippet-answer\">1 ПБ+, 40 Data Nodes, 15 000 msg/s Kafka, 500+ DAG — промышленная эксплуатация 24/7.</p>"),
        ("<h2 class=\"h3 fw-700 mb-4\">Технологический стек</h2>", "<h2 class=\"h3 fw-700 mb-2\">Какой технологический стек входит в платформу?</h2>"),
        ("<h2 class=\"h3 fw-700 mb-4\">Архитектура потоков данных</h2>", "<h2 class=\"h3 fw-700 mb-2\">Как устроена архитектура потоков данных?</h2>"),
        ("<h2 class=\"h3 fw-700 mb-3\">Умный SRE и защита от человеческого фактора</h2>", "<h2 class=\"h3 fw-700 mb-2\">Как платформа обеспечивает zero downtime?</h2>"),
        ("<h2 class=\"h3 fw-700 mb-3\">Справедливое лицензирование. Вы платите только за Production</h2>", "<h2 class=\"h3 fw-700 mb-2\">Сколько стоит DigiTrack Big Data Platform?</h2>\n        <p class=\"snippet-answer\">Dev/Test/UAT и management nodes — бесплатно. Production — по узлам или ресурсам. L4 включена.</p>"),
        ("<h2 class=\"h3 fw-700 mb-3\">Roadmap продукта (2026–2027)</h2>", "<h2 class=\"h3 fw-700 mb-2\">Когда выйдут ключевые функции roadmap?</h2>"),
        ("<h2 class=\"h4 mb-2 dp-cta-title\">Готовы к импортозамещению без потери контроля?</h2>", "<h2 class=\"h4 mb-2 dp-cta-title\">Как начать миграцию на открытый стек?</h2>"),
        ("<h2 class=\"h3 mb-0\">Последние статьи и новости</h2>", "<h2 class=\"h3 mb-0\">Какие статьи читать о платформе данных?</h2>"),
    ]
    for old, new in reps:
        html = html.replace(old, new)

    lic_table = """
          <div class="seo-table-wrap mt-3">
            <table class="seo-table">
              <thead><tr><th>Модель</th><th>Оплата</th></tr></thead>
              <tbody>
                <tr><td>Dev / Test / UAT</td><td>Бесплатно</td></tr>
                <tr><td>Management nodes (до 6)</td><td>Бесплатно</td></tr>
                <tr><td>Production Node-based</td><td>По Data Nodes</td></tr>
                <tr><td>Production Resource-based</td><td>vCPU + Storage</td></tr>
              </tbody>
            </table>
            <p class="small mb-0"><a href="blog/articles/tco-big-data.html">Рассчитать TCO →</a> · <a href="blog/articles/choose-bdp-15.html">15 критериев выбора →</a></p>
          </div>"""
    html = html.replace(
        '<div class="d-flex flex-wrap gap-2 mt-4 dp-licensing-actions',
        lic_table + '\n          <div class="d-flex flex-wrap gap-2 mt-4 dp-licensing-actions',
    )

    faq_section = """
    <section id="faq" class="py-6 bg-section">
      <div class="container">
        <h2 class="h3 fw-700 mb-4">Часто задаваемые вопросы о платформе данных</h2>
        <div class="accordion" id="faqAcc">
          <div class="accordion-item">
            <h2 class="accordion-header" id="df1"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#dfa1">Чем отличается от облачных решений?</button></h2>
            <div id="dfa1" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="snippet-answer mb-0">On-premise, полный контроль, нет egress-платежей, открытый код Apache.</p></div></div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="df2"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#dfa2">Есть ли vendor lock-in?</button></h2>
            <div id="dfa2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="snippet-answer mb-0">Нет — vanilla Apache + Ansible. <a href="blog/articles/opensource-enterprise.html">Open Source →</a></p></div></div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="df3"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#dfa3">Можно ли масштабировать без простоя?</button></h2>
            <div id="dfa3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="snippet-answer mb-0">Да — rolling restart и горизонтальное добавление Data Nodes.</p></div></div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="df4"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#dfa4">Подходит ли для MLOps?</button></h2>
            <div id="dfa4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="snippet-answer mb-0">JupyterHub + Delta Lake + Kafka для feature pipelines. <a href="blog/articles/ai-ready-platform.html">AI-ready →</a></p></div></div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="df5"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#dfa5">Как считается TCO?</button></h2>
            <div id="dfa5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="snippet-answer mb-0">Железо + инженеры + поддержка, без роялти за Hadoop/Spark.</p></div></div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="df6"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#dfa6">Где запросить архитектуру?</button></h2>
            <div id="dfa6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="snippet-answer mb-0"><a href="mailto:info@digi-track.ru">info@digi-track.ru</a> · <a href="contacts.html">Контакты →</a></p></div></div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="df7"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#dfa7">Когда регистрация в реестре РФ?</button></h2>
            <div id="dfa7" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="geo-timing mb-0">Q1 2027 — заявка в Реестр российского ПО.</p></div></div>
          </div>
        </div>
        <details class="seo-details mt-4">
          <summary>Чек-лист выбора Big Data Platform (10 критериев)</summary>
          <ul class="seo-checklist mt-3">
            <li>Open Source без проприетарных зависимостей</li>
            <li>Astra Linux / импортозамещение</li>
            <li>HA и zero downtime</li>
            <li>Delta Lake / ACID</li>
            <li>CDC Debezium</li>
            <li>Мультиверсионность Spark/Python</li>
            <li>IaC Ansible</li>
            <li>Dev-среды бесплатно</li>
            <li>L3/L4 поддержка</li>
            <li>Roadmap и реестр РФ</li>
          </ul>
        </details>
      </div>
    </section>
"""
    html = html.replace("    <!-- ПОСЛЕДНИЕ СТАТЬИ", faq_section + "\n    <!-- ПОСЛЕДНИЕ СТАТЬИ")
    html = html.replace('href="index.html">О компании</a>', 'href="contacts.html">Контакты</a>', 1)
    return html


def patch_partnership(html: str) -> str:
    html = upsert_meta(
        html,
        title="Партнёрство в федеративном обучении — DigiTrack",
        description="Станьте дата-партнёром: FL без передачи ПДн, revenue share, пилот 6 мес. Банки, телеком. Заявка: info@digi-track.ru",
        canonical_path="/partnership.html",
    )
    html = add_schema_link(html)

    reps = [
        ('<h1 class="display-5 fw-800 mb-3 text-white">Партнерство с DigiTrack</h1>', '<h1 class="display-5 fw-800 mb-3 text-white">Партнёрство в федеративном обучении — DigiTrack</h1>'),
        ('<h2 class="h3 fw-700 mb-4">Кто может стать партнером</h2>', '<h2 class="h3 fw-700 mb-2">Кто может стать партнёром DigiTrack?</h2>\n        <p class="snippet-answer">Банки, финтех, телеком и организации с Big Data — монетизация данных через FL без их передачи.</p>'),
        ('<h3 class="h5 mb-3">Финансовые организации</h3>', '<h3 class="h5 mb-3">Какие финансовые организации подходят?</h3>'),
        ('<h3 class="h5 mb-3">BigData организации</h3>', '<h3 class="h5 mb-3">Какие Big Data организации подходят?</h3>'),
        ('<h2 class="h3 mb-4">Что нужно для пилота со стороны дата партнера — на примере пилота по федеративному обучению</h2>', '<h2 class="h3 mb-2">Как проходит пилот федеративного обучения?</h2>\n        <p class="geo-timing">Полный цикл — 6 месяцев (M1–M6): kick-off → инфраструктура → обучение → оценка → prod.</p>'),
        ('<h2 class="h3 fw-700 mb-4">Преимущества партнерства</h2>', '<h2 class="h3 fw-700 mb-2">Почему выгодно партнёрство с DigiTrack?</h2>'),
        ('<h3 class="h5 mb-2">Монетизация данных</h3>', '<h3 class="h5 mb-2">Как происходит монетизация данных?</h3>'),
        ('<h3 class="h5 mb-2">Повышение точности</h3>', '<h3 class="h5 mb-2">Почему растёт точность моделей?</h3>'),
        ('<h3 class="h5 mb-2">Полная безопасность</h3>', '<h3 class="h5 mb-2">Как обеспечивается безопасность?</h3>'),
        ('<h2 class="h4 mb-2" style="color: #ffffff !important; font-size: 1.5rem !important;">Готовы стать партнером?</h2>', '<h2 class="h4 mb-2" style="color: #ffffff !important; font-size: 1.5rem !important;">Как подать заявку на партнёрство?</h2>'),
    ]
    for old, new in reps:
        html = html.replace(old, new)

    links = '<p class="small mb-4"><a href="federated-learning.html#tech">Технология FL →</a> · <a href="documents.html">Документация ПО →</a></p>'
    html = html.replace(
        '<p class="text-mute-300 mb-5">Мы открыты для сотрудничества',
        links + '\n        <p class="text-mute-300 mb-5">Мы открыты для сотрудничества',
    )

    extra_faq = """
          <div class="accordion-item">
            <h2 class="accordion-header" id="f6"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#fa6">Сколько длится пилот?</button></h2>
            <div id="fa6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="geo-timing mb-0">6 месяцев (M1–M6) по timeline на странице.</p></div></div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="f7"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#fa7">Где подать заявку?</button></h2>
            <div id="fa7" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body"><p class="snippet-answer mb-0"><a href="mailto:info@digi-track.ru">info@digi-track.ru</a> · <a href="contacts.html">Контакты →</a></p></div></div>
          </div>"""
    html = html.replace(
        "            </div>\n          </div>\n        </div>\n      </div>\n    </section>\n\n\n  </main>",
        "            </div>\n          </div>\n" + extra_faq + "        </div>\n      </div>\n    </section>\n\n\n  </main>",
        1,
    )

    checklist = """
    <section id="readiness-checklist" class="py-6">
      <div class="container">
        <h2 class="h3 fw-700 mb-2">Готов ли ваш бизнес к партнёрству с DigiTrack?</h2>
        <p class="snippet-answer">Чек-лист для CTO/CDO перед пилотом федеративного обучения или внедрением платформы данных.</p>
        <details class="seo-details" open>
          <summary>Чек-лист готовности</summary>
          <ul class="seo-checklist mt-3">
            <li>Есть on-premise инфраструктура или план её выделения</li>
            <li>Определён use case: скоринг, антифрод или платформа данных</li>
            <li>Согласованы требования ИБ и 152-ФЗ</li>
            <li>Есть дата-партнёр (FL) или объём данных &gt;100 ГБ (BDP)</li>
            <li>Назначен владелец проекта (CTO/CDO/CRO)</li>
          </ul>
        </details>
      </div>
    </section>

    <section id="contacts" class="py-6 bg-section">
      <div class="container">
        <h2 class="h3 fw-700 mb-2">Где связаться с DigiTrack?</h2>
        <p class="snippet-answer">Коммерческие предложения и консультации — по email и телефону. Офис в Москве.</p>
        <div class="seo-table-wrap">
          <table class="seo-table">
            <tbody>
              <tr><th>Email</th><td><a href="mailto:info@digi-track.ru">info@digi-track.ru</a></td></tr>
              <tr><th>Телефон</th><td><a href="tel:+79857704512">+7 985 770-45-12</a></td></tr>
              <tr><th>Адрес</th><td>115114, Москва, Шлюзовая наб., д. 8, стр. 1</td></tr>
              <tr><th>Документация ПО</th><td><a href="documents.html">documents.html</a></td></tr>
            </tbody>
          </table>
        </div>
        <p class="mb-0"><a href="contacts.html" class="btn-news-link">Страница контактов →</a></p>
      </div>
    </section>"""
    html = html.replace("    <!-- FAQ -->", checklist + "\n    <!-- FAQ -->")
    html = html.replace('href="index.html">О компании</a>', 'href="contacts.html">Контакты</a>', 1)
    return html


def patch_blog(html: str) -> str:
    html = upsert_meta(
        html,
        title="Блог DigiTrack — федеративное обучение, Big Data, 152-ФЗ",
        description="15 экспертных статей о федеративном обучении, VFL/HFL, Hadoop/Spark on-premise и confidential computing для enterprise.",
        canonical_path="/blog.html",
    )
    html = add_schema_link(html)
    html = html.replace(
        '<h2 class="h3 fw-700 mb-2">Блог DigiTrack</h2>',
        '<h1 class="h3 fw-700 mb-2">Блог DigiTrack — федеративное обучение и платформа данных</h1>\n          <p class="snippet-answer">Экспертные материалы о FL, VFL/HFL, Big Data Platform, 152-ФЗ и on-premise AI.</p>\n          <div class="blog-hub-filters d-flex flex-wrap gap-2 mb-3">\n            <button type="button" class="btn btn-sm btn-outline-secondary active" data-hub-filter="all">Все</button>\n            <button type="button" class="btn btn-sm btn-outline-secondary" data-hub-filter="fl">Федеративное обучение</button>\n            <button type="button" class="btn btn-sm btn-outline-secondary" data-hub-filter="bdp">Платформа данных</button>\n          </div>',
    )

    search_js = """
      const params = new URLSearchParams(location.search);
      const qParam = params.get('q');
      if (qParam && searchInput) {
        searchInput.value = qParam;
        searchInput.dispatchEvent(new Event('input'));
      }

      document.querySelectorAll('[data-hub-filter]').forEach(function(btn) {
        btn.addEventListener('click', function() {
          document.querySelectorAll('[data-hub-filter]').forEach(function(b) { b.classList.remove('active'); });
          btn.classList.add('active');
          const hub = btn.getAttribute('data-hub-filter');
          document.querySelectorAll('.blog-card').forEach(function(card) {
            const match = hub === 'all' || card.getAttribute('data-hub') === hub;
            card.classList.toggle('d-none', !match);
          });
        });
      });"""
    html = html.replace(
        "        });\n      }\n    });",
        "        });\n      }\n" + search_js + "\n    });",
    )
    html = html.replace('href="index.html">О компании</a>', 'href="contacts.html">Контакты</a>', 1)
    return html


def patch_learning_types(html: str) -> str:
    html = upsert_meta(
        html,
        title="VFL или HFL — типы федеративного обучения | DigiTrack",
        description="Как выбрать VFL или HFL для вашего проекта: горизонтальный и вертикальный режим федеративного обучения. Консультация: info@digi-track.ru",
        canonical_path="/learning-types.html",
    )
    html = add_schema_link(html)
    reps = [
        ("<h2 class=\"h3 mb-4\">Два основных типа федеративного обучения</h2>", "<h2 class=\"h3 mb-2\">Какие типы федеративного обучения существуют?</h2>"),
        ("<h2 class=\"h4 mb-3\">Когда использовать</h2>", "<h2 class=\"h4 mb-3\">Когда использовать HFL?</h2>"),
        ("<h2 class=\"h4 mb-3\">Примеры применения</h2>", "<h2 class=\"h4 mb-3\">Где применяется HFL?</h2>"),
        ("<h2 class=\"h4 mb-3\">Преимущества</h2>", "<h2 class=\"h4 mb-3\">В чём преимущества HFL?</h2>"),
        ("<h2 class=\"h4 mb-3\">Как выбрать подходящий тип?</h2>", "<h2 class=\"h4 mb-3\">Как выбрать VFL или HFL?</h2>"),
    ]
    for old, new in reps:
        html = html.replace(old, new, 1)
    html = html.replace(
        '<p class="text-mute-300 mb-4">',
        '<p class="snippet-answer"><a href="blog/articles/vfl-or-hfl.html">Подробное сравнение VFL и HFL →</a></p>\n        <p class="text-mute-300 mb-4">',
        1,
    )
    return html


def patch_documents(html: str) -> str:
    if '<meta name="description"' not in html:
        html = html.replace(
            "<title>Документы</title>",
            '<title>Документы DigiTrack Confidential Computing</title>\n  <meta name="description" content="Руководство, инструкция по установке и описание функциональных характеристик ПО DigiTrack Confidential Computing."/>',
        )
    html = html.replace(
        '<meta name="robots"',
        '<link rel="canonical" href="https://digi-track.ru/documents.html"/>\n  <meta name="robots"',
        1,
    ) if 'canonical' not in html else html
    return html


def patch_expert_review(html: str) -> str:
    if '<meta name="description"' not in html:
        html = html.replace(
            "<title>Экспертная проверка ПО</title>",
            '<title>Экспертная проверка ПО — DigiTrack</title>\n  <meta name="description" content="Материалы для экспертной проверки ПО DigiTrack Confidential Computing: скачивание, развёртывание, демо-стенд."/>\n  <meta name="robots" content="noindex, follow"/>',
        )
    return html


def add_article_ctas():
    manifest = json.loads((ROOT / "blog/articles-manifest.json").read_text(encoding="utf-8"))
    for item in manifest:
        path = ROOT / "blog/articles" / f"{item['slug']}.html"
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        if "article-product-cta" in html:
            continue
        cta = ARTICLE_CTA_FL if item.get("hub") == "fl" else ARTICLE_CTA_BDP
        if "</article>" in html:
            html = html.replace("</article>", cta + "\n      </article>", 1)
            path.write_text(html, encoding="utf-8")


def write_sitemap():
    pages = [
        ("index.html", "1.0", "weekly"),
        ("federated-learning.html", "1.0", "weekly"),
        ("data-platform.html", "1.0", "weekly"),
        ("partnership.html", "0.8", "monthly"),
        ("blog.html", "0.8", "weekly"),
        ("learning-types.html", "0.8", "monthly"),
        ("about.html", "0.7", "monthly"),
        ("site-map.html", "0.5", "monthly"),
        ("vacancies.html", "0.3", "monthly"),
        ("documents.html", "0.3", "yearly"),
        ("expert-review.html", "0.3", "yearly"),
    ]
    # never include deleted stubs: contacts.html, voprosy.html, kak-my-rabotaem.html
    manifest = json.loads((ROOT / "blog/articles-manifest.json").read_text(encoding="utf-8"))
    for item in manifest:
        pages.append((f"blog/articles/{item['slug']}.html", "0.6", "monthly"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio, freq in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE}/{path}</loc>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_contacts_html():
    """Stubs removed — contacts live at about.html#contacts."""
    for stub in ("contacts.html", "voprosy.html", "kak-my-rabotaem.html"):
        p = ROOT / stub
        if p.exists():
            p.unlink()


def main():
    css_path = ROOT / "styles.css"
    if "/* SEO / AEO / GEO blocks */" not in css_path.read_text(encoding="utf-8"):
        css_path.write_text(css_path.read_text(encoding="utf-8") + SEO_CSS, encoding="utf-8")

    write_contacts_html()
    write_sitemap()

    handlers = {
        "index.html": patch_index,
        "federated-learning.html": patch_federated_learning,
        "data-platform.html": patch_data_platform,
        "partnership.html": patch_partnership,
        "blog.html": patch_blog,
        "learning-types.html": patch_learning_types,
        "documents.html": patch_documents,
        "expert-review.html": patch_expert_review,
    }

    for name, fn in handlers.items():
        path = ROOT / name
        html = path.read_text(encoding="utf-8")
        html = fix_legal_h6(html)
        html = fn(html)
        path.write_text(html, encoding="utf-8")
        print(f"Updated {name}")

    for html_path in ROOT.glob("**/*.html"):
        if html_path.name in handlers:
            continue
        text = html_path.read_text(encoding="utf-8")
        new_text = fix_legal_h6(text)
        if "contacts.html" not in new_text and 'href="index.html">О компании</a>' in new_text:
            new_text = new_text.replace('href="index.html">О компании</a>', 'href="contacts.html">Контакты</a>', 1)
        if new_text != text:
            html_path.write_text(new_text, encoding="utf-8")
            print(f"Fixed footer/modals: {html_path.relative_to(ROOT)}")

    add_article_ctas()
    print("Done.")


if __name__ == "__main__":
    main()
