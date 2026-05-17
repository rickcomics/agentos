import os
import json
from system.notion import get_routed_items, update_item_result

class Agent:
    def __init__(self):
        base = os.path.dirname(__file__)

        # Загружаем конфиг
        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.rhythm = cfg.get("rhythm", 60)
        self.route_name = cfg.get("route_name", "worker_general")

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

    def process(self, item):
        """
        Здесь выполняется работа.
        Пока — заглушка.
        """
        print(f"[Worker] Выполняю задачу UID={item['uid']}")

        # Здесь будет логика обработки
        result = f"Задача UID={item['uid']} обработана."

        return result

    def run(self):
        print(f"[Worker] Проверяю задачи для маршрута '{self.route_name}'...")

        items = get_routed_items(self.route_name)

        if not items:
            print("[Worker] Нет задач для обработки.")
            return

        print(f"[Worker] Найдено задач: {len(items)}")

        for item in items:
            result = self.process(item)

            update_item_result(
                item_id=item["id"],
                result=result,
                status="Done"
            )

        self.save_state()
        print("[Worker] Обработка завершена.")
