import os
import json
from datetime import datetime, timezone
from system.notion import (
    count_items_by_status,
    get_processing_times,
    write_analytics_report
)

class Agent:
    def __init__(self):
        base = os.path.dirname(__file__)

        # Загружаем конфиг
        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.rhythm = cfg.get("rhythm", 1800)
        self.report_db = cfg.get("report_database", "ANALYTICS_DB")
        self.metrics = cfg.get("metrics", [])

        # Загружаем состояние
        self.state_path = os.path.join(base, "state.json")
        if os.path.exists(self.state_path):
            with open(self.state_path, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = {"last_report": 0}

    def save_state(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4)

    def run(self):
        print("[Analyst] Собираю метрики...")

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": {}
        }

        # Считаем задачи по статусам
        for status in ["New", "Routed", "Done", "Replied", "Archived"]:
            count = count_items_by_status(status)
            report["metrics"][status] = count

        # Время обработки
        processing_times = get_processing_times()
        report["processing_times"] = processing_times

        print("[Analyst] Пишу отчёт в Notion...")

        write_analytics_report(self.report_db, report)

        self.state["last_report"] = report["timestamp"]
        self.save_state()

        print("[Analyst] Отчёт создан.")
