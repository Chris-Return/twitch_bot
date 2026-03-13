from .AyaCommandInterpreter import AyaCommandInterpreter
from .CartCommandInterpreter import CartCommandInterpreter
from .ReveilCommandInterpreter import ReveilCommandInterpreter
import time

class MessageManager:
    def __init__(self):
        self.interpreters = [AyaCommandInterpreter(cooldown=10),
                             CartCommandInterpreter(cooldown=10),
                             ReveilCommandInterpreter(cooldown=10)]

    def register_interpreter(self, interpreter):
        self.interpreters.append(interpreter)

    def propagation(self, username, message, twSock):
        for interpreter in self.interpreters:
            try:
                if interpreter.activationCommand in message.lower():
                    if interpreter.can_execute():
                        interpreter.execute(username, message, twSock)
                    else:
                        remaining = int(interpreter.cooldown - (time.time() - interpreter.last_used))
                        twSock.sendMessage(f"{interpreter.activationCommand} en cooldown ({remaining})s")
            except Exception as e:
                print(f"Erreur dans l'interpreter {interpreter}: {e}")