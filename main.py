import signal
import select

from twitchsocket.TwitchSocket import TwitchSocket
from constantes import constantes
from commandes.MessageManager import MessageManager

from database.init_db import init_db
from database.seed import seed_roles
from sqlalchemy.orm import close_all_sessions

running = True

def shutdown_handler(signum, frame):
    global running
    print(f"Signal {signum} reçu, arrêt du bot...", flush=True)
    running = False


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


def main():
    init_db()
    print("Database initialized", flush=True)
    seed_roles()


def connect_to_twitch():
    global running

    twSock = TwitchSocket()
    sock = twSock.sock  # récupération du socket interne

    print(f"Connecté au chat de #{constantes.CHANNEL_NAME}", flush=True)

    messageManager = MessageManager()
    buffer = ""

    while running:
        try:
            ready, _, _ = select.select([sock], [], [], 1)

            if not ready:
                continue

            resp = twSock.getResp()
            buffer += resp

            lines = buffer.split("\r\n")
            buffer = lines.pop() 

            for line in lines:

                if not line:
                    continue

                if line.startswith("PING"):
                    twSock.sendPong()
                    continue

                if "Login authentication failed" in line:
                    print("ERREUR AUTHENTIFICATION", flush=True)

                if "PRIVMSG" in line:
                    try:
                        username = line.split("display-name=", 1)[1].split(";", 1)[0]
                        message = line.split("PRIVMSG", 1)[1].split(":", 1)[1]

                        messageManager.propagation(username, message, twSock)

                    except Exception as e:
                        print("Erreur parsing :", line, flush=True)
                        print("Exception :", e, flush=True)

                if "USERNOTICE" in line:
                    tags_part = line.split(" ", 1)[0]

                    tags = {
                        key: value
                        for key, value in (
                            tag.split("=", 1)
                            for tag in tags_part[1:].split(";")
                            if "=" in tag
                        )
                    }

                    if "msg-param-reward-id" in tags:
                        reward_id = tags["msg-param-reward-id"]
                        user_input = tags.get("msg-param-user-input", "")
                        username = tags.get("display-name", "Unknown")

                        print(
                            f"Channel Points déclenchés par {username}: reward {reward_id}, input: {user_input}",
                            flush=True,
                        )

                        # TODO: propager les rewards récupérés

        except Exception as e:
            print("Erreur dans la boucle principale :", e, flush=True)

    print("Fermeture du socket Twitch et des sessions SQLite...", flush=True)

    try:
        twSock.close()
    except Exception as e:
        print("Erreur fermeture socket :", e, flush=True)

    try:
        close_all_sessions()
    except Exception as e:
        print("Erreur fermeture sessions SQLite :", e, flush=True)

    print("Bot arrêté proprement", flush=True)


if __name__ == "__main__":
    main()
    connect_to_twitch()