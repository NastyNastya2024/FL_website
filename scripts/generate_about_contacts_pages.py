#!/usr/bin/env python3
"""Generate SEO-optimized about.html and contacts.html."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_schema(name: str) -> str:
    data = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
    return json.dumps(data, ensure_ascii=False, indent=2)


def nav(active: str) -> str:
    def cls(page: str) -> str:
        return " active" if active == page else ""

    return f"""  <nav class="navbar navbar-expand-lg navbar-dark sticky-top nav-glass" aria-label="Primary">
    <div class="container">
      <a class="navbar-brand fw-semibold" href="index.html">DigiTrack</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMain" aria-controls="navMain" aria-expanded="false" aria-label="Переключить меню">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navMain">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link{cls('index')}" href="index.html">Главная</a></li>
          <li class="nav-item"><a class="nav-link" href="federated-learning.html#tech">Федеративное обучение</a></li>
          <li class="nav-item"><a class="nav-link" href="data-platform.html">Дата-платформа</a></li>
          <li class="nav-item"><a class="nav-link" href="partnership.html">Партнёрство</a></li>
          <li class="nav-item"><a class="nav-link" href="vacancies.html">Вакансии</a></li>
          <li class="nav-item"><a class="nav-link{cls('blog')}" href="blog.html">Блог</a></li>
        </ul>
        <div class="d-flex gap-2">
          <button type="button" class="btn btn-primary-gy" data-bs-toggle="modal" data-bs-target="#contactModal">Узнать больше</button>
        </div>
      </div>
    </div>
  </nav>"""


def breadcrumbs(current: str) -> str:
    return f"""  <nav class="breadcrumb-nav" aria-label="Хлебные крошки">
    <div class="container">
      <ol class="breadcrumb mb-0" itemscope itemtype="https://schema.org/BreadcrumbList">
        <li class="breadcrumb-item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <a itemprop="item" href="index.html"><span itemprop="name">Главная</span></a>
          <meta itemprop="position" content="1"/>
        </li>
        <li class="breadcrumb-item active" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <span itemprop="name">{current}</span>
          <meta itemprop="position" content="2"/>
        </li>
      </ol>
    </div>
  </nav>"""


def footer() -> str:
    from apply_standard_footer import footer_html

    return footer_html("", compact=False) + """

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
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>"""


def head(title: str, description: str, canonical: str, schema_json: str) -> str:
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <meta name="description" content="{description}"/>
  <link rel="canonical" href="{canonical}"/>
  <meta name="robots" content="index, follow"/>
  <meta name="author" content="DigiTrack"/>
  <meta property="og:type" content="website"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="{description}"/>
  <meta property="og:image" content="https://digi-track.ru/img/DataIcon.png"/>
  <meta property="og:site_name" content="DigiTrack"/>
  <meta property="og:locale" content="ru_RU"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./styles.css"/>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <script type="application/ld+json">{schema_json}</script>
</head>
<body class="bg-deep">"""


