# services/user_worker.py

import threading
import queue
from services.user_service import get_or_create_user

# File d'attente globale
user_queue = queue.Queue()

# Flag pour éviter de lancer plusieurs workers
_worker_started = False

known_users = set()
known_users_lock = threading.Lock()

def _worker():
    while True:
        username = user_queue.get()

        if username is None:
            break  # arrêt propre

        try:
            get_or_create_user(username)
        except Exception as e:
            print(f"[WORKER ERROR] {e}")

        finally:
            user_queue.task_done()


def start_worker():
    global _worker_started

    if _worker_started:
        return

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    _worker_started = True


def enqueue_user(username: str):
    with known_users_lock:
        if username in known_users:
            return
        known_users.add(username)

    user_queue.put(username)