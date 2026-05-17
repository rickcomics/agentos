import os
import json
from system.imap import fetch_messages
from system.notion import write_page
from datetime import datetime, timezone

class Agent:
    def __init__(self):
        base = os.path.dirname(__file__)

        # Загружаем конфиг
        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.rhythm = cfg.get("rhythm", 10)
        self.mailbox = cfg.get("mailbox", "INBOX")
        self.batch_size = cfg.get("batch_size", 5)

        # Загружаем состояние
        state_path = os.path.join(base, "state.json")
        self.state_path = state_path

        if os.path.exists(state_path):
            with open(state_path, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = {"last_uid": 0}

    def save_state(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4)

    def run(self):
        print("[Intake] Проверяю почту...")

        last_uid = self.state.get("last_uid", 0)

        messages = fetch_messages(
            mailbox=self.mailbox,
            since_uid=last_uid,
            limit=self.batch_size
        )

        if not messages:
            print("[Intake] Новых писем нет.")
            return

        print(f"[Intake] Найдено новых писем: {len(messages)}")

        for uid, msg in messages:
            print(f"[Intake] Обрабатываю письмо UID={uid}")

            data = {
                "sender": msg.get("from"),
                "subject": msg.get("subject"),
                "body": msg.get("body"),
                "received_at": datetime.now(timezone.utc).isoformat(),
                "uid": uid
            }

            write_page(data)

            # Обновляем состояние
            self.state["last_uid"] = uid
            self.save_state()

        print("[Intake] Обработка завершена.")
