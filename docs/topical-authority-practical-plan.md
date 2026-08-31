# Топикал-авторитет: практическое задание (пункты 2–6)

Документ — практическая реализация последних 5 шагов плана построения топикал-авторитета для сайта **DigiTrack** по двум темам:

1. **Федеративное обучение (FL)**
2. **Платформа данных (Data Platform)**

> Полное семантическое ядро (слова и подтемы) — в [`seo-semantic-content-plan-fl-ppml.md`](./seo-semantic-content-plan-fl-ppml.md).  
> Конкурентный анализ keys.so / Wordstat — в [`competitive-seo-fl-ppml-data-platform.md`](./competitive-seo-fl-ppml-data-platform.md).

---

## Пункт 2. Полная семантика по каждой теме

### Тема A: Федеративное обучение

| Подтема (кластер) | Ключевые запросы и вариации | Источник |
|---|---|---|
| **Определение / «что это»** | федеративное обучение это, federated learning, FL, федеративное обучение искусственный интеллект, федерализация данных | keys.so, Wordstat |
| **Типы FL** | горизонтальное/вертикальное FL, vfl что это, VFL, cross-silo, cross-device, federated learning в IoT | keys.so, сайт |
| **Алгоритмы и механика** | FedAvg, federated averaging, федеративное усреднение, обмен градиентами, глобальная/локальная модель, сервер агрегации | семантика + пробел |
| **Данные и устойчивость** | non-IID, неоднородные данные, data drift, дрейф данных, распределённая гетерогенность | семантика + пробел |
| **Безопасность в FL** | атаки инверсии градиентов, утечка обновлений, privacy-preserving, верификация обновлений | семантика + пробел |
| **Privacy-технологии (смежные)** | ppml, homomorphic encryption, полностью гомоморфное шифрование, дифференцированные данные, конфиденциальные вычисления | keys.so |
| **Transfer / fine-tuning** | federated transfer learning, federated fine-tuning, федеративный файнтюнинг | семантика |
| **Отраслевые сценарии** | FL в медицине, врачебная тайна, конфиденциальная медицинская информация, FL + LLM | keys.so, сайт |
| **Смежные ML-техники** | дистилляция модели, dataset distillation, distribution matching distillation, синтетические данные | keys.so |

### Тема B: Платформа данных

| Подтема (кластер) | Ключевые запросы и вариации | Источник |
|---|---|---|
| **Определение / позиционирование** | дата платформа (3 516), data platform, платформа данных, enterprise data platform, on-premise, big data platform | Wordstat, keys.so |
| **Стек / инфраструктура** | hadoop, hadoop скачать, greenplum, Vanilla Hadoop, Astra Linux, российский Hadoop, сервер авто | keys.so, сайт |
| **Эксплуатация / SRE** | SRE-практики, управление кластером, rolling restart, мультиверсионность Spark/Python | сайт (блог) |
| **Data governance** | data governance, управление данными, политика доступа, аудит, комплаенс | keys.so, пробел |
| **Data lineage** | data lineage, data lineage что это, дата линедж, сквозная прослеживаемость | keys.so, пробел |
| **Качество и надёжность** | надёжность данных, data quality, data reliability, потоки данных | keys.so, пробел |
| **Метаданные** | metadata, OpenMetadata, Data Quality | сайт |
| **Аббревиатуры / смежные термины** | дит, дит это, ADOM, fbp | keys.so |

---

## Пункт 3. Проверка покрытия: что есть и что отсутствует

### Тема A: Федеративное обучение

| Подтема | Есть на сайте | Где | Пробел (нет / слабо) |
|---|---|---|---|
| Определение FL | ✅ частично | `federated-learning.html`, `index.html` | Нет отдельной страницы под «федеративное обучение это» |
| Горизонтальное FL | ✅ | `federated-learning.html`, `blog.html?article=2`, `learning-types.html` | — |
| Вертикальное FL / VFL | ✅ частично | `blog.html?article=1` | Нет страницы под `vfl что это` |
| FL + AI | ⚠️ упоминание | `index.html` | Нет отдельного материала |
| FL в IoT | ❌ | — | Нет |
| Cross-silo / cross-device | ❌ | — | Нет |
| FedAvg / агрегация | ❌ | — | Нет |
| Non-IID / data drift | ❌ | — | Нет |
| Атаки инверсии градиентов | ❌ | — | Нет |
| PPML / HE / DP | ⚠️ упоминание | `index.html`, `partnership.html`, `federated-learning.html` | Нет deep-dive страниц |
| Конфиденциальные вычисления | ✅ | `blog.html?article=3` | — |
| Distillation / synthetic data | ❌ | — | Нет |
| Федерализация данных | ❌ | — | Нет |

