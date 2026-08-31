#!/usr/bin/env python3
"""Merge about / contacts / FAQ / HowTo into about.html; stub-redirect old URLs."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://digi-track.ru"

from apply_standard_footer import footer_html  # noqa: E402


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def faq_accordion(questions: list[dict]) -> str:
    items = []
    for i, q in enumerate(questions, start=1):
        qid, aid = f"f{i}", f"fa{i}"
        items.append(
            f"""          <div class="accordion-item faq-item">
            <h2 class="accordion-header" id="{qid}">
              <button class="accordion-button collapsed faq-question" type="button" data-bs-toggle="collapse" data-bs-target="#{aid}" aria-expanded="false" aria-controls="{aid}">
                {q["name"]}
              </button>
            </h2>
            <div id="{aid}" class="accordion-collapse collapse" aria-labelledby="{qid}" data-bs-parent="#faqAcc">
              <div class="accordion-body snippet-answer faq-answer">{q["acceptedAnswer"]["text"]}</div>
            </div>
          </div>"""
        )
    return "\n".join(items)


def howto_steps(steps: list[dict]) -> str:
    blocks = []
    for step in steps:
        url = step.get("url", "#")
        if url.startswith(BASE):
            url = url.replace(BASE + "/", "")
        if "contacts.html" in url:
            url = "about.html#contacts"
        blocks.append(
            f"""          <article class="glass pad-2x mb-3 howto-step" id="howto-step-{step['position']}">
            <h3 class="h5 howto-step-name"><span class="badge bg-success me-2">{step["position"]}</span>{step["name"]}</h3>
            <p class="howto-step-text mb-2">{step["text"]}</p>
            <p class="small mb-0"><a href="{url}">Подробнее →</a></p>
          </article>"""
        )
    return "\n".join(blocks)


def build_schema(faq: dict, howto: dict) -> str:
    faq = json.loads(json.dumps(faq))
    howto = json.loads(json.dumps(howto))
    faq["url"] = f"{BASE}/about.html#faq"
    faq["@id"] = f"{BASE}/about.html#faqpage"
    howto["url"] = f"{BASE}/about.html#process"
    howto["@id"] = f"{BASE}/about.html#howto-order"

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE}/about.html#organization",
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
                    "hoursAvailable": {
                        "@type": "OpeningHoursSpecification",
                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                        "opens": "10:00",
                        "closes": "19:00",
                    },
                },
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Шлюзовая набережная, д. 8, стр. 1",
                    "addressLocality": "Москва",
                    "postalCode": "115114",
                    "addressCountry": "RU",
                },
                "geo": {"@type": "GeoCoordinates", "latitude": 55.7321, "longitude": 37.6534},
            },
            {
                "@type": "WebPage",
                "@id": f"{BASE}/about.html#webpage",
                "url": f"{BASE}/about.html",
                "name": "О компании DigiTrack — контакты, FAQ и этапы работы",
                "description": "Миссия DigiTrack, контакты, вопросы и ответы, пошаговый процесс заказа услуг.",
                "inLanguage": "ru-RU",
                "isPartOf": {"@id": f"{BASE}/#website"},
                "about": {"@id": f"{BASE}/about.html#organization"},
                "hasPart": [
                    {"@id": f"{BASE}/about.html#faqpage"},
                    {"@id": f"{BASE}/about.html#howto-order"},
                ],
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [
                        ".about-mission",
                        ".contact-phone",
                        ".contact-email",
                        ".faq-question",
                        ".faq-answer",
                        ".howto-step-name",
                    ],
                },
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{BASE}/about.html#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/index.html"},
                    {"@type": "ListItem", "position": 2, "name": "О компании", "item": f"{BASE}/about.html"},
                ],
            },
            faq,
            howto,
        ],
    }
    return json.dumps(graph, ensure_ascii=False, indent=2)


def redirect_stub(title: str, target: str, label: str) -> str:
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} — DigiTrack</title>
  <link rel="canonical" href="{BASE}/about.html{target}"/>
  <meta http-equiv="refresh" content="0;url=about.html{target}"/>
  <meta name="robots" content="noindex, follow"/>
  <script>location.replace("about.html{target}");</script>
</head>
<body>
  <p>Раздел перенесён на страницу компании: <a href="about.html{target}">{label}</a>.</p>
</body>
</html>
"""


