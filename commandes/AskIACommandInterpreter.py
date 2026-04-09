from .CommandInterpreter import CommandInterpreter
from services.message_service import get_global_last_messages
import random
import time

class AskIACommandInterpreter(CommandInterpreter):
    def __init__(self, gemini_bot, cooldown=10):
        super().__init__(cooldown)
        self.activationCommand = "cheffouhighbot"
        self.gemini_bot = gemini_bot

    def execute(self, username, message, twSock):
        print(username)
        if username not in ["ChrisReturn", "minmaj", "Zarakaih"]:
            return

        prompt_final = f"L'administrateur {username} a posé une question : {message}. Répond lui de façon bienveillante avec de vraies informations"

        try:
            response = self.gemini_bot.envoyer_message(prompt_final)
            
            if response:
                twSock.sendMessage(response)
                self.last_used = time.time()
                self.message_count = 0
                self.target_count = random.randint(100, 150)

        except Exception as e:
            print(f"Erreur lors du RandomBanter : {e}", flush=True)