**Итог по FL:** охват ~30–35% подтем. Сильные стороны — базовое FL и горизонтальное/вертикальное. Главные пробелы — алгоритмы, устойчивость данных, безопасность, VFL как термин, IoT/cross-*.

### Тема B: Платформа данных

| Подтема | Есть на сайте | Где | Пробел (нет / слабо) |
|---|---|---|---|
| Data platform (хаб) | ✅ | `data-platform.html` | — |
| Hadoop / on-prem / Astra Linux | ✅ | `data-platform.html`, `blog.html?article=6` | — |
| Greenplum | ✅ упоминание | `data-platform.html` | Нет отдельной статьи |
| SRE / rolling restart | ✅ | `blog.html?article=4` | — |
| Мультиверсионность | ✅ | `blog.html?article=5` | — |
| OpenMetadata / Data Quality | ✅ упоминание | `data-platform.html` | Нет deep-dive |
| Data governance | ❌ | — | Нет |
| Data lineage | ❌ | — | Нет |
| Надёжность данных | ❌ | — | Нет |
| Потоки данных | ❌ | — | Нет |
| Hadoop скачать / deployment | ⚠️ косвенно | блог про сборку | Нет FAQ/гайда |
| дит / дит это | ❌ | — | Нет |

**Итог по Data Platform:** охват ~45–50% подтем. Сильные стороны — продуктовая страница и инфраструктурный блог. Главные пробелы — governance, lineage, quality/reliability как отдельные сущности.

### Сводная матрица пробелов (приоритет для авторитета)

| Приоритет | Подтема | Тема | Частотность (если есть) | Статус |
|---|---|---|---|---|
| 🔴 P1 | Data lineage / data lineage что это | Data Platform | из keys.so | ❌ нет |
| 🔴 P1 | Data governance | Data Platform | из keys.so | ❌ нет |
| 🔴 P1 | федеративное обучение это / VFL | FL | из keys.so | ⚠️ слабо |
| 🔴 P1 | FedAvg / механика агрегации | FL | — | ❌ нет |
| 🟡 P2 | Надёжность данных / data quality | Data Platform | из keys.so | ❌ нет |
| 🟡 P2 | PPML / гомоморфное шифрование (deep-dive) | FL | ppml=30, HE=11 | ⚠️ упоминание |
| 🟡 P2 | Non-IID / data drift | FL | — | ❌ нет |
| 🟡 P2 | FL в IoT / cross-silo / cross-device | FL | — | ❌ нет |
| 🟢 P3 | Distillation / synthetic data | FL | из keys.so | ❌ нет |
| 🟢 P3 | Hadoop deployment / hadoop скачать | Data Platform | из keys.so | ⚠️ косвенно |
| 🟢 P3 | дит / дит это | Data Platform | из keys.so | ❌ нет |

---

## Пункт 4. Контентный план (закрытие пробелов)

### Фаза 1 — P1 (месяцы 1–2): закрыть критические пробелы

| # | Тип | Заголовок / URL (предложение) | Подтема | Ключевые запросы | Формат |
|---|---|---|---|---|---|
| 1 | Cluster | `/blog/data-lineage-chto-eto.html` | Data lineage | data lineage что это, data lineage, дата линедж | Статья 2000–3000 слов + FAQ |
| 2 | Cluster | `/blog/data-governance.html` | Data governance | data governance, управление данными | Статья 2500–3500 слов + схема |
| 3 | Cluster | `/blog/vfl-chto-eto.html` | VFL | vfl что это, вертикальное федеративное обучение | Статья 2000 слов + сравнение с HFL |
| 4 | Cluster | `/blog/federativnoe-obuchenie-eto.html` | Определение FL | федеративное обучение это, FL | Обзорная статья 3000+ слов |
| 5 | Cluster | `/blog/fedavg-algoritm.html` | FedAvg | FedAvg, federated averaging, федеративное усреднение | Техническая статья + диаграмма |

### Фаза 2 — P2 (месяцы 3–4): углубление

| # | Тип | Заголовок / URL (предложение) | Подтема | Ключевые запросы | Формат |
|---|---|---|---|---|---|
| 6 | Cluster | `/blog/nadezhnost-dannyh.html` | Data reliability | надёжность данных, data quality | Статья + чеклист |
| 7 | Cluster | `/blog/ppml-obzor.html` | PPML | ppml, privacy-preserving ML | Обзор + карта технологий |
| 8 | Cluster | `/blog/gomomorfnoe-shifrovanie.html` | HE | полностью гомоморфное шифрование, homomorphic encryption | Deep-dive |
| 9 | Cluster | `/blog/non-iid-data-drift-fl.html` | Устойчивость FL | non-IID, data drift, дрейф данных | Статья + кейсы |
| 10 | Cluster | `/blog/federated-learning-iot.html` | FL + IoT | federated learning IoT, cross-device | Статья + сценарии |

