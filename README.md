📘 README.md — AgentOS

Автономная компания, работающая без людей.
Модульная архитектура, ритмы, агенты, мосты, чистые функции.
Минимум зависимостей. Максимум устойчивости.

🧩 Содержание
Что такое AgentOS

- Архитектура
- Структура проекта
- Агенты
- Мосты (Bridges)
- API
- Сайт‑визитка
- Установка
- Настройка .env
- Notion схема
- Запуск
- Ритмы системы

🚀 Что такое AgentOS
AgentOS — это автономная компания, построенная на модульных агентах, которые:

- принимают входящие письма
- классифицируют задачи
- выполняют работу
- отвечают клиентам
- архивируют
- анализируют
- проверяют качество
- интегрируются с внешними системами

Каждый агент — независимый LEGO‑блок.
Каждый мост — чистая функция.
Каждый ритм — дыхание системы.

🧱 Архитектура

runtime.py        — дирижёр, запускает всех агентов
agents/           — независимые модули
system/           — мосты (Notion, IMAP, SMTP, LLM)
data/             — логи, кэш, глобальное состояние
api/              — внешний интерфейс
website/          — сайт‑визитка


🧩 Структура проекта

project/
│
├── runtime.py
├── shutdown.py
├── .env
│
├── agents/
│   ├── intake/
│   ├── filter/
│   ├── worker/
│   ├── responder/
│   ├── archivist/
│   ├── analyst/
│   ├── qa/
│   └── integrator/
│
├── system/
│   ├── imap.py
│   ├── smtp.py
│   ├── notion.py
│   ├── llm.py
│   ├── utils.py
│   └── config.py
│
├── api/
│   ├── server.py
│   └── routes/
│
└── website/


🤖 Агенты

Каждый агент — отдельный модуль с:

agent.py
config.json
state.json

Список агентов:

IntakeAgent — приём писем
FilterAgent — классификация и маршрутизация
WorkerAgent — выполнение задач
ResponderAgent — ответы клиентам
ArchivistAgent — архивирование
AnalystAgent — аналитика
QAAgent — контроль качества
IntegratorAgent — внешние интеграции

🌉 Мосты (Bridges)
Мосты — чистые функции, без логики:

IMAP — получение писем
SMTP — отправка писем
Notion — чтение/запись задач
LLM — локальная модель + fallback
Config — загрузка .env

🌐 API
Лёгкий FastAPI‑каркас:

/status — статус системы

/agents/start — запуск агентов

/agents/stop — остановка

/data/new — новые задачи

/data/routed/{route} — задачи по маршруту

Защита:

API‑ключ
CORS
rate‑limit

🖥 Сайт‑визитка
Статический сайт:

index.html
style.css
script.js

Функции:

- показывает статус системы
- отправляет заявки
- подключается к API

⚙️ Установка

git clone <repo>
cd project
pip install -r requirements.txt

Минимальные зависимости:

fastapi
requests

🔐 Настройка .env
Создай файл .env:

IMAP_HOST=
IMAP_USER=
IMAP_PASSWORD=

SMTP_HOST=
SMTP_PORT=465
SMTP_USER=
SMTP_PASSWORD=

NOTION_TOKEN=
NOTION_DATABASE=

ANALYTICS_DB=
QA_DB=

API_KEY=supersecret

🗂 Notion схема
Обязательные поля:

| Поле                  |  Тип            |
|-------------------    |-----------------|
| Email ID              | Title           |
| Sender                | Rich text       |
| Subject of the letter | Rich text       |         
| Summary               | Rich text       |
| Time of receipt       | Date            |
| Processing status     | Select          |
| Category              | Select          |
| Route                 | Rich text       |          
| Result                | Rich text       |          
| Reply                 | Rich text       |          
| Archived at           | Date            |
| Integrated            | Checkbox        |
|_______________________|_________________|

Processing status:

New
Routed
Done
Replied
Archived

▶️ Запуск

python runtime.py

🎵 Ритмы системы
Каждый агент живёт в своём ритме:

Intake — 10 сек
Filter — 30 сек
Worker — 1–5 мин
Responder — 2 мин
Archivist — 1 час
Analyst — 30 мин
QA — 10 мин
Integrator — 5 мин

🧠 Лицензия
MIT — система открыта, прозрачна, расширяема.




