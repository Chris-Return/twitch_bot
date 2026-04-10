from .AyaCommandInterpreter import AyaCommandInterpreter
from .CartCommandInterpreter import CartCommandInterpreter
from .ReveilCommandInterpreter import ReveilCommandInterpreter
from .LurkCommandInterpreter import LurkCommandInterpreter
from .InsulteIACommandInterpreter import InsulteIACommandInterpreter
from .DanseCommandInterpreter import DanseCommandInterpreter
from .LiveReactIACommandInterpreter import LiveReactIACommandInterpreter
from IA.brain import IABrain 
from IA.gemini import GeminiManager

class MessageManager:
    def __init__(self):
        self.gemini_bot = GeminiManager()
        self.interpreters = [AyaCommandInterpreter(cooldown=10),
                             CartCommandInterpreter(cooldown=10),
                             ReveilCommandInterpreter(cooldown=10),
                             LurkCommandInterpreter(cooldown=3),
                             InsulteIACommandInterpreter(self.gemini_bot, cooldown=30),
                             DanseCommandInterpreter(cooldown=100),
                             LiveReactIACommandInterpreter(self.gemini_bot, cooldown=0),
                             IABrain(self.gemini_bot)]
        

    def register_interpreter(self, interpreter):
        self.interpreters.append(interpreter)

    def propagation(self, username, message, twSock):
        for interpreter in self.interpreters:
            try:
                if interpreter.activationCommand in message.lower():
                    if interpreter.can_execute():
                        interpreter.execute(username, message, twSock)
                    #else:
                     #   remaining = int(interpreter.cooldown - (time.time() - interpreter.last_used))
                      #  twSock.sendMessage(f"{interpreter.activationCommand} en cooldown ({remaining})s")
            except Exception as e:
                print(f"Erreur dans l'interpreter {interpreter}: {e}", flush=True)