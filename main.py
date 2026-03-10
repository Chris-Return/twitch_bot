from twitchsocket.TwitchSocket import TwitchSocket
from constantes import constantes
from commandes.MessageManager import MessageManager
from database.init_db import init_db
from database.seed import seed_roles


def main():
    init_db()
    print("Database initialized")
    seed_roles()


def connect_to_twitch():
    
    twSock = TwitchSocket()
    print(f"Connecte au chat de #{constantes.CHANNEL_NAME}")
    messageManager = MessageManager()
    buffer = ""

    while True:
        resp = twSock.getResp()
        buffer += resp

        # Découpe toutes les lignes reçues
        lines = buffer.split("\r\n")
        buffer = lines.pop()  # dernière ligne incomplète

        for line in lines:
            if not line:
                continue

            # Répondre aux PING
            if line.startswith("PING"):
                twSock.sendPong()
                continue

            # Auth échoue ?
            if "Login authentication failed" in line:
                print("ERREUR AUTHENTIFICATION")

            # Messages du chat
            if "PRIVMSG" in line:
                try:
                    username = line.split("display-name=",1)[1].split(";",1)[0]
                    message = line.split("PRIVMSG", 1)[1].split(":", 1)[1]
                    messageManager.propagation(username, message, twSock)

                except Exception as e:
                    print("Erreur parsing :", line)
                    print("Exception :", e)
            
            # Messages Channel Points
            if "USERNOTICE" in line:
                # La partie tags est avant le premier espace
                tags_part = line.split(" ", 1)[0]  # @badge-info=...
                tags = {}
                for tag in tags_part[1:].split(";"):  # enlever @ et découper
                    if "=" in tag:
                        key, value = tag.split("=", 1)
                        tags[key] = value

                # Vérifie si c'est une reward
                if "msg-param-reward-id" in tags:
                    reward_id = tags["msg-param-reward-id"]
                    user_input = tags.get("msg-param-user-input", "")
                    username = tags.get("display-name", "Unknown")
                    print(f"Channel Points déclenchés par {username}: reward {reward_id}, input: {user_input}")

                    #TODO : Préparer un propagationReward

if __name__ == "__main__":
    main()
    try:
        connect_to_twitch()  # ta boucle principale
    except KeyboardInterrupt:
        print("Arrêt du bot")
    finally:
        print("Fermeture des connexions")