# Статьи для сайта (из content_DT)

Источник: `/Users/a1/Documents/GitHub/content_DT`  
Критерий отбора: **`kind` = `Pillar` или `Cluster`** — материалы для публикации на сайте (hub + спицы).  
Исключены **`kind` = `Внешняя`** — статьи для Habr, VC.ru и других внешних площадок.

HTML-файлы лежат в `content_DT/articles/*.html`.

---

## Сводка

| Показатель | Значение |
|---|---:|
| Всего статей в content_DT | 29 |
| **Для сайта** (Pillar + Cluster) | **16** |
| Внешние (Habr / VC.ru и др.) | 13 |

---

## Тема 1: Федеративное обучение (FL)

**Pillar (хаб):** `fl-guide`

| Тип | Кластер | Slug | Заголовок | Файл |
|---|---|---|---|---|
| Pillar | Обзор | `fl-guide` | Федеративное обучение: как обучать модели на распределённых данных | `articles/fl-guide.html` |

**Cluster (спицы):**

| Кластер | Slug | Заголовок | Файл |
|---|---|---|---|
| Сравнение подходов | `fl-sandbox-or-embeddings` | Федеративное обучение, Sandbox или Эмбеддинги: архитектурный компромисс между правом и эффективностью | `articles/fl-sandbox-or-embeddings.html` |
| Безопасность и комплаенс | `confidential-computing-152` | Юридические барьеры 152-ФЗ, GDPR и архитектура безопасного AI на основе Confidential Computing и FL | `articles/confidential-computing-152.html` |
| Типы FL | `vfl-or-hfl` | VFL или HFL: какой тип федеративного обучения подходит для финансового сектора | `articles/vfl-or-hfl.html` |
| Сравнение с эмбеддингами | `federated-xgboost-experiments` | Federated XGBoost vs Эмбеддинги: почему бустинг побеждает, а векторы — рассекречиваются | `articles/federated-xgboost-experiments.html` |
| Шифрование и защита | `homomorphic-encryption` | Гомоморфное шифрование в машинном обучении: магия или инструмент? | `articles/homomorphic-encryption.html` |
| Антифрод | `fl-antifraud` | Федеративное обучение для антифрода: как банкам совместно находить мошеннические схемы | `articles/fl-antifraud.html` |
| Фреймворки | `fate-flower-nvflare` | FATE, Flower, NVFlare или Диджи Трек: какой фреймворк выбрать для федеративного обучения | `articles/fate-flower-nvflare.html` |

---

## Тема 2: Платформа данных (Big Data Platform)

**Pillar (хаб):** `bdp-guide`

| Тип | Кластер | Slug | Заголовок | Файл |
|---|---|---|---|---|
| Pillar | Обзор | `bdp-guide` | Big Data Platform: инфраструктура данных для AI и аналитики | `articles/bdp-guide.html` |

**Cluster (спицы):**

| Кластер | Slug | Заголовок | Файл |
|---|---|---|---|
| TCO и экономика | `tco-big-data` | Сколько стоит собственная платформа данных: считаем TCO Big Data-инфраструктуры | `articles/tco-big-data.html` |
| Выбор платформы | `choose-bdp-15` | Как выбрать Big Data Platform для крупного предприятия: 15 критериев оценки | `articles/choose-bdp-15.html` |
| MLOps/DataOps | `mlops-dataops` | MLOps начинается с DataOps: почему без управления данными нельзя построить промышленный AI | `articles/mlops-dataops.html` |
| Инфраструктура | `ai-ready-platform` | AI-ready Data Platform: какая инфраструктура нужна для корпоративного AI | `articles/ai-ready-platform.html` |
| Суверенитет и импортозамещение | `opensource-enterprise` | Open Source для Enterprise: почему открытый код становится вопросом цифрового суверенитета | `articles/opensource-enterprise.html` |
| Масштабирование | `scale-to-federated` | Как масштабировать Big Data-инфраструктуру от одного кластера до федеративной архитектуры | `articles/scale-to-federated.html` |
| Надёжность | `ha-big-data-platform` | Как построить отказоустойчивую Big Data-платформу без простоя | `articles/ha-big-data-platform.html` |

---

## Hub-and-Spoke (перелинковка)

```
federated-learning.html  ←→  fl-guide (Pillar)
    ├── fl-sandbox-or-embeddings
    ├── confidential-computing-152
    ├── vfl-or-hfl
    ├── federated-xgboost-experiments
    ├── homomorphic-encryption
    ├── fl-antifraud
    └── fate-flower-nvflare

data-platform.html  ←→  bdp-guide (Pillar)
    ├── tco-big-data
    ├── choose-bdp-15
    ├── mlops-dataops
    ├── ai-ready-platform
    ├── opensource-enterprise
    ├── scale-to-federated
    └── ha-big-data-platform
```

---

## Исключены (внешние, не для сайта)

| Slug | Заголовок | Площадки |
|---|---|---|
| `fl-what-is` | 152‑ФЗ и федеративное обучение: как законно использовать данные партнёров для AI | Habr, VC.ru |
| `fl-vs-centralized` | Федеративное обучение vs централизованный ML | Habr, VC.ru |
| `train-ai-multi-company` | Как обучать AI на данных нескольких компаний, не раскрывая исходные данные | Habr, VC.ru |
| `raise-scoring-accuracy` | Как повысить точность скоринговой модели на партнёрских данных | Habr, VC.ru |
| `federated-xgboost-how` | Federated XGBoost — бустинг без передачи исходных данных | Habr, VC.ru |
| `why-classic-xgboost-fails` | Почему классический XGBoost не работает в распределённой среде | Habr, VC.ru |
| `confidential-computing-partner` | Confidential Computing vs Федеративное обучение | Habr, VC.ru |
| `partner-scoring-quality` | Партнёрский скоринг: как повысить качество модели | Habr, VC.ru |
| `replace-data-lake` | Можно ли заменить централизованный Data Lake в партнёрском скоринге | Habr, VC.ru |
| `fl-uplift-cases` | Как федеративное обучение повышает аплифт модели на партнёрских данных | Habr, VC.ru |
| `big-data-2026` | Big Data в 2026 году: почему инфраструктура данных становится стратегическим активом | Habr, VC.ru |
| `eighty-percent-data` | Почему 80% успеха AI-проекта зависит от данных, а не от модели | Habr, VC.ru |
| `vendor-lock-in` | Vendor Lock-in: сколько бизнес платит за зависимость от IT-вендора | Habr, VC.ru |

---

## Связь с текущим сайтом FL_website

На сайте сейчас в блоге **6 статей** (`blog.html?article=1..6`) — это старый контент, не из content_DT.

16 статей из content_DT — **новый контент-план** для интеграции в блог или отдельные landing/cluster-страницы.
