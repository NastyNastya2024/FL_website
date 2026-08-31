"""Transform article HTML for AI search: direct answers, FAQ, schema helpers."""

from __future__ import annotations

import html
import json
import re
import unicodedata
from dataclasses import dataclass, field

SITE_URL = "https://digi-track.ru"
ORG = {
    "@type": "Organization",
    "name": "DigiTrack",
    "legalName": 'ООО "ДТ"',
    "url": SITE_URL,
    "email": "info@digi-track.ru",
}

SEMANTIC_KEYWORDS: dict[str, list[str]] = {
    "fl-guide": [
        "федеративное обучение",
        "Federated Learning",
        "FL",
        "обучение на распределённых данных",
        "децентрализованное обучение",
        "FedAvg",
        "Federated XGBoost",
        "SecureBoost",
        "гомоморфное шифрование",
        "VFL",
        "HFL",
        "152-ФЗ",
        "confidential computing",
    ],
    "vfl-or-hfl": [
        "VFL",
        "HFL",
        "вертикальное федеративное обучение",
        "горизонтальное федеративное обучение",
        "vfl что это",
        "cross-silo federated learning",
        "PSI",
        "FedAvg",
        "федеративное обучение",
    ],
    "confidential-computing-152": [
        "152-ФЗ",
        "GDPR",
        "confidential computing",
        "конфиденциальные вычисления",
        "федеративное обучение",
        "персональные данные",
        "privacy-preserving ML",
        "TEE",
    ],
    "fl-sandbox-or-embeddings": [
        "федеративное обучение",
        "data sandbox",
        "эмбеддинги",
        "партнёрский скоринг",
        "152-ФЗ",
        "privacy-preserving ML",
    ],
    "homomorphic-encryption": [
        "гомоморфное шифрование",
        "homomorphic encryption",
        "HE",
        "федеративное обучение",
        "SecureBoost",
        "FedAvg",
        "privacy-preserving ML",
    ],
    "federated-xgboost-experiments": [
        "Federated XGBoost",
        "SecureBoost",
        "XGBoost",
        "эмбеддинги",
        "градиентный бустинг",
        "федеративное обучение",
        "VFL",
    ],
    "fl-antifraud": [
        "федеративное обучение",
        "антифрод",
        "VFL",
        "мошенничество",
        "банковская безопасность",
        "champion-challenger",
    ],
    "fate-flower-nvflare": [
        "FATE",
        "Flower",
        "NVFlare",
        "фреймворк федеративного обучения",
        "федеративное обучение",
        "on-prem",
    ],
    "bdp-guide": [
        "Big Data Platform",
        "платформа данных",
        "Hadoop",
        "Spark",
        "Delta Lake",
        "MLOps",
        "DataOps",
        "data governance",
        "AI-ready",
    ],
    "tco-big-data": [
        "TCO",
        "Big Data",
        "стоимость владения",
        "Hadoop",
        "on-premise",
        "Astra Linux",
    ],
    "choose-bdp-15": [
        "Big Data Platform",
        "выбор платформы данных",
        "enterprise",
        "импортозамещение",
        "Astra Linux",
        "Delta Lake",
    ],
    "mlops-dataops": [
        "MLOps",
        "DataOps",
        "Airflow",
        "Delta Lake",
        "data governance",
        "промышленный AI",
    ],
    "ai-ready-platform": [
        "AI-ready",
        "платформа данных",
        "Spark",
        "Delta Lake",
        "Kafka",
        "корпоративный AI",
    ],
    "opensource-enterprise": [
        "open source",
        "цифровой суверенитет",
        "импортозамещение",
        "Astra Linux",
        "реестр российского ПО",
        "Hadoop",
    ],
    "scale-to-federated": [
        "масштабирование Big Data",
        "scale-out",
        "Delta Lake",
        "rolling restart",
        "Ansible",
        "HA",
    ],
    "ha-big-data-platform": [
        "отказоустойчивость",
        "Zero Downtime",
        "HA",
        "Hadoop",
        "rolling restart",
        "NameNode",
        "YARN",
    ],
}

