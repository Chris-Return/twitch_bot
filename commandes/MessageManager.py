from .AyaCommandInterpreter import AyaCommandInterpreter
from .CartCommandInterpreter import CartCommandInterpreter
from .ReveilCommandInterpreter import ReveilCommandInterpreter
from .LurkCommandInterpreter import LurkCommandInterpreter
from .DanseCommandInterpreter import DanseCommandInterpreter
from .AskCommandCommandInterpreter import AskCommandCommandInterpreter
from IA.ConversationHistory import twitch_history
from IA.brain import IABrain 
from IA.gemini import GeminiManager

class MessageManager:
    def __init__(self):
        self.gemini_bot = GeminiManager()
        self.interpreters = [AyaCommandInterpreter(cooldown=10),
                             CartCommandInterpreter(cooldown=10),
                             ReveilCommandInterpreter(cooldown=10),
                             LurkCommandInterpreter(cooldown=3),
                             DanseCommandInterpreter(cooldown=100),
                             AskCommandCommandInterpreter(cooldown=20),
                             IABrain(self.gemini_bot)]
        

    def register_interpreter(self, interpreter):
        self.interpreters.append(interpreter)

    def propagation(self, username, message, twSock):
        twitch_history.add_message(username, message)
        for interpreter in self.interpreters:
            interpreter.before_execute(twSock)
            try:
                if interpreter.activationCommand in message.lower():
                    if interpreter.can_execute():
                        interpreter.execute(username, message, twSock)

            except Exception as e:
                print(f"Erreur dans l'interpreter {interpreter}: {e}", flush=True)