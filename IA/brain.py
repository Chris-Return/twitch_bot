import re
from commandes.CommandInterpreter import CommandInterpreter
from services.user_service import get_user_level
from constantes import constantes
from .outils.IASendMessage import IASendMessage
from services.message_service import get_global_last_messages

class IABrain(CommandInterpreter):
    def __init__(self, gemini_bot, cooldown=10):
        super().__init__(cooldown)
        self.activationCommand = "cheffouhighbot"
        self.gemini_bot = gemini_bot
        self.IAinterpreters = [
            IASendMessage()
        ]

    def execute(self, username, message, twSock):
        user_role_level = get_user_level(username)
        if user_role_level < constantes.ROLE_LEVEL_VIP:
            return
        
        try:
            history_raw = get_global_last_messages(limit=40)
            history_context = "\n".join(reversed(history_raw))

            prompt = (
                f"Voici les derniers messages du chat :\n"
                f"{history_context}\n"
                f"--- \n"
                f"L'utilisateur {username} vient de dire : {message}. "
                f"Réponds-lui en tenant compte du contexte ci-dessus si nécessaire. "
                f"Adresse-toi directement au(x) concerné(s)."
            )

            response = self.gemini_bot.envoyer_message(prompt)
            if not response:
                return

            commands = re.findall(r'\[(\w+)[\s:]+(.*?)\]', response)
            for command_name, command_args in commands:
                args = re.findall(r'"(.*?)"', command_args)
                for interpreter in self.IAinterpreters:
                    try:
                        if interpreter.activationCommand.upper() in command_name.upper():
                            if user_role_level >= interpreter.requiredRoleLevel:
                                interpreter.execute(username, message, twSock, args)
                    except Exception as e:
                        print(f"Erreur dans l'interpreter {interpreter}: {e}", flush=True)

        except:
            print(f"Erreur lors de la récupération de message IABrain : {e}", flush=True)
