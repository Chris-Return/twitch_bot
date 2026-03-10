from .CommandInterpreter import CommandInterpreter
import time
import random

class AyaCommandInterpreter(CommandInterpreter):
    def __init__(self, cooldown=10):
        super().__init__(cooldown)
        self.counter = 0

        # Liste des phrases possibles
        self.ayaPhrasesList = [
            "@{username} Ayaaaa... Ça fait {counter} fois.",
            "@{username} c'est fou il ne sait pas se maîtriser, ça fait {counter} fois.",
            "@{username} Ayaaaaaaaa ! On est à {counter} fois.",
            "@{username} et un aya de plus... ({counter})",
            "@{username} on enchaine avec un aya de plus, ça fait {counter} fois.",
            "@{username} vas-y frère ça fait {counter} fois..."
        ]

    def execute(self, username, message, twSock):
        if "#r3set" in message.lower():
            self.counter = 0

        if "!aya" in message.lower():
            if self.can_execute():
                self.counter += 1

                # Choisit une phrase aléatoire
                phrase = random.choice(self.ayaPhrasesList)

                # Remplace les variables
                response = phrase.format(username=username, counter=self.counter)

                msg = (
                    f"{username} hey c'est bon j'en ai marre de compter maintenant zeubi."
                    if self.counter == 10
                    else response
                )

                twSock.sendMessage(msg)
                self.last_used = time.time()

            else:
                remaining = int(self.cooldown - (time.time() - self.last_used))
                response = f"Commande !aya est en cooldown de {remaining} seconde(s)"
                twSock.sendMessage(response)