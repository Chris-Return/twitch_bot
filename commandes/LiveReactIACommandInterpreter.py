from .CommandInterpreter import CommandInterpreter
from services.message_service import get_global_last_messages
import random
import time

class LiveReactIACommandInterpreter(CommandInterpreter):
    def __init__(self, gemini_bot, cooldown=10):
        super().__init__(cooldown)
        self.activationCommand = ""
        self.gemini_bot = gemini_bot
        self.message_count = 0
        self.target_count = random.randint(70, 100)

    def execute(self, username, message, twSock):
        self.message_count += 1

        if self.message_count < self.target_count and "!livereact" not in message:
            return

        nb_messages_a_lire = min(self.message_count, 50)
        logs_chat = get_global_last_messages(nb_messages_a_lire)
        logs_chat.reverse()

        prompt_final = (
            f"CONTEXTE : Tu es un bot Twitch. Tu viens de lire les {nb_messages_a_lire} derniers messages. "
            "Interviens de manière spontanée pour commenter l'ambiance, te moquer gentiment d'un spectateur "
            "ou rebondir sur un sujet dont ils parlent.\n\n"
            "DERNIERS MESSAGES DU CHAT :\n"
            f"{' | '.join(logs_chat)}\n\n"
            "CONSIGNE : Réponds par une seule phrase courte et incisive."
        )

        try:
            pique = self.gemini_bot.envoyer_message(prompt_final, fallback=False)
            
            if pique:
                twSock.sendMessage(pique)
                self.last_used = time.time()
                self.message_count = 0
                self.target_count = random.randint(70, 100)

        except Exception as e:
            print(f"Erreur lors du RandomBanter : {e}", flush=True)