AUTHORITY_LINKS: dict[str, list[tuple[str, str]]] = {
    "fl-guide": [
        ("152-ФЗ «О персональных данных»", "https://www.consultant.ru/document/cons_doc_LAW_61801/"),
        ("Google AI — Federated Learning", "https://ai.google/research/pubs/pub47559"),
    ],
    "confidential-computing-152": [
        ("152-ФЗ «О персональных данных»", "https://www.consultant.ru/document/cons_doc_LAW_61801/"),
        ("GDPR (EU)", "https://gdpr.eu/"),
    ],
    "vfl-or-hfl": [
        ("Cross-silo Federated Learning (arxiv)", "https://arxiv.org/abs/1902.04885"),
    ],
    "homomorphic-encryption": [
        ("Homomorphic Encryption (NIST overview)", "https://csrc.nist.gov/projects/homomorphic-encryption"),
    ],
    "bdp-guide": [
        ("Apache Hadoop", "https://hadoop.apache.org/"),
        ("Delta Lake", "https://delta.io/"),
    ],
    "opensource-enterprise": [
        ("Реестр российского ПО", "https://reestr.digital.gov.ru/"),
    ],
}


@dataclass
class OptimizeResult:
    html: str
    faq_items: list[dict[str, str]] = field(default_factory=list)
    howto: dict | None = None


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def slugify(text: str) -> str:
    text = strip_tags(text).lower()
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text[:80] or "section"


def first_sentence(text: str, limit: int = 320) -> str:
    plain = strip_tags(text)
    if not plain:
        return ""
    m = re.match(r"^(.+?[.!?])(?:\s+|$)", plain, re.S)
    sentence = m.group(1).strip() if m else plain[:limit].rstrip() + "…"
    return sentence[:limit]


WEAK_ANSWER_STARTERS = (
    "именно поэтому",
    "для сборки",
    "в промышленном",
    "однако ",
    "наружу ",
    "однозначного ответа нет",
    "на рынке доступны",
)

GENERIC_HEADINGS = {
    "суть метода",
    "пример из финансового сектора",
    "сильные стороны hfl",
    "слабые стороны hfl",
    "сильные стороны vfl",
    "слабые стороны vfl",
    "когда выбирать hfl",
    "когда выбирать vfl",
}

OFF_TOPIC_PATTERNS = (
    "качество любой модели машинного обучения",
    "качество модели зависит от объёма",
    "в 2026 году данные стали",
    "определяется не столько архитектурой",
    "именно поэтому",
    "рассматривают три варианта",
    "обычно рассматривают три",
)

WEAK_LEAD_PATTERNS = (
    "именно поэтому",
    "рассматривают три варианта",
    "классический пример — партнёрский скоринг",
    "режим федерации зависит от структуры данных",
)

QUESTION_STOPWORDS = {
    "почему", "как", "что", "какой", "какая", "какие", "зачем", "когда", "где",
    "или", "в", "чём", "чем", "для", "и", "а", "на", "по", "из", "от", "до",
    "не", "ли", "это", "такое", "нужен", "нужно", "устроена", "устроен", "тип",
    "режим", "подходит", "обучение", "обучения", "данных", "данные",
}


def section_plain_text(section_html: str) -> str:
    parts = re.findall(r"<p[^>]*>(.*?)</p>", section_html, re.S | re.I)
    return " ".join(strip_tags(part) for part in parts if strip_tags(part))


def question_keywords(question: str) -> set[str]:
    words = re.findall(r"[\w-]+", strip_tags(question).lower(), re.UNICODE)
    return {w for w in words if len(w) > 3 and w not in QUESTION_STOPWORDS}


