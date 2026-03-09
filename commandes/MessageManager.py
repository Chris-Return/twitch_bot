from .AyaCommandInterpreter import AyaCommandInterpreter

class MessageManager:
    def __init__(self):
        self.interpreters = [AyaCommandInterpreter(cooldown=10)]

    def register_interpreter(self, interpreter):
        self.interpreters.append(interpreter)

    def propagation(self, username, message, twSock):
        for interpreter in self.interpreters:
            try:
                interpreter.execute(username, message, twSock)
            except Exception as e:
                print(f"Erreur dans l'interpreter {interpreter}: {e}")