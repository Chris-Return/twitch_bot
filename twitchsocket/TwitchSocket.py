import socket
from constantes import constantes

class TwitchSocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((constantes.TWITCH_IRC_URL, constantes.TWITCH_IRC_PORT))

        # CAP REQ pour recevoir les tags et commandes
        self.sendLine("CAP REQ :twitch.tv/tags")
        self.sendLine("CAP REQ :twitch.tv/commands")

        # Authentification
        self.sendLine(f"PASS {constantes.TWITCH_OAUTH_TOKEN}")
        self.sendLine(f"NICK {constantes.TWITCH_USERNAME}")
        self.sendLine(f"JOIN #{constantes.CHANNEL_NAME}")

    def getResp(self):
        return self.sock.recv(2048).decode("utf-8", errors="ignore")

    def sendPong(self):
        self.sock.sendall("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

    def sendMessage(self, msg):
        line = f"PRIVMSG #{constantes.CHANNEL_NAME} :{msg}"
        self.sock.sendall((line + "\r\n").encode("utf-8"))

    def sendLine(self, line):
        self.sock.sendall(f"{line}\r\n".encode("utf-8"))