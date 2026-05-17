import os
import json
from datetime import datetime, timezone
from system.notion import (
    get_all_items,
    write_qa_report
)

class Agent:
    def __init__(self):
        base = os.path.dirname(__file__)

        # Загружаем конфиг
        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.rhythm = cfg.get("rhythm", 600)
        self.qa_db = cfg.get("qa_database", "QA_DB")
        self.checks = cfg.get("checks", {})

        # Загружаем состояние
        self.state_path = os.path.join(base, "state.json")
        if os.path.exists(self.state_path):
            with open(self.state_path, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = {"last_check": 0}

    def save_state(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4)

    def run(self):
        print("[QA] Запускаю проверку качества...")

        items = get_all_items()

        issues = []

        for item in items:
            uid = item.get("uid")
            status = item.get("status")
            category = item.get("category")
            route = item.get("route")
            result = item.get("result")
            reply = item.get("reply")

            # Проверка маршрута
            if self.checks.get("missing_route") and not route:
                issues.append(f"UID={uid}: отсутствует Route")

            # Проверка категории
            if self.checks.get("missing_category") and not category:
                issues.append(f"UID={uid}: отсутствует Category")

            # Проверка результата
            if self.checks.get("empty_result") and status == "Done" and not result:
                issues.append(f"UID={uid}: статус Done, но Result пустой")

            # Проверка ответа
            if self.checks.get("reply_missing") and status == "Replied" and not reply:
                issues.append(f"UID={uid}: статус Replied, но письмо не зафиксировано")

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "issues": issues,
            "issues_count": len(issues)
        }

        print(f"[QA] Найдено проблем: {len(issues)}")

        write_qa_report(self.qa_db, report)

        self.state["last_check"] = report["timestamp"]
        self.save_state()

        print("[QA] Отчёт создан.")