def score_sentence(sentence: str, question: str) -> float:
    q_lower = strip_tags(question).lower()
    s_lower = sentence.lower()
    score = 0.0

    for pattern in OFF_TOPIC_PATTERNS:
        if pattern in s_lower:
            score -= 12

    if any(s_lower.startswith(prefix) for prefix in WEAK_ANSWER_STARTERS):
        score -= 8

    if "рассматривают три варианта" in s_lower or "рассматривают три подхода" in s_lower:
        score -= 12

    if s_lower.startswith("это позволяет"):
        score -= 6
        if "xgboost" in q_lower or "бустинг" in q_lower:
            score -= 8

    if q_lower.startswith("как ") and any(word in q_lower for word in ("обучать", "построить", "выбрать")):
        for marker in ("secureboost", "xgboost", "протокол", "федеративн", "fedavg", "алгоритм"):
            if marker in s_lower:
                score += 3
        if "secureboost" in s_lower and "xgboost" in q_lower:
            score += 8
        if "классический xgboost" in s_lower:
            score += 4
        if "запрещ" in s_lower or "невозмож" in s_lower:
            score += 2

    if q_lower.startswith("почему"):
        for marker in (
            "из-за", "невозмож", "нельзя", "запрещ", "изолиру",
            "152", "контур", "периметр", "тайн", "риск", "барьер",
        ):
            if marker in s_lower:
                score += 4
        if any(w in q_lower for w in ("заперт", "контур", "периметр", "изолир")):
            for marker in ("изолиру", "периметр", "контур", "инфраструктур", "владел"):
                if marker in s_lower:
                    score += 6
            if "data lake" in s_lower and "невозмож" in s_lower:
                score -= 2

    if q_lower.startswith("зачем"):
        for marker in ("необходим", "нужен", "нужны", "без ", "не будет", "треб"):
            if marker in s_lower:
                score += 3

    if q_lower.startswith("как ") and "выбрать" in q_lower:
        for marker in ("выбор", "критер", "определя", "зависит", "сценари", "сравн"):
            if marker in s_lower:
                score += 3
        for marker in ("дижитрек", "заслуживает", "особого внимания", "сбер", "stalactite"):
            if marker in s_lower:
                score -= 10

    if "разница" in q_lower or " или " in q_lower:
        for marker in ("применя", "когда", "подходит", "отлича", "режим"):
            if marker in s_lower:
                score += 2

    overlap = sum(1 for word in question_keywords(question) if word in s_lower)
    score += overlap * 2

    if "из-за" in s_lower or " потому что " in s_lower:
        score += 2

    if 55 <= len(sentence) <= 300:
        score += 1

    return score


def clean_direct_answer(sentence: str) -> str:
    sentence = re.sub(r"\s*\(статья по теме —.*?\)", "", sentence, flags=re.I).strip()
    sentence = re.sub(r"^(?:поэтому|именно поэтому)\s+", "", sentence, flags=re.I)
    sentence = re.sub(r"\s+", " ", sentence)
    if sentence and sentence[0].islower():
        sentence = sentence[0].upper() + sentence[1:]
    return sentence[:320]


def pick_direct_answer(section_html: str, question: str) -> tuple[str, str]:
    q_lower = strip_tags(question).lower()

    if re.search(r"\b(три|два|четыре|пять|15|10)\b", q_lower) or (
        " или " in q_lower and "?" in q_lower
    ):
        synth = synthesize_answer_from_list(section_html, question)
        if synth:
            return synth, synth

    if q_lower.startswith("как ") and "выбрать" in q_lower:
        synth = synthesize_answer_from_list(section_html, question)
        if synth:
            return synth, synth

    plain = section_plain_text(section_html)
    if not plain:
        return "", ""

    sentences = re.split(r"(?<=[.!?])\s+", plain)
    ranked: list[tuple[float, str]] = []
    for sentence in sentences:
        s = sentence.strip()
        if len(s) < 40:
            continue
        if s.endswith(":"):
            continue
        ranked.append((score_sentence(s, question), s))

    if ranked:
        ranked.sort(key=lambda item: item[0], reverse=True)
        best_score, best_sentence = ranked[0]
        if best_score >= 2:
            return clean_direct_answer(best_sentence), best_sentence

    synth = synthesize_answer_from_list(section_html, question)
    if synth:
        return synth, synth

    return "", ""