### Фаза 3 — P3 (месяцы 5–6): расширение охвата

| # | Тип | Заголовок / URL (предложение) | Подтема | Ключевые запросы | Формат |
|---|---|---|---|---|---|
| 11 | Cluster | `/blog/cross-silo-cross-device-fl.html` | Архитектуры FL | cross-silo, cross-device | Сравнительная статья |
| 12 | Cluster | `/blog/dataset-distillation.html` | Distillation | dataset distillation, дистилляция модели | Статья |
| 13 | Cluster | `/blog/hadoop-deployment-guide.html` | Hadoop deploy | hadoop скачать, развёртывание Hadoop | Гайд + FAQ |
| 14 | Cluster | `/blog/dit-departament-it.html` | ДИТ | дит, дит это | Объясняющая статья (если релевантно аудитории) |
| 15 | Update | `federated-learning.html` | FL hub | — | Добавить блоки: FedAvg, VFL, cross-*, FAQ |

### Обновление существующих страниц (не новые URL)

| Страница | Что добавить |
|---|---|
| `federated-learning.html` | H2 «VFL / HFL», H2 «FedAvg», FAQ (5–7 вопросов), ссылки на новые cluster-статьи |
| `data-platform.html` | H2 «Data governance», H2 «Data lineage», H2 «Надёжность данных», FAQ |
| `index.html` | 1–2 абзаца + ссылки на pillar/cluster по FL и Data Platform |
| `blog.html?article=1,2` | Добавить перелинковку на hub и новые статьи |

---

## Пункт 5. Внутренняя перелинковка (Hub and Spoke)

### Архитектура

```
                    ┌─────────────────────────┐
                    │   index.html (главная)  │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │                                   │
   ┌──────────▼──────────┐            ┌───────────▼──────────┐
   │  PILLAR (хаб) FL    │            │  PILLAR (хаб) Data   │
   │ federated-learning  │            │  data-platform.html  │
   │      .html          │            │                      │
   └──────────┬──────────┘            └───────────┬──────────┘
              │                                   │
    ┌─────────┼─────────┐               ┌─────────┼─────────┐
    │         │         │               │         │         │
 cluster   cluster   cluster         cluster   cluster   cluster
 VFL       FedAvg    PPML/HE         lineage   govern.   SRE/Hadoop
 IoT       non-IID   distillation    quality   deploy    Greenplum
```

### Таблица связей Hub ↔ Spoke

#### Хаб FL: `federated-learning.html`

| Cluster (спица) | Ссылка с хаба | Обратная ссылка на хаб | Анкор с хаба | Анкор обратно |
|---|---|---|---|---|
| Что такое FL | `/blog/federativnoe-obuchenie-eto.html` | ✅ | «Что такое федеративное обучение» | «Полное руководство по FL» |
| VFL | `/blog/vfl-chto-eto.html` | ✅ | «VFL — вертикальное FL» | «Федеративное обучение: обзор» |
| FedAvg | `/blog/fedavg-algoritm.html` | ✅ | «Алгоритм FedAvg» | «Все о федеративном обучении» |
| PPML | `/blog/ppml-obzor.html` | ✅ | «PPML и приватность в ML» | «FL и privacy» |
| Гомоморфное шифрование | `/blog/gomomorfnoe-shifrovanie.html` | ✅ | «Гомоморфное шифрование» | «FL + криптография» |
| Non-IID / drift | `/blog/non-iid-data-drift-fl.html` | ✅ | «Non-IID и дрейф данных» | «Проблемы FL» |
| FL в IoT | `/blog/federated-learning-iot.html` | ✅ | «FL в IoT» | «Федеративное обучение» |
| Cross-silo/device | `/blog/cross-silo-cross-device-fl.html` | ✅ | «Cross-silo и cross-device» | «Архитектуры FL» |
| Горизонтальное FL (есть) | `blog.html?article=2` | ✅ | «Горизонтальное FL» | «Обзор FL» |
| Вертикальное FL (есть) | `blog.html?article=1` | ✅ | «Вертикальное FL» | «Обзор FL» |
| Конфид. вычисления (есть) | `blog.html?article=3` | ✅ | «Конфиденциальные вычисления» | «FL и безопасность» |

#### Хаб Data Platform: `data-platform.html`

