import os
import json
from system.notion import get_done_items, update_reply_status
from system.smtp import send_email

class Agent:
    def __init__(self):
        base = os.path.dirname(__file__)

        # Загружаем конфиг
        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.rhythm = cfg.get("rhythm", 120)
        self.reply_template = cfg.get("reply_template", "")
        self.from_email = cfg.get("from_email", "")

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

    def build_reply(self, item):
        return self.reply_template.format(
            subject=item.get("subject", ""),
            body=item.get("body", "")
        )

    def run(self):
        print("[Responder] Проверяю задачи со статусом 'Done'...")

        items = get_done_items()

        if not items:
            print("[Responder] Нет задач для ответа.")
            return

        print(f"[Responder] Найдено задач: {len(items)}")

        for item in items:
            reply_text = self.build_reply(item)

            print(f"[Responder] Отправляю ответ для UID={item['uid']}")

            send_email(
                to=item["sender"],
                subject=f"Re: {item['subject']}",
                body=reply_text,
                from_email=self.from_email
            )

            update_reply_status(
                item_id=item["id"],
                status="Replied"
            )

        self.save_state()
        print("[Responder] Ответы отправлены.")