def about_body() -> str:
    return """
  <main class="py-6 about-page" style="padding-top: 7rem !important;">
    <div class="container">
      <h1 class="h2 fw-700 mb-2">О компании DigiTrack</h1>
      <p class="snippet-answer geo-definition mb-4">ООО «ДТ» (DigiTrack) — российский разработчик ПО для конфиденциальных вычислений, федеративного обучения и корпоративных платформ данных on-premise.</p>

      <section class="glass pad-2x mb-4" id="mission">
        <h2 class="h4 fw-600 mb-3">Наша миссия</h2>
        <p class="about-mission mb-0">Мы создаём программные продукты, которые позволяют обучать ML-модели и строить аналитику без вывода персональных данных за периметр организации. Наша цель — сделать конфиденциальные вычисления доступными для банков, телекома и enterprise в соответствии с 152-ФЗ и требованиями информационной безопасности.</p>
      </section>

      <section class="mb-4" id="competencies">
        <h2 class="h4 fw-600 mb-3">Ключевые компетенции</h2>
        <ul class="about-competencies">
          <li><strong>Федеративное обучение (FL)</strong> — VFL, HFL, Federated XGBoost, PSI, пилоты с дата-партнёрами. <a href="federated-learning.html">Подробнее →</a></li>
          <li><strong>Платформы данных on‑premise</strong> — Hadoop, Spark, Kafka, Delta Lake на Astra Linux без vendor lock-in. <a href="data-platform.html">Подробнее →</a></li>
          <li><strong>Конфиденциальные вычисления</strong> — гомоморфное шифрование, защищённый обмен градиентами, аудит ИБ.</li>
          <li><strong>ML‑инфраструктура для enterprise</strong> — MLOps, HA-кластеры, zero downtime, сопровождение L3/L4.</li>
        </ul>
      </section>

      <section class="mb-4" id="stats">
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
      </section>

      <section class="glass pad-2x mb-4 about-why-us" id="why-us">
        <h2 class="h4 fw-600 mb-3">Почему выбирают нас</h2>
        <ul class="mb-0">
          <li><strong>Собственные продукты</strong> — DigiTrack Confidential Computing и Big Data Platform, а не только консалтинг.</li>
          <li><strong>On-premise и 152-ФЗ</strong> — данные остаются у владельца, стек разворачивается в контуре заказчика.</li>
          <li><strong>Open source без vendor lock-in</strong> — Hadoop, Spark, Kafka; лицензия только за production-узлы BDP.</li>
          <li><strong>Экспертиза FL + Big Data</strong> — команда с опытом в ML, криптографии и платформенной инженерии.</li>
          <li><strong>Сопровождение после запуска</strong> — поддержка L3/L4, обновления и сопровождение дата-партнёров.</li>
        </ul>
      </section>

      <section class="mb-4" id="team">
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
      </section>

      <section class="glass pad-2x" id="join">
        <h2 class="h4 fw-600 mb-3">Присоединяйтесь к нам</h2>
        <p class="mb-3">Ищем ML-инженеров, backend- и platform-разработчиков, специалистов по информационной безопасности.</p>
        <p class="mb-0">
          <a href="vacancies.html" class="btn btn-primary-gy me-2 mb-2">Открытые вакансии</a>
          <a href="partnership.html" class="btn btn-outline-light mb-2">Стать партнёром</a>
          <a href="contacts.html" class="btn btn-outline-light mb-2">Связаться с нами</a>
        </p>
      </section>

      <p class="small mt-4 mb-0"><a href="voprosy.html">Вопросы и ответы →</a> · <a href="kak-my-rabotaem.html">Как мы работаем →</a> · <a href="contacts.html">Контакты →</a></p>
    </div>
  </main>"""


