from .CommandInterpreter import CommandInterpreter
import time

class ReveilCommandInterpreter(CommandInterpreter):
    def __init__(self, cooldown=10):
        super().__init__(cooldown)
        self.activationCommand = "!reveil"

    def execute(self, username, message, twSock):
        twSock.sendMessage("Hein quoi ? J'suis là moi ! @"+username)
        self.last_used = time.time()