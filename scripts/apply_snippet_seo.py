#!/usr/bin/env python3
"""Apply CTR-oriented Title/Description and sync og/twitter meta."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Title — самый важный элемент сниппета.
# Google: 50–60 символов; Яндекс: до 70 символов.
TITLE_LEN_GOOGLE = (50, 60)
TITLE_LEN_YANDEX = 70

# Description — поддерживает title; влияет на CTR.
# Рекомендуемая длина: 140–155 символов.
DESC_LEN = (140, 155)

TITLES: dict[str, str] = {
    "index.html": "Федеративное обучение и Big Data on-premise — DigiTrack 2026",
    "federated-learning.html": "DigiTrack FL: федеративное обучение для банков — пилот 2 нед",
    "data-platform.html": "Big Data on-premise от 600 000 ₽ — Dev/Test бесплатно",
    "learning-types.html": "VFL и HFL: в чём разница — таблица из 5 критериев [2026]",
    "about.html": "DigiTrack: 12 FAQ, 7 этапов внедрения и контакты в Москве",
    "blog.html": "Блог DigiTrack: 15 статей о FL, Big Data и 152-ФЗ [2026]",
    "partnership.html": "Партнёрство в федеративном обучении: пилот за 6 месяцев",
    "vacancies.html": "Вакансии DigiTrack: разработка FL и Big Data on-premise",
    "site-map.html": "Карта сайта DigiTrack: продукты, блог, FAQ и контакты",
    "documents.html": "Документация DigiTrack FL: скачать после авторизации",
    "expert-review.html": "Экспертная проверка DigiTrack: стенд и материалы для оценки",
    "login.html": "Вход в документацию DigiTrack FL — Confidential Computing",
    "blog/articles/fl-guide.html": "Что такое FL: 7 принципов, риски и применение [Обзор]",
    "blog/articles/bdp-guide.html": "Big Data Platform: 6 компонентов стека и риски [Обзор]",
    "blog/articles/tco-big-data.html": "TCO Big Data: формула и 5 статей расходов за 3–5 лет [Обзор]",
    "blog/articles/vfl-or-hfl.html": "VFL или HFL для банков: антифрод, скоринг, PSI [Кейс]",
    "blog/articles/choose-bdp-15.html": "Как выбрать Big Data Platform: 15 критериеv для CIO",
    "blog/articles/confidential-computing-152.html": "152-ФЗ и федеративное обучение: AI без утечки ПДн [2026]",
    "blog/articles/fate-flower-nvflare.html": "FATE vs Flower vs NVFlare: 10 критериев выбора FL [2026]",
    "blog/articles/federated-xgboost-experiments.html": "Federated XGBoost vs эмбеддинги: что безопаснее [2026]",
    "blog/articles/fl-antifraud.html": "Антифрод банков на FL: общая модель без обмена данными",
    "blog/articles/fl-sandbox-or-embeddings.html": "Sandbox, эмбеддинги или FL: 3 пути без выгрузки ПДн",
    "blog/articles/homomorphic-encryption.html": "Гомоморфное шифрование в ML: когда работает, когда нет",
    "blog/articles/ai-ready-platform.html": "AI-ready платформа: 7 компонентов для корпоративного AI",
    "blog/articles/ha-big-data-platform.html": "Отказоустойчивая Big Data без простоя: HA и rolling restart",
    "blog/articles/opensource-enterprise.html": "Open Source Big Data: суверенитет стека для enterprise",
    "blog/articles/scale-to-federated.html": "Масштабирование Big Data: от 1 кластера до федерации [2026]",
}

DESCRIPTIONS: dict[str, str] = {
    "index.html": (
        "Два продукта on-premise для банков: FL без передачи ПДн и Big Data Platform до 1 ПБ+. "
        "Dev/Test бесплатно. Запросите демо — ответ за 1 рабочий день."
    ),
    "federated-learning.html": (
        "VFL, HFL и Federated XGBoost on-premise по 152-ФЗ: данные не покидают периметр, "
        "пилот за 1–2 недели. Оставьте заявку на КП — info@digi-track.ru"
    ),
    "data-platform.html": (
        "Hadoop, Spark, Kafka и Delta Lake on-premise: 1 ПБ+, zero downtime, 3 тарифа от 600 000 ₽. "
        "Dev/Test бесплатно. Запросите расчёт — info@digi-track.ru"
    ),
    "learning-types.html": (
        "Таблица из 5 критериев: когда HFL, когда VFL, схемы и определения. "
        "Кейс для банков — в отдельной статье. Консультация по FL — info@digi-track.ru"
    ),
    "about.html": (
        "12 ответов о FL и BDP, процесс из 7 шагов, реквизиты ООО «ДТ» в Москве. "
        "Задайте вопрос или запросите коммерческое предложение — info@digi-track.ru"
    ),
    "blog.html": (
        "15 экспертных статей: VFL/HFL, TCO, 152-ФЗ, on-premise AI и антифрод для банков. "
        "Выберите тему и перейдите к продукту DigiTrack — info@digi-track.ru"
    ),
    "partnership.html": (
        "Станьте дата-партнёром: совместные модели FL без обмена сырыми данными, "
        "пилот ~6 месяцев, revenue share. Для банков и телекома — info@digi-track.ru"
    ),
    "vacancies.html": (
        "Открытые вакансии в команде FL и Big Data: ML, backend, DevOps on-premise. "
        "Удалённая работа в РФ. Отклик на info@digi-track.ru с темой «Вакансия»."
    ),
    "site-map.html": (
        "Все URL digi-track.ru: продукты FL и BDP, 15 статей блога, FAQ, 7 этапов заказа "
        "и контакты ООО «ДТ» в Москве. Быстрая навигация по разделам."
    ),
    "documents.html": (
        "Руководство, инструкция по установке и описание функциональных характеристик DigiTrack FL. "
        "Доступ после авторизации — запрос пароля на info@digi-track.ru"
    ),
    "expert-review.html": (
        "Скачайте материалы для экспертной проверки DigiTrack FL: документация, демо-стенд "
        "и инструкция по развёртыванию. Запрос доступа — info@digi-track.ru"
    ),
    "login.html": (
        "Служебный вход к документации DigiTrack Confidential Computing. "
        "Пароль по запросу на info@digi-track.ru — доступ после согласования NDA с заказчиком."
    ),
    "blog/articles/fl-guide.html": (
        "7 принципов федеративного обучения без передачи ПДн: VFL, HFL, риски и применение в enterprise. "
        "Обзор без рекламы — внедрение на странице DigiTrack FL."
    ),
    "blog/articles/bdp-guide.html": (
        "6 компонентов enterprise BDP: Hadoop, Spark, Kafka, Delta Lake, governance и on-premise. "
        "Обзор архитектуры — тарифы и демо на странице продукта."
    ),
    "blog/articles/tco-big-data.html": (
        "Формула TCO за 3–5 лет: CapEx, OpEx, 5 переменных и чек-лист для CIO. "
        "Без цен в статье — тарифы на data-platform, расчёт по запросу info@digi-track.ru"
    ),
    "blog/articles/vfl-or-hfl.html": (
        "Когда VFL, когда HFL в банке: антифрод, скоринг, PSI и типичные ошибки выбора. "
        "Прикладной кейс финсектора — запросите пилот FL на info@digi-track.ru"
    ),
    "blog/articles/choose-bdp-15.html": (
        "15 критериев enterprise BDP: HA, Astra Linux, TCO, open source и zero downtime. "
        "Сравните чек-лист с DigiTrack — запросите демо на info@digi-track.ru"
    ),
    "blog/articles/confidential-computing-152.html": (
        "Как совместить AI и 152-ФЗ: Confidential Computing и FL on-premise, доказательство что ПДн "
        "не покидали контур. Разбор для юристов и CISO — читайте статью."
    ),
    "blog/articles/fate-flower-nvflare.html": (
        "Сравнение FATE, Flower, NVFlare и DigiTrack: 10 критериев для тендера, модель угроз "
        "и российский стек. Выберите фреймворк FL без сюрпризов на проде."
    ),
    "blog/articles/federated-xgboost-experiments.html": (
        "Эмбеддинги можно инвертировать — Federated XGBoost считает сплиты без исходных записей. "
        "Как поднять качество скоринга на партнёрских данных без утечки."
    ),
    "blog/articles/fl-antifraud.html": (
        "Банки учат общую антифрод-модель без обмена транзакциями: закрывают слепые зоны между участниками. "
        "Кейсы Swift и FedFraud — как внедрить FL в антифрод."
    ),
    "blog/articles/fl-sandbox-or-embeddings.html": (
        "Sandbox, эмбеддинги или FL: три юридических конструкта и три модели угроз. "
        "Сравнение для финансов и телекома — выберите компромисс права и качества модели."
    ),
    "blog/articles/homomorphic-encryption.html": (
        "HE считает на шифротексте без раскрытия данных: где работает в ML, где дорого, "
        "и почему не «вся модель под FHE». Практичный разбор для ИБ и data science."
    ),
    "blog/articles/ai-ready-platform.html": (
        "7 компонентов AI-ready контура: 1 ПБ+, Delta Lake, Spark/Python, Kafka, Airflow, Jupyter "
        "и zero downtime. Чек-лист инфраструктуры для корпоративного AI."
    ),
    "blog/articles/ha-big-data-platform.html": (
        "HA NameNode, YARN, Hive и Patroni + rolling restart с drain: прод на 40 узлах и 1 ПБ+ "
        "без окна простоя. Пошаговый разбор отказоустойчивой Big Data."
    ),
    "blog/articles/opensource-enterprise.html": (
        "Open Source в enterprise — суверенитет стека, Astra Linux и реестр российского ПО, "
        "а не только экономия на лицензиях. Big Data без vendor lock-in."
    ),
    "blog/articles/scale-to-federated.html": (
        "От одного кластера к федерации: scale-out Data Nodes, Delta Lake, HA, Ansible "
        "и rolling restart без простоя. Мост от Big Data к федеративному обучению."
    ),
}

# Fix typo in choose-bdp title if introduced
TITLES["blog/articles/choose-bdp-15.html"] = "Как выбрать Big Data Platform: 15 критериев для CIO"


def apply_title(path: Path, title: str) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    for prop in ("og:title", "twitter:title"):
        pat = rf'<meta property="{prop}" content="[^"]*"/>'
        if re.search(pat, html):
            html = re.sub(pat, f'<meta property="{prop}" content="{title}"/>', html, count=1)
    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def apply_description(path: Path, desc: str) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html
    if re.search(r'<meta name="description"', html):
        html = re.sub(
            r'<meta name="description" content="[^"]*"/>',
            f'<meta name="description" content="{desc}"/>',
            html,
            count=1,
        )
    else:
        html = html.replace(
            '<link rel="canonical"',
            f'<meta name="description" content="{desc}"/>\n  <link rel="canonical"',
            1,
        )
        if html == orig:
            html = html.replace(
                "<title>",
                f'<meta name="description" content="{desc}"/>\n  <title>',
                1,
            )
    for prop in ("og:description", "twitter:description"):
        pat = rf'<meta property="{prop}" content="[^"]*"/>'
        if re.search(pat, html):
            html = re.sub(pat, f'<meta property="{prop}" content="{desc}"/>', html, count=1)
    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def check_title_length(title: str) -> list[str]:
    n = len(title)
    warnings: list[str] = []
    lo, hi = TITLE_LEN_GOOGLE
    if n < lo:
        warnings.append(f"title short ({n}<{lo})")
    elif n > hi:
        warnings.append(f"title long for Google ({n}>{hi})")
    if n > TITLE_LEN_YANDEX:
        warnings.append(f"title exceeds Yandex ({n}>{TITLE_LEN_YANDEX})")
    return warnings


def check_desc_length(desc: str) -> list[str]:
    n = len(desc)
    warnings: list[str] = []
    lo, hi = DESC_LEN
    if n < lo:
        warnings.append(f"desc short ({n}<{lo})")
    elif n > hi:
        warnings.append(f"desc long ({n}>{hi})")
    return warnings


def main() -> None:
    pages = sorted(set(TITLES) | set(DESCRIPTIONS))
    report: dict[str, dict] = {}
    for rel in pages:
        path = ROOT / rel
        if not path.exists():
            continue
        entry: dict = {}
        if rel in TITLES:
            apply_title(path, TITLES[rel])
            entry["title"] = len(TITLES[rel])
            entry["title_warnings"] = check_title_length(TITLES[rel])
        if rel in DESCRIPTIONS:
            apply_description(path, DESCRIPTIONS[rel])
            entry["desc"] = len(DESCRIPTIONS[rel])
            entry["desc_warnings"] = check_desc_length(DESCRIPTIONS[rel])
        report[rel] = entry
    title_bad = [r for r, m in report.items() if m.get("title_warnings")]
    desc_bad = [r for r, m in report.items() if m.get("desc_warnings")]
    print(json.dumps({"pages": report, "title_issues": title_bad, "desc_issues": desc_bad}, ensure_ascii=False, indent=2))
    if title_bad or desc_bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
