from commandes.CommandInterpreter import CommandInterpreter
from IA.ConversationHistory import twitch_history
from constantes import constantes

class IASilence(CommandInterpreter):
    def __init__(self):
        self.requiredRoleLevel = constantes.ROLE_LEVEL_VIEWER
        self.activationCommand = "SILENCE"

    def execute(self, username, message, sock, list=None):
        pass