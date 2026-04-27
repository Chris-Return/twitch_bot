from .CommandInterpreter import CommandInterpreter
from constantes import constantes
import time
import random

class LurkCommandInterpreter(CommandInterpreter):
    def __init__(self, cooldown=3):
        super().__init__(cooldown)
        self.activationCommand = "!lurk"
        self.counter = 0
        self.actualTag = ""

        self.lurkPhrasesList = [
            "@{username} merci pour ton lurk !",
            "Reviens nous vite @{username} !",
            "Merci pour le soutient @{username} <3"
        ]

        self.ennemiPhrasesList = [
            "@{username} Prend ton temps pour revenir surtout...",
            "@{username} Alléluia il est parti.",
            "@{username} On va enfin pouvoir respirer.",
            "@{username} Nice, on t'aime mais a petites doses.",
            "@{username} Wouah j'adore la légèreté de la délivrance.",
            "@{username} Bisous mon Zara ! Pouah c'est tellement pas naturel que j'en ai des boutons.",
            "@{username} Disparaît engeance démoniaque. chefsp1MidFing",
            "@{username} Si le paradis existe, j'y suis !"
        ]

    def execute(self, username, message, twSock):
        phrases_source = self.ennemiPhrasesList if username == "Zarakaih" else self.lurkPhrasesList
        phrase = random.choice(phrases_source)
        response = phrase.format(username=username, counter=self.counter)
        twSock.sendMessage(response)
        self.last_used = time.time()