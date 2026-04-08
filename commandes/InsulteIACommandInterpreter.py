from .CommandInterpreter import CommandInterpreter
from services.message_service import get_last_messages_from_db
import re

class InsulteIACommandInterpreter(CommandInterpreter):
    def __init__(self, gemini_bot, cooldown=30):
        super().__init__(cooldown)
        self.activationCommand = "!insulte"
        self.gemini_bot = gemini_bot

    def execute(self, username, message, twSock):
        match = re.search(r"!insulte\s+@?(\w+)", message)
        
        if match:
            cible = match.group(1)
        else:
            cible = username 

        messages_bdd = get_last_messages_from_db(cible, limit=40)
        messages_bdd.reverse()
        
        if not messages_bdd:
            prompt = f"L'utilisateur {username} veut que tu te moques de {cible}, mais {cible} n'a rien dit. Fais une vanne sur le fait qu'il est invisible ou muet."
        else:
            prompt = (
                f"L'utilisateur {username} demande une pique contre {cible}.\n"
                f"Voici les derniers messages de {cible} sur le chat :\n"
                f"{'- ' + '\n- '.join(messages_bdd)}\n\n"
                f"CONSIGNE : Génère une petite pique bien sentie en t'adressant directement à {cible}."
            )
        try:
            pique = self.gemini_bot.envoyer_message(prompt)
            if pique:
                twSock.sendMessage(f"@{username} {pique}")
                
        except Exception as e:
            print(f"Erreur lors de la commande !insulte : {e}")