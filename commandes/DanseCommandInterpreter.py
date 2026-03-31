from .CommandInterpreter import CommandInterpreter
import time

class DanseCommandInterpreter(CommandInterpreter):
    def __init__(self, cooldown=100):
        super().__init__(cooldown)
        self.activationCommand = "chefsp1PomPon chefsp1PomPon chefsp1PomPon".lower()
        self.actualTag = ""

    def execute(self, username, message, twSock):
        print("Passage dans Danse")
        print(username)
        if username in ["ChrisReturn", "minmaj", "Zarakaih"]:
            twSock.sendMessage("On s'ambiance ici zebi !")
            self.last_used = time.time()