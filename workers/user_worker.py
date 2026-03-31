import threading
import queue
from services.message_service import save_twitch_message

user_queue = queue.Queue()
_worker_started = False

known_users = set()
known_users_lock = threading.Lock()

def _worker():
    while True:
        data = user_queue.get()
        if data is None:
            break
        
        try:
            save_twitch_message(
                data["username"], 
                data["content"], 
                skip_user_check=data["is_known"]
            )
        except Exception as e:
            print(f"[WORKER ERROR] {data['username']}: {e}")
        finally:
            user_queue.task_done()

def start_worker():
    global _worker_started
    if _worker_started:
        return
    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    _worker_started = True

def enqueue_message(username: str, content: str):
    is_known = False
    with known_users_lock:
        if username in known_users:
            is_known = True
        else:
            known_users.add(username)

    user_queue.put({
        "username": username,
        "content": content,
        "is_known": is_known
    })