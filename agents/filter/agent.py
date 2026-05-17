import os
import json
from system.notion import get_new_items, update_item

class Agent:
    def __init__(self):
        base = os.path.dirname(__file__)

        # Загружаем конфиг
        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.rhythm = cfg.get("rhythm", 30)
        self.routes = cfg.get("routes", {})
        self.keywords = cfg.get("keywords", {})

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

    def classify(self, text):
        text = text.lower()

        for category, words in self.keywords.items():
            for w in words:
                if w.lower() in text:
                    return category

        return "other"

    def run(self):
        print("[Filter] Проверяю новые записи...")

        items = get_new_items()

        if not items:
            print("[Filter] Новых задач нет.")
            return

        print(f"[Filter] Найдено новых задач: {len(items)}")

        for item in items:
            text = f"{item.get('subject', '')} {item.get('body', '')}"

            category = self.classify(text)
            route = self.routes.get(category, "worker_general")

            print(f"[Filter] → UID={item['uid']} → {category} → {route}")

            update_item(
                item_id=item["id"],
                category=category,
                route=route,
                status="Routed"
            )

        self.save_state()
        print("[Filter] Обработка завершена.")
