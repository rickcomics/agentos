import threading
import time
import importlib
import json
import os
import signal
from system.config import load_env

# Глобальный флаг для остановки всех агентов
RUNNING = True

def stop_all(signum, frame):
    global RUNNING
    RUNNING = False
    print("\n[Runtime] Остановка системы...")

signal.signal(signal.SIGINT, stop_all)
signal.signal(signal.SIGTERM, stop_all)

def load_agent(agent_name):
    """
    Загружает агент как модуль:
    agents/<agent_name>/agent.py → класс Agent
    """
    module_path = f"agents.{agent_name}.agent"
    module = importlib.import_module(module_path)
    return module.Agent

def run_agent(agent_name):
    """
    Запускает агента в его ритме.
    """
    agent_class = load_agent(agent_name)
    agent = agent_class()

    print(f"[Runtime] Агент '{agent_name}' запущен. Ритм: {agent.rhythm} сек")

    while RUNNING:
        try:
            agent.run()
        except Exception as e:
            print(f"[Runtime] Ошибка в агенте '{agent_name}': {e}")

        time.sleep(agent.rhythm)

    print(f"[Runtime] Агент '{agent_name}' остановлен.")

def load_agents_list():
    """
    Читает список агентов из agents/ (каждая папка = агент).
    """
    agents_dir = "agents"
    agents = []

    for name in os.listdir(agents_dir):
        full = os.path.join(agents_dir, name)
        if os.path.isdir(full) and not name.startswith("__"):
            agents.append(name)

    return agents

def main():
    load_env()  # загружаем .env
    agents = load_agents_list()

    print("[Runtime] Найдены агенты:", agents)

    threads = []

    for agent_name in agents:
        t = threading.Thread(target=run_agent, args=(agent_name,), daemon=True)
        t.start()
        threads.append(t)

    print("[Runtime] Все агенты запущены.")

    # Ждём завершения
    while RUNNING:
        time.sleep(1)

    print("[Runtime] Ожидание завершения потоков...")
    for t in threads:
        t.join()

    print("[Runtime] Система остановлена.")

if __name__ == "__main__":
    main()