def remove_sentence_from_html(html_part: str, sentence: str) -> str:
    if not sentence:
        return html_part

    variants = [sentence]
    if not re.match(r"^(?:поэтому|именно поэтому)\s", sentence, re.I):
        variants.append(f"Поэтому {sentence[0].lower()}{sentence[1:]}" if sentence else sentence)

    def repl_paragraph(match: re.Match[str]) -> str:
        inner = strip_tags(match.group(1))
        updated = inner
        for variant in variants:
            if variant in updated:
                updated = updated.replace(variant, " ", 1)
        if updated == inner:
            return match.group(0)
        updated = re.sub(r"\s+", " ", updated).strip(" ,;—")
        if len(updated) < 25:
            return ""
        return f"<p>{html.escape(updated)}</p>"

    cleaned = re.sub(r"<p[^>]*>(.*?)</p>", repl_paragraph, html_part, flags=re.S | re.I)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def strip_off_topic_intro(html_part: str) -> str:
    """Remove generic intro sentences that do not answer the section question."""

    def repl_paragraph(match: re.Match[str]) -> str:
        inner = strip_tags(match.group(1))
        if not inner:
            return match.group(0)
        sentences = re.split(r"(?<=[.!?])\s+", inner)
        kept = [
            s for s in sentences
            if s.strip() and not any(p in s.lower() for p in OFF_TOPIC_PATTERNS)
        ]
        if not kept:
            return match.group(0)
        if len(kept) == len(sentences):
            return match.group(0)
        updated = " ".join(kept).strip()
        if len(updated) < 25:
            return ""
        return f"<p>{html.escape(updated)}</p>"

    return re.sub(r"<p[^>]*>(.*?)</p>", repl_paragraph, html_part, flags=re.S | re.I)


def heading_to_question(title: str) -> str:
    title = strip_tags(title).strip()
    if not title:
        return title
    if title.endswith("?"):
        return title

    lower = title.lower()

    if re.match(r"^(как|что|почему|когда|где|какой|какая|какие|зачем|сколько)\b", lower):
        return title.rstrip(".") + "?"

    if "— в чём разница" in lower or "— в чем разница" in lower:
        return title.rstrip(".") + "?"

    if lower.startswith("проблема:"):
        rest = title.split(":", 1)[1].strip().rstrip(".")
        return f"Почему {rest[0].lower() + rest[1:] if rest else rest}?"

    if lower.startswith("суть "):
        return f"В чём суть {title[5:].strip().rstrip('.')}?"

    if re.match(r"^[A-ZА-Я0-9]{2,} и [A-ZА-Я0-9]{2,}", title):
        left = title.split("—")[0].strip()
        return f"В чём разница между {left}?"

    if " — " in title:
        left, right = title.split(" — ", 1)
        right_lower = right.lower()
        if "подход" in right_lower or "метод" in right_lower:
            return f"Что такое {left.strip()}?"
        if "кейс" in right_lower:
            return f"Почему {left.strip().lower()} — {right.rstrip('.')}?"
        if "слой" in right_lower or "этап" in right_lower:
            return f"Зачем нужен {left.strip()}?"
        if "разница" in right_lower:
            return f"{left.strip()} — {right.rstrip('.')}?"
        return f"{left.strip()}: {right.rstrip('.')}?"

    if re.match(r"^(три|два|четыре|пять|шесть|15|10)\b", lower):
        if ":" in title:
            left, right = title.split(":", 1)
            return f"Какие {left.strip().lower()}: {right.strip().rstrip('.')}?"
        return title.rstrip(".") + "?"

    if " как " in lower and "кейс" in lower:
        return f"Почему {title.rstrip('.')}?"

    if ":" in title:
        left, right = title.split(":", 1)
        right = right.strip()
        if re.match(r"^как\b", right.lower()):
            return right.rstrip(".") + "?"
        return f"Как устроена {left.strip().lower()}?"

    if " или " in lower:
        return title.rstrip(".") + "?"

    if "таблица" in lower or "сравн" in lower:
        return title.rstrip(".") + "?"

    return title.rstrip(".") + "?"


