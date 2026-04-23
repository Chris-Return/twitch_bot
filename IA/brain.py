import re
import shlex
from commandes.CommandInterpreter import CommandInterpreter
from services.user_service import get_user_level, get_user_role
from services.useraffinity_service import get_user_affinity_context
from constantes import constantes
from .outils.IASendMessage import IASendMessage
from .outils.IASetRoleLevel import IASetRoleLevel
from .outils.IAAddAffinity import IAAddAffinity
from .outils.IAAddLove import IAAddLove
from .outils.IAAddRespect import IAAddRespect
from IA.ConversationHistory import twitch_history

class IABrain(CommandInterpreter):
    def __init__(self, gemini_bot, cooldown=10):
        super().__init__(cooldown)
        self.activationCommand = "cheffouhighbot"
        self.gemini_bot = gemini_bot
        self.IAinterpreters = [
            IASendMessage(),
            IASetRoleLevel(),
            IAAddRespect(),   
            IAAddAffinity(),   
            IAAddLove()
        ]

    def execute(self, username, message, twSock):
        user_role_level = get_user_level(username)
        user_role_name = get_user_role(username)

        if user_role_level < constantes.ROLE_LEVEL_VIEWER_ASSIDU:
            return
        
        try:
            history_context = twitch_history.get_context()
            twitch_history.clear()
            relation_context = get_user_affinity_context(username)

            prompt = (
                f"Contexte relationnel avec l'utilisateur {username} :\n"
                f"{relation_context}\n"
                f"Historique du chat :\n"
                f"{history_context}\n"
                f"--- \n"
                f"L'utilisateur {username} dispose du rôle {user_role_name} et vient de dire : {message}."
                f"Réponds-lui en tenant compte du contexte ci-dessus si nécessaire. "
                f"Adresse-toi directement au(x) concerné(s)."
            )

            response = self.gemini_bot.envoyer_message(prompt)
            print(f"prompt actuel :\n {prompt}", flush=True)
            print(f"Réponse de l'IA : {response}", flush=True)
            if not response:
                return

            commands = re.findall(r'\[(\w+)[\s:]+(.*?)\]', response)
            for command_name, command_args in commands:
                try:
                    clean_args_str = command_args.replace('“', '"').replace('”', '"')
                    args = shlex.split(clean_args_str)
                    
                except ValueError:
                    args = [command_args.strip('" ')]

                for interpreter in self.IAinterpreters:
                    if user_role_level >= interpreter.requiredRoleLevel and command_name == interpreter.activationCommand:
                        try:
                            interpreter.execute(username, message, twSock, args)
                        except Exception as e:
                            print(f"Erreur d'exécution dans {command_name}: {e}")

        except:
            print(f"Erreur lors de la récupération de message IABrain : {e}", flush=True)
