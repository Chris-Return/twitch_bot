from .CommandInterpreter import CommandInterpreter
from constantes import constantes
import time
import random

class CartCommandInterpreter(CommandInterpreter):
    def __init__(self, cooldown=10):
        super().__init__(cooldown)
        self.activationCommand = "!cart"
        self.counter = 0
        self.actualTag = "MonsterHunter"

        self.cartPhrasesList = [
            "@{username} ouais il a l'habitude de cart, ça fait {counter} fois aujourd'hui.",
            "@{username} c'est le genre de mec qui rejoint ta quête pour la foirer. ça fait {counter} cart.",
            "@{username} j'te dis pas la chute de DPS là. On est à {counter} cart.",
            "@{username} c'est une dinguerie de mourir là dessus. Il a cart {counter} fois.",
            "Pour te dire la vérité @{username} il n'a jamais vraiment été bon sur ce jeu. ({counter} cart)",
            "@{username} quand tu cart {counter} fois dans la même journée il faut savoir se remettre en question.",
            "Si encore il faisait un effort @{username} j'dis pas... Mais bon ça fait {counter} cart.",
            "Au pire @"+constantes.CHANNEL_NAME+" tu peux lancer une game d'Animal Crossing... ({counter} cart)",
            "Bon ok en vrai @{username} ça peut arriver de cart {counter} fois sur un malentendu.",
            "@{username} y'a des gens qui savent jouer à Monster hunter, et puis y'a "+constantes.CHANNEL_NAME+" qui cart {counter} fois."
        ]

    def execute(self, username, message, twSock):
        self.counter += 1
        phrase = random.choice(self.cartPhrasesList)
        response = phrase.format(username=username, counter=self.counter)

        msg = (
            f"@{username} C'est tellement une catastrophe que je n'ai même plus envie de compter."
            if self.counter == 10
            else response
        )

        twSock.sendMessage(msg)
        self.last_used = time.time()