def split_first_paragraph(section_html: str) -> tuple[str, str]:
    m = re.match(r"(\s*)(<p[^>]*>.*?</p>)(.*)", section_html, re.S | re.I)
    if not m:
        return "", section_html
    return m.group(2), m.group(1) + m.group(3)


def list_item_gist(item: str) -> str:
    item = item.strip()
    if not item:
        return ""
    if "—" in item:
        left, right = item.split("—", 1)
        label = left.strip()
        desc = right.strip()
        m = re.match(r"^(.+?[.!?])", desc)
        gist = (m.group(1) if m else desc[:90]).strip().rstrip(".")
        return f"{label} — {gist}"
    m = re.match(r"^(.+?[.!?])", item)
    return (m.group(1) if m else item[:120]).strip().rstrip(".")


def synthesize_answer_from_list(section_html: str, question: str = "") -> str:
    ul = re.search(r"<ul[^>]*>(.*?)</ul>", section_html, re.S | re.I)
    if not ul:
        return ""
    items = [strip_tags(item) for item in re.findall(r"<li[^>]*>(.*?)</li>", ul.group(1), re.S | re.I)]
    labels = []
    for item in items[:4]:
        if not item:
            continue
        label = item.split("—")[0].split("-")[0].strip()
        if label:
            labels.append(label)

    q_lower = question.lower()
    if len(labels) >= 2 and ("разница" in q_lower or ("hfl" in q_lower and "vfl" in q_lower)):
        parts = []
        for item in items[:2]:
            item = item.strip()
            if "—" in item:
                left, right = item.split("—", 1)
                desc = right.strip()
                m = re.match(r"^(.+?[.!?])", desc)
                desc_short = (m.group(1) if m else desc[:90]).strip().rstrip(".")
                parts.append(f"{left.strip()} — {desc_short}")
            else:
                m = re.match(r"^(.+?[.!?])", item)
                parts.append((m.group(1) if m else item[:120]).strip().rstrip("."))
        if len(parts) >= 2:
            if "федератив" not in q_lower and ("hfl" in q_lower or "vfl" in q_lower or "режим" in q_lower):
                return (
                    f"В федеративном обучении два режима: {parts[0]}; {parts[1]}."
                )
            return f"{parts[0]}; {parts[1]}."

    if len(labels) < 2:
        return ""
    if len(items) >= 3 and re.search(r"\bтри\b", q_lower):
        gists = [list_item_gist(item) for item in items[:3]]
        gists = [g for g in gists if g]
        if len(gists) == 3:
            return f"{gists[0]}; {gists[1]}; {gists[2]}."
    if q_lower.startswith("как ") and "выбрать" in q_lower and len(labels) >= 3:
        return (
            f"На рынке доступны фреймворки {labels[0]}, {labels[1]} и {labels[2]} — "
            f"выбор зависит от сценария (VFL/HFL), требований ИБ и инфраструктуры."
        )
    if len(labels) == 3:
        gists = [list_item_gist(item) for item in items[:3]]
        gists = [g for g in gists if g]
        if len(gists) == 3:
            return f"{gists[0]}; {gists[1]}; {gists[2]}."
        return f"Три подхода: {labels[0]}, {labels[1]} и {labels[2]}."
    return f"Ключевые варианты: {', '.join(labels)}."


def is_weak_lead_paragraph(paragraph_html: str) -> bool:
    text = strip_tags(paragraph_html).lower()
    return any(pattern in text for pattern in WEAK_LEAD_PATTERNS)


