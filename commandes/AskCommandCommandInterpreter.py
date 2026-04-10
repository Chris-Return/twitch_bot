from .CommandInterpreter import CommandInterpreter
import time

class AskCommandCommandInterpreter(CommandInterpreter):
    def __init__(self, cooldown=30):
        super().__init__(cooldown)
        self.activationCommand = "!commande"

    def execute(self, username, message, twSock):
        msg = "Tu peux utiliser les commandes suivantes : !aya (compteur de aya) !cart (compteur de morts)... Bon ok c'est pas fou, juste mentionne moi et demande moi c'que tu veux si t'es un habitué du stream."
        twSock.sendMessage(msg)
        self.last_used = time.time()