def build_about(faq: dict, howto: dict) -> str:
    schema = build_schema(faq, howto)
    accordion = faq_accordion(faq["mainEntity"])
    steps = howto_steps(howto["step"])
    footer = footer_html("")

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>О компании DigiTrack — контакты, FAQ и этапы работы</title>
  <meta name="description" content="DigiTrack (ООО «ДТ»): о компании, контакты в Москве, вопросы и ответы, пошаговый процесс заказа FL и Big Data Platform."/>
  <link rel="canonical" href="{BASE}/about.html"/>
  <meta name="robots" content="index, follow"/>
  <meta name="author" content="DigiTrack"/>
  <meta property="og:type" content="website"/>
  <meta property="og:url" content="{BASE}/about.html"/>
  <meta property="og:title" content="О компании DigiTrack — контакты, FAQ и этапы работы"/>
  <meta property="og:description" content="Миссия, контакты, FAQ и этапы работы DigiTrack."/>
  <meta property="og:image" content="{BASE}/img/DataIcon.png"/>
  <meta property="og:site_name" content="DigiTrack"/>
  <meta property="og:locale" content="ru_RU"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./styles.css"/>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <script type="application/ld+json">{schema}</script>
</head>
<body class="bg-deep">
  <nav class="navbar navbar-expand-lg navbar-dark sticky-top nav-glass" aria-label="Primary">
    <div class="container">
      <a class="navbar-brand fw-semibold" href="index.html">DigiTrack</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMain" aria-controls="navMain" aria-expanded="false" aria-label="Переключить меню">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navMain">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="index.html">Главная</a></li>
          <li class="nav-item"><a class="nav-link" href="federated-learning.html#tech">Федеративное обучение</a></li>
          <li class="nav-item"><a class="nav-link" href="data-platform.html">Дата-платформа</a></li>
          <li class="nav-item"><a class="nav-link" href="partnership.html">Партнёрство</a></li>
          <li class="nav-item"><a class="nav-link" href="vacancies.html">Вакансии</a></li>
          <li class="nav-item"><a class="nav-link" href="blog.html">Блог</a></li>
        </ul>
        <div class="d-flex gap-2">
          <button type="button" class="btn btn-primary-gy" data-bs-toggle="modal" data-bs-target="#contactModal">Узнать больше</button>
        </div>
      </div>
    </div>
  </nav>
  <nav class="breadcrumb-nav" aria-label="Хлебные крошки">
    <div class="container">
      <ol class="breadcrumb mb-0" itemscope itemtype="https://schema.org/BreadcrumbList">
        <li class="breadcrumb-item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <a itemprop="item" href="index.html"><span itemprop="name">Главная</span></a>
          <meta itemprop="position" content="1"/>
        </li>
        <li class="breadcrumb-item active" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <span itemprop="name">О компании</span>
          <meta itemprop="position" content="2"/>
        </li>
      </ol>
    </div>
  </nav>

  <main class="py-6 about-page company-hub" style="padding-top: 7rem !important;">
    <div class="container">
      <nav class="company-page-nav mb-4" aria-label="Разделы страницы">
        <ul class="list-inline small mb-0">
          <li class="list-inline-item me-3"><a href="#about">О компании</a></li>
          <li class="list-inline-item me-3"><a href="#contacts">Контакты</a></li>
          <li class="list-inline-item me-3"><a href="#faq">Вопросы и ответы</a></li>
          <li class="list-inline-item"><a href="#process">Как мы работаем</a></li>
        </ul>
      </nav>

      <section id="about" class="mb-5">
        <h1 class="h2 fw-700 mb-2">О компании DigiTrack</h1>
        <p class="snippet-answer geo-definition mb-4">ООО «ДТ» (DigiTrack) — российский разработчик ПО для конфиденциальных вычислений, федеративного обучения и корпоративных платформ данных on-premise.</p>

        <div class="glass pad-2x mb-4" id="mission">
          <h2 class="h4 fw-600 mb-3">Наша миссия</h2>
          <p class="about-mission mb-0">Мы создаём программные продукты, которые позволяют обучать ML-модели и строить аналитику без вывода персональных данных за периметр организации. Наша цель — сделать конфиденциальные вычисления доступными для банков, телекома и enterprise в соответствии с 152-ФЗ и требованиями информационной безопасности.</p>
        </div>

        <div class="mb-4" id="competencies">
          <h2 class="h4 fw-600 mb-3">Ключевые компетенции</h2>
          <ul class="about-competencies">
            <li><strong>Федеративное обучение (FL)</strong> — VFL, HFL, Federated XGBoost, PSI, пилоты с дата-партнёрами. <a href="federated-learning.html">Подробнее →</a></li>
            <li><strong>Платформы данных on‑premise</strong> — Hadoop, Spark, Kafka, Delta Lake на Astra Linux без vendor lock-in. <a href="data-platform.html">Подробнее →</a></li>
            <li><strong>Конфиденциальные вычисления</strong> — гомоморфное шифрование, защищённый обмен градиентами, аудит ИБ.</li>
            <li><strong>ML‑инфраструктура для enterprise</strong> — MLOps, HA-кластеры, zero downtime, сопровождение L3/L4.</li>
          </ul>
        </div>

        <div class="mb-4" id="stats">
          <h2 class="h4 fw-600 mb-3">Цифры и факты</h2>
          <div class="row g-3 about-stats">
            <div class="col-6 col-md-4">
              <div class="glass pad-2x text-center h-100">
                <div class="h3 fw-700 text-success mb-1">2023</div>
                <p class="small mb-0">год основания компании</p>
              </div>
            </div>
            <div class="col-6 col-md-4">
              <div class="glass pad-2x text-center h-100">
                <div class="h3 fw-700 text-success mb-1">10+</div>
                <p class="small mb-0">пилотов и внедрений FL/BDP</p>
              </div>
            </div>
            <div class="col-12 col-md-4">
              <div class="glass pad-2x text-center h-100">
                <div class="h3 fw-700 text-success mb-1">30+</div>
                <p class="small mb-0">инженеров, исследователей и архитекторов</p>
              </div>
            </div>
          </div>
        </div>

        <div class="glass pad-2x mb-4 about-why-us" id="why-us">
          <h2 class="h4 fw-600 mb-3">Почему выбирают нас</h2>
          <ul class="mb-0">
            <li><strong>Собственные продукты</strong> — DigiTrack Confidential Computing и Big Data Platform, а не только консалтинг.</li>
            <li><strong>On-premise и 152-ФЗ</strong> — данные остаются у владельца, стек разворачивается в контуре заказчика.</li>
            <li><strong>Open source без vendor lock-in</strong> — Hadoop, Spark, Kafka; лицензия только за production-узлы BDP.</li>
            <li><strong>Экспертиза FL + Big Data</strong> — команда с опытом в ML, криптографии и платформенной инженерии.</li>
            <li><strong>Сопровождение после запуска</strong> — поддержка L3/L4, обновления и сопровождение дата-партнёров.</li>
          </ul>
        </div>

        <div class="mb-4" id="team">
          <h2 class="h4 fw-600 mb-3">Наша команда</h2>
          <div class="row g-4 align-items-center">
            <div class="col-12 col-md-4 text-center">
              <img src="img/gudov.png" alt="Команда DigiTrack — эксперты по ML и платформам данных" class="rounded-3 about-team-photo" width="280" height="280" loading="lazy"/>
            </div>
            <div class="col-12 col-md-8">
              <p class="mb-2">В DigiTrack работают разработчики с опытом в машинном обучении, криптографии и построении корпоративных data-платформ: PhD и senior-инженеры, архитекторы ПО и специалисты по compliance.</p>
              <p class="mb-0">Мы создаём полноценные продукты — от алгоритмов и API до документации и пользовательских интерфейсов. <a href="blog.html">Экспертные материалы в блоге →</a></p>
            </div>
          </div>
        </div>

        <div class="glass pad-2x" id="join">
          <h2 class="h4 fw-600 mb-3">Присоединяйтесь к нам</h2>
          <p class="mb-3">Ищем ML-инженеров, backend- и platform-разработчиков, специалистов по информационной безопасности.</p>
          <p class="mb-0">
            <a href="vacancies.html" class="btn btn-primary-gy me-2 mb-2">Открытые вакансии</a>
            <a href="partnership.html" class="btn btn-outline-light mb-2">Стать партнёром</a>
            <a href="#contacts" class="btn btn-outline-light mb-2">Связаться с нами</a>
          </p>
        </div>
      </section>

      <hr class="border-ink-700 my-5"/>

      <section id="contacts" class="mb-5 contacts-page">
        <h2 class="h2 fw-700 mb-2">Контакты</h2>
        <p class="snippet-answer mb-4">Свяжитесь с DigiTrack для коммерческих предложений, пилотов федеративного обучения и внедрения Big Data Platform.</p>

        <div class="mb-5" id="reach-us">
          <h3 class="h4 fw-600 mb-3">Свяжитесь с нами</h3>
          <div class="row g-4">
            <div class="col-12 col-md-6 col-lg-4">
              <div class="glass pad-2x h-100">
                <h4 class="h6 text-mute-400 mb-2">Телефон</h4>
                <p class="contact-phone mb-0"><a href="tel:+79857704512">+7 985 770-45-12</a></p>
              </div>
            </div>
            <div class="col-12 col-md-6 col-lg-4">
              <div class="glass pad-2x h-100">
                <h4 class="h6 text-mute-400 mb-2">Email</h4>
                <p class="contact-email mb-0"><a href="mailto:info@digi-track.ru">info@digi-track.ru</a></p>
              </div>
            </div>
            <div class="col-12 col-lg-4">
              <div class="glass pad-2x h-100">
                <h4 class="h6 text-mute-400 mb-2">График работы</h4>
                <p class="contact-hours mb-0">Пн–Пт: 10:00–19:00 (МСК)<br/>Сб–Вс: по договорённости</p>
              </div>
            </div>
          </div>
        </div>

        <div class="mb-5" id="address">
          <h3 class="h4 fw-600 mb-3">Адрес и реквизиты</h3>
          <div class="row g-4">
            <div class="col-12 col-lg-6">
              <p class="contact-address mb-3"><strong>Юридический и фактический адрес:</strong><br/>115114, г. Москва, Шлюзовая набережная, д. 8, стр. 1</p>
              <div class="seo-table-wrap">
                <table class="seo-table">
                  <tbody>
                    <tr><th>Наименование</th><td>ООО «ДТ» (DigiTrack)</td></tr>
                    <tr><th>ИНН</th><td>9705200012</td></tr>
                    <tr><th>ОГРН</th><td>1237700339788</td></tr>
                    <tr><th>Документация ПО</th><td><a href="documents.html">documents.html</a></td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-12 col-lg-6">
              <div class="contact-map rounded-3 overflow-hidden">
                <iframe src="https://yandex.ru/map-widget/v1/?ll=37.653400%2C55.732100&z=16&pt=37.653400%2C55.732100,pm2rdm" width="100%" height="360" frameborder="0" allowfullscreen="true" title="Офис DigiTrack на Яндекс.Картах" loading="lazy"></iframe>
              </div>
              <p class="small mt-2 mb-0"><a href="https://yandex.ru/maps/?pt=37.6534,55.7321&z=16&l=map" target="_blank" rel="noopener noreferrer">Открыть на Яндекс.Картах →</a></p>
            </div>
          </div>
        </div>

        <div class="mb-5" id="social">
          <h3 class="h4 fw-600 mb-3">Мы в соцсетях</h3>
          <ul class="list-inline contact-social mb-0">
            <li class="list-inline-item me-3"><a href="https://t.me/digitrack" rel="noopener noreferrer" target="_blank">Telegram</a></li>
            <li class="list-inline-item me-3"><a href="https://vk.com/digitrack" rel="noopener noreferrer" target="_blank">VK</a></li>
            <li class="list-inline-item me-3"><a href="https://www.youtube.com/@digitrack" rel="noopener noreferrer" target="_blank">YouTube</a></li>
            <li class="list-inline-item"><a href="https://www.linkedin.com/company/digitrack" rel="noopener noreferrer" target="_blank">LinkedIn</a></li>
          </ul>
        </div>

        <div class="mb-0" id="contact-form">
          <h3 class="h4 fw-600 mb-3">Напишите нам</h3>
          <form class="glass pad-2x contact-form" id="contactForm" novalidate>
            <div class="row g-3">
              <div class="col-12 col-md-6">
                <label for="contactName" class="form-label">Имя</label>
                <input type="text" class="form-control" id="contactName" name="name" required autocomplete="name"/>
              </div>
              <div class="col-12 col-md-6">
                <label for="contactEmail" class="form-label">Email</label>
                <input type="email" class="form-control" id="contactEmail" name="email" required autocomplete="email"/>
              </div>
              <div class="col-12">
                <label for="contactMessage" class="form-label">Сообщение</label>
                <textarea class="form-control" id="contactMessage" name="message" rows="5" required placeholder="Опишите задачу: FL, Big Data Platform или партнёрство"></textarea>
              </div>
              <div class="col-12">
                <button type="submit" class="btn btn-primary-gy">Отправить</button>
                <p class="small text-mute-400 mt-2 mb-0">Нажимая «Отправить», вы соглашаетесь на обработку данных для ответа на обращение.</p>
              </div>
            </div>
          </form>
        </div>
      </section>

      <hr class="border-ink-700 my-5"/>

      <section id="faq" class="mb-5">
        <h2 class="h2 fw-700 mb-2">Вопросы и ответы о DigiTrack</h2>
        <p class="snippet-answer geo-definition mb-4">Ответы об услугах, стоимости, сроках внедрения, гарантии и поддержке федеративного обучения и платформы данных.</p>
        <div class="accordion" id="faqAcc">
{accordion}
        </div>
        <p class="small mt-4 mb-0">Не нашли ответ? Смотрите <a href="#process">этапы работы</a>, <a href="partnership.html">партнёрство</a> или <a href="#contacts">напишите нам</a>.</p>
      </section>

      <hr class="border-ink-700 my-5"/>

      <section id="process" class="mb-0">
        <div id="howto-order">
          <h2 class="h2 fw-700 mb-2">Как мы работаем</h2>
          <p class="snippet-answer">Пошаговый процесс заказа федеративного обучения, Big Data Platform или партнёрства с DigiTrack — от заявки до поддержки после запуска.</p>
          <p class="geo-timing mb-4">Ориентировочный срок полного цикла — 6 месяцев. Стоимость — от 1 000 000 ₽ без НДС.</p>
          <h3 class="h4 mb-3">Этапы работы</h3>
{steps}
          <p class="mt-4"><button type="button" class="btn btn-primary-gy" data-bs-toggle="modal" data-bs-target="#contactModal">Оставить заявку</button></p>
          <p class="small mt-3 mb-0">Подробнее о сроках и стоимости — в <a href="#faq">разделе вопросов и ответов</a>. Материалы по продуктам — в <a href="blog.html">блоге</a>.</p>
        </div>
      </section>
    </div>
  </main>

  <section class="contact-cta-bar py-4 border-top border-ink-700" aria-label="Связаться с нами">
    <div class="container text-center text-lg-start">
      <p class="mb-0 snippet-answer"><strong>Остались вопросы?</strong> <a href="#contacts">Свяжитесь с нами</a> — ответим в течение 1 рабочего дня.</p>
    </div>
  </section>

