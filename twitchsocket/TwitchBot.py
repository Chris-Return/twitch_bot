import os
import select
import time
from twitchsocket.TwitchSocket import TwitchSocket
from constantes import constantes
from commandes.MessageManager import MessageManager
from services.signal_handlers import running_flag
from twitchsocket.ShutdownBot import shutdown_bot
from workers.user_worker import enqueue_user

MAX_RUNTIME_MINUTES = int(os.getenv("MAX_RUNTIME_MINUTES", "300"))

def connect_to_twitch():
    twSock = TwitchSocket()
    sock = twSock.sock
    print(f"Connecté au chat de #{constantes.CHANNEL_NAME}", flush=True)

    messageManager = MessageManager()
    buffer = ""

    start_time = time.time()
    max_runtime_seconds = MAX_RUNTIME_MINUTES * 60

    while running_flag["running"]:
        if time.time() - start_time >= max_runtime_seconds:
            print(f"Temps maximum de {MAX_RUNTIME_MINUTES} minutes atteint, arrêt automatique...", flush=True)
            running_flag["running"] = False
            break

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
                        enqueue_user(username)
                        messageManager.propagation(username, message, twSock)
                    except Exception as e:
                        print("Erreur parsing :", line, flush=True)
                        print("Exception :", e, flush=True)

                if "USERNOTICE" in line:
                    tags_part = line.split(" ", 1)[0]
                    tags = {key: value for key, value in (tag.split("=", 1) for tag in tags_part[1:].split(";") if "=" in tag)}

                    if "msg-param-reward-id" in tags:
                        reward_id = tags["msg-param-reward-id"]
                        user_input = tags.get("msg-param-user-input", "")
                        username = tags.get("display-name", "Unknown")
                        print(f"Channel Points déclenchés par {username}: reward {reward_id}, input: {user_input}", flush=True)

        except Exception as e:
            print("Erreur dans la boucle principale :", e, flush=True)

    shutdown_bot(twSock)