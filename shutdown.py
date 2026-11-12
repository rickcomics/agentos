import importlib
import os
import signal
import threading
import time
from pathlib import Path

from system.config import load_env

RUNNING = True
PID_FILE = Path(".agentos.pid")


def stop_all(signum, frame):
    global RUNNING
    RUNNING = False
    print("\n[Runtime] Stopping system...")


signal.signal(signal.SIGINT, stop_all)
signal.signal(signal.SIGTERM, stop_all)


def load_agent(agent_name: str):
    module_path = f"agents.{agent_name}.agent"
    module = importlib.import_module(module_path)
    return module.Agent


def load_agents_list():
    agents_dir = Path("agents")
    if not agents_dir.exists():
        return []

    agents = []
    for path in sorted(agents_dir.iterdir()):
        if path.is_dir() and not path.name.startswith("__"):
            agents.append(path.name)
    return agents


def run_agent(agent_name: str):
    try:
        agent_class = load_agent(agent_name)
        agent = agent_class()
        print(f"[Runtime] Agent '{agent_name}' started. Rhythm: {getattr(agent, 'rhythm', 10)}s")

        while RUNNING:
            try:
                agent.run()
            except Exception as exc:
                print(f"[Runtime] Agent '{agent_name}' error: {exc}")

            time.sleep(getattr(agent, 'rhythm', 10))

        print(f"[Runtime] Agent '{agent_name}' stopped.")
    except Exception as exc:
        print(f"[Runtime] Failed to load agent '{agent_name}': {exc}")


def main():
    load_env()
    agents = load_agents_list()
    print("[Runtime] Agents found:", agents)

    with PID_FILE.open("w", encoding="utf-8") as f:
        f.write(str(os.getpid()))

    threads = []
    for agent_name in agents:
        thread = threading.Thread(target=run_agent, args=(agent_name,), daemon=True)
        thread.start()
        threads.append(thread)

    print("[Runtime] All agents started.")

    while RUNNING:
        time.sleep(1)

    print("[Runtime] Waiting for threads to finish...")
    for thread in threads:
        thread.join()

    try:
        PID_FILE.unlink(missing_ok=True)
    except Exception:
        pass

    print("[Runtime] System stopped.")


if __name__ == "__main__":
    main()