def inject_direct_answer(
    section_html: str,
    question: str,
    faq_items: list[dict[str, str]],
    *,
    add_to_faq: bool,
) -> str:
    if 'class="direct-answer"' in section_html:
        return section_html

    first_p, rest = split_first_paragraph(section_html)
    if not first_p and not rest.strip():
        return section_html

    display, raw = pick_direct_answer(section_html, question)
    if not display:
        synth = synthesize_answer_from_list(section_html, question)
        if synth:
            display, raw = synth, synth
    if not display:
        return section_html

    first_p = remove_sentence_from_html(first_p, raw) if first_p else ""
    rest = remove_sentence_from_html(rest, raw)
    if display != raw:
        first_p = remove_sentence_from_html(first_p, display) if first_p else first_p
        rest = remove_sentence_from_html(rest, display)
    first_p = strip_off_topic_intro(first_p)
    if first_p and is_weak_lead_paragraph(first_p):
        first_p = ""

    body_after = first_p

    direct = (
        f'<p class="direct-answer"><strong>Краткий ответ:</strong> '
        f"{html.escape(display)}</p>"
    )
    if add_to_faq and strip_tags(question).lower() not in GENERIC_HEADINGS:
        faq_items.append({"question": question, "answer": display})
    return direct + body_after + rest


def extract_howto(section_html: str, title: str) -> dict | None:
    ol = re.search(r"<ol[^>]*>(.*?)</ol>", section_html, re.S | re.I)
    if not ol:
        return None
    steps = re.findall(r"<li[^>]*>(.*?)</li>", ol.group(1), re.S | re.I)
    steps = [strip_tags(s) for s in steps if strip_tags(s)]
    if len(steps) < 3:
        return None
    if not re.match(r"^как\b", title.lower()):
        return None
    return {
        "@type": "HowTo",
        "name": title,
        "step": [
            {"@type": "HowToStep", "position": i + 1, "text": step}
            for i, step in enumerate(steps)
        ],
    }


def optimize_section(
    level: int,
    heading_html: str,
    body_html: str,
    faq_items: list[dict[str, str]],
    howto_holder: list[dict | None],
) -> str:
    question = heading_to_question(heading_html)
    anchor = slugify(question)
    tag = f"h{level}"
    out = f'<{tag} id="{anchor}">{html.escape(question)}</{tag}>'

    body = inject_direct_answer(body_html, question, faq_items, add_to_faq=(level == 2))
    if level == 2 and howto_holder[0] is None:
        howto = extract_howto(body, question)
        if howto:
            howto_holder[0] = howto

    return out + body


