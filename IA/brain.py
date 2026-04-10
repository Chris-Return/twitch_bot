import re
from commandes.CommandInterpreter import CommandInterpreter
from services.user_service import get_user_level
from constantes import constantes

class IABrain(CommandInterpreter):
    def __init__(self, gemini_bot, cooldown=10):
        super().__init__(cooldown)
        self.activationCommand = "cheffouhighbot"
        self.gemini_bot = gemini_bot
        self.IAinterpreters = [

        ]

    def execute(self, username, message, twSock):
        user_role_level = get_user_level(username)
        if user_role_level < constantes.ROLE_LEVEL_VIP:
            return
        
        try:
            prompt = f"L'utilisateur {username} demande : {message}. Adresse toi directement au(x) concerné(s)."
            response = self.gemini_bot.envoyer_message(prompt)
            if not response:
                return
            
            print(f"Réponse de l'IA : {response}", flush=True)
            
            commands = re.findall(r'\[(\w+):\s*(.*?)\]', response)
            for command_name, command_args in commands:
                args = re.findall(r'"(.*?)"', command_args)
                for interpreter in self.IAinterpreters:
                    try:
                        if interpreter.activationCommand in command_name:
                            if user_role_level >= interpreter.requiredRoleLevel:
                                interpreter.execute(username, message, twSock, args)
                    except Exception as e:
                        print(f"Erreur dans l'interpreter {interpreter}: {e}", flush=True)

        except:
            print(f"Erreur lors de la récupération de message IABrain : {e}", flush=True)