| Cluster (спица) | Ссылка с хаба | Обратная ссылка | Анкор с хаба | Анкор обратно |
|---|---|---|---|---|
| Data lineage | `/blog/data-lineage-chto-eto.html` | ✅ | «Data lineage — что это» | «Платформа данных» |
| Data governance | `/blog/data-governance.html` | ✅ | «Data governance» | «Enterprise data platform» |
| Надёжность данных | `/blog/nadezhnost-dannyh.html` | ✅ | «Надёжность данных» | «Data platform DigiTrack» |
| Hadoop deploy | `/blog/hadoop-deployment-guide.html` | ✅ | «Развёртывание Hadoop» | «On-premise платформа» |
| Rolling restart (есть) | `blog.html?article=4` | ✅ | «Rolling restart кластера» | «SRE-практики» |
| Мультиверсионность (есть) | `blog.html?article=5` | ✅ | «Мультиверсионность Spark/Python» | «Управление кластером» |
| Hadoop + Astra (есть) | `blog.html?article=6` | ✅ | «Российский Hadoop на Astra Linux» | «Платформа больших данных» |

### Правила перелинковки

1. **Хаб → все спицы:** на pillar-странице блок «Подробнее по теме» со ссылками на каждый cluster.
2. **Спица → хаб:** в начале и конце каждой статьи — ссылка «← Вернуться к обзору».
3. **Спица ↔ спица:** 1–2 контекстные ссылки между связанными cluster-статьями (например, VFL ↔ PPML, lineage ↔ governance).
4. **Главная → оба хаба:** явные CTA-блоки на `federated-learning.html` и `data-platform.html`.
5. **Блог → хабы:** каждая статья блога должна ссылаться на соответствующий pillar.
6. **Анкоры:** разнообразные, не «читать далее» — использовать ключевые слова из семантики.

---

## Пункт 6. План регулярного обновления контента

### Расписание обновлений

| Тип контента | Частота | Что делать | Пример |
|---|---|---|---|
| **Pillar-страницы** (хабы) | Каждые 3 месяца | Добавить новые cluster-ссылки, обновить FAQ, актуализировать цифры/версии стека | `data-platform.html`: обновить версию Hadoop, добавить ссылку на новую статью |
| **Cluster-статьи** (спицы) | Каждые 6 месяцев | Проверить актуальность, добавить новые примеры/кейсы, обновить дату публикации | `blog/fedavg-algoritm.html`: добавить ссылку на свежий research |
| **Блог (существующие)** | Каждые 6 месяцев | Перелинковка на новые материалы, мини-обновление текста | `blog.html?article=6`: ссылка на governance/lineage |
| **Семантика / keys.so** | Каждые 2 месяца | Проверить новые запросы, «потерянные» ключи, позиции | Экспорт keys.so → сверка с [`seo-semantic-content-plan-fl-ppml.md`](./seo-semantic-content-plan-fl-ppml.md) |
| **Wordstat** | Каждые 3 месяца | Обновить частотности по `дата платформа`, FL-кластерам | Сверка приоритетов контент-плана |
| **ИКС / видимость** | Ежемесячно | Яндекс.Вебмастер → ИКС, keys.so → видимость по темам | Отслеживать рост по FL и Data Platform |

### Чеклист ежеквартального аудита

- [ ] Все pillar-страницы ссылаются на актуальный набор cluster-статей
- [ ] Каждая cluster-статья ссылается обратно на pillar
- [ ] Нет «висячих» статей без перелинковки
- [ ] FAQ на pillar-страницах покрывает топ-5 запросов из keys.so
- [ ] Даты «Обновлено» проставлены на изменённых страницах
- [ ] Новые запросы из keys.so добавлены в семантическое ядро
- [ ] Пробелы из матрицы (пункт 3) закрыты или в работе
- [ ] ИКС не падает / растёт видимость по тематическим кластерам

### KPI топикал-авторитета (что отслеживать)

| Метрика | Инструмент | Базовая линия | Цель (6 мес.) |
|---|---|---|---|
| Запросов в топ-10 по FL | keys.so | ~10 (оценка) | 25+ |
| Запросов в топ-10 по Data Platform | keys.so | ~10 (оценка) | 30+ |
| Страниц в выдаче | keys.so | 12 | 30+ |
| Упоминания в ИИ-ответах Алисы | keys.so | 13 | 30+ |
| ИКС | Яндекс.Вебмастер | текущий | +20% |
| Внутренних ссылок hub↔spoke | ручной аудит | ~5 | 30+ |

---

## Следующий шаг

После утверждения URL-структуры из пункта 4 можно:

1. Написать тексты для P1-статей (5 штук) с готовой структурой H1/H2/FAQ.
2. Добавить блоки перелинковки на существующие `federated-learning.html` и `data-platform.html`.
3. Зафиксировать дату первого квартального аудита (пункт 6).
