from commandes.CommandInterpreter import CommandInterpreter
from constantes import constantes
from services.message_service import save_twitch_message
import re

class IASendMessage(CommandInterpreter):
    def __init__(self):
        super().__init__()
        self.required_role_level = constantes.ROLE_LEVEL_VIEWER_ASSIDU
        self.activationCommand="TALK"

    def execute(self, username: str, message: str, sock, list = None):
        save_twitch_message("CheffouHighBot", list[0], skip_user_check=False)
        sock.sendMessage(list[0])