from database.init_db import init_db
from database.seed import seed_roles
from services.signal_handlers import register_shutdown_signals
from twitchsocket.TwitchBot import connect_to_twitch
from workers.user_worker import start_worker

def main():
    init_db()
    print("Database initialized", flush=True)
    seed_roles()

if __name__ == "__main__":
    register_shutdown_signals()
    main()
    start_worker()
    connect_to_twitch()