{footer}

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
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>
  <script>
  document.getElementById('year').textContent = new Date().getFullYear();
  document.getElementById('contactForm').addEventListener('submit', function (e) {{
    e.preventDefault();
    var name = document.getElementById('contactName').value.trim();
    var email = document.getElementById('contactEmail').value.trim();
    var message = document.getElementById('contactMessage').value.trim();
    var subject = encodeURIComponent('Заявка с сайта DigiTrack');
    var body = encodeURIComponent('Имя: ' + name + '\\nEmail: ' + email + '\\n\\n' + message);
    window.location.href = 'mailto:info@digi-track.ru?subject=' + subject + '&body=' + body;
  }});
  </script>
</body>
</html>
"""


def patch_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    for page in ("contacts.html", "voprosy.html", "kak-my-rabotaem.html"):
        text = re.sub(
            rf"\s*<url>\s*<loc>{re.escape(BASE)}/{re.escape(page)}</loc>.*?</url>",
            "",
            text,
            count=1,
            flags=re.S,
        )
    path.write_text(text, encoding="utf-8")


def patch_schema_files(faq: dict, howto: dict) -> None:
    faq["url"] = f"{BASE}/about.html#faq"
    faq["@id"] = f"{BASE}/about.html#faqpage"
    howto["url"] = f"{BASE}/about.html#process"
    howto["@id"] = f"{BASE}/about.html#howto-order"
    (ROOT / "schemas" / "faq-schema.jsonld").write_text(
        json.dumps(faq, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "schemas" / "howto-schema.jsonld").write_text(
        json.dumps(howto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    faq = load_schema("faq-schema.jsonld")
    howto = load_schema("howto-schema.jsonld")
    (ROOT / "about.html").write_text(build_about(faq, howto), encoding="utf-8")
    # Do not recreate contacts/voprosy/kak-my-rabotaem stubs — use about.html#…
    for stub in ("contacts.html", "voprosy.html", "kak-my-rabotaem.html"):
        p = ROOT / stub
        if p.exists():
            p.unlink()
    patch_sitemap()
    patch_schema_files(faq, howto)
    print("Merged company page → about.html; stub pages removed from tree and sitemap")


if __name__ == "__main__":
    main()