def optimize_body_html(body_html: str) -> OptimizeResult:
    faq_items: list[dict[str, str]] = []
    howto_holder: list[dict | None] = [None]

    tokens = re.split(r"(<h[23][^>]*>.*?</h[23]>)", body_html, flags=re.S | re.I)
    out: list[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        hm = re.match(r"<h([23])[^>]*>(.*?)</h\1>", token, re.S | re.I)
        if hm:
            level = int(hm.group(1))
            heading = hm.group(2)
            body = tokens[i + 1] if i + 1 < len(tokens) else ""
            out.append(
                optimize_section(level, heading, body, faq_items, howto_holder)
            )
            i += 2
            continue
        out.append(token)
        i += 1

    return OptimizeResult(html="".join(out), faq_items=faq_items, howto=howto_holder[0])


def build_faq_section(faq_items: list[dict[str, str]], limit: int = 8) -> str:
    items = faq_items[:limit]
    if len(items) < 2:
        return ""

    blocks = ['<section class="article-faq mt-5 pt-4 border-top" aria-labelledby="faq-heading">']
    blocks.append('<h2 id="faq-heading">Частые вопросы</h2>')
    blocks.append('<div class="faq-list">')
    for item in items:
        q = html.escape(item["question"])
        a = html.escape(item["answer"])
        blocks.append(
            f'<details class="faq-item">'
            f'<summary><h3 class="faq-question h6 mb-0">{q}</h3></summary>'
            f'<p class="faq-answer text-mute-300 mb-0 mt-2">{a}</p>'
            f"</details>"
        )
    blocks.append("</div></section>")
    return "".join(blocks)


def build_authority_section(slug: str) -> str:
    links = AUTHORITY_LINKS.get(slug, [])
    if not links:
        return ""
    lis = "".join(
        f'<li><a href="{html.escape(url)}" rel="noopener noreferrer" target="_blank">{html.escape(label)}</a></li>'
        for label, url in links
    )
    return (
        '<section class="article-sources mt-4 pt-3 border-top" aria-labelledby="sources-heading">'
        '<h2 id="sources-heading" class="h6 fw-600">Нормативная база и источники</h2>'
        f'<ul class="small text-mute-300 mb-0">{lis}</ul>'
        "</section>"
    )


def build_author_box(hub: str) -> str:
    product_link = (
        "../../federated-learning.html"
        if hub == "fl"
        else "../../data-platform.html"
    )
    product_name = (
        "DigiTrack Confidential Computing"
        if hub == "fl"
        else "Big Data Platform DigiTrack"
    )
    return (
        '<aside class="article-author mb-4" aria-label="Об авторе">'
        '<p class="small text-mute-300 mb-0">'
        "<strong>Экспертный материал DigiTrack</strong> — ООО «ДТ», разработчик "
        f'<a href="{product_link}">{product_name}</a>. '
        "Практический опыт внедрения on-premise в финансовом секторе и enterprise Big Data."
        "</p></aside>"
    )


def build_keywords_line(slug: str, hub: str, cluster: str) -> str:
    terms = SEMANTIC_KEYWORDS.get(slug, [])
    if hub == "fl" and "федеративное обучение" not in terms:
        terms = ["федеративное обучение", *terms]
    if hub == "bdp" and "платформа данных" not in terms:
        terms = ["платформа данных", "Big Data", *terms]
    if cluster and cluster not in terms:
        terms = [*terms, cluster.lower()]
    unique: list[str] = []
    seen: set[str] = set()
    for t in terms:
        key = t.lower()
        if key not in seen:
            seen.add(key)
            unique.append(t)
    joined = ", ".join(unique[:14])
    return (
        f'<p class="article-keywords small text-mute-400 mb-4">'
        f"<strong>По теме:</strong> {html.escape(joined)}</p>"
    )


def json_ld_script(data: dict) -> str:
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "</script>"
    )


def build_schema_graph(
    *,
    slug: str,
    title: str,
    description: str,
    hub: str,
    hub_label: str,
    faq_items: list[dict[str, str]],
    howto: dict | None,
) -> str:
    url = f"{SITE_URL}/blog/articles/{slug}.html"
    graph: list[dict] = []

    graph.append(
        {
            "@type": "Article",
            "@id": f"{url}#article",
            "headline": title,
            "description": description,
            "inLanguage": "ru-RU",
            "author": ORG,
            "publisher": {**ORG, "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/img/DataIcon.png"}},
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "about": SEMANTIC_KEYWORDS.get(slug, [hub_label])[:8],
        }
    )

    graph.append(
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{SITE_URL}/index.html"},
                {"@type": "ListItem", "position": 2, "name": "Блог", "item": f"{SITE_URL}/blog.html"},
                {"@type": "ListItem", "position": 3, "name": title, "item": url},
            ],
        }
    )

    if faq_items:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["question"],
                        "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
                    }
                    for item in faq_items[:8]
                ],
            }
        )

    if howto:
        howto = {**howto, "@id": f"{url}#howto"}
        graph.append(howto)

    payload = {"@context": "https://schema.org", "@graph": graph}
    return json_ld_script(payload)


def optimize_article_html(body_html: str, slug: str, hub: str, cluster: str) -> tuple[str, list[dict[str, str]], dict | None]:
    result = optimize_body_html(body_html)
    authority = build_authority_section(slug)
    optimized = result.html + authority
    return optimized, [], result.howto
