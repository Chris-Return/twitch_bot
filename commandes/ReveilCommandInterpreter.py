from .CommandInterpreter import CommandInterpreter
import time

class ReveilCommandInterpreter(CommandInterpreter):
    def __init__(self, cooldown=10):
        super().__init__(cooldown)

    def execute(self, username, message, twSock):
        if "!reveil" in message.lower():
            if self.can_execute():
                twSock.sendMessage("Hein quoi ? J'suis là moi ! @"+username)
                self.last_used = time.time()