import os
import json
from datetime import datetime, timezone
from system.notion import get_items_by_status, archive_item

class Agent:
    def __init__(self):
        base = os.path.dirname(__file__)

        # Загружаем конфиг
        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.rhythm = cfg.get("rhythm", 3600)
        self.archive_status = cfg.get("archive_status", "Replied")
        self.archive_to = cfg.get("archive_to", "Archived")

        # Загружаем состояние
        self.state_path = os.path.join(base, "state.json")
        if os.path.exists(self.state_path):
            with open(self.state_path, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = {"last_timestamp": 0}

    def save_state(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4)

    def run(self):
        print(f"[Archivist] Ищу задачи со статусом '{self.archive_status}'...")

        items = get_items_by_status(self.archive_status)

        if not items:
            print("[Archivist] Нет задач для архивации.")
            return

        print(f"[Archivist] Найдено задач: {len(items)}")

        for item in items:
            print(f"[Archivist] Архивирую UID={item['uid']}")

            archive_item(
                item_id=item["id"],
                new_status=self.archive_to,
                archived_at=datetime.now(timezone.utc).isoformat()
            )

        self.save_state()
        print("[Archivist] Архивация завершена.")
