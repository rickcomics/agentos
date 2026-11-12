import os
import signal
from pathlib import Path


PID_FILE = Path(".agentos.pid")


def main():
    try:
        pid = int(PID_FILE.read_text(encoding="utf-8").strip())
        os.kill(pid, signal.SIGTERM)
        print("[Shutdown] Stop signal sent.")
    except FileNotFoundError:
        print("[Shutdown] No running AgentOS process found.")
    except ProcessLookupError:
        print("[Shutdown] Process already stopped.")
    except ValueError:
        print("[Shutdown] PID file is invalid.")
    except Exception as exc:
        print(f"[Shutdown] Failed to stop: {exc}")
    finally:
        try:
            PID_FILE.unlink(missing_ok=True)
        except Exception:
            pass


if __name__ == "__main__":
    main()
