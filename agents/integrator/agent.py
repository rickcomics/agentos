import os
import json
from datetime import datetime, timezone
import requests
from system.notion import get_items_by_status, mark_integrated

class Agent:
    def __init__(self):
        base = os.path.dirname(__file__)

        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.rhythm = cfg.get("rhythm", 300)
        self.integrations = cfg.get("integrations", {})
        self.sync_status = cfg.get("sync_status", "Done")

        self.state_path = os.path.join(base, "state.json")
        if os.path.exists(self.state_path):
            with open(self.state_path, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = {"last_sync": 0}

    def save_state(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4)

    def sync_webhook(self, item):
        cfg = self.integrations.get("webhook", {})
        if not cfg.get("enabled"):
            return

        url = cfg.get("url")
        if not url:
            return

        payload = {
            "uid": item["uid"],
            "sender": item.get("sender"),
            "subject": item.get("subject"),
            "body": item.get("body"),
            "status": item.get("status"),
            "result": item.get("result"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        try:
            r = requests.post(url, json=payload, timeout=5)
            print(f"[Integrator] Webhook {item['uid']} → {r.status_code}")
        except Exception as e:
            print(f"[Integrator] Ошибка webhook: {e}")

    def run(self):
        print(f"[Integrator] Синхронизирую задачи со статусом '{self.sync_status}'...")

        items = get_items_by_status(self.sync_status)

        if not items:
            print("[Integrator] Нет задач для интеграции.")
            return

        print(f"[Integrator] Найдено задач: {len(items)}")

        for item in items:
            self.sync_webhook(item)
            # здесь позже можно добавить CRM, Trello, Jira и т.п.

            mark_integrated(item_id=item["id"])

        self.state["last_sync"] = datetime.now(timezone.utc).isoformat()
        self.save_state()

        print("[Integrator] Синхронизация завершена.")
