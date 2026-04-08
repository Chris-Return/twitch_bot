from .CommandInterpreter import CommandInterpreter
import time
import random

class DanseCommandInterpreter(CommandInterpreter):
    def __init__(self, cooldown=100):
        super().__init__(cooldown)
        self.activationCommand = "chefsp1PomPon chefsp1PomPon chefsp1PomPon".lower()
        self.actualTag = ""

    def execute(self, username, message, twSock):
        if username in ["ChrisReturn", "minmaj", "Zarakaih"]:
            nombre_danse = random.randint(3, 8)
            message_danse = ("chefsp1PomPon " * nombre_danse).strip()
            twSock.sendMessage(message_danse)
            self.last_used = time.time()