def contacts_body() -> str:
    return """
  <main class="py-6 contacts-page" style="padding-top: 7rem !important;">
    <div class="container">
      <h1 class="h2 fw-700 mb-2">Контакты</h1>
      <p class="snippet-answer mb-4">Свяжитесь с DigiTrack для коммерческих предложений, пилотов федеративного обучения и внедрения Big Data Platform.</p>

      <section class="mb-5" id="reach-us">
        <h2 class="h4 fw-600 mb-3">Свяжитесь с нами</h2>
        <div class="row g-4">
          <div class="col-12 col-md-6 col-lg-4">
            <div class="glass pad-2x h-100">
              <h3 class="h6 text-mute-400 mb-2">Телефон</h3>
              <p class="contact-phone mb-0"><a href="tel:+79857704512">+7 985 770-45-12</a></p>
            </div>
          </div>
          <div class="col-12 col-md-6 col-lg-4">
            <div class="glass pad-2x h-100">
              <h3 class="h6 text-mute-400 mb-2">Email</h3>
              <p class="contact-email mb-0"><a href="mailto:info@digi-track.ru">info@digi-track.ru</a></p>
            </div>
          </div>
          <div class="col-12 col-lg-4">
            <div class="glass pad-2x h-100">
              <h3 class="h6 text-mute-400 mb-2">График работы</h3>
              <p class="contact-hours mb-0">Пн–Пт: 10:00–19:00 (МСК)<br/>Сб–Вс: по договорённости</p>
            </div>
          </div>
        </div>
      </section>

      <section class="mb-5" id="address">
        <h2 class="h4 fw-600 mb-3">Адрес и реквизиты</h2>
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
            <p class="small mt-3 mb-0"><a href="about.html">О компании →</a> · <a href="voprosy.html">Вопросы и ответы →</a></p>
          </div>
          <div class="col-12 col-lg-6">
            <div class="contact-map rounded-3 overflow-hidden">
              <iframe src="https://yandex.ru/map-widget/v1/?ll=37.653400%2C55.732100&z=16&pt=37.653400%2C55.732100,pm2rdm" width="100%" height="360" frameborder="0" allowfullscreen="true" title="Офис DigiTrack на Яндекс.Картах" loading="lazy"></iframe>
            </div>
            <p class="small mt-2 mb-0"><a href="https://yandex.ru/maps/?pt=37.6534,55.7321&z=16&l=map" target="_blank" rel="noopener noreferrer">Открыть на Яндекс.Картах →</a></p>
          </div>
        </div>
      </section>

      <section class="mb-5" id="social">
        <h2 class="h4 fw-600 mb-3">Мы в соцсетях</h2>
        <ul class="list-inline contact-social mb-0">
          <li class="list-inline-item me-3"><a href="https://t.me/digitrack" rel="noopener noreferrer" target="_blank">Telegram</a></li>
          <li class="list-inline-item me-3"><a href="https://vk.com/digitrack" rel="noopener noreferrer" target="_blank">VK</a></li>
          <li class="list-inline-item me-3"><a href="https://www.youtube.com/@digitrack" rel="noopener noreferrer" target="_blank">YouTube</a></li>
          <li class="list-inline-item"><a href="https://www.linkedin.com/company/digitrack" rel="noopener noreferrer" target="_blank">LinkedIn</a></li>
        </ul>
      </section>

      <section class="mb-4" id="contact-form">
        <h2 class="h4 fw-600 mb-3">Напишите нам</h2>
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
      </section>
    </div>
  </main>

  <script>
  document.getElementById('contactForm').addEventListener('submit', function (e) {
    e.preventDefault();
    var name = document.getElementById('contactName').value.trim();
    var email = document.getElementById('contactEmail').value.trim();
    var message = document.getElementById('contactMessage').value.trim();
    var subject = encodeURIComponent('Заявка с сайта DigiTrack');
    var body = encodeURIComponent('Имя: ' + name + '\\nEmail: ' + email + '\\n\\n' + message);
    window.location.href = 'mailto:info@digi-track.ru?subject=' + subject + '&body=' + body;
  });
  </script>"""


def cta() -> str:
    return """
  <section class="contact-cta-bar py-4 border-top border-ink-700" aria-label="Связаться с нами">
    <div class="container">
      <p class="mb-0 snippet-answer"><strong>Остались вопросы?</strong> <a href="contacts.html">Свяжитесь с нами</a> — ответим в течение 1 рабочего дня.</p>
    </div>
  </section>"""


def main() -> None:
    about_schema = load_schema("about-schema.jsonld")
    contacts_schema = load_schema("contacts-schema.jsonld")

    about_html = (
        head(
            "О компании DigiTrack — федеративное обучение и платформы данных",
            "DigiTrack (ООО «ДТ»): миссия, компетенции FL и Big Data, команда разработчиков конфиденциальных вычислений on-premise.",
            "https://digi-track.ru/about.html",
            about_schema,
        )
        + "\n"
        + nav("about")
        + "\n"
        + breadcrumbs("О компании")
        + about_body()
        + cta()
        + footer()
        + "\n</body>\n</html>\n"
    )

    contacts_html = (
        head(
            "Контакты DigiTrack — телефон, email, адрес в Москве",
            "Контакты DigiTrack: +7 985 770-45-12, info@digi-track.ru, Москва, Шлюзовая наб. 8/1. Форма обратной связи и карта офиса.",
            "https://digi-track.ru/contacts.html",
            contacts_schema,
        )
        + "\n"
        + nav("contacts")
        + "\n"
        + breadcrumbs("Контакты")
        + contacts_body()
        + footer()
        + "\n</body>\n</html>\n"
    )

def main() -> None:
    from merge_company_page import main as merge_main

    merge_main()
    print("Delegated to merge_company_page.py (about + redirects)")


if __name__ == "__main__":
    main()
